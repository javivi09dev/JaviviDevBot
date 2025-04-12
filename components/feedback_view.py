import discord
from discord import ui
from config.bot import bot
from config.config_manager import load_config

class FeedbackModal(ui.Modal, title="Feedback del Ticket"):
    rating = ui.TextInput(
        label="Calificación (1-5)",
        placeholder="Escribe un número del 1 al 5",
        required=True,
        min_length=1,
        max_length=1
    )
    
    comment = ui.TextInput(
        label="Comentario",
        placeholder="Escribe tu opinión sobre el servicio recibido",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            rating = int(self.rating.value)
            if not 1 <= rating <= 5:
                await interaction.response.send_message("La calificación debe ser un número entre 1 y 5.", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("La calificación debe ser un número válido.", ephemeral=True)
            return

        config = load_config()
        feedback_channel = bot.get_channel(config.get("feedback_channel"))
        
        if not feedback_channel:
            await interaction.response.send_message("El canal de feedback no está configurado.", ephemeral=True)
            return

        # Crear embed con el feedback
        embed = discord.Embed(
            title="📝 Nuevo Feedback",
            description=f"**Usuario:** {interaction.user.mention}\n**Calificación:** {'⭐' * rating}",
            color=discord.Color.gold()
        )
        embed.add_field(name="Comentario", value=self.comment.value, inline=False)
        
        await feedback_channel.send(embed=embed)
        await interaction.response.send_message("¡Gracias por tu feedback! Ha sido enviado correctamente.", ephemeral=True)

class FeedbackView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Enviar Feedback", style=discord.ButtonStyle.green, custom_id="feedback_button")
    async def feedback_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FeedbackModal()) 