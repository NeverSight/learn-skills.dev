---
name: xhs-cli
description: "(LEGACY — use xiaohongshu-cli instead) CLI skill for Xiaohongshu (小红书, RedNote, XHS) to search notes, read posts, browse profiles, like, favorite, comment, and publish from the terminal"
author: jackwener
version: "1.0.0"
tags:
  - xhs
  - xiaohongshu
  - 小红书
  - rednote
  - social-media
  - cli
---

> [!WARNING]
> **This skill is superseded by [xiaohongshu-cli](https://github.com/jackwener/xiaohongshu-cli).**
> `xiaohongshu-cli` uses a reverse-engineered API, runs faster, and is actively maintained.
> This package (`xhs-cli`) uses a headless browser approach and is kept for legacy use only.
> **New users and agents should install `xiaohongshu-cli` instead.**

# xhs-cli Skill

A CLI tool for interacting with Xiaohongshu (小红书). Use it to search notes, read details, browse user profiles, and perform interactions like liking, favoriting, and commenting.

## Prerequisites

```bash
# Install (requires Python 3.8+)
uv tool install xhs-cli
# Or: pipx install xhs-cli
```

## Authentication

All commands require valid cookies to function.

```bash
xhs status                     # Check saved login session (no browser extraction)
xhs login                      # Auto-extract Chrome cookies
xhs login --cookie "a1=..."    # Or provide cookies manually
```

Authentication first uses saved local cookies. If unavailable, it auto-detects local Chrome cookies via browser-cookie3. If extraction fails, QR code login is available.

## Command Reference

### Search

```bash
xhs search "咖啡"              # Search notes (rich table output)
xhs search "咖啡" --json       # Raw JSON output
```

### Read Note

```bash
# View note (xsec_token auto-resolved from search cache)
xhs read <note_id>
xhs read <note_id> --comments  # Include comments
xhs read <note_id> --xsec-token <token>  # Manual token
xhs read <note_id> --json
```

### User

```bash
# Look up user profile (by internal user_id, hex format)
xhs user <user_id>
xhs user <user_id> --json

# List user's published notes
xhs user-posts <user_id>
xhs user-posts <user_id> --json

# Followers / Following
xhs followers <user_id>
xhs following <user_id>
```

### Discovery

```bash
xhs feed                       # Explore page recommended feed
xhs feed --json
xhs topics "旅行"              # Search topics/hashtags
xhs topics "旅行" --json
```

### Interactions (require login)

```bash
# Like / Unlike (xsec_token auto-resolved)
xhs like <note_id>
xhs like <note_id> --undo

# Favorite / Unfavorite
xhs favorite <note_id>
xhs favorite <note_id> --undo

# Comment
xhs comment <note_id> "好棒！"

# Delete your own note
xhs delete <note_id>
```

### Favorites

```bash
xhs favorites                  # List your favorites
xhs favorites --max 10         # Limit count
xhs favorites --json
```

### Post

```bash
xhs post "标题" --image photo1.jpg --image photo2.jpg --content "正文"
xhs post "标题" --image photo1.jpg --content "正文" --json
```

### Account

```bash
xhs status                     # Quick saved-session check
xhs whoami                     # Full profile info
xhs whoami --json
xhs login                      # Login
xhs logout                     # Clear cookies
```

## JSON Output

Major query commands support `--json` for machine-readable output:

```bash
xhs search "咖啡" --json | jq '.[0].id'           # First note ID
xhs whoami --json | jq '.userInfo.userId'          # Your user ID
xhs favorites --json | jq '.[0].displayTitle'      # First favorite title
```

## Common Patterns for AI Agents

```bash
# Get your user ID for further queries
xhs whoami --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('userInfo',{}).get('userId',''))"

# Search and get note IDs (xsec_token auto-cached for later use)
xhs search "topic" --json | python3 -c "import sys,json; [print(n['id']) for n in json.load(sys.stdin)[:3]]"

# Check login before performing actions
xhs status && xhs like <note_id>

# Read a note with comments for summarization
xhs read <note_id> --comments --json
```

## Error Handling

- Commands exit with code 0 on success, non-zero on failure
- Error messages are prefixed with ❌
- Login-required commands show clear instruction to run `xhs login`
- `xsec_token` is auto-resolved from cache; manual `--xsec-token` available as fallback

## Safety Notes

- Do not ask users to share raw cookie values in chat logs.
- Prefer auto-extraction via `xhs login` over manual cookie input.
- If auth fails, ask the user to re-login via `xhs login`.

