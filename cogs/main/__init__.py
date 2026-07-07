from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Bot, Cog, Context, command, slash_command


class Main(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='ping')
    async def command_ping(self, ctx: Context):
        '''See bot latency'''
        await ctx.reply(f'Pong with {self.bot.latency*1000:.2f} ms')

    @slash_command(name='ping')
    async def slash_command_ping(self, inter: ApplicationCommandInteraction):
        '''See bot latency'''
        await inter.send(f'Pong with {self.bot.latency*1000:.2f} ms')


def setup(bot: Bot):
    bot.add_cog(Main(bot))
