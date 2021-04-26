from discord.utils import get
from main_singleton import Main
from bot import Bot
from misc import fake_sync

def load():
    main = Main.i()

    def is_talk_channel(cid):
        return bool(str(cid) in main.config["talk-channels"])

    def get_talk_role(guild):
        return get(guild.roles, id=int(main.config["talk-role"]))

    @main.bot.ee.on(Bot.EVENT_USER_CONNECT_VOICE)
    @fake_sync
    async def _on_user_connect(member, channel):
        if is_talk_channel(channel.id):
            await member.add_roles(get_talk_role(channel.guild))

    @main.bot.ee.on(Bot.EVENT_USER_DISCONNECT_VOICE)
    @fake_sync
    async def _on_user_disconnect(member, channel):
        await member.remove_roles(get_talk_role(channel.guild))

    @main.bot.ee.on(Bot.EVENT_USER_SWITCHED_VOICE)
    @fake_sync
    async def _on_user_disconnect(member, _, channel):
        if is_talk_channel(channel.id):
            await member.add_roles(get_talk_role(channel.guild))
        else:
            await member.remove_roles(get_talk_role(channel.guild))
