---
name: scenario-textures
description: "Use when a task involves game textures or materials through the Scenario MCP: seamless or tileable textures, themed texture packs (brick, wood, stone, floors, hand-painted), PBR materials (albedo, metallic, roughness, normal) on 3D assets, retexturing a mesh, material iteration from reference images, texture upscaling that must preserve tiling, or sizing textures for game engines. Keywords: seamless texture, tileable, PBR, material, retexture, texture upscale, surface."
license: MIT
---

# Scenario texture and material workflows

## Overview

Scenario generates seamless, tileable textures from text or reference images, upscales them without breaking the tile, and applies PBR materials when texturing 3D meshes. Model availability differs per team and evolves, so always discover models at run time instead of hardcoding IDs: `recommend` with the need in the user's own words for a capability, `search` for a member known by name.

Connection and the core generation loop: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step                | Tool                                              | Notes                                                                                                                                                           |
| ------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Find texture models | `recommend` with the need in the user's own words | `capability` is `txt2img` or `img2img` with the texture in `prompt` (the catalog tags texture models `txt2img_texture`, `img2img_texture`); `search` for a name |
| Inspect inputs      | `model_schema_get`                                | Always call before `model_run`                                                                                                                                  |
| Generate            | `model_run`                                       | `dry_run=true` prices a batch first                                                                                                                             |
| Wait                | `jobs_wait`                                       | Re-call with `pending_job_ids`                                                                                                                                  |
| View and save       | `asset_display`, then `asset_download`            | Download for engine import                                                                                                                                      |
| Upscale             | `model_run` on a texture upscaler                 | 2x to 8x, tiling preserved                                                                                                                                      |

## What live search confirmed at authoring time (examples to re-discover, not constants)

- Seamless generation: `model_scenario-texture` (Scenario Texture) takes a prompt (a tileable hint is appended automatically), `width`/`height` from 16 to 3840 in multiples of 16, `quality`, `seed`, up to 10 `referenceImages` for style, and `eraseSeam` (off by default) with `overlap`/`featherRadius` to inpaint away both seam axes.
- Themed texture LoRAs (Flux.1 LoRA, tag `sc:texture`): floors, marble, concrete, stone walls, wood boards, brick, terracotta, hand-painted, cybernetic, realistic textures. They expose dedicated texture capabilities (`txt2img_texture`, `img2img_texture`, `controlnet_texture`).
- Tiling-safe upscaling: `model_sc-upscale-flux-texture` (Scenario Texture Upscale), `upscaleFactor` 2 (the minimum) to 8, presets `precise`/`balanced`/`creative` riding the same `strength` and controlnet sliders the schema exposes. It re-renders, so expect small tonal drift: `precise` with low strength minimizes it, and the result is compared against the source before shipping.
- Material-look conversion: `model_sc-texture-converter` (Texture Converter) turns a flat image into a surface material using `raised`, `shiny`, `polished`, `angular` sliders and an `invert` relief toggle.
- PBR maps come from two different routes. For a flat texture, 2D map extractors (`recommend`, `capability="img2img"`, with the user's words about extracting maps from a flat texture; `search` only for one already known by name) return a full set in one img2img call: `model_patina` (PATINA Image to Maps) outputs base color, normal, roughness, metalness, and height, each as its own image asset whose `metadata.type` names it (`texture-albedo`, `texture-normal`, `texture-smoothness`, `texture-metallic`, `texture-height`) in the order requested; the roughness request comes back labeled smoothness, so confirm the convention before wiring it. `model_patina-material` tiles a PBR material straight from a prompt. For a mesh, 3D texturing and image-to-3D models emit the maps instead (Tripo 3.0 Texturing, Tencent Texture Edit, Meshy 7 Retexture); enable the PBR toggle found via `model_schema_get`. Retexturing a full mesh is a 3D-to-3D pipeline: see `scenario-3d`, and `scenario-meshy` for the Meshy retexture contract.

## Worked example: seamless brick, iterated then upscaled

1. `recommend` with the user's own words as `prompt` ("seamless tileable weathered brick"), pick the seamless generator (e.g. `model_scenario-texture`).
2. `model_schema_get` `model_id="model_scenario-texture"`.
3. `model_run` with `parameters={"prompt": "weathered red brick wall, moss in the mortar joints", "width": 1024, "height": 1024, "eraseSeam": true, "seed": 42}`. For a themed pack, price the batch with `dry_run=true` first, then launch the runs with `wait=false`.
4. `jobs_wait` with `job_ids=["job_..."]` (the ids returned by `model_run`). A ~180s timeout is not an error: re-call with the returned `pending_job_ids` as `job_ids`, never a second `model_run`. Then `asset_display` the output asset.
5. Iterate: rerun with the same `seed` and an edited prompt, or add `referenceImages=["asset_..."]` to lock a style.
6. Upscale: `recommend` with `capability="img2img"` and the user's own words as `prompt` ("upscale this texture without breaking the tile"), hold the pick to tiling preservation (a generic upscaler breaks the repeat), `model_schema_get` it, then `model_run` with the image and the factor and preset fields the schema names (at authoring time the texture upscaler took `upscaleFactor: 2` and `preset: "precise"`), raising the factor only deliberately: cost follows output pixels, and this leg can only be `dry_run`-priced once its input asset exists, so a two-step chain is never priced up front.
7. Verify tiling at no cost: the saved PNG's left column against its right and top row against bottom should differ no more than neighboring interior columns do, and a 2x2 self-tile proof sheet shows any seam instantly.
8. `asset_download` the final asset for engine import.

## Common mistakes

- Skipping `model_schema_get`: parameter names differ per model and most models reject an empty payload.
- Using a generic upscaler on a tileable texture: it breaks the repeat at the seams. Use the texture-specific upscaler, which preserves tiling.
- Generating huge sizes directly: generate near 1024, then upscale 2x to 8x. Generation dimensions cap at 3840.
- Routing a flat texture through a 3D texturing model just to get PBR maps: the 2D map extractors do that in one img2img call, and the 3D models are for meshes.
- Ignoring engine sizing: engines expect square power-of-two textures (the seamless generator defaults to 1024x1024, 1:1). The generator accepts any multiple of 16, so choose 1024 or 2048 deliberately.
- Hardcoding model IDs: availability differs per team. Re-discover each session.
