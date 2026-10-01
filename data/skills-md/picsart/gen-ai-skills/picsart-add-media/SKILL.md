---
name: picsart-add-media
description: Bring the user's own clips, photos, or files into Picsart.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, upload, local-files, widget]
---

# Add Media (Upload Widget)

Picsart's MCP tools take **URLs**, not local paths, and most agent hosts (browser-based chats,
Claude Code without shell access, ChatGPT web) can't read a file straight off the user's disk
either. The fix is a browser-based **upload widget**: an MCP tool opens a drag-and-drop panel in
the user's browser, the browser uploads the file directly to Picsart's CDN, and the widget hands
the resulting URL back to you. No file bytes ever pass through a tool call.

## When to Use

Fires on things like "I have 3 video clips", "here are my photos", "use my footage", "combine
these clips" — anything where the media is the user's own and you don't already have a link to
it.

Reach for this whenever the next step needs a URL (`image_url`, `video_url`, `startFrame`, …) and
the source is something on the user's own machine, a chat attachment you can't fetch, or anything
else not already a public `https://` link.

## Prerequisites

A Picsart MCP connector present in the current tool list. This skill calls whichever of these is
connected:

- **`picsart_upload_widget`** — on the Picsart MCP connector (tools prefixed `picsart_*`). This
  variant also offers a "Save to Drive" option and a Drive-browsing tab, because that connector
  has Drive access.
- **`mp_upload`** — on the Picsart media-tools connector (tools prefixed `mp_*`). This variant has
  no Drive integration; its second tab is "Use existing" (picks from `known_urls` you pass in),
  not a Drive browser.

If both are connected, either works — prefer whichever the current tool list actually shows first.
If neither is connected, say so; don't guess a tool name.

## How to Run

_No script to run — this skill is one tool call plus a short wait for the user's next message._

## Quick Reference

| Argument | What it does |
|---|---|
| _(none)_ | Opens the widget with no pre-filled context — a plain drag-and-drop |
| `purpose` | Label shown on the dropzone (e.g. `"product photo"`) |
| `accept` | Restrict to `image`, `video`, or `audio` |
| `detected_files` | Filenames you can see in the conversation but can't reach yourself (e.g. a chat attachment) — rendered as a *hint* only |
| `known_urls` | URLs already produced earlier in the conversation, seeded as pickable chips so the user isn't asked to re-upload something already available |

## Procedure

### 1. Call the upload tool

Call `picsart_upload_widget` or `mp_upload` (per Prerequisites) with whichever of `purpose`,
`accept`, `detected_files`, `known_urls` apply. All arguments are optional — calling with none
just opens the widget.

```json
{ "purpose": "product photo", "accept": "image", "known_urls": ["https://cdn.picsart.io/…already-uploaded.jpg"] }
```

- `detected_files` is a **label hint only, never a filter** — it's model-supplied and can be
  wrong or hallucinated. The user can still drop any file they want; don't tell them a file is
  "not accepted" because it wasn't in your `detected_files` list.
- `known_urls` saves a re-upload: if a URL already exists from earlier in the conversation (a
  prior generation result, a prior upload), pass it here so it shows up as a chip the user can
  pick instead of finding the file again.

### 2. Tell the user what to do, then wait for their next message

The widget reports the uploaded URL(s) back to you via a mechanism most agent hosts only deliver
on the **user's next message** — not instantly within the same turn. This is a real two-turn
handshake, not a delay you can poll through.

Say something like: "I've opened the upload panel — drop your file in and let me know once it's
there." Then stop and wait. Do **not** claim you can't see the file, or that the upload failed,
just because nothing arrived in the same turn you called the tool.

### 3. Hand the URL to the tool the user actually wanted

Once the URL comes back (on the user's next message), pass it into the URL-shaped parameter of
whatever tool the user's original request needs (`image_url`, `video_url`, etc.).

## Pitfalls

- **Expecting the URL in the same turn.** It won't be there — see step 2. Prompt the user and
  wait for their next message instead of reporting failure early.
- **Treating `detected_files` as a filter.** It's a display hint for filenames you can see but
  can't fetch. Never reject or second-guess a file the user actually drops based on this list.
- **Re-asking for a file that's already uploaded.** Check the conversation for a URL you already
  have before opening the widget — pass it via `known_urls` instead of starting over.
- **Guessing the tool name.** `picsart_upload_widget` and `mp_upload` live on different
  connectors with a real feature difference (Drive tab vs. "Use existing" tab) — read what's
  actually connected rather than assuming one is always present.

## Verification

- The tool call that opened the widget returned without error.
- A URL came back on a subsequent user message and looks like a real hosted link (not a local
  path).
- The downstream tool call accepting that URL didn't fail on the URL itself.

## Related

- [`picsart-api`](../picsart-api/SKILL.md) — the MCP tool catalog this skill feeds URLs into.
