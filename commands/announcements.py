import discord
from discord import app_commands
from config.bot import bot

@bot.tree.command(name="anuncio", description="Crea un anuncio")
@app_commands.describe(mensaje="Contenido del anuncio")
@app_commands.checks.has_permissions(administrator=True)
async def anuncio(interaction: discord.Interaction, mensaje: str):
    embed = discord.Embed(
        title="📢 Anuncio Importante",
        description=mensaje,
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mensaje", description="Envía un mensaje personalizado")
@app_commands.describe(contenido="Contenido del mensaje")
@app_commands.checks.has_permissions(administrator=True)
async def mensaje(interaction: discord.Interaction, contenido: str):
    await interaction.response.send_message(contenido) 