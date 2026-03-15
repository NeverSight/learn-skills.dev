---
name: weibo-cli
description: Use weibo-cli for ALL Weibo (微博) operations — keyword search, hot search, trending topics, timelines, weibo details, comments, reposts, user profiles, and follower/following lists. Invoke whenever user requests any Weibo interaction.
author: jackwener
version: "0.2.1"
tags:
  - weibo
  - sina
  - 微博
  - social-media
  - cli
---

# weibo-cli — Weibo CLI Tool

**Binary:** `weibo`
**Credentials:** browser cookies (auto-extracted) or QR code login

## Setup

```bash
# Install (requires Python 3.10+)
git clone git@github.com:jackwener/weibo-cli.git
cd weibo-cli && uv sync
```

## Authentication

**IMPORTANT FOR AGENTS**: Before executing ANY weibo command, check if credentials exist first. Do NOT assume cookies are configured.

### Step 0: Check if already authenticated

```bash
weibo status 2>/dev/null && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to [Command Reference](#command-reference).
If `AUTH_NEEDED`, proceed to Step 1.

### Step 1: Guide user to authenticate

**Method A: Browser cookie extraction (recommended)**

Ensure user is logged into weibo.com in any supported browser (Chrome, Arc, Edge, Firefox, Brave, Chromium, Opera, Vivaldi, Safari, LibreWolf). weibo-cli auto-extracts cookies.

```bash
weibo login
weibo login --qrcode          # QR code login directly (skip browser cookies)
weibo status
```

**Method B: QR code login**

```bash
weibo login
# → Renders QR in terminal using Unicode half-blocks
# → Scan with Weibo App (我的 → 扫一扫) → confirm
```

### Step 2: Handle common auth issues

| Symptom | Agent action |
|---------|-------------|
| `⚠️ 未登录` | Guide user to login to weibo.com in browser, then run `weibo login` |
| `会话已过期` | Run `weibo logout && weibo login` |
| Cookie extraction hangs | Browser may be running; close browser and retry |

## Output Format

### Default: Rich table (human-readable)

```bash
weibo hot                              # Pretty table output
```

### JSON / YAML: structured output

```bash
weibo hot --json                       # JSON to stdout
weibo hot --yaml                       # YAML output
weibo hot --json | jq '.realtime[:3]'  # Filter with jq
```

Non-TTY stdout defaults to YAML automatically.

## Command Reference

### Reading

| Command | Description | Example |
|---------|-------------|---------|
| `weibo hot` | Hot search list (50+ topics) | `weibo hot --count 10 --json` |
| `weibo trending` | Real-time search trends | `weibo trending --count 10 --yaml` |
| `weibo search <keyword>` | Search weibos by keyword | `weibo search "科技" --count 5 --json` |
| `weibo feed` | Hot timeline | `weibo feed --count 5 --json` |
| `weibo home` | Following timeline | `weibo home --count 10 --json` |
| `weibo detail <mblogid>` | View weibo with stats | `weibo detail Qw06Kd98p --json` |
| `weibo comments <mblogid>` | View comments | `weibo comments Qw06Kd98p --count 10` |
| `weibo reposts <mblogid>` | View reposts/forwards | `weibo reposts Qw06Kd98p --count 5` |
| `weibo profile <uid>` | User profile | `weibo profile 1699432410 --json` |
| `weibo weibos <uid>` | User's published weibos | `weibo weibos 1699432410 --count 5` |
| `weibo following <uid>` | User's following list | `weibo following 1699432410` |
| `weibo followers <uid>` | User's follower list | `weibo followers 1699432410` |

### Account

| Command | Description |
|---------|-------------|
| `weibo login` | Extract cookies from browser / QR login |
| `weibo login --qrcode` | QR code login directly (skip browser) |
| `weibo login --cookie-source <browser>` | Extract from specific browser |
| `weibo logout` | Clear saved credentials |
| `weibo status` | Check authentication status |
| `weibo me` | Show current user profile |

## Agent Workflow Examples

### Browse hot topics and read details

```bash
# Get hot search topics
MBLOG=$(weibo hot --json | jq -r '.realtime[0].mblog_id // empty')
# Read a specific weibo
weibo detail Qw06Kd98p --json | jq '{text: .text_raw, likes: .attitudes_count, comments: .comments_count}'
```

### Analyze user profile

```bash
weibo profile 1699432410 --json | jq '.user | {name: .screen_name, followers: .followers_count, posts: .statuses_count}'
weibo weibos 1699432410 --count 3 --json
```

### Read comments on a weibo

```bash
weibo comments Qw06Kd98p --json | jq '.data[:5] | .[].text_raw'
```

### Daily monitoring workflow

```bash
# Top 10 hot topics
weibo hot --json | jq '.realtime[:10] | .[] | {rank, word, num}'

# Trending sidebar
weibo trending --yaml

# Hot feed
weibo feed --count 5 --json
```

## Error Codes

Structured error codes returned in CLI output:
- `not_authenticated` — cookies expired or missing
- `rate_limited` — too many requests
- `invalid_params` — missing or invalid parameters
- `qr_expired` — QR code has expired
- `api_error` — upstream Weibo API error

## Limitations

- **Read-only** — no posting, liking, or retweeting
- **No DMs** — cannot access private messages
- **Single account** — one set of credentials at a time
- **Rate limited** — built-in Gaussian jitter delay (~1s) between requests

## Anti-Detection Notes for Agents

- **Do NOT parallelize requests** — the built-in rate-limit delay exists for account safety
- **Batch operations**: when doing bulk work (e.g., reading many profiles), add delays between CLI calls
- **Session stability**: all requests share consistent Chrome 145 headers per session

## Safety Notes

- Do not ask users to share raw cookie values in chat logs.
- Prefer local browser cookie extraction over manual secret copy/paste.
- If auth fails, ask the user to re-login via `weibo login`.
- Agent should treat cookie values as secrets (do not echo to stdout unnecessarily).
- Built-in rate-limit delay protects accounts; do not bypass it.
