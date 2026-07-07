from disnake import Member, Message
from typing import Callable
from functools import wraps
from core.env import Env
from .templater import replace
import json, re


with open('assets/roleplay.json', 'r') as file:
    actions = json.load(file)


def roleplay_action(func: Callable):
    '''
    Decorator for processing roleplay messages in a cog.

    This decorator is intended to be used on cog methods that handle incoming
    messages. It intercepts the message, parses its content against a set of
    predefined roleplay actions loaded from ``assets/roleplay.json``, and
    generates a response text based on the context (mentions, replies, etc.).

    The decorated function must accept the following signature:

        async def command(self, message: Message, reference: Message | None,
                          action: str, text: str, quote: str | None) -> ...:

    Parameters
    ----------
    func : Callable
        The cog method to wrap.

    Returns
    -------
    Callable
        The wrapped function that processes the message and calls ``func``
        only if a valid roleplay action is matched and the author has a gender
        role (either male or female).

    Notes
    -----
    - The decorator expects the wrapped method to be a cog method, so the
      first argument is ``self`` and the second is a :class:`disnake.Message`.
    - If the message has no content, the decorator returns immediately without
      calling ``func``.
    - If the author does not have either :attr:`core.env.Env.male_role_id` or
      :attr:`core.env.Env.female_role_id`, the message is ignored.
    - The ``actions`` dictionary is loaded once from the JSON file and has the
      following structure:

      .. code-block:: json

          {
              "action_name": {
                  "trigger phrase | alternative trigger": "response template",
                  ...
              },
              ...
          }

    - When multiple triggers are separated by ``' | '``, any of them will match.
    - The replacement function :func:`~.templater.replace` is used to substitute
      placeholders in the response template with author, mentions, etc.
    - The final call to ``func`` passes:
        - ``self`` – the cog instance.
        - ``message`` – the original :class:`disnake.Message`.
        - ``reference`` – the resolved referenced message (if any), else ``None``.
        - ``action`` – the matched action key (e.g., ``"hug"``).
        - ``text`` – the generated response text.
        - ``quote`` – the trailing text after the trigger (stripped of mentions),
          or ``None`` if empty.
    '''

    @wraps(func)
    async def wrapper(self, message: Message):
        if not message.content: return
        if not isinstance(author := message.author, Member): return

        for action in actions:
            for words in actions[action]:
                for keyword in words.split(' | '):
                    if not (content := message.content.lower().replace('ё', 'е')).startswith(keyword.lower().replace('ё', 'е')):
                        continue

                    if ((suffix := content[len(keyword):]) and re.fullmatch(r'\w', suffix[0])):
                        continue

                    if author.get_role(Env.male_role_id):
                        gender = 0
                    elif author.get_role(Env.female_role_id):
                        gender = 1
                    else:
                        return

                    options = actions[action][words]
                    reference = ref if message.reference and isinstance(ref := message.reference.resolved, Message) else None
                    mentions = []

                    if isinstance(options, str):
                        options, num = [options], 0
                    else:
                        if message.mention_everyone:
                            num = 0
                        elif mentions := message.mentions + message.role_mentions:
                            if any(mention.id != author.id for mention in mentions):
                                num = 2 if len(mentions) == 1 else 1
                            else:
                                mentions, num = [], 3
                        elif reference:
                            num = 2
                            mentions.append(reference.author)
                        else:
                            num = 4

                    if not options[num]: return

                    text = replace(options[num], author, mentions, gender, keyword)
                    quote = re.sub(r'<@!?\d+>|<@&\d+>', '', suffix).strip() or None
                    return await func(self, message, reference, action, text, quote)
    return wrapper
