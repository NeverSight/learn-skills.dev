---
name: scenario-blender-2d-animation
description: "Use when a 2D side-scroller shot, platformer cutscene, game trailer or parallax animation has to be built in Blender from Scenario-generated pictures (flat image cards, an orthographic camera, keyed jumps, rigid-body props), or when a finished shot needs a new theme or look without re-animating. Also use when image planes in Blender float above the ground, a tiled parallax layer shows a seam, or physics props leave the picture plane."
license: MIT
---

# Scenario Blender 2D animation

## Overview

Generate the art once per look; animate it once in Blender. A concept frame (an imagined in-game
screenshot) fixes the style, and the eight other pictures (sky, far and mid layers, ground strip,
foreground plants, props sheet, tree, the hero in two poses) take it as their reference, so the set
holds together. An image-to-video clip of the hero running in place on magenta becomes a looping
image sequence. One Blender script lays the pictures out as flat cards in depth, drives their
parallax from an orthographic camera that follows the hero, keys the jumps and runs rigid-body
physics on the props. A new look is ten new generations and a few measured numbers. The reference
result is a 7.7 second, 1080p, 24 fps shot in three looks. The deliverable is the film and its
`.blend`, which reads the pictures from `SET_DIR/game/` by relative path, so ship the folder with
it; for sprite strips a game engine plays, use `scenario-side-view-game-kit` or
`scenario-sprite-animation`.

Discover both lanes with `recommend`, the user's words as `prompt`: `capability: "txt2img"` for the
pictures, which need a reference-image input, a transparent background and exact width and height
(if the pick lacks one, or is a specialty for another style than the look, such as pixel art for a
painted cartoon, take the next ranked pick), and `capability: "img2video"` for the run clip, which
needs a first frame. `model_schema_get` each pick. Payload names below (`referenceImages`,
`background`, `numOutputs`) are examples: use the fields your pick's schema lists. Before
generating, tell the user the total for the nine pictures and the clip: `dry_run` the concept frame
and quote the rest from `recommend`, since a `dry_run` naming an asset that does not exist yet
returns 404. Then `dry_run` each later payload once its input exists, before running it.

