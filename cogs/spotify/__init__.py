from disnake import ApplicationCommandInteraction, Member, VoiceClient, VoiceProtocol
from disnake.ext.commands import Bot, Cog, guild_only, slash_command
from aiohttp import ClientSession
from core.api import fetch_token, poll_token
from core.config import Conf
from core.env import Env
from .librespot import start_playback
from .states import get_player, cleanup_player
import asyncio, logging


logger = logging.getLogger('spotify')


class Spotify(Cog):
    def __init__(self, bot: Bot, api_key: str):
        self.bot = bot
        self.api_key = api_key
        self.interval = 5
        self.timeout = 300
        self.players = []

    def get_login_url(self, user_id: int):
        return f'{Conf.base_url}/auth/login?{user_id=}'

    @slash_command(name='spotify')
    @guild_only()
    async def spotify(self, inter: ApplicationCommandInteraction):
        '''Play music from a Spotify client'''
        assert inter.guild and isinstance(inter.author, Member)
        await inter.response.defer(ephemeral=True)

        user_id = inter.author.id
        headers = {'X-Auth-Key': self.api_key}

        # Fetch the user's accept token
        async with ClientSession(headers=headers) as session:
            if not (token := await fetch_token(session, str(user_id))):
                await inter.edit_original_response(f'Link your Discord account to Spotify:\n{self.get_login_url(user_id)}')
                if not (token := await poll_token(session, str(user_id), self.interval, self.timeout)):
                    return await inter.edit_original_response('Spotify authorization timeout has expired')

        # User not in the voice
        if not (voice := inter.author.voice) or not (channel := voice.channel):
            return await inter.edit_original_response('You are not in the voice channel')

        # Client already exists
        match client := inter.guild.voice_client:
            case VoiceClient():
                if player := get_player(self.players, inter.guild.id):
                    if player.user_id != inter.author.id:
                        return await inter.edit_original_response('The bot is already being used by another user')
                    else:
                        if client.is_playing():
                            client.stop()
                            await asyncio.sleep(0.1)
                        cleanup_player(self.players, inter.guild.id)
            case VoiceProtocol():
                await client.disconnect(force=True)
                client = None
            case None: pass
            case _: return await inter.edit_original_response('The bot is already being used as another player')

        # Connect client
        try:
            if not client:
                client = await channel.connect()
            if client.channel.id != channel.id:
                await client.move_to(channel)
        except Exception:
            msg = 'Error when conneting/moving to voice channel'
            logger.exception(msg)
            return await inter.edit_original_response(msg)

        # Playback start
        try:
            await start_playback(client, self.players, inter.guild.id, inter.author.id, token)
        except Exception:
            msg = 'Error starting playback'
            logger.exception(msg)
            await inter.edit_original_response(msg)
            cleanup_player(self.players, inter.guild.id)
            if client and client.is_connected():
                await client.disconnect(force=True)
            return

        await inter.edit_original_response(f'Select {client.user.display_name} as the Spotify Connect Device to start playback')


def setup(bot: Bot):
    if not (api_key := Env.api_key):
        raise ValueError('API_KEY must be set in the environment')
    bot.add_cog(Spotify(bot, api_key))
