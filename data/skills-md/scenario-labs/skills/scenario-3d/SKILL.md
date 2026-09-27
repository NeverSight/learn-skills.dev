---
name: scenario-3d
description: Use when generating or handling 3D assets through the Scenario MCP server, including text-to-3D or image-to-3D meshes, GPT-6 Astra 3D, GLB, FBX, OBJ, STL, or VOX files, PBR-textured or game-ready models, voxel models, multi-view reconstruction, retexture, remesh, UV unwrap, auto-rigging a biped or quadruped, or retargeting an animation, previewing a mesh in the inline 3D viewer, capturing a viewer screenshot, or downloading a model for import into Unity, Unreal, Godot, or Blender.
license: MIT
---

# Scenario 3D Asset Workflows

## Overview

Scenario runs text-to-3D, image-to-3D, and 3D-to-3D models behind the same MCP generation loop used for images. The most reliable pipeline generates a concept image first, then feeds it to an image-to-3D model; direct text-to-3D exists (`txt23d`) but image-to-3D has the larger catalog and more art direction control. Per-family contracts: `scenario-meshy`, `scenario-rodin`, `scenario-sparc3d`. Walkable scenes and Gaussian splats: `scenario-3d-worlds`. Retexturing a finished mesh or scene with PBR materials: `scenario-patina-retexture`. Connection and the core generation loop: see the `scenario` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step           | Tool                                                                           | Notes                                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Find 3D models | `recommend` with the capability and the user's own words (`search` for a name) | Capabilities: `txt23d`, `img23d`, `3d23d`                                                                                                                                   |
| Inspect inputs | `model_schema_get`                                                             | Always call before `model_run`                                                                                                                                              |
| Generate       | `model_run`                                                                    | Pass reference images as asset IDs                                                                                                                                          |
| Wait           | `jobs_wait`                                                                    | Any `job_id` returned without assets (`in_progress` after a timed-out wait, `queued` or `in-progress` after `wait=false`) goes in `job_ids`; never poll `job_get` in a loop |
| Preview        | `asset_display`                                                                | Interactive GLB/FBX/VOX/OBJ viewer on MCP App hosts                                                                                                                         |
| Download       | `asset_download`                                                               | Returns a URL; save with `curl -L`                                                                                                                                          |

## Worked example: concept image to game-ready mesh

A realistic sequence for "make a 3D treasure chest prop":

1. Generate the concept: pick a text-to-image model via `recommend` with the user's own words as `prompt`, then `model_schema_get` and `model_run` with a prompt describing a single centered subject on a plain background. If the user has a reference, `upload_asset` it (plus `upload_asset_complete` when multipart) and pass that asset ID instead.
2. `recommend` with `capability="img23d"` and the user's own words as `prompt`. Live members include the Hunyuan 3D, Meshy, Tripo, and Trellis families, and Scenario's own GPT-6 Astra 3D, which reconstructs one object from 1 to 8 photos or renders into an editable mesh with named parts and per-part PBR materials. Astra is built for props and hard-surface subjects, not characters, and its schema carries the cost levers a game team asks about first: `buildEffort` and `refineSteps` move the price (both `cost_impact`), and `faceBudget` caps the delivered triangle count at export (10k to 50k for a game-ready asset; the default keeps fine detail and is not that). A refinement pass on a previous output was not exposed at authoring time: an edit is a new run with the corrected references.
3. `model_schema_get` on the chosen model. 3D schemas vary widely: single image vs multi-view arrays, polycount targets, PBR toggles, topology choices.
4. `model_run` with `parameters={"image": "asset_xxx", ...}` and `wait=false` (`dry_run=true` first to price a batch), then `jobs_wait` with `job_ids=["<job_id>"]` (re-call it with the returned `pending_job_ids` as `job_ids` if it times out). A downstream step (rig, retexture) has no payload to `dry_run` until its input mesh exists: quote it from `recommend` as an estimate, then re-price it with `dry_run` on the real asset before launching.
5. `asset_display` with the output `asset_id` to preview, then `asset_download` and `curl -L -o chest.glb "<url>"` for engine import.

Multi-view models accept several images of one subject from different angles; the count and the ordering vary per model, so take both from `model_schema_get` (the first image is usually the front view).

## Texture and lighting controls

Several image-to-3D families split texture from geometry, and each dial is one `model_schema_get` away, so read them before promising a look. Authoring-time examples from the Tripo members:

