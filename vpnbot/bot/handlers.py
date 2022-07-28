from aiogram import Dispatcher, Bot
from aiogram import types

from vpnbot.bot.locales import lu, ll
from vpnbot.bot.locales import START, SETTINGS, LANGUAGE
from vpnbot.bot.keyboards import MainMenuKeyboard, SettingsMenuKeyboard, ChangeLanguageMenuKeyboard
from vpnbot.orm.pool import db_first_message


def _lazy_load(bot: Bot, dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def process_start_cmd(message: types.Message):
        await db_first_message(bot['pool'], message)
        await bot.send_message(message.chat.id, ll(message.chat.id, START),
                               reply_markup=MainMenuKeyboard(message.chat.id)
                               )

    @dp.message_handler(commands=["menu"])
    async def process_menu_cmd(message: types.Message):
        await bot.send_message(message.chat.id, ll(message.chat.id, START),
                               reply_markup=MainMenuKeyboard(message.chat.id)
                               )

    @dp.message_handler()
    async def process_echo_cmd(message: types.Message):
        await bot.send_message(message.chat.id, message.text)

    @dp.callback_query_handler(MainMenuKeyboard.query_settings)
    async def process_settings_callback(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id)
        await bot.edit_message_text(
            ll(query.message.chat.id, SETTINGS),
            query.message.chat.id,
            query.message.message_id,
            query.inline_message_id,

            reply_markup=SettingsMenuKeyboard(query.message.chat.id)
        )

    @dp.callback_query_handler(MainMenuKeyboard.query_vpn)
    async def process_settings_callback(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id)

    @dp.callback_query_handler(SettingsMenuKeyboard.query_language)
    async def process_settings_callback(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id)
        await bot.edit_message_text(
            ll(query.message.chat.id, LANGUAGE),

            query.message.chat.id,
            query.message.message_id,
            query.inline_message_id,

            reply_markup=ChangeLanguageMenuKeyboard(query.message.chat.id)
        )

    @dp.callback_query_handler(SettingsMenuKeyboard.query_back)
    async def process_settings_callback(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id)
        await bot.edit_message_text(
            ll(query.message.chat.id, START),

            query.message.chat.id,
            query.message.message_id,
            query.inline_message_id,

            reply_markup=MainMenuKeyboard(query.message.chat.id)
        )

    @dp.callback_query_handler(ChangeLanguageMenuKeyboard.query_back)
    async def process_settings_callback(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id)
        await bot.edit_message_text(
            ll(query.message.chat.id, SETTINGS),

            query.message.chat.id,
            query.message.message_id,
            query.inline_message_id,

            reply_markup=SettingsMenuKeyboard(query.message.chat.id)
        )

    @dp.callback_query_handler(ChangeLanguageMenuKeyboard.query_language)
    async def process_settings_callback(query: types.CallbackQuery):
        language = query.data.split('.')[-1]
        await lu(bot, query.message.chat.id, language)

        await bot.answer_callback_query(query.id)
        await bot.edit_message_text(
            ll(query.message.chat.id, SETTINGS),

            query.message.chat.id,
            query.message.message_id,
            query.inline_message_id,

            reply_markup=SettingsMenuKeyboard(query.message.chat.id)
        )
