from disnake.utils import escape_markdown, escape_mentions
from typing import Any, List


def humanize_list(items: List[Any]) -> str:
    if not items:
        return ''
    if len(items) == 1:
        return f'{items[0]}'
    if len(items) == 2:
        return f'{items[0]} и {items[1]}'
    return ', '.join(map(str, items[:-1])) + f' и {items[-1]}'


def escape(text: str, *, as_needed: bool = False, ignore_links: bool = True):
    '''
    A helper function that escapes Discord's markdown,
    and also everyone, here, role, and user mentions.
    '''
    return escape_mentions(escape_markdown(text, as_needed=as_needed, ignore_links=ignore_links))


def cleanup_code(content: str) -> str:
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')
