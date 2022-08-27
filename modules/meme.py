from discord.ext import commands
from discord import app_commands
import discord

import requests
import random

from .command import Command

class Meme(commands.GroupCog):
    def __init__(self):
        super().__init__()

    async def category(self, command: Command, category: str):
        pass

    @commands.command(name='meme_category')
    async def _c_category(self, ctx: commands.Context, category: str):
        pass

    @app_commands.command(name='category', description='取得特定分類的梗圖')
    async def _i_category(self, interaction: discord.Interaction, category: str):
        pass