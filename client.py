import asyncio
import logging

from decouple import config
from telethon import TelegramClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
APP_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("TOKEN")
tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH)
print("OK?")
omkk = asyncio.get_event_loop()
tgbot.start(bot_token=BOT_TOKEN)
omkk.run_until_complete(tgbot.run_until_disconnected())
