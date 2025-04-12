import discord
from discord import ui
from config.bot import bot
from config.config_manager import load_config
import asyncio

class TicketSelect(ui.Select):
    def __init__(self):
        config = load_config()
        options = []
        
        for category_name in config.get('ticket_categories', {}).keys():
            options.append(discord.SelectOption(
                label=category_name,
                value=category_name
            ))
        
        super().__init__(
            placeholder="Selecciona una categoría de ticket",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_select"
        )

    async def callback(self, interaction: discord.Interaction):
        category_name = self.values[0]
        config = load_config()
        
        if category_name not in config['ticket_categories']:
            await interaction.response.send_message(
                "Esta categoría de ticket no está disponible actualmente.",
                ephemeral=True
            )
            return
        
        # Crear canal de ticket
        category = interaction.guild.get_channel(config['ticket_categories'][category_name])
        ticket_channel = await interaction.guild.create_text_channel(
            f'ticket-{interaction.user.name}',
            category=category
        )
        
        # Configurar permisos
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
        
        # Enviar mensaje de confirmación
        await interaction.response.send_message(
            f"Ticket creado en {ticket_channel.mention}",
            ephemeral=True
        )
        
        # Mensaje en el canal del ticket
        embed = discord.Embed(
            title="🎫 Ticket de Soporte",
            description=(
                f"Bienvenido {interaction.user.mention}!\n\n"
                "Por favor, describe tu consulta o problema.\n"
                "Un miembro del staff te atenderá pronto.\n\n"
                "Para cerrar el ticket, un administrador debe usar el comando `/cerrar_ticket`"
            ),
            color=discord.Color.blue()
        )
        
        # Añadir información del usuario
        embed.add_field(
            name="👤 Usuario",
            value=f"{interaction.user.mention} ({interaction.user})",
            inline=True
        )
        embed.add_field(
            name="📅 Fecha",
            value=interaction.created_at.strftime("%d/%m/%Y %H:%M"),
            inline=True
        )
        embed.add_field(
            name="📋 Categoría",
            value=category_name,
            inline=False
        )
        
        await ticket_channel.send(embed=embed)

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class CloseTicketButton(ui.Button):
    def __init__(self):
        super().__init__(
            label="Cerrar Ticket",
            style=discord.ButtonStyle.danger,
            custom_id="close_ticket"
        )

    async def callback(self, interaction: discord.Interaction):
        # Verificar permisos
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "No tienes permisos para cerrar tickets.",
                ephemeral=True
            )
            return
        
        # Enviar confirmación
        await interaction.response.send_message(
            "El ticket se cerrará en 5 segundos...",
            ephemeral=True
        )
        
        # Esperar 5 segundos
        await asyncio.sleep(5)
        
        # Eliminar el canal
        await interaction.channel.delete() 