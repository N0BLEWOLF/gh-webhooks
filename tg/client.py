from decouple import config
from telethon import Button, TelegramClient, events
import logging
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

tgbot = TelegramClient("kensur", APP_ID, API_HASH)

tgbot.start(bot_token=BOT_TOKEN)

if __name__ == "__main__":
    tgbot.run_until_disconnected()
