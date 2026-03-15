---
name: supadata
description: >
  Extract transcripts, structured data, and search YouTube and social video platforms
  (TikTok, Instagram, X/Twitter, Facebook) using the Supadata API. Use for: fetching
  YouTube transcripts, searching YouTube videos by keyword, bulk-transcribing a channel
  or list of URLs, extracting structured/visual data from tutorial videos (AI tools,
  UI demos, on-screen prompts), and getting video/channel metadata. Prefer this over
  any yt-dlp or youtube-data-api approach.
metadata:
  clawdbot:
    emoji: 📡
    requires:
      env:
        - SUPADATA_API_KEY
---

# Supadata Skill

One API for YouTube transcripts, search, channel ingestion, structured extraction, and metadata across YouTube + social video platforms.

**Base URL:** `https://api.supadata.ai/v1`  
**Auth header:** `x-api-key: $SUPADATA_API_KEY`  
**Env var:** `SUPADATA_API_KEY`

---

## When to Use Which Endpoint

| Goal | Endpoint | Cost |
|---|---|---|
| Get transcript from a YouTube/social URL | `/transcript` or `/youtube/transcript` | 1 credit (native) / 2 credits/min (AI) |
| Transcribe many videos at once | `/youtube/transcript-batch` | 1 credit/video (native) |
| Search YouTube by keyword | `/youtube/search` | 1 credit/page |
| List all video IDs from a channel | `/youtube/channel-videos` | 1 credit |
| Get video/channel/playlist metadata | `/youtube/video`, `/youtube/channel`, `/metadata` | 1 credit |
| Extract structured data from a tutorial (visual content) | `/extract` | varies (AI vision) |
| Scrape a web page to Markdown | `/web/scrape` | 1 credit |

**Key decision: Transcript vs Extract**
- Use **Transcript** when content is mostly spoken / narrated. Cheaper, faster.
- Use **Extract** when the video is a tutorial/demo where important content is shown on screen but NOT spoken aloud (e.g. Midjourney prompts typed into UI, ComfyUI node graphs, on-screen settings panels, code shown without narration). Extract runs a vision model on the video frames.

---

## 1. YouTube Transcript

### Single video (YouTube-specific, most common)
```bash
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?url=https://youtu.be/VIDEO_ID&text=true&lang=en" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

**Parameters:**
| Param | Values | Notes |
|---|---|---|
| `url` | YouTube URL | Required |
| `text` | `true` / `false` | `true` = plain string, `false` = timestamped chunks |
| `lang` | ISO 639-1 (e.g. `en`) | Optional, defaults to first available |

**Response (`text=true`):**
```json
{
  "content": "Full transcript as plain text...",
  "lang": "en",
  "availableLangs": ["en", "es"]
}
```

**Response (`text=false`):**
```json
{
  "content": [
    { "text": "Hello everyone", "offset": 0, "duration": 2500, "lang": "en" }
  ],
  "lang": "en",
  "availableLangs": ["en"]
}
```

### Cross-platform transcript (YouTube, TikTok, Instagram, X, Facebook, file URL)
```bash
curl -X GET "https://api.supadata.ai/v1/transcript?url=URL_HERE&text=true&mode=auto" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

**`mode` values:**
- `native` — fetch existing captions only (cheapest, 1 credit, no AI). Use this first.
- `auto` — try native, fall back to AI speech-to-text if no captions exist (default)
- `generate` — always AI speech-to-text (2 credits/min, use when you need it for content without captions)

**Async handling:** Large videos return HTTP 202 with a `jobId`. Poll with:
```bash
curl "https://api.supadata.ai/v1/transcript/JOB_ID" -H "x-api-key: $SUPADATA_API_KEY"
```

---

## 2. Batch Transcript (multiple videos)

Use for bulk channel ingestion or list of URLs.
```bash
curl -X POST "https://api.supadata.ai/v1/youtube/transcript-batch" \
  -H "x-api-key: $SUPADATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://youtu.be/VIDEO_ID_1",
      "https://youtu.be/VIDEO_ID_2"
    ],
    "text": true,
    "lang": "en"
  }'
```

Returns a `batchId`. Poll results:
```bash
curl "https://api.supadata.ai/v1/youtube/batch/BATCH_ID" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

---

## 3. YouTube Search

Search YouTube and get structured results. Far cleaner than SerpApi for programmatic use — native sort/filter params, ISO dates, integer view counts.

```bash
curl -X GET "https://api.supadata.ai/v1/youtube/search?query=AI+image+prompts&type=video&sortBy=views&uploadDate=month&duration=medium&limit=20" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

**Parameters:**
| Param | Values | Notes |
|---|---|---|
| `query` | string | Required |
| `type` | `video`, `channel`, `playlist`, `movie`, `all` | Default: `all` |
| `sortBy` | `relevance`, `rating`, `date`, `views` | Default: `relevance` |
| `uploadDate` | `hour`, `today`, `week`, `month`, `year`, `all` | Default: `all` |
| `duration` | `short` (<4min), `medium` (4–20min), `long` (>20min), `all` | Default: `all` |
| `features` | array: `hd`, `subtitles`, `4k`, `live`, `creative-commons`, `360`, `hdr` | Optional |
| `limit` | 1–5000 | Auto-paginates. Each page ~20 results = 1 credit. |
| `nextPageToken` | string | Manual pagination token from previous response |

**Response:**
```json
{
  "query": "AI image prompts",
  "results": [
    {
      "type": "video",
      "id": "VIDEO_ID",
      "title": "Best Midjourney Prompts 2024",
      "description": "...",
      "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
      "duration": 847,
      "viewCount": 234567,
      "uploadDate": "2024-11-15T00:00:00.000Z",
      "channel": {
        "id": "CHANNEL_ID",
        "name": "AI Creator Hub",
        "thumbnail": "https://..."
      }
    }
  ],
  "nextPageToken": "eyJ..."
}
```

