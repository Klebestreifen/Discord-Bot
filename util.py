from datetime import datetime
from pymitter import EventEmitter
import json
import re

def file2str(filename):
    rtn = ""
    with open(filename, "r", encoding="utf8") as file:
        rtn = file.read()
    return rtn

class JSON_File():
    EVENT_RELOAD = "reload"

    def __init__(self, path):
        self.path = path
        self.on_reload_handelrs = {"last" : 0}
        self.ee = EventEmitter()
        self.reload()

    def reload(self):
        self.data = json.loads(file2str(self.path))
        self.ee.emit(JSON_File.EVENT_RELOAD, self)

    def __getitem__(self, key):
        return self.data[key]

CONFIG = JSON_File("config/settings.json")
IGNORE_PATTERNS = []

CONFIG.ee.on(JSON_File.EVENT_RELOAD)
def on_config_reload(cfg):
    global IGNORE_PATTERNS
    IGNORE_PATTERNS = [re.compile(r) for r in cfg["ignore-pattern"]]

CONFIG.reload()

def log(msg):
    print("[", datetime.now(), f"] {str(msg)}")

def generate_paramether_list(dc_msg):
    l = dc_msg.content.split('!')[1].split(' ')
    l = [(i.lower()) for i in l ]
    return l