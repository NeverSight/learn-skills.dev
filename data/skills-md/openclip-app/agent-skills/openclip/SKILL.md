---
name: openclip
description: 'Turn long videos into short, captioned viral clips from your agent via the OpenClip MCP server. Also FREE with just an account, no subscription needed - transcribe a video, convert/compress/trim/crop/resize/mute a video, extract thumbnails, edit an image, remove an image background. Plus generate a short UGC-style ad clip from a brief. Triggers include "clip this video", "make shorts", "repurpose this", "find viral moments", "transcribe this", "convert to mp4/gif/mp3", "compress this video", "remove the background", "make a UGC ad", "openclip".'
---

# OpenClip: video editing from your agent

OpenClip is a video editing MCP server. Its headline pipeline turns a long video into
short, captioned, ranked clips. Its full `/mcp` and `/mcp/key` endpoints expose 31 tools
in six groups, listed below. The ChatGPT app exposes only its reviewed clip-pipeline
subset.

- **Documentation**: `search_docs` searches OpenClip product features, settings, workflows,
  integrations, and troubleshooting guidance. Call it when product behavior is unclear.
- **Clipping pipeline**: `submit_video`, `get_video_status`, `list_clips`, `render_clip`,
  `get_render_status`, `list_caption_presets`, `get_transcript`, `list_supported_providers`,
  `list_videos`.
- **Uploads**: `create_upload`, `complete_upload` (see the gotcha below: complete_upload
  starts the PAID pipeline; free tools skip it).
- **Free media utilities** (account only, NO subscription): `transcribe`, `edit_video`,
  `convert_media`, `extract_thumbnails`, `edit_image`, `remove_background`,
  `get_tool_job_status`.
- **UGC generation**: `generate_ugc`, `get_ugc_job_status`, `list_ugc_creators`, `list_ugc_jobs`.
- **Account & presets**: `get_account`, `get_usage`, `list_agents`, `create_agent`,
  `update_agent`, `describe_agent_settings`, `create_agent_logo_upload`, `set_agent_logo`.

## Setup (once)

The remote server supports **OAuth one-click** as the primary path: paste the server URL
(`https://openclip.app/mcp`) into your client and **sign in with your OpenClip account**, no
token to copy.

1. Add the remote server to your agent (server URL: `https://openclip.app/mcp`):
   - **Claude Desktop:** Settings → Connectors → Add custom connector → paste
     `https://openclip.app/mcp` → Connect → sign in.
   - **Claude Code:** `claude mcp add --transport http openclip https://openclip.app/mcp`,
     then run `/mcp` and authorize in the browser.
   - **Cursor** (`.cursor/mcp.json`):
     `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp" } } }`, Cursor runs OAuth.
2. **Manual Bearer token (alternative, for header-only / programmatic clients):** generate an
   **MCP token** at **openclip.app/settings/connect** ("Generate MCP token", shown once) and
   connect to the **`/mcp/key`** endpoint with it as a Bearer header:
   - **Claude Code:**
     `claude mcp add --transport http openclip https://openclip.app/mcp/key --header "Authorization: Bearer <token>"`
   - **Cursor** (`.cursor/mcp.json`):
     `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp/key", "headers": { "Authorization": "Bearer <token>" } } } }`
   - **Any MCP client:** POST to `https://openclip.app/mcp/key` with header `Authorization: Bearer <token>`.
3. Sanity check: call `get_account`. Confirm `credits_remaining > 0`.

(Self-hosting/dev only: run the local stdio server with `php artisan mcp:start openclip`.)

## The loop (processing is ASYNC, always poll)

1. **Submit**: `submit_video(url)` → returns a `job_id` with `status:"queued"`. This ALWAYS
   succeeds (queues the job) when authenticated, it does NOT pre-check subscription or credits.
