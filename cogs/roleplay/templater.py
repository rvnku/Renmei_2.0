from disnake import Member, Role, User
from typing import List, Optional, Union
from core.utils.misc import humanize_list
import re


def replace(text: str, author: Member, target: Optional[List[Union[Member, Role, User]]], gender: int, keyword: str) -> str:
    text = text.format(author.mention, target and humanize_list([t.mention for t in target]), kw=keyword)
    if '[' in text:
        pattern = r'\[([^\[\]]*?\|[^\[\]]*?)\]'
        def replacer(match):
            options = match.group(1).split('|')
            return options[gender] if gender < len(options) else options[0]
        text = re.sub(pattern, replacer, text)
    return text
