import discord
from discord import app_commands
from config.bot import bot
from config.config_manager import load_config

@bot.tree.command(name="info", description="Muestra información sobre JaviviDev y cómo comprar")
async def info(interaction: discord.Interaction):
    config = load_config()
    embed = discord.Embed(
        title="ℹ️ Información de JaviviDev",
        description="Bienvenido/a a nuestro servidor de mods y plugins de Minecraft!",
        color=discord.Color.blue()
    )
    
    # Información de compras
    embed.add_field(
        name="🛒 ¿Cómo comprar?",
        value=(
            "Para realizar una compra:\n"
            "1. Usa el comando `/ticket`\n"
            "2. Selecciona la categoría de tu producto\n"
            "3. Un miembro del staff te atenderá pronto"
        ),
        inline=False
    )
    
    # Redes sociales
    embed.add_field(
        name="🌐 Redes Sociales",
        value=(
            "• Twitter: [@JaviviDev](https://twitter.com/JaviviDev)\n"
            "• Ko-fi: [JaviviDev](https://ko-fi.com/javividev)\n"
            "• GitHub: [JaviviDev](https://github.com/JaviviDev)"
        ),
        inline=False
    )
    
    # Información adicional
    embed.add_field(
        name="📌 Información Adicional",
        value=(
            "• Todos nuestros productos son 100% originales\n"
            "• Soporte 24/7 para clientes\n"
            "• Actualizaciones gratuitas\n"
            "• Garantía de satisfacción"
        ),
        inline=False
    )
    
    # Footer con información del servidor
    embed.set_footer(
        text=f"Servidor: {interaction.guild.name}",
        icon_url=interaction.guild.icon.url if interaction.guild.icon else None
    )
    
    await interaction.response.send_message(embed=embed) 