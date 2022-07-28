import logging

from aiogram import Bot, Dispatcher
from vpnbot.bot.handlers import _lazy_load


def create_dispatcher(token: str) -> (Bot, Dispatcher):
    logging.info("Creating dispatcher")

    bot = Bot(token)
    dp = Dispatcher(bot)

    logging.info("Loading bot handlers.")
    _lazy_load(bot, dp)

    return bot, dp
