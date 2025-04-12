import discord
from config.bot import bot
import random

# Lista de mensajes de bienvenida
welcome_messages = [
    "¡Bienvenido/a {member.mention} a {guild.name}! 🎉",
]

@bot.event
async def on_member_join(member: discord.Member):
    # Obtener el canal de bienvenida (puedes configurarlo en config.json)
    welcome_channel = member.guild.system_channel
    
    if welcome_channel is not None:
        # Seleccionar un mensaje aleatorio
        welcome_message = random.choice(welcome_messages).format(member=member, guild=member.guild)
        
        # Crear embed de bienvenida
        embed = discord.Embed(
            title="👋 ¡Nuevo Miembro!",
            description=welcome_message,
            color=discord.Color.green()
        )
        
        # Añadir información adicional
        embed.add_field(
            name="📅 Fecha de unión",
            value=member.joined_at.strftime("%d/%m/%Y %H:%M"),
            inline=True
        )
        embed.add_field(
            name="👥 Miembros totales",
            value=member.guild.member_count,
            inline=True
        )
        
        # Añadir avatar del miembro
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Enviar mensaje de bienvenida
        await welcome_channel.send(embed=embed)
        
        # Enviar mensaje privado al nuevo miembro
        try:
            dm_embed = discord.Embed(
                title=f"¡Bienvenido/a a {member.guild.name}!",
                description=(
                    "¡Gracias por unirte a nuestro servidor! 🎉\n\n"
                    "Aquí encontrarás:\n"
                    "• Soporte para tus mods/plugins de Minecraft\n"
                    "• Una comunidad amigable\n"
                    "• Y mucho más...\n\n"
                    "Si necesitas ayuda, no dudes en preguntar. ¡Disfruta tu estancia!"
                ),
                color=discord.Color.blue()
            )
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            # Si no se pueden enviar mensajes privados, ignorar
            pass 