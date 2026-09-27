---
name: scenario-reve
description: "Use when generating or editing images with Reve models on Scenario via MCP: text-to-image from a prompt alone, instruction edits (swap poster text, recolor a product, change materials, relight or restyle a scene), merging references with consistent subjects, blending up to 6 images into one composite, or choosing between Reve v2.1 and Reve Remix. Keywords: Reve v2.1, Reve Remix, Reve AI, txt2img, img2img, frame tags, compositing, style blending, text swap."
license: MIT
---

# Scenario Reve Image

## Overview

Reve, Reve AI's image family on Scenario, splits into two members that share a brand and little else: v2.1 is a reasoning-driven generator and instruction editor (a top-2 text-to-image arena entry at authoring time), Remix a fast, cheap compositor that blends several images into one. Discover them with `search` and treat `model_schema_get` as the contract: they disagree on field names, prompt caps, and ratio lists.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic image work: the `scenario-image` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

At authoring time (the live schema wins):

| Member     | Capabilities     | References                          | Prompt cap | Aspect ratios                            |
| ---------- | ---------------- | ----------------------------------- | ---------- | ---------------------------------------- |
| Reve v2.1  | txt2img, img2img | `references`, optional              | 4000       | 18 values, 4:1 through 1:4, default auto |
| Reve Remix | img2img          | `referenceImages`, required, 1 to 6 | 2560       | 7 values, 16:9 through 9:16, default 3:2 |

Three parameters each: the prompt, the reference array, `aspectRatio`. Neither member has a mask, seed, width and height, negative prompt, or batch-count field, so an edit is scoped by wording and size comes only as a ratio. `auto` (v2.1 only) picks a fitting shape; pass an explicit ratio when the deliverable demands one.

Pick by job. v2.1 covers generation from a prompt alone and precise edits: swap the text on a poster, recolor a product, change a material, relight or restyle, merge references while every subject stays consistent. Remix blends photos, illustrations, or design assets into one cohesive composite. Where either would do, `dry_run` both: at authoring time a v2.1 run cost several times a Remix run and took over a minute at p50 against Remix's twenty-odd seconds.

## Frame tags wire v2.1 references

In a v2.1 prompt, a reference is addressed with a `<frame>N</frame>` tag, numbered from 0 in the order the assets appear in `references`: the first is `<frame>0</frame>`, the second `<frame>1</frame>`. Use the tags whenever more than one reference is in play; without them the model guesses which image you mean. Remix documents no tag syntax: name subjects in plain words ("the bottle from the first image, the lighting from the second").

## Edits are instructions, not masks

Neither member takes a mask, so the prompt carries the whole edit: state what changes and what must stay untouched. v2.1's reasoning rewards specific plain-language instructions over keyword lists, and its 4000-character budget leaves room for constraints. For masked inpainting on an exact region, use a model that exposes a `mask` field (see `scenario-image`).

## Worked example: swapping the text on a poster

1. `search` with `target="models"`, `query="reve"`, `public=true`. At authoring time the hits were `model_reve-v2-1` (generation and instruction edits) and `model_reve-remix` (multi-image blends); re-discover each session.
2. `model_schema_get` on the pick: field names, caps, and the ratio list before anything else.
3. `upload_asset` the poster (see the `scenario` skill) to get an asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "Replace the headline on the poster in <frame>0</frame> with 'SUMMER SALE', matching the original font, perspective, and lighting. Change nothing else.", "references": ["asset_x"], "aspectRatio": "auto"}` for the cost estimate.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` to check the swap, then `asset_download` to save.

## Common mistakes

- Counting frames from 1: `<frame>1</frame>` is the second reference; the first is `<frame>0</frame>`.
- Carrying a field name across members: v2.1 takes `references`, Remix takes `referenceImages`; each schema lists only its own.
- Running Remix without references: `referenceImages` is required (1 to 6 at authoring time); prompt-only generation belongs to v2.1.
- Reusing a v2.1 prompt on Remix without checking length: 4000 characters overflow its 2560 cap.
- Sending width, height, a mask, or a seed: none exists on either member; `aspectRatio` is the only size control.
- Treating a v2.1 `jobs_wait` timeout as an error: p50 latency topped a minute at authoring time; re-call with `pending_job_ids`.
