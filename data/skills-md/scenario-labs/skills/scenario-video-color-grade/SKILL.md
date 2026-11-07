---
name: scenario-video-color-grade
description: "Use when color grading, color correcting, or relighting an existing video or still with deterministic code instead of a generative model: cinematic looks (teal and orange, film stock, bleach bypass, noir, duotone, faded 70s), golden hour, blue hour or day-for-night, log footage (S-Log3) to Rec.709, matching a reference image's colors, black and white with one kept or swapped color, .cube LUT export, a look comparison grid, or a grading showreel."
license: MIT
---

# Scenario Video Color Grade

## Overview

Every grade here is math the agent writes, measures, and tunes; no generative model touches the
pixels. Per-pixel color operations bake into a 33³ `.cube` LUT that ffmpeg applies. Spatial
operations (relight, keyed or masked selective color) run per frame in numpy before the LUT. Results
are exact, identical on every frame, and editable: the LUTs load in Premiere, After Effects, and
Resolve. Framing, motion, and frame count are kept, so a seamless loop stays seamless.

Scenario supplies two preset LUT tool models and the segmentation masks that make selective color
exact. New footage is out of scope. Connection and the core loop: the `scenario` skill. Running the
LUT tool models on long clips (cost follows the clip, `wait=false`): `scenario-video-editing`. Music
for a reel: `scenario-audio`. If a sibling skill named here is missing from your available skills,
ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended,
proceed from tool schemas and flag the gap.

The scripts run locally with `python3` and need ffmpeg, numpy, scipy, and Pillow. Each prints its
usage when run without arguments, refuses to overwrite outputs without `--force`, and never calls
Scenario. Paths below are relative to this skill's folder.

## Two routes: a Scenario preset, or your own recipe

Scenario's 3D Color LUT tool models apply one preset (`lutStyle`, about 150 at authoring time) at an
opacity (`lutIntensity`): film-stock emulations, log-to-Rec.709 conversions for the common camera
log formats, print-film conversions, and creative looks. `model_scenario-postprocessing-lut` grades
images and `model_scenario-postprocessing-lut-video` grades video. Both ids are fixed: each is
Scenario's single deterministic tool for the operation, so discovery would only re-derive it. The
video tool keeps frame count and timing.

Use a preset first when:

- **The footage is log.** Pick the preset for the camera's log format. It covers far more cameras
  than the local `decode_log` op, which reads S-Log3 only.
- **A preset look is the ask** (a film stock, a print emulation), or the grade must stay inside
  Scenario: no local ffmpeg or Python, a node in a Scenario workflow, many images.

Write a recipe when the look must be tuned or invented, needs position (masks, relight, vignette,
grain, halation), must match a reference, must ship as a `.cube` file, or feeds a reel. The tool
models take only their own presets, never a custom `.cube`. The routes chain: convert log on
Scenario, then grade its Rec.709 output with a recipe that drops `decode_log`.

Running a preset:

1. `model_schema_get` on both ids and read `lutStyle`'s allowed values; never guess them. Shortlist
   only values the video tool lists too.
2. Try two or three presets on one still with the image tool. Names do not say which input a preset
   expects, so compare similar ones (two print emulations of one stock) side by side.
3. `upload_asset` the clip, price it with `model_run` and `dry_run=true`, run the pick, `jobs_wait`,
   then `asset_download`.
4. `ffprobe` the result: at authoring time the video tool could return MPEG-4 Part 2. Re-encode for
   the web with
   `ffmpeg -i in.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart -c:a copy out.mp4`.

## Quick reference

- [render_looks.py](scripts/render_looks.py): applies looks to a video (one mp4 per look, audio
  copied) or to one frame (PNG stills plus a labeled `grid.jpg`), and writes `luts/<key>.cube`.
- [inspect_frame.py](scripts/inspect_frame.py): `grid` (pixel coordinates), `sample` (hue,
  saturation, and brightness percentiles of rectangles), `key` (red overlay of what a selective key
  keeps, with blob sizes).
- [match.py](scripts/match.py): measures a reference image for the `match` op, a Reinhard transfer
  in CIE Lab.
- [showreel.py](scripts/showreel.py): a reel of every look, with a typed name panel, wipes on one
  continuous clip, a grid finale, and an optional end card and music.
- [grade.py](scripts/grade.py), [spatial.py](scripts/spatial.py), [media.py](scripts/media.py): the
  color ops and LUT writer, relight and keying, ffmpeg I/O. The scripts above import them.
- [looks_library.json](assets/looks_library.json): 21 tuned starting looks, including day-for-night,
  keyed black and white, a reference match, and four relight presets.
- [looks.json](examples/looks.json): twelve tuned looks, with mask-based black and white plus one
  color and a reference match that needs `match.py` first.
- [ops.md](references/ops.md), [looks.md](references/looks.md), [keying.md](references/keying.md),
  [relight.md](references/relight.md): every op, how each library look is built, keys and masks,
  relighting.

## Steps

1. **Look at the source.** `ffprobe` it and pull three or four frames from different moments. Note
   whether it is log (milky, flat), normal, or already graded. The looks were tuned on a soft,
   slightly desaturated source; on a contrasty one, cut saturation and contrast by about a third.
   Note the light direction and the key objects' colors.
