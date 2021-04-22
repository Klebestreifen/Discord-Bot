import json
import re

def file2str(filename):
    rtn = ""
    with open(filename, "r", encoding="utf8") as file:
        rtn = file.read()
    return rtn

config = json.loads(file2str("config/settings.json"))
igp = [re.compile(r) for r in config["ignore-pattern"]]

def log(msg):
    print(msg)

def generate_paramether_list(dc_msg):
    l = dc_msg.content.split('!')[1].split(' ')
    l = [(i.lower()) for i in l ]
    return l