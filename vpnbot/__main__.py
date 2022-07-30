from vpnbot.api.app import setup_fastapi
from vpnbot.bot.dispatcher import create_dispatcher
from vpnbot.orm.pool import setup_async_engine
from vpnbot.utils.bot import setup_event_loop, get_bot_token


def main():
    loop = setup_event_loop()

    bot, dispatcher = create_dispatcher(get_bot_token())
    bot['engine'] = setup_async_engine()
    api = setup_fastapi()

    loop.create_task(dispatcher.start_polling())
    loop.run_until_complete(api.serve())


if __name__ == '__main__':
    main()
