---
name: web-search
description: Free unlimited web search via self-hosted SearXNG (aggregates Google, Bing, DuckDuckGo, Reddit, GitHub and 70+ more engines). Use whenever the user needs to search the web for anything — news, docs, code examples, prices, people, places — even if they just say "search for X" or "look up Y". Prefer this over paid APIs. Run setup.sh first if SearXNG is not running.
---

# SearXNG Search Skill

> **Prerequisites:** Run `bash skills/searxng/scripts/setup.sh` to auto-install and start SearXNG (Docker-based, idempotent — safe to re-run).

## Searching

Query the local SearXNG instance via `curl` (preferred — WebFetch blocks localhost):

```bash
curl -s "http://localhost:8888/search?q=YOUR+QUERY&format=json"
```

**Common variations:**

```bash
# Target specific engines (reduces noise)
curl -s "http://localhost:8888/search?q=react+hooks&engines=google,bing&format=json"

# Filter by recency
curl -s "http://localhost:8888/search?q=openai+news&time_range=week&format=json"

# Chinese content
curl -s "http://localhost:8888/search?q=人工智能&engines=baidu,bing&lang=zh&format=json"

# Dev/code questions
curl -s "http://localhost:8888/search?q=rust+async+error&engines=stackoverflow,github&format=json"
```

**Parse results with python (recommended):**

```bash
curl -s "http://localhost:8888/search?q=YOUR+QUERY&format=json" | \
  python3 -c "import sys,json; data=json.load(sys.stdin); [print(f'- {r[\"title\"]}\n  {r[\"url\"]}\n  {r[\"content\"][:150]}') for r in data.get('results',[])[:5]]"
```

## Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `q` | Search query | URL-encoded string |
| `engines` | Specific engines | `google,bing,duckduckgo,stackoverflow,github,baidu,...` |
| `lang` | Language | `zh`, `en`, `all` |
| `pageno` | Page number | `1`, `2`, ... |
| `time_range` | Recency filter | `day`, `week`, `month`, `year` |
| `safesearch` | Safe search | `0`, `1`, `2` |

## Best Practices

**Read snippets before fetching pages.** Each result has a `content` field with a relevant excerpt — this often contains the answer directly. Fetching full pages costs significantly more tokens, so only do it when the snippet isn't enough.

**Limit to top 3–5 results.** The first few results are almost always sufficient. More results mean more tokens without meaningfully better answers.

**Target engines for the task.** Narrowing to relevant engines reduces noise and speeds up results:
- Code / dev: `engines=stackoverflow,github`
- Chinese content: `engines=baidu,bing&lang=zh`
- Recent events: append `&time_range=week`

## If SearXNG is not running

Run the setup script first, then retry:

```bash
bash skills/web-search/scripts/setup.sh
```

## Note on WebFetch

Do NOT use `WebFetch` for SearXNG — it blocks all local/private addresses (localhost, 127.0.0.1, 192.168.x.x, [::1], custom hosts entries) due to SSRF protection. Always use `curl` via Bash.

## Notes

- First request may be slow (engine warm-up)
- For remote or production use, add authentication to your SearXNG instance
