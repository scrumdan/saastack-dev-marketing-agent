import os, requests

def search_github_repos(query, per_page=20):
    url = "https://api.github.com/search/repositories"
    headers = {}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    params = {"q": query, "sort":"stars", "order":"desc", "per_page": per_page}
    r = requests.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    out=[]
    for item in r.json().get("items",[]):
        out.append({
            "source":"github","full_name":item.get("full_name"),
            "stars":item.get("stargazers_count",0),
            "url":item.get("html_url"),
            "description":item.get("description","") or ""
        })
    return out
