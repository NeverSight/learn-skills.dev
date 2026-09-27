---
name: scenario-rodin
description: "Use when generating 3D assets with Rodin Hyper3D models on Scenario via MCP: image-to-3D from up to five multiview stills, text-to-3D from a prompt, fast prototyping versus full quality tiers, quad or triangle topology, PBR materials, HighPack 4K textures, T-pose or A-pose characters for rigging, or splitting a finished mesh into parts and retexturing it with Bang!. Keywords: Rodin Gen-2.5, Hyper3D, Deemos, image to 3D, text to 3D, part segmentation, texture delight."
license: MIT
---

# Scenario Rodin 3D

## Overview

Rodin Hyper3D, Deemos Technology's 3D family on Scenario, picks its mode by member: image-to-3D and text-to-3D each ship as a full model and a Fast variant, and Bang! splits finished meshes into parts. Discover them with `search` and treat `model_schema_get` as the contract: the lanes agree on ideas and disagree on parameter names.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic 3D work: the `scenario-3d` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Pick the member by task:

| Task                          | Member                      | Required inputs   |
| ----------------------------- | --------------------------- | ----------------- |
| Image to 3D (`img23d`)        | Gen-2.5, or Fast            | `images`          |
| Text to 3D (`txt23d`)         | Gen-2.5 Text to 3D, or Fast | `prompt`          |
| Split and retexture (`3d23d`) | Bang!                       | `model` + `image` |

`images` is an array even for one still (up to 5 at authoring time), every entry a view of one subject, never an alternative concept. Prompt is optional on the image members: left empty, Rodin writes one from the images. Shared generator knobs: `qualityMeshOption` (topology and poly budget in one enum string, "18K Quad"), `material` (PBR, Shaded, All, None), `textureDelight` (strips baked lighting), `TAPose` (true poses the character in T or A pose for rigging; the schema does not pick between them), `seed` (0 to 65535).

## The lane decides the dialect

Full and Fast express the same ideas through different parameters, so a payload never moves between lanes unchanged. At authoring time the full lane's `tier` ran Gen-2.5-Extreme-Low through Gen-2.5-Extreme-High (Extreme High bills double the base rate), HighPack rode in `addons` as a string (on a Quad mesh it multiplies faces about 16 times), `geometryInstructMode: "creative"` loosened interpretation, `isSymmetric` steered symmetry, and `isMicro` took effect only on Extreme High. The Fast lane's `tier` stopped at Gen-2.5-Minimum, Gen-2.5-Extreme-Low, and Gen-2.5-Low for one fixed price, `highPack` was a boolean, `enableCreativeMode` added generative robustness without losing consistency, and meshes capped at 20K behind an Auto default. In both lanes HighPack means 4K textures plus high-poly geometry at extra cost: `dry_run` the exact payload before any batch. Text members drop the image-only switches (`useOriginalAlpha`, `previewRender`).

## Bang! wants a finished mesh

Bang! is 3D-to-3D: it takes an existing 3D asset as `model` plus a reference `image` (both required at authoring time, `prompt` is optional guidance), splits the mesh into semantically meaningful parts, and regenerates each part's materials in the same pass. `strength` (2 to 12, default 5) sets how fine the split gets, higher splitting into more parts; `material` defaults to PBR here, not All; `resolution` "Basic" is 2K, "High" is 4K. At authoring time it ran several minutes and cost more per asset than a default generator run: `dry_run` it like any other member.

## Worked example: a rig-ready character from turnaround stills

1. `search` with `target="models"`, `query="rodin"`, `public=true`. Match capability to task (`img23d` here, `txt23d` for prompt-only, Fast for cheap drafts), e.g. `model_rodin-hyper3d-v2-5` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: enums, defaults, and caps before anything else.
3. `upload_asset` the turnaround stills (see the `scenario` skill) to get asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"images": ["asset_front", "asset_side", "asset_back"], "prompt": "stylized adventurer, clean silhouette", "tier": "Gen-2.5-Medium", "qualityMeshOption": "18K Quad", "material": "PBR", "textureDelight": true, "TAPose": true}`; re-estimate after any tier or HighPack change.
5. Re-run with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout. Full-lane jobs take minutes; a timeout is not a failure and never justifies a second `model_run`.
6. `asset_display` the mesh, then `asset_download` for engine import (details in the `scenario-3d` skill).

## Common mistakes

- A bare string in `images`: one still goes as `["asset_x"]`.
- Carrying a payload across lanes: `addons: "HighPack"` versus boolean `highPack`, `geometryInstructMode` versus `enableCreativeMode`, disjoint `tier` enums.
- Asking the Fast lane for Medium or High tiers or a 500K mesh: its enums stop at Low and 20K.
- Setting `isMicro` below Extreme High on the full lane: it changes nothing.
- Handing Bang! an image as `model`: `model` is a 3D asset; the `image` guides the regenerated textures.
- Freeform enum strings: values are exact, "Gen-2.5-Medium", "18K Quad", not "medium" or "18k quad".
