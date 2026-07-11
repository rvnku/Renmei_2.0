from disnake import MediaGalleryItem
from disnake.ui import MediaGallery, TextDisplay
from json import JSONDecodeError
from cloudscraper import requests


def roleplay_message(action: str, text: str, quote: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://nekos.best/',
    }
    try:
        result = requests.get(
            'https://nekos.best/api/v2/' + action,
            headers=headers,
            timeout=30
        ).json()['results'][0]
    except JSONDecodeError:
        return None

    components = [
        TextDisplay(f'### {text}'),
        MediaGallery(MediaGalleryItem(result['url'])),
        TextDisplay(f'-# Момент из аниме «{result['anime_name']}»')
    ]
    if quote:
        components.insert(1, TextDisplay(f'>>> {quote}'))
    return components
