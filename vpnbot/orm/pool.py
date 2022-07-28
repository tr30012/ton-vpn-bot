import asyncio
import logging

from collections import AsyncIterable
from aiogram import types

from sqlalchemy import select
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

from vpnbot.orm.queries import does_user_exists_query, insert_user_query
from vpnbot.utils.orm import get_database_uri, get_database_pool_size, get_database_pool_max_overflow


class AsyncExecute(AsyncIterable):
    __slots__ = (
        'query', 'connection', 'cls_'
    )

    def __init__(self, connection: AsyncConnection, query: Select, cls_: type):
        self.connection = connection
        self.query = query
        self.cls_ = cls_

    async def __aiter__(self):
        for row in await self.connection.execute(self.query):
            yield self.cls_(row)


def setup_async_pool() -> AsyncEngine:
    logging.info("Creating connection pool.")

    engine: AsyncEngine = create_async_engine(
        get_database_uri(),
        pool_size=get_database_pool_size(),
        max_overflow=get_database_pool_max_overflow(),
        poolclass=QueuePool,
    )

    async def check_engine():
        async with engine.connect() as connection:
            await connection.execute(select(1))
            logging.info("Successfully created.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_engine())

    return engine


async def db_first_message(pool: AsyncEngine, message: types.Message):
    async with pool.connect() as connection:
        result = (await connection.execute(
            does_user_exists_query(message.from_user)
        )).scalar()

        if not result:
            await connection.execute(
                insert_user_query(message.from_user)
            )
            await connection.commit()
