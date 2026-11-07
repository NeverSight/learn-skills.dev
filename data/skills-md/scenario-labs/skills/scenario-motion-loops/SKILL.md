---
name: scenario-motion-loops
description: "Use when someone wants seamless looping motion graphics for video in their own brand colors: animated backgrounds behind titles, filler for the dead seconds between AI shots, bumpers, transitions or shape animations, built as code and rendered to MP4, optionally with their mascot, product or character from Scenario composited over the loop. Keywords: seamless loop, motion background, canvas animation, motion graphics, loop seam, motion blur, H.264 export, alpha composite."
license: MIT
---

# Scenario Motion Loops

## Overview

A loop is a pure function of time, drawn with Canvas 2D in one HTML file. Nothing is generated, so
nothing warps or flickers, one color change rebrands it, and it renders at any size.

- `draw(ctx, w, h, t, P)` paints the frame at `t` seconds. Every period divides the 12 s loop, so
  the frame at 12 s is the frame at 0 s.
- [scripts/loop-template.html](scripts/loop-template.html) holds the helpers (`M.*`), the palette
  (`P`) and `tile(...)` registration. Tiles from the Motion Loops exploration on scenario.com (80
  loops, each with its code) run in it unchanged.
- [scripts/render-loop.mjs](scripts/render-loop.mjs) checks the page, renders stills or the MP4, and
  checks the encoded file.
- Scenario makes only the subject: a mascot, product or character as a cut-out PNG with alpha. The
  page draws it on the loop's clock, so the composite keeps the motion blur and still loops. The
  loop itself costs nothing.

Needs Node 18 or newer, ffmpeg 5.1 or newer with ffprobe, and Playwright where the script runs
(`npm install playwright`, then `npx playwright install chromium`, or `--channel chrome` with Google
Chrome installed). Connection, model discovery, uploads and pricing: see the `scenario` skill. The
cut-out: `scenario-image-editing`. The video shot: `scenario-video`, and its background removal:
`scenario-video-editing`. If a sibling skill named here is missing from your available skills, ask
the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed
from tool schemas and flag the gap.

## Quick reference

```bash
cp scripts/loop-template.html loop.html            # one loop per file: settings, draw(), overlay
# open loop.html in a browser to preview; ?t=3 freezes it, ?tone=accent or ?tone=light switches tone
node scripts/render-loop.mjs loop.html --check     # determinism and loop seam, no video
node scripts/render-loop.mjs loop.html --stills look --at 0,3,6,9               # stills to look at
node scripts/render-loop.mjs loop.html --out loop.mp4                            # 12 s, 1920x1080, 24 fps
node scripts/render-loop.mjs loop.html --params "overlay=subject.png" --out loop.mp4   # with a cut-out
node scripts/render-loop.mjs loop.html --width 1080 --height 1920 --out loop-9x16.mp4  # vertical
node scripts/render-loop.mjs --qa loop.mp4 composite.mp4   # seam and format check of any MP4
```

- Run it from a folder where Playwright is installed. Existing files are never overwritten without
  `--force`.
- The page check renders one moment twice (they must match) and compares the frame at exactly 12 s
  with the frame at 0 s. It also compares the step across the loop point with the motion around it
  and at every cycle boundary.
- A render refuses to encode unless the check prints `PASS`. `--ignore-seam` is only for a cut
  designed to sit at the loop point; it waives the seam verdict of both checks.
- Defaults, the settings the 80 loops shipped with: 24 fps, 8 motion-blur sub-frames over a 180
  degree shutter, 2x supersampling, H.264 High, CRF 16, 4:2:0, BT.709 limited range, faststart.
- A full 1080p render took about 6 minutes at authoring time (about 1.3 s per frame). Run it with a
  long timeout, or in the background.

Rules every tile follows:

- **Periods**: every period divides 12 s (1, 1.5, 2, 3, 4, 6, 12). Use `M.phase(t, period, offset)`.
- **Scrolls**: move a whole number of pattern repeats per period; a fractional repeat jumps at the
  seam.
- **Randomness**: only from `M.rand(i, salt)`. Never `Math.random`, `Date` or state carried between
  frames: motion blur and the checks render frames out of order.
- **Units**: sizes from `u = h / 100`, counts from `w`, so a loop holds at 16:9, 9:16, 1:1 and
  thumbnail size.
- **Colors**: only from `P` (`bg`, `fg`, `fg2`, `mid`, `accent`, `paper`, `ink`). Rebrand by
  changing `BRAND`; fix contrast by changing tone (dark, accent, light), never by adding a color.
- **Multi-hue loops**: a rainbow or hue sweep is the one exception. Compute hues as
  `hsl(${360 * M.phase(t, 12)}, ...)` with a period dividing 12, and keep its settings in `BRAND` so
  it still rebrands from one place.
- **Easing**: from `M.ease`, with anticipation, overshoot and holds. Constant speed only for scrolls
  and streams.

Patterns that close the loop, depth without a 3D engine, and review habits:
[references/loop-craft.md](references/loop-craft.md). Read it before writing a new `draw()`.

## Worked example: a brand mascot floating over a coded loop

Goal: a 12 s seamless 1920x1080 loop in the brand's colors with the brand's mascot floating in it,
and optionally a version where the mascot waves.

