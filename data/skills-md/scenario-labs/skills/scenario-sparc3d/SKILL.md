---
name: scenario-sparc3d
description: "Use when turning images or photos into 3D meshes with Sparc3D models on Scenario via MCP: single-image or multi-view image-to-3D, watertight meshes for game assets, AR/VR, or 3D printing, mesh-only versus PBR-textured output, face count targets, resolution tiers, or reconstructing human heads and busts with the Portrait variants. Keywords: Sparc3D 2.1 and 2.0, Hitem3D, image to 3D, img23d, multiview, watertight, PBR, GLB, OBJ, STL, FBX."
license: MIT
---

# Scenario Sparc3D Image-to-3D

## Overview

Sparc3D, Hitem3D's image-to-3D family on Scenario, turns one to four photos into a watertight mesh with no text prompt: the source images are the entire art direction. A base line handles props and objects, a Portrait line human heads and busts, each in 2.1 and 2.0 generations. Discover them with `search` and treat `model_schema_get` as the contract: members disagree on which knobs exist and how values are spelled.

Connection and the core loop: the `scenario` skill in this repo; model-agnostic 3D work: the `scenario-3d` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Names from the live schema; differences as of authoring time:

| Parameter     | Role                                        | Differences across members                                                                                            |
| ------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `images`      | 1 to 4 views: front, then back, left, right | same                                                                                                                  |
| `requestType` | numeric: mesh only or mesh plus texture     | same                                                                                                                  |
| `resolution`  | detail and topology tier                    | `1536fast`/`1536pro` on 2.1, `1536profast`/`1536pro` on 2.1 Portrait, `1536`/`1536pro` on 2.0; absent on 2.0 Portrait |
| `face`        | target face count, 100K to 2M, default 2M   | absent on 2.0                                                                                                         |
| `pbr`         | PBR material, default true                  | inert without texture output                                                                                          |

At authoring time `requestType` 1 meant bare mesh, 3 (the default) textured. Resolution defaults differ: 2.1 opens on its fast tier, 2.1 Portrait on pro.

## Views are positional

In `images`, slot one is the front view; extras are back, left, and right, in that order, all of one subject. A front view alone works; extra views buy stabler geometry on unseen sides. One centered subject on a plain background converts best.

## Long jobs, moving prices

`resolution` buys generation detail; `face` sets delivered mesh weight (500K for lightweight assets, 2M for high fidelity). `requestType`, `resolution`, and `pbr` all move cost, spanning four times on one member at authoring time, so `dry_run` the exact parameter set before a batch. Runtimes are long (medians near 17 to 21 minutes at authoring time, a slow quartile reaching past 30), so `jobs_wait` timeouts are normal: re-call with `pending_job_ids`, never a second `model_run`, never `job_get` polling.

## Worked example: a game prop from one concept image

1. `search` with `target="models"`, `query="sparc3d"`, `public=true`. Prefer the newest non-deprecated base hit, e.g. `model_hitem-sparc-3d-2-1` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: knob presence and `resolution` spelling come only from here.
3. `upload_asset` the concept image, or generate one first with a text-to-image model.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"images": ["asset_front"], "requestType": 3, "resolution": "1536fast", "face": 500000, "pbr": true}` for the cost estimate; re-estimate after touching any cost knob.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout; expect several rounds.
6. `asset_display` to preview the mesh, then `asset_download` for engine import. No schema field selects the container (the catalog advertises GLB, OBJ, STL, and FBX): confirm the delivered format from the returned asset before promising an engine target.

## Common mistakes

- Passing a `prompt`: no member takes text; direction lives in the source images.
- A bare string for `images`: one view still goes as `["asset_x"]`.
- A side view in slot one: it is read as the front.
- Carrying knobs across members: the non-pro tier is spelled three ways, `face` is missing on 2.0, `resolution` on 2.0 Portrait.
- Expecting `pbr` to texture a mesh-only run: it acts only when `requestType` asks for texture.
- Sending a creature or prop to Portrait: a head and face specialist, not a higher-quality tier.
