from disnake.ext.commands import Bot
from mafic import NodePool


async def add_nodes(pool: NodePool):
    await pool.create_node(
        host='127.0.0.1',
        port=2333,
        label='MAIN',
        password='renmei'
    )


def connect_nodes(bot: Bot):
    pool = NodePool(bot)
    bot.loop.create_task(add_nodes(pool))
