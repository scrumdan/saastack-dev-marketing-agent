import os
import requests
from urllib.parse import quote_plus

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def _serpapi_search(query, num=20):
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_KEY not set in .env")
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "num": num,
        "hl": "en",
        "api_key": SERPAPI_KEY,
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("organic_results", []) or []

def fetch_linkedin_posts(include_terms, max_results=25, include_pulse=False):
    """
    Finds public LinkedIn posts matching your include_terms using Google via SerpAPI.
    Returns lightweight items the rest of the pipeline can score.
    """
    # Build a query like: site:linkedin.com/posts term1 OR term2 OR ...
    q_terms = " OR ".join([f'"{t}"' for t in include_terms]) or ""
    queries = [f'site:linkedin.com/posts {q_terms}']
    if include_pulse:
        queries.append(f'site:linkedin.com/pulse {q_terms}')

    items = []
    seen_urls = set()

    for q in queries:
        results = _serpapi_search(q, num=max_results)
        for res in results:
            url = res.get("link") or ""
            if not url or "linkedin.com" not in url:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            title = res.get("title") or "(LinkedIn post)"
            snippet = res.get("snippet") or ""
            # Normalize into your item shape
            items.append({
                "source": "linkedin",
                "title": title,
                "url": url,
                "description": snippet,
                # LinkedIn doesn’t expose score; ranking handles None → 0
                "score": 0,
            })
    return items
