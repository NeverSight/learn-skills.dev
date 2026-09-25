---
name: scenario-minimax-video
description: "Use when generating video with MiniMax Hailuo models on Scenario via MCP: text-to-video, image-to-video from a first frame, first and last frame anchors, reference images for character or style consistency, motion from reference videos, voice from reference audio, native stereo audio with synced dialogue and SFX, bracketed camera commands, or choosing between H3 and Hailuo 2.3 or 2.3 Fast. Keywords: MiniMax, Hailuo 3.0, H3, Hailuo 2.3, T2V, I2V, V2V, 2K, native audio, promptOptimizer."
license: MIT
---

# Scenario MiniMax Video

## Overview

MiniMax's Hailuo video family on Scenario spans two generations. H3 (Hailuo 3.0) folds text, keyframe, and reference conditioning into one model and generates stereo audio in the same pass; the Hailuo 2.3 pair (standard and Fast) are lean text and first-frame animators. Discover them with `search` and treat `model_schema_get` as the contract: the generations agree on almost nothing, not even the spelling of a resolution.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

H3's mode follows from the inputs (names from the live schema):

| Mode         | Inputs                                                 | Behavior                                                                                 |
| ------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Text         | `prompt`                                               | `aspectRatio` honored (21:9 through 9:16, default `adaptive`)                            |
| First frame  | `firstFrameImage` (+ `prompt`)                         | shape follows the image; `aspectRatio` ignored                                           |
| First + last | `firstFrameImage` + `lastFrameImage`                   | `lastFrameImage` is valid only alongside `firstFrameImage`                               |
| Reference    | `referenceImages`, `referenceVideos`, `referenceAudio` | guides subject, style, motion, and voice, not forced frames; `aspectRatio` still applies |

Keyframes and references are mutually exclusive: neither frame combines with any reference array. `referenceAudio` never rides alone; it requires at least one image or video reference. Reference parameters are arrays even for one asset. At authoring time H3 took 9 reference images, 3 videos, and 3 audio files (videos and audio each 2 to 15 seconds, and 2 to 15 seconds in total), 5 to 15 seconds of output, at `768P` or `2K`.

The 2.3 members take only `prompt` and `firstFrameImage`, plus a coupled pair: at authoring time 10 second `duration` was available only at `768p`, and `1080p` only at 6 seconds. Their `promptOptimizer` (default true) rewrites the prompt before generation: leave it on for thin prompts, switch it off when engineered wording must survive verbatim. H3 has no such switch, and no member has a seed.

## Picking the member

H3 led a public image-to-video arena at authoring time and is the family's only member with references, a last-frame anchor, or native audio. It is also the slow, expensive one: a typical 2K clip cost around five times a 2.3 run and took four times as long, and reference media adds more (the first 5 reference images are free, each further image is billed, and reference videos bill per second of uploaded footage). So iterate on 2.3 Fast, spend H3 on keepers, and `dry_run` the same job on both before a batch. The 2.3 line holds its own on motion coherence and stylized rendering (anime, illustration, ink wash, game CG).

## Camera in brackets, motion in moderation

The whole family reads bracketed camera commands inline in the prompt: `[Push in]`, `[Pull out]`, `[Pan left]`, `[Tilt up]`, `[Truck right]`, `[Pedestal up]`, `[Zoom out]`, `[Shake]`, `[Tracking shot]`, `[Static shot]`. Up to three moves combine in one bracket (`[Pan left, Pedestal up]`); separate brackets sequence them. Keep 2 or 3 motion cues per shot in total: piling on moves invites background wobble and texture flicker. Image-to-video tends to drift even unprompted, so lock statics explicitly ("Static camera, locked shot, tripod mounted").

Write the rest as natural prose, ordered camera, subject, action, scene, lighting and mood, style. On H3, sound lives in the prompt too: describe dialogue lines, SFX, and ambience inline so they sync to the action; no audio parameter exists to switch instead.

## Worked example: a character clip from reference stills

1. `search` with `target="models"`, `query="minimax hailuo"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_minimax-h3` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: modes, caps, and allowed values before anything else.
3. `upload_asset` two clean, evenly lit character stills (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "[Tracking shot] The scout from the reference images sprints across a rooftop at dusk, coat snapping in the wind, warm rim light, footsteps and distant traffic in the audio, cinematic realism.", "referenceImages": ["asset_a", "asset_b"], "duration": 8, "resolution": "2K", "aspectRatio": "16:9"}` for the cost estimate; re-estimate after changing duration, resolution, or the reference count.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`; H3 at 2K commonly runs several minutes.
6. `asset_display` the output and review it with sound on: dialogue and SFX sync are part of what you paid for.

## Common mistakes

- Combining `firstFrameImage` with a reference array: keyframes and references never mix.
- Passing `referenceAudio` alone: it requires at least one image or video reference.
- Sending `lastFrameImage` without `firstFrameImage`: the pair anchors both endpoints or neither.
- Expecting `aspectRatio` to win over a first frame: the shape follows the image.
- Carrying one member's values to another: 10 seconds is 768p-only on 2.3, 1080p is 6-second-only, and H3 spells resolutions `768P` and `2K` where 2.3 spells `768p` and `1080p`.
- Stacking camera moves: past 2 or 3 cues the background wobbles and textures flicker.
