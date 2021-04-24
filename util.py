import json
import re

def file2str(filename):
    rtn = ""
    with open(filename, "r", encoding="utf8") as file:
        rtn = file.read()
    return rtn

class JSON_File():
    def __init__(self, path):
        self.path = path
        self.reload()

    def reload(self):
        self.data = json.loads(file2str(self.path))

    def on_reload(self, func):
        pass # TODO

    def __getitem__(self, key):
        return self.data[key]

config = JSON_File("config/settings.json")
igp = [re.compile(r) for r in config["ignore-pattern"]]

def log(msg):
    print(msg)

def generate_paramether_list(dc_msg):
    l = dc_msg.content.split('!')[1].split(' ')
    l = [(i.lower()) for i in l ]
    return l