from decouple import config
#from telethon import Button, TelegramClient, events
from pyrogram import (
    Client,
    __version__
)
import logging
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

tgbot = Client(session_name="kensur", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
