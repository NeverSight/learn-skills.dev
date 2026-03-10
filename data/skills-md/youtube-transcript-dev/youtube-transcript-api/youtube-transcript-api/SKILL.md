---
name: youtube-transcript-api
description: Extract, transcribe, and translate YouTube video transcripts using the YouTubeTranscript.dev V2 API. Supports captions, ASR audio transcription, batch processing (up to 100 videos), translation to 100+ languages, and multiple output formats. Use when working with YouTube videos, subtitles, captions, or video-to-text conversion.
license: MIT
compatibility: Requires network access to youtubetranscript.dev API. Works with any language or runtime that can make HTTP requests.
metadata:
  author: YouTubeTranscript.dev
  version: "2.0"
---

# YouTube Transcript API Skill

Use this skill when the user wants to extract transcripts from YouTube videos, transcribe videos without captions, translate video content, or process multiple videos in batch.

## When to Use

- User asks to get a transcript/subtitles/captions from a YouTube video
- User wants to transcribe a YouTube video that has no captions (ASR)
- User wants to translate a YouTube video transcript to another language
- User needs to process multiple YouTube videos at once
- User wants to build an AI/LLM pipeline that uses YouTube video content
- User wants to repurpose video content into text (blog posts, summaries, etc.)

## API Overview

**Base URL:** `https://youtubetranscript.dev/api/v2`

**Authentication:** Bearer token via `Authorization: Bearer YOUR_API_KEY`

Users can get a free API key at [youtubetranscript.dev](https://youtubetranscript.dev).

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v2/transcribe` | Extract transcript from a single video |
| `POST` | `/api/v2/batch` | Extract transcripts from up to 100 videos |
| `GET`  | `/api/v2/jobs/{job_id}` | Check status of an ASR job |
| `GET`  | `/api/v2/batch/{batch_id}` | Check status of a batch request |

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `video` | Yes (single) | YouTube URL or 11-character video ID |
| `video_ids` | Yes (batch) | Array of IDs or URLs (up to 100) |
| `language` | No | ISO 639-1 code (e.g., `"es"`, `"fr"`). Omit for best available |
| `source` | No | `auto` (default), `manual`, or `asr` |
| `format` | No | `timestamp`, `paragraphs`, or `words` |
| `webhook_url` | No | URL for async delivery (required for `source="asr"`) |

### Credit Costs

| Method | Cost | Speed |
|--------|------|-------|
| Native Captions | 1 credit | 5–10 seconds |
| Translation | 1 credit per 2,500 chars | 5–10 seconds |
| ASR (Audio) | 1 credit per 90 seconds | 2–20 minutes (async) |

## Examples

### Basic Transcript Extraction (Python)

```python
import requests

API_KEY = "your_api_key"

response = requests.post(
    "https://youtubetranscript.dev/api/v2/transcribe",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"video": "dQw4w9WgXcQ"}
)

data = response.json()
for segment in data["data"]["transcript"]:
    print(f"[{segment['start']:.1f}s] {segment['text']}")
```

### Basic Transcript Extraction (JavaScript/Node.js)

```javascript
const response = await fetch("https://youtubetranscript.dev/api/v2/transcribe", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ video: "dQw4w9WgXcQ" }),
});

const { data } = await response.json();
console.log(data.transcript);
```

### Using the Node.js SDK

```bash
npm install youtube-audio-transcript-api
```

```javascript
import { YouTubeTranscript } from "youtube-audio-transcript-api";

const yt = new YouTubeTranscript({ apiKey: "your_api_key" });

// Simple extraction
const result = await yt.getTranscript("dQw4w9WgXcQ");

// With translation
const translated = await yt.transcribe({
  video: "dQw4w9WgXcQ",
  language: "es",
});

// Batch (up to 100 videos)
const batch = await yt.batch({
  video_ids: ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"],
});
```

### Basic Transcript Extraction (cURL)

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ"}'
```

### Batch Processing (up to 100 videos)

```bash
curl -X POST https://youtubetranscript.dev/api/v2/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_ids": ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"]}'
```

### Translation

Add `"language": "es"` (or any ISO 639-1 code) to get the transcript translated:

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "language": "es"}'
```

### ASR Transcription (videos without captions)

For videos that don't have captions, use ASR with a webhook:

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "VIDEO_ID", "source": "asr", "webhook_url": "https://yoursite.com/webhook"}'
```

This returns immediately with `status: "processing"`. Results are delivered to the webhook URL when ready. Poll with `GET /api/v2/jobs/{job_id}` if not using webhooks.

## Error Handling

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `invalid_request` | Invalid JSON or missing required fields |
| 401 | `invalid_api_key` | Missing or invalid API key |
| 402 | `payment_required` | Insufficient credits |
| 404 | `no_captions` | No captions available and ASR not used |
| 429 | `rate_limit_exceeded` | Too many requests — check `Retry-After` header |

## Important Notes

- Always ask the user for their API key if they haven't provided one. Free keys are available at [youtubetranscript.dev](https://youtubetranscript.dev).
- Omitting the `language` parameter returns the best available transcript without translation (saves credits).
- ASR is async — always use a webhook URL or poll the jobs endpoint.
- Batch endpoint accepts both YouTube URLs and 11-character video IDs.
- Re-fetching an already-owned transcript costs 0 credits.

## Resources

- [Website](https://youtubetranscript.dev)
- [Full API Docs & OpenAPI Spec](https://youtubetranscript.dev/api-docs)
- [npm SDK](https://www.npmjs.com/package/youtube-audio-transcript-api)
- [Pricing](https://youtubetranscript.dev/pricing)
