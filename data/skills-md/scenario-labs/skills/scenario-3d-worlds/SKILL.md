---
name: scenario-3d-worlds
description: "Use when generating navigable 3D worlds or Gaussian splat scenes on Scenario via MCP: text-to-world, image-to-world, a 360 panorama or skybox turned into a walkable splat, multi-view photos or a video walkthrough reconstructed as a splat, or one object photo to splat. Keywords: World Labs Marble 1.1, 1.1 Plus, 1.0 Draft, Hunyuan World, HY World, image-to-skybox, skybox-to-splat, multiview-to-splat, TripoSplat, gaussian splatting, 3DGS, spz, world generation, explorable scene, VR."
license: MIT
---

# Scenario 3D Worlds

## Overview

These models build explorable environments as 3D Gaussian splats, not polygon meshes: volumetric scenes to walk through and render in real time, with no UVs or topology to edit (Marble splats also export to triangle or collider mesh). Three vendors sit side by side: World Labs Marble in three quality tiers, Hunyuan's HY World pipeline, and TripoSplat for single objects. Discover them with `search` and treat `model_schema_get` as the contract; HY World members carried a geo restriction tag at authoring time, so hits differ by team and region.

Connection and the core loop: see the `scenario` skill; polygon meshes, rigging, and the 3D viewer: the `scenario-3d` skill; skybox-only work with no splat stage: the `scenario-skyboxes` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Pick the member by what you already have (input names from the live schemas):

| You have                   | Member                                   | Inputs                                     |
| -------------------------- | ---------------------------------------- | ------------------------------------------ |
| A text idea                | Marble, any tier                         | `prompt` alone                             |
| One image, flat or 360     | Marble                                   | `images`, one entry; `isPano: true` if 360 |
| 2 to 8 photos of one scene | Marble                                   | `images`                                   |
| A walkthrough video        | Marble or HY Multi-view to Splat         | `video`                                    |
| Many overlapping photos    | HY Multi-view to Splat                   | `images`, 2 to 64 at authoring time        |
| One photo of a place       | HY Image to Skybox, then Skybox to Splat | `image`, then `panorama`                   |
| One photo of an object     | TripoSplat                               | `image`; background removal is automatic   |

`images` and `video` are mutually exclusive wherever both exist; `isPano` applies only when exactly one image is passed. TripoSplat wants one clean object and every other member wants a scene: aiming either at the other's subject is the main failure mode.

## Draft on Marble, then upgrade

The three Marble tiers (1.0 Draft, 1.1, 1.1 Plus) take identical inputs, and the same inputs with the same `seed` reproduce the same world on every tier. Iterate on Draft, which returned in about a minute at authoring time, then rerun the identical parameters on 1.1 (balanced) or 1.1 Plus (highest fidelity, dynamically grows larger worlds when the scene allows). The cost spread across tiers was more than tenfold at authoring time, so `dry_run` before committing. `splatResolution` picks the stored density (`100k`, `500k`, `full`); `disableRecaption: true` stops Marble rewriting your prompt.

## The HY World pipeline runs long

Image to Skybox is an image model, not a 3D one: it expands one photo of a place into a 2:1 equirectangular panorama (`backend` trades `full` fidelity against `qwen` speed and cost). Its output asset id goes to Skybox to Splat as `panorama`. There, the three trajectory toggles (`applyNavTraj`, `applyUpRoute`, `applyReconIteration`, default true) drive cost and time; `maxSteps` sharpens marginally and materially moves neither. The splat stage ran close to an hour at median at authoring time: keep re-calling `jobs_wait` with `pending_job_ids`; a timeout is not a failure and never justifies a second `model_run`. Multi-view to Splat is the opposite, fast and cheap: best when the camera moved through a static scene with parallax.

## Worked example: graybox a level from a concept image

1. `search` with `target="models"`, `query="marble world"`, `public=true`. Tiers appear side by side, e.g. `model_worldlabs-marble-1-0-draft` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with the Draft id: fields, caps, and defaults before anything else.
3. `upload_asset` the concept image (see the `scenario` skill) for an asset id.
4. `model_run` with `dry_run=true` and `parameters={"images": ["asset_x"], "prompt": "abandoned observatory interior, dusk light through the dome slit", "seed": 1234, "splatResolution": "full"}`; repeat the dry run on the 1.1 id to see the upgrade cost.
5. `model_run` on Draft with `wait=false`, then `jobs_wait` with the job id, re-called with `pending_job_ids` on timeout.
6. `asset_display` the splat and walk it; adjust and repeat on Draft until the layout is right.
7. Rerun the identical parameters, same `seed`, on the 1.1 or 1.1 Plus id from step 1, then `asset_download` the final `.spz`.

## Common mistakes

- Passing `images` and `video` together: mutually exclusive on Marble and Multi-view to Splat.
- A single equirectangular input without `isPano: true`: Marble reads it as a flat photo.
- Changing or omitting `seed` between the draft and the upgrade tier: a different world comes back.
- Feeding TripoSplat a scene, or a world model a lone object.
- Treating a `jobs_wait` timeout on Skybox to Splat as a failure: the job is still running.
- Adjusting `maxSteps` to buy quality or cut cost: the trajectory toggles move cost, `maxSteps` barely moves sharpness.
- Expecting UVs or editable topology from a splat: for polygon assets, use the mesh generators in `scenario-3d`.
