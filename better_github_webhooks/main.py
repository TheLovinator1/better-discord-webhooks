from discord_webhook import DiscordEmbed
from fastapi import FastAPI, Request

from better_github_webhooks.github.star import star
from better_github_webhooks.webhook import send_embed

app = FastAPI()


# TODO: Add support for ping/pong
@app.post("/webhook")
async def webhook(request: Request):
    # The JSON we get from GitHub
    response = await request.json()

    embed = DiscordEmbed(description=str(response))

    # Pretty print the JSON
    # print(json.dumps(response, indent=4, sort_keys=True))

    if "starred_at" in response:
        embed = star(response)

    # Send Webhook to Discord
    send_embed(embed)

    # Return a 200 OK
    # TODO: Add correct response that GitHub expects
    return {"status": "SUCCESS"}
