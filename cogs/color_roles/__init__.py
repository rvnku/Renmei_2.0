from disnake import Guild, Member
from disnake.ext.commands import Bot, Cog, GuildNotFound
from disnake.utils import get
from core.utils import get_primary_color
from core.config import Conf
import re


class ColorRoles(Cog):
    def __init__(self, guild: Guild):
        self.guild = guild

    async def cog_load(self):
        for member in self.guild.members:
            await self.update_member_role(member)
        for role in self.guild.roles:
            if re.fullmatch(r'#[0-9a-f]{6}', role.name) and not role.members:
                await role.delete()

    async def update_member_role(self, member: Member):
        color = await get_primary_color(member.display_avatar.url)
        if role := next((role for role in member.roles if role.name.startswith('#')), None):
            if role.color != color:
                await role.edit(name=str(color), color=color)
        else:
            latest = next((role for role in member.guild.roles if role.name.startswith('#')), None)
            if not (role := get(member.guild.roles, name=str(color))):
                role = await member.guild.create_role(name=str(color), color=color)
            await member.add_roles(role)
            if latest and latest.position > 1:
                await role.edit(position=latest.position)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id != self.guild.id: return
        await self.update_member_role(member)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        if member.guild.id != self.guild.id: return
        if role := next((role for role in member.roles if role.name.startswith('#')), None):
            await role.delete()

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if after.guild.id != self.guild.id: return
        if before.guild_avatar == after.guild_avatar != None: return
        await self.update_member_role(after)


def setup(bot: Bot):
    if not isinstance(guild := bot.get_guild(Conf.guild_id), Guild):
        raise GuildNotFound(str(Conf.guild_id))
    bot.add_cog(ColorRoles(guild))
