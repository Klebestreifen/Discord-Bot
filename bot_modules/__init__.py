# Register modules hear
__BML = [
    "admin",
    "insider",
    "talk"
]

###############################################################################

def load():
    from misc import log

    def _load_one(name):
        __import__(f"bot_modules.{name}", globals(), locals(), ["load"], 0).load()

    for _bm in __BML:
        log(f"Loading {_bm} module")
        _load_one(_bm)
