import requests
import random
import discord
from ..command import Command

from .misc import frame_photo_emoji, end_emoji, _generate_embed_option

class MemeUI:
    def _generate_meme_embed(self) -> discord.Embed:
        raw = requests.get('https://memes.tw/wtf/api')
        recommendation = raw.json()

        random_recommendation = random.choice(recommendation)

        embed = discord.Embed(
            title=random_recommendation['title'], 
            url=random_recommendation['url'])
        if random_recommendation['hashtag'] != "":        
            embed.add_field(name='Tags', value=random_recommendation['hashtag'], inline=True)
        embed.add_field(name='上傳時間', value=random_recommendation['created_at']['date_time_string'], inline=True)
        embed.set_author(name=f"此梗圖由 {random_recommendation['author']['name']} 上傳", icon_url="https://i.imgur.com/p4vHa3y.png")
        embed.set_image(url=random_recommendation['src'])
        
        embed = discord.Embed.from_dict(dict(**embed.to_dict(), **_generate_embed_option(self.bot, self.bot_version)))

        return embed

    async def SendMeme(self, command: Command):
        class MemeButton(discord.ui.View):

            _generate_meme_embed = self._generate_meme_embed

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
                embed = self._generate_meme_embed()
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

        embed = self._generate_meme_embed()
        view = MemeButton()
        msg = await command.send(embed=embed, view=view)

        if command.command_type == 'Interaction':
            msg = await command.original_response()