---
name: openclip-transcription
description: Transcribe video or audio to JSON, SRT, and VTT with speaker diarization and time codes, using OpenClip. FREE with just an OpenClip account, no subscription. Use when asked to "transcribe this", "get me a transcript", "make subtitles", "generate an SRT", "who said what in this recording", "pull quotes from this video", or "what was said at 4:30".
---

# OpenClip: transcription

`transcribe` turns a video or audio file into a time-coded transcript. It is FREE, it needs an
OpenClip account but no subscription and no credits. Output formats: JSON (structured, with
timings), SRT, and VTT.

## Setup (once)

OpenClip is a remote MCP server at `https://openclip.app/mcp`. Sign in with your OpenClip
account when the OAuth prompt appears, there is no API key to copy.

- **Claude Code:** `claude mcp add --transport http openclip https://openclip.app/mcp`, then `/mcp` to authorize.
- **Claude Desktop / web:** Settings, Connectors, "Add custom connector", paste the URL, sign in.
- **Cursor** (`.cursor/mcp.json`): `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp" } } }`
- **Header-only clients:** mint an MCP token at `openclip.app/settings/connect` and connect to
  `https://openclip.app/mcp/key` with `Authorization: Bearer <token>`.

Sanity check: call `get_account`.

## The loop

1. **Upload.** `create_upload(filename, content_type)` returns an `id` and an `upload_url`.
   PUT the raw bytes to `upload_url`, then pass the `id` as `video`.
   **Do NOT call `complete_upload`**, that starts the paid clipping pipeline. Free tools read
   the uploaded file directly. Videos already in `list_videos` work as inputs too.
2. **Transcribe.** `transcribe(video, language?, diarize?)`.
   - `language` - omit to auto-detect. Set it when you already know the language and want to
     stop a short or noisy clip being misdetected.
   - `diarize` - defaults to `true`, labels who is speaking. Turn it off for single-speaker
     audio to keep the output clean.
3. **Poll.** Returns a `tool_job` hashid. Poll `get_tool_job_status(tool_job)` every 5 to 10
   seconds. `queued` / `processing` are in flight, `completed` returns permanent CDN `outputs`
   URLs (one per format: json, srt, vtt), `failed` returns `error`. Most jobs finish inside a
   minute or two.
4. **Read the output.** Fetch the JSON output for programmatic work (segments with start and end
   times, speaker labels). Hand the user the SRT or VTT URL when they want a subtitle file.

## Two different transcript tools

Do not mix these up:

- **`transcribe`** - the FREE tool. Works on any file you upload. This skill.
- **`get_transcript`** - reads the transcript of a video that already went through the PAID
  clipping pipeline. Supports `start_ms` / `end_ms` windows at sentence or word level. Use it
  when you already have a clipping `job_id`, not for a fresh upload.

## Rules

- Always poll. Transcription is async, it never returns the text synchronously.
- Times are milliseconds.
- Output URLs are permanent CDN links, not signed or expiring.
- Free usage is rate limited per day with a per-file size cap. The error text explains how to
  lift a limit.

## Example prompts to actions

- "Transcribe this interview" - `create_upload`, PUT bytes, `transcribe(video)`, poll, return the
  transcript.
- "I need an SRT for this video" - same, then hand back the `srt` output URL.
- "Who said what in this meeting recording?" - `transcribe(video, diarize=true)`, poll, read the
  JSON output and group segments by speaker.
- "Pull the best quotes out of this talk" - transcribe, poll, read the JSON, then select quotes
  with their time codes.
- "It is in Dutch, transcribe it" - `transcribe(video, language="nl")`, poll.

## Related

To then cut the video at those time codes, see `openclip-video-editing` (`edit_video` with
`operation="trim"`). To find the moments worth cutting automatically, see `openclip-clipping`.
