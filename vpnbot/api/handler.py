from aiohttp import web


async def handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "OK"}, status=200)
