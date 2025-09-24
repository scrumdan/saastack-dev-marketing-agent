import os, re, json
from pathlib import Path
import praw

STATE = Path("state/posted_reddit.json")

def _get_submission_id(permalink_or_url: str):
    m = re.search(r"/comments/([a-z0-9]+)/", permalink_or_url)
    return m.group(1) if m else None

def _load_posted():
    if STATE.exists():
        try:
            return set(json.loads(STATE.read_text()))
        except Exception:
            return set()
    return set()

def _save_posted(ids: set):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(list(ids))))

def post_comment(item: dict, reply_text: str, cfg: dict):
    reddit_cfg = cfg.get("autopost", {}).get("reddit", {})
    allowed = set([s.lower() for s in reddit_cfg.get("allowed_subreddits", [])])
    min_score = int(reddit_cfg.get("min_score", 5))

    sub = item.get("subreddit", "").lower()
    if allowed and sub not in allowed:
        return False, f"skip: subreddit r/{sub} not allowed"
    if item.get("score", 0) < min_score:
        return False, f"skip: score {item.get('score', 0)} < {min_score}"

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")
    user_agent = os.getenv("REDDIT_USER_AGENT", "saastack-agent/0.1 by u/youruser")

    if not all([client_id, client_secret, username, password]):
        return False, "missing reddit credentials (need CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD)"

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
        check_for_async=False,
    )
    reddit.read_only = False

    sid = _get_submission_id(item.get("url",""))
    if not sid:
        return False, "skip: cannot parse submission id"

    already = _load_posted()
    if sid in already:
        return False, "skip: already commented on this submission"

    if reply_text.count("http") > 1:
        return False, "skip: more than one link detected"

    try:
        submission = reddit.submission(id=sid)
        c = submission.reply(reply_text)
        already.add(sid)
        _save_posted(already)
        return True, f"https://reddit.com{c.permalink}"
    except Exception as e:
        return False, f"reddit error: {e}"
