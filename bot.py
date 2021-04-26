import asyncio
import re
import traceback
import discord
from pymitter import EventEmitter

from misc import log
from command import Command
from main_singleton import Main

class Bot(discord.Client):
    """ Discord-Bot Kenrnel class """

    EVENT_READY                 = "reday"
    EVENT_MESSAGE               = "message"
    EVENT_USER_CONNECT_VOICE    = "userconnectvoice"
    EVENT_USER_DISCONNECT_VOICE = "userdisconnectvoice"
    EVENT_USER_SWITCHED_VOICE   = "userswitchedvoice"

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.ee = EventEmitter()

    async def on_ready(self):
        log("Bot online")
        self.ee.emit(Bot.EVENT_READY, self)

    async def on_message(self, msg):
        self.ee.emit(Bot.EVENT_MESSAGE, self, msg)

        async def execute(msg):
            cmd_name = msg.content.split('!')[1].split(' ')[0].lower()
            log(f"Command [{cmd_name}] from [{str(msg.author)}]")
            try:
                cmd = next(x for x in Command.commands if x.name == cmd_name)
                await cmd.execute(msg)
            except StopIteration:
                await msg.channel.send("Bitte was soll ich machen? Den Command kenne ich nicht. Hast du dich vertippt?")
                await asyncio.sleep(1)
                await msg.channel.send("Wenn ich den kennen sollte, dann wende dich ans Klebi. Der hilft gerne.")

        def îs_ignored_token(m):
            for _p in Main.i().igp:
                if re.match(_p, m):
                    return True
            return False

        if msg.author.bot:
            return
        if îs_ignored_token(msg.content):
            return
        if msg.content.startswith("!") and len(msg.content) >= 2 :
            await asyncio.sleep(0.5)
            try:
                await execute(msg)
            except Exception:
                await msg.channel.send("Oh! Da hast du wohl einen Bug gefunden!")
                await asyncio.sleep(1)
                await msg.channel.send("Irgendwas stimmt hier nicht. Ich weiß leider auch nicht was...")
                await asyncio.sleep(1)
                await msg.channel.send(f"Hay {Main.i().config['developer-mention']}! Schau dir das mal bitte an!")
                await asyncio.sleep(1)
                await msg.channel.send("Ich will ja, dass mein Code ordentlich funktioniert!")

                error_user = await self.fetch_user(Main.i().config["send-error-to-user-id"])
                await error_user.send(f"```\n{traceback.format_exc()}\n```")
    
    async def on_voice_state_update(self, member, before, after):
        # If channel difference
        if before.channel != after.channel:
            if before.channel is None:
                self.ee.emit(Bot.EVENT_USER_CONNECT_VOICE, member, after.channel)
            elif after.channel is None:
                self.ee.emit(Bot.EVENT_USER_DISCONNECT_VOICE, member, before.channel)
            else:
                self.ee.emit(Bot.EVENT_USER_SWITCHED_VOICE, member, before.channel, after.channel)