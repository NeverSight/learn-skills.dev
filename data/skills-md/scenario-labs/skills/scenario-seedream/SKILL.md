---
name: scenario-seedream
description: "Use when generating or editing images with Seedream models on Scenario via MCP: text-to-image, image-to-image editing with reference images, posters or packaging with exact in-image text (non-Latin scripts included), subject-preserving instruction edits, sequence sets of related images in one run, or splitting a finished image into a base plus transparent PNG layers with Layerize. Keywords: Seedream 5.0 Pro, 5.0 Lite, 4.5, Layerize, ByteDance, txt2img, img2img, layer extraction."
license: MIT
---

# Scenario Seedream Images

## Overview

Seedream, ByteDance's image family on Scenario, spans generation, reference-driven editing, and one member that only takes images apart: Layerize splits a finished image into editable layers. The members agree on little else, so discover them with `search` and read `model_schema_get` before every run.

Connection and the core loop: see the `scenario` skill; model-agnostic image work: the `scenario-image` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

At authoring time (fields and caps are per member, read the live schema):

| Member           | References                  | Sizing                                              | Notes                                                       |
| ---------------- | --------------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| 5.0 Pro          | `referenceImages`, up to 10 | exact `width` and `height`, 672 to 3136 px, step 16 | exact in-image text; 3500-char prompt                       |
| 5.0 Lite         | `referenceImages`, up to 14 | `width` and `height`, up to 4K                      | fast and cheap; 2048-char prompt                            |
| 4.5              | `referenceImages`           | `size` (2K, 4K) plus `aspectRatio` enum             | subject-preserving edits; `"auto"` ratio follows the source |
| 5.0 Pro Layerize | one `image`, required       | `size` tier: auto, 1K, 1.5K, 2K                     | splits, never generates; prompt optional                    |

On the three generators, mode follows from the inputs: empty `referenceImages` is text-to-image, one or more is an edit or a multi-reference generation (with several, the prompt gives each reference a role by position), and the array shape holds even for one asset. Sequence mode (`sequentialImageGeneration: "auto"` plus `maxImages`) lets Lite and 4.5 return a related set in one run, input plus generated capped at 15 images; Pro has no sequence fields. Pro also cost two to three times as much per image as Lite or 4.5 and took about two minutes against under one, so iterate on the cheap members and spend Pro on finals; `dry_run` both before a batch (the estimate prices the run exactly as submitted, a whole sequence included). Pro and Layerize carry `optimizePromptMode`: the default `standard` reasons about the prompt first and is slower; `fast` costs the same and is usually enough when a reference already sets the composition (on Layerize it trades some split fidelity for speed).

## Write the exact copy into the prompt

Pro renders legible in-image text, multi-line layouts and non-Latin scripts included. Quote the exact strings in the prompt instead of paraphrasing them, give each a position and a size rank (headline across the top, date line small at the foot), and keep to a few elements at one or two sizes: letters are drawn, not typeset, so paragraphs and many small labels turn to shapes, and copy past that budget (tour dates, credits) is composited in post from the start. Proofread with `asset_display`; a word that garbles is spelled out letter by letter after the quoted string on the rerun, and one that still garbles goes to post. To swap copy on a reference, quote the new string, pin its position, and require the original typeface, size and color with everything else unchanged.

## Layerize: one image in, an editable stack out

Layerize returns a base layer plus up to 16 transparent PNG cutouts, rebuilding the background behind whatever it lifts. The prompt picks the mode: empty runs a full automatic split; an enumerated list of parts ("Separate this poster into transparent layers: headline, product, shadow, background") cuts better than "all layers"; `<bbox>x1 y1 x2 y2</bbox>` on a 0 to 1000 grid, origin top left, confines the split to one region. Set `size` explicitly, since auto inherits the source's tier and the tier moves the price; cost is otherwise flat per run, not per layer. Layers come back cropped to their own bounds with bbox and z-index metadata, not aligned to the source canvas, and there is no PSD export.

## Worked example: a poster, then its layers

1. `search` with `target="models"`, `query="seedream"`, `public=true`. Prefer the newest non-deprecated hit for the job, e.g. `model_bytedance-seedream-5-0-pro` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: sizing fields, caps, defaults.
3. `model_run` with that id, `dry_run=true`, and `parameters={"prompt": "Concert poster, teal and cream, screen-print grain. Headline \"MIDNIGHT ORBIT\" across the top, date line \"Nov 14, Union Hall\" small at the foot.", "width": 1600, "height": 2368}`; both sizing fields move price.
4. Rerun `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
5. `asset_display` and proofread the rendered text.
6. `model_schema_get` on the Layerize hit, then `model_run` with that id and `parameters={"image": "<poster asset id>", "prompt": "Separate this poster into transparent layers: the headline text, the date line, and the background. Clean edges, complete transparency.", "size": "2K"}`.
7. `jobs_wait`, then `asset_display` each layer and `asset_download` the keepers.

## Common mistakes

- Reusing one member's parameter block on another: pixels on Pro and Lite, tier enums on 4.5 and Layerize; pixels sent to an enum field are rejected.
- Passing `referenceImages` to Layerize or `image` to the generators: the input field's name and shape differ per member.
- Expecting Layerize layers to overlay the source directly: each is cropped to its own bounds, so reposition with the returned metadata.
- Asking Pro for a sequence: the sequence fields existed on Lite and 4.5 only.
- Moving a 3000-character prompt from Pro to Lite: prompt caps are per member.
