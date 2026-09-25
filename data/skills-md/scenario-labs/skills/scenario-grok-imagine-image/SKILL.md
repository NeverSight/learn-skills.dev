---
name: scenario-grok-imagine-image
description: "Use when generating or editing images with Grok Imagine models on Scenario via MCP: text-to-image, instruction editing with up to three reference images, posters, packaging, ads, or infographics with exact in-image text, photoreal shots from camera and lighting cues, extended aspect ratios up to 20:9 and 9:20, quality and resolution tiers, or batches of variations. Keywords: Grok Imagine Image 2.0, Image Quality, xAI, Aurora, Grok, txt2img, img2img, typography, 2K."
license: MIT
---

# Scenario Grok Imagine Images

## Overview

Grok Imagine, xAI's image family on Scenario, puts generation and editing in every member: the same model reads an empty `referenceImages` as text-to-image and a filled one as an edit, so the inputs pick the mode and the member picks the tier. Members ship side by side, agreeing on the prompt contract and disagreeing on knobs and price, so discover them with `search` and treat `model_schema_get` as the contract. The Grok Imagine video members belong to the `scenario-grok-imagine-video` skill.

Connection and the core loop: see the `scenario` skill; model-agnostic image work: the `scenario-image` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

At authoring time (caps are per member, read the live schema):

| Member  | Aspect ratios                               | Notes                                                  |
| ------- | ------------------------------------------- | ------------------------------------------------------ |
| 2.0     | 14 values up to 20:9 and 9:20, default auto | adds `quality` (low, medium); strongest text and edits |
| Quality | same 14, default 1:1                        | fast at 2k; price near flat across variants            |
| Image   | 10 values, 2:1 through 1:2                  | cheapest per image                                     |

The rest is shared: `prompt` up to 10000 characters, `referenceImages` capped at 3, `numOutputs` 1 to 10, `resolution` at 1k or 2k. No seed, mask, negative prompt, or pixel sizing exists anywhere in the family: size is ratio times resolution tier, and `aspectRatio` decides what is in frame, not just the crop. In editing mode `aspectRatio` is ignored entirely and the output follows the source's proportions. The price spread is why the older members stay live: one image on the unversioned member cost a fraction of a versioned run at authoring time, and 2.0's 2k text-to-image ran well over a minute where the others took seconds. So iterate cheap and fast (the unversioned member, or 2.0 at `quality: "low"` and 1k), spend a medium 2k run on keepers, and `dry_run` two members on the same job before a batch: `numOutputs`, `quality`, `resolution`, and references all move price.

## Write the copy, not a vibe

The family's edge is legible in-image text: posters, packaging, infographics, memes. It only pays when the prompt carries the copy verbatim: wrap every literal string in quotes, give each a role ("the title reads ...", "a line beneath reads ..."), keep strings short, and close with "no other text", or the model invents extra labels. Real numbers and statistics go in as quoted copy too, since invented figures look plausible. Render small type at 2k and proofread in `asset_display` before building on the result. For the rest, write a short natural-language brief, subject, setting, composition, light, finish, in 30 to 80 words: quality adjectives ("8K", "masterpiece") are ignored and negatives mostly too, so state positives ("clean empty background", not "no clutter") and keep one aesthetic per prompt.

## Edits are instructions, no mask exists

Editing is prompt-driven: pass up to three `referenceImages` and describe the change. Two habits keep it surgical: describe only what changes and name what stays ("keep the pose, background, and lighting unchanged"), and chain one edit per run instead of stacking several. With more than one reference, state each image's role (subject, style, scene) so the blend lands where intended. The output inherits the source's proportions, so reframe before the edit, never with `aspectRatio`.

## Worked example: a branded label onto a product photo

1. `search` with `target="models"`, `query="grok imagine image"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_xai-grok-imagine-image-2-0` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: the reference cap, `quality` and `resolution` values, and the ratio list before anything else.
3. `upload_asset` the product photo (see the `scenario` skill) to get its asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "Add a minimalist front label to the bottle where the title reads \"LUMEN\" in a clean white serif and a smaller line beneath reads \"Sparkling Citrus Soda\". Keep the bottle shape, glass tint, background, shadows, and lighting unchanged, no other text.", "referenceImages": ["asset_abc"], "quality": "medium", "resolution": "2k"}`; re-estimate after any change to `quality`, `resolution`, `numOutputs`, or references.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` and proofread the label at full size, then `asset_download` the keeper.

## Common mistakes

- Setting `aspectRatio` on an edit: it is ignored and the output keeps the source's proportions; reframe the source first.
- Describing copy loosely ("a catchy tagline"): text comes back garbled or invented; quote exact strings and end with "no other text".
- Negative prompts: largely ignored; state the positive instead.
- A bare string where the schema says array: one reference still goes as `["asset_x"]`.
- Carrying `quality` beyond 2.0: at authoring time no other member had the field; check the live schema before reusing parameters across members.
- Fine print at 1k: small type blurs; render text-heavy finals at 2k.
