import os, praw

def fetch_reddit(subs, query_terms, limit=30):
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "saastack-agent/0.1 by u/yourname")

    if not (client_id and client_secret):
        return []

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        check_for_async=False,
    )
    reddit.read_only = True

    q = " OR ".join(query_terms)
    results = []
    for sub in subs:
        for post in reddit.subreddit(sub).search(q, sort="new", limit=limit):
            results.append({
                "source":"reddit","subreddit":sub,
                "title":post.title,
                "url":f"https://reddit.com{post.permalink}",
                "score":post.score,
                "created_utc":post.created_utc
            })
    return results
