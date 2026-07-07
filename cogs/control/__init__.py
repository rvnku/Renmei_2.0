from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Bot, Cog, Context, MissingRequiredArgument, Param, command, is_owner, slash_command
from disnake.ext.commands.context import AnyContext
from cogs.control.commands import command_exec
from core.env import Env


class Control(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(name='exec', hidden=True, guild_ids=[Env.guild_id])
    async def command_exec(self, ctx: Context, *, code: str):
        '''Execute python code in the command method'''
        await command_exec(ctx, self, self.bot, code)

    @is_owner()
    @slash_command(name='exec', hidden=True, guild_ids=[Env.guild_id])
    async def slash_command_exec(self, inter: ApplicationCommandInteraction,
        code: str = Param(description='Your python code')):
        '''Execute python code in the command method'''
        await inter.response.defer()
        await command_exec(inter, self, self.bot, code)

    @command_exec.error  # type: ignore[reportArgumentType]
    @slash_command_exec.error  # type: ignore[reportArgumentType]
    async def handler_command_exec(self, ctx: AnyContext, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            if isinstance(ctx, Context):
                await ctx.send_help(ctx.command)


def setup(bot: Bot):
    bot.add_cog(Control(bot))
