---
name: image-to-sculpt
description: >-
  Turns one image of any subject (an AI image, a render, a photo of a figurine or product, a drawing, or an idea
  turned into an image first) into a watertight 3D sculpt that is measured against the image and recorded step by
  step in Blender: front maps (mask, metric depth and focal length, normals), generated views of the unseen sides
  (registered over the whole circle and screened), a visual hull, then many recorded fit passes against every
  normal map, silhouette and the photo's depth, with symmetry, focus regions, gap cuts and smoothing. Ships a CLI
  (`scripts/i2s.py`) for case scaffolding, fal calls with a budget, registration, carving, fitting, map checks,
  Blender replay, timelapse and turntable films, exports (GLB, OBJ, STL) and a report. Use when the user wants a
  3D model or sculpt "from this image", a figurine or character turned into a mesh, a sculpting timelapse, or a
  check of a 3D model against a reference image. Not for scenes or rooms, text-to-3D without any image, rigging
  or animation, PBR texturing, or CAD-accurate parts.
license: MIT
metadata:
  hermes:
    tags:
      - 3d
      - sculpting
      - blender
      - image-to-3d
      - normal-maps
      - photogrammetry
    category: graphics
---

# Image 2 Sculpt

One image in, a sculpt out that you can prove: every surface the image shows is fitted to that image's own
normals, outline and depth in its own camera, every hidden surface comes from generated views that had to agree
with each other first, and every step of the build is recorded and replayed in Blender.

## Input routing

Any input ends in the same case layout (`i2s.py new CASE --input ...`). Details: `references/inputs.md`.

| Input | Do this | Notes |
|---|---|---|
| A character/creature/object render or AI image | `new` → `run` | the main path |
| A photo of a real object (figurine, toy, product, statue) | `new --kind photo` → `run` | MoGe gives real focal length and depth |
| A cut-out PNG with transparency | `new` → `run` | the alpha channel is the mask; no mask call |
| A busy image with several things in it | `prep --select "the red dragon"` | SAM-3 picks the subject |
| A drawing, sketch or flat illustration | `prep --restyle` | nano banana turns it into a 3D render first, keeping the pose |
| Several photos of the same object | `views --import DIR` | your photos replace generated views; angles found by registration |
| Only an idea | `imagine OUT.png "idea"` → `new` | a clean full-figure render to start from |
| No API key | a cut-out PNG (+ your own views) | front-only works too: the silhouette is inflated, depth behind is a guess |

## Workflow

Post a labelled visual at every checkpoint (`checks/sheet_*.png`, the views sheet, a turntable frame): images
first, numbers second. Fix rounds add steps; nothing recorded is ever edited.

1. **Scaffold.** `i2s.py new CASE --input IMG --subject "short noun phrase"`. Look at the image and write the
   subject phrase yourself ("stocky cartoon troll", "ceramic owl figurine"): it goes into every view prompt. The
   input is copied with its sha256 and padded to the nearest generator aspect ratio, so every view shares one lens.
2. **Front maps.** `i2s.py prep CASE` (mask, MoGe-3 depth + focal length, Marigold normals; units normalised to
   the subject). Check `ref/front_mask.png` and `ref/front_normals.png` before going on. Wrong subject picked →
   `--select`. Drawing → `--restyle`.
3. **Views.** `i2s.py views CASE` (9 views + 1 held out, ~$2 estimated; `--set minimal` for 5). Look at every
   generated image: a changed pose, an extra limb or a cropped subject is a bad view. Registration will reject
   views that disagree (IoU < 0.80 against the hull of the others), but say what you saw. Regions no view sees
   need new views at angles that look into them (`--angles "-30:25"`), not more smoothing
   (`references/views.md`).
4. **Hull.** `i2s.py hull CASE`: registration of every view (the asked-for angle is only a prior: left/right
   swaps are found, front/back is kept), re-centring, screening, the recorded carve, symmetry detection. Read the
   registered angles in `case.json`; `i2s.py symmetry CASE on|off` overrides the detected mirror plane.
