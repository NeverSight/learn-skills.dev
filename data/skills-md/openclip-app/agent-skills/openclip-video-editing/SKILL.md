---
name: openclip-video-editing
description: Edit a video file from your agent with OpenClip - trim, crop, reframe to 9:16 or 1:1, resize, rotate, flip, compress to a target size, or mute the audio. FREE with just an OpenClip account, no subscription. Use when asked to "cut this video down", "trim to 30 seconds", "make it vertical", "crop to 9:16", "resize this video", "compress this, it is too big", "rotate this clip", "remove the audio", or "edit this video".
---

# OpenClip: video editing

`edit_video` performs one operation per call on a video file: crop, trim, rotate, resize,
compress, or mute. It is FREE, it needs an OpenClip account but no subscription and no credits.

Chain calls to combine operations: feed the output of one call into the next.

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
3. Pass the returned `id` as the `video` argument.

**Do NOT call `complete_upload`.** That starts the paid clipping pipeline. Free tools read the
uploaded file directly. A video already in `list_videos` works as an input too.

## Operations

Every call is `edit_video(video, operation, ...params)`.

- **crop** - either `aspect` (`"1:1"`, `"9:16"`, `"16:9"`, `"4:5"`) or explicit `x`, `y`,
  `width`, `height`. Use `aspect: "9:16"` to reframe landscape footage for TikTok, Reels,
  and Shorts.
- **trim** - `start_ms` and `end_ms`, both required. Times are milliseconds.
- **rotate** - `degrees` (`90`, `180`, `270`) and/or `flip` (`none`, `horizontal`, `vertical`).
- **resize** - `width` and `height` in pixels.
- **compress** - either `target_mb` (aim for a file size) or `crf` (18 to 32, lower is better
  quality and a bigger file). Reach for `target_mb` when the user names a size limit.
- **mute** - no params, strips the audio track.

## Polling

`edit_video` returns a `tool_job` hashid with `status: "queued"`. Poll
`get_tool_job_status(tool_job)` every 5 to 10 seconds:

- `queued` / `processing` - still working, keep polling.
- `completed` - returns permanent CDN `outputs` URLs plus `result_meta`.
- `failed` - returns `error`.

Never assume a call finished synchronously.

## Rules

- One operation per call. To trim and then reframe, run trim first, then pass its output to a
  crop call.
- Times are milliseconds everywhere, not seconds.
- Output URLs are permanent CDN links, not signed or expiring.
- Free usage is rate limited per day with a per-file size cap. The error text explains how to
  lift a limit.

## Example prompts to actions

- "Cut this down to the first 30 seconds" - `create_upload`, PUT bytes,
  `edit_video(video, operation="trim", start_ms=0, end_ms=30000)`, poll.
- "Make this vertical for TikTok" - `edit_video(video, operation="crop", aspect="9:16")`, poll.
- "This file is 400MB, get it under 50" - `edit_video(video, operation="compress", target_mb=50)`, poll.
- "Strip the audio" - `edit_video(video, operation="mute")`, poll.
- "Trim to the middle minute and make it square" - trim, poll, then crop the output with
  `aspect="1:1"`, poll again.

## Related

Converting between formats (mp4, gif, mp3) is `convert_media`, see the `openclip-convert`
skill. Turning a long video into ranked short clips is the paid pipeline, see
`openclip-clipping`.
