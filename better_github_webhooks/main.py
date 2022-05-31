from fastapi import FastAPI, Request

from better_github_webhooks.github.issues import issues
from better_github_webhooks.github.push import pushed
from better_github_webhooks.github.star import star
from better_github_webhooks.webhook import send_embed

app = FastAPI()


# TODO: Add support for ping/pong
@app.post("/webhook")
async def webhook(request: Request):
    # The JSON we get from GitHub
    response = await request.json()
    x_github_event: str = request.headers.get("x-github-event")
    print(f"x-github-event: {x_github_event}")

    if x_github_event == "star":
        embed = star(response)
    elif x_github_event == "push":
        embed = pushed(response)
    elif x_github_event == "issues":
        embed = issues(response)

    # Send Webhook to Discord
    if embed:
        response = send_embed(embed)
        print(response)
        if response.status_code != 200:
            print(response.reason)

    # Return a 200 OK
    # TODO: Add correct response that GitHub expects
    return {"status": "SUCCESS"}
