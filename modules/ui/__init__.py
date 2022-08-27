from .meme import MemeUI

class UI(MemeUI):
    def __init__(self, bot, bot_version):
        self.bot = bot
        self.bot_version = bot_version
        MemeUI().__init__()