---
name: openclip-ugc-ads
description: Generate short vertical UGC-style ad clips from a structured creative brief with OpenClip, picking from a roster of AI creators. Use when asked to "make a UGC ad", "generate a talking-head ad", "create TikTok ad creative", "test some ad angles", "make an AI influencer video", "generate ad variations", or "make a product ad without filming".
---

# OpenClip: UGC ad generation

`generate_ugc` renders a short vertical UGC-style clip (roughly 7 to 12 seconds) from a creative
brief. Free accounts get ONE generation per day. Paid accounts are metered in credits by the
seconds rendered.

Renders are heavy. Expect a couple of minutes per clip, not seconds.

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

1. **Discover the roster FIRST.** `list_ugc_creators` returns the valid `creator` and
   `start_frame` values for this team: a curated roster plus the team's own saved creators,
   grouped by niche. Never guess a creator name, pick one from this call.
2. **Generate.** `generate_ugc(...)` with either:
   - `brief_name` - a server-side preset, the fast path, or
   - `brief` - an inline object of structured creative fields (`character` and friends).
3. **Poll.** Returns a `ugc_job` hashid. Poll `get_ugc_job_status(ugc_job)` every 10 to 15
   seconds. `queued` / `rendering` are in flight. `completed` returns `video_url` plus
   `result_meta` (duration, dimensions, fps, seed). `failed` returns `error`.
4. **Review past work.** `list_ugc_jobs` lists a team's previous UGC clips, and is how you find
   a `ugc_job` id to poll if you lost it.

## The brief is structured, not a prompt

This is the thing agents get wrong most. `brief` is **not** a prose prompt. It is an object of
discrete creative fields (`character`, and the other fields the API accepts). Writing a
paragraph into one field wastes the structure and produces mush.

Write each field as a concrete, physical, filmable detail:

- Name what is in frame, not how it should feel. "Holding the bottle at chest height, kitchen
  counter behind" beats "energetic and aspirational vibes".
- One idea per field. Do not stack three beats into `character`.
- Constraints produce better output than adjectives. A specific setting, a specific prop, and a
  specific action beat "high quality, professional, engaging".

## Testing ad angles

When the user wants variations rather than one clip, change ONE variable per render so the
comparison means something:

- Same creator, different hook.
- Same hook, different creator, when you are testing who lands the message.
- Same everything, different `start_frame`, when you are testing the thumbnail moment.

Free accounts get one generation per day, so on a free account, spend it on the single most
different angle rather than a near-duplicate. Check `get_account` before promising a batch.

## Rules

- `list_ugc_creators` before every first generation in a session. The roster is team-specific
  and changes.
- Always poll. Renders take minutes, `generate_ugc` returns immediately.
- Clips are short by design, roughly 7 to 12 seconds. Do not promise a 60 second ad.
- Free tier is ONE generation per day. Say so before the user plans a batch on a free account.
- `result_meta` includes the `seed`. Keep it when the user liked a render and wants a close
  variant.

## Errors

Tool failures come back as a tool result with `isError: true` and a plain-text message, not an
HTTP status. `"Not authenticated. Reconnect your OpenClip token."` means reconnect or re-mint
the token. Validation messages (an unknown creator, a malformed brief) come back as the message
text, fix the argument and retry.

## Example prompts to actions

- "Make a UGC ad for my app" - `list_ugc_creators`, pick a fitting creator,
  `generate_ugc(brief={...})`, poll `get_ugc_job_status`, return `video_url`.
- "Give me three angles to test" - one render per angle, one variable changed each time, poll
  each. Check the daily limit first on a free account.
- "Use the same girl as last time" - `list_ugc_jobs` to find the previous job, read its creator,
  reuse it.
- "What creators can I use?" - `list_ugc_creators`, show them grouped by niche.

## Related

Clipping real long-form footage into shorts is `openclip-clipping`. Free trimming, cropping, and
compression of the generated clip is `openclip-video-editing`.
