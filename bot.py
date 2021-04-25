import asyncio
import re
import traceback
import discord
from discord.utils import get

from misc import log
from command import Command
from main_singleton import Main

class Bot(discord.Client):
    """ Discord-Bot Kenrnel class """

    async def on_ready(self):
        log("Bot online")

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

        def îs_ignored_token(m):
            for p in Main.get().igp:
                if re.match(p, m):
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
                await msg.channel.send(f"Hay {Main.get().config['developer-mention']}! Schau dir das mal bitte an!")
                await asyncio.sleep(1)
                await msg.channel.send("Ich will ja, dass mein Code ordentlich funktioniert!")

                error_user = await self.fetch_user(Main.get().config["send-error-to-user-id"])
                await error_user.send(f"```\n{traceback.format_exc()}\n```")
    
    async def on_voice_state_update(self, member, before, after):
        def is_talk_channel(cid):
            return bool(str(cid) in Main.get().config["talk-channels"])

        # If channel difference
        if (before.channel != after.channel):
            channel = after.channel or before.channel
            guild = channel.guild

            talk_role = get(guild.roles, id=int(Main.get().config["talk-role"]))

            # If disconnected
            if after.channel is None:
                # Then remove the role
                await member.remove_roles(talk_role)

            # Else-If the new channel not in whitelist
            elif not is_talk_channel(after.channel.id):
                # Then remove the role
                await member.remove_roles(talk_role)

            # Else garnd <@im Talk> role
            else:
                # Because the user is connected to whitelisted talk
                await member.add_roles(talk_role)