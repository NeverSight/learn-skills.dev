---
name: openclip-captions
description: Burn styled, animated captions into a short clip with OpenClip using caption presets (beast, pop, kendrick, mozi, dan, sara, lucy, tayo and more) or a custom caption style and position. Use when asked to "add captions", "add subtitles to this short", "burn in the text", "make it look like MrBeast captions", "restyle the captions", "put words on screen", or "caption this clip".
---

# OpenClip: captions on clips

`render_clip` burns animated captions into a viral moment produced by the OpenClip clipping
pipeline. This is part of the PAID pipeline, it needs an active subscription and credits.

Captions here are **rendered into the video**, not a sidecar subtitle file. If the user wants an
SRT or VTT file instead, that is the free `transcribe` tool, see `openclip-transcription`.

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

1. **Have a moment.** You need a `moment_id` from `list_clips(job_id)`. If the user has not run
   a video through the pipeline yet, start with `submit_video`, see the `openclip-clipping`
   skill.
2. **Pick a preset.** Call `list_caption_presets` to get the current keys. Known keys:
   `default`, `dan`, `dan-reveal`, `pop`, `mozi`, `kendrick`, `sara`, `lucy`, `tayo`, `beast`.
   **Always confirm with the call**, keys can change. That same call also returns the full
   caption-style property schema and the caption position options, which is what you need for
   custom styling rather than a named preset.
3. **Render.** `render_clip(moment_id, caption_preset)`.
4. **Poll.** Rendering is async. Poll `list_clips(job_id)` and watch that moment's
   `rendered_clip` field. When it appears it holds `{url, size_bytes}`, the finished captioned
   video. `get_render_status` reports on the render directly.

## Choosing a preset

Presets are visual styles, not just fonts. When the user names a creator or a vibe, map it:

- Big, punchy, word-by-word pop with heavy outline - `beast`.
- Clean and readable, safe default for a brand account - `default`.
- Bouncy and playful - `pop`.
- Reveal-style where words appear progressively - `dan-reveal`.

When the user does not care, use `default` and show them the other keys so they can swap.
When they want something no preset covers, pull the caption-style property schema from
`list_caption_presets` and build a custom style instead of forcing a near-miss preset.

## Rules

- Always confirm preset keys with `list_caption_presets` before rendering. An unknown
  `caption_preset` comes back as a validation message on the tool result.
- Always poll. `render_clip` returns immediately, the video is not ready yet.
- A moment can be re-rendered with a different preset. `rendered_clip` reflects the latest
  successful render.
- `clip` is the unrendered cut, `clip_watermarked` is the watermarked version, `rendered_clip`
  is the captioned output. Hand the user the right one.
- Times are milliseconds.

## Errors

Tool failures come back as a tool result with `isError: true` and a plain-text message, not an
HTTP status.

- `"Viral moment not found."` - the `moment_id` is wrong or belongs to another account.
  Re-fetch with `list_clips` and use an id from that response.
- `"Not authenticated. Reconnect your OpenClip token."` - reconnect or re-mint the token.
- An unknown preset key returns the validation message text. Call `list_caption_presets` and
  retry with a real key.

## Example prompts to actions

- "Add captions to that clip" - `list_caption_presets`, `render_clip(moment_id, caption_preset="default")`, poll.
- "Make it look like MrBeast" - `render_clip(moment_id, caption_preset="beast")`, poll.
- "What caption styles are there?" - `list_caption_presets`, show the keys.
- "Caption all the top 3" - `list_clips`, take the top 3 by `virality_score`, `render_clip` each,
  poll until every `rendered_clip` is present.
- "I want the captions at the top in my brand font" - `list_caption_presets` for the style schema
  and position options, then render with a custom style.

## Related

Producing the clips to caption is `openclip-clipping`. Standalone SRT and VTT subtitle files are
`openclip-transcription`. Locking a caption preset into a reusable processing agent is covered
in `openclip-clipping`.
