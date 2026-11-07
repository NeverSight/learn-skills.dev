---
name: img2figma
description: This skill should be used when the user wants to turn a static image — a screenshot, mockup, concept render or design comp — into a real, editable Figma file with proper layers, auto-layout frames, editable text and true vector logos (not a pasted bitmap). Triggers on "image to Figma", "screenshot to Figma", "turn this mockup into Figma", "make this PNG a real design", or pointing at a .png/.jpg and asking for a Figma version. Also covers the reverse leg — reading a Figma frame back out via the Figma MCP server to build code from it.
argument-hint: <path-to-image> [output-project-name]
---

# img2figma — image → editable Figma, by measurement

Turn a flat image into a real Figma layer tree. Not a traced bitmap: auto-layout
frames, editable `TextNode`s, true vector logos, per-side strokes.

## The core principle

**Never build from your impression of the image. Build from measured values.**

Every fidelity miss traces back to eyeballing something that should have been
measured. The loop is always: measure the source → author HTML → render →
diff numerically → correct → repeat. Do not skip the diff because it "looks
right"; it will not be right, and you will not be able to see the 3px.

## Why HTML in the middle

The pipeline is `image → measured HTML/CSS → headless Chromium →
getComputedStyle → Figma nodes`.

The DOM is where the precision lives. Corner radii, shadows, gradients,
opacity, exact spacing are all trivially exact via `getComputedStyle()` and
near-impossible to recover from pixels. The screenshot→HTML hop is the only
lossy step, and because *you* author the HTML against measurements, nothing is
guessed. Everything after it is measurement, not inference.

### The hard ceiling — say this out loud to the user

**Alpha compositing is unrecoverable from an image.** A screenshot is already
composited. `rgba(0,0,0,0.5)` over white and opaque `#808080` are byte-identical.
You cannot recover opacity, `backdrop-filter` or blend modes from pixels. Any
colour you extract is a *resolved* colour that breaks the moment the background
changes. This is a theoretical limit, not an engineering gap. Do not promise
around it.

## Pipeline

```
source.png
   │  1. measure    panel bounds, element geometry, colours   (scripts/measure.py + ad-hoc numpy)
   ▼
index.html          hand-authored to the measured numbers
   │  2. render     scripts/render.mjs  → out/render.png
   │  3. diff       scripts/measure.py  → per-element dx/dy/dw/dh
   │  ↺  correct and repeat until deltas are ±2px
   │  4. extract    scripts/extract.mjs → plugin/scene.json
   │  5. verify     scripts/sim.mjs     → mock-Figma position check
   ▼
Figma plugin (plugin/) — drop scene.json
```

## 0. Survey before you build

**Always run `scripts/plan.py <source>` first.** It reports dimensions, ink
density, proposed section seams and the payload cost. Never start authoring
without knowing how big the thing actually is.

```
python3 scripts/plan.py assets/source.png
```

- **≤ ~1600px tall → single frame.** Build as one `#frame`.
- **Taller → build in sections.** `plan.py` proposes horizontal seams by finding
  rows where the dominant background colour changes *on a quiet row* (low edge
  energy). A photograph shifts colour down its height too, so requiring the seam
  row to be quiet is what stops the hero being carved into strips. Treat the
  proposal as a starting point and sanity-check it against the image.

Each section is its own `index-NN.html` → `out/scene-NN.json`, built and
verified independently, then stacked:

```bash
node src/render.mjs  index-01.html out/render-01.png
node src/extract.mjs index-01.html out/scene-01.json
# ...repeat per section...
node src/merge.mjs                       # -> plugin/scene.json (vertical auto-layout page)
```

`merge.mjs` deduplicates assets across sections, so a logo used four times
embeds once.

### Payload

Every placed raster ships base64 inside `scene.json` at ~1.37x its file size.
A single full-bleed photo cost 3 MB on a 1672x941 hero. **Downscale placed
photos to about 2x their display size before embedding** — past roughly 8 MB the
plugin drop gets unpleasant.

### Frame sizing traps

- `#frame` must be `flex: none`. `<body>` is a flex container, `flex-shrink`
  defaults to 1, and a frame wider than the viewport is **squashed, not
  clipped** — so every measurement is taken against the wrong width.
- `render.mjs` derives the viewport from the frame and hard-fails if the written
  PNG does not match. `measure.py` refuses to diff two differently-sized images.
  Both exist because a clipped render is still a valid PNG: 16% of a design once
  went unmeasured while the diff reported clean convergence.

## 1. Measure the source

Find the design panel first. Mockups usually inset the design inside a coloured
frame; everything downstream is relative to that panel, so get it exact.

```python
# panel bounds: distance from the outer/frame colour
a = np.array(Image.open(src).convert("RGB")).astype(int)
outer = a[5, 5]
mask = np.abs(a - outer).sum(axis=2) > 60
ys, xs = np.where(mask)
# panel = xs.min()..xs.max(), ys.min()..ys.max()
```

