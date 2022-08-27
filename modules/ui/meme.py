import requests
import random
import discord
from ..command import Command

from ..generator import _generate_meme_embed
from .misc import frame_photo_emoji, end_emoji

class MemeUI:
    async def SendMeme(self, command: Command):
        class MemeButton(discord.ui.View):
            
            bot = self.bot
            bot_version = self.bot_version

            def __init__(self, *, timeout=60):
                super().__init__(timeout=60)

            @property
            def suggest_button(self):
                return self.children[0]

            @property
            def end_button(self):
                return self.children[1]

            def change_button_status(self, status: str):
                self.suggest_button.disabled = self.end_button.disabled = status == 'waiting'
                if status == 'waiting':
                    self.suggest_button.style = self.end_button.style = discord.ButtonStyle.gray
                else:
                    self.suggest_button.style = discord.ButtonStyle.blurple
                    self.end_button.style = discord.ButtonStyle.danger
                    
            @discord.ui.button(emoji=frame_photo_emoji, label="給我另一張梗圖", style=discord.ButtonStyle.blurple)
            async def regenerate_meme(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.change_button_status('waiting')
                await interaction.response.edit_message(
                    content=discord.PartialEmoji.from_str("<a:Loading:1011280276325924915>"), 
                    embed=None, view=view)
                embed = _generate_meme_embed(self.bot, self.bot_version)
                self.change_button_status('done')
                await interaction.edit_original_response(content=None, embed=embed, view=view)

            @discord.ui.button(emoji=end_emoji, style=discord.ButtonStyle.danger)
            async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.pong()
                await interaction.message.delete()
                self.stop()

            async def on_timeout(self):
                self.clear_items()
                await msg.edit(view=self)
                await msg.add_reaction('🛑')

        embed = _generate_meme_embed(self.bot, self.bot_version)
        view = MemeButton()
        msg = await command.send(embed=embed, view=view)

        if command.command_type == 'Interaction':
            msg = await command.original_response()