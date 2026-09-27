---
name: scenario-gemini-omni
description: "Use when generating, extending, or editing video with Gemini Omni models on Scenario via MCP: text-to-video, image-to-video from a first frame, reference-to-video keeping a character, product, or place consistent, appending footage to a clip, restyling footage by prompt (season, wardrobe, art style), native audio with dialogue and ambience, or picking between first-frame and reference conditioning. Keywords: Gemini Omni Flash, 1.1 Flash, Google, T2V, I2V, V2V, extend, subject consistency."
license: MIT
---

# Scenario Gemini Omni Video

## Overview

Gemini Omni, Google's video family on Scenario, splits its modes across catalog members instead of folding them into one model: a text and first-frame generator (ranked first for text-to-video in public arena voting at authoring time), a reference-to-video member for subject consistency, an edit member that restyles existing footage, and on the newer 1.1 Flash line an extend member that appends footage to a clip. Every member generates audio in the same pass. Pick the line and the member by mode with `search`, reading ids and descriptions rather than rank (the newer 1.1 members ranked below the original line at authoring time), then treat `model_schema_get` as the contract. Gemini image models are the `scenario-gemini-image` skill's domain; Gemini TTS belongs to audio.

Connection and the core loop: see the `scenario` skill; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Two lines at authoring time, Flash and 1.1 Flash, one member per mode (names from the live schemas):

| Member             | Mode                | Inputs                                                                                                                                          |
| ------------------ | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Gemini Omni        | text or first frame | `prompt` and/or `image`, plus optional `referenceImages` (up to 7); on 1.1 an optional `lastFrameImage` beside `image`                          |
| Reference-to-Video | consistent subjects | `referenceImages` required (1 to 7), `prompt` optional; on 1.1 a `referenceVideo` of 3 s or less can replace the images or join up to 5 of them |
| Edit               | restyle a clip      | `video` and a change `prompt`, both required; optional `referenceImages` (1 to 5)                                                               |
| Extend (1.1 only)  | continue a clip     | `video` required, `prompt` optional                                                                                                             |

At authoring time both generators took `duration` 3 to 10 seconds (default 8) and `aspectRatio` `16:9` or `9:16`. Edit exposes neither knob: length and shape follow the source clip. Extend inherits the shape too (no `aspectRatio`) but takes `duration` 3 to 10 (default 6) as footage appended after the source, so an 8 s clip plus 6 returns about 14 s. The original Flash members render 720p only; the 1.1 Flash line adds `resolution` on every member: `360p` a faster draft tier, `720p` the default, `1080p` and `4k` upscaled. The tier does not move price (at authoring time a generation quoted the same at 360p and 1080p, and so did Extend), so a cheap draft is a shorter `duration`, not a lower tier. Seed and negative prompt exist nowhere in the family. Cost moves with `duration`, a first-frame `image`, Reference-to-Video's references, and Edit's and Extend's source clips; Edit spanned the family's widest cost range at authoring time and its jobs ran about twice as long, so `dry_run` before editing anything long.

## Sound is prompted, not switched

No member has an audio parameter: every clip arrives with generated dialogue, ambience, and effects, and the prompt is the only lever. On the generators, end the prompt with an explicit audio line naming what should be heard ("crackling campfire, distant owls") and put spoken words in quotes; leave it out and the model chooses for you. On Edit, never prompt audio: it regenerates to match the new look on its own.

## Identity from images, change from words

Reference-to-Video takes the subject's look from `referenceImages`, and re-describing it in the prompt fights the images. Call the subject "the character" or "the product" and spend the words on action, setting, camera, and sound; several angles of one subject tighten the hold, distinct subjects share one scene, and with no prompt at all the subjects still appear. There is no first-frame anchor here: when the clip must open on an exact composition, pass that still as `image` on the base member, which also accepts references alongside it and, on 1.1, a `lastFrameImage` to interpolate towards (it needs the first frame).

Edit is the inverse: motion, camera path, and timing are locked from the source `video`, only the look moves. Lead the prompt with the change ("make it winter", "swap the red car for a vintage blue Beetle"), name the target concretely, and never ask for new choreography, cuts, or camera moves: those instructions will not take.

## Worked example: a mascot short with a consistent character

1. `search` with `target="models"`, `query="gemini omni"`, `public=true`. Pick the member by mode, here `model_google-omni-flash-r2v` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: required fields, caps, and defaults before anything else.
3. `upload_asset` two or three angles of the mascot (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "The character skips across a rain-slick plaza, catches a falling leaf, and holds it up in triumph. Overcast soft light, low tracking shot. Audio: light rain, footsteps on wet stone, one bright chirp.", "referenceImages": ["asset_a", "asset_b"], "duration": 8, "aspectRatio": "16:9"}`; references and duration move the cost, so re-estimate after changing either.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and review it with sound: the audio is part of the deliverable.

## Common mistakes

- Describing the reference subject's appearance in the prompt: identity comes from the images; write action and setting around "the character".
- Asking Edit for new motion, cuts, or re-timing: they are locked to the source; prompt only the look change.
- Passing `duration` or `aspectRatio` to Edit, or `aspectRatio` to Extend: not in their schemas; the output follows the source clip.
- Hunting for an audio toggle: none exists; steer sound in the prompt or accept the model's choice.
- Restating a first-frame `image` as a static scene: describe the motion continuing from it.
- Packing a multi-scene story into one run: 3 to 10 seconds holds one continuous beat; carry a beat past 10 seconds with Extend, or sequence shots with the `scenario-video-assembly` skill.
