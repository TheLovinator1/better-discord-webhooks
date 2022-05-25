import json

from fastapi import FastAPI, Request

from webhook_filter.webhook import send_webhook

app = FastAPI()


@app.post("/webhook")
async def webhook(hook: Request):
    # TODO: Add ping/pong
    # The JSON we get from GitHub
    response = await hook.json()

    # Pretty print the JSON
    print(json.dumps(response, indent=4, sort_keys=True))

    # Send Webhook to Discord
    send_webhook(response)

    # Return a 200 OK
    return {"status": "SUCCESS"}
