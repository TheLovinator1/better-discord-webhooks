import os

from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

load_dotenv()

webhook_url: str = os.environ["WEBHOOK_URL"]


def send_webhook(json_from_github):
    json_action = json_from_github["action"]
    action = "something"
    thing = "something"

    if json_action == "deleted":
        action = "deleted"
    if json_action == "created":
        action = "created"
    if json_action == "started":
        action = "started"

    if "starred_at" in json_from_github:
        # Starboi
        if action == "created" or action == "started":
            thing = "starred ⭐ <:PogU:789631728180002816>"

        if action == "deleted":
            thing = "unstarred ⭐ <:Sadge:744182660515102722>"
    else:
        return

    repo_name = json_from_github["repository"]["full_name"]
    sender_name = json_from_github["sender"]["login"]
    msg = f"**{repo_name}** - {sender_name} {thing}"

    webhook = DiscordWebhook(url=webhook_url, content=msg)
    response = webhook.execute()
    print(response)
