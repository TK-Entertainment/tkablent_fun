from typing import *
import os, dotenv, sys

import discord
from discord.ext import commands
import atexit
import asyncio

print(f'''
Current Version
{sys.version}
''')

production = False

if production:
    prefix = '$'
    status = discord.Status.online
    production_status = 'ce' # ce for cutting edge, s for stable
    bot_version = f'20220825.3-{production_status}'
else:
    prefix = '%'
    status = discord.Status.dnd
    branch = 'master'
    bot_version = f'LOCAL DEVELOPMENT / {branch} Branch'

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, status=status)

from modules import *

precenses = [
    discord.Game(f'需要幫助? | {bot.command_prefix}help'),
    discord.Game(f'來點迷因? | {bot.command_prefix}meme'),
    discord.Game(f'來點幹話? | {bot.command_prefix}bullshit'),
    discord.Game(f'來點音樂? | {bot.command_prefix}play'),
]

async def precense_update():
    while True:
        for precense in precenses:
            await bot.change_presence(activity=precense)
            await asyncio.sleep(10)

# def on_exit():
    # cog: MusicCog = bot.cogs['MusicCog']

    # node: wavelink.Node = cog.playnode
    # for player in node.players:
    #     player.disconnect()
    # node.disconnect()

@bot.event
async def on_ready():
    bot.loop.create_task(precense_update())
    await bot.add_cog(RootCommands(bot, bot_version))
    await bot.tree.sync()

    # await cog.resolve_ui()

    # atexit.register(on_exit)
    print(f'''
        =========================================
        Codename TKablent | Version Alpha
        Copyright 2022-present @ TK Entertainment
        Shared under CC-NC-SS-4.0 license
        =========================================

        Discord Bot TOKEN | Vaild 有效

        If there is any problem, open an Issue with log
        else no any response or answer

        If there isn't any exception under this message,
        That means bot is online without any problem.
        若此訊息下方沒有任何錯誤訊息
        即代表此機器人已成功開機
    ''')

try:
    bot.run(TOKEN)
except AttributeError:
    print(f'''
    =========================================
    Codename TKablent | Version Alpha
    Copyright 2022-present @ TK Entertainment
    Shared under CC-NC-SS-4.0 license
    =========================================
    
    Discord Bot TOKEN | Invaild 無效

    我們在準備您的機器人時發生了一點問題
    We encountered some problem when the bot is getting ready
    
    似乎您提供在 .env 檔案中的 TOKEN 是無效的
    請確認您已在 .env 檔案中輸入有效且完整的 TOKEN
    It looks like your TOKEN is invaild
    Please make sure that your Discord Bot TOKEN is already in .env file
    and it's a VAILD TOKEN.
    ''')