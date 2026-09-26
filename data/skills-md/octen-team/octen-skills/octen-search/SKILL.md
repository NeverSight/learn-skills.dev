---
name: octen-search
description: USE FOR web search. Real-time web search for AI agents powered by Octen. Fast, fresh, and relevant — returns ranked results with highlights, full content, domain filtering, and time filtering. Average response under 80ms with minute-level index freshness. Also supports broad (multi-query) search that fans one question into several sub-queries for comprehensive coverage.
homepage: https://octen.ai
keywords: [web search, search, octen, real-time search, web, news, research, LLM search, AI search]
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl"],"env":["OCTEN_API_KEY"]},"primaryEnv":"OCTEN_API_KEY"}, "homepage": "https://octen.ai", "support": "support@octen.ai"}
---

# Octen Search

Octen's search skill. It provides real-time **web search** plus **broad
(multi-query) search** (see [Broad Search](#broad-search) below). Image and
video search live in the separate **octen-image-search** and
**octen-video-search** skills.

> **Requires API Key**: Get one at https://octen.ai
>
> Set it: `export OCTEN_API_KEY=your-api-key`

## API Key Setup

**Before searching, ensure `OCTEN_API_KEY` is set. If it is missing — or any call returns `401` — stop and do not retry blindly: tell the user a key is required, point them to https://octen.ai to get one, help them configure it for their agent (below), then continue once it's set.**

Configure the key for the relevant agent/runtime:

- **Claude Code** — add `{ "env": { "OCTEN_API_KEY": "your-key" } }` to `~/.claude/settings.json` (a transient shell `export` will not persist)
- **Cursor / Hermes / generic shell** — `export OCTEN_API_KEY="your-key"` in `~/.zshrc` or `~/.bashrc`
- **Codex** — `~/.codex/config.toml` → `[shell_environment_policy]`, `set = { OCTEN_API_KEY = "your-key" }`
- **OpenClaw** — add `OCTEN_API_KEY=your-key` to `~/.openclaw/.env`

See the [README](https://github.com/Octen-Team/octen-skills#prerequisites) for full per-agent instructions.

## Quick Start (cURL)

### Basic Search
```bash
curl -s -X POST "https://api.octen.ai/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{"query": "latest AI research 2026", "count": 5}'
```

### With Highlight and Time Filtering
```bash
curl -s -X POST "https://api.octen.ai/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "query": "summary judgment",
    "count": 10,
    "time_basis": "published",
    "start_time": "2025-01-01T00:00:00Z",
    "end_time": "2026-01-01T00:00:00Z",
    "highlight": {"enable": true, "max_tokens": 300}
  }'
```

### With Domain Filtering
```bash
curl -s -X POST "https://api.octen.ai/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "query": "climate change policy",
    "count": 5,
    "include_domains": ["nature.com", "science.org"],
    "exclude_domains": ["spam.com"]
  }'
```

### With Language Filtering
```bash
curl -s -X POST "https://api.octen.ai/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "query": "climate change 2026",
    "count": 5,
    "language": ["ja", "zh"]
  }'
```

### With Full Content
```bash
curl -s -X POST "https://api.octen.ai/search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "query": "latest WHO guidance on influenza vaccination",
    "count": 5,
    "full_content": {"enable": true, "max_tokens": 1000}
  }'
```

## Endpoint

```http
POST https://api.octen.ai/search
```

**Authentication**: `X-Api-Key: <API_KEY>` header

**Content-Type**: `application/json`

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `query` | string | **Yes** | - | Search query (max 500 chars) |
| `topic` | string | No | `general` | Search vertical: `general` or `news` |
| `count` | integer | No | `5` | Number of results (1–100) |
| `include_domains` | string[] | No | - | Only include results from these domains (max 1200 domains, each max 60 chars) |
| `exclude_domains` | string[] | No | - | Exclude results from these domains (max 1200 domains, each max 60 chars) |
| `include_text` | string[] | No | - | Strings that must appear in result page text (max 5 items, each max 30 chars) |
| `exclude_text` | string[] | No | - | Strings that must not appear in result page text (max 5 items, each max 30 chars) |
| `language` | string[] | No | `[]` | Filter results to these languages, as ISO 639-1 codes (e.g. `["en", "ja"]`). Supported: `ar`, `de`, `en`, `es`, `fr`, `hi`, `id`, `it`, `ja`, `ko`, `nl`, `pl`, `pt`, `ru`, `th`, `tr`, `vi`, `zh`. Empty = no language filter. See https://localizely.com/iso-639-1-list/ |
| `time_basis` | string | No | `auto` | Time field used for filtering: `auto`, `published`, `crawled` |
| `start_time` | string | No | - | Start time filter, ISO 8601 (e.g. `2025-01-01T00:00:00Z`) |
| `end_time` | string | No | - | End time filter, ISO 8601 (must be after `start_time`) |
| `highlight` | object | No | `{"enable": true}` | Highlight options (see below) |
| `format` | string | No | `text` | Output format for highlights: `text` or `markdown` |
| `safesearch` | string | No | `strict` | Adult content filter: `off` or `strict` |
| `full_content` | object | No | `{"enable": false}` | Full content options (see below) |
| `include_images` | boolean | No | `false` | Return the page's cover image and in-body images per result (see Response Fields). For searching *for* images, use the octen-image-search skill instead |

### Highlight Options

| Field | Type | Default | Description |
|--|--|--|--|
| `enable` | boolean | `true` | Return query-relevant highlights in each result |
| `max_tokens` | integer | `512` | Max tokens per highlight (100–20000) |

### Full Content Options

| Field | Type | Default | Description |
|--|--|--|--|
| `enable` | boolean | `false` | Return full raw page content for each result |
| `max_tokens` | integer | `2048` | Max tokens per result (100–100000) |

## Response Format

### Response Fields

| Field | Type | Description |
|--|--|--|
| `code` | integer | Status code. `0` = success |
| `msg` | string | Human-readable status message |
| `request_id` | string | Unique request identifier |
| `data.query` | string | The original query |
| `data.results[]` | array | List of search results |
| `data.results[].title` | string | Page title |
| `data.results[].url` | string | Page URL |
| `data.results[].highlight` | string? | Query-relevant snippets (when `highlight.enable` is true) |
| `data.results[].full_content` | string? | Full page content (when `full_content.enable` is true) |
| `data.results[].authors` | string? | Website name or author |
| `data.results[].time_published` | string? | Publish time, ISO 8601 |
| `data.results[].time_last_crawled` | string? | Last crawl time, ISO 8601 |
| `data.results[].favicon` | string? | Favicon URL of the result site |
| `data.results[].cover_image` | object? | Page cover image `{url, description}` (when `include_images` is true and the page has one) |
| `data.results[].images[]` | array? | In-body images of the page as `{url, description}`, in order of appearance (when `include_images` is true) |
| `meta.usage.num_search_queries` | integer | Number of search queries executed |
| `meta.usage.full_content_tokens` | integer | Total tokens returned in full_content |
| `meta.latency` | number | Response time in milliseconds |
| `meta.warning` | string? | Warning message, if any |

### JSON Example

```json
{
  "code": 0,
  "msg": "success",
  "request_id": "req_abc123def456",
  "data": {
    "query": "latest WHO guidance on influenza vaccination",
    "results": [
      {
        "title": "Influenza (Seasonal) - World Health Organization (WHO)",
        "url": "https://www.who.int/news-room/fact-sheets/detail/influenza-(seasonal)",
        "highlight": "WHO recommends annual vaccination for high-risk groups\n\n...\n\nSeasonal influenza vaccination policies vary by region...",
        "authors": "World Health Organization",
        "time_published": "2024-10-15T00:00:00Z",
        "time_last_crawled": "2026-01-20T02:12:34Z"
      }
    ]
  },
  "meta": {
    "usage": {
      "num_search_queries": 1,
      "full_content_tokens": 0
    },
    "latency": 237,
    "warning": null
  }
}
```

## Broad Search

**Broad Search** expands your query into several related sub-queries from
different angles, searches them concurrently, and returns results **grouped per
sub-query** (not deduplicated across groups) — ready to ground a complete answer.

**Use it when** a single `/search` only reaches a few of the relevant subtopics:
- **Comparisons** across many sources (pricing, products, vendors)
- **Surveys / deeper research**
- **Multi-angle questions** that have more than one facet

For a single focused lookup, use plain `/search` instead.

**Pass the original query as-is** — Octen generates the sub-queries for you, so
do **not** rewrite or pre-split the question into multiple calls; to widen
coverage, raise `max_queries` (default `5`; up to `30` for surveys/research,
lower for a tighter search).

### Endpoint

```http
POST https://api.octen.ai/broad-search
```

### Example

```bash
curl -s -X POST "https://api.octen.ai/broad-search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "query": "compare cloud GPU pricing across major providers",
    "max_queries": 5,
    "search_options": {"count": 10, "highlight": {"enable": true}}
  }'
```

### Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `query` | string | **Yes** | - | Original search query (max 500 chars) |
| `max_queries` | integer | No | `5` | Upper bound on the number of sub-queries generated (1–30); raise toward 30 for surveys/research, lower for a tighter search |
| `search_options` | object | No | - | Options applied to **each** sub-query — same fields and defaults as the [Parameters](#parameters) table above (`topic`, `count`, `include_domains`, `language`, time filters, `highlight`, `full_content`, `include_images`, …) |

### Response

Same envelope (`code`, `msg`, `request_id`, `meta`) as Search. `data` contains:

| Field | Type | Description |
|--|--|--|
| `data.query` | string | The original query |
| `data.queries[]` | string[] | The generated sub-queries |
| `data.search_results[]` | array | One result group per sub-query |
| `data.search_results[].query` | string | The sub-query for this group |
| `data.search_results[].results[]` | array | Results for that sub-query (same shape as Search `data.results[]`) |
| `data.search_results[].latency` | integer | Latency for that sub-query, in milliseconds |

## Error Codes

| HTTP Status | Description |
|--|--|
| `400` | Missing or invalid parameter |
| `401` | Invalid or missing API key |
| `403` | Insufficient balance |
| `429` | Rate limited |
| `500` | Internal server error |

## Security

- API key is sent **only** to the hardcoded endpoint `https://api.octen.ai/search` via HTTPS
- Authentication uses the standard `X-Api-Key` header
- No environment variables are sent to any other endpoints or external services

## Notes

- **Highlight** is enabled by default — set `"highlight": {"enable": false}` to disable
- **Full content** is disabled by default — enable it to get raw page text for RAG/grounding
- Use `include_domains` / `exclude_domains` to scope results to trusted sources
- Use `language` (ISO 639-1 codes, e.g. `["ja", "zh"]`) to filter results by language — on Broad Search set it **inside `search_options`**, not top-level
- Use `start_time` / `end_time` with `time_basis` to filter by publish or crawl time
- `format: "markdown"` returns highlights in markdown; `format: "text"` returns plain text
