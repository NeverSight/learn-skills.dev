---
name: scenario-luma-video
description: "Use when generating or editing video with Luma Ray models on Scenario via MCP: cinematic text-to-video, image-to-video from a start frame, start plus end frame anchors, seamless looping clips, HDR output, restyling footage while preserving motion with edit strengths and face, pose, depth, or trajectory controls, reframing to another aspect ratio by outpainting, or budget prompt edits on real footage. Keywords: Luma, Dream Machine, Ray 3.2, Ray 3, Modify Video, Reframe, T2V, I2V, V2V, loop, HDR."
license: MIT
---

# Scenario Luma Video

## Overview

Luma's video line on Scenario is four sibling models, one per mode: Ray 3.2 generates from text or frame anchors, Ray 3.2 Edit restyles footage under structural controls, Ray 3.2 Reframe outpaints to a new aspect ratio, and Modify Video makes budget prompt edits. Route by member before tuning anything; Luma's image models belong to the `scenario-luma-image` skill. Discover the live set with `search` and treat `model_schema_get` as the contract.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Each mode is its own model (names from the live schemas, caps as of authoring time):

| Member          | Inputs                                | Behavior                                                                 |
| --------------- | ------------------------------------- | ------------------------------------------------------------------------ |
| Ray 3.2         | `prompt` (+ `startFrame`, `endFrame`) | text or image to video; `endFrame` is only valid alongside `startFrame`  |
| Ray 3.2 Edit    | `video` + `prompt`                    | restyles while keeping motion and timing; `editStrength` plus controls   |
| Ray 3.2 Reframe | `video` + `prompt` + `aspectRatio`    | fits a new ratio by outpainting, never cropping; prompt fills the canvas |
| Modify Video    | `video` (+ `prompt`, `firstFrame`)    | budget prompt edits via a `mode` ladder; source up to 30 seconds, 100 MB |

On Ray 3.2 the options veto one another. At authoring time `duration` was a unit string, "5s" or "10s", never a number; "10s" refused `loop`, `hdr`, `startFrame`, and `endFrame`. `hdr` required 720p or 1080p from the 540p, 720p, 1080p `resolution` list; six `aspectRatio` values ran 9:16 through 21:9. Edit and Reframe share that resolution list; Modify Video has no resolution parameter. `duration`, `resolution`, and `hdr` each move the price (1080p ran several times 720p's cost and wait), so `dry_run` the option set before a batch.

## Two editors, one strength ladder

Ray 3.2 Edit and Modify Video restyle through the same nine-value ladder, `adhere_1` through `reimagine_3` (adhere stays close, flex restyles but keeps recognizable elements, reimagine transforms), and share little else. Edit names the ladder `editStrength`; Modify names it `mode`. Edit takes a guide image as `startFrame`; Modify's `firstFrame` is an edited copy of the source's own first frame, not an arbitrary style image. Edit alone offers `keyframes` (up to 64 image-and-index anchors, mutually exclusive with the single `startFrame` guide), face, pose, depth, normals, and trajectory conditioning toggles, resolution choice, and `hdr`; or pass `autoControls: true` instead of a manual `editStrength`. The price gap ran near two orders of magnitude at authoring time, so `dry_run` the same clip on both and pay for Edit's controls only when the edit needs them.

## Prompt motion, not adjectives

Ray rewards natural-language prompts of roughly 50 to 300 words built around motion: a subject mid-action, one named camera move (slow push-in, handheld follow), and one physical consequence of the action (droplets scattering, dust rising). Concrete lighting language lands directly. With `loop`, hold motion intensity constant (steady rain, drifting steam) so the cycle closes cleanly. On Reframe, prompt only the edges: describe what the new canvas should contain and leave the original subject alone.

## Worked example: a 16:9 hero clip recut for 9:16

1. `search` with `target="models"`, `query="luma"`, `public=true`. Prefer the newest non-deprecated generation, e.g. `model_luma-ray-3-2` and its Edit and Reframe siblings (live hits at authoring time: re-discover each session).
2. `model_schema_get` with the generator id: options and their vetoes before anything else.
3. `upload_asset` the product still (see the `scenario` skill) to get an asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "A crystal perfume bottle catches soft window light as a single drop arcs off the stopper, slow push-in, product commercial style.", "startFrame": "asset_a", "duration": "5s", "resolution": "1080p", "aspectRatio": "16:9"}`; re-estimate after any option change.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `model_schema_get` the Reframe sibling, then `model_run` with `parameters={"video": "<generated asset id>", "aspectRatio": "9:16", "prompt": "continue the marble counter downward and the softly lit wall upward", "resolution": "1080p"}`, same wait discipline.
7. `asset_display` both and inspect the outpainted edges before delivery.

## Common mistakes

- `duration: 5` or `"5"`: Ray 3.2 takes the unit string, `"5s"` or `"10s"`.
- A 10 second loop, HDR grade, or frame anchor: `"10s"` excludes all three; drop to `"5s"`.
- Ray parameter names on Modify Video: it takes `firstFrame` and `mode`, not `startFrame` and `editStrength`.
- `editStrength` with `autoControls`, or `startFrame` with `keyframes`: each pair is mutually exclusive on Edit.
- Prompting the whole scene on Reframe: the prompt describes only the added canvas; the source subject stays.
- Vibrant, whimsical, or hyper-realistic in a Ray prompt: they degrade quality in this family.
