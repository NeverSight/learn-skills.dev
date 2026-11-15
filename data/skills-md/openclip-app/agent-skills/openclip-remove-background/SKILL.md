---
name: openclip-remove-background
description: Remove the background from an image with OpenClip and get back a transparent PNG. FREE with just an OpenClip account, no subscription. Use when asked to "remove the background", "make the background transparent", "cut out the subject", "isolate this product shot", "get me a transparent PNG", "knock out the background", or "extract the person from this photo".
---

# OpenClip: background removal

`remove_background` takes an image and returns a transparent PNG with the background cut out.
It is FREE, it needs an OpenClip account but no subscription and no credits. There are no
parameters to tune, one call does the whole job.

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
   PUT the raw bytes to `upload_url`, then pass the `id` as `file`.
   **Do NOT call `complete_upload`**, that starts the paid clipping pipeline. Free tools read
   the uploaded file directly.
2. **Call.** `remove_background(file)`. No other params.
3. **Poll.** Returns a `tool_job` hashid. Poll `get_tool_job_status(tool_job)` every 5 to 10
   seconds. `queued` / `processing` are in flight, `completed` returns a permanent CDN
   `outputs` URL for the transparent PNG, `failed` returns `error`.
4. **Return the PNG URL.** It is transparent, so it will look like it has a checkerboard or a
   black background in some previews. That is expected, the alpha channel is there.

## Rules

- Always poll, the tool is async.
- The output is always PNG. Transparency needs an alpha channel, so jpg is not an option. If
  the user wants it flattened onto a colour or resized afterwards, chain `edit_image`
  (see `openclip-thumbnails`).
- Output URLs are permanent CDN links, not signed or expiring.
- Free usage is rate limited per day with a per-file size cap. The error text explains how to
  lift a limit.

## Example prompts to actions

- "Remove the background from this photo" - `create_upload`, PUT bytes, `remove_background(file)`,
  poll, return the transparent PNG URL.
- "Cut out the product for a listing" - same, then `edit_image(file, operation="resize", ...)` on
  the output if they need specific dimensions.
- "I need this logo on transparent" - same, then hand back the PNG.

## Related

Resizing, cropping, and reformatting images is `openclip-thumbnails` (`edit_image`). Pulling a
frame out of a video to cut out is also `openclip-thumbnails` (`extract_thumbnails`).
