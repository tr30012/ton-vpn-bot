from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

import settings
from db.pool import AsyncExecute
from db.queries import select_users_languages, update_user_language

START = "command.start.reply"
SETTINGS = "command.settings.reply"
LANGUAGE = "command.settings.language.reply"

LOCALE_SUCCESS = "command.change.locale.success"
LOCALE_FAIL = "command.change.locale.fail"

INLINE_SETTINGS = "inline.button.settings"
INLINE_GET_VPN = "inline.button.getvpn"

INLINE_CHANGE_LANGUAGE = "inline.button.change-language"
INLINE_BACK = "inline.button.back"

__english = {
    START: ("Hello there! It is official bot of DedokVPN.\n\n"
            "Choose what do you want to do.\n\n"
            "Press action button under this message."),

    SETTINGS: ("Choose what do you want to do.\n\n"
                "Press action button under this message."),

    LANGUAGE: "Choose language below:",

    LOCALE_SUCCESS: "You changed locale to English.",
    LOCALE_FAIL: "Something went wrong.\nTry again later.",

    INLINE_GET_VPN: "Get VPN",
    INLINE_SETTINGS: "Settings",

    INLINE_BACK: "< Back",
    INLINE_CHANGE_LANGUAGE: "Change language"
}

__russian = {
    START: ("Здравствуйте! Это официальный бот DedokVPN.\n\n"
            "Выберите, что вы хотите сделать.\n\n"
            "Нажмите кнопку выбора действия внизу"),

    SETTINGS: ("Выберите, что вы хотите сделать.\n\n"
                "Нажмите кнопку выбора действия внизу."),

    LANGUAGE: "Выберите язык:",

    LOCALE_SUCCESS: "Вы поменяли язык на русский.",
    LOCALE_FAIL: "Что-то пошло не так.\nПопробуйте позже.",

    INLINE_GET_VPN: "Получит VPN",
    INLINE_SETTINGS: "Настройки",

    INLINE_BACK: "< Назад",
    INLINE_CHANGE_LANGUAGE: "Поменять язык"
}

__locales = {
    "en": __english,
    "ru": __russian
}

__users = {}


async def prefetch_languages(bot: Bot) -> dict:
    pool: AsyncEngine = bot['pool']

    async with pool.connect() as connection:
        async for row in AsyncExecute(connection, select_users_languages(), dict):
            __users.update({row['telegram_id']: row['language_code']})

    return __users


# Short and save definition for locales dictionary
def ll(telegram_id: int, code: str) -> str:
    if telegram_id in __users:
        return __locales[__users[telegram_id]][code]
    else:
        return __locales[settings.LANGUAGE][code]


# Short definition for rewriting chats languages
async def lu(bot: Bot, telegram_id: int, language: str):
    __users[telegram_id] = language

    pool: AsyncEngine = bot['pool']

    async with pool.connect() as connection:
        await connection.execute(update_user_language(telegram_id, language))
        await connection.commit()


# Short definition to validate language
def vl(language: str) -> bool:
    return language in __locales
