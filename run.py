import yaml
from dotenv import load_dotenv
from sources.hn import fetch_hn
from sources.reddit import fetch_reddit
from sources.github import search_github_repos
from sources.linkedin import fetch_linkedin_posts
from rank import topk
from generate import draft_reply
from deliver.slack import send_to_slack, review_card

from pathlib import Path
import json
SEEN_FILE = Path("state/seen_urls.json")
seen = set(json.loads(SEEN_FILE.read_text())) if SEEN_FILE.exists() else set()

def load_cfg():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def gather(cfg):
    terms_incl = cfg["keywords"]["include"]
    items = []
    try:
        items += fetch_hn(terms_incl)
        print(f"[gather] HN: {len(items)} total")
    except Exception as e:
        print("[gather] HN error:", e)
    try:
        ritems = fetch_reddit(["programming","devops","startups","saas","selfhosted"], terms_incl)
        items += ritems
        print(f"[gather] Reddit: {len(ritems)}; total {len(items)}")
    except Exception as e:
        print("[gather] Reddit error:", e)
    try:
        gitems = search_github_repos(" ".join(terms_incl))
        items += gitems
        print(f"[gather] GitHub: {len(gitems)}; total {len(items)}")
    except Exception as e:
        print("[gather] GitHub error:", e)
    try:
        litems = fetch_linkedin_posts(terms_incl, max_results=20)
        items += litems
        print(f"[gather] LinkedIn: {len(litems)}; total {len(items)}")
    except Exception as e:
        print("[gather] LinkedIn error:", e)
    # Deduplicate by URL
    deduped = {}
    for item in items:
        url = item.get("url")
        if url and url not in deduped:
            deduped[url] = item
    return list(deduped.values())

def main():
    load_dotenv()
    cfg = load_cfg()
    terms_incl = cfg["keywords"]["include"]
    terms_excl = cfg["keywords"]["exclude"]
    product = cfg["product"]

    items = gather(cfg)
    top = topk(items, terms_incl, terms_excl, k=5)
    if not top:
        print("No relevant items found.")
        return


    for it in top:
        reply = draft_reply(it, product, cfg)
        blocks = review_card(it, reply, interactive=True)
        send_to_slack(blocks)

if __name__ == "__main__":
    main()
