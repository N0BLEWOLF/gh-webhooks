import re
import traceback
from datetime import datetime
from html import escape

import github
from aiohttp import web
from bs4 import BeautifulSoup as bs
from decouple import config
from requests import get
from telethon import Button, events

from config import AUTH_CHATS, tgbot

print("Go Injoi!")


def better_time(text):
    try:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    except ValueError:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S+05:30")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    return cr_time


g = github.Github()


if re.search(" ", AUTH_CHATS):
    GB_grps = AUTH_CHATS.split(" ")
else:
    GB_grps = AUTH_CHATS


def better_time(text):
    try:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    except ValueError:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S+05:30")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    return cr_time


g = github.Github()


async def send_msg(chat, text, buttons=None, **kwargs):
    txt = text
    parse_mode = kwargs.get("parse_mode", "markdown")
    link_preview = False
    if isinstance(chat, list):
        for ch in chat:
            if buttons is not None:
                await tgbot.send_message(
                    int(ch),
                    txt,
                    buttons=buttons,
                    link_preview=link_preview,
                    parse_mode=parse_mode,
                )
            else:
                await tgbot.send_message(
                    int(ch), txt, link_preview=link_preview, parse_mode=parse_mode
                )
            break
    elif isinstance(chat, str) or isinstance(chat, int):
        if buttons is not None:
            await tgbot.send_message(
                int(chat),
                txt,
                buttons=buttons,
                link_preview=link_preview,
                parse_mode=parse_mode,
            )
        else:
            await tgbot.send_message(
                int(chat), txt, link_preview=link_preview, parse_mode=parse_mode
            )


