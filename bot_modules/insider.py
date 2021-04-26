import random

from misc import generate_paramether_list
from command import Command
from main_singleton import Main

def load():
    @Command.register("insider", "permission.command.insider")
    async def _command_insider(msg):
        params = generate_paramether_list(msg)
        i_cats = Main.get().config["insider"]

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