from disnake import MediaGalleryItem
from disnake.ui import MediaGallery, TextDisplay
import requests


def roleplay_message(action: str, text: str, quote: str):
    result = requests.get('https://nekos.best/api/v2/' + action).json()['results'][0]

    components = [
        TextDisplay(f'### {text}'),
        MediaGallery(MediaGalleryItem(result['url'])),
        TextDisplay(f'-# Момент из аниме «{result['anime_name']}»')
    ]
    if quote:
        components.insert(1, TextDisplay(f'>>> {quote}'))
    return components
