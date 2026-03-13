---
name: plurk
description: Read and respond to Plurk social network content — fetch your timeline, get individual plurks, view another user's public plurks, read responses to a plurk, and post responses. Requires OAuth credentials.
compatibility: Requires uv in PATH (for running the Python script). Set PLURK_APP_KEY, PLURK_APP_SECRET, PLURK_AUTH_TOKEN, PLURK_AUTH_SECRET env vars before use.
metadata:
  {
    "author": "akhy",
    "version": "1.0.0",
    "upstream": "https://www.plurk.com",
    "openclaw":
      {
        "emoji": "💬",
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

# Plurk Skill

Interact with [Plurk](https://www.plurk.com) via the [Plurk API 2.0](https://www.plurk.com/API).

## Prerequisites

Set these env vars before using this skill:

```bash
export PLURK_APP_KEY="your_consumer_key"
export PLURK_APP_SECRET="your_consumer_secret"
export PLURK_AUTH_TOKEN="your_access_token"
export PLURK_AUTH_SECRET="your_access_secret"
```

## Script

All operations go through `scripts/plurk.py`. Run from the repo root:

```bash
uv run plurk/scripts/plurk.py <command> [options]
```

Run without arguments or with `--help` to see full usage:

```bash
uv run plurk/scripts/plurk.py --help
```

## Operations

### Get your timeline

```bash
# Latest 20 plurks
uv run plurk/scripts/plurk.py timeline

# With options
uv run plurk/scripts/plurk.py timeline --limit 10
uv run plurk/scripts/plurk.py timeline --filter my
uv run plurk/scripts/plurk.py timeline --offset "2009-6-20T21:55:34"
```

**`--filter` values:** `my` | `responded` | `private` | `favorite` | `replurked` | `mentioned`

**Response:** `{ "plurks": [...], "plurk_users": { "<id>": {...} } }`

### Get a single plurk

```bash
uv run plurk/scripts/plurk.py get-plurk <plurk_id>
```

**Response:** `{ "plurks": {...}, "user": {...} }`

### Get another user's public timeline

```bash
uv run plurk/scripts/plurk.py public-timeline <user_id_or_nickname>
uv run plurk/scripts/plurk.py public-timeline alvin --limit 10
```

**Response:** `{ "plurks": [...], "plurk_users": { "<id>": {...} } }`

### Get responses for a plurk

```bash
uv run plurk/scripts/plurk.py responses <plurk_id>
uv run plurk/scripts/plurk.py responses <plurk_id> --from 5 --count 20
```

**Response:** `{ "responses": [...], "friends": {...}, "responses_seen": N }`

### Post a response

```bash
uv run plurk/scripts/plurk.py respond <plurk_id> <qualifier> <content>

# Example
uv run plurk/scripts/plurk.py respond 12345 says "Great post!"
```

**Qualifier values:** `says` · `thinks` · `feels` · `hopes` · `wishes` · `needs` · `will` · `is` · `wants` · `has` · `was` · `wonders` · `adores` · `hates` · `loves` · `likes` · `dislikes` · `asks` · `shares` · `knows` · `fears` · `replies`

**Response:** `{ "id": N, "content": "...", "qualifier": "...", "qualifier_translated": "..." }`

## Plurk Permalink

Each plurk has a public permalink. The `plurk_id` from the API is an integer — convert it to base36 to build the URL:

```
https://www.plurk.com/p/<plurk_id in base36>
```

**Python:**
```python
import numpy  # not needed — use built-in
def to_base36(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    while n:
        result = digits[n % 36] + result
        n //= 36
    return result or "0"

permalink = f"https://www.plurk.com/p/{to_base36(plurk_id)}"
```

**jq (requires external base conversion):**
```bash
# Extract plurk_id and build permalink via Python one-liner
uv run plurk/scripts/plurk.py get-plurk 12345 \
  | jq '.plurks.plurk_id' \
  | python3 -c "import sys; n=int(sys.stdin.read()); d='0123456789abcdefghijklmnopqrstuvwxyz'; r=''; \
    exec(\"while n: r=d[n%36]+r; n//=36\"); print(f'https://www.plurk.com/p/{r or 0}')"
```

## Rendering Avatars

User objects returned by the API include `id`, `has_profile_image`, and `avatar` fields. Use these to construct avatar URLs:

**User has a profile image (`has_profile_image == 1`):**

| `avatar` value | URL pattern |
|---|---|
| `null` | `https://avatars.plurk.com/{user_id}-{size}.gif` |
| number | `https://avatars.plurk.com/{user_id}-{size}{avatar}.gif` |

**Sizes:** `small` · `medium` · `big` (big uses `.jpg` instead of `.gif`)

**No profile image (`has_profile_image == 0`):**

```
https://www.plurk.com/static/default_small.jpg
https://www.plurk.com/static/default_medium.jpg
https://www.plurk.com/static/default_big.jpg
```

**jq helper to extract avatar URLs from timeline:**

```bash
uv run plurk/scripts/plurk.py timeline | jq '
  .plurk_users | to_entries[] | .value |
  {
    nick_name,
    avatar: (
      if .has_profile_image == 1 then
        if .avatar == null then
          "https://avatars.plurk.com/\(.id)-medium.gif"
        else
          "https://avatars.plurk.com/\(.id)-medium\(.avatar).gif"
        end
      else
        "https://www.plurk.com/static/default_medium.jpg"
      end
    )
  }
'
```

## Response Format

All responses are JSON. Use `jq` to extract fields:

```bash
# List plurk content and IDs from timeline
uv run plurk/scripts/plurk.py timeline | jq '.plurks[] | {id: .plurk_id, content: .content_raw}'

# Get response count for a plurk
uv run plurk/scripts/plurk.py get-plurk 12345 | jq '.plurks.response_count'

# List responses with author IDs
uv run plurk/scripts/plurk.py responses 12345 | jq '.responses[] | {user_id, content: .content_raw}'
```