2. **Poll status**: `get_video_status(job_id)` until `status` is `completed` (or `failed`).
   Do NOT call list_clips before completion. Read `status` for the real state:
   - `failed` (often almost immediately after submit) usually means **no active subscription** -
     advise the user to subscribe at openclip.app.
   - `pending_credits` means the team is **out of credits**, advise the user to top up.
   - `download_failed` means the source URL couldn't be fetched, ask the user to check the link.
3. **List clips**: `list_clips(job_id)` → viral moments with `virality_score` (0-10),
   title/hook, start/end (ms), and `clip` / `rendered_clip` URLs.
4. **(Optional) Render captioned**: `render_clip(moment_id, caption_preset)`. Async too, poll
   `list_clips` and watch the moment's `rendered_clip` for the finished URL. Preset keys:
   `list_caption_presets`.

## Free media utilities (no subscription needed)

`transcribe`, `edit_video`, `convert_media`, `extract_thumbnails`, `edit_image`, and
`remove_background` are FREE: they only need an account, not a subscription or credits.
All follow the same async pattern:

1. Get a file in: for a local file call `create_upload(filename, content_type)`, PUT the
   bytes to the returned `upload_url`, and use the returned `id` as `file`/`video`.
   **Do NOT call `complete_upload` for free tools** - that starts the paid clipping
   pipeline; free tools read the uploaded file directly. (Videos already in
   `list_videos` work as inputs too.)
2. Call the tool. It returns a `tool_job` hashid with `status: "queued"`.
3. Poll `get_tool_job_status(tool_job)` every 5-10s: `queued`/`processing` are in-flight,
   `completed`/`failed` terminal. On `completed` it returns permanent CDN `outputs` URLs
   (e.g. json/srt/vtt for transcribe, a zip of frames for extract_thumbnails). On
   `failed` it returns `error`.

Operation cheat sheet (full params in `reference.md`): `edit_video` does one `operation`
of crop, trim, rotate, resize, compress, or mute; `convert_media` targets mp4/webm/mov/mkv,
gif, or mp3/aac/wav/flac; `edit_image` does compress, resize, or crop; `remove_background`
returns a transparent PNG. Free usage is rate-limited per day with per-file size caps; the
error text explains how to lift a limit.

Note the transcript split: `transcribe` is the free tool for uploaded files;
`get_transcript` reads the time-coded transcript of a video that went through the paid
clipping pipeline (supports `start_ms`/`end_ms` windows at sentence or word level).

## UGC generation

`generate_ugc` renders a short (~7-12s) vertical UGC-style clip from a creative brief
(NOT a prose prompt: structured fields like `character`, or a server-side `brief_name`
preset). Free accounts get ONE generation per day; paid accounts are metered in credits by
the seconds rendered. It returns a `ugc_job` hashid; poll `get_ugc_job_status` every
10-15s (`queued`/`rendering` in-flight, `completed` returns `video_url` + `result_meta`,
`failed` returns `error`). Renders are heavy: expect a couple of minutes.

Before generating, call `list_ugc_creators` to discover the valid `creator` and
`start_frame` values for the team (curated roster plus the team's own saved creators,
grouped by niche). Use `list_ugc_jobs` to review a team's past UGC clips or find a
`ugc_job` id to poll.

## Reusable presets (agents)

To make repeat workflows identical (same tracker model, caption preset, and logo
watermark), save a processing agent once with `create_agent` and pass it to
`submit_video`. `describe_agent_settings` documents every nested field and allowed value;
`update_agent` patches only the fields you send; `create_agent_logo_upload` +
`set_agent_logo` attach a watermark (max 2 MB). `get_usage` reports the credit balance
(credits are MINUTES of processing) and recent activity.

## Rules & gotchas

- Always poll; never assume a submit is instantly done. Poll `get_video_status` in a loop.
- Pick clips by `virality_score` (higher = better) unless the user says otherwise.
- Times are milliseconds. `clip.url` is a permanent CDN URL (not signed/expiring).
- `submit_video` queues regardless of subscription/credit state; the gate surfaces LATER in
  `get_video_status` (`failed` = no subscription, `pending_credits` = out of credits). Read the
  status and advise the user accordingly, do NOT expect a synchronous "subscribe" error.
