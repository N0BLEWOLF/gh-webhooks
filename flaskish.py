import io
import os
import logging
import random
import sys
import subprocess
import traceback
import threading
import uvicorn
import requests
from decouple import config
#from pyrogram import (
#    Client,
#    __version__
#)
BOT_TOKEN = config("TOKEN")
from fastapi import FastAPI,Request
#from flask import Flask, request, Response
print("Successfully deployed!")
app = FastAPI(debug=True)
API = f'https://api.telegram.org/bot{BOT_TOKEN}/'
def post_tg(chat, message, parse_mode):
    """Send message to desired group"""
    response = requests.post(
        API + "sendMessage",
        params={
            "chat_id": chat,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True}).json()
    return response

@app.post('/webhook')
async def respond(request: Request):
    result = await request.json()
#    await tgbot.start(bot_token=BOT_TOKEN)
    #print(request.json)
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
                commit_ts = commit["timestamp"]
                if len((commit["message"])) > 300:
                    commit_msg = (commit["message"]).split("\n")[0]
                else:
                    commit_msg = commit["message"]
                text = f"**{commit_msg}**\n[{commit['id'][:7]}]({commit['url']})\n**Commited at**{commit_ts.stfrtime(d_form)}\n{commit['author']['name']} <{commit['author']['email']}>"
                post_tg(-1001237141420, text, parse_mode="markdown")
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
                text = f"**Opened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts.stfrtime(d_form)}\n[Commits]({pull_commits})"
            elif pr_action == "closed":
                text = f"**Closed Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts.stfrtime(d_form)}\n[Commits]({pull_commits})"
            else:
                text = f"**Reopened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {pull_ts.stfrtime(d_form)}\n[Commits]({pull_commits})"

             post_tg(-1001237141420, text, parse_mode="markdown")
		elif data.get('action') == "started":
			text = f"🌟 {data['sender']['html_url']} {data['sender']['login']} gave a star to [{data['repository']['name']}]({data['repository']['html_url']})"
			post_tg(-1001237141420, text, parse_mode="markdown")
        else:
            umm = result["head_commit"]
            commit_msg = umm["message"]
            umm["id"]
            umm["url"]
            umm["timestamp"]
            umm["author"]["username"]
            umm["author"]["email"]
            # loop.run_until_complete()
    except BaseException:
        traceback.print_exc()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), log_level="info")
