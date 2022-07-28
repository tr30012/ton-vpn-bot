def get_database_uri() -> str:
    return 'postgresql+asyncpg://tr30012:hackme@127.0.0.1:5432/vpnbot'


def get_database_pool_size() -> int:
    return 15


def get_database_pool_max_overflow() -> int:
    return 0


