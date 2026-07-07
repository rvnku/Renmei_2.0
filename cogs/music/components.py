from disnake.ui import Container, TextDisplay
from mafic.track import Track
from core.utils import escape


def to_time(seconds: int) -> str:
    if seconds // 3600:
        return f'{seconds // 3600}:{seconds % 3600 // 60:02}:{seconds % 60:02}'
    return f'{seconds // 60}:{seconds % 60:02}'


def create_track_card(track: Track):
    return Container(
        TextDisplay(
            f'## Currently playing\n'
            f'> **{escape(track.title)}** by *{escape(track.author)}*\n'
            f'- Duration: `{to_time(track.length // 1000)}`'
        )
    )
