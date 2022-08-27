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
    def __init__(self, ui):
        super().__init__()
        self.ui: UI = ui

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

    async def bullshit(self, command: Union[commands.Context, discord.Interaction]):
        if not isinstance(command, Command):
            command: Optional[Command] = Command(command)
        await self.ui.SendBullshit(command)

    @commands.command(name='bullshit')
    async def _c_bullshit(self, ctx: commands.Context):
        await self.bullshit(ctx)

    @app_commands.command(name='bullshit', description='給我一句至理名言 (幹話)')
    async def _i_bullshit(self, interaction: discord.Interaction):
        await self.bullshit(interaction)