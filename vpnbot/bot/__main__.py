from vpnbot.bot.dispatcher import create_dispatcher
from vpnbot.utils.bot import get_bot_token
from vpnbot.orm.pool import setup_async_pool
from aiogram.utils import executor


def main():
    bot, dispatcher = create_dispatcher(get_bot_token())
    bot['engine'] = setup_async_pool()
    executor.start_polling(dispatcher)
