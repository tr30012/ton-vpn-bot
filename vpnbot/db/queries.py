from sqlalchemy import insert, exists
from db.schemas import users_table
from aiogram.types import User

from db.tokens import create_token


def insert_user_query(user: User):
    return (
        insert(users_table).
        values(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            api_token=create_token(),
            is_admin=0
        ))


def does_user_exists_query(user: User):
    return (
        exists(users_table).
        where(users_table.c.telegram_id == user.id).
        select()
    )

