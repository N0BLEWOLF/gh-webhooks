from fastapi import FastAPI, Request

from client import config, tgbot
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from decouple import config

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
APP_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("TOKEN")
tgbot = Bot(token=BOT_TOKEN)

print("OK?")

omkk = asyncio.get_event_loop()

dp = Dispatcher(tgbot)

app = FastAPI(debug=True)

print("Go Injoi!")


@app.get("/")
async def test(request: Request):
    return {"hello": "world"}


@app.get("/omk")
async def fuck(request: Request):
    om = await tgbot.send_message(-1001237141420, "TEST")
    print(om)
    return {"msg": "MC"}


PORT = config("PORT")
if __name__ == "__main__":
    threading.Thread(target=executor.start_polling, args=(dp, skip_updates=True))
    uvicorn.run("test:app", host="0.0.0.0", port=int(PORT), log_level="info", reload=False)
