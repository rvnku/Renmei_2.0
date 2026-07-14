from disnake import ClientException, FFmpegPCMAudio, VoiceClient
from subprocess import Popen, DEVNULL
from typing import List
from .states import PlayerInfo, get_player, remove_player, cleanup_player
import asyncio, logging, os, select


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
    except ClientException as exc:
        process.terminate()
        if os.path.exists(path):
            os.unlink(path)
        remove_player(players, guild_id)
        raise RuntimeError(f'FFmpeg error: {exc}')

    asyncio.create_task(monitor_playback_start(path, player_info, players, client, guild_id))

    def after_callback(exc):
        if exc:
            logger.error(f'Playback error: {exc}')
        if not player_info.active: return

        if player_info.process.poll() is None:
            try:
                source = FFmpegPCMAudio(path, before_options='-re -f s16le -ar 44100 -ac 2')
            except ClientException as exc:
                logger.error(f'FFmpeg error on restart: {exc}')
                cleanup_player(players, guild_id)
                return
            client.play(source, after=after_callback)
        else:
            cleanup_player(players, guild_id)

    client.play(source, after=after_callback)


async def monitor_playback_start(path: str, player_info: PlayerInfo, players: List[PlayerInfo], client: VoiceClient, guild_id: int):
    timeout = 60
    start_time = asyncio.get_event_loop().time()

    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        logger.error('Cannot open pipe for monitoring')
        return

    poll = select.poll()
    poll.register(fd, select.POLLIN)

    try:
        while True:
            if not player_info.active: break

            if asyncio.get_event_loop().time() - start_time > timeout:
                logger.info('Timeout waiting for playback start, cleaning up')
                cleanup_player(players, guild_id)
                if client.is_connected():
                    await client.disconnect(force=True)
                break

            if poll.poll(0): break
            await asyncio.sleep(0.5)
    finally:
        poll.unregister(fd)
        os.close(fd)


async def stop_playback(client: VoiceClient, players: List[PlayerInfo], guild_id: int, user_id: int):
    if not (player := get_player(players, guild_id)): return
    if player.user_id != user_id: return
    player.active = False
    client.stop()
    cleanup_player(players, guild_id)
    await client.disconnect(force=True)
