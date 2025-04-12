import discord
from discord import app_commands
from config.bot import bot
import asyncio
from components.feedback_view import FeedbackView

@bot.tree.command(name="cerrar_ticket", description="Cierra el ticket actual")
@app_commands.checks.has_permissions(administrator=True)
async def cerrar_ticket(interaction: discord.Interaction):
    # Verificar si estamos en un canal de ticket
    if not interaction.channel.name.startswith('ticket-'):
        await interaction.response.send_message(
            "Este comando solo puede usarse en canales de ticket.",
            ephemeral=True
        )
        return
    
    # Obtener el usuario que creó el ticket
    ticket_owner = None
    for member in interaction.channel.members:
        if not member.bot:
            ticket_owner = member
            break

    # Enviar mensaje de confirmación
    await interaction.response.send_message(
        "El ticket se cerrará en 5 segundos...",
        ephemeral=True
    )
    
    # Crear embed de cierre
    embed = discord.Embed(
        title="🎫 Ticket Cerrado",
        description=(
            f"Este ticket ha sido cerrado por {interaction.user.mention}\n"
            "El canal será eliminado en 5 segundos."
        ),
        color=discord.Color.red()
    )
    
    # Enviar mensaje de cierre
    await interaction.channel.send(embed=embed)
    
    # Enviar mensaje privado al usuario con el botón de feedback
    if ticket_owner:
        try:
            feedback_embed = discord.Embed(
                title="📝 Feedback del Ticket",
                description="¡Gracias por usar nuestro servicio! Por favor, tómate un momento para calificar tu experiencia.",
                color=discord.Color.green()
            )
            view = FeedbackView()
            await ticket_owner.send(embed=feedback_embed, view=view)
        except discord.Forbidden:
            pass  # El usuario tiene los mensajes privados desactivados

    # Esperar 5 segundos
    await asyncio.sleep(5)
    
    # Eliminar el canal
    await interaction.channel.delete() 