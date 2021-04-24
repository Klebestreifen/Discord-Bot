from datetime import datetime

def log(msg):
    print("[", datetime.now(), f"] {str(msg)}")

def generate_paramether_list(dc_msg):
    l = dc_msg.content.split('!')[1].split(' ')
    l = [(i.lower()) for i in l ]
    return l