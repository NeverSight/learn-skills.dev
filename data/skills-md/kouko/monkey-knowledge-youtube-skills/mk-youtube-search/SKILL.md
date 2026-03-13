---
name: mk-youtube-search
description: Search YouTube videos. Use when user wants to find videos by keyword or topic.
license: MIT
metadata:
  version: 1.2.1
  author: kouko
  tags:
    - youtube
    - search
    - video
compatibility:
  claude-code: ">=1.0.0"
---

# YouTube Search

Search YouTube videos and list results.

## Quick Start

```
/mk-youtube-search <query> [count] [mode]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| query | Yes | - | Search keywords |
| count | No | 10 | Number of results |
| mode | No | fast | `fast` or `full` (see below) |

## Mode Selection

| Mode | Speed | Metadata | Use When |
|------|-------|----------|----------|
| `fast` | ~1-2s | Basic (no upload_date) | General searches, topic exploration |
| `full` | ~5-8s | Complete (includes upload_date, description) | Time-sensitive searches, recent content |

**When to use `full` mode:**
- User asks for "recent" or "latest" videos on a topic
- Search query includes time indicators (e.g., "2024", "this week", "new")
- User wants to sort or filter by upload date
- Content is time-sensitive (news, events, updates)

**When to use `fast` mode (default):**
- General topic searches
- Tutorial or educational content
- Evergreen content that doesn't require recency

## Examples

- `/mk-youtube-search AI tutorial` → fast mode (general topic)
- `/mk-youtube-search "machine learning" 10` → fast mode
- `/mk-youtube-search "Claude AI news" 5 full` → full mode (time-sensitive)
- `/mk-youtube-search "latest iPhone review" 10 full` → full mode (recent content)

## How it Works

1. Execute: `{baseDir}/scripts/search.sh "<query>" <count> <mode>`
2. Parse JSON output
3. Write video metadata to centralized store (`/tmp/monkey_knowledge/youtube/meta/`)
4. Display results in table format

## Output Format

| # | Title | Channel | Duration | Views | Upload Date | URL |
|---|-------|---------|----------|-------|-------------|-----|
| 1 | ... | ... | 10:23 | 1.2M | 2024-01-15 | https://... |

Note: Upload Date is only available in `full` mode.

## JSON Output

```json
{
  "status": "success",
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Video Title",
      "url": "https://www.youtube.com/watch?v=...",
      "channel": "Channel Name",
      "channel_url": "https://www.youtube.com/channel/UC...",
      "duration_string": "10:23",
      "view_count": 1234567,
      "upload_date": "20240115",
      "live_status": "not_live",
      "description": "First 200 chars..."
    }
  ]
}
```

Note: In `fast` mode, `upload_date`, `live_status`, and `description` will be `null`.

## Notes

- Default result limit: 10 videos
- Default mode: `fast` (use `full` for time-sensitive searches)
- Uses system yt-dlp/jq if available, otherwise auto-downloads on first run
- Search results are saved to centralized metadata store for use by other skills (only in `full` mode)
