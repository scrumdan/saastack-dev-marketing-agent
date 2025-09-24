SYSTEM = """You are a senior platform engineer writing credibly for developers.
No hype. Prefer specifics, code, and measured claims. If uncertain, say so.
Brand voice: developer-honest, concise, friendly."""

REPLY_TEMPLATE = """Context:
- Product: {product_name}
- Claims: {claims}
- Proof: {proof_points}
- Link(s): {links}
- Thread URL: {thread_url}
- Post Title: {title}

Task:
Draft a short reply that:
1) Acknowledges the OP’s real pain using concrete language.
2) Offers a specific technique or example (no fluff).
3) Mentions {product_name} only if truly relevant; never hard sell.
4) Includes ONE optional link (if appropriate), else no link.
5) 80–120 words, markdown-plain, no emojis, no exclamation marks."""

ARTICLE_TEMPLATE = """Audience: {persona}
Goal: Draft a 600–800 word technical post with a runnable example.
Topic: {topic}
Include:
- Problem framing grounded in real engineering tradeoffs
- Minimal code sample (language: TypeScript or Python)
- Benchmarks or time-saved estimates with assumptions stated
- Clear 'When NOT to use this' section
Tone: candid, senior engineer explaining to peers."""
