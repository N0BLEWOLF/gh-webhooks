import logging
import threading
import traceback

import uvicorn
from decouple import config
from fastapi import FastAPI, Request

from telethon import TelegramClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH)

tgbot.start(bot_token=BOT_TOKEN)
