from .meme import MemeUI
from .bullshit import BullshitUI

class UI(MemeUI, BullshitUI):
    def __init__(self, bot, bot_version):
        self.bot = bot
        self.bot_version = bot_version
        MemeUI().__init__()
        BullshitUI().__init__()