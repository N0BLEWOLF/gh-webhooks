import logging
import threading

from sanic import Sanic
from sanic.response import json
from telethon import TelegramClient
from client import tgbot
app = Sanic(name="MC")

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
