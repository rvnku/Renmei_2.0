from disnake import ApplicationCommandInteraction, Message, User
from disnake.ext.commands import Bot, Cog, Context, Param, UserConverter, UserNotFound, group, slash_command, user_command
from disnake.ext.commands.context import AnyContext
from .commands import command_info
from typing import Optional
import logging


class Information(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger('info')

    @group(name='info')
    async def command_info(self, _: Context): pass
    @slash_command(name='info')
    async def slash_command_info(self, _: ApplicationCommandInteraction): pass

    @command_info.command(name='user')
    async def command_info_user(self, ctx: Context, user: Optional[str]):
        '''Information about user'''
        subject = None
        if user:
            if not (subject := await UserConverter().convert(ctx, user)):
                raise UserNotFound(user)
        elif reference := ctx.message.reference:
            if not isinstance(message := reference.resolved, Message):
                message = await ctx.channel.fetch_message(reference.message_id) if reference.message_id else None
            if message:
                subject = message.author
        subject = subject or ctx.author
        subject = await self.bot.fetch_user(subject.id)
        await command_info(self.bot, ctx, subject)

    @user_command(name='Information about user')
    async def user_command_info(self, inter: ApplicationCommandInteraction, user: User):
        '''Information about user'''
        await inter.response.defer()

        subject = await self.bot.fetch_user(user.id)
        await command_info(self.bot, inter, subject)

    @slash_command_info.sub_command(name='user')
    async def slash_command_info_user(
        self, inter: ApplicationCommandInteraction,
        user: Optional[str] = Param(description='Member or user by ID, mention, username, nickname or global name', default=None)):
        '''Information about user'''
        await inter.response.defer()

        if user:
            if not (subject := await UserConverter().convert(inter, user)):
                raise UserNotFound(user)
        else:
            subject = inter.author
        subject = await self.bot.fetch_user(subject.id)
        await command_info(self.bot, inter, subject)

    @command_info_user.error  # type: ignore[reportArgumentType]
    @user_command_info.error  # type: ignore[reportArgumentType]
    @slash_command_info_user.error  # type: ignore[reportArgumentType]
    async def handler_info_user(self, ctx: AnyContext, error: Exception):
        if isinstance(error, UserNotFound):
            msg = 'U_U User not found alas'
        else:
            self.logger.error('An unknown error occurred in the command `info user`', exc_info=True)
            msg = '@~@ Unknown error'

        if isinstance(ctx, Context):
            return await ctx.reply(msg)
        return await ctx.send(msg)


def setup(bot: Bot):
    bot.add_cog(Information(bot))
