import os
import settings


def create_token():
    return os.urandom(settings.API_TOKEN_LENGTH).hex()
