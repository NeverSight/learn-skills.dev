---
name: ddg-search
description: DuckDuckGo web search via CLI. Use when you need to search the web for information, research topics, find news, or discover resources. Supports text search, news search, and image search with JSON output for programmatic use.
---

# DDG Search

DuckDuckGo search CLI wrapper around the `ddgs` Python package.

## Usage

```bash
# Text search (default)
ddg "your search query"

# News search
ddg "your query" -t news

# Image search
ddg "your query" -t images

# JSON output (for scripting)
ddg "your query" --json

# Limit results
ddg "your query" -n 5

# Specific region
ddg "your query" -r us-en
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-t, --type` | Search type: text, news, images | text |
| `-n, --max-results` | Max results to return | 10 |
| `-r, --region` | Region code (e.g., us-en, de-de) | wt-wt (worldwide) |
| `--safe` | Safe search: on, moderate, off | moderate |
| `--json` | Output as JSON | false |

## Common Region Codes

- `wt-wt` - Worldwide
- `us-en` - United States
- `de-de` - Germany
- `gb-en` - United Kingdom
- `in-en` - India

## Script Location

`/root/clawd/ddg-skill/scripts/ddg`

## Dependencies

- Python 3.8+
- `ddgs` package (`pip install ddgs`)
