from disnake import ClientException, FFmpegPCMAudio, VoiceClient
from subprocess import Popen, DEVNULL
from typing import List
from .states import PlayerInfo, remove_player, cleanup_player
import asyncio, logging, os


logger = logging.getLogger('sp_playback')


async def start_playback(client: VoiceClient, players: List[PlayerInfo], guild_id: int, user_id: int, token: str):
    path = f'/tmp/spotify_pipe_{user_id}'
    if os.path.exists(path):
        os.unlink(path)
    os.mkfifo(path)

    process = await asyncio.to_thread(
        Popen,
        [
            'librespot',
            '-n', client.user.display_name,
            '-k', token,
            '-B', 'pipe',
            '-d', path,
            '-b', '320',
        ],
        stdout=DEVNULL,
        stderr=DEVNULL
    )

    player_info = PlayerInfo(guild_id, user_id, process, path)
    players.append(player_info)

    try:
        source = FFmpegPCMAudio(path, before_options='-re -f s16le -ar 44100 -ac 2')
    except ClientException as e:
        process.terminate()
        if os.path.exists(path):
            os.unlink(path)
        remove_player(players, guild_id)
        raise RuntimeError(f"FFmpeg error: {e}")

    def after_callback(exc):
        if exc:
            logger.error(f"Playback error: {exc}")
        cleanup_player(players, guild_id)

    client.play(source, after=after_callback)
