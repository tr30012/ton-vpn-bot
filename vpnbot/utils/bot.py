import sys


def get_bot_token() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        raise ValueError('You need to specify bot token.')
