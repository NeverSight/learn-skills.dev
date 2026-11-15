---
name: openclip-convert
description: Convert and compress media from your agent with OpenClip - video to mp4, webm, mov, mkv, or gif, and audio to mp3, aac, wav, or flac. FREE with just an OpenClip account, no subscription. Use when asked to "convert this to mp4", "turn this into a gif", "extract the audio as mp3", "make this a webm", "rip the audio", "this file is too big", or "change the format".
---

# OpenClip: media conversion

`convert_media` changes a file's container or codec, including video to gif and video to
audio-only. It is FREE, it needs an OpenClip account but no subscription and no credits.

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
3. Pass the returned `id` as the `file` argument.

**Do NOT call `complete_upload`.** That starts the paid clipping pipeline. Free tools read the
uploaded file directly. A file already in `list_videos` works as an input too.

## Targets

`convert_media(file, to, ...params)`.

- **Video containers** - `mp4`, `webm`, `mov`, `mkv`. Default to `mp4` when the user just wants
  something that plays everywhere.
- **gif** - optional `fps` (default 12) and `width` (default 480). Raise `fps` for smoother
  motion, raise `width` for a sharper gif, both make the file much bigger. Trim the source first
  if it is long, gifs balloon fast.
- **Audio** - `mp3`, `aac`, `wav`, `flac`. Use this to rip audio out of a video. `mp3` for
  sharing, `wav` or `flac` when the audio feeds another tool that wants lossless.

To hit a file size rather than change format, that is `edit_video` with `operation="compress"`
(`target_mb` or `crf`), see the `openclip-video-editing` skill.

## Polling

`convert_media` returns a `tool_job` hashid with `status: "queued"`. Poll
`get_tool_job_status(tool_job)` every 5 to 10 seconds:

- `queued` / `processing` - still working, keep polling.
- `completed` - returns permanent CDN `outputs` URLs plus `result_meta`.
- `failed` - returns `error`.

Never assume a call finished synchronously.

## Rules

- Always poll, conversion is async.
- Output URLs are permanent CDN links, not signed or expiring.
- Free usage is rate limited per day with a per-file size cap. The error text explains how to
  lift a limit.
- Converting a long video to gif produces an enormous file. Trim to the interesting few seconds
  first, then convert.

## Example prompts to actions

- "Convert this to mp4" - `create_upload`, PUT bytes, `convert_media(file, to="mp4")`, poll.
- "Make a gif of this" - trim to the moment first with `edit_video`, then
  `convert_media(file, to="gif", fps=15, width=640)`, poll.
- "Get me just the audio" - `convert_media(file, to="mp3")`, poll.
- "I need lossless audio for editing" - `convert_media(file, to="wav")`, poll.

## Related

Trimming, cropping, and size-targeted compression live in `openclip-video-editing`.
Transcribing the audio you just extracted is `openclip-transcription`.
