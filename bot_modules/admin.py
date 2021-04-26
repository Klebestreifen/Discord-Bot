from misc import log
from command import Command
from emojis import Emojis

def load():
    @Command.register("test", "permission.command.test")
    async def _command_test(msg):
        await msg.channel.send(Emojis.FUGU_HAPPY)
