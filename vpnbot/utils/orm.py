from os import environ


def get_database_uri() -> str:
    host = environ.get('POSTGRES_HOST')
    port = environ.get('POSTGRES_PORT')
    user = environ.get('POSTGRES_USER')
    password = environ.get('POSTGRES_PASSWORD')
    database = environ.get('POSTGRES_DB')

    if None not in (host, port, user, password, database):
        return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'

    return 'postgresql+asyncpg://tr30012:hackme@127.0.0.1:5432/vpnbot'


def get_database_pool_size() -> int:
    return 15


def get_database_pool_max_overflow() -> int:
    return 0


