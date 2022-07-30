import fastapi
import uvicorn
from .routers import routers


def setup_fastapi() -> uvicorn.Server:
    app = fastapi.FastAPI(docs_url='/')

    for router in routers:
        app.include_router(router)

    config = uvicorn.Config(app, port=8000, log_level='info')
    server = uvicorn.Server(config)

    return server
