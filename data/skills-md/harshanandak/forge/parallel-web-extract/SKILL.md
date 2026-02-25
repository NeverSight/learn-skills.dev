---
name: parallel-web-extract
description: "Scrape and extract structured content from URLs using Parallel AI REST API (curl). Use for pricing pages, docs, product info. No binary install — requires PARALLEL_API_KEY in .env.local."
compatibility: Requires PARALLEL_API_KEY in .env.local. Uses curl.
metadata:
  author: harshanandak
  version: "1.0.0"
---

# Parallel Web Extract

Extract structured content from any URL using Parallel AI. Results in 5-30 seconds.

> **CLI alternative (recommended)**: Install `parallel-cli` for official skill:
> `npx skills add parallel-web/parallel-agent-skills --skill parallel-web-extract`

## Setup

```bash
API_KEY=$(grep "^PARALLEL_API_KEY=" .env.local | cut -d= -f2)
```

## Extract Request

```bash
curl -s -X POST "https://api.parallel.ai/v1beta/extract" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -H "parallel-beta: search-extract-2025-10-10" \
  -d '{
    "url": "https://example.com/pricing",
    "objective": "Extract all pricing plans and their features"
  }'
```

## When to Use

- Scrape a specific URL you already know
- Extract pricing, specs, or structured data from a page
- Get clean content from documentation sites

For finding URLs first, use `parallel-web-search` then extract.

## Error Handling

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Bad key | Check PARALLEL_API_KEY in .env.local |
| 400 | Invalid URL | Ensure URL is accessible |
| 429 | Rate limit | Wait 60s |
