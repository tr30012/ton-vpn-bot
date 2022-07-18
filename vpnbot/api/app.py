from aiohttp import web
from api.handler import handler
from settings import create_logger

logger = create_logger("app.creator")


def create_app(**kwargs) -> web.Application:
    logger.info("Creating app.")

    app = web.Application()
    app.add_routes([web.post("/api", handler)])

    for kwarg in kwargs:
        app[kwarg] = kwargs[kwarg]

    return app
