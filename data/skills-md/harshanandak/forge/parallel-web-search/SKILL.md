---
name: parallel-web-search
description: "Web search using Parallel AI REST API (curl). Fast fact lookups, news, sources. No binary install — requires PARALLEL_API_KEY in .env.local."
compatibility: Requires PARALLEL_API_KEY in .env.local. Uses curl.
metadata:
  author: harshanandak
  version: "1.0.0"
---

# Parallel Web Search

Fast web search via Parallel AI REST API. Use for quick facts, news, finding sources. Results in 5-60 seconds.

> **CLI alternative (recommended)**: Install `parallel-cli` for official skill:
> `npx skills add parallel-web/parallel-agent-skills --skill parallel-web-search`

## Setup

```bash
# Load API key (Windows/Git Bash compatible)
API_KEY=$(grep "^PARALLEL_API_KEY=" .env.local | cut -d= -f2)
```

Get your key at https://platform.parallel.ai — add to `.env.local`:
```
PARALLEL_API_KEY=your-key-here
```

## Search Request

```bash
curl -s -X POST "https://api.parallel.ai/v1beta/search" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -H "parallel-beta: search-extract-2025-10-10" \
  -d '{
    "objective": "your search query here"
  }'
```

## Full Options

```json
{
  "objective": "Find current Bitcoin price",
  "search_queries": ["BTC price today"],
  "max_results": 5,
  "mode": "agentic",
  "source_policy": {
    "include_domains": ["bloomberg.com", "reuters.com"]
  }
}
```

## Response

```json
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "excerpt": "...",
      "relevance_score": 0.95
    }
  ]
}
```

## Source Filtering

Include only specific domains:
```json
{"source_policy": {"include_domains": ["arxiv.org", "nature.com"]}}
```

Exclude domains:
```json
{"source_policy": {"exclude_domains": ["reddit.com", "twitter.com"]}}
```

## When to Use

- Quick fact lookups, current prices, news
- Finding source URLs for further extraction
- Research queries where speed > depth

For deep analysis, use `parallel-deep-research` instead.

## Error Handling

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Bad key | Check PARALLEL_API_KEY in .env.local |
| 429 | Rate limit | Wait 60s, retry with backoff |
| 400 | Bad request | Validate JSON body |