1. **Build the loop first (local, free).** `cp scripts/loop-template.html mascot-loop.html`, set
   `BRAND.accent` to the brand color, and keep the example tile (Perspective Floor, a grid streaming
   toward the camera) or write your own `draw()`. Then:

   ```bash
   node scripts/render-loop.mjs mascot-loop.html --check
   node scripts/render-loop.mjs mascot-loop.html --stills look --at 0,3,6,9
   ```

   `--check` must end in `PASS`. Look at the stills.

2. **Make the cut-out.** Connect and pick the team and project per the `scenario` skill. Upload the
   user's mascot file if there is one. `recommend` with:

   ```json
   {
     "capability": "img2img",
     "prompt": "The mascot from the reference image, full body, three-quarter view, a light floating pose, cut out on a transparent background with clean edges, no shadow, no text",
     "limit": 5
   }
   ```

   Without a file, use `"capability": "txt2img"` and describe the mascot. Prefer a member whose
   `model_schema_get` schema offers a transparent background. Otherwise remove the background
   afterwards per `scenario-image-editing`. Price with `dry_run` and wait for the user's go.
   Unattended, run only within a budget the task states; otherwise stop and report the price. Then
   `asset_download` with `"format": "png"` and `curl -L -o subject.png "<url>"` into the folder of
   `mascot-loop.html`.

3. **Inspect the cut-out.** View the PNG at 100% over the loop's background color. Halos at the
   outline show on dark tones: regenerate rather than hide them. A background remover's schema often
   has an edge or threshold setting: raise it on the re-run.

4. **Composite in the canvas and render.**

   ```bash
   node scripts/render-loop.mjs mascot-loop.html --params "overlay=subject.png" --stills look --at 0,0.75,1.5,2.25 --force
   node scripts/render-loop.mjs mascot-loop.html --params "overlay=subject.png" --out mascot-loop.mp4 --psnr 4
   ```

   `drawOverlay()` in the page floats the subject on a 3 s bob and a 6 s sway with a contact shadow,
   so the composite still loops. Adjust size and placement there. The script checks the page,
   renders 288 frames, encodes, and checks the file's loop point. `--psnr` compares one encoded
   frame with its lossless render.

5. **Optional: a shot where the mascot moves.**
   - Generate it per `scenario-video`: `img2video` from the cut-out, prompted "the mascot waves and
     turns its head, plain flat background, locked-off camera, no cuts". A plain background and a
     locked camera make the removal clean.
   - Remove its background per `scenario-video-editing`, choosing WebM VP9 with alpha (ProRes 4444
     for editing software).
   - Render the loop without the overlay (`--out loop-plain.mp4`) and lay the shot over it:

   ```bash
   ffmpeg -stream_loop -1 -i loop-plain.mp4 -c:v libvpx-vp9 -i shot.webm \
     -filter_complex "[1:v]fps=24,scale=-2:720[s];[0:v][s]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" \
     -c:v libx264 -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
     -color_range tv -movflags +faststart -an composite.mp4
   ```

   The composite is as long as the shot. It is not a seamless loop unless the shot loops: run `--qa`
   on anything meant to loop.

6. **Hand over** the HTML (the loop stays editable), the MP4, the stills and any composite.

## Common mistakes

- **A seam jump at 12 s.** A period that does not divide 12 (a 5 s cycle), or a scroll that moves
  2.5 repeats. `--check` reports `SEAM JUMP`. Fix the period; never crossfade the ends.
- **State, `Math.random` or `Date` in a tile.** The same `t` gives different frames and the loop
  cannot close. `--check` reports `NOT DETERMINISTIC`.
- **Color helpers that only read hex.** `P.mid` and `M.mixColor` return `rgb()` strings, and a
  hex-only parser silently turns them black. Use the template's `M.rgba` and `M.mixColor`.
- **Strobing on fast moves.** Eight sub-frames show stepped copies on a whole-frame push; one
  full-page swipe needed 40. Raise `--samples` for very fast loops.
- **Treating every flag as a bug.** A designed snap (a pop, a burst) or a hold at the loop point can
  trip the seam check. Look at the frames before changing the code.
- **A counter that wraps wrong.** Anything indexed by cycle wraps with `M.mod`, or it reads "06 /
  05" at the loop point.
- **Text before the font loads.** Canvas text does not wait for web fonts: await
  `document.fonts.load(...)` before the first frame, or draw no text.
- **Opening the page from `file://` to render.** A local overlay image taints the canvas and the
  readback fails. `render-loop.mjs` serves the folder over a local address; the browser preview is
  unaffected.
- **Chasing bitrate.** On flat color the file looks small, but the encoder adds almost no loss. The
  real loss is 4:2:0 chroma on thin saturated lines: check with `--psnr` and thicken those lines.
- **Color flags without `setparams`.** `-colorspace`, `-color_primaries` and `-color_trc` alone left
  primaries and transfer untagged on ffmpeg 7. End the filter chain with `setparams`, as both
  commands here do. `--qa` reports `UNTAGGED COLOR` otherwise.
- **Losing the alpha of a VP9 shot.** ffmpeg's built-in VP9 decoder ignores alpha and the shot
  arrives in a black box. Put `-c:v libvpx-vp9` before `-i shot.webm`. ffprobe reports such a file
  as `yuv420p` with `alpha_mode=1`; it still has alpha.
- **Making the loop with a video model.** A generated clip's last frame rarely meets its first. Keep
  the loop in code; use Scenario for the subject.
