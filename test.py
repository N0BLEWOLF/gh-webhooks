import threading

from sanic import Sanic
from sanic.response import json

from client import tgbot

app = Sanic(name="MC")


@app.route("/omk")
async def test(request):
    return json({"hello": "world"})


@app.route("/")
async def fuck(request):
    om = await tgbot.send_message(-1001237141420, "TEST")
    print(om)
    return json({"msg": "MC"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
