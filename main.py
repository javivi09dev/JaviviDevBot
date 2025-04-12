from config.bot import bot
import commands.tickets
import commands.announcements
import commands.config_commands
import commands.public_commands
import commands.ticket_commands
import events.server_events
from components.ticket_view import TicketView
from components.feedback_view import FeedbackView
import os
import sys
from discord import app_commands

# Configurar la codificación por defecto
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('------')
    try:
        # Registrar las vistas
        bot.add_view(TicketView())
        bot.add_view(FeedbackView())
        synced = await bot.tree.sync()
        print(f'Sincronizado {len(synced)} comandos')
    except Exception as e:
        print(f'Error al sincronizar comandos: {str(e)}', file=sys.stderr)

@bot.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
    else:
        error_msg = str(error)
        print(f"Error en comando: {error_msg}", file=sys.stderr)
        await interaction.response.send_message(f"Ocurrió un error: {error_msg}", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
