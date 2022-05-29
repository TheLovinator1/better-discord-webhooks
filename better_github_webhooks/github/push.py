"""One or more commits are pushed to a repository branch or tag.

Note: You will not receive a webhook for this event when you push more
than three tags at once.

Availability:
    Repository webhooks
    Organization webhooks
    GitHub Apps with the contents permission
"""
from discord_webhook import DiscordEmbed


def pushed(response):
    repo_name = response["repository"]["full_name"]
    repo_url = response["repository"]["html_url"]
    num_commits = len(response["commits"])

    commit_list = []
    for commit in response["commits"]:
        commit_message = commit["message"]
        commit_message_split = commit_message.split("\n")
        url = commit["url"]
        sha = commit["id"][:7]
        field_row = f"[{sha}]({url})  {commit_message_split[0]}"
        commit_list.append(field_row)

        print(field_row)

    embed = DiscordEmbed(
        description="\n".join(commit_list),
        url=repo_url,
        title=f"{repo_name} - {num_commits} new commit{'' if num_commits == 1 else 's'}!",  # noqa: E501, pylint: disable=line-too-long
    )

    # Username and avatar of the user who pushed to the repository
    username = response["sender"]["login"]
    avatar = response["sender"]["avatar_url"]
    embed.set_author(name=username, icon_url=avatar)

    # Return the embed so it can be sent to Discord in the main function
    return embed
