import asyncio
import settings

from collections import AsyncIterable
from aiogram import Bot, types
from sqlalchemy import select
from sqlalchemy.pool import QueuePool
from aiohttp.web import Application
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

from db.queries import does_user_exists_query, insert_user_query

logger = settings.create_logger("database")


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


def setup_async_pool(app: Application, bot: Bot):
    logger.info("Creating connection pool.")

    engine: AsyncEngine = create_async_engine(
        settings.DBURI,
        pool_size=settings.POOL_SIZE,
        max_overflow=settings.POOL_MAX_OVERFLOW,
        poolclass=QueuePool,
        echo=settings.POOL_ECHO
    )

    async def check_engine():
        async with engine.connect() as connection:
            await connection.execute(select(1))
            logger.info("Successfully created.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_engine())

    app['pool'] = engine
    bot['pool'] = engine


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





