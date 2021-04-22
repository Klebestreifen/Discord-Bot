from util import config
from classes.Bot import Bot

class Main:
    """
        Python-Main class
    """
    _instance = None

    @staticmethod
    def get():
        if Main._instance is None: Main._instance = Main()
        return Main._instance

    #######################################################

    def __init__(self):
        self.bot = Bot()

    def run(self):
        self.bot.run(config["token"])