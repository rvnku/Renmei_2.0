from disnake.ext.commands import Bot
from .listener import listener


def create_console_loop(bot: Bot):
    bot.loop.create_task(listener(bot))
