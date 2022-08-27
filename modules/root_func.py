from typing import *

from discord.ext import commands
from discord import app_commands
import discord

import requests
import json
import random

from .command import Command
from .meme import Meme
from .bullshit import Bullshit

from .ui import UI

class RootCommands(commands.Cog):
    def __init__(self, bot, bot_version):
        super().__init__()
        self.bot = bot
        self.ui: UI = UI(bot, bot_version)

    async def meme(self, command: Union[commands.Context, discord.Interaction]):
        if not isinstance(command, Command):
            command: Optional[Command] = Command(command)
        await self.ui.SendMeme(command)

    @commands.command(name='meme')
    async def _c_meme(self, ctx: commands.Context):
        await self.meme(ctx)

    @app_commands.command(name='meme', description='找給我好笑的梗圖owo')
    async def _i_meme(self, interaction: discord.Interaction):
        await self.meme(interaction)