---
name: scenario-veo
description: "Use when generating or extending video with Google Veo models on Scenario via MCP: text-to-video, image-to-video from a first frame, first and last frame transitions, reference-to-video (R2V) with asset or style reference images, native audio with dialogue, sound effects, and ambience, negative prompts, seeded reruns, extending a 16:9 clip, or choosing a quality, fast, or lite tier. Keywords: Veo 3.1, Veo 3.1 Fast, Veo 3.1 Lite, Extend Video, Google, T2V, I2V, V2V, 720p, 1080p."
license: MIT
---

# Scenario Veo Video

## Overview

Veo, Google's video family on Scenario, ships four members at authoring time: Veo 3.1 (full quality, reference images with a style switch), Veo 3.1 Fast (same modes, quicker, no switch), Veo 3.1 Lite (frame anchors only, cheapest), and Veo 3.1 Extend Video (continues a clip). Discover them with `search` and treat `model_schema_get` as the contract: members agree on parameter names and disagree on which inputs exist at all.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Mode follows from the inputs (names from the live schema):

| Mode        | Inputs                     | Behavior                                                  |
| ----------- | -------------------------- | --------------------------------------------------------- |
| Text        | `prompt`                   | `aspectRatio` 16:9 or 9:16                                |
| First frame | `image` (+ `prompt`)       | opens on that frame; a mismatched image may be cropped    |
| Transition  | `image` + `lastFrameImage` | bridges the stills; prompt one continuous move            |
| Reference   | `referenceImages` (1 to 3) | subject or style consistency; `duration` locked to 8      |
| Extend      | `video` (Extend member)    | continues the clip; 16:9 source, short side 720p or 1080p |

`image` and `referenceImages` are mutually exclusive. `referenceImagesType` exists on full Veo 3.1 alone and reads the whole array one way: `ASSET` (default) carries subjects, objects, and scenes; `STYLE` carries palette, lighting, and texture. Fast takes references without the switch; Lite takes none. Shared across the three generators at authoring time: `negativePrompt`, `resolution` (`720p`, `1080p`), `duration` (4, 6, or 8 seconds), and `seed`. `generateAudio` is required on every member and moves the price. The Extend member takes only `prompt`, `video`, `generateAudio`, and `seed`: no duration, resolution, or ratio controls. At authoring time price spanned roughly five times between Lite and full 3.1 for one image-to-video job, and one extension cost more than a fresh full generation, so aim for the shot in one 8 second pass and `dry_run` the same payload on two members before a batch.

## The soundstage is in the prompt

With `generateAudio: true`, Veo renders synchronized dialogue, effects, and ambience, and it takes audio direction literally. Put spoken lines in quotation marks, prefix effects with `SFX:` and room tone with `Ambient noise:`. A prompt with no audio direction still gets a soundtrack, just not the one you meant. When a clip needs silence for later scoring, set `generateAudio: false` rather than prompting for quiet.

## Prompt one continuous shot

Write present-tense prose ordered as cinematography, subject, action, context, style: camera and shot scale first, one primary arc, roughly 90 to 250 words. For several beats in one clip, timestamp lines work (`[00:00-00:02] Medium shot...`), spans fitting inside the chosen duration.

## Worked example: a dialogue shot from character references

1. `search` with `target="models"`, `query="veo"`, `public=true`. Prefer the newest non-deprecated hits, e.g. `model_veo3-1` and `model_veo3-1-fast` (live hits at authoring time: re-discover each session).
2. `model_schema_get` on the chosen id: confirm which reference inputs exist before writing the payload.
3. `upload_asset` two character stills (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "Medium shot, the knight lowers her visor and says, \"Hold the line.\" Torchlight flickers on wet stone. Ambient noise: distant thunder. SFX: metal visor clank.", "referenceImages": ["asset_a", "asset_b"], "referenceImagesType": "ASSET", "duration": 8, "resolution": "1080p", "aspectRatio": "16:9", "generateAudio": true}`. Estimate the same job on the Fast id (drop `referenceImagesType`, absent there) and compare.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and review with sound. To iterate on wording alone, hold an explicit `seed` fixed across reruns.

## Common mistakes

- Combining `image` with `referenceImages`: mutually exclusive; pick the opening state or consistency.
- Any duration but 8 with `referenceImages`: reference mode supports only 8 seconds.
- Sending `referenceImages` to Lite or `referenceImagesType` to Fast: the schema decides which inputs exist.
- Omitting `generateAudio`: it is required on every member; pass it explicitly.
- Extending a 9:16 clip: Extend takes 16:9 sources with a 720p or 1080p short side only.
- Writing the prompt as a list of negatives: describe the wanted scene, reserve `negativePrompt` for what to discourage.
