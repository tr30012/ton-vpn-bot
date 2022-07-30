from .locales import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


class MainMenuKeyboard(InlineKeyboardMarkup):
    def __init__(self, chat_id: int, *args, **kwargs):
        super().__init__(*args, row_width=1, **kwargs)

        btn_settings = InlineKeyboardButton(
            ll(chat_id, INLINE_SETTINGS),
            callback_data='keyboard.inline.main-menu.settings'
        )

        btn_get_vpn = InlineKeyboardButton(
            ll(chat_id, INLINE_GET_VPN),
            callback_data='keyboard.inline.main-menu.getvpn'
        )

        self.add(btn_get_vpn, btn_settings)

    @staticmethod
    def query_settings(query: CallbackQuery) -> bool:
        return query.data == 'keyboard.inline.main-menu.settings'

    @staticmethod
    def query_vpn(query: CallbackQuery) -> bool:
        return query.data == 'keyboard.inline.main-menu.getvpn'


class SettingsMenuKeyboard(InlineKeyboardMarkup):
    def __init__(self, chat_id: int, *args, **kwargs):
        super().__init__(*args, row_width=1, **kwargs)

        btn_choose_language = InlineKeyboardButton(
            ll(chat_id, INLINE_CHANGE_LANGUAGE),
            callback_data='keyboard.inline.settings.choose-language'
        )

        btn_back = InlineKeyboardButton(
            ll(chat_id, INLINE_BACK),
            callback_data='keyboard.inline.settings.back'
        )

        self.add(btn_choose_language, btn_back)

    @staticmethod
    def query_language(query: CallbackQuery) -> bool:
        return query.data == 'keyboard.inline.settings.choose-language'

    @staticmethod
    def query_back(query: CallbackQuery) -> bool:
        return query.data == 'keyboard.inline.settings.back'


class ChangeLanguageMenuKeyboard(InlineKeyboardMarkup):
    def __init__(self, chat_id: int, *args, **kwargs):
        super().__init__(*args, row_width=2, **kwargs)

        btn_russian_language = InlineKeyboardButton(
            b'\xF0\x9F\x87\xB7\xF0\x9F\x87\xBA'.decode('utf-8') + " Русский",
            callback_data='keyboard.inline.settings.choose-language.ru'
        )

        btn_english_language = InlineKeyboardButton(
            b'\xF0\x9F\x87\xBA\xF0\x9F\x87\xB8'.decode('utf-8') + " English",
            callback_data='keyboard.inline.settings.choose-language.en'
        )

        btn_back = InlineKeyboardButton(
            ll(chat_id, INLINE_BACK),
            callback_data='keyboard.inline.settings.choose-language.back'
        )

        self.row(btn_russian_language, btn_english_language)
        self.add(btn_back)

    @staticmethod
    def query_back(query: CallbackQuery) -> bool:
        return query.data == 'keyboard.inline.settings.choose-language.back'

    @staticmethod
    def query_language(query: CallbackQuery) -> bool:
        return 'keyboard.inline.settings.choose-language.' in query.data
