from file_handling import JSON_File
from misc import log
import re

class Main():
    """
        Python-Main class
    """
    _instance = None

    @staticmethod
    def get():
        if Main._instance is None:
            Main._instance = Main()
        return Main._instance

    #######################################################

    def __init__(self):
        log("Constructing Bot")
        
        from bot import Bot

        self.bot = Bot()
        self.config = JSON_File("config/settings.json")
        self.igp = []

        @self.config.ee.on(JSON_File.EVENT_RELOAD)
        def _on_config_reload(cfg):
            self.igp = [re.compile(r) for r in cfg["ignore-pattern"]]

        self.config.reload()

    def run(self):
        self.bot.run(self.config["token"])
