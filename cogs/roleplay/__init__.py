from disnake.ext.commands import Bot, Cog
from disnake import Event, Message
from .components import roleplay_message
from .decorator import roleplay_action
from core.checkers import own_guild_only
from typing import Optional


class RolePlay(Cog):
    @Cog.listener(Event.message)
    @own_guild_only(silent=True)
    @roleplay_action
    async def action(self, message: Message, reference: Optional[Message], action: str, text: str, quote: str):
        await message.delete(delay=0.1)

        components = roleplay_message(action, text, quote)
        if reference:
            await reference.reply(components=components)
        else:
            await message.channel.send(components=components)


def setup(bot: Bot):
    bot.add_cog(RolePlay())
