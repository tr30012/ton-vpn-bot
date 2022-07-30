import logging
import sys
import asyncio

from os import environ

__uvloop = True

try:
    import uvloop
except ImportError:
    __uvloop = False


def get_bot_token() -> str:
    token = environ.get('TOKEN')

    if token is not None:
        return token

    try:
        return sys.argv[1]
    except IndexError:
        raise ValueError('You need to specify bot token.')


def setup_event_loop() -> asyncio.AbstractEventLoop:
    if __uvloop:
        uvloop.install()

    logging.info(f'Setting up event loop with policy: {asyncio.get_event_loop_policy()}')

    return asyncio.get_event_loop()
