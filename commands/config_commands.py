import discord
from discord import app_commands
from config.bot import bot
from config.config_manager import load_config, save_config
from components.ticket_view import TicketView

@bot.tree.command(name="configurar_canal", description="Configura un canal específico para una función")
@app_commands.describe(
    tipo="Tipo de canal a configurar",
    canal="El canal a configurar"
)
@app_commands.choices(tipo=[
    app_commands.Choice(name="Bienvenida", value="welcome"),
    app_commands.Choice(name="Tickets", value="tickets"),
    app_commands.Choice(name="Anuncios", value="announcements"),
    app_commands.Choice(name="Términos y Condiciones", value="terms")
])
@app_commands.checks.has_permissions(administrator=True)
async def configurar_canal(interaction: discord.Interaction, tipo: app_commands.Choice[str], canal: discord.TextChannel):
    config = load_config()
    
    if tipo.value == "welcome":
        config["welcome_channel"] = canal.id
        await interaction.response.send_message(f"✅ Canal de bienvenida configurado en {canal.mention}", ephemeral=True)
    elif tipo.value == "tickets":
        config["ticket_channel"] = canal.id
        # Crear mensaje de tickets con imagen
        view = TicketView()
        await canal.send(file=discord.File("assets/tickets.png"), view=view)
        await interaction.response.send_message(f"✅ Canal de tickets configurado en {canal.mention}", ephemeral=True)
    elif tipo.value == "announcements":
        config["announcements_channel"] = canal.id
        await interaction.response.send_message(f"✅ Canal de anuncios configurado en {canal.mention}", ephemeral=True)
    elif tipo.value == "terms":
        config["terms_channel"] = canal.id
        # Crear mensaje de términos y condiciones
        embed = discord.Embed(
            title="📜 Términos y Condiciones",
            description="Por favor, lee atentamente los siguientes términos y condiciones antes de realizar cualquier compra o solicitud de servicio.",
            color=discord.Color.blue()
        )
        
        # Sección de Servicios
        embed.add_field(
            name="📋 Servicios",
            value=(
                "• Los servicios se solicitarán mediante la creación de un ticket o siguiendo el proceso establecido en el servidor.\n"
                "• El cliente deberá proporcionar toda la información necesaria para completar su pedido de manera precisa y clara.\n"
                "• El equipo se reserva el derecho de rechazar solicitudes que no cumplan con los requisitos mínimos."
            ),
            inline=False
        )
        
        # Sección de Precios y Pagos
        embed.add_field(
            name="💰 Precios y Pagos",
            value=(
                "• Los precios estarán claramente especificados en el servidor o en el canal de ventas.\n"
                "• Todos los pagos deben realizarse mediante los métodos aceptados en el servidor. (Ko-Fi) \n"
                "• Los pagos contienen comisiones y son finales, no se emitirán reembolsos excepto en casos excepcionales.\n"
                "• Los servicios se iniciarán únicamente después de recibir el pago completo."
            ),
            inline=False
        )
        
        # Sección de Propiedad Intelectual
        embed.add_field(
            name="©️ Propiedad Intelectual",
            value=(
                "• Los pedidos (Mods, plugins, etc)son propiedad del cliente una vez completado el pago. Tanto el código fuente como el ejecutable.\n"
                "• El creador retiene los derechos de autor hasta recibir el pago completo.\n"
                "• El cliente no podrá revender, redistribuir o usar los trabajos de manera que infrinja los derechos del creador."
            ),
            inline=False
        )
        
        # Footer
        embed.set_footer(
            text="Al realizar una compra o solicitar un servicio, aceptas estos términos y condiciones."
        )
        
        await canal.send(embed=embed)
        await interaction.response.send_message(f"✅ Canal de términos y condiciones configurado en {canal.mention}", ephemeral=True)
    
    save_config(config)

@bot.tree.command(name="configurar_rol", description="Configura un rol para una función específica")
@app_commands.describe(
    tipo="Tipo de rol a configurar",
    rol="El rol a configurar"
)
@app_commands.choices(tipo=[
    app_commands.Choice(name="Staff", value="staff"),
    app_commands.Choice(name="Moderador", value="moderator"),
    app_commands.Choice(name="Soporte", value="support")
])
@app_commands.checks.has_permissions(administrator=True)
async def configurar_rol(interaction: discord.Interaction, tipo: app_commands.Choice[str], rol: discord.Role):
    config = load_config()
    
    if "roles" not in config:
        config["roles"] = {}
    
    config["roles"][tipo.value] = rol.id
    save_config(config)
    
    await interaction.response.send_message(f"✅ Rol {rol.mention} configurado como {tipo.name}", ephemeral=True)

@bot.tree.command(name="ver_config", description="Muestra la configuración actual del servidor")
@app_commands.checks.has_permissions(administrator=True)
async def ver_config(interaction: discord.Interaction):
    config = load_config()
    embed = discord.Embed(
        title="⚙️ Configuración del Servidor",
        color=discord.Color.blue()
    )
    
    # Canales
    channels_text = ""
    if config.get("welcome_channel"):
        channel = interaction.guild.get_channel(config["welcome_channel"])
        channels_text += f"👋 Bienvenida: {channel.mention if channel else 'No configurado'}\n"
    if config.get("ticket_channel"):
        channel = interaction.guild.get_channel(config["ticket_channel"])
        channels_text += f"🎫 Tickets: {channel.mention if channel else 'No configurado'}\n"
    if config.get("announcements_channel"):
        channel = interaction.guild.get_channel(config["announcements_channel"])
        channels_text += f"📢 Anuncios: {channel.mention if channel else 'No configurado'}\n"
    if config.get("terms_channel"):
        channel = interaction.guild.get_channel(config["terms_channel"])
        channels_text += f"📜 Términos: {channel.mention if channel else 'No configurado'}\n"
    
    embed.add_field(name="📌 Canales", value=channels_text or "No hay canales configurados", inline=False)
    
    # Roles
    if "roles" in config:
        roles_text = ""
        for role_type, role_id in config["roles"].items():
            role = interaction.guild.get_role(role_id)
            if role:
                roles_text += f"• {role_type.capitalize()}: {role.mention}\n"
        if roles_text:
            embed.add_field(name="👥 Roles", value=roles_text, inline=False)
    
    # Categorías de tickets
    if config.get("ticket_categories"):
        categories_text = ""
        for category_name, category_id in config["ticket_categories"].items():
            category = interaction.guild.get_channel(category_id)
            if category:
                categories_text += f"• {category_name}: {category.mention}\n"
        if categories_text:
            embed.add_field(name="🎫 Categorías de Tickets", value=categories_text, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True) 