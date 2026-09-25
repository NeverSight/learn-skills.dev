---
name: scenario-gemini-image
description: "Use when generating or editing images with Google's Gemini image models (Nano Banana) on Scenario via MCP: text-to-image, natural-language instruction editing, identity locking or style transfer from reference images, multi-image fusion, pulling stills from a video clip, Google Search grounding, thinking level tuning, 512 to 4K output, or choosing between Flash, Pro, and Lite. Keywords: Gemini 3.1 Flash, Gemini 3.0 Pro, Gemini 3.1 Lite, Nano Banana 2, Nano Banana Pro, txt2img, img2img."
license: MIT
---

# Scenario Gemini Image

## Overview

Gemini, Google's image family on Scenario (the Nano Banana line), generates and edits through one required `prompt`: edits are instructions against the references, never mask painting. Discover members with `search` and treat `model_schema_get` as the contract: the creative fields are shared and nearly everything else is per member.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic image work: the `scenario-image` skill. Gemini video belongs to the `scenario-gemini-omni` skill; Gemini speech models are the audio domain. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Three members at authoring time (per-member facts move, so read the schema):

| Member    | Resolution                  | Sets it apart                                                |
| --------- | --------------------------- | ------------------------------------------------------------ |
| 3.1 Flash | `512` to `4K`, default `1K` | video input, four `thinkingLevel` steps, Search grounding    |
| 3.0 Pro   | `1K` to `4K`, default `2K`  | built for complex instruction edits and multi-image fusion   |
| 3.1 Lite  | fixed 1K, no `resolution`   | fastest and cheapest; `thinkingLevel` is `MINIMAL` or `HIGH` |

Shared fields: `referenceImages` (up to 14, an array even for one), `numOutputs` (1 to 4 variations of one prompt), `aspectRatio` (`21:9` through `9:16` plus the default `auto`; pin the ratio when a placement demands one), and a prompt cap near 250000 characters, so a full brief fits verbatim. Flash alone takes `video` (one clip, about 15 MB, sampled at `videoFps`, default 1 fps) to pull stills from footage; `video` and `referenceImages` are mutually exclusive. `useGoogleSearch` (Flash and Pro) grounds the run in live web context and moves the price, like every field marked `cost_impact`. No mask, seed, or negative-prompt field exists: regional edits are sentences, and reruns give variations, not reproductions.

## Write instructions, not tags

Describe subject, setting, and style in plain sentences. For edits, state the change and what must survive it: "keep the shoe's shape, colors, and branding unchanged; place it on a sunlit deck". With several references, assign roles by position ("image 1 is the character's face, image 2 the outfit, image 3 the background style"); unassigned references blur together. Lock identity explicitly: say the features must be preserved while pose, lighting, or scene changes. Quote in-image copy exactly and say where each block sits ("the title reads 'LUMEN', top third"); unquoted wording is treated as a theme to depict, not copy to render. When one word keeps mangling, do not rerun the design: pass the keeper in `referenceImages` and spell the word letter by letter ("the title reads 'LUMEN', spelled L, U, M, E, N"), changing nothing else. On Flash and Lite, `thinkingLevel` defaults to `HIGH`, the careful setting; drop to `MINIMAL` for speed on simple runs.

## Price the member before the batch

The cost cliff sits between members more than between resolutions: at authoring time the same 1K edit cost about double on Flash what Lite charged, Pro's 2K default roughly doubled it again, and Lite returned in under half the time. `dry_run=true` the same parameters on two members before any batch, and re-estimate whenever `resolution`, `numOutputs`, references, or `useGoogleSearch` change.

## Worked example: product restyle with locked identity

1. `search` with `target="models"`, `query="gemini"`, `public=true`. Video and speech members surface too; pick an image member, e.g. `model_google-gemini-3-1-flash` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: fields, caps, and defaults.
3. `upload_asset` the product photo and the style reference (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "Image 1 is the product: keep its shape, label, and colors exactly. Image 2 sets the mood: warm sunset palette, soft shadows. Place the product on a marble counter in natural window light.", "referenceImages": ["asset_a", "asset_b"], "aspectRatio": "4:5", "resolution": "2K", "numOutputs": 2}` for the cost estimate.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` to review both variations, `asset_download` to save the pick.

## Common mistakes

- Passing `video` and `referenceImages` together on Flash: they are mutually exclusive.
- Reaching for `seed` or `mask`: neither exists on any member; describe the edit and batch `numOutputs` to pick from.
- Carrying fields across members: `resolution` fails on Lite, `thinkingLevel` on Pro, `video` everywhere but Flash.
- Keyword-tag prompts: comma lists underperform; write the sentence you would give a designer.
- Several references with no roles: outputs blend them; say which image is which by position.
- Enabling `useGoogleSearch` for stylistic work: it raises cost and earns it only on factual, real-world subjects.
