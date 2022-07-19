from aiohttp import web
from aiohttp_apispec import docs


@docs(
    tags=["health-check"],
    summary="Simple health check",
    description="Check of bot api",
)
async def health(request: web.Request) -> web.Response:
    return web.json_response({"status": "OK"}, status=200)
