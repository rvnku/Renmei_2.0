from disnake import Interaction, Message
from disnake.ext.commands import Context
from core.errors import NoOwnGuild
from core.confg import Conf
from functools import wraps
from typing import Callable


def own_guild_only(*, silent: bool = False):
    '''
    Restrict a command or event listener to the bot's own guild.

    This decorator can be applied to:
      - Slash/user/message commands (handling :class:`disnake.Interaction`)
      - Text commands (handling :class:`disnake.ext.commands.Context`)
      - Event listeners (handling :class:`disnake.Message`)

    The decorated callable **must** accept one of the above types as its
    first positional argument (after ``self`` if it's a cog method).

    Parameters
    ----------
    silent : bool, default=False
        If ``True``, the decorated function will be skipped silently when the
        command/listener is invoked outside the own guild. No exception is
        raised, and the function body is not executed.
        If ``False`` (default), a :class:`core.errors.NoOwnGuild` exception
        is raised when the context does not belong to the own guild.

    Raises
    ------
    NoOwnGuild
        When ``silent=False`` and the command/listener is invoked in a
        different guild than :attr:`core.env.Env.guild_id`.

    Notes
    -----
    - The own guild ID is taken from :attr:`core.env.Env.guild_id`.
    - For **commands**, it is usually desirable to raise an exception so that
      a global error handler can respond to the user (e.g., "This command is
      only available in the official server").
    - For **event listeners** (e.g., ``Event.message``), using ``silent=True``
      is recommended to silently ignore messages from other guilds without
      polluting logs or stopping execution.
    '''

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if args and isinstance(ctx := args[0], Message | Context | Interaction):
                if not ctx.guild or ctx.guild.id != Conf.guild_id:
                    if silent: return
                    else: raise NoOwnGuild()
            else:
                raise NotImplementedError()

            return await func(self, *args, **kwargs)
        return wrapper
    return decorator
