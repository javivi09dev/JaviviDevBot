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
from discord import app_commands

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
        print(f'Error al sincronizar comandos: {e}')

@bot.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Ocurrió un error: {str(error)}", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
