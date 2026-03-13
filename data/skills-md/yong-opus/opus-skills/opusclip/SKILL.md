---
name: opusclip
description: Turn long-form videos into short clips using the OpusClip API. Use when the user wants to clip a YouTube video, upload a local video for clipping, manage clip collections, list brand templates, share projects publicly, censor profanity, or any task involving OpusClip. Triggers on phrases like "clip this video", "create shorts", "opusclip", "make clips from video", "upload to opusclip".
---

# OpusClip

Turn long-form videos into short clips via the OpusClip API.

## Prerequisites

- `OPUSCLIP_API_KEY` must be set. Get it from https://clip.opus.pro/dashboard
- The CLI at `scripts/opusclip` requires `curl` and `jq`

## CLI Quick Reference

Run the bundled CLI at `scripts/opusclip`. All commands output JSON.

```
opusclip submit --url URL [options]           Submit video for clipping (alias: create-project)
opusclip list --project ID [--summary]        List clips (alias: get-clips)
opusclip describe --project ID --clip CID     Get clip details (transcript, layout info)
opusclip storyboard --project ID --clip CID   Generate 2x2 frame preview (requires ffmpeg)
opusclip trim --project ID --clip CID --start S --end E  Local trim (requires ffmpeg)
opusclip preview --project ID [--output PATH] Generate HTML preview and open in browser
opusclip share --project ID                   Share project (alias: share-project)
opusclip templates                            List brand templates
opusclip upload --file PATH [options]         Upload local video + create project
opusclip collections <sub> [options]          Manage collections
opusclip censor <sub> [options]               Censor profanity in clips
```

### submit

Alias: `create-project`

```bash
opusclip submit --url "https://youtube.com/watch?v=..." [options]
```

| Flag | Description |
|------|-------------|
| `--url` | (required) Video URL |
| `--model` | `ClipBasic` (talking-head) or `ClipAnything` (diverse) |
| `--prompt` | Custom clipping prompt (ClipAnything only) |
| `--keywords` | Comma-separated topic keywords (ClipBasic only) |
| `--aspect` | `portrait` (default), `landscape`, `square` |
| `--durations` | Target clip lengths in seconds, e.g. `"30,60"` |
| `--range-start` / `--range-end` | Clip only a portion (seconds) |
| `--template` | Brand template ID |
| `--genre` | Video genre hint |
| `--lang` | Source language code |
| `--title` | Video title metadata |
| `--webhook` | Webhook URL for completion notification |
| `--skip-curate` | Process original video without AI curation |
| `--remove-filler` | Remove filler words |

### upload

Same flags as `submit` plus `--file PATH`. Handles the full 4-step GCS upload flow automatically.

### list

Alias: `get-clips`

```bash
opusclip list --project PROJECT_ID
opusclip list --project PROJECT_ID --summary
opusclip list --collection COLLECTION_ID
```

| Flag | Description |
|------|-------------|
| `--project` | Project ID to fetch clips for |
| `--collection` | Collection ID to fetch clips for |
| `--summary` | Output condensed JSON with title, description, hashtags, scores, duration, and preview/export URLs (instead of full raw response) |

When presenting clips to the user, always use `--summary` to get human-readable fields (title, description, hashtags, scores). Display clips with their title and description rather than just clip IDs.

### preview

Generate an HTML preview page with video players for all clips and open it in the browser.

```bash
opusclip preview --project PROJECT_ID
opusclip preview --project PROJECT_ID --output /path/to/output.html
opusclip preview --collection COLLECTION_ID
```

| Flag | Description |
|------|-------------|
| `--project` | Project ID |
| `--collection` | Collection ID |
| `--output` | Custom output path (default: `/tmp/opusclip-preview-{id}.html`) |

The preview page shows clips sorted by score with inline video players, titles, descriptions, hashtags, and detailed AI scores (hook, coherence, connection, trend). Use this whenever the user wants to watch or preview their clips.

### share

Alias: `share-project`

```bash
opusclip share --project PROJECT_ID
```

