---
name: scenario-meshy
description: "Use when creating or refining 3D assets with Meshy models on Scenario via MCP: image-to-3D from one photo or 1-4 multi-view angles, text-to-3D, retexturing an existing GLB, remeshing to a target polycount, UV unwrapping, auto-rigging a humanoid character, or applying a library animation clip. Keywords: Meshy 7 and Meshy 6, Ultra mode, Smart Topology, PBR maps, texture prompt, triangle or quad topology, game-ready mesh, A-pose, T-pose, GLB pipeline."
license: MIT
---

# Scenario Meshy 3D

## Overview

Meshy on Scenario is a toolchain rather than one model: image-to-3D generators (Meshy 7 Image to 3D, Meshy 7 Multi Image to 3D, Meshy T2 Smart Topology), Meshy 6 Text-to-3D, and GLB-in, GLB-out utilities (Retexture, Remesh, UV Unwrap, Rigging, Animation). Work runs as a pipeline: generate a mesh, refine it, then rig or animate, each stage its own `model_run` whose `model` parameter takes the 3D asset id the previous stage returned. Discover members with `search` and treat `model_schema_get` as the contract: members disagree on defaults as basic as `enablePbr` (true on Image to 3D, false on Multi Image and Retexture at authoring time).

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic 3D work (viewer, capture, engine import): the `scenario-3d` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Members and their traps (names from the live schema, caps at authoring time):

| Member              | Core input                        | Watch for                                                          |
| ------------------- | --------------------------------- | ------------------------------------------------------------------ |
| 7 Image to 3D       | `image` (1-4)                     | `ultraMode` takes a single image only; raw mesh by default         |
| 7 Multi Image to 3D | `image` (1-4, first = front view) | remeshes in-run; `savePreRemeshedModel` keeps the raw GLB          |
| T2 Smart Topology   | `image` (1-4)                     | animation-ready topology; `targetPolycount` caps at 15,000         |
| 6 Text-to-3D        | `prompt` (600 chars)              | `shouldRemesh` off by default                                      |
| Retexture           | `model` + one style input         | geometry untouched; keep inputs near 30K polys; `enableOriginalUv` |
| Remesh              | `model`                           | `targetPolycount` 100 to 300,000, `resizeHeight`, `originAt`       |
| UV Unwrap           | `model`                           | rejects meshes above 44,000 faces; Remesh down first               |
| Rigging             | `model`, `heightMeters`           | humanoid skeleton and skin weights                                 |
| Animation           | `model`, `actionId`               | auto-rigs, then applies the clip                                   |

One silent rule runs through every texture control: an image beats text. On the generators `textureImage` overrides `texturePrompt` (the text is ignored, not blended), and both need `shouldTexture` on (Text-to-3D has no such toggle: it always textures). Retexture is stricter: exactly one of `textStylePrompt`, `imageStyle`, or `multiviewImage` (1 to 4 views, first is the front). `textureResolution` runs 2k, 4k, or 8k; at 8k the PBR maps come back at 4K with no emission map (Meshy 7 never produces one), and 8k pairs only with triangle topology when remeshing. `poseMode` takes lowercase `"a-pose"` or `"t-pose"`: set one on any character headed for rigging.

## Generate raw, refine on purpose

Keep `shouldRemesh` off on Meshy 7 Image to 3D (the schema recommends it): take the raw mesh at generation, then control polycount with Remesh, which owns `targetPolycount`, topology, `resizeHeight` in meters (0 keeps scale), and origin placement. On the generator, `targetPolycount` does nothing while `shouldRemesh` is off. `ultraMode` buys finer geometry for extra cost but accepts one input image; when hidden sides matter more than micro detail, spend the budget on up to four views instead. Costs spread widely (at authoring time the single-image Meshy 7 p50 ran three times the multi-image one), so `dry_run` before batches.

## Rig or animate, not both

Rigging and Animation are alternatives, not stages. Animation auto-rigs internally, then applies the clip named by `actionId`, a number from Meshy's animation library (ids listed at docs.meshy.ai/en/api/animation-library). Run Rigging alone when you want a rigged GLB for your own clips; go straight to Animation for a moving character, optionally setting `postProcessOperation` to `change_fps` (`postProcessFps` 24, 25, 30, or 60) or `extract_armature`. Both scale the rig from `heightMeters`, so pass the character's real height.

## Worked example: photo to animated character

1. `search` with `target="models"`, `query="meshy"`, `public=true`. Single-image route: `model_meshy-7-img23d` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id, then `upload_asset` the character photo (see the `scenario` skill).
3. `model_run` with `dry_run=true` and `parameters={"image": ["asset_photo"], "poseMode": "t-pose", "texturePrompt": "worn leather armor, muted palette", "enablePbr": true}` for the estimate; then re-run with `wait=false` and `jobs_wait` with the job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
4. `asset_display` the GLB; check silhouette and texture before spending further.
5. `search` for the animation member, `model_schema_get`, then `model_run` with `parameters={"model": "<GLB asset id from step 4>", "heightMeters": 1.8, "actionId": <id from the library>}`.
6. `jobs_wait`, `asset_display`, then `asset_download` for engine import.

## Common mistakes

- `texturePrompt` next to `textureImage` expecting a blend: the image wins, the text is ignored.
- Two style inputs on Retexture: it takes exactly one of prompt, style image, or multi-view images.
- `ultraMode: true` with several images: Ultra requires a single input image.
- UV Unwrap on a dense mesh: above 44,000 faces the job is rejected; Remesh down first.
- Rigging before Animation: Animation rigs by itself, so the chain wastes a job.
- `targetPolycount` on Image to 3D or Text-to-3D with `shouldRemesh` off: it does not apply.
- A bare string where the schema says array: one photo goes as `["asset_x"]`.
