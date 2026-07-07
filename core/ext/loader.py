from disnake.ext.commands import Bot, ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError
from .search import search_extensions
import logging


logger = logging.getLogger('extensions')


def load_extensions(bot: Bot):
    for extension in search_extensions('cogs'):
        try:
            bot.load_extension(extension)
        except ExtensionNotFound:
            logger.error(f'The extension `{extension}` could not be imported.', exc_info=True)
        except ExtensionAlreadyLoaded:
            logger.error(f'The extension `{extension}` is already loaded.', exc_info=True)
        except NoEntryPointError:
            logger.error(f'The extensios `{extension}` does not have a setup function.', exc_info=True)
        except ExtensionFailed:
            logger.error(f'The extension `{extension}` or its setup function had an execution error.', exc_info=True)
        else:
            logger.info(f'The extensios `{extension}` was sucessfully loaded.')

def reload_extensions(bot: Bot):
    for extension in search_extensions('cogs'):
        try:
            bot.reload_extension(extension)
        except ExtensionNotLoaded:
            logger.error(f'The extension `{extension}` was not loaded.', exc_info=True)
        except ExtensionNotFound:
            logger.error(f'The extension `{extension}` could not be imported.', exc_info=True)
        except NoEntryPointError:
            logger.error(f'The extensios `{extension}` does not have a setup function.', exc_info=True)
        except ExtensionFailed:
            logger.error(f'The extension `{extension}` setup function had an execution error.', exc_info=True)
        else:
            logger.info(f'The extensios `{extension}` was sucessfully reloaded.')

def unload_extensions(bot: Bot):
    for extension in search_extensions('cogs'):
        try:
            bot.unload_extension(extension)
        except ExtensionNotFound:
            logger.error(f'The name of the extension `{extension}` could not be resolved.', exc_info=True)
        except ExtensionNotLoaded:
            logger.error(f'The extension `{extension}` was not loaded.', exc_info=True)
        else:
            logger.info(f'The extensios `{extension}` was sucessfully reloaded.')