| Flag | Description |
|------|-------------|
| `--project` | (required) Project ID |

### collections

```bash
opusclip collections list
opusclip collections create --name "NAME"
opusclip collections delete --id ID
opusclip collections export --id ID
opusclip collections add-clip --id COL_ID --content-id PROJECT_ID.CLIP_ID
opusclip collections remove-clip --id COL_ID --content-id PROJECT_ID.CLIP_ID
```

### censor

```bash
opusclip censor create --project PID --clip CID [--beep]
opusclip censor status --job JOB_ID
```

Statuses: `QUEUED` → `PROCESSING` → `CONCLUDED` / `FAILED`

### describe

Get structured information about a clip. Use this to understand clip content without watching the video.

```bash
opusclip describe --project PROJECT_ID --clip CLIP_ID
opusclip describe --transcript --project PROJECT_ID --clip CLIP_ID
opusclip describe --layout --project PROJECT_ID --clip CLIP_ID
```

| Flag | Description |
|------|-------------|
| `--project` | (required) Project ID |
| `--clip` | (required) Clip ID |
| `--transcript` | Show only transcript text |
| `--layout` | Show only layout/framing info |

Without `--transcript` or `--layout`, shows both. Use `--transcript` when you need to understand what was said. Use `--layout` to check current framing before suggesting layout changes.

### storyboard

Generate a 2x2 frame grid image from a clip's preview video. Requires `ffmpeg`.

```bash
opusclip storyboard --project PROJECT_ID --clip CLIP_ID
opusclip storyboard --project PROJECT_ID --clip CLIP_ID --output /path/to/output.jpg
```

| Flag | Description |
|------|-------------|
| `--project` | (required) Project ID |
| `--clip` | (required) Clip ID |
| `--output` | Custom output path (default: `/tmp/opusclip-storyboard-{clipId}.jpg`) |

Opens the image automatically on macOS/Linux. Use this for quick visual review of a clip's content.

### trim

Trim a clip's preview video locally. Requires `ffmpeg`.

```bash
opusclip trim --project PROJECT_ID --clip CLIP_ID --start 3 --end 50
opusclip trim --project PROJECT_ID --clip CLIP_ID --start 3 --end 50 --output trimmed.mp4
```

| Flag | Description |
|------|-------------|
| `--project` | (required) Project ID |
| `--clip` | (required) Clip ID |
| `--start` | (required) Start time in seconds |
| `--end` | (required) End time in seconds |
| `--output` | Custom output path (default: `/tmp/opusclip-trimmed-{clipId}.mp4`) |

## Common Workflows

### Clip a YouTube video
```bash
opusclip submit --url "https://youtube.com/watch?v=VIDEO_ID"
# Wait for processing, then:
opusclip list --project PROJECT_ID --summary
# Preview clips in browser:
opusclip preview --project PROJECT_ID
```

### Use ClipAnything with a custom prompt
```bash
opusclip submit \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --model ClipAnything \
  --prompt "Find the most emotional moments" \
  --durations "30,60,90"
```

### Upload a local video, clip, and organize
```bash
opusclip upload --file video.mp4 --title "Interview" --model ClipBasic
opusclip list --project PROJECT_ID
opusclip collections create --name "Best Clips"
opusclip collections add-clip --id COL_ID --content-id PROJECT_ID.CLIP_ID
opusclip collections export --id COL_ID
```

### Clip, curate, and share
```bash
opusclip submit --url "https://youtube.com/watch?v=..."
opusclip list --project PROJECT_ID --summary

# Understand clip content
opusclip describe --transcript --project PROJECT_ID --clip CLIP_ID

# Visual review
opusclip storyboard --project PROJECT_ID --clip CLIP_ID

# Share
opusclip share --project PROJECT_ID
```

## Constraints

- Rate limit: 30 req/min
- Max video: 10 hours, 30 GB
- Max concurrent: 50 projects
- Projects expire after 30 days
- 1 credit = 1 minute of video

## API Reference

For detailed endpoint schemas, parameters, and response formats, see [references/api-reference.md](references/api-reference.md).
