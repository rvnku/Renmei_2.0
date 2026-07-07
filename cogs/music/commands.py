from disnake import Member
from disnake.ext.commands import Context
from disnake.ext.commands.context import AnyContext
from .components import create_track_card
from mafic.player import Player
from mafic.playlist import Playlist


async def play(ctx: AnyContext, query: str):
    assert ctx.guild and isinstance(ctx.author, Member)

    if not ctx.author.voice or not ctx.author.voice.channel:
        msg = 'You must be in the voice channel'
        if isinstance(ctx, Context):
            return await ctx.reply(msg)
        return ctx.send(msg)

    if not isinstance(player := ctx.guild.voice_client, Player):
        if player: await player.disconnect(force=True)
        player = await ctx.author.voice.channel.connect(cls=Player)

    if not (tracks := await player.fetch_tracks(query)):
        msg = 'No tracks found'
        if isinstance(ctx, Context):
            return await ctx.reply(msg)
        return await ctx.send(msg)

    elif isinstance(tracks, Playlist):
        tracks = tracks.tracks
    track = tracks[0]
    await player.play(track)
    components = create_track_card(track)
    if isinstance(ctx, Context):
        return await ctx.reply(components=components)
    return await ctx.send(components=components)
