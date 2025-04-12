import discord
from discord import app_commands
from config.bot import bot
from config.config_manager import load_config, save_config

@bot.tree.command(name="crear_categoria", description="Crea una nueva categoría para tickets")
@app_commands.describe(nombre_categoria="Nombre de la categoría a crear")
@app_commands.checks.has_permissions(administrator=True)
async def crear_categoria(interaction: discord.Interaction, nombre_categoria: str):
    config = load_config()
    if nombre_categoria in config['ticket_categories']:
        await interaction.response.send_message(f'La categoría {nombre_categoria} ya existe.', ephemeral=True)
        return
    
    category = await interaction.guild.create_category(nombre_categoria)
    config['ticket_categories'][nombre_categoria] = category.id
    save_config(config)
    
    await interaction.response.send_message(f'Categoría {nombre_categoria} creada exitosamente!', ephemeral=True)

@bot.tree.command(name="ticket", description="Crea un nuevo ticket")
@app_commands.describe(categoria="Categoría del ticket")
async def ticket(interaction: discord.Interaction, categoria: str):
    config = load_config()
    if categoria not in config['ticket_categories']:
        await interaction.response.send_message('Categoría no válida.', ephemeral=True)
        return
    
    category = interaction.guild.get_channel(config['ticket_categories'][categoria])
    ticket_channel = await interaction.guild.create_text_channel(
        f'ticket-{interaction.user.name}',
        category=category
    )
    
    await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
    
    await interaction.response.send_message(f'Ticket creado en {ticket_channel.mention}', ephemeral=True)
    await ticket_channel.send(f'{interaction.user.mention} Bienvenido a tu ticket!') 