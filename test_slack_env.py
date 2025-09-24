import os
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

token = os.getenv("SLACK_BOT_TOKEN")
chan  = os.getenv("SLACK_CHANNEL_ID")
print("SLACK_BOT_TOKEN:", repr(token))
print("SLACK_CHANNEL_ID:", repr(chan))
print("TOKEN set?", bool(token), "CHANNEL set?", bool(chan))
client = WebClient(token=token)
resp = client.chat_postMessage(channel=chan, text="✅ Bot token & channel ID are working.")
print("OK?", resp.data.get("ok"), "ts:", resp.data.get("ts"))
