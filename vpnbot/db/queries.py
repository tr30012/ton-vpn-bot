from sqlalchemy import insert, exists, select, update
from sqlalchemy.sql import Update, Select, Insert

from db.schemas import users_table
from aiogram.types import User

from db.tokens import create_token


def insert_user_query(user: User) -> Insert:
    language_code = 'ru' if user.language_code == 'ru' else 'en'

    return (
        insert(users_table).
        values(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=language_code,
            api_token=create_token(),
            is_admin=0
        ))


def does_user_exists_query(user: User) -> Select:
    return (
        exists(users_table).
        where(users_table.c.telegram_id == user.id).
        select()
    )


def select_users_languages() -> Select:
    return select(users_table.c.telegram_id, users_table.c.language_code)


def update_user_language(telegram_id: int, language_code: str) -> Update:
    return (
        update(users_table).
        where(users_table.c.telegram_id == telegram_id).
        values(language_code=language_code)
    )
