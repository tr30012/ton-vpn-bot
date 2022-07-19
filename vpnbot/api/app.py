from aiohttp import web
from api.handler import health
from settings import create_logger
from aiohttp_apispec import setup_aiohttp_apispec

logger = create_logger("app.creator")


def create_app(**kwargs) -> web.Application:
    logger.info("Creating app.")

    app = web.Application()
    app.add_routes([web.post("/health", health)])

    setup_aiohttp_apispec(
        app=app, title="VPN Bot API", swagger_path="/"
    )

    for kwarg in kwargs:
        app[kwarg] = kwargs[kwarg]

    return app
