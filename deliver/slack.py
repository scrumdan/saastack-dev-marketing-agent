import os, json, requests
from typing import List, Dict

try:
    from slack_sdk import WebClient
except Exception:
    WebClient = None

def _web_client():
    token = os.getenv("SLACK_BOT_TOKEN")
    if WebClient and token:
        return WebClient(token=token)
    return None

def review_card(item, reply_text, interactive: bool = True) -> List[Dict]:
    title = item.get('title','').strip() or '(no title)'
    url = item.get('url','').strip() or ''
    source = (item.get('source','') or '').upper()

    blocks = [
      {"type":"section","text":{"type":"mrkdwn","text":f"*Source:* {source}  •  *Title:* {title}\n<{url}>"}},
      {"type":"section","text":{"type":"mrkdwn","text":f"*Draft reply:*\n{reply_text}"}},
    ]
    if interactive:
      blocks += [{
        "type":"actions","elements":[
           {"type":"button","text":{"type":"plain_text","text":"Approve & Post"},"style":"primary","action_id":"approve_and_post"}
        ]
      }]
    blocks += [{"type":"divider"}]
    return blocks

def send_to_slack(blocks: List[Dict]):
    client = _web_client()
    channel = os.getenv("SLACK_CHANNEL_ID")

    if client and channel:
        try:
            resp = client.chat_postMessage(channel=channel, blocks=blocks, text="New drafts to review")
            return resp
        except Exception:
            pass

    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        raise RuntimeError("No Slack credentials: set SLACK_BOT_TOKEN+SLACK_CHANNEL_ID or SLACK_WEBHOOK_URL")
    r = requests.post(webhook, data=json.dumps({"blocks":blocks}), headers={"Content-Type":"application/json"}, timeout=15)
    r.raise_for_status()
    return {"ok": True, "via": "webhook"}
