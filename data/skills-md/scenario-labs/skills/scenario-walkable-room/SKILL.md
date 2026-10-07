---
name: scenario-walkable-room
description: "Use when one interior photo, uploaded or generated on Scenario, should become a room a visitor walks into in a web browser and plays with: props lifted out of the photo and rebuilt as 3D objects to grab, throw, and hear land, inside a Gaussian splat world, or restyled variants of one room. Keywords: image-blaster, walkable room, photo to 3D room, clean plate, object cut-out, splat world, physics props, grab and throw, impact sounds, heightfield collision."
license: MIT
---

# Scenario Walkable Room

## Overview

One photo of a room becomes a place to walk into and touch: a complete 3D Gaussian splat world (walls behind the camera included) with the room's small objects rebuilt as real 3D models a visitor can pick up, throw, and hear land. Restyle the photo first and the same room comes in several looks. The route follows the open-source [image-blaster](https://github.com/neilsonnn/image-blaster) pipeline, with every generation on Scenario through MCP:

1. **Uncover**: describe the photo literally and list its single movable objects with a box, the surface each stands on, a size estimate, and materials. Pick two or three per room.
2. **Plate**: one removal-only image edit that erases those objects and nothing else.
3. **Cut-outs**: one image edit per object on the original photo, drawing it alone on white.
4. **World**: a single-image world model on the plate.
5. **Objects**: image-to-3D on each cut-out, with PBR textures.
6. **Sounds**: a few short impact one-shots per object.
7. **Assembly**: level and scale the world from its own splats, fit the lens it assumed, derive a collision heightfield, put each object back where the photo had it, and show it all with a streaming splat renderer and a physics engine.

Steps 1 and 7 are the agent's own work on downloaded files; every generation in between is an MCP call. Connection, uploads, and the core loop: see the `scenario` skill. Edits: `scenario-image` or `scenario-gemini-image`. Worlds: `scenario-3d-worlds`. 3D models: `scenario-3d`. Sound: `scenario-audio` or `scenario-sonilo`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Discover each paid stage's member with `recommend`, passing the capability and the user's own words, and read `next_step` before taking a pick, per the `scenario` skill. `recommend` has no capability for worlds, so find the single-image world member with `search` as `scenario-3d-worlds` teaches. Never assert a generative model's id as a constant. Read every pick's `model_schema_get` and price the exact payload with `model_run` `dry_run=true` before running it.

| Step      | Discovery                     | What to send and check                                                                                                                                          |
| --------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Uncover   | none, read the photo yourself | Single movable items only, with a normalized box, support, size in meters, materials ([references/objects.md](references/objects.md))                           |
| Plate     | `img2img`, takes a reference  | `remove the following from the image: ...` and nothing else; compare with the photo for over-removal and recoloring                                             |
| Cut-out   | `img2img`, same member        | One edit per object on the original photo, square, about 1K, white background ([references/objects.md](references/objects.md))                                  |
| World     | `search`, single-image world  | The plate, full-resolution splats, a fixed `seed`, a prompt describing the room without the objects                                                             |
| Object    | `img23d` with PBR             | One cut-out per job, PBR on, a moderate face count (about 50,000); pick the GLB by its type (`asset_get` `mimeType` `model/gltf-binary`), never by output order |
| Sound     | `txt2audio`, sound effects    | One clip of about 6 s per object holding several impacts separated by silence                                                                                   |
| Calibrate | none, local                   | Floor, level, scale, lens, heightfield, placement ([references/calibration.md](references/calibration.md))                                                      |
| Viewer    | none, local                   | Paged splat streaming, heightfield walker, convex-hull props, grab and throw, panned sounds ([references/viewer.md](references/viewer.md))                      |

Launch every batch with `wait=false`, then `jobs_wait` on the ids, re-called with `pending_job_ids` on timeout. A world takes several minutes; a timeout is not a failure and never justifies a second `model_run`.

## Worked example: the user's living room, walkable, with things to throw

