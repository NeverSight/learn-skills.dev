---
name: skool-monitor
description: Monitor and interact with Skool communities - read posts, create posts, reply to comments, like content, and search. Use when user asks to check Skool, read community posts, interact with Skool, or manage Skool community.
---

# Skool Community Monitoring & Interaction

## Goal
Monitor AND interact with Skool community via reverse-engineered API. Read posts, create posts, reply to comments, like content, and search.

## CRITICAL SAFETY CONSTRAINTS

**NEVER perform write operations without explicit user approval:**
- DO NOT create posts unless explicitly requested
- DO NOT like posts unless explicitly requested
- DO NOT reply to posts unless explicitly requested
- Read operations are safe and can be performed freely

## Scripts
- `./scripts/skool_unreads.py` - Fetch unread posts
- `./scripts/skool_scraper.py` - Read posts and extract content
- `./scripts/skool_browser_client.py` - Write operations (recommended)
- `./scripts/skool_client.py` - Write operations (legacy)
- `./scripts/skool_comment_scraper.py` - Scrape comments

## Quick Reference

```bash
# Check unreads from last 48 hours (most common)
python3 ./scripts/skool_unreads.py --since 48 --summary

# Just get unread count
python3 ./scripts/skool_unreads.py --count-only

# Read posts
python3 ./scripts/skool_scraper.py posts --community makerschool --limit 10

# Create post (REQUIRES APPROVAL)
python3 ./scripts/skool_browser_client.py create \
  --title "Title" --content "Content" --labels 3b2896c64f8f415ca62105fdae269357

# Reply to post (REQUIRES APPROVAL)
python3 ./scripts/skool_browser_client.py reply --post-id <id> --content "Reply"

# Like post (REQUIRES APPROVAL)
python3 ./scripts/skool_browser_client.py like --post-id <id>

# Search
python3 ./scripts/skool_client.py search --query "keyword"
```

## Unread Posts

```bash
# Last 48 hours with summary
python3 ./scripts/skool_unreads.py --since 48 --summary

# Export to JSON
python3 ./scripts/skool_unreads.py --since 48 --output .tmp/unreads.json
```

Output categorizes as:
- New posts (never viewed)
- New comments (posts with new activity)

## Write Operations (Browser-Based)

Uses Playwright to maintain real browser session and auto-generate WAF tokens.

```bash
# Create post
python3 ./scripts/skool_browser_client.py create \
  --title "My Post" --content "Content here" --labels <label_id>

# Reply
python3 ./scripts/skool_browser_client.py reply --post-id <id> --content "Reply text"

# Like/Unlike
python3 ./scripts/skool_browser_client.py like --post-id <id>
python3 ./scripts/skool_browser_client.py unlike --post-id <id>
```

## Rate Limits
- Reading: Stay under 1 req/sec
- Writing: Max 1 post per 30 seconds, 5 comments per minute, 10 likes per minute

## Troubleshooting

| Error | Solution |
|-------|----------|
| 403 Forbidden | WAF token expired (use browser_client instead of manual) |
| 401 Unauthorized | Update auth_token from browser cookies |
| 429 Too Many Requests | Wait 60 seconds, reduce frequency |

## Environment
```
SKOOL_AUTH_TOKEN=your_token
SKOOL_CLIENT_ID=your_client_id
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `since` | integer | No | Hours to look back (default: 48) |
| `community` | string | No | Community slug (default: makerschool) |
| `action` | string | No | Action: read, create, reply, like, search |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `posts` | array | Unread posts with metadata |
| `summary` | string | AI summary of unreads (if --summary flag) |

### Credentials
| Name | Source |
|------|--------|
| `SKOOL_AUTH_TOKEN` | .env |
| `SKOOL_CLIENT_ID` | .env |

### Composable With
Skills that chain well with this one: `skool-rag`

### Cost
Free (reverse-engineered API)
