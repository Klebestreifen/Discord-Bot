from misc import log
from command import Command
from emojis import Emojis
from main_singleton import Main

def load():
    @Command.register("test", "permission.command.test")
    async def _command_test(msg):
        await msg.channel.send(Emojis.FUGU_HAPPY)

    @Command.register("reload", "permission.command.reload")
    async def _command_reload(msg):
        Main.i().reload()
        await msg.channel.send(Emojis.FUGU_HAPPY)
