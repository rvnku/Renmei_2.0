from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Bot, Cog, Context, MissingRequiredArgument, Param, group, guild_only, slash_command
from disnake.ext.commands.context import AnyContext
from .commands import play


class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name='music', aliases=['m'])
    async def command_music(self, _: Context): pass
    @slash_command(name='music')
    async def slash_command_music(self, _: ApplicationCommandInteraction): pass

    @command_music.command(name='play')
    @guild_only()
    async def command_music_play(self, ctx: Context, *, query: str):
        '''Play song in voice channel'''
        await play(ctx, query)

    @slash_command_music.sub_command(name='play')
    @guild_only()
    async def slash_command_music_play(self, inter: ApplicationCommandInteraction, query: str = Param(description='Search query')):
        '''Play song in voice channel'''
        await play(inter, query)

    @command_music_play.error  # type: ignore[reportArgumentType]
    @slash_command_music_play.error  # type: ignore[reportArgumentType]
    async def handler_music_play(self, ctx: AnyContext, error: Exception):
        if isinstance(error, MissingRequiredArgument):
            if isinstance(ctx, Context):
                await ctx.send_help(ctx.command)


def setup(bot: Bot):
    bot.add_cog(Music(bot))