- `texture: false` returns a bare mesh with no texture and is a `cost_impact` field, the cheap path when the user will texture in a DCC. `textureQuality` (`fast`, `standard`, `detailed`, `extreme`) also moves the price, and a texture version picker, left empty, keeps the provider's default.
- `delight` strips lighting and shadows baked into the reference image so the mesh lights correctly in the user's engine. It defaulted to on; turn it off only when the painted shading is the art style, as on a hand-painted prop. The export stays a lit material either way, so for no engine relighting at all the user sets an unlit shader on import.
- The `pbr` flag's description said PBR on, its default, ignores the texture parameters. A texture setting the user asked for is honored only with `pbr: false` there, so read that description on the chosen member and say which one won.
- Geometry and texture take separate seeds (`seed`, `textureSeed`): hold `seed` and the image fixed and vary `textureSeed` alone for texture variants on one shape.
- `autoSize` scales the output to real-world meters and defaulted to off: set it to `true` for a real-scale engine import, or the mesh keeps its native size. The asset's `dimensions` still read the unit-normalized mesh (longest side 1.0) because the meters sit in the GLB's node scale, so `dimensions` is not proof it failed.

## Inspecting results

`asset_display` renders 3D assets in an interactive viewer (GLB, FBX, VOX, OBJ) on hosts that support MCP Apps; other hosts get the `app_url` dashboard link. The viewer's capture button calls `capture_3d_view`, an app-only tool: it uploads the current camera view as a new image asset and posts the `asset_id` back into the conversation. Use that capture as a reference image for follow-up generations or similarity `search`. Never call `capture_3d_view` yourself; it requires PNG canvas data only the viewer has.

## Refining meshes

3D-to-3D utilities (`3d23d` capability) cover retexturing, remeshing, UV unwrapping, and part segmentation. Find them with `recommend`: `capability="3d23d"` plus the operation in the user's own words. Most take the source `asset_id` in a `kind: "3d"` file field, usually named `model` (also `mesh`, `file3d`); 400 `Input model is required` or `Provide a reference image or a 3D model` means the mesh went in under another name (an image field, or a URL), never that the tool wants something else.

Splitting a finished mesh into parts is a contested lane, so it stays a `recommend` pick: at authoring time several vendors offered mesh segmentation with a granularity control, one combined the split with a PBR retexture, and image-to-parts members build the parts from the picture instead. A convincing mesh is not a game-ready one: part separation, joint placement, materials, and animation are each their own pass, and polygon caps differ by topology on the members that offer both (a quad cap sat well under the triangle cap on one), so read the slider's `max` off the schema instead of promising a count. A named provider feature is a valid `search` target, but an empty result or one member's body-plan enum does not prove a capability is absent platform-wide. For an unmet need such as a hinged prop, use `recommend` with that need and inspect the returned schemas; if none exposes it, report it as unverified in the inspected models, without inventing a call from the provider's own site.

## Rigging and animation

Rigging is a separate `3d23d` step run on a finished mesh, not a flag on the generator. Find the models with `recommend`: `capability="3d23d"` plus the rigging need in the user's own words.

Body plan picks the model. Humanoid models take the mesh and little else (a front-facing hint, or an approximate height, depending on the model) and infer a biped skeleton. Non-biped work goes to a model exposing `rigType`, whose values cover `quadruped`, `hexapod`, `octopod`, `avian`, `serpentine`, and `aquatic`.

Three schema details decide whether the output is usable:

- **Formats.** Rigging models accept GLB, and often OBJ, FBX, or STL. None exposes an output-format field, so the rig comes back as GLB or FBX and most descriptions do not say which: expect a DCC pass when the engine needs the other.
- **Size ceiling.** A `max_size` on the file input is the exception rather than the rule (one humanoid rigging model caps at 30 MB). Check the schema before assuming a large mesh needs decimating.
- **Animation versus rig.** Where a rigger exposes `animation` it retargets a preset clip, and its `allowed_values` are rig-type prefixed (`quadruped:walk`), so read them rather than guess. By default only the retarget file comes back: set `includeRiggedModel` to keep the plain rigged mesh too (the two come back as separate assets with identical `metadata`, so `asset_get` tells them apart: the retarget has `properties.hasAnimations` true and an `animationFrameCount`, the plain rig false and null, and their order is not guaranteed).

When only motion is wanted, motion-transfer video models animate a still character image with no skeleton at all: see `scenario-video`. Video-to-motion models that auto-rig an uploaded mesh are the one place an `outputFormat` enum picks the engine target.

## Common mistakes

- Running `model_run` without `model_schema_get`: 3D model parameters differ far more between models than image models do.
- Passing a local file path as an image input: `upload_asset` first, then pass the returned asset ID.
- Hardcoding model IDs: catalogs rotate (a `deprecated:<replacement_id>` tag names the successor). Re-discover each session, `recommend` for the need or `search` for a name.
- Pasting raw asset URLs into chat instead of calling `asset_display`.
- Forgetting `-L` with curl: download URLs may redirect before serving the file.
- Promising a named skeleton, an influence count, or bones for wings and extra limbs: pick the closest body plan, then finish the rest in a DCC.
- Sending a biped to a `rigType` model: the enum has no biped value, because humanoids have their own rigging models.
