import re, math

def score_item(item, include_terms, exclude_terms):
    text = " ".join([str(item.get(k,"")) for k in ("title","text","description")]).lower()

    # Exclusions
    for x in exclude_terms:
        if re.search(rf"\\b{re.escape(x.lower())}\\b", text):
            return -1

    # Keyword hits
    kw_score = sum(1 for t in include_terms if re.search(rf"\\b{re.escape(t.lower())}\\b", text))

    # Social/log signals
    social = item.get("points") or item.get("score") or item.get("stars") or 0
    s_log = math.log1p(max(0, social))

    return kw_score * 2 + s_log

def topk(items, include_terms, exclude_terms, k=15):
    scored = [(score_item(i, include_terms, exclude_terms), i) for i in items]
    scored = [x for x in scored if x[0] >= 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in scored[:k]]
