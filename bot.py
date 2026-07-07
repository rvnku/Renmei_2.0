from disnake import Intents
from disnake.ext.commands import Bot, CommandError, CommandNotFound, Context, when_mentioned_or
from core.console import create_console_loop
from core.mafic import connect_nodes
from core.ext import load_extensions
import datetime, logging


class Renmei(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or('.'),
            # help_command=RenmeiHelpCommand,
            description='Rina\'s personal discord bot',
            strip_after_prefix=True,
            case_insensitive=True,
            intents=Intents.all()
        )
        self.logger = logging.getLogger('renmei')
        self.started_at = datetime.datetime.now()

    async def on_ready(self):
        load_extensions(self)
        create_console_loop(self)
        connect_nodes(self)

    async def on_command_error(self, context: Context, exception: CommandError) -> None:
        if (command := context.command) and command.has_error_handler(): return
        if (cog := context.cog) and cog.has_error_handler(): return
        if isinstance(exception, CommandNotFound): return
        if command:
            self.logger.exception(f'An unknown error occurred in the command {context.clean_prefix + command.qualified_name}', exc_info=exception)
        else:
            await super().on_command_error(context, exception)
