import discord
from discord.utils import get
import asyncio
import re
import traceback
import sys

from util import config, log, igp
from classes.Command import Command

class Bot(discord.Client):
    """
        Discord-Bot Kenrnel class
    """
    async def on_ready(self):
        log("Bot ready")

    async def on_message(self, msg):
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

        def ignoredToken(m):
            for p in igp:
                if re.match(p, m):
                    return True
            return False

        if msg.author.bot: return
        if ignoredToken(msg.content): return
        if msg.content.startswith("!") and len(msg.content) >= 2 :
            await asyncio.sleep(0.5)
            try:
                await execute(msg)
            except Exception:
                await msg.channel.send("Oh! Da hast du wohl einen Bug gefunden!")
                await asyncio.sleep(1)
                await msg.channel.send("Irgendwas stimmt hier nicht. Ich weiß leider auch nicht was...")
                await asyncio.sleep(1)
                await msg.channel.send(f"Hay {config['developer-mention']}! Schau dir das mal bitte an!")
                await asyncio.sleep(1)
                await msg.channel.send("Ich will ja, dass mein Code ordentlich funktioniert!")

                error_user = await self.fetch_user(config["send-error-to-user-id"])
                await error_user.send(f"```\n{traceback.format_exc()}\n```")
    
    async def on_voice_state_update(self, member, before, after):
        def is_talk_channel(id):
            return bool(str(channel.id) in config["talk-channels"])

        if (before.channel != after.channel):
            channel = after.channel or before.channel
            guild = channel.guild

            talk_role = get(guild.roles, id=int(config["talk-role"]))

            if after.channel == None:
                # Disconnected
                await member.remove_roles(talk_role)
            elif not is_talk_channel(after.channel.id):
                # Switch to non-talk
                await member.remove_roles(talk_role)
            else:
                # Connected to talk
                await member.add_roles(talk_role)