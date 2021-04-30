from fastapi import FastAPI, Request

from client import config, tgbot
import asyncio
import logging

from decouple import config
from aiohttp import web
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
APP_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("TOKEN")

print("OK?")

omkk = asyncio.get_event_loop()

dp = Dispatcher(tgbot)

app = FastAPI(debug=True)

print("Go Injoi!")


@app.get("/")
async def test(request: Request):
    return {"hello": "world"}


async def webh(request):
    s = await request.json()
    om = await tgbot.send_message(-1001237141420, "TEST")
    print(om)
    return web.json_response({"msg": "MC"})


PORT = config("PORT")
if __name__ == "__main__":
    app = web.Application()
    app.router.add_route("GET", "/webhook", webh)
