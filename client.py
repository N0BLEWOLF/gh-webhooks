import logging
from telethon import TelegramClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH).start(
    bot_token=TOKEN
)

tgbot.run_until_disconnected()
