import logging

from aiogram import Bot, Dispatcher, types
from decouple import config

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

bot = Bot(token=BOT_TOKEN)
tgbot = Dispatcher(bot)
# tgbot.start(bot_token=BOT_TOKEN)
