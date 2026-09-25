---
name: scenario-vidu
description: "Use when generating video with Vidu models on Scenario via MCP: text-to-video, image-to-video from a single still, start and end frame interpolation, reference-to-video keeping characters and props consistent from up to 7 reference images or reference videos, anime-style motion, movement amplitude control, or deciding between Q3, Q2, Q1, and 2.0 tiers. Keywords: Vidu Q3 Pro, Q2 Turbo, Shengshu Technology, T2V, I2V, R2V, Reference2V, start end frame, background music toggle."
license: MIT
---

# Scenario Vidu Video

## Overview

Vidu, Shengshu Technology's video family on Scenario, ships one model per mode per tier instead of folding every mode into one model: the model name carries both the mode (T2V, I2V, Reference2V) and the tier (Q3, Q2, Q1, 2.0). Fifteen members were live at authoring time, so `search` the family, pick by name, and treat `model_schema_get` as the contract, since caps disagree at every tier boundary.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Choose the model line by what you hold (input names from the live schemas):

| You hold             | Line        | Key inputs                                                |
| -------------------- | ----------- | --------------------------------------------------------- |
| Text only            | T2V         | `prompt`, `aspectRatio`, `duration`, `resolution`         |
| One still to animate | I2V         | `generationType: "image_to_video"`, `images` with one id  |
| Start and end frames | I2V         | `generationType: "start_end_to_video"`, `images` with two |
| Identity references  | Reference2V | `images`, up to 7                                         |

In start/end mode array order decides: the first id opens the clip, the second closes it, and `generationType` must match the image count. No I2V member exposes `aspectRatio`: geometry follows the source stills. Reference2V carries identity (characters, props, palette), not the opening state; to open on an exact frame, switch to an I2V member. One Reference2V member (Q2 Pro at authoring time) also took `videos`: up to 2 reference videos (one of 8 seconds or two of 5, 100MB each, aspect between 1:4 and 4:1), requiring `images` or `videos`.

Every member takes `seed`. `audio` (default false) is a background-music toggle, not sound design, and on most Q2 members it silently does nothing at 9 or 10 seconds.

## Tier picks the caps

At authoring time: Q3 ran 1 to 16 seconds; Q2 ran 1 to 10, with start/end mode capped at 8; 2.0 I2V took exactly 4 or 8 seconds, and 8 only at 720p; Q1 exposed no duration or resolution at all, and 2.0 Reference2V no duration. `movementAmplitude` (auto, small, medium, large) exists only on the Q1 and 2.0 lines, and the general or anime `style` selector only on Q1 I2V members; on Q2 and Q3, motion energy and style go in the prompt. Turbo and Fast variants cut latency at the same duration and resolution caps as their Pro siblings. `duration` and `resolution` both move cost, several-fold on one member alone, so `dry_run` the exact job before a batch.

## Two prompt shapes

T2V and I2V want a 120 to 180 word single-shot paragraph in present tense: scene and lighting, one or two motions, one camera move in plain verbs (pan, dolly, zoom in), emotion as physical cues ("her shoulders slump"), no cuts, and in I2V nothing that is not already in the still. Reference2V wants the opposite: one short sentence, roughly 20 to 40 words, naming which element comes from which reference by position, "the character from image1 wearing the armor from image2, walking through a snowstorm". Prompt length caps differ per member, 2000 to 5000 characters.

## Worked example: bridging two keyframes

1. `search` with `target="models"`, `query="vidu"`, `public=true`. Prefer the newest tier in the mode you need, e.g. `model_vidu-i2v-q3-pro` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: duration bounds, resolutions, defaults.
3. `upload_asset` the start and end stills (see the `scenario` skill) for two asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"generationType": "start_end_to_video", "images": ["asset_start", "asset_end"], "prompt": "The knight slowly lowers his sword as dusk settles over the courtyard. The camera dollies in on his face.", "duration": 8, "resolution": "1080p"}`; expand the prompt to the full paragraph shape above in real runs, and re-estimate after any change to duration or resolution.
5. Re-run `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and check both anchor frames landed.

## Common mistakes

- Two images with `generationType: "image_to_video"`, or one with start/end: the type must match the image count, and order sets start versus end.
- Expecting a Reference2V clip to open on a reference image: references fix identity, not frame one; use an I2V member for exact opening frames.
- Carrying caps across tiers: 16 seconds is Q3 only; 2.0 I2V accepts only 4 or 8, and 8 forces 720p.
- Prompting dialogue or sound effects: `audio` only adds background music, and it drops out at 9 or 10 seconds on most Q2 members.
- A 150-word paragraph on Reference2V, or a bare sentence on T2V: the two modes want opposite prompt shapes.
- Passing `videos` to any Reference2V member: at authoring time only one took reference videos; read the schema first.
