import discord
from ..command import Command

from .misc import queue_emoji, end_emoji
from ..generator import _generate_random_bullshit, bullshit_database

class BullshitUI:
    def __init__(self):
        pass

    async def SendBullshit(self, command: Command):
        class SubmitCreation(discord.ui.Modal):
            def __init__(self, submitter: discord.Member):
                submittertext = f"{submitter.name}#{submitter.discriminator}"
                self.submitpeople = discord.ui.TextInput(
                    custom_id="submitpeople",
                    label="提交者 (請勿更改，否則將無法正常提交)",
                    min_length=len(submittertext),
                    max_length=len(submittertext),
                    default=submittertext)

                self.bullshit_text = discord.ui.TextInput(
                    custom_id="bstext",
                    label="幹話",
                    placeholder=f"在此填入您的幹話")

                super().__init__(title="提交你的創意", timeout=120)

                for component in (self.submitpeople, self.bullshit_text):
                    self.add_item(component)

            async def on_submit(self, interaction):
                if self.submitpeople.value != f"{command.author.name}#{command.author.discriminator}":
                    await interaction.response.send_message(f"Expression Error!\nExpected Value: {command.author.name}#{command.author.discriminator}\nGot Value: {self.submitpeople.value}\n\nReturn Error: 請勿更改提交者，否則將無法正常提交。", ephemeral=True)
                    return

                bullshit_database.append(self.bullshit_text.value)
                await interaction.response.send_message(f"Expression Test Passed!\nExpected Value: {command.author.name}#{command.author.discriminator}\nGot Value: {self.submitpeople.value}\n\nReturn: 已收到您的創作!", ephemeral=True)

        class BullshitButton(discord.ui.View):

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
                    
            @discord.ui.button(emoji=queue_emoji, label="給我另一個幹話", style=discord.ButtonStyle.blurple)
            async def regenerate_meme(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.change_button_status('waiting')
                await interaction.response.edit_message(
                    content="<a:Loading:1011280276325924915> 幹話載入中...", 
                    embed=None, view=view)
                bullshit = _generate_random_bullshit(self.bot, self.bot_version)
                self.change_button_status('done')
                await interaction.edit_original_response(content=None, embed=bullshit, view=view)

            @discord.ui.button(label="提交幹話", style=discord.ButtonStyle.success)
            async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(SubmitCreation(interaction.user))

            @discord.ui.button(emoji=end_emoji, style=discord.ButtonStyle.danger)
            async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.pong()
                await interaction.message.delete()
                self.stop()

            async def on_timeout(self):
                self.clear_items()
                await msg.edit(view=self)
                await msg.add_reaction('🛑')

        bullshit = _generate_random_bullshit(self.bot, self.bot_version)
        view = BullshitButton()
        msg = await command.send(embed=bullshit, view=view)

        if command.command_type == 'Interaction':
            msg = await command.original_response()

    

