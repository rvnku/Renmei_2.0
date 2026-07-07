from disnake.ext.commands import Bot, Context
from disnake.ext.commands.context import AnyContext
from disnake import AllowedMentions, User
from .components import member_components, user_components


async def command_info(bot: Bot, ctx: AnyContext, user: User):
    if (member := ctx.guild and ctx.guild.get_member(user.id)):
        components = await member_components(bot, user, member)
    else:
        components = await user_components(bot, user)

    if isinstance(ctx, Context):
        await ctx.reply(components=components, allowed_mentions=AllowedMentions.none())
    else:
        await ctx.send(components=components, allowed_mentions=AllowedMentions.none())
