---
name: mk-youtube-get-channel-latest
description: Get latest videos, livestreams, shorts, or podcasts from a YouTube channel
license: MIT
metadata:
  version: 1.0.1
  author: kouko
  tags:
    - youtube
    - channel
    - videos
    - livestream
    - shorts
    - podcast
compatibility:
  claude-code: ">=1.0.0"
---

# YouTube Channel Latest Content

Get the latest content from a YouTube channel with type filtering.

## Quick Start

```
/mk-youtube-get-channel-latest <channel> [limit] [type]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| channel | Yes | - | Channel URL, @handle, username, or **video URL** |
| limit | No | 10 | Number of items (1-50) |
| type | No | all | Content type filter |

## Type Options

| Type | Tab URL | Description |
|------|---------|-------------|
| `all` | All tabs | Fetches from /videos, /shorts, /streams, /podcasts and merges by date |
| `videos` | `/videos` | Regular videos |
| `live` | `/streams` | Livestreams (current, past, upcoming) |
| `shorts` | `/shorts` | YouTube Shorts |
| `podcasts` | `/podcasts` | Podcast episodes |

## Examples

- `/mk-youtube-get-channel-latest @GoogleDevelopers` - Latest 10 items from channel
- `/mk-youtube-get-channel-latest @MKBHD 5 videos` - Latest 5 regular videos
- `/mk-youtube-get-channel-latest @NASA 10 live` - Latest 10 livestreams
- `/mk-youtube-get-channel-latest @shorts 20 shorts` - Latest 20 shorts
- `/mk-youtube-get-channel-latest https://www.youtube.com/@TED 3 podcasts` - Latest 3 podcast episodes
- `/mk-youtube-get-channel-latest https://www.youtube.com/watch?v=xxx 5` - Get latest from video's channel
- `/mk-youtube-get-channel-latest https://youtu.be/xxx 5 shorts` - Get shorts from video's channel

## How it Works

1. Parse channel parameter (URL, @handle, username, or **video URL**)
2. If video URL: extract channel URL using yt-dlp
3. Normalize to channel base URL
4. Execute: `{baseDir}/scripts/channel-latest.sh "<channel>" <limit> <type>`
5. For specific types: fetch from corresponding tab URL
6. For `all` type: fetch from all 4 tabs, deduplicate, sort by upload_date, return top N
7. Return JSON array of content items

## Output Format

**Success:**
```json
[
  {
    "video_id": "dQw4w9WgXcQ",
    "title": "Video Title",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "channel": "Rick Astley",
    "channel_url": "https://www.youtube.com/channel/UC...",
    "duration_string": "3:32",
    "view_count": 1500000000,
    "upload_date": "20091025",
    "live_status": "not_live",
    "description": "First 200 chars of description..."
  }
]
```

**Error:**
```json
{
  "status": "error",
  "message": "No content found for this channel"
}
```

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| video_id | string | YouTube video ID |
| title | string | Video title |
| url | string | Full YouTube URL |
| channel | string | Channel name |
| channel_url | string | Channel URL |
| duration_string | string | Human-readable duration (e.g., "10:23") |
| view_count | number | View count (may be null for upcoming) |
| upload_date | string | Upload date in YYYYMMDD format |
| live_status | string | Status: not_live, is_live, was_live, is_upcoming |
| description | string | First 200 characters of description |

## Centralized Metadata Store

This skill automatically saves partial metadata for each video to `/tmp/monkey_knowledge/youtube/meta/{YYYYMMDD}__{video_id}.meta.json`. This metadata can be accessed by downstream skills (caption, audio, transcribe, summary).

Note: This is partial metadata (marked `partial: true`). Running `/mk-youtube-get-info` on a specific video will update it with complete metadata.

## Notes

- Auto-downloads yt-dlp and jq on first run
- Supports video URL input: automatically extracts channel and fetches latest content
- Uses YouTube's official tab classification for each content type
- `all` type fetches from 4 tabs, deduplicates, and sorts by upload date
- Live status values: `not_live`, `is_live`, `was_live`, `is_upcoming`
- Podcasts require the channel to have a podcasts tab enabled
- For channels without specific content types, returns empty array
