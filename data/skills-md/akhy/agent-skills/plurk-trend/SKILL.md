---
name: plurk-trend
description: Show trending plurks from the last 24 hours — top plurks ranked by number of responses, descending. Builds on the plurk skill. Useful for discovering popular or viral content on Plurk.
compatibility: Requires uv in PATH. Set PLURK_APP_KEY, PLURK_APP_SECRET, PLURK_AUTH_TOKEN, PLURK_AUTH_SECRET env vars before use. See the plurk skill for credential setup.
metadata:
  {
    "author": "akhy",
    "version": "1.0.0",
    "upstream": "https://www.plurk.com",
    "depends-on": "plurk",
    "openclaw":
      {
        "emoji": "📈",
        "homepage": "https://www.plurk.com",
        "requires": { "bins": ["uv"], "env": ["PLURK_APP_KEY", "PLURK_APP_SECRET", "PLURK_AUTH_TOKEN", "PLURK_AUTH_SECRET"] },
        "primaryEnv": "PLURK_APP_KEY",
        "install":
          [
            {
              "id": "brew-uv",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Plurk Trend Skill

Fetch and rank the most-responded-to plurks from your timeline in the last 24 hours.

Depends on the **plurk** skill for credentials and API access.

## Prerequisites

Same env vars as the `plurk` skill:

```bash
export PLURK_APP_KEY="your_consumer_key"
export PLURK_APP_SECRET="your_consumer_secret"
export PLURK_AUTH_TOKEN="your_access_token"
export PLURK_AUTH_SECRET="your_access_secret"
```

## Script

```bash
uv run plurk-trend/scripts/plurk_trend.py [--top N] [--since DURATION]
```

- `--top N` — number of trending plurks to show (default: 10)
- `--since DURATION` — time window in Go-style duration (default: `24h`)
- `--min-responses N` — exclude plurks with fewer than N responses (default: 1)

**Duration format:** combine `h` (hours), `m` (minutes), `s` (seconds) — e.g. `24h`, `6h`, `1h30m`, `90m`, `30s`

## How It Works

1. Paginates through your timeline collecting all plurks within the given time window
2. Excludes plurks with zero responses
3. Sorts remaining plurks by `response_count` descending
4. Returns the top N

## Output Format

JSON array of plurk objects:

```json
[
  {
    "plurk_id": 123456,
    "permalink": "https://www.plurk.com/p/abc1",
    "posted": "Fri, 05 Jun 2009 23:07:13 GMT",
    "plurker": "Alvin Lim (@alvin)",
    "qualifier": "says",
    "content_raw": "Hello world!",
    "content": "Hello world!",
    "response_count": 42
  }
]
```

## Formatting Suggestions

When presenting results to a user, apply these rules:

**Content:** Use `content_raw` for plain-text mediums (terminal, chat, markdown). Use `content` only when the medium renders HTML and inline images.

**Plurker name:** Already formatted as `display_name (@nick_name)` in the output.

**Responses:** Show as a count, e.g. `42 responses`.

**Permalink:** Included in output as `permalink` — use it to link directly to the plurk.

### Example rendered output

```
#1 — 42 responses
Alvin Lim (@alvin) says:
Hello world!
https://www.plurk.com/p/abc1

#2 — 37 responses
...
```

### jq helpers

```bash
# Default top 10, last 24h
uv run plurk-trend/scripts/plurk_trend.py

# Top 5, last 6 hours
uv run plurk-trend/scripts/plurk_trend.py --top 5 --since 6h

# Only plurks with at least 5 responses
uv run plurk-trend/scripts/plurk_trend.py --min-responses 5

# Last 1.5 hours
uv run plurk-trend/scripts/plurk_trend.py --since 1h30m

# Last 90 minutes
uv run plurk-trend/scripts/plurk_trend.py --since 90m

# Plain text summary
uv run plurk-trend/scripts/plurk_trend.py | jq -r '
  to_entries[] |
  "#\(.key + 1) — \(.value.response_count) responses\n\(.value.plurker) \(.value.qualifier):\n\(.value.content_raw)\n\(.value.permalink)\n"
'
```
