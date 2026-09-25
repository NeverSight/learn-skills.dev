---
name: octen-video-search
description: USE FOR finding web videos by a text query, powered by Octen. Returns ranked videos with the matched segment (start/end timestamps), duration, cover image, source page, and author. In Beta. Contact us to request beta access at https://octen.ai. Use it when the user wants to find videos, clips, tutorials, or a specific moment within video content.
homepage: https://octen.ai
keywords: [video search, video, octen, find videos, clips, tutorials, segment search, AI search]
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl"],"env":["OCTEN_API_KEY"]},"primaryEnv":"OCTEN_API_KEY"}, "homepage": "https://octen.ai", "support": "support@octen.ai"}
---

# Octen Video Search

Find web videos by a text query. Each result includes the **matched segment**
(start/end timestamps within the video), duration, cover image, source page, and
author — so you can jump straight to the relevant moment.

> **In Beta. Contact us to request beta access.** Octen Video Search is in
> invite-only beta — request access via https://octen.ai (or support@octen.ai).
> Calls will fail without access; if so, tell the user it's in beta and how to
> reach Octen.

## API Key Setup

**Before searching, ensure `OCTEN_API_KEY` is set. If it is missing — or any call returns `401` — stop and do not retry blindly: tell the user a key is required, point them to https://octen.ai, help them configure it for their agent, then continue once it's set. A `403` means the key is valid but the request was refused — either no beta access or insufficient account balance; relay both possibilities and how to request beta access.**

Configure the key for the relevant agent (same as other Octen skills):

- **Claude Code** — add `{ "env": { "OCTEN_API_KEY": "your-key" } }` to `~/.claude/settings.json`
- **Cursor / generic shell** — `export OCTEN_API_KEY="your-key"` in `~/.zshrc` or `~/.bashrc`
- **Codex** — `~/.codex/config.toml` → `[shell_environment_policy]`, `set = { OCTEN_API_KEY = "your-key" }`
- **OpenClaw** — add `OCTEN_API_KEY=your-key` to `~/.openclaw/.env`

## Endpoint

```http
POST https://api.octen.ai/video-search
```

**Authentication**: `X-Api-Key: <API_KEY>` header · **Content-Type**: `application/json`

## Quick Start (cURL)

```bash
curl -s -X POST "https://api.octen.ai/video-search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "inputs": [{"type": "text", "data": "how to tie a tie"}],
    "count": 5
  }'
```

### With Time Filtering

```bash
curl -s -X POST "https://api.octen.ai/video-search" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${OCTEN_API_KEY}" \
  -d '{
    "inputs": [{"type": "text", "data": "GPT-5 launch keynote"}],
    "count": 10,
    "time_range": "month"
  }'
```

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `inputs` | array | **Yes** | - | One text input: `[{"type": "text", "data": "<query>"}]` (query max 500 chars) |
| `count` | integer | No | `5` | Number of results (1–10) |
| `time_range` | string | No | - | Relative time window: `day`, `week`, `month`, `year` (or `d`, `w`, `m`, `y`) |
| `start_time` | string | No | - | Start time filter, ISO 8601 |
| `end_time` | string | No | - | End time filter, ISO 8601 (must be after `start_time`) |
| `safesearch` | string | No | `strict` | Adult content filter: `off` or `strict` |

## Response Format

| Field | Type | Description |
|--|--|--|
| `request_id` | string | Unique request identifier |
| `data.results[]` | array | List of video results |
| `data.results[].title` | string | Video title |
| `data.results[].url` | string | Video URL |
| `data.results[].source_page` | string | Page the video was found on |
| `data.results[].description` | string? | Video description |
| `data.results[].cover_url` | string? | Cover/thumbnail image URL |
| `data.results[].duration_seconds` | integer? | Total video duration in seconds |
| `data.results[].match_segment` | object? | Matched segment `{start_seconds, end_seconds}` |
| `data.results[].authors` | string? | Channel / author |
| `data.results[].time_published` | string? | Publish time, ISO 8601 |
| `data.results[].time_last_crawled` | string? | Last crawl time, ISO 8601 |
| `meta.latency` | number | Response time in milliseconds |
| `meta.warning` | string? | Warning message, if any |

## Error Codes

| HTTP Status | Description |
|--|--|
| `400` | Missing or invalid parameter |
| `401` | Invalid or missing API key |
| `403` | Insufficient balance, or no beta access |
| `429` | Rate limited |
| `500` | Internal server error |

## Notes

- Input is **text only** today (`{"type": "text", "data": "..."}`).
- `match_segment` gives the timestamps of the most relevant moment — surface them so the user can jump straight to it.
- `count` is capped at 10.
