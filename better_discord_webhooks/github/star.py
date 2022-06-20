"""Activity related to a repository being starred."""
from datetime import datetime

from discord_webhook import DiscordEmbed


def star(response):
    msg = response
    repo_name = response["repository"]["full_name"]
    repo_url = response["repository"]["html_url"]
    repo_name_and_url = f"[{repo_name}]({repo_url})"

    # The action performed. Can be created or deleted.
    if response["action"] == "created":
        msg = f"**{repo_name_and_url}** ⭐ added"
    elif response["action"] == "deleted":
        msg = f"**{repo_name_and_url}** ⭐ removed"

    embed = DiscordEmbed(description=msg)

    starred_at: str | None = response["starred_at"]
    if starred_at is not None:
        # Convert starred_at to a datetime object
        utc_dt = datetime.strptime(starred_at, "%Y-%m-%dT%H:%M:%SZ")
        # Convert UTC datetime to seconds since epoch
        timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
        embed.set_timestamp(timestamp)
    else:
        # Use current time instead of reading from GitHub webhook
        embed.set_timestamp()

    # Username and avatar of the user who un/starred the repository
    username = response["sender"]["login"]
    avatar = response["sender"]["avatar_url"]
    embed.set_author(name=username, icon_url=avatar)

    # Total number of stars, stargazer instead of stargazers if singular
    total_stars = response["repository"]["stargazers_count"]
    footer_text = f"{total_stars} stargazer{'' if total_stars == 1 else 's'}"
    embed.set_footer(text=footer_text)

    # Return the embed so it can be sent to Discord in the main function
    return embed