- **Projects/folders are not supported** by this API, don't promise them.

## Error handling

These are **MCP tools**, not a REST/HTTP API. A failed tool call returns a normal tool result
with `isError: true` and a short **plain-text message** (no HTTP 401/402/403/422 status, no JSON
error envelope). Read the message text and act on it:

- **`"Not authenticated. Reconnect your OpenClip token."`**, the connection isn't carrying a
  valid identity → reconnect. For the OAuth path, re-run the connector sign-in (e.g. `/mcp` in
  Claude Code); for the manual `/mcp/key` path, re-generate the MCP token on the connect page and
  re-add the server with the new Bearer token. (A token missing the `mcp:use` scope/ability is
  rejected at the transport before any tool runs, same fix: reconnect / re-mint.)
- **`"Job not found."`** (`get_video_status`, `list_clips`), the `job_id` is wrong, from a
  different account, or expired → re-check the id you passed; if it was from an earlier session,
  re-submit the video.
- **`"Viral moment not found."`** (`render_clip`), the `moment_id` is wrong or belongs to
  another account → re-fetch moments with `list_clips` and use an id from that response.
- **`"Video not yet available. Check get_video_status for progress."`** (`list_clips`), the job
  hasn't produced a video record yet (still queued/downloading) → keep polling
  `get_video_status` and only call `list_clips` once `status` is `completed`.
- **Validation messages** (e.g. a bad/missing `url`, an unknown `caption_preset`), the
  validation error text is returned as the tool message → fix the offending argument and retry.
- **Subscription / credits are NOT errors here**, they appear as `get_video_status` `status`
  values (`failed` = no subscription → subscribe; `pending_credits` = out of credits → top up),
  not as a tool error. See "The loop" above.

## Example prompts → actions

- "Clip this: <url>" → `submit_video(url)`, poll `get_video_status`, then `list_clips`.
- "Give me the top 3 moments from job_…" → `list_clips`, sort by `virality_score`, take 3.
- "Render moment m_… with the Beast captions" → `render_clip(m_…, caption_preset="beast")`, poll.
- "Transcribe this recording" → `create_upload`, PUT bytes, `transcribe(video)`, poll
  `get_tool_job_status` (NO `complete_upload`).
- "Convert this to a gif" / "compress this video" → `create_upload`, PUT bytes,
  `convert_media(file, to="gif")` / `edit_video(file, operation="compress")`, poll.
- "Remove the background from this image" → `create_upload`, PUT bytes,
  `remove_background(file)`, poll, return the transparent PNG.
- "Make a UGC ad for my app" → `generate_ugc(brief={...})`, poll `get_ugc_job_status`.

See `reference.md` for status values, preset keys, operation params, and field shapes.

## Focused skills

This skill covers the whole surface. When a job is squarely one of these, the focused skill has
more depth on it:

| Skill | Covers | Needs a subscription |
| --- | --- | --- |
| `openclip-clipping` | Long video to ranked viral moments | Yes |
| `openclip-captions` | Burning styled captions into a clip | Yes |
| `openclip-repurpose` | End-to-end long-form to a posting-ready batch | Yes |
| `openclip-ugc-ads` | UGC-style ad clips from a brief | No, 1/day free |
| `openclip-video-editing` | Trim, crop, resize, rotate, compress, mute | No |
| `openclip-transcription` | Transcripts, SRT, VTT, diarization | No |
| `openclip-convert` | mp4, webm, mov, mkv, gif, mp3, aac, wav, flac | No |
| `openclip-thumbnails` | Frames from video, plus image editing | No |
| `openclip-remove-background` | Transparent PNG cutouts | No |

Install any of them with `npx skills add OpenClip-App/agent-skills`.
