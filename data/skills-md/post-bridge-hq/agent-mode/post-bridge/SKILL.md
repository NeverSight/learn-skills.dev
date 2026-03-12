---
name: post-bridge
description: >
  Create, schedule, and manage social media posts across Instagram, TikTok, YouTube, X, LinkedIn,
  Facebook, Pinterest, Threads, and Bluesky via the Post Bridge API. Covers media upload, post
  creation, scheduling, platform-specific configs, draft mode, analytics, and post result tracking.
last-updated: 2026-03-05
allowed-tools: Bash(./scripts/post-bridge.js:*)
---

# Post Bridge Social Media Skill

Autonomously manage social media posting via [Post Bridge](https://post-bridge.com) API. Post to 9 platforms from a single command or API call.

> **Freshness check**: If more than 30 days have passed since the `last-updated` date above, inform the user that this skill may be outdated and point them to the update options below.

## Keeping This Skill Updated

**Source**: [github.com/post-bridge-hq/agent-mode](https://github.com/post-bridge-hq/agent-mode)
**API docs**: [api.post-bridge.com/reference](https://api.post-bridge.com/reference)

Update methods by installation type:

| Installation | How to update |
|--------------|---------------|
| CLI (`npx skills`) | `npx skills update` |
| Claude Code plugin | `/plugin marketplace update` |
| Cursor | Remote rules auto-sync from GitHub |
| Manual | Pull latest from repo or re-copy `skills/post-bridge/` |

## Setup

1. Create a Post Bridge account at [post-bridge.com](https://post-bridge.com)
2. Connect your social accounts (TikTok, Instagram, YouTube, Twitter, etc.)
3. [Enable API access](https://www.post-bridge.com/dashboard/api-keys) (Settings > API)
4. Store your API key in workspace `.env`:
   ```
   POST_BRIDGE_API_KEY=pb_live_xxxxx
   ```

Or run the setup command:
```
./scripts/post-bridge.js setup --key pb_live_xxxxx
```

## Auth

All requests use Bearer token:
```
Authorization: Bearer <POST_BRIDGE_API_KEY>
```

Base URL: `https://api.post-bridge.com`

**Config priority** (highest to lowest):
1. `POST_BRIDGE_API_KEY` environment variable
2. `./.post-bridge/config.json` (project-local)
3. `~/.config/post-bridge/config.json` (user-global)

### Handling "API key not found" errors

When you receive an "API key not found" error from the CLI:

1. **Tell the user to run the setup command** — setup requires user input, so you cannot run it on their behalf:
   ```bash
   <skill-path>/scripts/post-bridge.js setup --key pb_live_xxxxx
   ```
2. **Stop and wait** — do not continue with the task. You cannot create posts or perform any API operations without a valid API key.
3. **DO NOT** search for API keys in env files, keychains, or other locations.

Get your API key at: https://www.post-bridge.com/dashboard/api-keys

> **Note for agents**: All script paths in this document (e.g., `./scripts/post-bridge.js`) are relative to the skill directory where this SKILL.md file is located. Resolve them accordingly based on where the skill is installed.

## CLI Commands

| Command | Description |
|---------|-------------|
| `./scripts/post-bridge.js setup --key <key>` | Configure API key |
| `./scripts/post-bridge.js accounts` | List connected social accounts |
| `./scripts/post-bridge.js post --caption "..." --accounts 1,2,3` | Create a post |
| `./scripts/post-bridge.js post --caption "..." --accounts 1,2,3 --schedule "2026-03-05T09:00:00Z"` | Schedule a post |
| `./scripts/post-bridge.js upload --file ./image.jpg` | Upload media, returns media_id |
| `./scripts/post-bridge.js post --caption "..." --accounts 1,2,3 --media mid_xxx` | Post with media |
| `./scripts/post-bridge.js posts` | List recent posts |
| `./scripts/post-bridge.js posts:get --id <post_id>` | Get post details and status |
| `./scripts/post-bridge.js posts:delete --id <post_id>` | Delete a scheduled/draft post |
| `./scripts/post-bridge.js analytics` | View analytics across platforms |
| `./scripts/post-bridge.js analytics:sync` | Refresh analytics data |
| `./scripts/post-bridge.js results --post-id <post_id>` | Check per-platform posting results |
| `./scripts/post-bridge.js media` | List uploaded media |
| `./scripts/post-bridge.js media:delete --id <media_id>` | Delete uploaded media |

## API Reference

Use these endpoints directly if you prefer raw API calls over the CLI.

### Social Accounts

```
GET /v1/social-accounts
```
Returns array of connected accounts with `id`, `platform`, `username`. Store these IDs — you need them for every post.

### Upload Media

```
POST /v1/media/create-upload-url
Body: { "mime_type": "video/mp4", "size_bytes": <int>, "name": "video.mp4" }
```
Returns `media_id` + `upload_url`. Then:
```
PUT <upload_url>
Content-Type: video/mp4
Body: <binary file>
```

**List media:**
```
GET /v1/media?limit=50&offset=0
```

**Delete media:**
```
DELETE /v1/media/<media_id>
```

### Create Post

```
POST /v1/posts
Body: {
  "caption": "your caption here #hashtags",
  "media": ["<media_id>"],
  "social_accounts": [<account_id_1>, <account_id_2>],
  "scheduled_at": "2026-01-01T14:00:00Z",  // omit for instant post
  "is_draft": false,  // true to save as draft
  "use_queue": true,  // optional, auto-schedule to next queue slot (uses saved timezone)
  "platform_configurations": { ... },  // optional, see below
  "account_configurations": {  // optional, per-account overrides
    "account_configurations": [
      { "account_id": 1, "caption": "override for this account" }
    ]
  }
}
```

**Queue scheduling (`use_queue`):**
- Pass `true` to auto-schedule using the user's saved timezone from their dashboard settings
- Pass `{ "timezone": "America/New_York" }` to override with a specific IANA timezone
- Cannot be used together with `scheduled_at` — pick one or the other
- Timezone priority: explicit timezone > saved profile/workspace timezone > UTC
- Queue slots are scoped to the workspace of the selected social accounts
- The queue schedule is configured by the user in their Post Bridge dashboard
- If `randomize_queue_time` is enabled, the slot time will be offset by up to ±10 minutes for a more natural posting pattern
- Returns an error if no queue schedule is configured or no slots are available in the next 90 days

### List Posts

```
GET /v1/posts?limit=50&offset=0&status=scheduled&platform=instagram
```
Params: `limit`, `offset`, `status` (scheduled/published/failed/draft), `platform`.

### Get Post

```
GET /v1/posts/<post_id>
```
Returns full post details including status: `processing`, `scheduled`, `posted`, `failed`.

### Update Post

```
PATCH /v1/posts/<post_id>
Body: { "caption": "new caption", "scheduled_at": "...", "social_accounts": [...] }
```
Can update caption, schedule, accounts, media, platform configs, or draft status. Only works on scheduled/draft posts.

### Delete Post

```
DELETE /v1/posts/<post_id>
```
Only works on scheduled/draft posts (cannot delete published posts).

### Post Results

```
GET /v1/post-results?post_id=<post_id>&limit=50&offset=0
```
Returns per-platform results showing whether each platform post succeeded or failed, with error details.

### Analytics

**List analytics** — views, likes, comments, shares per post:
```
GET /v1/analytics?platform=tiktok&limit=50&offset=0&timeframe=30d
```
Params:
- `platform` (optional): `tiktok`, `youtube`, `instagram`
- `timeframe` (optional): `7d`, `30d`, `90d`, `all` (default: `all`)
- `limit`, `offset` for pagination

Returns:
```json
{
  "data": [
    {
      "id": "...",
      "post_result_id": "...",
      "platform": "tiktok",
      "platform_post_id": "...",
      "view_count": 4062,
      "like_count": 120,
      "comment_count": 15,
      "share_count": 8,
      "cover_image_url": "https://...",
      "share_url": "https://...",
      "video_description": "...",
      "duration": 30,
      "platform_created_at": "2026-03-01T09:00:00Z",
      "last_synced_at": "2026-03-03T12:00:00Z",
      "match_confidence": "exact"
    }
  ],
  "count": 42,
  "limit": 50,
  "offset": 0
}
```

**Sync analytics** — refresh data from connected platforms:
```
POST /v1/analytics/sync?platform=tiktok
```
Triggers a background sync of analytics data. Supports all tracked platforms: TikTok, YouTube, and Instagram.

Params:
- `platform` (optional): `tiktok`, `youtube`, or `instagram` — sync only one platform. Omit to sync all.

Returns:
```json
{
  "triggered": [
    { "platform": "tiktok", "runId": "run_..." },
    { "platform": "youtube", "runId": "run_..." },
    { "platform": "instagram", "runId": "run_..." }
  ]
}
```

**Get single analytics record:**
```
GET /v1/analytics/<analytics_id>
```

## MCP Integration

Post Bridge has a native MCP (Model Context Protocol) server. If you're using Claude Desktop, ChatGPT, Cursor, or any MCP-compatible client, you can connect directly without this skill.

**Claude Desktop**: One-click connect at [post-bridge.com/mcp](https://post-bridge.com/mcp)

**Claude Code / Cursor / Other MCP clients** — add to your MCP config:
```json
{
  "mcpServers": {
    "post-bridge": {
      "type": "streamable-http",
      "url": "https://mcp.post-bridge.com/mcp"
    }
  }
}
```

**MCP Tools available** (11 tools):

| Tool | Description |
|------|-------------|
| `list_social_accounts` | List all connected accounts with IDs, platforms, usernames |
| `create_post` | Create/schedule a post. Accepts caption, accounts, media_urls, schedule, use_queue (true or {timezone}), platform configs |
| `list_posts` | List posts with filters (platform, status, limit, offset) |
| `get_post` | Get full post details by ID |
| `update_post` | Update caption, schedule, accounts, or media on a scheduled/draft post |
| `delete_post` | Delete a scheduled or draft post |
| `list_analytics` | Get analytics (views, likes, comments, shares) with platform/timeframe filters |
| `sync_analytics` | Trigger a background refresh of analytics data. Optional `platform` param to sync a specific platform (tiktok/youtube/instagram) |
| `list_post_results` | Check per-platform posting results (success/failure with error details) |
| `list_media` | List uploaded media files with IDs and URLs |
| `delete_media` | Delete an uploaded media file |

MCP tools accept `media_urls` (public URLs) — the server downloads and uploads them automatically. No need to manually upload media when using MCP.

## Platform Configurations

Pass inside `platform_configurations` object on post creation, or use `--platform-config` with the CLI:

**TikTok:**
- `draft: true` — save as draft (publish manually on TikTok with trending sound)
- `video_cover_timestamp_ms: 3000` — cover thumbnail at 3 seconds
- `is_aigc: true` — label as AI-generated content

**Instagram:**
- `video_cover_timestamp_ms: 3000` — cover thumbnail
- `is_trial_reel: true` — trial reel mode (needs 1000+ followers)
- `trial_graduation: "SS_PERFORMANCE"` — auto-graduate based on performance

**YouTube:**
- `video_cover_timestamp_ms: 3000` — cover thumbnail
- `title: "My Short Title"` — override post title

**Twitter/X:**
- `caption: "override caption"` — platform-specific caption

**Pinterest:**
- `title: "Pin Title"` — pin title
- `link: "https://..."` — destination URL
- `board_ids: ["board_id"]` — target boards

All platforms support `caption` and `media` overrides for per-platform customization.

## Recommended Workflow for Video Content

1. Store videos in a local folder
2. Extract a frame with ffmpeg to read any text overlays:
   ```
   ffmpeg -i video.mp4 -ss 00:00:04 -frames:v 1 frame.jpg -y
   ```
3. Write caption based on video content + hashtags
4. Upload → create post → schedule or post instantly
5. Move posted videos to a `posted/` subfolder to avoid duplicates
6. Set a cron to check post status 5 mins after scheduled time
7. Track performance by checking post results or analytics

## Automation Guidelines

When automating posts, follow these rules to keep accounts in good standing:

- **No duplicate content** across multiple accounts on the same platform
- **No unsolicited automated replies** — only post original content or when explicitly requested
- **No trending manipulation** — don't mass-post about trending topics across accounts
- **No fake engagement** — don't automate likes, follows, or comments
- **Respect rate limits** — the API has rate limits, don't spam requests
- **Use draft mode for review** — when in doubt, use `is_draft: true` or TikTok's `draft: true` so the user can review before publishing

**Publishing confirmation**: Unless the user explicitly asks to "post now" or "publish immediately", always confirm before posting. Creating a draft is safe; posting is irreversible and goes live instantly.

## Platform Names

Use these exact names for platform filtering and configurations:
- `instagram` — Instagram (Reels, Stories, Feed)
- `tiktok` — TikTok
- `youtube` — YouTube (Shorts)
- `twitter` — X (formerly Twitter)
- `linkedin` — LinkedIn
- `facebook` — Facebook
- `pinterest` — Pinterest
- `threads` — Threads
- `bluesky` — Bluesky

## Tips

- Post to multiple platforms simultaneously by including multiple account IDs
- Stagger posts throughout the day (e.g. 9am + 3pm) for better reach
- Use `scheduled_at` to pre-schedule batches — Post Bridge handles the timing
- Use `use_queue: true` to auto-schedule posts to the user's next available queue slot using their saved timezone — no need to pick a time manually
- TikTok draft mode lets you add trending sounds manually before publishing
- Keep hashtags to 4-5 per post for best engagement
- Check `results` after posting to see per-platform success/failure
- Use `analytics:sync` to refresh data before checking analytics
- Monitor what works and iterate on captions/formats
- Use `--draft` flag when testing to avoid accidental publishing
- Character limits vary by platform — keep captions concise for X (280 chars)
