import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM, REPLY_TEMPLATE, ARTICLE_TEMPLATE

load_dotenv()
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm(system, prompt, temperature=0.4):
    resp = _client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
        temperature=temperature
    )
    return resp.choices[0].message.content.strip()

def draft_reply(item, product, cfg):
    prompt = REPLY_TEMPLATE.format(
        product_name=product["name"],
        claims="\n".join(product["key_claims"]),
        proof_points="\n".join(product["proof_points"]),
        links=str(product["links"]),
        thread_url=item.get("url",""),
        title=item.get("title","(no title)")
    )
    return llm(SYSTEM, prompt)

def draft_article(topic, persona, product):
    prompt = ARTICLE_TEMPLATE.format(persona=persona, topic=topic)
    return llm(SYSTEM, prompt)
