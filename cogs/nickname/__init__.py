from disnake import Event, Forbidden, Guild, Member, Message, Role, TextChannel
from disnake.ext.commands import Bot, ChannelNotFound, Cog, GuildNotFound, RoleNotFound
from core.checkers import own_guild_only
from core.utils import get_euphopy
from core.config import Conf
import contextlib, re


class NicknameChanger(Cog):
    def __init__(self, channel: TextChannel, role: Role):
        self.channel = channel
        self.role = role

    @own_guild_only(silent=True)
    @Cog.listener(Event.message)
    async def event(self, message: Message):
        if message.channel.id != self.channel.id: return
        if message.author.bot: return
        assert isinstance(message.author, Member)

        await message.delete()

        if not message.content: return
        nickname = ' '.join(message.content.lower().split())
        if not re.fullmatch(r'([а-яё]{2,20}+\s*){1,3}', nickname): return
        if get_euphopy(nickname) < 0.4: return

        with contextlib.suppress(Forbidden):
            await message.author.edit(nick=nickname, roles=list(set(message.author.roles + [self.role])))


def setup(bot: Bot):
    if not isinstance(guild := bot.get_guild(Conf.guild_id), Guild):
        raise GuildNotFound(str(Conf.guild_id))
    if not isinstance(channel := guild.get_channel(Conf.nickname_channel_id), TextChannel):
        raise ChannelNotFound(str(Conf.nickname_channel_id))
    if not isinstance(role := guild.get_role(Conf.member_role_id), Role):
        raise RoleNotFound(str(Conf.member_role_id))
    bot.add_cog(NicknameChanger(channel, role))
