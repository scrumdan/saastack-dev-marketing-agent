# SaaStack Dev & Tech-Founder Marketing Agent (MVP)

Minimal human-in-the-loop **marketing agent** tuned for **developers** and **technical co-founders**.
- Sources: Hacker News, Reddit, GitHub
- Drafts replies → posts review cards to Slack
- Optional mini-app: **Approve & Post** to Reddit from Slack

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp config.example.yaml config.yaml
python run.py
```

If no relevant items are found, broaden `keywords.include` in `config.yaml`.

## Slack Mini‑App: Approve → Auto‑Post (Reddit)

1) **Create Slack App** (api.slack.com/apps → New App → From scratch)
- Add bot scope: `chat:write`
- Enable **Interactivity & Shortcuts** → set Request URL to `https://<YOUR-NGROK>.ngrok-free.app/slack/events`
- Install app → copy **Bot User OAuth Token** and **Signing Secret**

2) **.env additions**
```
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_CHANNEL_ID=C0123456789
```

3) **Run the mini-app**
```bash
export PORT=3000
python slack_app/app.py
# in another terminal:
ngrok http 3000
```

4) **Enable autopost + Reddit creds** (optional)
- In `config.yaml`:
```yaml
autopost:
  enabled: true
  reddit:
    allowed_subreddits: ["programming","devops","selfhosted","saas","startups"]
    min_score: 10
```
- In `.env`:
```
REDDIT_USERNAME=YourRedditUser
REDDIT_PASSWORD=your-password
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=saastack-agent/0.1 by u/YourRedditUser
```

## Files
```
.
├─ run.py
├─ requirements.txt
├─ prompts.py
├─ generate.py
├─ rank.py
├─ config.example.yaml → copy to config.yaml
├─ .env.example → copy to .env
├─ deliver/
│  ├─ slack.py          # interactive if bot token present; webhook fallback
│  └─ notion.py         # stub
├─ sources/
│  ├─ hn.py
│  ├─ reddit.py
│  └─ github.py
├─ posters/
│  └─ reddit_poster.py  # approve→post to Reddit
└─ slack_app/
   └─ app.py            # Slack Bolt + Flask mini-app
```

## License
MIT
