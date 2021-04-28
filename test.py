import logging
import threading

from sanic import Sanic
from sanic.response import json
from telethon import TelegramClient

app = Sanic(name="MC")

APP_ID = 3512712
API_HASH = "4ff3477ad1d19aad032dc015f5d05a52"
TOKEN = "1767375736:AAF_oQ0mN8T2Zu8DtYZAUeX9ou5MyBQw_HQ"

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH).start(
    bot_token=TOKEN
)


@app.route("/omk")
async def test(request):
    return json({"hello": "world"})


@app.route("/")
async def fuck(request):
    om = await tgbot.send_message("The_Masoom_Bachha", "Hi")
    print(om)
    return json({"msg": "MC"})


if __name__ == "__main__":
    threading.Thread(target=app.run(host="0.0.0.0", port=8000), daemon=True).start()
    tgbot.run_until_disconnected()
