---
name: scenario-grok-imagine-video
description: "Use when generating or editing video with Grok Imagine models on Scenario via MCP: text-to-video, image-to-video from a first frame, reference-to-video with @image tags for consistent people, products, or clothing, prompt-based editing, extending a clip from its last frame, native audio with lip-synced dialogue and sound effects, or choosing between first-frame and reference conditioning. Keywords: Grok Imagine Video 1.5, R2V, Grok Edit Video, Grok Extend Video, xAI, T2V, I2V, V2V."
license: MIT
---

# Scenario Grok Imagine Video

## Overview

Grok Imagine, xAI's video family on Scenario, splits its modes across single-purpose members: text and first-frame generation, reference-to-video, prompt editing, and clip extension each live in their own model, so picking the member is picking the mode. Discover them with `search` and treat `model_schema_get` as the contract: members agree on prompt style and disagree on every cap. The Grok Imagine image models belong to the `scenario-grok-imagine-image` skill.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Pick the member by intent (input names from the live schema):

| Intent                   | Member        | Inputs                                                     |
| ------------------------ | ------------- | ---------------------------------------------------------- |
| Text-to-video            | Video 1.5     | `prompt` alone; `aspectRatio` auto lands on 16:9           |
| Animate a still          | Video 1.5     | `image` + `prompt`; auto follows the image ratio           |
| Identity, opening free   | Video 1.5 R2V | `referenceImages` + `prompt` tagging `@image1`             |
| Restyle or swap in place | Edit Video    | `video` + a prompt naming only the changes                 |
| Continue a clip          | Extend Video  | `video` + a continuation prompt; `duration` is new seconds |

Caps are per member, so read them off `model_schema_get`. At authoring time the generation members took 1 to 15 seconds, 1 to 4 `numOutputs`, and eight `aspectRatio` values including auto; 1080p existed only on Video 1.5's text and first-frame modes, while R2V stopped at 720p and defaulted to 480p. The earlier unversioned Grok Imagine Video takes the same inputs as Video 1.5, also caps at 720p, and runs cheaper per `dry_run`. R2V took up to 7 `referenceImages`; Extend generated 2 to 10 new seconds; Edit exposed no duration or resolution and preprocessed its source down to 8.7 seconds at 720p, so trim to the segment first (see `scenario-video`). No seed, negative prompt, or camera parameter exists anywhere in the family.

## First frame or references

`image` locks frame one: the video opens on that exact composition and animates out of it. `referenceImages` (its own member, R2V) carries people, products, and clothing across the shot without deciding how it opens. Tags bind by array order: `@image1` is `referenceImages[0]` (`<IMAGE_1>` also works), and one clean subject per reference keeps control; a busy reference dilutes it. If the opening must match a composition exactly, render that still and pass it as `image`; when only a face, product, or outfit must stay consistent, use R2V and tag each reference where it acts.

## Sound is prompted, not switched

Generation members produce native audio and no parameter controls it: the prompt is the whole mixing desk. Left unaddressed, the track tends toward generic background music, so end every prompt with named sounds ("Audio: rain on glass, distant traffic") or "no music". Dialogue written in quotes with a delivery verb lip-syncs: She says calmly: "We're live." Structure the rest like a director: scene, camera, style, motion, audio, in present tense, one continuous shot, one dominant camera move, physical actions instead of named emotions. 80 to 150 words touching at least three of those layers beat a one-line scene; editing prompts run shorter, naming only what changes. Extension prompts describe the next beat, not a new scene: open with a bridge ("the shot continues"), keep the established light and cast, and restate the audio.

## Worked example: dialogue over an animated hero still

1. `search` with `target="models"`, `query="grok imagine video"`, `public=true`. Match the member by name: first-frame animation wants e.g. `model_xai-grok-imagine-video-1-5` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: fields, caps, and defaults before anything else.
3. `upload_asset` the hero still (see the `scenario` skill) to get its asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "The frame shows a knight on a cliff at dusk. She lowers her sword, turns to the camera, and says quietly: 'It ends tonight.' Slow dolly-in, wind lifting her cloak. Audio: wind, distant thunder, her line clear. No music.", "image": "asset_abc", "duration": 8, "resolution": "1080p"}` for the cost estimate; re-estimate after any change to duration, resolution, or `numOutputs`.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and watch it with sound: the audio direction is judged by ear.

## Common mistakes

- Leaving audio to the default: generic music appears; direct the sound or state "no music" in every prompt.
- Prompting an exact opening frame in R2V: references guide identity, not frame one; pass the still as `image` on Video 1.5.
- Expecting 1080p everywhere: at authoring time it existed only on Video 1.5 text and first-frame runs, and R2V silently defaults to 480p.
- Feeding Edit Video a long clip and expecting full-length output: the source is preprocessed down (8.7 seconds at authoring time); trim to the segment first.
- Reading Extend's `duration` as total length: it counts only new footage.
- Stacking camera moves or contradictory directions ("zoom in as the camera pulls back"): one dominant move per shot.
