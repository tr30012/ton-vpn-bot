import os


def create_token():
    return os.urandom(16).hex()