**Pagination cost note:** `limit=100` will consume ~5 credits (100/20 pages). Use limit carefully for bulk research.

---

## 4. Channel Video List

Get all video IDs from a YouTube channel for bulk ingestion.
```bash
curl -X GET "https://api.supadata.ai/v1/youtube/channel-videos?url=https://youtube.com/@CHANNEL_HANDLE" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

Returns array of video IDs. Feed into batch transcript endpoint.

---

## 5. Extract — Structured Data from Video (Vision + Audio)

Use when video content is **visual** — prompts shown on screen, UI demos, workflow screenshots, settings panels not narrated aloud.

```bash
curl -X POST "https://api.supadata.ai/v1/extract" \
  -H "x-api-key: $SUPADATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "prompt": "Extract all AI image prompts shown on screen. Include the exact text of each prompt, the tool or platform visible (Midjourney, Stable Diffusion, etc), and any parameter settings shown (aspect ratio, model, steps, etc).",
    "schema": {
      "type": "object",
      "properties": {
        "prompts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "timestamp": { "type": "string" },
              "tool": { "type": "string" },
              "promptText": { "type": "string" },
              "parameters": { "type": "string" }
            },
            "required": ["promptText"]
          }
        }
      },
      "required": ["prompts"]
    }
  }'
```

Always returns async `jobId` (HTTP 202). Poll:
```bash
curl "https://api.supadata.ai/v1/extract/JOB_ID" -H "x-api-key: $SUPADATA_API_KEY"
```

**Schema strategy:**
- Run with `prompt` only first → API auto-generates schema → reuse returned `schema` for consistency across future videos of same type
- Provide both `prompt` + `schema` for maximum control

**Pre-built schema examples for our use cases:**

### AI Image Prompt Extractor
```json
{
  "type": "object",
  "properties": {
    "prompts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": { "type": "string" },
          "tool": { "type": "string", "description": "Midjourney, FLUX, Stable Diffusion, etc" },
          "promptText": { "type": "string" },
          "parameters": { "type": "string", "description": "e.g. --ar 16:9 --stylize 750" },
          "resultVisible": { "type": "boolean", "description": "Is the generated image shown?" }
        },
        "required": ["promptText"]
      }
    }
  },
  "required": ["prompts"]
}
```

### Key Takeaways Extractor
```json
{
  "type": "object",
  "properties": {
    "topic": { "type": "string" },
    "summary": { "type": "string" },
    "keyTakeaways": { "type": "array", "items": { "type": "string" } },
    "actionItems": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["topic", "summary", "keyTakeaways"]
}
```

### Video Chapters
```json
{
  "type": "object",
  "properties": {
    "chapters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string" },
          "startTime": { "type": "string" },
          "summary": { "type": "string" }
        },
        "required": ["title", "startTime"]
      }
    }
  },
  "required": ["chapters"]
}
```

---

## 6. Video / Channel Metadata

```bash
# Single video metadata
curl "https://api.supadata.ai/v1/youtube/video?url=https://youtu.be/VIDEO_ID" \
  -H "x-api-key: $SUPADATA_API_KEY"

# Channel metadata
curl "https://api.supadata.ai/v1/youtube/channel?url=https://youtube.com/@HANDLE" \
  -H "x-api-key: $SUPADATA_API_KEY"

# Cross-platform (YouTube, TikTok, Instagram, X, Facebook)
curl "https://api.supadata.ai/v1/metadata?url=URL" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

---

## 7. Web Scrape (bonus — same key)

Extract any web page to clean Markdown.
```bash
curl "https://api.supadata.ai/v1/web/scrape?url=https://example.com" \
  -H "x-api-key: $SUPADATA_API_KEY"
```

---

## Python Usage (SDK)

```python
from supadata import Supadata

supadata = Supadata(api_key=os.environ["SUPADATA_API_KEY"])

# Transcript
transcript = supadata.youtube.transcript(url="https://youtu.be/VIDEO_ID", text=True, lang="en")
print(transcript.content)

# Search
results = supadata.youtube.search(query="AI image prompts", type="video", sort_by="views", upload_date="month", limit=20)
for r in results.results:
    print(r.title, r.view_count)

# Extract (async)
job = supadata.extract(url="https://youtu.be/VIDEO_ID", prompt="Extract all prompts shown on screen")
result = supadata.extract.get_results(job.job_id)
print(result.data)
```

Install SDK: `pip install supadata`

---

## Content Pipeline Pattern

**Discover → Filter → Ingest → Extract → Store**

```
1. search(query, sortBy=views, uploadDate=month)  → get ranked video list
2. Filter by viewCount > threshold, duration = medium/long
3. batch_transcript(urls)                          → pull all transcripts
4. If tutorial/demo video → extract(url, schema)   → get visual prompts
5. Feed to agent → classify → store in laniameda-kb
```

---

## Pricing Reference

| Action | Credits |
|---|---|
| Native transcript (captions exist) | 1 |
| AI-generated transcript | 2 per minute of video |
| Search (per page ~20 results) | 1 |
| Channel video list | 1 |
| Video/channel/playlist metadata | 1 |
| Web scrape | 1 |
| Extract (AI vision) | varies |

**Default to `mode=native` for transcripts.** Only use `generate` when captions don't exist.

---

## Error Handling

| Code | Meaning |
|---|---|
| 400 | Invalid request / missing params |
| 401 | Bad API key |
| 404 | Video not found / no transcript available |
| 429 | Rate limit hit |
| 202 | Async job started — poll with jobId |
