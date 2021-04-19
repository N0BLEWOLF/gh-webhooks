import logging
import traceback

import uvicorn
from decouple import config
from fastapi import FastAPI, Request

# from pyrogram import (
#    Client,
#    __version__
# )
from telethon import TelegramClient

# from flask import Flask, request, Response

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

# tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)

# app = Flask("Kek")
app = FastAPI(debug=True)
print("Successfully deployed!")


@app.post("/webhook")
async def respond(request: Request):
    result = await request.json()
    tgbot = TelegramClient("kensur", api_id=APP_ID, api_hash=API_HASH)
    await tgbot.start(bot_token=BOT_TOKEN)
    # print(request.json)
    try:
        # check_s = result["check_suite"]
        # umm = check_s["app"]["head_commit"]
        if result.get("commits"):
            rng = len(result["commits"])
            if rng > 10:
                rng = 10
            for x in range(rng):
                commit = result["commits"][x]
                if len(escape(commit["message"])) > 300:
                    commit_msg = (commit["message"]).split("\n")[0]
                else:
                    commit_msg = escape(commit["message"])
                text = f"**{commit_msg}**\n[{commit['id'][:7]}]({commit['url']})\n{commit['author']['name']} <{commit['author']['email']}>"
                await tgbot.send_message(-1001237141420, text)
        elif result.get("pull_request"):
            pr_action = result["action"]
            pr = result["pull_request"]
            pull_r = pr["html_url"]
            pull_t = pr["title"]
            pr["body"]
            pull_commits = pr["commits_url"]
            pull_ts = pr["created_at"]
            pull_pusher = pr["user"]["login"]
            if pr_action == "opened":
                text = f"**Opened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts}\n[Commits]({pull_commits})"
            elif pr_action == "closed":
                text = f"**Closed Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts}\n[Commits]({pull_commits})"
            else:
                text = f"**Reopened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts}\n[Commits]({pull_commits})"
            await tgbot.send_message(-1001237141420, text)

        else:
            umm = result["head_commit"]
            commit_msg = umm["message"]
            commit_id = umm["id"]
            commit_url = umm["url"]
            commit_timestamp = umm["timestamp"]
            committer_name = umm["author"]["username"]
            committer_mail = umm["author"]["email"]
            await tgbot.send_message(
                -1001237141420,
                f"Commit: [{commit_id}]({commit_url})\nMessage: **{commit_msg}**\nTimeStamp: `{commit_timestamp}`\nCommiter: {committer_name} <{committer_mail}>",
            )
    except BaseException:
        traceback.print_exc()
    # return Response(status=200)


"""tgbot = Client("kensur",
                   api_id=APP_ID,
                   api_hash=API_HASH,
                   bot_token=BOT_TOKEN)"""

PORT = config("PORT")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), log_level="info")
