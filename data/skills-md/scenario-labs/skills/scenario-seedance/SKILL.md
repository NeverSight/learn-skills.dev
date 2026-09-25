---
name: scenario-seedance
description: "Use when generating or editing video with Seedance models on Scenario via MCP: text-to-video, image-to-video from a first frame, first and last frame anchors, reference-to-video with identity, product, or world references, prompt-based editing, extending a clip, audio-conditioned motion, shot sound without music, or deciding between first-frame and reference conditioning. Keywords: Seedance 2.5 and 2.0, ByteDance, T2V, I2V, V2V, multimodal references, native audio, video extension."
license: MIT
---

# Scenario Seedance Video

## Overview

Seedance, ByteDance's video family on Scenario, folds every mode below into one model that infers which from your inputs, so the conditioning you pass decides more than prompt wording. Discover it with `search` and treat `model_schema_get` as the contract: members ship side by side, agreeing on the shape and disagreeing on every number.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill; choreography held across cuts from a storyboard: the `scenario-seedance-storyboard` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Mode follows from the inputs (names from the live schema):

| Mode         | Inputs                            | Behavior                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Text         | `prompt`                          | `aspectRatio` honored (21:9 through 9:16)                                                                                                                                                                                                                                                                                                                                                                                  |
| First frame  | `image` (+ `prompt`)              | opens on that frame; `aspectRatio` ignored, size follows `resolution` and may land only near the ratio                                                                                                                                                                                                                                                                                                                     |
| First + last | `image` + `lastFrameImage`        | `lastFrameImage` is only valid alongside `image`                                                                                                                                                                                                                                                                                                                                                                           |
| Reference    | `referenceImages`                 | carries identity and world, not the opening state                                                                                                                                                                                                                                                                                                                                                                          |
| Edit         | `referenceVideos` + edit prompt   | requires `duration: -1`; output follows the source                                                                                                                                                                                                                                                                                                                                                                         |
| Extend       | `referenceVideos` + extend prompt | inferred from wording: "extend @video1", what holds (character, wardrobe, light), the action that continues, no cut; geometry follows the source; `duration` is the footage appended and the output holds only that tail (a 10 s source with `duration` 15 returned 15 s of new footage at authoring time; Auto priced as the source length), so concatenate source and tail and read the delivered length off `asset_get` |

`image` and the reference arrays are mutually exclusive. `referenceVideos` (motion conditioning) and `referenceAudio` (timing and energy conditioning) combine with `referenceImages`; on the 2.0 line reference audio also requires one image or video reference, where 2.5 takes it alone. Reference parameters are arrays even for one asset. Prompt tags bind by array order: `@image1` is `referenceImages[0]`, likewise `@video1` and `@audio1`, and the prompt says what each tag governs and what it leaves alone ("@image1 defines the bottle and label, nothing of the set"), for video and audio tags as much as for images. No seed, mask, or camera parameter exists: camera moves live in the prompt, one dominant move and one action per shot. Several actions go as timecoded beats ("0-2s ... 2-4s ..."), one per beat, the last ending inside `duration`, the shot named as one continuous take.

Caps are per member, so read them off `model_schema_get`. At authoring time 2.5 took 30 reference images, 10 videos, 10 audio, 4 to 30 seconds, up to 1080p; the 2.0, Fast, and Mini hits took 9, 3, 3, and 4 to 15, with 4k on 2.0 alone and no `lastFrameImage` on Mini. Price moves further than the caps do, six times across the family for one 4 second 480p job, so `dry_run` the same job on two members before a batch.

## The conditioning rule

In reference mode, frame one anchors to the base state of the reference world, and no prompt wording overrides it. If the shot must open in a specific state, render a still of it and pass it as `image`; use `referenceImages` when only identity, world, and palette matter. Deciding this per shot before generating is worth more than any prompt tuning.

## Sound from the shot, music from elsewhere

`generateAudio` (default true) is one switch over the whole track: it scores the shot as well as sounding it. A score written inside a shot survives no cut, since each shot invents its own key and tempo and the next one restarts them.

So run the lanes apart. Keep `generateAudio: true` for what the picture makes, footsteps, impacts, room tone, dialogue, each landing on frame, and exclude the score in the prompt ("diegetic sound only, no music, no score"). Spoken lines go in quotes, sized to the clip's seconds, with the speaker named and the delivery in two or three words. Score the sequence once with a music model (see the `scenario-audio` skill) and lay that track over the assembled cut (see the `scenario-video-assembly` skill, or `scenario-seedance-music-video` when the song comes first): re-scoring then costs one audio run, not every shot again.

The prompt is the only lever, so listen to what comes back: when music leaks in anyway, re-run that shot with `generateAudio: false` and add sound from a sound-effects or video-to-audio model.

## Worked example: a product shot from references

1. `search` with `target="models"`, `query="seedance"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_bytedance-seedance-2-5` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: fields, caps, and defaults before anything else.
3. `upload_asset` the product stills (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "@image1 defines the bottle and label. Slow dolly-in as condensation beads. Diegetic sound only, no music. No text, no captions.", "referenceImages": ["asset_a", "asset_b"], "duration": 8, "resolution": "720p", "generateAudio": true}` for the cost estimate; re-estimate after any change to duration, resolution, or references.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and watch it with sound before the music goes on.

## Common mistakes

- Prompting an opening state in reference mode: it will not appear; pass it as `image`.
- A bare string where the schema says array: one reference still goes as `["asset_x"]`.
- Combining `image` with `referenceImages` or `referenceVideos`: mutually exclusive inputs.
- Carrying one member's caps or price to another: 30 references, 30 seconds, and 1080p are each true of one and false of the next.
- Letting shots score themselves and then cutting them together: the music restarts at every cut.
- Rendering captions, prices, logos, or UI: reserve clean space and composite text in post.
