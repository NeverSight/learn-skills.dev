---
name: p5-paint-animation
description: >
  Turn a text prompt, a photo, or a live video clip into hand-made-looking p5.js
  animation — pencil handwriting that writes itself, photos repainted as
  brushstroke art with paint-on animation and camera moves, and short videos
  (iPhone Live Photos included) repainted frame-by-frame as a living painting.
  Trigger on: "handwritten text animation", "paint this photo", "painted video",
  "sketch effect", "turn my live photo into a painting", "write-on effect".
  Everything is 100% code: p5.brush strokes rendered headlessly, no image models.
---

# p5 Paint Animation

Three flows, one engine. Pick by input:

| Input | Flow | Output |
|---|---|---|
| Text prompt / phrase | A: Write-on | Handwriting animates onto ruled paper, pen-tracked for camera |
| Photo | B: Repaint + paint-on | Brushstroke painting, still or painting-itself film, camera pull |
| Video / Live Photo | C: Living painting | Every frame repainted over a locked stroke lattice |


## When to use / when not

Use for: hand-made-looking motion — handwriting that writes itself, photos as
brushstroke paintings (still or animating), short clips as living paintings.
Do NOT use for: crisp typography or brand-accurate text (use real fonts),
photoreal output, footage longer than ~10s (render cost scales per frame ≈
5–20s each), or live/interactive pages (this renders offline MP4/PNG).

## Requirements and side effects

- Requires: Node 22.12+, ffmpeg on PATH, ~500MB disk (Chromium).
- `sh scripts/setup.sh` (run manually, once) uses the committed lockfile to
  download pinned dependencies from the npm registry: puppeteer 25.9.0,
  p5 2.3.2 (LGPL-2.1), and p5.brush 2.2.1 (MIT). Puppeteer downloads its
  pinned Chrome for Testing build from Google's download service. Read-only
  downloads; no credentials, no cost, nothing uploaded.
- Renders launch sandboxed headless Chromium on a blank page. Network and local
  file requests from sketches are blocked; sketches receive inputs as data URLs.
- Writes only inside paths you pass (`out.png` / `out.mp4`, plus a sibling
  `.track.json` and, with `--keep-frames 1`, a `_frames_*` directory).
- Optional, only for flow C subject matting: `npx hyperframes
  remove-background` (downloads the HyperFrames CLI from npm; local CoreML
  inference, no data leaves the machine).

## Verify success

Render any command below, then open the output: the last frame must show the
complete artwork (text fully written / painting fully covered), and re-running
with the same `--seed` must produce identical bytes on the canvas. The smoke
test used for review: `node render-anim.mjs sketches/handwriting.anim.js
/tmp/t.mp4 --size 1600x900 --seed 7 --inject 'PHRASE="go make something"'`.

## Setup (once)

```
sh scripts/setup.sh
```

Installs the exact dependency tree recorded in `scripts/package-lock.json`.
All commands below run from `scripts/`.

## Flow A — prompt → write-on animation

```
node render-anim.mjs sketches/handwriting.anim.js out.mp4 \
  --size 1600x900 --fps 24 --seed 7 --hold 12 \
  --inject 'PHRASE="your text here";SIZE=170'
```

- Full alphabet: lowercase, caps, digits, `? . , - / @`. Wraps automatically.
- Dials via `--inject`: `SIZE`, `INK` (hex), `BRUSH` (`"2B"` pencil, `"crayon"`,
  `"charcoal"`), `PAPER=1` for blank paper.
- The run writes `out.track.json` — per-frame pen position. For a
  camera-follows-pen move, crop each frame along the smoothed track
  (exponential follow, gain ~0.14, camera y LOCKED to the baseline — never
  follow the pen tip's y or the camera bounces on every ascender).
- For scraggly/messy writing raise the per-letter jitter in the sketch; for
  word-sync to a voiceover, transcribe first and start each word's strokes at
  its spoken time.

## Flow B — photo → painting (+ paint-on film + camera)

Still:

```
node render.mjs sketches/repaint.anim.js out.png \
  --size 720x900 --seed 3 --image photo.jpg --inject "STYLE=0;DETAIL=3"
```

Paint-on film (the painting paints itself, coarse-to-fine, painter-ordered —
calm regions first, the face last):

```
node render-anim.mjs sketches/repaint.anim.js out.mp4 \
  --size 720x900 --seed 3 --image photo.jpg --fps 14 --hold 40 \
  --inject 'STYLE=0;DETAIL=3;SUBJECT="0.5,0.5,0.44,0.55"'
```

- **Crop to the subject first.** Face size in frame is destiny: selfie-distance
  faces resolve beautifully; small faces stay figures. Portrait 4:5 or 9:16.
- Dials: `STYLE` 0 pastel / 1 gouache / 2 charcoal-sketch. `DETAIL` 1 painterly,
  2 faces resolve, 3 soft features (noses), 5 portrait-grade (adds a second
  fine lap). `LOOSE` 0.7–1.5 stroke wildness. `SAT` color compensation (~1.1).
- `SUBJECT="cx,cy,rx,ry"` (image fractions) paints everything inside that
  ellipse through all passes FIRST and drops a `subject-done` frame marker.
  Camera pull-out recipe: hold tight on the subject, then at the marker frame
  ease wide with ffmpeg zoompan (cosine ease, ~2s):
  `zoompan=z='if(lte(in,M),1.9,1.85-0.85*(0.5-0.5*cos(PI*min((in-M)/28,1))))'`
  (upscale 2x lanczos first so the tight phase stays sharp).

## Flow C — video / Live Photo → living painting

```
node render-video.mjs clip.mov out.mp4 \
  --size 720x900 --fps 12 --seed 7 --inject "STYLE=0;DETAIL=2"
```

- The stroke lattice is built ONCE from frame 1 and locked; only colors and
  orientations resample per frame. Strokes hold still — the painting never
  "boils" while the subject moves.
- **Live Photos:** get the paired `.mov` (share-sheet Options → Live Photo ON,
  or Photos.app → Export Unmodified Original). If it arrives as bare JPEG the
  motion was stripped in transit — ask for a 2–3s normal video instead; that's
  better input anyway.
- **Motion triage first.** Live Photos include the phone swinging. Measure
  per-frame motion (`ffprobe -f lavfi "movie=in.mov,signalstats"` → YDIF),
  paint only the calm window with `--start/--dur`, and ping-pong the result
  (forward+reverse concat) for a seamless breathing loop.
- Big camera motion? `WORLD=1` tracks the camera by image correlation and
  lets strokes live in world coordinates — the camera pans across one growing
  painting. Translation-only; fast zooms drift.
- Subject-only painting: matte frames first (`npx hyperframes
  remove-background`), pass the matted PNGs with `--frames DIR` and
  `MASKED=1`, and set `BG` to your paper color.
- Dark footage: grade with **gamma only** (`eq=gamma=1.2`). Never boost
  saturation before painting — shadow chroma noise becomes literal teal paint.

## QC gates (all flows)

- Read the actual output frames; never ship on intent. Check: faces resolve,
  no bare-canvas gaps, first/mid/last frames coherent.
- Same seed = identical render. Iterate one dial at a time against a fixed seed.
- For anything joining a larger film, verify seams numerically per
  motion-doctrine — this skill produces material, not final grammar.

`references/flows.md` has full worked recipes; `references/gotchas.md` is the
list of failure modes already hit so you don't hit them again.