@tgbot.on(events.CallbackQuery(pattern="stars_count"))
async def callback(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    stars = repo.stargazers_count
    await event.answer(f"Total 🌟Stars🌟 are {stars}.", alert=True)


@tgbot.on(events.CallbackQuery(pattern="forks_count"))
async def fucku(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    forks = repo.forks_count
    await event.answer(f"Total Forks are {forks} ⚡️.", alert=True)


@tgbot.on(events.CallbackQuery(pattern="pr_count"))
async def pcount(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    open_pr_count = 0
    closed_pr_count = 0
    total_prs = 0
    for r in repo.get_pulls(state="open"):
        open_pr_count += 1
    for r in repo.get_pulls(state="closed"):
        closed_pr_count += 1
    for r in repo.get_pulls(state="all"):
        total_prs += 1
    await event.answer(
        f"Total Open Pull Requests are {open_pr_count}.\nTotal Closed Pull Requests are {closed_pr_count}\n\nTotal Pull Requests are {total_prs}",
        alert=True,
    )


@tgbot.on(events.CallbackQuery(pattern="deploy_count"))
async def pcount(event):
    a = get("https://elements.heroku.com/buttons/teamultroid/ultroid").content
    b = bs(a, "html.parser", from_encoding="utf-8")
    c = b.find_all("span", "stats-value")
    msg = f"Ultroid - Total Deploys to heroku: {c[0].text}"
    await event.answer(msg, alert=True)


@tgbot.on(events.CallbackQuery(pattern="issue_count"))
async def pcount(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    issue_count = 0
    for r in repo.get_issues(state="open"):
        issue_count += 1
    await event.answer(f"Total Open Issues are: {issue_count}", alert=True)


@tgbot.on(events.NewMessage(pattern="^/stats"))
async def fucku(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    desc = repo.description
    lang = repo.language
    last_c = repo.last_modified
    watchers = repo.watchers_count
    license = repo.get_license().license.name
    text = f"**{repo.title} Stats**\n\n**Repo:** [Ultroid]({repo.html_url})\n**Description:** {desc}\n**Last Updated:** {last_c}\n**Language:** {lang}\n**Watchers:** {watchers}\n\n**License:** {license}\n\n\n#GithubBot"
    btns = [
        [
            Button.inline("🌟Stars🌟", b"stars_count"),
            Button.inline("🍴Forks", b"forks_count"),
        ],
        [
            Button.inline("Pull Requests", b"pr_count"),
            Button.inline("Issues", b"issue_count"),
        ],
        [
            Button.inline("Deploys", b"deploy_count"),
        ],
    ]
    await send_msg(event.chat_id, text, buttons=btns, link_preview=False)


async def respond(request):
    result = await request.json()
    #    await tgbot.start(bot_token=BOT_TOKEN)
    # print(request.json)
    d_form = "%d/%m/%y || %H:%M"

    try:
        # check_s = result["check_suite"]
        # umm = check_s["app"]["head_commit"]
        if result.get("commits"):
            commits_text = ""

            rng = len(result["commits"])
            if rng > 10:
                rng = 10
            for x in range(rng):
                commit = result["commits"][x]
                pull_ts = commit["timestamp"]
                str_time = better_time(pull_ts)
                commit_url = commit["url"]
                strr = commit["author"]["email"]
                Commiter = ""
                if re.search("noreply.github.com", strr):
                    strss = strr.split("+")
                    fk = strss[1].split("@")[0]
                    Commiter += fk
                elif commit["author"]["username"]:
                    Commiter += commit["author"]["username"]
                else:
                    users = g.search_users(commit["author"]["email"])
                    for user in users:
                        Commiter += user.login

                if len(escape(commit["message"])) > 300:
                    commit_msg = escape((commit["message"]).split("\n")[0])
                else:
                    commit_msg = commit["message"]

                btns = [
                    (
                        Button.url("View Commit", f"{str(commit_url)}"),
                        Button.url(
                            "Commited By",
                            f"https://github.com/{Commiter}",
                        ),
                    )
                ]
                if len(commits_text) > 1000:
                    commits_text += f"{commit_msg}\n<a href='{commit['url']}'>{commit['id'][:7]}</a> by {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
                    text = f"""✨ <b>{escape(result['repository']['name'])}</b> : New {len(result['commits'])} commits on {escape(result['ref'].split('/')[-1])} branch
{commits_text}#GithubBot"""
                    await send_msg(GB_grps, text, parse_mode="html", link_preview=False)
                else:
                    commits_text += f"{commit_msg}\n{commit['id'][:7]} by {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
                    text = f"""✨ <b>{escape(result['repository']['name'])}</b> : New {len(result['commits'])} commits to {escape(result['ref'].split('/')[-1])} branch
{commits_text}#GithubBot"""
                    await send_msg(
                        GB_grps,
                        text,
                        parse_mode="html",
                        buttons=btns,
                        link_preview=False,
                    )

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
                text = f"**Opened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#GithubBot"
            elif pr_action == "closed":
                text = f"**Closed Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#GithubBot"
            else:
                text = f"**Reopened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#GithubBot"
            await send_msg(GB_grps, text, parse_mode="markdown", link_preview=False)
        elif result.get("action") == "started":

            @tgbot.on(events.CallbackQuery(pattern="stars"))
            async def callback(event):
                total_stars = result["repository"]["stargazers_count"]
                await event.answer(f"Total 🌟Stars🌟 are now {total_stars} .", alert=True)

            repo_name = result["repository"]["name"]
            repo_url = result["repository"]["html_url"]
            stargiver_uname = result["sender"]["login"]
            stargiver_profile = result["sender"]["html_url"]
            result["repository"]["stargazers_count"]
            text = f"🌟 [{stargiver_uname}]({stargiver_profile}) starred [{repo_name}]({repo_url}).\n\n#GithubBot"
            await send_msg(
                GB_grps,
                text,
                parse_mode="markdown",
                buttons=Button.inline("Total Stars", b"stars"),
                link_preview=False,
            )
        elif result.get("forkee"):

            @tgbot.on(events.CallbackQuery(pattern="forks"))
            async def fucku(event):
                total_forks = result["repository"]["forks_count"]
                await event.answer(f"Total Forks are {total_forks} ⚡️ .", alert=True)

            repo_n = str(result["repository"]["name"])
            repo_url = str(result["repository"]["html_url"])
            forker_u = str(result["sender"]["login"])
            forker_p = str(result["sender"]["html_url"])
            text = f"""🍴[{forker_u}]({forker_p}) **forked** [{repo_n}]({repo_url})\n\n#GithubBot"""

            await send_msg(
                GB_grps,
                text,
                parse_mode="markdown",
                buttons=Button.inline("Total Forks", b"forks"),
                link_preview=False,
            )
        else:
            return
            # IDK WHat
            # loop.run_until_complete()
    except BaseException:
        traceback.print_exc()


PORT = config("PORT")
if __name__ == "__main__":
    app = web.Application()
    app.router.add_route("POST", "/webhook", respond)
    web.run_app(app, port=PORT)
