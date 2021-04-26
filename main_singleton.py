from file_handling import JSON_File
from misc import log
import re

class Main():
    """ Python-Main class """
    _instance = None

    @classmethod
    def i(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

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
        from bot_modules import load
        load()
        self.bot.run(self.config["token"])
