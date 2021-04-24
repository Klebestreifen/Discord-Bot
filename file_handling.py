from pymitter import EventEmitter
import json

def file2str(filename):
    rtn = ""
    with open(filename, "r", encoding="utf8") as file:
        rtn = file.read()
    return rtn

class JSON_File():
    EVENT_RELOAD = "reload"

    def __init__(self, path):
        self.path = path
        self.ee = EventEmitter()
        self.reload()

    def reload(self):
        self.data = json.loads(file2str(self.path))
        self.ee.emit(JSON_File.EVENT_RELOAD, self)

    def __getitem__(self, key):
        return self.data[key]