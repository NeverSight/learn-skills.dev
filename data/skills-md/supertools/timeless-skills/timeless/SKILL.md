---
name: timeless
description: Query and manage Timeless meetings, rooms, transcripts, and AI documents. Capture podcast episodes and YouTube videos into Timeless for transcription. Use when the user asks about their meetings, wants to search meetings, read transcripts, get summaries, list rooms, create rooms, add/remove conversations from rooms, resolve Timeless share links, upload recordings, chat with Timeless AI about meeting content, or capture podcasts/YouTube videos.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIMELESS_ACCESS_TOKEN
      bins:
        - curl
        - node
      anyBins:
        - yt-dlp
    primaryEnv: TIMELESS_ACCESS_TOKEN
    emoji: "\u23F0"
    homepage: https://github.com/supertools/timeless-skills
---

# Timeless

> **Source**: [github.com/supertools/timeless-skills](https://github.com/supertools/timeless-skills)

Interact with [Timeless](https://timeless.day) meeting data: search meetings, read transcripts, get AI summaries, browse rooms, upload recordings, chat with the AI agent, and capture podcasts/YouTube videos for transcription.

## API Reference

For full endpoint documentation with response schemas, status enums, and detailed examples, read `api-reference.md` (in this skill folder).

## Prerequisites

- `TIMELESS_ACCESS_TOKEN` env var (get token at [my.timeless.day/api-token](https://my.timeless.day/api-token))
- `yt-dlp` for YouTube downloads (install via package manager: `apt install yt-dlp`, `brew install yt-dlp`, or `pip install yt-dlp`. Alternatively set `YTDLP_PATH` to point to an existing binary.)

Set up in OpenClaw:
```bash
openclaw config patch env.vars.TIMELESS_ACCESS_TOKEN=<your_token>
```

## Base URL

```
https://my.timeless.day
```

## Authentication Header

All requests:
```
Authorization: Token $TIMELESS_ACCESS_TOKEN
```

---

## Operations

### 1. List Meetings

```
GET /api/v1/spaces/meeting/
```

**Required parameter:** `include` must be `owned` or `shared`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `include` | string | **Required.** `owned` or `shared` |
| `search` | string | Search by title or attendees |
| `start_date` | string | From date (YYYY-MM-DD) |
| `end_date` | string | To date (YYYY-MM-DD) |
| `status` | string | `COMPLETED`, `SCHEDULED`, `PROCESSING`, `FAILED` |
| `page` | integer | Page number (default: 1) |
| `per_page` | integer | Results per page (default: 20) |

```bash
curl -s "https://my.timeless.day/api/v1/spaces/meeting/?include=owned&status=COMPLETED&per_page=50" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

**Response:** `{ count, next, previous, results: [{ uuid, title, start_ts, end_ts, status, primary_conversation_uuid, host_user, conversation_source, created_at }] }`

**Key fields:**
- `uuid` = space UUID (for Get Space)
- `primary_conversation_uuid` = conversation UUID (for Get Transcript)

> To get ALL meetings, make two calls: `include=owned` and `include=shared`, then merge.

---

### 2. List Rooms

```
GET /api/v1/spaces/room/
```

Same query parameters as List Meetings (except rooms don't have `start_ts`, `end_ts`, or `status`).

```bash
curl -s "https://my.timeless.day/api/v1/spaces/room/?include=owned" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

**Response:** `{ count, next, previous, results: [{ uuid, title, host_user, created_at }] }`

---

### 3. Get Space (Meeting or Room Details)

Spaces have three access levels. **Try in order until one succeeds:**

#### 3a. Private Space (your own)

```bash
curl -s "https://my.timeless.day/api/v1/spaces/{uuid}/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

#### 3b. Workspace Space (shared within team)

> **`host_uuid` is required** for shared spaces. Get it from the `host_user.uuid` field in the List Meetings or List Rooms response.

```bash
curl -s "https://my.timeless.day/api/v1/spaces/{uuid}/workspace/?host_uuid={hostUuid}" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

#### 3c. Public Space (publicly shared)

```bash
curl -s "https://my.timeless.day/api/v1/spaces/public/{uuid}/{hostUuid}/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

**Response includes:**
- `conversations[]`: Recordings in this space (each has `uuid`, `name`, `start_ts`, `end_ts`, `status`, `language`)
- `artifacts[]`: AI-generated documents. Check `type` field (e.g., `"summary"`). Content is in `content.body` (HTML).
- `contacts[]`: Each has nested `conversations[]`
- `organizations[]`: Each has nested `conversations[]`
- `threads[]`: AI chat threads. Use `threads[0].uuid` to chat with the agent.

**Collecting all conversations in a room:**
Deduplicate conversation UUIDs from `conversations[]` + `contacts[].conversations[]` + `organizations[].conversations[]`.

---

### 4. Get Transcript

```bash
curl -s "https://my.timeless.day/api/v1/conversation/{conversation_uuid}/transcript/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

**Response:**
```json
{
  "items": [
    { "text": "...", "start_time": 0.5, "end_time": 3.2, "speaker_id": "speaker_0" }
  ],
  "speakers": [
    { "id": "speaker_0", "name": "Alice Johnson" }
  ],
  "language": "he"
}
```

**How to get conversation_uuid:**
- From List Meetings: `primary_conversation_uuid` field
- From Get Space: `conversations[].uuid`

**Format as readable text** by mapping `speaker_id` to speaker names:
```
[00:00:00] Alice Johnson: ...
[00:00:03] Bob Smith: ...
```

---

### 5. Get Recording URL

```bash
curl -s "https://my.timeless.day/api/v1/conversation/{conversation_uuid}/recording/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

**Response:** `{ "media_url": "https://storage.googleapis.com/...signed..." }`

> The URL is time-limited. Fetch it fresh when needed.

---

### 6. Upload a Recording

Three-step flow:

```bash
# Step 1: Get presigned URL
curl -X POST "https://my.timeless.day/api/v1/conversation/storage/presigned-url/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_name": "recording.mp3", "file_type": "audio/mpeg"}'

# Step 2: Upload file to the presigned URL
curl -X PUT "PRESIGNED_URL" \
  -H "Content-Type: audio/mpeg" \
  --upload-file recording.mp3

# Step 3: Trigger processing
curl -X POST "https://my.timeless.day/api/v1/conversation/process/media/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"language": "he", "filename": "Recording Title"}'
```

**Response (step 3):** `{ "event_uuid": "...", "space_uuid": "..." }`

Poll `GET /api/v1/spaces/{space_uuid}/` until `is_processing` is `false`.

Or use the helper script: `bash scripts/upload.sh FILE_PATH LANGUAGE [TITLE]`

**Supported formats:** mp3, wav, m4a, mp4, webm, ogg

---

### 7. Resolve a Timeless Share URL

URLs like `https://my.timeless.day/m/ENCODED_ID` contain two Base64-encoded short IDs (22 chars each).

**Decoding (shell):**
```bash
ENCODED="the_part_after_/m/"
DECODED=$(echo "$ENCODED" | base64 -d)
SPACE_ID=$(echo "$DECODED" | cut -c1-22)
HOST_ID=$(echo "$DECODED" | cut -c23-44)
```

**Decoding (Python):**
```python
import base64

def decode_timeless_url(url):
    encoded = url.rstrip('/').split('/m/')[-1]
    combined = base64.b64decode(encoded).decode()
    return combined[:22], combined[22:]  # (space_id, host_id)
```

After decoding, fetch with Get Space (try private -> workspace -> public).

---

### 8. Chat with Timeless AI

Ask questions about a meeting or room.

#### Step 1: Send Message

```bash
curl -X POST "https://my.timeless.day/api/v1/agent/space/chat/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "space_uuid": "SPACE_UUID",
    "thread_uuid": "THREAD_UUID",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "What were the action items?"}],
      "date": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
      "metadata": {"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'", "mentions": []},
      "id": "'$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen)'"
    }
  }'
```

Get `thread_uuid` from the space's `threads[0].uuid` (via Get Space).

#### Step 2: Poll for Response

```bash
curl -s "https://my.timeless.day/api/v1/agent/threads/{thread_uuid}/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN"
```

Poll every 2-3 seconds until `is_running` is `false`. The AI response is the last message with `role: "assistant"` in the `messages` array.

---

### 9. Create a Room

```bash
curl -X POST "https://my.timeless.day/api/v1/spaces/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"has_onboarded": true, "space_type": "ROOM", "title": "My Room"}'
```

**Response:** Full space object. Extract `uuid` for adding resources.

---

### 10. Add/Remove Conversations from a Room

```bash
# Add a conversation
curl -X POST "https://my.timeless.day/api/v1/spaces/{room_uuid}/resources/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resource_type": "CONVERSATION", "resource_uuid": "CONVERSATION_UUID"}'

# Remove a conversation
curl -X DELETE "https://my.timeless.day/api/v1/spaces/{room_uuid}/resources/" \
  -H "Authorization: Token $TIMELESS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resource_type": "CONVERSATION", "resource_uuid": "CONVERSATION_UUID"}'
```

Call Add once per conversation you want to attach. Get conversation UUIDs from List Meetings (`primary_conversation_uuid`) or Get Space (`conversations[].uuid`).

---

## Common Workflows

### Export All Transcripts
1. List all meetings with `include=owned&status=COMPLETED&per_page=100`
2. Paginate through all pages
3. For each meeting, fetch transcript using `primary_conversation_uuid`

### Get Everything from a Room
1. Get Space for the room UUID
2. Collect all conversation UUIDs from `conversations[]`, `contacts[].conversations[]`, `organizations[].conversations[]` (deduplicate)
3. Fetch transcript for each conversation UUID

### Search and Read
1. List meetings with `search=your+query`
2. Pick the meeting, get its `primary_conversation_uuid`
3. Fetch transcript
4. Optionally, Get Space for AI summaries in `artifacts[]`

---

## Automation Patterns

Timeless does not have webhooks yet. To build automations that react to new meetings, use **cron polling with a state file**.

### The Pattern: Poll, Deduplicate, Act

A cron job runs every 5-10 minutes. Each run:

1. Read a state file (`timeless-processed.json`). Create it with an empty `processed` array if missing.
2. Poll for completed meetings: `GET /api/v1/spaces/meeting/?include=owned&status=COMPLETED&start_date=YYYY-MM-DD`
3. For each meeting: if its `uuid` is already in `processed`, skip it.
4. For new meetings: fetch whatever data you need (transcript, space details, artifacts), then run your automation logic.
5. Append processed UUIDs to the state file.
6. **If nothing is new, exit silently.** Do not message the user.

**State file format:**
```json
{
  "processed": ["uuid-1", "uuid-2", "uuid-3"],
  "last_check": "2026-03-05T12:00:00Z"
}
```

**Key rules:**
- A UUID in `processed` is never processed again. This prevents duplicate work.
- Periodically prune old UUIDs (e.g., older than 30 days) to keep the file small.
- Also fetch `include=shared` if the automation should cover meetings shared with you.

**Cron setup (OpenClaw):**
```
openclaw cron add "timeless-poll" --schedule "*/5 * * * *" --task "Check for new completed Timeless meetings. Read timeless-processed.json for state. Poll the API. For new meetings: [your automation here]. If nothing new, reply HEARTBEAT_OK."
```

### What You Can Do With a New Meeting

Once the polling pattern detects a new completed meeting, you have access to:
- **Transcript** (full speaker-attributed text via Get Transcript)
- **AI summary and action items** (via Get Space `artifacts[]`)
- **Participants and metadata** (via Get Space `conversations[].event.attendees`)
- **Recording URL** (via Get Recording)
- **AI chat** (ask follow-up questions via Chat with Timeless AI)

Combine these with any external tool or API. Some examples of what people build:

- Auto-generate a recap presentation or document after every meeting
- Feed meeting data into a dashboard that tracks topics, action items, or meeting load over time
- Auto-curate Timeless rooms by adding conversations that match rules (participant, title, topic)
- Push summaries or action items to Slack, email, Notion, or a CRM
- Run sentiment analysis or extract custom fields from transcripts
- Build a searchable meeting knowledge base

The pattern is always the same: poll for new meetings, pull the data, do your thing.

---

## Capture: Podcasts

Scripts in `scripts/` folder.

1. **Search**: `bash scripts/podcast.sh search "podcast name"`
2. **List episodes**: `bash scripts/podcast.sh episodes FEED_URL [limit]`
3. **Download**: `bash scripts/podcast.sh download MP3_URL /tmp/episode.mp3`
4. **Upload to Timeless**: `bash scripts/upload.sh /tmp/episode.mp3 en "Episode Title"`
5. Clean up the file from /tmp

### Spotify links

Extract the episode title via oEmbed, then search by name:
```bash
curl -s "https://open.spotify.com/oembed?url=SPOTIFY_URL"
```

---

## Capture: YouTube

1. **Get info**: `bash scripts/youtube.sh info "YOUTUBE_URL"`
2. **Download video**: `bash scripts/youtube.sh download "YOUTUBE_URL" /tmp/video.mp4`
3. **Upload to Timeless**: `bash scripts/upload.sh /tmp/video.mp4 en "Video Title"`
4. Clean up the file from /tmp

Downloads as mp4 (video+audio). No ffmpeg needed. Uses the best pre-muxed format (typically 720p), which is fine for Timeless.

---

## Capture: Adding to a Room

After uploading, attach the content to a Timeless room for organized collections.

1. Upload returns a `space_uuid`. Poll `GET /api/v1/spaces/{space_uuid}/` until `is_processing=false`.
2. From the space response, get the `conversation.uuid`.
3. Add to room: `POST /api/v1/spaces/{room_uuid}/resources/` with `{"resource_type": "CONVERSATION", "resource_uuid": "CONV_UUID"}`

To create a new room first: `POST /api/v1/spaces/` with `{"has_onboarded": true, "space_type": "ROOM", "title": "My Collection"}`

---

## Notes

- Podcast MP3s can be large (100-300MB for long episodes). Downloads may take a minute.
- YouTube downloads require yt-dlp. If not installed, the script will fail with a clear error.
- Always clean up downloaded files from /tmp after uploading.
- Set `YTDLP_PATH` env var if yt-dlp is not on PATH.

---

## Error Handling

| Code | Action |
|------|--------|
| 401 | Token expired. Re-authenticate at my.timeless.day/api-token |
| 403 | No access. Try workspace or public endpoint. |
| 404 | Not found. Check UUID. |
| 429 | Rate limited. Wait and retry. |

## Rate Limiting

No official limits, but be respectful:
- 0.5s delay between sequential requests
- Max ~60 requests per minute
- Use pagination, don't fetch everything at once