5. **Fit.** `i2s.py fit CASE --stage all` (forms → surface → detail, 38 recorded passes), then `cut` (opens gaps
   between fingers, legs, arm and body that the photo shows), `smooth` (removes webs and specks), `fit --stage
   polish`. `i2s.py run CASE` does steps 2-8 in order with this default plan (`references/fitting.md`).
6. **Check and iterate.** `i2s.py check CASE` writes a sheet per view: reference, reference normals, sculpt,
   normal error, silhouette difference. Look for lumps, webs, missing gaps, flattened features. Target them:
   `parts CASE --prompt "hands"` then `fit --stage focus --region hands`, `cut --region hands`,
   `smooth --region box:...` (`references/checking.md`). Never claim a fix without the before/after sheet.
7. **Finish, Blender, films.** `finish` (facet smoothing, OBJ/STL), `blender` (every step replayed from the photo's
   camera, 360° turntable, each view, `sculpt.blend`, GLB), `film` (two-panel timelapse that ends in the 360°
   turn, turntable, views sheet, hero image) (`references/blender-and-delivery.md`).
8. **Report and stop.** `report` writes `out/REPORT.md`, `out/index.html` and the per-step chart. Present the
   timelapse, the views sheet and the measured table, say what is weak, and stop. The user decides what next.

## Hard rules

- **The photo governs what it sees.** Generated views only fill in where the photo does not see; their depth is
  never used (it disagrees by centimetres between views). Never average a generated view's normals over the photo's.
- **Register every view; never trust the requested angle.** Generated views were off by 20–155° on the troll,
  mostly left/right swaps. The search allows those but keeps front views in front and back views behind (a
  symmetric subject's back outlines like its front). Read the registered angles in `case.json`.
- **Screen before you carve.** A view that disagrees with the others is a different subject or pose: reject it
  (and say so) rather than cutting the sculpt with it.
- **Hold one view out.** It never moves the surface; its camera is frozen before fitting. Report it separately
  from the views used to fit. It is generated too, so it measures consistency, not truth.
- **Measure, don't eyeball alone.** IoU, outline distance, normal angle, roughness against the reference's own
  roughness, the photo's depth. One number never stands for "quality": report them side by side.
- **Distance fields stay exact.** Every operation re-distances the grid (exact triangle distances in a band, EDT
  beyond). Offsetting an inexact field, mirroring the field itself, or blurring normal targets made staircases,
  moiré rings and flattened noses in the case this was built from (`references/lessons.md`).
- **Record everything.** Every carve, pass, cut and smoothing is a step in `build/steps/` and `build/log.jsonl`,
  replayed in Blender and shown in the timelapse. Never edit a recorded step; add a new one.
- **Paid calls:** every fal call goes through the case budget (`settings.budget_usd`), its request id is saved in
  `case.json` before waiting, and nothing is resubmitted blindly. `FAL_KEY` is never printed or written.
- **Visual feedback at every checkpoint**, and frame 0 of every film is a finished thumbnail.
- **Say what is invented.** The back of a subject seen only from the front is the generator's guess.

## References

| File | Read when |
|---|---|
| `references/inputs.md` | routing an unusual input; masks, restyle, select, imported photos, idea-only |
| `references/views.md` | generating, judging, registering, screening and adding views |
| `references/fitting.md` | what a pass does, stages, parameters, cut / smooth / focus, the default plan |
| `references/checking.md` | reading map sheets and metrics, the held-out view, what to fix next |
| `references/blender-and-delivery.md` | Blender replay, films, exports, the report, the review page |
| `references/conventions.md` | world frame, cameras, units, file formats (for writing new tools) |
| `references/lessons.md` | what went wrong on the first cases and why the rules above exist |

Templates: `templates/CONTRACT.md` (copied into every case), `templates/acceptance.json` (targets).
