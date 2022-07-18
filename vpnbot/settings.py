import json
import logging
import os.path

config: dict = {}

with open('config.json', 'r') as fs:
    config.update(json.load(fs))

TOKEN = config['token']
LOGLEVEL = config['log.level']
LOGPATH = config['log.path']
LANGUAGE = config['language']
API_HOST = config['api.host']
API_PORT = config['api.port']
API_TOKEN_LENGTH = config['api.token.length']
DBURI = config['db.connection.uri']
POOL_SIZE = config['db.pool.size']
POOL_MAX_OVERFLOW = config['db.pool.max-overflow']
POOL_ECHO = config['db.pool.echo']

if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(LOGPATH + f"/{name}.log")

    cf_format = logging.Formatter('%(process)d - %(asctime)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(cf_format)
    f_handler.setFormatter(cf_format)

    f_handler.setLevel(logging.WARNING)

    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    logger.setLevel(LOGLEVEL)

    return logger


# TODO! Query database for user languages
def load_chats_languages() -> dict:
    return {}
