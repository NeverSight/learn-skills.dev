---
name: hiapi-seedance-2-0-video
description: Generate videos with HiAPI's seedance-2.0 model via the HiAPI unified async task API. Use when a user asks to create a video with Seedance 2.0, HiAPI Seedance 2.0, or this specific skill.
metadata:
  short-description: Generate Seedance 2.0 videos through HiAPI
---

# HiAPI Seedance 2.0 Video

Use this skill when the user wants video generation through HiAPI's `seedance-2.0` model.

## Requirements

- Node.js 18 or newer.
- `HIAPI_API_KEY` must be set in the environment.
- `HIAPI_BASE_URL` is optional and defaults to `https://api.hiapi.ai`.

Important links:

- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- Docs: https://docs.hiapi.ai

Never invent a video result. If the API call fails, report the status code, compact error message, and the next action from the Error Guidance section.

## Generate A Video

Run:

```bash
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "A cinematic ocean cliff shot at golden hour" \
  --seconds 5 \
  --resolution 720p \
  --ratio 16:9
```

For image-to-video, pass a public image URL or data URI:

```bash
node scripts/hiapi-seedance-2-video.mjs --prompt "The product photo comes alive with soft camera movement" --input-reference "https://example.com/product.jpg"
```

Supported durations:

- any integer from `4` to `15`

Supported resolutions:

- `480p`
- `720p`
- `1080p`
- `4k`

`4k` is the premium tier (about 2x the per-second price of 1080p, 5x of 720p). Confirm with the user before generating at `4k`; see https://www.hiapi.ai/en/pricing.

Supported ratios:

- `16:9`
- `9:16`
- `1:1`
- `4:3`
- `3:4`
- `21:9`
- `adaptive`

Media modes are mutually exclusive:

- **Text-to-video**: no media fields.
- **First-frame image-to-video**: use `--first-frame-url` or legacy alias `--input-reference`.
- **First+last-frame image-to-video**: use both `--first-frame-url` and `--last-frame-url`.
- **Multimodal reference video generation**: use `--reference-image-url`, `--reference-video-url`, and/or `--reference-audio-url`.

Do not mix first/last-frame fields with reference image/video/audio fields. Multimodal reference mode can ask in the prompt for a reference image to act as first or last frame, but strict first/last-frame identity should use first+last-frame mode.

Reference material limits:

- `reference_image_urls` plus first/last-frame images: at most 9 images total.
- `reference_video_urls`: at most 3 videos; each 2-15 seconds; total duration at most 15 seconds. The CLI requires one `--reference-video-duration` per video URL.
- `reference_audio_urls`: at most 3 audio clips; each 2-15 seconds; total duration at most 15 seconds. The CLI requires one `--reference-audio-duration` per audio URL.

The script creates a video task, polls for up to 120 minutes by default, downloads the video to `outputs/` when possible, and prints JSON with the saved file path or remote URL. Use `--timeout-minutes <1-120>` to choose a shorter polling limit.

## API Contract

This skill calls:

```text
POST /v1/tasks
GET /v1/tasks/{taskId}
```

with:

```json
{
  "model": "seedance-2.0",
  "input": {
    "prompt": "...",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "first_frame_url": "https://example.com/photo.jpg",
    "last_frame_url": "https://example.com/end.jpg",
    "reference_image_urls": ["asset://image-1"],
    "reference_video_urls": ["asset://video-1"],
    "reference_audio_urls": ["asset://audio-1"],
    "return_last_frame": false,
    "web_search": false,
    "nsfw_checker": false,
    "generate_audio": true,
    "seed": 12345
  }
}
```

`first_frame_url` is optional. The CLI still accepts `--input-reference` as a convenience alias, then sends it as `input.first_frame_url`. Do not include `reference_*_urls` in the same request as first/last-frame fields. `generate_audio` is omitted from the request unless explicitly set — the API default is `true` (audio on); pass `--no-audio` (or `--no-generate-audio`) to disable it, `--generate-audio` to force it on. `seed` is an optional integer from 0 to 2147483647 for reproducible generation; it is omitted unless `--seed` is passed.

For details, read `references/api.md` and `references/output.md`.

## Result Lifecycle And Production Notes

- **Callbacks (production):** Video tasks can run for a while. Polling `GET /v1/tasks/{taskId}` is fine for this CLI and local debugging, but for production backends HiAPI recommends a top-level `callback.url` with `when: final` so HiAPI notifies your service instead of you long-polling. This skill does not send `callback`; see `references/api.md`.
- **Output retention (paid if extended):** Generated videos are temporary and expire about 7 days after creation; downloads are always free. By default this skill uses the temporary tier. To keep specific outputs longer, run with `--storage persistent` — the output then uses the persistent tier, billed at `$0.05 / GB · month` (charged daily); videos can be large, so the bill adds up. Only suggest this after telling the user it costs money; point them to https://docs.hiapi.ai/storage/. Deleting a persistent output stops its charges.

## Check Configuration

Run:

```bash
node scripts/check-config.mjs
```

Use `--live` only to verify that the public HiAPI pricing endpoint is reachable. It does not authenticate or validate the configured API key.

## Error Guidance

- Missing `HIAPI_API_KEY`: tell the user to create or copy a key from https://www.hiapi.ai/en/register and export it.
- HTTP `401` or `403`: tell the user to verify the HiAPI API key.
- HTTP `402`, HTTP `403` with quota text, insufficient balance, credits, quota, or payment errors: tell the user to add credits or check billing at https://www.hiapi.ai/en/dashboard and review pricing at https://www.hiapi.ai/en/pricing.
- HTTP `400`: tell the user to check duration, resolution, ratio, media mode, reference counts, and reference audio/video durations.
- HTTP `429`: tell the user to wait and retry or reduce concurrent video generations.
- Task failure: ask the user to try a clearer prompt or a different image.
- Timeout: explain that video generation may still be running and the user can retry later.
- Optional skill update notice: tell the user the printed update command can be run later.
- Required skill update notice: tell the user the printed update command must be run before using this skill again.
