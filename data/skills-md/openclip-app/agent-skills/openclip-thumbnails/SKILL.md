---
name: openclip-thumbnails
description: Pull still frames out of a video as thumbnail images with OpenClip, then compress, resize, crop, or reformat them to jpg, png, or webp. FREE with just an OpenClip account, no subscription. Use when asked for "a thumbnail from this video", "a still frame", "a poster image", "preview frames", "a contact sheet", "grab a screenshot from the video", or "resize this image".
---

# OpenClip: thumbnails and image editing

Two free tools, usually used together:

- `extract_thumbnails` - pull frames out of a video.
- `edit_image` - compress, resize, crop, or reformat an image.

Both are FREE, they need an OpenClip account but no subscription and no credits.

## Setup (once)

OpenClip is a remote MCP server at `https://openclip.app/mcp`. Sign in with your OpenClip
account when the OAuth prompt appears, there is no API key to copy.

- **Claude Code:** `claude mcp add --transport http openclip https://openclip.app/mcp`, then `/mcp` to authorize.
- **Claude Desktop / web:** Settings, Connectors, "Add custom connector", paste the URL, sign in.
- **Cursor** (`.cursor/mcp.json`): `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp" } } }`
- **Header-only clients:** mint an MCP token at `openclip.app/settings/connect` and connect to
  `https://openclip.app/mcp/key` with `Authorization: Bearer <token>`.

Sanity check: call `get_account`.

## Getting the file in

1. `create_upload(filename, content_type)` returns an `id` and an `upload_url`.
2. PUT the raw bytes to `upload_url`.
3. Pass the returned `id` as the `video` (thumbnails) or `file` (image editing) argument.

**Do NOT call `complete_upload`.** That starts the paid clipping pipeline. Free tools read the
uploaded file directly. Videos already in `list_videos` work as inputs too.

## extract_thumbnails

`extract_thumbnails(video, count?, width?)`.

- `count` - 1 to 10, default 1. Frames are spread across the video, so `count: 5` gives you a
  rough contact sheet to pick from.
- `width` - optional pixel width for the output frames.

The output is a **zip of frames**, not individual image URLs. Hand the user the zip URL, or
unpack it if you need a specific frame.

When the user wants a frame from an exact moment rather than an even spread, trim the video to
that moment first with `edit_video` (`operation="trim"`, see `openclip-video-editing`) and then
extract one thumbnail from the trimmed clip.

## edit_image

`edit_image(file, operation, ...params)`, one operation per call:

- **compress** - `quality` 1 to 100 (default 80), optional `format` (`jpg`, `png`, `webp`).
- **resize** - `width` and `height` in pixels, optional `format`.
- **crop** - either `aspect` (`"1:1"`, `"9:16"`, `"16:9"`, `"4:5"`) or explicit `x`, `y`,
  `width`, `height`, optional `format`.

Use `webp` when the image is going on a web page and `jpg` when it needs to work everywhere.

## Polling

Both tools return a `tool_job` hashid with `status: "queued"`. Poll
`get_tool_job_status(tool_job)` every 5 to 10 seconds:

- `queued` / `processing` - still working, keep polling.
- `completed` - returns permanent CDN `outputs` URLs plus `result_meta`.
- `failed` - returns `error`.

## Rules

- Always poll, both tools are async.
- One `edit_image` operation per call. To resize and then compress, run two calls in sequence.
- `extract_thumbnails` returns a zip, always. Do not promise the user individual frame URLs.
- Output URLs are permanent CDN links, not signed or expiring.
- Free usage is rate limited per day with a per-file size cap.

## Example prompts to actions

- "Grab a thumbnail from this video" - `create_upload`, PUT bytes,
  `extract_thumbnails(video)`, poll, return the zip URL.
- "Give me 5 frames to choose from" - `extract_thumbnails(video, count=5)`, poll.
- "I want the frame at 1:30" - `edit_video(video, operation="trim", start_ms=90000, end_ms=91000)`,
  poll, then `extract_thumbnails` on that output, poll.
- "Make this image a square webp" - `edit_image(file, operation="crop", aspect="1:1", format="webp")`, poll.
- "This PNG is huge, shrink it" - `edit_image(file, operation="compress", quality=75, format="webp")`, poll.

## Related

Cutting out the subject to a transparent PNG is `openclip-remove-background`. Video trimming
and cropping is `openclip-video-editing`.
