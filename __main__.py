import random

from util import config, log, file2str, generate_paramether_list
from classes.Command import Command
from classes.Emojis import Emojis
from classes.Main import Main

###########################################################
"""
    COMMANDS
    The server commands are listed here.
"""

@Command.register("test", "permission.command.test")
async def command_test(msg):
    await msg.channel.send(Emojis.FUGU_HAPPY)

@Command.register("insider", "permission.command.insider")
async def command_insider(msg):
    params = generate_paramether_list(msg)
    i_cats = config["insider"]

    def insider_list():
        str_i_list = "```\n"
        for cat, insiders in i_cats.items():
            str_i_list += f"{str(len(insiders))} Insider in der Rubrik \"{cat}\"\n"
        str_i_list += "\n```"
        return str_i_list

    if len(params) == 1:
        await msg.channel.send(
            "Verwende den Command so:" 
            "```!insider <rubrik>```"
            "Hier ist die Liste darüber, über welche Rubrik ich etwas weiß:\n" 
            + insider_list()
        )
        return
    elif not len(params) == 2:
        await msg.channel.send(
            "Syntaxfehler\n"
            "Verwende den Command so:" 
            "```!insider <rubrik>```"
            "Hier ist die Liste darüber, über welche Rubrik ich etwas weiß:\n" 
            + insider_list()
        )
        return

    try:
        i_list = i_cats[params[1]]
        await msg.channel.send(random.choice(i_list))
    except KeyError:
        await msg.channel.send(
            "Aus dieser Rubrik kenne ich keine Insider.\n" +
            "Hier ist die Liste darüber, über welche Rubrik ich etwas weiß:\n" +
            insider_list()
        )
    

###########################################################
"""
    MAIN-CALL
    Program start
"""
if __name__ == "__main__": Main.get().run()
