import sys
from os import environ


def get_bot_token() -> str:
    token = environ.get('TOKEN')

    if token is not None:
        return token

    try:
        return sys.argv[1]
    except IndexError:
        raise ValueError('You need to specify bot token.')
