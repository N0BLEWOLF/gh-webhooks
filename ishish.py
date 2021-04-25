import traceback
from datetime import datetime

import requests
import uvicorn
from html import escape
from decouple import config
from fastapi import FastAPI, Request

# from pyrogram import (
#    Client,
#    __version__
# )
BOT_TOKEN = config("TOKEN")
# from flask import Flask, request, Response
print("Successfully deployed!")
app = FastAPI(debug=True)
API = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def post_tg(chat, message, parse_mode):
    """Send message to desired group"""
    response = requests.post(
        API + "sendMessage",
        params={
            "chat_id": chat,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        },
    ).json()
    return response


def better_time(text):
    try:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    except ValueError:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S+05:30")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    return cr_time


@app.post("/webhook")
async def respond(request: Request):
    result = await request.json()
    #    await tgbot.start(bot_token=BOT_TOKEN)
    # print(request.json)
    d_form = "%d/%m/%y || %H:%M"
    try:
        # check_s = result["check_suite"]
        # umm = check_s["app"]["head_commit"]
        if result.get("commits"):
            rng = len(result["commits"])
            if rng > 10:
                rng = 10
            for x in range(rng):
                commit = result["commits"][x]
                pull_ts = commit["timestamp"]
                str_time = better_time(pull_ts)
                if len((commit["message"])) > 300:
                    commit_msg = (commit["message"]).split("\n")[0]
                else:
                    commit_msg = commit["message"]
                text = f"<b>{escape(data['repository']['name'])}</b> - New {len(data['commits'])} commits ({escape(data['ref'].split('/')[-1])})\n{commit_msg}</b>\n[{commit['id'][:7]}]({commit['url']})\n<b>Commited at</b> {str_time}\n<b>Commited By:</b> {commit['author']['name']} <{commit['author']['email']}>"
                post_tg(-1001237141420, text, parse_mode="HTML")
        elif result.get("pull_request"):
            pr_action = result["action"]
            pr = result["pull_request"]
            pull_r = pr["html_url"]
            pull_t = pr["title"]
            pr["body"]
            pull_commits = pr["commits_url"]
            pull_ts = pr["created_at"]
            str_time = better_time(pull_ts)
            pull_pusher = pr["user"]["login"]
            if pr_action == "opened":
                text = f"**Opened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})"
            elif pr_action == "closed":
                text = f"**Closed Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})"
            else:
                text = f"**Reopened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})"
            post_tg(-1001237141420, text, parse_mode="markdown")
        elif result.get("action") == "started":
            repo_name = result["repository"]["name"]
            repo_url = result["repository"]["html_url"]
            stargiver_uname = result["sender"]["login"]
            stargiver_profile = result["sender"]["html_url"]
            total_stars = result["repository"]["stargazers_count"]
            text = f"🌟 [{stargiver_uname}]({stargiver_profile}) gave a star to [{repo_name}]({repo_url}).\nTotal 🌟Stars🌟 are now {total_stars}."
            post_tg(-1001237141420, text, parse_mode="markdown")
        else:
            return
            # IDK WHat
            # loop.run_until_complete()
    except BaseException:
        traceback.print_exc()


PORT = config("PORT")
if __name__ == "__main__":
    uvicorn.run("ishish:app", host="0.0.0.0", port=int(PORT), log_level="info")
