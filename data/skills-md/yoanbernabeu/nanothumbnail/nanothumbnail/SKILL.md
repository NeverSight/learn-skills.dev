---
name: nanothumbnail
description: Create, edit, critique and export YouTube thumbnails by driving the NanoThumbnail studio (Google Nano Banana models) through its MCP server. Use when the user wants a YouTube thumbnail, video cover or Shorts cover made, improved, A/B-compared or exported — "make a thumbnail for my video", "miniature YouTube", "improve this thumbnail", "which thumbnail is best".
---

# NanoThumbnail

NanoThumbnail is a free, local-first studio that runs in the user's browser and generates thumbnails with Google's Nano Banana models, on the user's own API key. The `nanothumbnail` MCP server lets you drive it: every action shows up live in the studio, so work *with* the user, not around them.

Answer in the user's language. Thumbnail text (`overlayText`) goes in the language of the video.

## 0. Check the connection

The tools come from the `nanothumbnail` MCP server (`get_state`, `generate`, `edit_thumbnail`…).

- Tools missing → the server isn't installed. Tell the user to run `claude mcp add nanothumbnail -- npx -y nanothumbnail-mcp` (other clients: an MCP server running `npx -y nanothumbnail-mcp`), then restart the session. Stop there.
- A tool says the studio is not connected → call `open_studio`. It opens the studio in the browser; the user must click **Allow** once. If it times out, give the user the pairing code from the error message.
- Start every session with `get_state`: it tells you the project, the brief already typed, the people (personas) available, whether an API key is set, and recent thumbnails.

## 1. Money first

Each image costs the user real API credits (more with `nano-banana-pro` and higher resolutions).

- Explore with `count: 1` or `2`. Ask before `count: 4`, 4K, or more than ~6 generations in a row.
- `nano-banana-2` is cheaper and faster for exploring; `nano-banana-pro` renders text and fine detail best — switch to it (`set_output`) for the final round.
- `score_thumbnail`, `rank_thumbnails` and `suggest_concepts` are cheap text/vision calls; use them freely.
- Never loop "generate until it's good". After 2 rounds without progress, stop and ask the user.

## 2. Workflow

1. **Understand the video.** You need the title and the one thing that makes someone click (the promise, the stakes, the surprise). If the user gave a script or a URL, extract that. Ask at most one question if it's truly missing.
2. **Project.** One project per video: `new_project` named after the video, unless `get_state` shows the user is already working on it.
3. **Concept.** Propose 2–3 distinct angles in one short message (emotion/reaction, result/transformation, mystery/object…) — write them yourself or call `suggest_concepts`. Let the user pick unless they told you to decide.
4. **Assets.** If the creator appears in the thumbnail, select their persona with `set_people` (identity is locked from their photos). Attach products, screenshots or style examples with `add_reference` (absolute `path` or `url`) and a clear `label`. To restyle an existing video's thumbnail, `remix_youtube`.
5. **Generate.** `generate` with `videoTitle`, `brief`, `overlayText`, `styleId` (see `list_styles`). Write the brief as described in [references/craft.md](references/craft.md). Look at the previews you get back.
6. **Critique honestly.** Check the result against the checklist in [references/craft.md](references/craft.md). `score_thumbnail` gives a structured critique with `suggestedEdits`.
7. **Iterate by editing, not regenerating.** When the composition works, fix details with `edit_thumbnail` — one change per call ("make the text yellow", "remove the cable on the left"). Use `region` (fractions 0–1 of width/height) to confine a change to one area. Regenerate only when the concept itself is wrong.
8. **Compare.** With 2–4 good candidates, `rank_thumbnails` (also shows them side by side to the user). `set_view` with `view: "feed"` shows the winner among other videos, as a viewer would see it — suggest the user looks.
9. **Deliver.** `set_favorite` on the winner, then `export_thumbnail` (default `youtube` = 1280×720 JPEG under 2 MB) to the path the user wants. Report the path and one line on why this one.

## 3. Rules of thumb

- Text on the thumbnail: 0–4 words, never a repeat of the title — it adds to it. When text keeps coming out wrong, switch `textMode` to `"space"` and tell the user to add the text in their editor.
- One focal point. A face showing a clear emotion beats a busy scene. Big, close, contrasted.
- Must read at phone size: if you can't tell what it is from a 168×94 px glance, it fails.
- Keep the bottom-right corner free (YouTube's duration badge). `set_view` with `safeZones: true` shows it.
- Never invent a real person's likeness: people come from personas or references the user provided.
- Don't change the user's API keys or provider, don't delete their work; the tools won't let you anyway.

## 4. Handing back

Keep chat updates short: what you did, what you see, what you suggest next. The user sees the images in the studio; don't describe them at length. When you stop, say where things stand (project, favourite id, exported file).
