import io
import logging
import random
import sys
import traceback

import redis
import requests
from decouple import config
from telethon import Button, TelegramClient, events
from flask import Flask, request, Response

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

tgbot = TelegramClient("Botzhub", APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

app = Flask("Kek")

print("Successfully deployed!")

@app.route('/webhook', methods=['POST'])
async def respond():
    result = request.json
    #print(request.json)
    try:
        check_s = result["check_suite"]
        umm = check_s["app"]["head_commit"]
        commit_msg = umm["message"]
        commit_id = umm["id"]
        commit_timestamp = umm["timestamp"]
        committer_name = umm["committer"]["name"]
        committer_mail = umm["committer"]["email"]
        async def start(event):
            await tgbot.send_message(-1001237141420,
                f"Commit: `{commit_id}`\nMessage: *{commit_msg}*\nTimeStamp: `{commit_timestamp}`\nCommiter: {committer_name} <{committer_email}>"
    except:
        import traceback
        traceback.print_exc()
    return Response(status=200)
app.run(host="0.0.0.0", port=80)
