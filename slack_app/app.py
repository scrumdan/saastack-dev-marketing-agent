import os, re, yaml
from flask import Flask, request, make_response
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
from posters.reddit_poster import post_comment as reddit_autopost

load_dotenv()

bolt_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)
app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

def extract_item_and_reply_from_blocks(blocks):
    item = {}; reply_text = ""
    if not blocks or len(blocks) < 2: return item, reply_text
    try:
        t1 = blocks[0]["text"]["text"]
        m_url = re.search(r"<(https?://[^>]+)>", t1)
        if m_url:
            url = m_url.group(1)
            item["url"] = url
            if "reddit.com" in url:
                item["source"] = "reddit"
                m_sub = re.search(r"/r/([A-Za-z0-9_]+)/", url)
                if m_sub:
                    item["subreddit"] = m_sub.group(1)
        m_title = re.search(r"\*Title:\* (.+)\n", t1)
        if m_title:
            item["title"] = m_title.group(1).strip()
        item.setdefault("score", 100)
    except Exception:
        pass
    try:
        t2 = blocks[1]["text"]["text"]
        reply_text = re.sub(r"^\*Draft reply:\*\n", "", t2).strip()
    except Exception:
        pass
    return item, reply_text

@bolt_app.action("approve_and_post")
def handle_approve(ack, body, client, logger):
    ack()
    channel = body.get("channel",{}).get("id")
    ts = body.get("message",{}).get("ts")
    blocks = body.get("message",{}).get("blocks", [])
    user = body.get("user",{}).get("id","")

    item, reply_text = extract_item_and_reply_from_blocks(blocks)
    if not item or not reply_text:
        client.chat_postEphemeral(channel=channel, user=user, text="Could not parse draft content.")
        return

    cfg = yaml.safe_load(open("config.yaml"))
    if not cfg.get("autopost", {}).get("enabled"):
        client.chat_postEphemeral(channel=channel, user=user, text="Autopost disabled in config.yaml")
        return

    ok, info = (False, "unsupported source")
    if item.get("source") == "reddit":
        ok, info = reddit_autopost(item, reply_text, cfg)

    status_line = f"✅ *Approved & posted:* {info}" if ok else f"⚠️ *Approval failed:* {info}"
    try:
        client.chat_update(channel=channel, ts=ts, blocks=blocks + [
            {"type":"context","elements":[{"type":"mrkdwn","text":status_line}]}
        ])
    except Exception as e:
        logger.error(f"chat_update failed: {e}")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@app.route("/", methods=["GET"])
def health():
    return make_response("OK", 200)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, debug=False) #was True