Then measure elements with **projection profiles**, not connected components
(no scipy dependency, and text lines fall out naturally):

- Build a boolean ink mask for a band.
- Row-runs give you lines; column-runs within a line give you extent.
- **Light ink on dark → `lum > thr`. Dark ink on light → `lum < thr`.**
  `scripts/measure.py` has an `INVERT` flag; set it per design.

### Measurement traps that cost real time

- **Band clamping.** If your band starts at `x0=350`, it can never report an
  element at x=300 — it reports 350 and you chase a phantom layout bug. Make
  bands generously wider than the thing you are measuring.
- **Row-gap merging.** Serif descenders and tight leading merge adjacent lines
  into one blob. When a headline reports `h=109` for a 52px line-height, that is
  two lines merged, not a broken build. Measure headline lines in *fixed
  windows* per line instead of relying on run detection.
- **Threshold bleed.** A bright photographic element under text will merge with
  it. Raise the threshold for that band rather than trusting the merged result.

Sample colours as the **modal** value in a clean region, not the mean — means
are dragged by antialiasing and icons.

## 2. Author the HTML

Build at the panel's **native pixel size** so the diff is 1:1. Scaling to 1440
is a one-line change afterwards.

- Root element must be `#frame` with the exact panel dimensions.
- Use flex where the design is genuinely a row/stack — it becomes real Figma
  auto-layout. Use absolute positioning for overlays.
- Prefer `white-space: pre` with real newlines over `<br>` (both work now, but
  `pre` keeps one clean TextNode).
- Photographic elements stay as `<img>`. Logos should be **real SVG** — the
  single biggest fidelity win, and it makes the logo a true vector in Figma.

### Typography: match cap height first

Different typefaces have different cap-height ratios. Measure the target's cap
height, then solve for font-size:

```
font-size = measured_cap_height / cap_ratio_of_your_face
```

Blender Pro is ~0.615; most grotesques are ~0.72; check, don't assume. Once cap
heights match (`dh +0`), tune tracking to close the width gap. **You cannot
match both cap height and advance width across different typefaces** — say so,
and prioritise cap height.

## 3–4. Render, diff, correct

Run `render.mjs` then `measure.py target.png render.png`. Correct the largest
delta, re-run. Stop when text blocks are within ±2px. Flag anything that
cannot converge as a typeface-substitution limit rather than quietly leaving it.

## 5. Extract and verify

`extract.mjs` walks the DOM and emits `plugin/scene.json`. It reports warnings —
**read them, they are the point**. `sim.mjs` runs the real plugin code against a
mock Figma API and checks every node's position.

**Critical: a position check cannot see missing or misaligned text.** See
`reference/gotchas.md` — every bug in that file passed a 1.00px geometry check.

## 6. Import to Figma

```
Figma → Plugins → Development → Import plugin from manifest…
  <skill>/plugin/manifest.json
Run it, drop scene.json onto the drop zone.
```

One plugin serves every design — `scene.json` is the only thing that changes.
Re-import the manifest if `code.js` has been updated.

**Fonts must be installed system-wide first**, and Figma only scans fonts at
launch, so restart it after installing. `.woff2` cannot be installed on macOS —
convert with fontTools (`ft.flavor = None`) and merge per-weight families into
one family with proper typographic names (nameID 16/17), or Figma shows three
separate families.

## Propose-then-verify auto-layout

Naively mapping flex → auto-layout produces output that *looks* plausible and
silently moves things, because CSS has `margin: auto`, baseline alignment and
`flex-grow` with no Figma equivalent. So the plugin:

1. Builds the frame as auto-layout.
2. Compares each child's resulting position to the browser-measured position.
3. Over 1.5px, demotes that frame to absolute positioning and logs it.

`margin-left: auto` is the case that proves it: Chrome's `getComputedStyle`
reports the *used pixel value*, never `"auto"`, so it is undetectable from
styles. The first proposal lands ~1000px off, verification catches it, and
`SPACE_BETWEEN` recovers it exactly.

**Demotions in the log are the system working, not failing.** Do not present
them as errors.

## Reverse leg — Figma → code

With the Figma MCP server connected, `get_metadata` returns the live selection's
full geometry tree and `get_screenshot` returns a render. Note:

- The **local** Dev Mode server (`127.0.0.1:3845/mcp`) is **read-only** — 5
  tools — but reads the current selection with no fileKey.
- The **remote** server (`https://mcp.figma.com/mcp`) has ~26 tools including
  writes (`use_figma`, `generate_figma_design`, `create_new_file`).
- `get_design_context` **hard-fails** without a whitelisted directory — it
  refuses to return code at all, not just assets. Tell the user to add one via
  Dev Mode → MCP panel → Allowed directories.

## Report honestly

State plainly: which fonts were substituted, which assets are approximations,
what the geometry deltas actually are, and that the plugin output has not been
verified in real Figma unless it has. The verification is a mock; it does not
test real font metrics, vector import or image decoding.
