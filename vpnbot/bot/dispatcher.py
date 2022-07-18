from aiogram import Bot, Dispatcher
from bot.handlers import _lazy_load
from settings import create_logger


logger = create_logger("dispatcher.creator")


def create_dispatcher(token: str) -> (Bot, Dispatcher):
    logger.info("Creating dispatcher")

    bot = Bot(token)
    dp = Dispatcher(bot)

    logger.info("Loading bot handlers.")
    _lazy_load(bot, dp)

    return bot, dp

