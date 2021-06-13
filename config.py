import logging

from decouple import config
from telethon import TelegramClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
APP_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("TOKEN")
AUTH_CHATS = config("AUTH_CHATS")
tgbot = TelegramClient(None, APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

print("OK?")