1. **Photo.** `upload_asset` the user's photo (per the `scenario` skill: `file_size`, PUT the parts, `upload_asset_complete`) and reuse the asset id. With no photo, `recommend` with `capability="txt2img"` for a photoreal interior: a doorway view at about chest height, level and centered, wide lens, a few small objects on tables and the sofa. For several looks, edit that photo once per style, opening the prompt with the fixed architecture (windows, door, floor plan, camera, lens) before the new finishes, furniture, and light.
2. **Filing.** Create the run's collection before the first generation (`collection_create` through the catalog write lane, arguments under `parameters`), then `collection_add_assets` each keeper as it lands.
3. **Uncover.** `asset_display` each photo, describe it literally, and write the object list. Choose two or three objects per room: separate, unoccluded, one or two materials, standing on the floor, a table, or a seat.
4. **Plate.** `recommend` with `capability="img2img"` and "remove objects from a room photo, keep everything else", `model_schema_get` for the reference-image field, `dry_run`, then run with the photo as the reference:

   > remove the following from the image: the {object} on the {support}, {where}; the {object} {where}

   `asset_display` the plate next to the photo. Removal edits sometimes recolor an object instead of erasing it, or take its neighbors too (every cushion on a bench, a carved screen beside a lamp): re-run with a narrower list, or drop that object.

5. **Cut-outs.** One edit per object on the original photo, never the plate, with the isolation prompt in [references/objects.md](references/objects.md). Name anything resting on the object so it stays out.
6. **World.** Find the single-image world member per `scenario-3d-worlds`, `model_schema_get`, `dry_run`, then run each plate with `wait=false`, full-resolution splats, one fixed `seed` for every room, and a prompt describing the room as it is without the removed objects. Collect the ids with `jobs_wait` (re-called with `pending_job_ids`; a world takes several minutes), then `asset_download` each `.spz`.
7. **Objects.** `recommend` with `capability="img23d"` and "textured PBR prop from a product cut-out", read the face-count, texture, and PBR fields off `model_schema_get`, `dry_run`, then one job per cut-out with `wait=false` and `jobs_wait` on the ids. Each job returns several assets (the mesh with its textures and previews): take the one whose `asset_get` `mimeType` is `model/gltf-binary`, inspect it in the viewer (`scenario-3d`), then `asset_download` it.
8. **Sounds.** `recommend` with `capability="txt2audio"` and "short impact sound effects", then one clip per object:

   > Four separate one-shot impacts, each followed by a full second of silence: {the object, its material} {knocked over / dropped} onto {the room's floor}, {the character of the sound}. Close-miked, dry room, no music, no voices.

9. **Assemble.** Calibrate each world and place its objects per [references/calibration.md](references/calibration.md), then build the page per [references/viewer.md](references/viewer.md). Simplify the GLBs for the web (about 15,000 to 20,000 triangles, 1K WebP textures, Meshopt) and load physics after the room is on screen.

## Common mistakes

- Treating the world as metric: it is not. Measure the camera's height above the fitted floor and compare the objects' projected heights with their estimated sizes; at authoring time that put the photo camera about 1 m above the floor in every room.
- Assuming every world shares the photo's lens: restyles of one photo came back with fields of view from about 50 to 76 degrees from the same world model. Fit the lens per world before projecting boxes.
- Cutting out from the plate: the object is no longer there. Cut-outs come from the original photo.
- Uncovering plants, glass, or objects holding other objects: image-to-3D closes foliage into a solid shell with leaves painted on. Skip them, or name and remove what they hold.
- Placing objects from the base of the box on the floor plane alone: objects on tables or seats float or sink. The surface right behind the bottom of the box is where each one stood.
- Dropping props into physics on page load: noisy supports send them tumbling. Start rigid props asleep where the photo had them; let only soft ones (cushions) settle.
- Playing a sound on every contact force: a resting object reports its own weight every step. Sound only when the object was moving into the contact.
- Trusting PBR metalness from image-to-3D: lacquer and glaze come back as metal and render as chrome. Keep metalness only on real metal.
- Changing the payload after a 3D job reports `failure` with a result-download error: that is a platform error, not a bad input. Confirm with `job_get` that the job's status is `failure` and it has no assets (and that no later job for the same input succeeded, via `jobs_list`) before retrying once with the same payload; a `jobs_wait` timeout is not a failure and never justifies a second run.
- Running heavy local jobs in parallel (calibration, mesh conversion, splat level-of-detail builds): run them one or two at a time.
