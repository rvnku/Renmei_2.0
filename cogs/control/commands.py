from disnake.ext.commands import Bot, Cog, Context
from disnake.ext.commands.context import AnyContext
from disnake.ui import TextDisplay
from core.errors import CompileError
from core.utils import cleanup_code
from .execution import execute, get_latest
from .components import compile_error_components, runtime_error_components, output_result_components
from typing import Optional
import disnake


async def command_exec(ctx: AnyContext, cog: Cog, bot: Bot, text: str) -> Optional[str]:
    env = {
        'bot': bot,
        'self': cog,
        'cog': cog,
        'disnake': disnake,
        'discord': disnake,
        'ctx': ctx,
        'inter': ctx,
        '_': get_latest(),
        '__name__': '__exec__'
    }
    env.update(globals())
    code = cleanup_code(text)

    try:
        response = await execute(code, env)
    except CompileError as exc:
        components = await compile_error_components(code, exc)
    except RuntimeError as exc:
        components = await runtime_error_components(code, exc)
    else:
        components = await output_result_components(code, response)

    if isinstance(ctx, Context):
        if isinstance(components, TextDisplay): return
        await ctx.reply(components=components)
    else:
        await ctx.send(components=components)
