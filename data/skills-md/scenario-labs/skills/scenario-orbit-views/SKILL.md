---
name: scenario-orbit-views
description: "Use when a single image of a character, creature, prop, vehicle, or building must be seen from new camera angles through the Scenario MCP server: turnarounds, a 360 orbit, views from behind, above, below, or straight down, consistent multi-angle renders on the same grounded background or on transparency, or novel views that go through a 3D intermediary instead of guessing."
license: MIT
---

# Scenario Orbit Views

## Overview

Asking an image model to "show it from behind" guesses the geometry, and each angle drifts in size, pose, and ground contact. The reliable route puts a 3D step in the middle: rebuild the subject as an untextured mesh, render a gray clay layout for every camera, then let a reference-capable image model repaint each layout from the original picture. The mesh fixes silhouette, scale, and perspective; the picture supplies identity, colors, and finish. Connection and the core generation loop: see the `scenario` skill. Image-to-3D model choice: `scenario-3d`. The background panorama: `scenario-skyboxes`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

The Blender steps run locally in a shell with Blender 4.x or later; everything that generates goes through MCP tools. Check for Blender before the first paid step (on macOS it is usually `/Applications/Blender.app/Contents/MacOS/Blender`, not on the PATH). When it is missing, ask the user to install it, or unattended, stop and report it: no MCP tool renders a mesh from chosen cameras.

## Quick reference

| Step           | How                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source picture | One subject, whole body with margin, plain background, a known camera (slightly above eye level, turned about 30 degrees)                            |
| Mesh           | `recommend` an image-to-3D model, geometry only (texture is not needed), `asset_download` the GLB                                                    |
| World          | A skybox panorama in the same art style, flat open floor all around the viewpoint                                                                    |
| Camera zero    | [render_grounded.py](scripts/render_grounded.py) `--search`, then [match_view.py](scripts/match_view.py), confirmed by eye                           |
| Layouts        | [render_grounded.py](scripts/render_grounded.py), then [compose_layout.py](scripts/compose_layout.py): background, clay, real cast shadow per camera |
| Upload         | `upload_asset` with `file_size`, PUT the parts, `upload_asset_complete`, one per layout                                                              |
| Repaint        | Reference-capable image model, `referenceImages: [layout, source]`, prompt below                                                                     |
| No background  | Background-removal model on the same repainted frame, then [studio_shadow.py](scripts/studio_shadow.py)                                              |
| Wait           | `jobs_wait` takes at most 32 ids per call; re-call with `pending_job_ids`                                                                            |

All four scripts are run by the agent in a local shell, not by the MCP server. `render_grounded.py` runs inside Blender (`blender -b --factory-startup --python render_grounded.py -- ...`); the other three need Python with Pillow and numpy. Each prints its usage when run without arguments.

## Worked example: eight views plus top-down of one character

1. `upload_asset` the user's picture (or generate one with a plain background and the camera above), `upload_asset_complete`.
2. `recommend` an image-to-3D model with the user's words ("untextured mesh from one image"), plus `max_cost_cu` when the user set a budget, then `model_schema_get` and `model_run` with `dry_run=true` to price (image-to-3D jobs are expensive; a dry run rejects a payload missing its required image, so a quote for the whole chain before the source exists prices against any uploaded picture), then `wait=false` and `jobs_wait`. `asset_download` the GLB and save it with `curl -L`.
3. Find a skybox model with `search` (target="models", query="skybox", public=true, as `scenario-skyboxes` teaches; `recommend` has no skybox capability and can return a generic image model whose edges do not wrap) and generate one panorama in the picture's style, prompting for "viewpoint standing in the middle of an open empty floor at eye level, the floor clearly visible all around, no people". Download it.
4. `blender ... render_grounded.py -- --glb hero.glb --out search --search`, then `python3 match_view.py hero.png search/cameras.json`. The top row's azimuth and elevation are `<az>` and `<el>` below; open the matching `search/search_az..._el...png` next to the picture to confirm, since front and back can score alike.
5. `blender ... render_grounded.py -- --glb hero.glb --pano world.png --out views --az0 <az> --elev <el> --only 00,02,04,06,08,10,12,14,top` (the eye ring has 16 cameras, 22.5 degrees apart; `--height` sets the panorama eye height, `--yaw` turns the world, `--zoom` the framing). Keys count from camera zero, not from the subject's front, so with a turned source key 08 shows the back at that same turn; for views square to the subject, render into another `--out` with `--az0` set to the search frame where it faces the camera squarely. Then `python3 compose_layout.py views`. Look at every layout: the clay must stand on the floor, with the shadow under it.
6. Upload each `layout_<key>.jpg`. `recommend` an image model for reference-guided repainting, and check that its `model_schema_get` lists `referenceImages` (1024 square, a high quality tier and an opaque background worked well). Price one with `dry_run=true` (the quote covers one view: multiply by the view count before launching), then launch one `model_run` per view with `wait=false`, `referenceImages: ["<layout asset>", "<source asset>"]`, and:

   > Image 1 is the exact final frame: a plain gray clay 3D model standing on the ground of a finished background, with its real cast shadow, seen from the exact camera angle wanted. Image 2 is the original design reference of the {kind}. Repaint the gray clay model as {what}, matching Image 2 for identity, design, materials and colors: {details}. {finish}. Follow the clay model exactly: same silhouette, pose, proportions, position and size in frame, and the same camera angle. {ground}; keep the cast shadow of Image 1. Keep the background of Image 1: same place, composition, perspective and horizon, in {background style}, crisp and detailed. Light the {kind} with the scene: {light}. No gray clay left, no extra characters or objects, no text.

   `{ground}` names the contact, for example "Her boots stand on the wet cobblestones exactly where the clay feet touch the ground". Add a line for parts the picture never shows (a shield on the back, a count of bags).

7. `jobs_wait` in batches of 32 or fewer. `asset_download` every result and build a contact sheet of all views. Regenerate only the views that fail; a fresh run of the same prompt usually fixes a one-off.
8. Transparent set: `recommend` a background-removal model, read its image field from `model_schema_get`, run it on each repainted asset id (not on a new studio repaint), download, then `python3 studio_shadow.py views/clay_<key>.png cut_<key>.png studio_<key>.png`. It prints how much of the clay body the cutout covers and how much lies outside it: a view far off the others, or with corners not clear, lost part of the subject or kept background, so rerun its removal.

## Common mistakes

- Repainting each angle independently on a plain background: scale drifted 7 to 53 percent between views in testing. Repaint the grounded layout, and cut out that same frame.
- Compositing the subject over a flat background photo: it floats and the horizon does not move with the camera. The dome floor is what gives true perspective from above and below.
- Adding a third reference, such as a previous view of the same angle: its mistakes are copied (one run gained an extra bag on every back view). Keep two references unless the extra one is verified clean.
- A "harmonize" pass over a finished view: it re-crops the frame and breaks the alignment with the clay.
- Skipping camera zero: view 00 then does not match the picture the user started from.
- Hardcoding model ids or prices: discover with `recommend`, price with `dry_run=true`.
- Passing more than 32 ids to `jobs_wait`, or polling `job_get`.
- Trusting a view without looking: check contact sheets for extra limbs, wrong sides, and leftover gray clay.
