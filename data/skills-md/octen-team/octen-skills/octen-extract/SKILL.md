---
name: octen-extract
description: USE FOR extracting clean, LLM-ready content from one or more web page URLs, powered by Octen. Fetch 1-20 URLs in one call and get markdown/text content plus a page category, page-structure label, and (optionally) query-driven highlights. Use it for reading articles, scraping pages for RAG/grounding, summarization, or fact lookup from known URLs.
homepage: https://octen.ai
keywords: [extract, scrape, url, web page, content extraction, markdown, RAG, octen, read url]
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["curl"],"env":["OCTEN_API_KEY"]},"primaryEnv":"OCTEN_API_KEY"}, "homepage": "https://octen.ai", "support": "support@octen.ai"}
---

# Octen Extract

Turn one or more URLs into clean, LLM-ready content. Beyond the page body, each
result also carries a **category**, a **page-structure** label, and — when you
pass a `query` — **query-relevant highlights** instead of the full page.

> **Requires API Key**: Get one at https://octen.ai · Set it: `export OCTEN_API_KEY=your-api-key`

## API Key Setup

**Before extracting, ensure `OCTEN_API_KEY` is set. On `401`, stop and tell the user a key is required (https://octen.ai), help them configure it, then continue.** Configure the key for the relevant agent (same as other Octen skills):

- **Claude Code** — add `{ "env": { "OCTEN_API_KEY": "your-key" } }` to `~/.claude/settings.json`
- **Cursor / generic shell** — `export OCTEN_API_KEY="your-key"` in `~/.zshrc` or `~/.bashrc`
- **Codex** — `~/.codex/config.toml` → `[shell_environment_policy]`, `set = { OCTEN_API_KEY = "your-key" }`
- **OpenClaw** — add `OCTEN_API_KEY=your-key` to `~/.openclaw/.env`

## Endpoint

```http
POST https://api.octen.ai/extract
```

**Authentication**: `X-Api-Key: <API_KEY>` header · **Content-Type**: `application/json`

## Quick Start (cURL)

### Batch extract (full content)

```bash
curl -s -X POST "https://api.octen.ai/extract" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "urls": ["https://example.com", "https://octen.ai"],
    "format": "markdown"
  }'
```

### Query-driven highlights (instead of full content)

```bash
curl -s -X POST "https://api.octen.ai/extract" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "urls": ["https://en.wikipedia.org/wiki/Python_(programming_language)"],
    "query": "async programming"
  }'
```

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `urls` | string[] | **Yes** | - | 1–20 URLs to fetch in one batch |
| `query` | string | No | - | When set, each result returns query-relevant `highlights` and OMITS `full_content` (max 500 chars) |
| `max_age_seconds` | integer | No | `86400` | Accept cached results within this age (min 300); older cached versions are re-fetched |
| `format` | string | No | `markdown` | Content format: `markdown` or `text` |
| `timeout` | integer | No | `30` | Per-URL fetch budget in seconds (1–60) |
| `include_images` | boolean | No | `false` | Include image resources found on the page (also returns `cover_image` when the page has one) |
| `include_videos` | boolean | No | `false` | Include video URLs found on the page |
| `include_audio` | boolean | No | `false` | Include audio URLs found on the page |

## Response Format

| Field | Type | Description |
|--|--|--|
| `request_id` | string | Unique request identifier |
| `data.results[]` | array | One result per URL |
| `data.results[].url` | string | The URL |
| `data.results[].status` | string | `success` or `failed` |
| `data.results[].error_message` | string? | Why it failed (when `status` = failed) |
| `data.results[].title` | string? | Page title |
| `data.results[].full_content` | string? | Cleaned page content (when no `query`) |
| `data.results[].highlights` | string[]? | Query-relevant snippets (when `query` is set) |
| `data.results[].category` | object? | `{primary, secondary}` — what the page is about |
| `data.results[].page_structure` | object? | `{primary, secondary}` — what kind of page it is |
| `data.results[].time_published` | string? | Publish time, ISO 8601 |
| `data.results[].time_last_crawled` | string? | Last crawl time, ISO 8601 |
| `data.results[].favicon` | string? | Page favicon URL — returned by default when available |
| `data.results[].cover_image` | object? | `{url}` — page cover image (when `include_images` is true and the page has one) |
| `data.results[].images` / `videos` / `audio` | — | Media resources (when the matching `include_*` is true) |
| `meta.usage.total_urls` | integer | URLs requested |
| `meta.usage.successful_urls` | integer | URLs successfully fetched |

## Error Codes

| HTTP Status | Description |
|--|--|
| `400` | Missing or invalid parameter |
| `401` | Invalid or missing API key |
| `403` | Insufficient balance |
| `429` | Rate limited |
| `500` | Internal server error |

## Notes

- **Partial success is first-class**: a failed URL is returned with `status: "failed"` + an `error_message`; sibling URLs in the same batch still succeed. Always check per-result `status`.
- Pass `query` only when you want focused `highlights` for RAG/grounding; omit it to get the full cleaned page.
- `category` and `page_structure` let you route or filter pages (e.g., skip an index/operation page, keep a content page) without reading the whole body.