2. **Set up `looks.json`.** Copy the library or the example set next to the clip, then keep, rename,
   add, or delete looks. A look holds `name` and `settings` (the reel's two label lines), optional
   `relight`, optional `selective`, `ops` (baked into the LUT), and optional `vignette`, `grain`,
   and `halation`. They apply in that order. Keys sort the outputs; keys starting with `_` are
   notes.
3. **Still test before any video.**
   `python3 scripts/render_looks.py clip.mp4 --looks looks.json --out still_test --frame 40`, then
   open `grid.jpg`. Check that every look differs from the source, none clips or turns skin orange,
   and skin stays believable outside the stylized looks. Iterate here: a still takes seconds, a
   render minutes. Test two frames on a moving clip.
4. **Keyed looks: measure, then preview.** `inspect_frame.py grid` for full-resolution coordinates
   (the still-test `grid.jpg` tiles are downscaled), `sample` on the object and what shares its
   color (skin, lips, ground), then `key ... --frame 10 90 160` for the overlay: red on a gray frame
   marks what is kept. The separating dimension is often brightness or saturation, not hue. For an
   exact result, use object masks (worked example).
5. **Relight** at 0.3 to 1 stop, from the side that already holds the highlights. It changes light
   character, never geometry or cast shadows: tell the user so.
6. **Match a reference** with
   `python3 scripts/match.py clip.mp4 reference.jpg match/reference.json [--crop w:h:x:y]`, then use
   `{"op": "match", "stats": "match/reference.json"}`. Re-measure whenever the source changes.
   Matching the same kind of scene at another hour is a convincing time-of-day change.
7. **Render** with
   `python3 scripts/render_looks.py clip.mp4 --looks looks.json --out renders [--only k1,k2]`.
   - Pure color looks go straight through ffmpeg.
   - Relit and keyed looks took about 1 to 2 s per 1080p frame together at authoring time, so run
     long clips in the background.
   - A look whose mask or match stats are missing is skipped with a message.
   - Verify that each render's frame count equals the source's, and sweep keyed and relit renders
     for flicker, skin, and edges.
8. **Reel (optional)**:
   `python3 scripts/showreel.py --renders renders --looks looks.json --source 00_ungraded --out reel.mp4 --order k1,k2 --music track.mp3`.
   Put a dramatic look (duotone, noir) second or third, and prefer a clip that loops cleanly. The
   reel normalizes music to about -18 LUFS. The reel carries no branding by default. Add an end card
   only when the user asks, with their own `--credit` text or `--logo` (a white transparent PNG).
9. **Deliver** the renders, `renders/luts/*.cube` (in Premiere: Lumetri, Creative, Look), the grid,
   and the reel. Name the looks with spatial parts: their LUT alone is only the color, so an editor
   needs a mask too.

## Worked example: black and white with one kept color

The grading is local; only the masks come from Scenario, and the mask job never changes a pixel.

1. `recommend` with the need in the user's words, for example "segment one object across every frame
   of a video". Pick a video segmentation member, `model_schema_get` it, and build the parameters
   from its schema.
2. `upload_asset` the exact clip you grade. Price with `model_run` and `dry_run=true`, then run once
   per object with a short noun phrase as the text prompt ("red leather jacket", "red fuel pump").
   `jobs_wait`, then `asset_download` each mask video into `masks/`.
3. Overlay each mask's outline on two or three full-resolution frames. Its frame count must equal
   the clip's.
4. Give the look a `selective` block. A mask entry with a `key` keeps only the keyed color inside
   that object, so the white panels of a red pump stay gray:

```json
"selective": {
  "masks": [{"path": "masks/jacket.mp4"},
            {"path": "masks/pump.mp4", "key": {"center": 11, "width": 18, "min_sat": 0.28, "max_val": 0.62}}],
  "weights": [0.3, 0.55, 0.15], "sat": 1.7, "val": 1.05
}
```

5. Still test, then render. To swap the color (red to gold), add `"shift": 34` to the same block.

At authoring time, twelve looks on an 8-second loop cost 112 CU in all: two masks and the reel's
music. The grades themselves cost nothing.

## Common mistakes

- **Writing a recipe a preset already covers.** Log conversion and film-stock emulations are
  `lutStyle` presets: check them first.
- **Shipping the video LUT tool's output unchecked.** Re-encode MPEG-4 Part 2 to H.264 for the web.
- **A color key alone for one kept color.** Skin, lips, and warm backgrounds share the object's
  color and turn up colored at the edges. Use masks plus a key inside the object whenever the object
  sits near skin.
- **Hue-only keys.** A teal car reflecting a warm sky has almost no teal pixels, and lips share a
  red jacket's hue. Separate by brightness or saturation, set `min_area`, and preview. If it still
  leaks, tell the user it needs a mask.
- **Heuristic region masks ("change only the sky").** Hair, columns, and motion blur leak through.
  Offer a graduated filter or a reference match instead.
- **One source's tuning on another.** Re-run the still test on every new source.
- **Trademarks as look names.** Keep movie titles and film-stock brands out of public names; use
  descriptive ones ("Scorched Desert", "Vintage Slide").
- **`-shortest` with audio slightly shorter than the video.** ffmpeg drops the last frame and the
  loop breaks. The scripts avoid it; keep it that way in custom commands.
- **Grading alone.** Grading is taste: show grids and short previews, and iterate on what the user
  points at.