Connection, uploads and the core loop: the `scenario` skill. If a sibling skill named here is
missing from your available skills, ask the user to install it
(`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and
flag the gap.

The scripts run locally and never call Scenario. Blender 5.x runs the scene script, headless or in
an open session (through a Blender MCP connection, for example); in a session, start from File >
New, since `--live` empties the open file and refuses any file but a new one or its own output.
Python 3 with Pillow, NumPy and SciPy runs the helpers, and ffmpeg reads the clip. Every helper
prints its usage when run without arguments and refuses to overwrite an existing output (or its
input) unless given `--force`.

## Quick reference

| Step          | How                                                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Pick models   | `recommend` (`txt2img`, `img2video`), `model_schema_get`, then `model_run` with `dry_run: true` per distinct payload                      |
| Concept frame | Text to image, 16:9, opaque, two takes: an in-game screenshot, strict side view, layers named in order ([prompts](references/prompts.md)) |
| Layers        | One call per layer with the concept as reference; transparent except the sky; wide (3072 x 1152) for tiled layers                         |
| Sheets        | Props, tree and foreground on transparent backgrounds with wide gaps, numbered in reading order                                           |
| Hero          | Two poses (rest, jump) side by side on flat magenta; [reframe_stills.py](scripts/reframe_stills.py) makes square first frames             |
| Run clip      | Image to video from the rest pose: "like a treadmill", locked camera, magenta that never changes; 5 s is enough                           |
| Run loop      | [run_loop.py](scripts/run_loop.py): key, find the cleanest one-period loop, write `hero_run/run_001.png`...                               |
| Cut and key   | [prep_assets.py](scripts/prep_assets.py) `cut` (sheets), `key` (magenta stills), `tile` (seamless wide layers)                            |
| Hulls         | [trace_hulls.py](scripts/trace_hulls.py): convex hull of each prop's alpha into `shapes.json`                                             |
| Measure       | [measure_set.py](scripts/measure_set.py): horizon, ground line, island and pedestal tops ([example config](examples/config.json))         |
| Build         | [build_scene.py](scripts/build_scene.py) `-- --set SET_DIR --review`, then `--final`                                                      |
| New look      | New concept frame, the same eight pictures and clip, same file names, a new `config.json`; nothing else changes                           |
| Wait          | `jobs_wait` with up to 32 `job_ids`; on timeout re-call with the returned `pending_job_ids`                                               |

## Worked example: a jungle run, then a snow day

Pass `team_id` and `project_id` on every call (the `scenario` skill covers picking them).

1. **Concept frame.**
   `recommend { "capability": "txt2img", "prompt": "<the user's request>; needs reference image input, transparent background, exact width and height" }`,
   `model_schema_get` the pick, price two takes with
   `model_run { "model_id": "<pick>", "dry_run": true, "parameters": { "prompt": "...", "width": 1536, "height": 864, "background": "opaque", "numOutputs": 2 } }`
   and the screenshot prompt from [references/prompts.md](references/prompts.md) section 1. Run it,
   `jobs_wait` if it returns a `job_id`, `asset_display` both takes and keep the one whose layers
   you can name one by one. Its asset id is the reference for everything that follows.
2. **Layers, one call each.** The same pick with `referenceImages: ["<concept id>"]`: the sky (2560
   x 1440, opaque), the far layer and the mid layer (3072 x 1152, transparent), the ground strip
   (2048 x 768, transparent, a flat walkable top at about 30 percent from the top, no end caps) and
   a foreground sheet of five plant clusters (3072 x 1024, transparent). Price them, then run them
   with `wait: false` in waves within the team's concurrency ceiling (the `parallel-custom-jobs` row
   in the `scenario` skill: a launch refused with that 429 created no job, so relaunch it in the
   next wave), retiring each wave with `jobs_wait`.
3. **Props and tree.** A props sheet (2048 x 1536, transparent): numbered props in a loose grid with
   wide gaps (a pot, a tall vessel, a lidded jar, a heavy statue, the fruit that will fall, a coin,
   a floating island, a flat pedestal), and the tree alone (1024 x 1536) with no fruit in its crown.
   The names `cut` gives them in step 6 are roles, whatever a new look draws: `jar` stands on the
   pedestal with `idol`, the heaviest, on its lid and `pot_round` beside it, `amphora` stands on the
   grass past the landing, and `coconut` is the fruit.
4. **Hero.** Two poses on flat magenta (1536 x 1024, opaque, two takes): rest on the left, jump on
   the right, both the same size, pure side profile facing right. `asset_download` the kept take,
   then `python3 scripts/reframe_stills.py hero.png --name hero --out frames` writes `hero_rest.png`
   and `hero_action.png` (lower `--figure` for a long tail). Upload the rest frame with
   `upload_asset` and `upload_asset_complete`.
5. **Run clip.**
   `recommend { "capability": "img2video", "prompt": "<the user's request>; first frame input, 5 seconds" }`,
   `model_schema_get`, price a five-second clip with the rest frame's asset id in the schema's
   first-frame field and the treadmill prompt ([prompts.md](references/prompts.md) section 5), with
   audio off and a 1:1 aspect ratio where the schema has those fields (the loop keeps only silent
   frames, and the jump still's scale assumes the clip is the square first frame resized), run it,
   `jobs_wait` (minutes, re-called as needed), `asset_download`.
6. **Process.** Into `jungle/game/` (the sky stays one wide card: copy it as `sky.png`):
   `python3 scripts/prep_assets.py tile raw/sea.png jungle/game/sea_tile.png 384`, the same for the
   mid layer (`jungle_tile.png`; a fade of one eighth of the width) and the ground
   (`ground_tile.png`, `256` for 2048 px);
   `python3 scripts/prep_assets.py cut raw/props.png jungle/game pot_round,amphora,jar,idol,coconut,coin,island,pedestal`;
   `CUT_GROW=2 python3 scripts/prep_assets.py cut raw/foreground.png jungle/game fg_bush,fg_fern,fg_hibiscus,fg_boulder,fg_curl`;
   `python3 scripts/prep_assets.py key frames/hero_action.png jungle/game/hero_jump.png`;
   `python3 scripts/run_loop.py clips/hero_run.mp4 jungle/game/hero_run` (it prints `run_n`,
   `run_fig_px`, `run_pad_px` and `run_canvas_px`, the clip's height);
   `python3 scripts/trace_hulls.py jungle/game`. Copy the tree (keyed or already transparent) as
   `palm.png`.
7. **Measure.** `python3 scripts/measure_set.py jungle/game --ground-h 4.3` (the ground card's
   height in meters, `ground_h` in the config) prints the horizon, the walkable line (already moved
   10 cm down so the feet sink into the grass lip), the island and pedestal tops and the jump
   still's feet row. Write them with the run numbers into `jungle/game/config.json`. Layer heights,
   the fruit positions and the hero's height in meters are set by eye on the review stills: start
   from [examples/config.json](examples/config.json)
   ([references/pipeline.md](references/pipeline.md) lists every key).
8. **Build and review.**
   `blender -b --factory-startup --python-exit-code 1 -P scripts/build_scene.py -- --set jungle --review`.
   Outputs land in the folder holding `jungle/` (or `--out DIR`): `platformer_scene<tag>.blend`,
   `review<tag>/` and, with `--final`, `platformer<tag>.mp4`; a rebuild over them needs `--force`.
   Look at the 11 review stills: feet on the ground, the tree standing on the ground, no seam, the
   tower standing until the hero reaches it, every piece inside the frame. Then `--final` renders
   the film. Before delivery, walk [references/checks.md](references/checks.md).
9. **A new look.** Generate a new concept frame (a white winter valley, a snow leopard cub in a red
   hat), the same eight pictures and clip with it as reference, process into `snow/game/` with the
   same names, measure a new `config.json` (with `"tag": "_snow"`) and run the same build with
   `--set snow`. Two looks line up frame for frame. The snow clip's background drifted, so its loop
   came from
   `run_loop.py clip.mp4 snow/game/hero_run --key border --from 60 --to 124 --skip 0 --periods 8:16 --clean`.
10. **Ledger.** One line per Scenario job with model, parameters, inputs, outputs, job id, cost,
    kept or not, and why.

## Common mistakes

- Trusting the grass tips as the ground line: every look's hero floated 3 to 8 cm plus the run bob
  until the line moved about 10 cm into the lip, which `measure_set.py` now applies.
- Keying a drifting clip on fixed magenta: one run clip went from magenta through red and yellow to
  green. Use `--key border` and take the loop from a stretch away from any red or pink on the
  character.
- Cutting leafy sheets with the default grow: the five foreground plants came out as four pieces
  until the cut ran with `CUT_GROW=2`. Check the printed count against the names.
- Not checking enclosed pink after keying: `prep_assets.py key` keeps pink enclosed by the
  silhouette (a cat's inner ears), but look at ears, tongues and flowers.
- Hard-coding the run length: the cat and the snow leopard looped in 12 frames, the red panda in 9.
  Copy `run_n` from `run_loop.py`'s output.
- A landmark at the end of a wide layer: `tile` joins the two ends along the path where they differ
  least, keeping a tree whole or dropping it, but a landmark as wide as the overlap gets cut; ask
  for content spread across the width.
- Passing a local path or URL to `model_run`: upload the file first and pass the asset id.
- Hard-coding model ids or prices, or polling `job_get` instead of re-calling `jobs_wait`.

Changing `build_scene.py` itself (depths, parallax factors, physics): read
[references/pipeline.md](references/pipeline.md) first, which records the decisions the reference
shot paid for.
