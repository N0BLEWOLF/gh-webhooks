import asyncio
import threading
import traceback

from flask import Flask

from tg import BOT_TOKEN, tgbot

loop = asyncio.get_event_loop()

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def index(res):
    result = res.json
    try:
        # check_s = result["check_suite"]
        # umm = check_s["app"]["head_commit"]
        if result.get("commits"):
            rng = len(result["commits"])
            if rng > 10:
                rng = 10
            for x in range(rng):
                commit = result["commits"][x]
                if len((commit["message"])) > 300:
                    commit_msg = (commit["message"]).split("\n")[0]
                else:
                    commit_msg = commit["message"]
                text = f"**{commit_msg}**\n[{commit['id'][:7]}]({commit['url']})\n{commit['author']['name']} <{commit['author']['email']}>"
                loop.run_until_complete(await tgbot.send_message(-1001237141420, text))
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

            loop.run_until_complete(
                await tgbot.send_message(int("-1001237141420"), text)
            )

        else:
            umm = result["head_commit"]
            commit_msg = umm["message"]
            commit_id = umm["id"]
            commit_url = umm["url"]
            commit_timestamp = umm["timestamp"]
            committer_name = umm["author"]["username"]
            committer_mail = umm["author"]["email"]
            loop.run_until_complete(
                await tgbot.send_message(
                    -1001237141420,
                    f"Commit: [{commit_id}]({commit_url})\nMessage: **{commit_msg}**\nTimeStamp: `{commit_timestamp}`\nCommiter: {committer_name} <{committer_mail}>",
                )
            )
    except BaseException:
        traceback.print_exc()


if __name__ == "__main__":
    threading.Thread((app.run(host="0.0.0.0", debug=True)), daemon=True).start()
    tgbot.start(BOT_TOKEN)
    tgbot.run_until_disconnected()
