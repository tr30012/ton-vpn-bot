import settings

from bot.dispatcher import create_dispatcher
from api.app import create_app
from db.pool import setup_async_pool

from aiohttp import web
from asyncio import get_event_loop
from aiogram.dispatcher.webhook import configure_app


def main():
    loop = get_event_loop()

    bot, dp = create_dispatcher(settings.TOKEN)

    app = create_app(bot=bot, dp=dp)

    configure_app(dp, app, '/bot')

    setup_async_pool(app, bot)

    loop.create_task(dp.start_polling())

    web.run_app(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        loop=loop
    )


if __name__ == "__main__":
    main()
