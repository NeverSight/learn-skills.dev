---
name: rawugc-api
description: Call the RawUGC Video Generation API to create and manage AI videos (Sora 2 and other models). Use when the user wants to generate AI videos via RawUGC, integrate RawUGC API, check video status, list videos, or work with Sora/text-to-video/image-to-video generation.
requires:
  env:
    - RAWUGC_API_KEY
compatibility: Requires RAWUGC_API_KEY (Bearer token for https://rawugc.com/api/v1). Obtain from RawUGC dashboard.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---

# RawUGC Video Generation API

Procedural knowledge for agents to call the RawUGC Video Generation API. All requests require an API key from the RawUGC dashboard, passed via environment variable.

## Authentication

- **Environment variable**: Read the API key from `RAWUGC_API_KEY`. The key is created in the RawUGC dashboard and must be kept secret; do not hardcode or log it.
- **Header**: Send on every request: `Authorization: Bearer <value of RAWUGC_API_KEY>`.
- If `RAWUGC_API_KEY` is missing or empty, inform the user they must set it and obtain a key from the RawUGC dashboard.

## Base URL

- **Production**: `https://rawugc.com/api/v1`
- All paths below are relative to this base.

## Endpoints

### POST /videos/generate

Initiate video generation.

**Request body (JSON)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | Yes | One of: `sora-2-text-to-video`, `sora-2-image-to-video`, `kling-2.6/motion-control`, `veo3`, `veo3_fast` |
| `prompt` | string | For text-to-video / veo3 | Text description (1–5000 chars). Required for `sora-2-text-to-video`, `veo3`, `veo3_fast` |
| `imageUrls` | string[] | For image-to-video / kling | Array of image URLs (max 10). Required for `sora-2-image-to-video`; for `kling-2.6/motion-control` also requires `videoUrls` |
| `videoUrls` | string[] | For kling | Array of video URLs (max 1). Required only for `kling-2.6/motion-control` |
| `aspectRatio` | string | No | `portrait` or `landscape` (some models also support `16:9`, `9:16`, `Auto`) |
| `nFrames` | string | No | `"10"` or `"15"` (video length) |
| `selectedCharacter` | string | No | Character username (e.g. `rawugc.mia`) |
| `characterOrientation` | string | No | `image` or `video` |
| `mode` | string | No | `720p` or `1080p` (for supported models) |

**Response (201)**: `taskId`, `model`, `status` (e.g. `pending`), `creditsUsed`, `newBalance`, `estimatedCompletionTime`, `createdAt`.

### GET /videos/:taskId

Get status of a generation task. Path parameter: `taskId` (from the generate response).

**Response (200)**: `taskId`, `status` (`pending` | `processing` | `completed` | `failed`), `model`, `prompt`, `creditsUsed`, `resultUrl` (when `status === 'completed'`), `createdAt`, `completedAt`, `failCode`, `failMessage`, `progress` (0–100).

### GET /videos

List the user's videos with optional filters and pagination.

**Query parameters**: `status` (optional: `pending` | `processing` | `completed` | `failed`), `limit` (1–100, default 50), `page` (default 1).

**Response (200)**: `videos` (array of same shape as GET /videos/:taskId), `pagination`: `total`, `page`, `pageSize`, `hasMore`.

## Errors

Responses use RFC 7807 Problem Details (JSON): `type`, `title`, `status` (HTTP code), `detail`, optional `instance`, optional `errors` (field-specific validation messages).

| Status | Meaning |
|--------|---------|
| 400 | Validation error (invalid body or params). Surface `detail` and `errors` to the user. |
| 401 | Authentication error (missing or invalid API key). Tell user to check `RAWUGC_API_KEY`. |
| 402 | Insufficient credits. User must add credits in RawUGC dashboard. |
| 404 | Video not found (GET /videos/:taskId). |
| 429 | Rate limit exceeded. Retry after the time indicated by response or back off. |
| 500 | Internal server error. Suggest retry or contact support. |

## Workflow: Generate then poll

1. **Generate**: `POST /videos/generate` with the desired body. On 201, note `taskId`.
2. **Poll**: Call `GET /videos/:taskId` periodically (e.g. every 10–30 seconds). Optionally use exponential backoff.
3. **Finish**: When `status === 'completed'`, use `resultUrl` for the video. When `status === 'failed'`, surface `failCode` and `failMessage` to the user.

For full request/response shapes and status codes, see [reference.md](reference.md).
