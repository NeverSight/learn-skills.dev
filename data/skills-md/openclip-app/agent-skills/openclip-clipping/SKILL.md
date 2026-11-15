---
name: openclip-clipping
description: Turn a long video into short vertical clips ranked by a virality score, using OpenClip. Give it a podcast, webinar, interview, stream, or YouTube URL and get back the best moments with hooks, titles, social copy, and downloadable clip URLs. Use when asked to "clip this video", "find the viral moments", "make shorts from this", "cut this podcast into clips", "what are the best bits of this", "make TikToks from this stream", or "give me the top moments".
---

# OpenClip: clipping long video into shorts

The headline OpenClip pipeline: submit a long video, get back ranked "viral moments" with
titles, hooks, social copy, and clip URLs. This is the PAID pipeline, it needs an active
OpenClip subscription and credits (credits are minutes of processing).

Processing is ASYNC at every step. Always poll, never assume a call finished.

## Setup (once)

OpenClip is a remote MCP server at `https://openclip.app/mcp`. Sign in with your OpenClip
account when the OAuth prompt appears, there is no API key to copy.

- **Claude Code:** `claude mcp add --transport http openclip https://openclip.app/mcp`, then `/mcp` to authorize.
- **Claude Desktop / web:** Settings, Connectors, "Add custom connector", paste the URL, sign in.
- **Cursor** (`.cursor/mcp.json`): `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp" } } }`
- **Header-only clients:** mint an MCP token at `openclip.app/settings/connect` and connect to
  `https://openclip.app/mcp/key` with `Authorization: Bearer <token>`.

Sanity check: call `get_account` and confirm `credits_remaining > 0`.

## The loop

1. **Submit.** `submit_video(url)` returns a `job_id` with `status: "queued"`.
   Call `list_supported_providers` first if you are unsure a source URL is supported.
   For a local file: `create_upload(filename, content_type)`, PUT the bytes, then
   `complete_upload` (which is what starts this paid pipeline).
2. **Poll.** `get_video_status(job_id)` until `status` is `completed` or terminal.
   Do NOT call `list_clips` before `completed`.
3. **List.** `list_clips(job_id)` returns the viral moments.
4. **Render (optional).** `render_clip(moment_id, caption_preset)` burns in captions. Also
   async, see the `openclip-captions` skill.

## Reading the status correctly

This is the part agents get wrong. `submit_video` ALWAYS succeeds when you are authenticated.
It queues the job, it does NOT pre-check your subscription or credits. The gate surfaces later,
in `get_video_status`, as a status value rather than an error:

- `pending`, `downloading`, `processing` - in flight, keep polling.
- `completed` - terminal, now call `list_clips`.
- `failed` - terminal. When it happens almost immediately after submit, this usually means
  **no active subscription**. Tell the user to subscribe at openclip.app.
- `pending_credits` - the team is **out of credits**. Tell the user to top up.
- `download_failed` (on the nested `video.status`) - the source URL could not be fetched. Ask
  the user to check the link.

Do not expect a synchronous "you need to subscribe" error. Read the status and advise.

`video.progress` is COARSE, it is not a smooth percentage. Roughly 0 when failed, single digits
while downloading, ~10 uploaded, ~20 processing, 100 completed. Use `status` for control flow,
never `progress`.

## What a moment looks like

Each entry from `list_clips`:

- `id` - hashid, pass this to `render_clip`.
- `title`, `hook`, `quote`, `social_copy`, `platforms`, `category` - the copy to post with.
- `start_time_ms`, `end_time_ms`, `duration_ms` - times are milliseconds.
- `virality_score` - 0 to 10. **Rank by this** unless the user says otherwise.
- `viral_score_details` - sub-scores 0 to 100: hook strength, shareability, rewatchability,
  surprise, emotional impact. Use these to explain WHY a clip ranked where it did.
- `thumbnail_url`, and assets `clip` `{url, size_bytes, type}`, `clip_watermarked`, and
  `rendered_clip` `{url, size_bytes}` once `render_clip` has succeeded.

Clip URLs are permanent CDN links, not signed or expiring.

## Reusable presets

To make repeat runs identical (same tracker model, caption preset, composition, logo
watermark), save a processing agent once with `create_agent` and pass it to `submit_video`.
`describe_agent_settings` documents every nested field and allowed value. `update_agent`
patches only the fields you send. `create_agent_logo_upload` plus `set_agent_logo` attach a
watermark (max 2 MB). `get_usage` reports the credit balance and recent activity.

## Errors

These are MCP tools, not a REST API. A failure comes back as a tool result with `isError: true`
and a plain-text message. No HTTP status codes, no JSON error envelope.

- `"Not authenticated. Reconnect your OpenClip token."` - reconnect the connector, or re-mint
  the MCP token for the `/mcp/key` path.
- `"Job not found."` - wrong, expired, or another account's `job_id`. Re-submit if it came from
  an old session.
- `"Viral moment not found."` - wrong `moment_id`. Re-fetch with `list_clips`.
- `"Video not yet available. Check get_video_status for progress."` - you called `list_clips`
  too early. Keep polling `get_video_status`.
- Validation messages come back as the message text. Fix the argument and retry.

## Rules

- Always poll. Never assume a submit is instantly done.
- Rank by `virality_score`, higher is better.
- Times are milliseconds.
- **Projects and folders are not supported** by this API. Do not promise them.
- `list_videos` shows videos already in the account.

## Example prompts to actions

- "Clip this: <url>" - `submit_video(url)`, poll `get_video_status`, then `list_clips`.
- "Top 3 moments from job_..." - `list_clips`, sort by `virality_score`, take 3.
- "Why is that one the best?" - read `viral_score_details` for that moment.
- "Make shorts from my last upload" - `list_videos`, pick it, submit, poll, list.

## Related

Burning in styled captions is `openclip-captions`. The full long-form to multi-platform
workflow is `openclip-repurpose`. Free trimming and cropping with no subscription is
`openclip-video-editing`.
