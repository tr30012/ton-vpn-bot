from sqlalchemy.ext.asyncio import AsyncConnection

from vpnbot.orm.pool import setup_async_engine


engine = setup_async_engine()


async def connection_pool() -> AsyncConnection:
    connection: AsyncConnection = await engine.connect()

    try:
        yield connection
    finally:
        await connection.close()

