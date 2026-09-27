---
name: scenario-luma-image
description: "Use when generating or editing images with Luma Uni-1 models on Scenario via MCP: text-to-image, prompt-based editing of an existing image, style or character reference images with named roles, web search grounding for real-world subjects, rendering exact title text into posters, aspect ratio control, or choosing between Uni-1 Max and Uni-1. Keywords: Luma Labs, Uni-1, Photon, txt2img, img2img, image edit, reference images, webSearch, reasoning image model."
license: MIT
---

# Scenario Luma Image

## Overview

Uni-1, Luma Labs' image family on Scenario, folds generation and editing into one contract: every member is both `txt2img` and `img2img`, and passing a `source` image is what flips the run into edit mode, so where each image lands (source versus reference) decides more than prompt wording. These are reasoning models that plan lighting and composition before rendering, so a run takes a minute or two, not seconds. Discover members with `search` and treat `model_schema_get` as the contract: the tiers share every field name and disagree on caps and price. Luma's video models are the `scenario-luma-video` skill's domain.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic image work (sizing families, masks, batch fields): the `scenario-image` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Mode follows from the inputs (names from the live schema):

| Mode   | Inputs                             | Behavior                                                                            |
| ------ | ---------------------------------- | ----------------------------------------------------------------------------------- |
| Create | `prompt` (+ `imageRef`)            | full scene from the prompt; `aspectRatio` honored, default 3:2                      |
| Edit   | `source` + `prompt` (+ `imageRef`) | prompt states the change; output keeps the source ratio unless `aspectRatio` is set |

`imageRef` is an array of guiding images and combines with `source`. Caps are per member: at authoring time the Max hit took 9 references and the standard 8, with the source occupying one of those slots when editing; both took a 6000 character `prompt`, nine `aspectRatio` values from 1:3 to 3:1, and `outputFormat` png (default) or jpeg. Each reference adds cost, so re-estimate with `dry_run` after changing the count. `webSearch` (default false) has the model fetch real-world visuals before generating: enable it when the prompt names a real place, product, or style the model may not know. No seed, mask, pixel-size, or batch-count field exists: sizing is the ratio alone, masked edits belong to other models, and identical re-runs cannot be pinned, so change one thing per iteration. At authoring time the Max tier cost roughly two and a half times the standard for one 2K image despite near-identical public arena ratings, so `dry_run` the same job on both before a batch.

## References work by role

The model follows a reference reliably only when the prompt says what to take from it: character likeness, style, composition, color palette, lighting, texture, or mood. Unlabeled references get guessed at, and there is no adherence slider; influence rises with prompt specificity ("use the first reference for the exact colorway and stitching"). Roles stack across references, one each. Reusing one canonical reference across iterations is what holds a character steady.

## Create prompts describe, edit prompts preserve

Create prompts read as one scene in natural prose: subject, setting, lighting, mood, style, and always name the lighting, the single biggest quality lever. For text in the image, put the exact string in quotes; rendered text is a family strength, and the Max tier's advertised edge is accurate non-Latin scripts, not Latin text generally. Edit prompts are surgical: state the change first, then pin what must not move ("Change X to Y. Keep Z exactly as it is."). One scene or one change per run.

## Worked example: a travel poster with rendered title text

1. `search` with `target="models"`, `query="luma uni"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_luma-uni-1-max` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: reference cap, ratio list, and defaults before anything else.
3. `upload_asset` the palette reference (see the `scenario` skill) to get its asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "A travel poster of Kyoto in autumn, a pagoda above red maples, warm golden hour light, flat-print texture. Use the reference for color palette and print grain. The title text \"KYOTO\" in bold serif across the top.", "imageRef": ["asset_a"], "aspectRatio": "2:3", "webSearch": true}` (a real place is named, so ground it).
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout. The model reasons before rendering (median latency near 90 seconds at authoring time), so a timeout is not a failure and never justifies a second `model_run`.
6. `asset_display` to check the title spelling and palette, then `asset_download` to save.

## Common mistakes

- A style reference passed as `source`: that flips the run into edit mode and the output hugs the reference. References go in `imageRef`; `source` is only the image being changed.
- Unlabeled references: name each one's role in the prompt or the model guesses which to follow.
- An edit prompt with no preservation clause: whatever is not pinned is fair game.
- Expecting a square by default: create mode defaults to 3:2, so set `aspectRatio` explicitly.
- Hunting for `seed`, `mask`, `width`, or a batch count: none exist at authoring time; read `model_schema_get` instead of assuming.
- Carrying the Max member's reference cap or price to the standard one: they share field names, not numbers.
