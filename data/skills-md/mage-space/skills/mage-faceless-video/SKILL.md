---
name: mage-faceless-video
description: |
  Narrated faceless videos with Mage: explainers, history and science
  shorts, stories, and listicles in a consistent illustrated style (stickman
  cartoon, paper diorama, pastel flat 2D, hand-drawn ink, claymation,
  whiteboard, watercolor, pixel art, and more), with a voiceover, no
  presenter on camera. Researches the facts, writes the narration, locks the
  look with a Mango 3 style key, and renders clips with narration and sound
  on Cherry 2 Pro; longer videos are made in blocks and joined. Use when:
  "faceless video", "faceless YouTube / TikTok channel", "explainer video",
  "narrated video about…", "animated story", "stickman video", "history
  short", "make a video explaining…", "YouTube Shorts about a fact".
  NOT for: videos with a presenter or product demo (use mage-ugc-video),
  thumbnails for the video (mage-youtube-thumbnail), photoreal films, or
  editing an existing video (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems. Joining clips into one file needs a shell with ffmpeg.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Faceless Video

Make a narrated video with no one on camera: a clear script, one locked illustrated style, a steady narrator voice, and scenes that match every line.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_reference` (for a narrator voice). If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Facts.** For a real topic, use your web search or research tools and keep a short source list. Never script facts from memory alone, and never invent quotes, dates, or numbers. For a personal story, use only what the user tells you.

## UX rules

1. Ask in two turns, never merged. **Turn 1, style:** show the style menu (`references/styles.md`) as options, or accept a custom style or style images. **Turn 2, production:** length, aspect (`9:16` Shorts/Reels/TikTok by default, `16:9` for YouTube), narration language, and voice (describe it, or pick a saved voice `@handle`). Skip a question the request already answers.
2. Show the script and the style key image before rendering video, with the total price; wait for a yes.
3. Keep every visual non-photorealistic and consistent; no real people's likenesses.
4. Deliver the final video (or the ordered clips) with the duration, style, and a Sources list for factual topics. Links expire after 30 days.

## Plan

| Length | Plan |
|---|---|
| Up to 15 s | One clip |
| 15–30 s | One clip of 20–30 s, or two of 15 s |
| Over 30 s | Blocks of 10–15 s, one scene each, joined at the end |

Each block holds about 2.5 spoken words per second: roughly 25 words for 10 s, 35 for 15 s.

## Workflow

1. **Research and script.** Hook in the first line, one idea per block, a payoff at the end. Spell out numbers as spoken. Label blocks: `Block 1: "<narration>"`.
2. **Style key.** One Mango 3 (`mango`, `mango-v3`) image in the chosen style and aspect, from the recipe in `references/styles.md`: a representative scene from the video. Its URL becomes the style reference for every clip. Show it and let the user approve or adjust (cheap).
3. **Narrator voice** (for more than one block). For the same voice in every block, make a 10-second sample with Seed Audio (`seed_audio`) in the chosen voice, save it with `create_reference` (`kind: "audio"`), and mention its `@handle` in every clip prompt. A saved voice the user already has works the same way.
4. **Clip prompts,** one per block, from the template in `references/styles.md`: STYLE (the same descriptor in every block), SCENE (what's on screen for this line), MOTION, NARRATION (the exact line), SOUND (ambience or music bed, no other voices).
5. **Render** with Cherry 2 Pro (`cherry`, `cherry-2-pro`), style key in `image`, the chosen `aspect_ratio`, `duration` per block (`"10"` or `"15"`, up to `"30"` for a single clip), `resolution: "720p"`. Cherry Mini (`cherry-mini`) or Lemon (`lemon`) make cheaper drafts. `get_model`, `estimate_cost` for every block, quote the total, then `generate` all blocks (new UUID `idempotency_key` each) and wait on each with `get_request` (`wait_seconds: 120`).
6. **Review.** Regenerate only a block whose style drifted, whose narration was cut off, or that shows text or faces it shouldn't. Tighten that block's line if it ran long.
7. **Join** multi-block videos when you can run commands:

   ```bash
   # download each block in order as block-01.mp4, block-02.mp4, …
   printf "file '%s'\n" block-*.mp4 > blocks.txt
   ffmpeg -f concat -safe 0 -i blocks.txt -c:v libx264 -crf 20 -c:a aac -movflags +faststart final.mp4
   ```

   Without a shell, deliver the blocks as a numbered list in order and say they're ready to join in any editor.

## Deliver

```text
Faceless short ready (30 s, 9:16, paper diorama, 10,395 Gems): https://…
Sources: <list>
```

Offer once: a thumbnail (`mage-youtube-thumbnail`) or another cut in a different style.

## References

- `references/styles.md`: the style menu, style-key recipes, and the clip prompt template.
