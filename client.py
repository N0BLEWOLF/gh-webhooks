import asyncio
import logging

from aiorun import run
from decouple import config
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
APP_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("TOKEN")
tgbot = Bot(token=BOT_TOKEN)

print("OK?")

omkk = asyncio.get_event_loop()

dp = Dispatcher(bot)

executor.start_polling(dp, skip_updates=True))
