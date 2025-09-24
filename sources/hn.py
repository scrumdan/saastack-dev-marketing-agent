import requests, time

def fetch_hn(query_terms, hits_per_page=20):
    q = " OR ".join([f'"{t}"' for t in query_terms])
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": q, "tags": "story", "hitsPerPage": hits_per_page}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    items = []
    for h in r.json().get("hits", []):
        items.append({
            "source": "hn",
            "title": h.get("title"),
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "points": h.get("points", 0),
            "author": h.get("author"),
            "created_at": h.get("created_at"),
            "text": h.get("_highlightResult",{}).get("title",{}).get("value","")
        })
    time.sleep(0.4)
    return items
