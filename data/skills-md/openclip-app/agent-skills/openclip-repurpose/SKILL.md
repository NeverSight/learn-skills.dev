---
name: openclip-repurpose
description: Turn one long video into a full batch of platform-ready short clips for TikTok, Reels, and YouTube Shorts with OpenClip - find the moments, reframe to vertical, burn in captions, and write the post copy for each. Use when asked to "repurpose this podcast", "turn this into a week of content", "make a content batch from this webinar", "get 10 shorts out of this", "cut this up for social", or "give me clips ready to post".
---

# OpenClip: repurposing long-form into a content batch

This is the end-to-end workflow skill. One long video in, a set of ready-to-post vertical clips
out, each with captions and copy. It stitches together the OpenClip clipping pipeline,
captions, and the free media tools.

The clipping pipeline is PAID (needs an active subscription and credits). The reframing and
trimming tools are free.

## Setup (once)

OpenClip is a remote MCP server at `https://openclip.app/mcp`. Sign in with your OpenClip
account when the OAuth prompt appears, there is no API key to copy.

- **Claude Code:** `claude mcp add --transport http openclip https://openclip.app/mcp`, then `/mcp` to authorize.
- **Claude Desktop / web:** Settings, Connectors, "Add custom connector", paste the URL, sign in.
- **Cursor** (`.cursor/mcp.json`): `{ "mcpServers": { "openclip": { "url": "https://openclip.app/mcp" } } }`
- **Header-only clients:** mint an MCP token at `openclip.app/settings/connect` and connect to
  `https://openclip.app/mcp/key` with `Authorization: Bearer <token>`.

Sanity check: call `get_account` and confirm `credits_remaining > 0`.

## The workflow

**Before you start**, agree two things with the user: how many clips they want, and which
platforms. Those two answers drive every decision below. Do not silently pick for them.

1. **Submit the source.** `submit_video(url)`. Returns a `job_id`, status `queued`.
   For a local file: `create_upload`, PUT the bytes, then `complete_upload`.
2. **Poll to completion.** `get_video_status(job_id)` until `completed`. A near-instant `failed`
   means no active subscription. `pending_credits` means out of credits. Say so plainly and stop,
   do not keep polling a terminal state.
3. **Pull the moments.** `list_clips(job_id)`. Sort by `virality_score` (0 to 10) and take the
   number the user asked for. Show them the shortlist with title, hook, duration, and score
   BEFORE rendering anything, so they can veto. Rendering costs credits.
4. **Caption each pick.** `list_caption_presets`, then `render_clip(moment_id, caption_preset)`
   for each approved moment. Poll `list_clips` until every moment has a `rendered_clip`.
5. **Reframe if needed.** The pipeline output is already short-form oriented. If the user needs a
   different aspect for a specific platform, run the free `edit_video(video, operation="crop",
   aspect="9:16" | "1:1" | "4:5")` on the rendered clip.
6. **Hand over the batch.** For each clip give: the `rendered_clip` URL, `title`, `hook`,
   `social_copy`, `duration_ms`, `virality_score`, and the suggested `platforms` field.

## Platform shapes

- **TikTok, Reels, Shorts** - 9:16 vertical. This is the default, the pipeline targets it.
- **Instagram feed** - 4:5 or 1:1. Crop the rendered clip with `edit_video`.
- **X and LinkedIn** - 16:9 or 1:1 both work. Captions matter more than aspect, most of these
  autoplay muted.

Each moment carries a `platforms` field from the pipeline. Use it as a starting suggestion, not
a rule, and reconcile it with what the user actually posts to.

## Sequencing and cost

- Batch the polling. Submit once, then poll `get_video_status` on a loop rather than
  re-submitting.
- Render only the approved moments. Every `render_clip` is work, do not render all ten when the
  user wanted three.
- For a recurring workflow (same captions, same composition, same logo watermark every time),
  save a processing agent with `create_agent` and pass it to `submit_video`. That makes every
  future batch identical without re-specifying. `describe_agent_settings` lists every field.
- `get_usage` shows the credit balance (credits are minutes of processing) before you start a
  big batch. Check it when the user asks for a large number of clips.

## Rules

- Always poll, every step is async.
- Rank by `virality_score`, higher is better. Explain rankings with `viral_score_details`
  (hook strength, shareability, rewatchability, surprise, emotional impact).
- Times are milliseconds.
- Clip URLs are permanent CDN links, not signed or expiring.
- **Projects and folders are not supported.** Do not promise the user a folder structure.
- Do not rewrite `social_copy` into influencer voice unless asked. It is generated to match the
  clip, and heavy-handed rewriting usually makes it worse.

## Example prompts to actions

- "Turn this podcast into 10 TikToks" - submit, poll, `list_clips`, show top 10 shortlist,
  get approval, render each with captions, poll, hand over the batch.
- "Give me a week of content from this webinar" - same, sized to 5 to 7 clips, grouped by theme
  using each moment's `category`.
- "Just the best one, captioned like MrBeast" - submit, poll, take the top
  `virality_score`, `render_clip(moment_id, caption_preset="beast")`, poll.
- "Same look as last time" - reuse the saved agent id on `submit_video`.

## Related

The pipeline mechanics and status handling in detail are in `openclip-clipping`. Caption
presets and custom caption styling are in `openclip-captions`. Free cropping, trimming, and
compression are in `openclip-video-editing`.
