---
name: dreamina-video
description: Generate talking-photo digital human videos with Dreamina (ByteDance OmniHuman) via AceDataCloud API. Use when animating a portrait image with a driving audio track to produce a lip-synced video where the person speaks. Supports mask-based multi-person targeting and async task polling.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN in .env file (see _shared/authentication.md).
---

# Dreamina Talking-Photo Video Generation

Generate audio-driven digital human videos through AceDataCloud's Dreamina API (powered by ByteDance OmniHuman 1.5). Provide a portrait image and driving audio to produce a lip-synced talking-photo video.

> **Setup:** See [authentication](../_shared/authentication.md) for token setup.

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/dreamina/videos \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/portrait.jpg",
    "audio_url": "https://example.com/voiceover.mp3",
    "async": true
  }'
```

The response contains a `task_id`. Poll for the result:

```bash
curl -X POST https://api.acedata.cloud/dreamina/tasks \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"action": "retrieve", "id": "<task_id>"}'
```

> **Async:** See [async task polling](../_shared/async-tasks.md). Poll `POST /dreamina/tasks` until `response.data.status` equals `"done"`.

## Model

| Model | Description |
|-------|-------------|
| `omnihuman-1.5` | ByteDance OmniHuman 1.5 — audio-driven lip-sync digital human (default and only available model) |

## Workflow

### Basic Talking-Photo

Generate a video where a portrait person speaks a given audio track.

```json
POST /dreamina/videos
{
  "model": "omnihuman-1.5",
  "image_url": "https://example.com/portrait.jpg",
  "audio_url": "https://example.com/speech.mp3",
  "prompt": "Natural expression, steady head movement, warm tone",
  "async": true
}
```

### Multi-Person Mask

To target a specific person in a group image, provide `mask_url` array with subject mask URLs.

```json
POST /dreamina/videos
{
  "image_url": "https://example.com/group-photo.jpg",
  "audio_url": "https://example.com/speech.wav",
  "mask_url": ["https://example.com/person-mask.png"],
  "async": true
}
```

## Parameters

| Parameter | Required | Values | Description |
|-----------|----------|--------|-------------|
| `image_url` | ✓ | URL | Portrait image URL (public, clear frontal face works best) |
| `audio_url` | ✓ | URL | Driving audio URL (mp3/wav, publicly reachable, keep under 60s) |
| `model` | | `"omnihuman-1.5"` | Model to use (default: `omnihuman-1.5`) |
| `prompt` | | string | Steers expression, emotion, stability, and style |
| `mask_url` | | array of URLs | Subject mask URLs to target a specific person in a multi-person image |
| `callback_url` | | URL | Webhook for result delivery |
| `async` | | boolean | Return task ID immediately for polling |

## Task Queries

Retrieve one task:

```json
POST /dreamina/tasks
{"action": "retrieve", "id": "<task_id>"}
```

You can also query by `trace_id`:

```json
POST /dreamina/tasks
{"action": "retrieve", "trace_id": "<trace_id>"}
```

Retrieve several tasks:

```json
POST /dreamina/tasks
{"action": "retrieve_batch", "ids": ["<id1>", "<id2>"]}
```

A completed response contains `response.data.video_url` when `response.data.status` is `"done"`.

## Gotchas

- Both `image_url` and `audio_url` are **required**
- The portrait should be a clear, well-lit, front-facing image with the face unobstructed
- Audio must be publicly reachable; keep it under 60s (≤30s recommended for 1080p quality)
- Use `async: true` or `callback_url` for longer jobs — synchronous mode may time out
- `mask_url` is only needed for multi-person images when you want to target one specific person
- Check `response.data.status` when polling — the terminal state is `"done"`
- Billed by output video duration

> **MCP:** See [MCP servers](../_shared/mcp-servers.md) for tool-use integration.
