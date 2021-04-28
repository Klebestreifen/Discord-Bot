import re
from pymitter import EventEmitter

from file_handling import JSON_File
from misc import log

class Main():
    """ Python-Main class """
    _instance = None

    EVENT_RELOAD = "reload"

    @classmethod
    def i(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    #######################################################

    def __init__(self):
        log("Constructing Bot")
        
        from bot import Bot

        self.ee = EventEmitter()

        self.config = object() # __postinit
        self.igp = []          # __postinit

        self.bot = Bot()

        self.__pi_done = False

    def reload(self):
        self.ee.emit(Main.EVENT_RELOAD)

    def __postinit(self):
        """ Post-init for everything that needs a ready main instance. """
        
        if self.__pi_done:
            return

        self.config = JSON_File("config/settings.json")
        self.igp = []

        @self.config.ee.on(JSON_File.EVENT_RELOAD)
        def _on_config_reload(cfg):
            self.igp = [re.compile(r) for r in cfg["ignore-pattern"]]

        self.__pi_done = True

        self.reload()

    def run(self):
        self.__postinit()
        from bot_modules import load
        load()

        self.bot.run(self.config["token"])
