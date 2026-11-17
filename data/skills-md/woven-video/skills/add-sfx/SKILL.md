---
name: add-sfx
description: Use when a video edit, motion graphic, app demo, reel, short, animation, or interface needs sound effects, audio cues, whooshes, impacts, beeps, glitches, camera sounds, applause, or local .wav files.
license: MIT
compatibility: Requires Node.js, network access to https://www.woven.video/sfx, and woven-sfx-mcp MCP server.
metadata:
  author: woven-video
  version: "0.2"
  site: https://www.woven.video/sfx
---

# Add SFX

Search and cache Woven SFX sound effects for projects that need local `.wav` files.

## When To Use

- A video edit, reel, short, animation, product demo, or UI needs a sound effect.
- The user asks for a whoosh, pop, beep, glitch, impact, camera sound, applause, ding, scratch, or similar audio cue.
- An edit plan already names sound ids and the files must exist locally before assembly or render.

Do not use this skill for background music, voiceover, lip sync, audio cleanup, or generated songs.

## Prerequisites

1. **MCP server configured** - skill install alone does not enable tools. If `sfx_*` tools are missing, direct the user to [references/mcp-setup.md](references/mcp-setup.md), then restart the agent.
2. **Project-local sound library** - resolved in order: `WOVEN_SFX_LIBRARY` env -> `sfx-library` in `.claude/project.md` -> `./sounds/sfx/` under cwd.

## Workflow

### 1. Search For Sounds

Call `sfx_search` with normal words. Prefer concrete sound words over editing abstractions.

```js
sfx_search({ query: "fast whoosh", limit: 5 })
sfx_search({ query: "camera shutter", limit: 5 })
sfx_search({ query: "short beep", limit: 5 })
sfx_search({ query: "glitch", limit: 5 })
```

Pick the closest result by `id`, tags, duration, and default volume. Do not invent sound ids or filenames.

### 2. Pull The Selected Sound

```js
sfx_pull({ id: "<sound-id>" })
```

Use the returned `localPath` wherever the project needs the `.wav`.

### 3. Verify Local Cache

Before assembly or render, confirm planned sounds are present:

```js
sfx_list_installed({})
```

If a planned id is missing, call `sfx_pull({ id: "<sound-id>" })`.

## Search Hints

| Need | Good queries |
|---|---|
| Transition movement | `whoosh`, `fast whoosh`, `deep whoosh` |
| UI feedback | `beep`, `click`, `ding`, `notification` |
| Camera moment | `camera`, `camera shutter`, `camera flash` |
| Digital break | `glitch`, `scratch`, `record scratch` |
| Impact or emphasis | `impact`, `drop`, `thud`, `pop` |
| Crowd reaction | `applause`, `cheers`, `gasp` |

## Recording Results

When writing an edit plan or handoff, include:

- `id` - catalog sound id
- `file` - `.wav` filename from the search result
- `localPath` - returned by `sfx_pull`
- `duration_ms` - clip length for timing
- `default_volume` - starting gain; adjust only when the mix needs it

## Common Mistakes

- Do not start from transition labels like `pull-in` or `fade`; search for the sound you want.
- Do not use a resolver workflow. Search first, then pull by returned `id`.
- Do not guess filenames. Search first, then pull by returned `id`.
- Do not use Woven SFX for music beds or voice tracks.
