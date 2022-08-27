import discord
import random
import requests

from .ui.misc import _generate_embed_option

# This will be replaced with static file after testing
bullshit_database: dict = {}

def _generate_random_bullshit(bot, bot_version) -> discord.Embed:
    # if choice == 0, pick from public database api
    # if choice == 1, pick from user-provided database
    choice = random.randint(0, 1)
    if choice == 0 or (choice == 1 and len(bullshit_database) == 0):
        raw = requests.get('https://api.howtobullshit.me/bullshit')
        bullshit = raw.text.replace("Bad Request\n", "")
        bullshit = bullshit.replace("&nbsp;", "")
        bullshit = bullshit.replace("<br>", "\n")
        source = "幹話產生器"
        source_url = "https://howtobullshit.me/"
    else:
        bullshit = random.choice(bullshit_database.values())
        source = "使用此機器人的各位"
        source_url = None
    
    embed = discord.Embed(title="給你的一個至理名言 (幹話)", description=bullshit)
    embed.set_author(name=f"此幹話由 {source} 提供", icon_url="https://i.imgur.com/p4vHa3y.png", url=source_url)

    embed = discord.Embed.from_dict(dict(**embed.to_dict(), **_generate_embed_option(bot, bot_version)))

    return embed

def _generate_meme_embed(bot, bot_version) -> discord.Embed:
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
    
    embed = discord.Embed.from_dict(dict(**embed.to_dict(), **_generate_embed_option(bot, bot_version)))

    return embed