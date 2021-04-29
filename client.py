import asyncio
import logging

from aiorun import run
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


async def main():
    await tgbot.start(bot_token=BOT_TOKEN)
    await tgbot.run_until_disconnected()


run(main())
