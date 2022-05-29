import os

from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv

load_dotenv(verbose=True)

webhook_url: str = os.environ["WEBHOOK_URL"]


def send_embed(embed: DiscordEmbed):
    webhook = DiscordWebhook(
        url=webhook_url,
        username="GitHub",
        avatar_url="https://lovinator.space/GitHub_logo.png",
        rate_limit_retry=True,
    )
    webhook.add_embed(embed)
    return webhook.execute()


def send_webhook(msg: str):
    webhook = DiscordWebhook(
        url=webhook_url,
        username="GitHub",
        avatar_url="https://lovinator.space/GitHub_logo.png",
        content=msg,
        rate_limit_retry=True,
    )
    return webhook.execute()
