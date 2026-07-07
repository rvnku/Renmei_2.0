from disnake.ext.commands import Bot
from core.ext import reload_extensions
import asyncio, logging, sys


logger = logging.getLogger('console')


async def listener(bot: Bot):
    loop = asyncio.get_running_loop()
    while not loop.is_closed():
        try:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line: break  # EOF

            command = line.rstrip()
            if not command.startswith('/'): continue
            if command == '/stop':
                logger.info('Stopping the client with the /stop command...')
                await bot.close()
                break
            elif command == '/reload':
                logger.info('Reload extensions with the /reload command...')
                reload_extensions(bot)
            else:
                logger.warning(f'Unknown console command was received: {command}')

        except Exception as e:
            logger.error(f'Unexpected error in console listener: {e}')
            break
