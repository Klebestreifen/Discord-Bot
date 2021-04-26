import asyncio
from datetime import datetime

def log(msg):
    print("[", datetime.now(), f"] {str(msg)}")

def generate_paramether_list(dc_msg):
    l = dc_msg.content.split('!')[1].split(' ')
    l = [(i.lower()) for i in l ]
    return l

def fake_sync(func):
    def decorated(*args, **kwargs):
        return asyncio.ensure_future(func(*args, **kwargs))
    return decorated