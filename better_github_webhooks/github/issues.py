"""Activity related to an issue.

Availability
    Repository webhooks
    Organization webhooks
    GitHub Apps with the issues permission
"""
from better_github_webhooks.diff import get_diff
from discord_webhook import DiscordEmbed


def issue_opened(embed: DiscordEmbed):
    pass


def issue_closed(embed: DiscordEmbed):
    pass


def issue_reopened(embed: DiscordEmbed):
    pass


def issue_transferred(embed: DiscordEmbed):
    pass


def issue_locked(embed: DiscordEmbed):
    pass


def issue_unlocked(embed: DiscordEmbed):
    pass


def issue_labeled(embed: DiscordEmbed):
    pass


def issue_unlabeled(embed: DiscordEmbed):
    pass


def issue_assigned(embed: DiscordEmbed):
    pass


def issue_unassigned(embed: DiscordEmbed):
    pass


def issue_pinned(embed: DiscordEmbed):
    pass


def issue_unpinned(embed: DiscordEmbed):
    pass


def issue_deleted(embed: DiscordEmbed):
    pass


def issue_edited(response) -> str:
    """Get the diff between the before and after so we can use in in the
    embed.

    Args:
        response (_type_): The response from the webhook.

    Returns:
        str: The diff between the before and after. ```json is code tag
        with colors.
    """
    before = response["changes"]["body"]["from"]
    after = response["issue"]["body"]

    msg = get_diff(before, after)
    print(msg)

    return msg


def issue_milestoned(embed: DiscordEmbed):
    pass


def issue_demilestoned(embed: DiscordEmbed):
    pass


def issues(response):
    action = response["action"]

    repo_name = response["repository"]["full_name"]
    repo_url = response["repository"]["html_url"]

    issue_number = response["issue"]["number"]
    issue_title = response["issue"]["title"]
    issue_body = response["issue"]["body"]

    embed = DiscordEmbed(
        title=f"{repo_name} - Issue {action}: #{issue_number} {issue_title}",
        description=issue_body,
        url=repo_url,
    )

    if action == "opened":
        embed.color = 45572  # Green

    elif action == "closed":
        embed.color = 262322  # Red

    elif action == "reopened":
        issue_reopened(embed)

    elif action == "transferred":
        issue_transferred(embed)

    elif action == "locked":
        issue_locked(embed)

    elif action == "unlocked":
        issue_unlocked(embed)

    elif action == "labeled":
        issue_labeled(embed)

    elif action == "unlabeled":
        issue_unlabeled(embed)

    elif action == "assigned":
        issue_assigned(embed)

    elif action == "unassigned":
        issue_unassigned(embed)

    elif action == "pinned":
        issue_pinned(embed)

    elif action == "unpinned":
        issue_unpinned(embed)

    elif action == "deleted":
        issue_deleted(embed)

    elif action == "edited":
        msg = issue_edited(response)
        embed.description = msg

    elif action == "milestoned":
        issue_milestoned(embed)

    elif action == "demilestoned":
        issue_demilestoned(embed)

    # Username and avatar of the user who pushed to the repository
    username = response["sender"]["login"]
    avatar = response["sender"]["avatar_url"]
    embed.set_author(name=username, icon_url=avatar)

    # Return the embed so it can be sent to Discord in the main function
    return embed
