---
name: specimen
description: Use when someone asks for a Specimen icon, runs /specimen, or wants a 3D product icon — a glossy object on a soft tile, lit like a piece in a display case, looping, in a dark and a light theme — for a feature grid, a landing page, a changelog or an empty state, shipped as video or as a live element with nothing to install.
---

# Specimen: make an icon

You are making one Specimen icon: a single glossy object on a soft rounded tile, lit like a piece in a display case. The colour arrives only as light. It loops without a jump. From one piece file it ships in a dark and a light theme, as path traced video or as a live raster element.

The pieces in `examples/` are the bar. Read the one closest to the request before you write anything. If what you make would look out of place next to them, it is not done.

You write one thing: the piece file, `<name>.specimen.js`. The tile, the studio, the lights, the post, the themes, the path tracer, the denoiser and the encode are fixed and live in `runtime/`. Never edit `runtime/`, never paste a changed copy of it, never re-implement what it already does. If you think the runtime is missing something, tell the person instead of working around it.

Every file named below is in this skill's folder. The piece is written in the person's working directory (or where they say); media goes where they say (`public/icons/`, …) or beside the piece, prefixed with the icon's name. Never create a folder of your own in their project. Run the scripts from there, by their path in this folder.

Specimen is only this skill. There is no npm package and no install step. Never run `npm install`, never add a dependency to the person's project, never import `three` in the piece: it gets everything through `ctx`.

### The skill folder

```
specimen/
  SKILL.md          this file
  concepts.md       objects that read well, metaphors by product area, what failed
  package.json      { "type": "module" }, so Node reads this folder's scripts the same under any project
  render.mjs        piece → webm + mp4 + poster per theme (video), or runtime + piece + posters (--live)
  sheet.mjs         contact sheet: raster frames, a dark row and a light row per piece; --pt, --guide
  validate.mjs      the measurable rules (section 5)
  piece.mjs         reads a piece in Node: its name, its syntax errors with the line, the contract
  session.mjs       opens a piece on the runtime page in headless Chrome
  cdp.mjs           Chrome finder, a minimal DevTools Protocol client and a static server
  runtime/          fixed — never edited
    specimen.js     the bundle: three (WebGPU), the path tracer, the denoiser, the stage, <specimen-icon>
    weights.tza     the denoiser's weights
    THIRD_PARTY_NOTICES.md  the bundled packages' and the weights' licences; --live ships it as specimen.js.LICENSE.txt
    page.html       the page render, sheet and validate load a piece into
  examples/         the reference pieces (section 7)
```

The scripts run with plain `node` (22 or newer) and use only Node built-ins. They drive the Chrome already on the machine (or `SPECIMEN_CHROME`), and video needs `ffmpeg`. If one is missing, the script names it: tell the person exactly what is missing and how to get it (`brew install ffmpeg`); don't install anything on your own.

---

## 0. Delivery

Ask this first, in one message, before any concept:

> **Video** (default) — path traced, `<name>-dark.webm/.mp4` and `<name>-light.webm/.mp4` with a poster each, and a `<video>` snippet. The best look, a few hundred KB per theme, plays everywhere.
> **Live** — `specimen.js` (with its licence file) and the piece copied into their static folder, a poster per theme, and a `<specimen-icon>` snippet. It is raster, not path traced: softer reflections, no denoiser. Say so plainly. It needs WebGPU and falls back to the poster without it or with reduced motion.
> **Both** — video by default, live on top only where they turn it on.

Both themes are rendered unless the person asks for one. Also ask where the files go; if they don't say, put them beside the piece. If there is nobody to ask, take video, both themes, beside the piece, and say so.

### Size

Render at the size the icon is shown at: a video stretched past its pixels goes soft at the edges, and no encode setting gets them back. Find the width first in the project, in the CSS or component the icon goes into, at its widest breakpoint. Ask only when you can't tell, in the same message as the delivery:

| shown at (CSS px) | `--size` | video | per theme |
|---|---|---|---|
| up to 160 | 384 | 320 px | ~4 min |
| up to 320 | 768 | 640 px | ~17 min |
| up to 480 | 1152 | 960 px | ~36 min |

The video has to be at least twice the CSS width for retina screens, and it comes out at 5/6 of `--size`: take the first row that covers the width. Wider than 480: `--size` is 2.4 × the width rounded up to a multiple of 12, and the time grows with its square. For live, the size only sets the posters. If there is nobody to ask and nothing to read, take 768 and say so.

## 1. Concept

Read `concepts.md`. Offer two or three concepts, one line each:

> **Name.** The object · what moves · where the accent lives · the finishes.

Example:
> **Bolt.** A thick soft-bevelled lightning bolt · a charge of light runs down through it twice per loop and pools in the tip · the charge and the pool under the tile · gloss body.

Then suggest two or three palettes for the accent, the one colour the icon carries, and let the person pick or name their own:

> **Palette.** Cyan `#22d3ee` (a cool, technical read) · amber `#f59e0b` (warm, an alert) · neutral `#a1a1aa` (no colour at all: the object reads by its finishes alone).

The colour is the person's call: their brand, their section, their grid. Suggest from the product area (security reads cool, alerts warm, a monochrome grid neutral) and from the icons already beside it on the page; never pick one silently. The palette sets `scene.accent` and, if they want a different emission, `scene.glow`.

Wait for the person to pick. Skip this only when they arrived with the object and the motion already chosen. If there is nobody to ask, take the concept with the clearest silhouette and say which one you took.

What makes a concept good:
- **One object, one idea.** A concept that needs a caption is not one yet.
- **Silhouette first.** Squint: if the outline alone doesn't say what it is, change the object.
- **The object means something in the product.** Auth gets a lock, alerts a bell. See `concepts.md`.
- **One motion that tells the story,** small and slow: a turn, a swing, a charge, a pulse. Not three things at once.

## 2. Read the closest example

Open the example in `examples/` nearest to the concept and read it whole. Copy its structure: the `scene` block, how it builds geometry with `geo.*`, how its `update(phase)` keeps every term periodic.

## 3. Write the piece

An ES module with two exports and no imports:

```js
export const scene = {
	accent: '#38bdf8',              // the piece's only colour, always as light (a Tailwind 500 reads well)
	glow: '#7dd3fc',                // optional: the colour of its emission; default is the accent a step lighter
	duration: 8,                    // seconds, 4–12; the loop must not jump
	fit: { scale: 0.9, x: 0, y: 0 },// optical fit into the 58% safe area (section 4)
	lights: { tint: 0.45 },         // optional: accent, rim, under, underFill, floor, tint, strips
};

export function object( ctx ) {
	// build with ctx.mat.*, ctx.geo.*, ctx.texture()
	return { mesh, update( phase ) { /* phase runs 0 → 1 once per loop */ } };
}
```

### `ctx`

| Key | What it is |
|---|---|
| `THREE` | the bundle's three instance; the piece never imports three |
| `mat` | the material roles below, resolved by the current theme |
| `geo.roundedRect(shape, w, h, r)` | a rounded rectangle on a `Shape` or `Path` (holes); `w`, `h` are half extents |
| `geo.bevelExtrude(shape, { depth, bevel, segments, curveSegments })` | a shape extruded with soft rounded edges, centred on z = 0 |
| `geo.lathe(profile, segments)` | a profile of `[x, y]` pairs revolved around +Y |
| `geo.planarUV(geometry, w, h)` | uv 0..1 across `[-w, w] × [-h, h]`, for the dynamic texture |
| `texture(w, h)` | the one dynamic texture: `{ tex, draw(fn(u, v) → [r, g, b]) }`. Pass `tex` as `emissiveMap` to a role and call `draw` in `update`. A second call throws: the path tracer holds one dynamic texture per object. Details below |
| `gradient(stops, { srgb })` | a static vertical gradient, stops `[t, css colour]` from top (0) to bottom (1); for flames and trails |
| `accent`, `glow` | the two colours as `THREE.Color`, for the texture's `draw` |
| `theme` | `'dark'` or `'light'`, read only; a last resort |
| `TAU`, `bump(x, c, w)`, `smoothstep(x, a, b)` | animation helpers: `bump` is a gaussian `exp(-((x − c) / w)²)`, 1 at `c` and near 0 past `2w` (never exactly 0); `smoothstep` rises 0 → 1 between `a` and `b` |

### Space and size

The tile is 2 × 2 units, centred on the origin, facing the camera (+x right, +y up, +z towards the camera). The safe box is 1.16 units square (58% of the tile), centred at y = +0.04. Build the object about 1.0–1.3 units wide and at most ~1.6 tall, centred on its own origin, at `z ≈ 0.45`: the examples are this size at `fit.scale` 0.8–0.9.

`scene.fit` wraps the object in a group: `scale` multiplies it about the world origin (it does not re-centre), and `x`, `y` move it in world units (`y: -0.08` is 4% of the tile down). Nothing centres the object for you: if it sits off centre on the sheet, centre its geometry first (`geometry.center()`, or move the parts inside a group), then tune `fit`.

Thickness that reads at 64 px: tubes and rods of radius 0.12 or more, bevels of 0.05 or more. The key light is a soft box above and to the right, so a negative `rotation.y` (around −0.3, which turns the object's right side towards the camera) catches it on the bevels.

### The dynamic texture

`draw(fn)` calls `fn(u, v)` once per texel, with `u` and `v` in 0..1 across the texture (`v = 0` is its first row), and the texture is read through the mesh's own UVs. Extrusions and flat shapes need `geo.planarUV(geometry, w, h)`, which maps `v = 0` to the bottom (y = −h) and `u = 0` to the left. A lathe, a tube or a sphere already has UVs (a `TubeGeometry`'s `u` runs along its path). Return linear colour in 0..1: values are clamped, and `emissiveIntensity` (the bolt uses 3) scales them. Use `glow.r * k, glow.g * k, glow.b * k` with `k` in 0..1, and keep a dark base (`k ≈ 0`) where the body should stay black. `texture(256, 16)` is enough for a band along a path, `128 × 128` for a face: `draw` runs on the CPU every frame.

### Material roles

Every material comes from `mat.*`. Never construct one (`new THREE.MeshStandardMaterial(…)` fails validation): a hand-made material has one colour, and the light theme needs another.

| Role | Dark | Light | Use it for |
|---|---|---|---|
| `mat.body(o)` | glossy black | white glazed ceramic | the object's mass |
| `mat.chrome(o)` | chrome | chrome | rings, bands, hinges, the shackle |
| `mat.glass(o)` | dark glass | clear glass over a white core | dies, lenses, screens |
| `mat.inlay(o)` | black a step lighter | pearl grey | raised details on the body |
| `mat.glow(k, o)` | emission in the glow colour | the glow as surface colour, faint emission | badges, keyholes, a tip bead: one small lit part, never the mass |
| `mat.light(k, o)` | warm white glow | warm, faint glow | windows, portholes, flames |

`o` overrides physical values only: `finish`, `finishRepeat`, `roughness`, `metalness`, `clearcoat`, `normalMap`, `side`, `transparent`, `depthWrite`, `emissiveMap`, `alphaMap`, `emissiveIntensity`. Passing a colour (`color`, `emissive`, …) throws: the theme picks colours. A dynamic texture on `emissiveMap` emits in dark and becomes pigment on white ceramic in light, so the same `draw` works in both. A `mat.glow` part is the one place the accent shows as a surface in the light theme, which is why it stays small: a badge, a bead, a keyhole.

### Finishes

Every role takes a surface finish: `mat.body({ finish: 'brushed', finishRepeat: 5 })`. The finish sets the physical values (and, for the textured ones, a fine static map) and keeps the role's colour, so it works in both themes. Values the piece passes itself still win over the finish.

| Finish | What the light does on it | Good on |
|---|---|---|
| `gloss` | a mirror under clearcoat: sharp reflections of the studio strips | bodies that should read as lacquer |
| `matte` | no reflection, only soft form shading | skirts, cores, parts that must sit back |
| `brushed` | metal with fine lines: the highlight stretches into a streak across them | plates, frames, collars, a lock's body |
| `perforated` | metal with a grid of round holes, each catching its own glint | grilles, keycap plates, speaker faces |
| `speckle` | a rough field with sparse bright glints, like stone or sparkle paint | caps, keytops, a bell's body |

`finishRepeat` is how many tiles per UV unit (default 10). Extrusions have UVs in scene units, so the pitch is the same at any size; lathes and tubes run 0..1, so they want a smaller number (3–5). A fine finish reads as a material; a coarse one reads as a print (brushed lines too wide looked like wood grain).

The two thin strips that draw those crisp lines can be scaled with `scene.lights.strips` (0–1, default 1). Turn them down when a fine bevel sweeps through one as the object turns: the reflection is thinner than a pixel and flickers on and off across frames. The bolt uses `strips: 0`.

`validate.mjs` reads the source as text, so even a comment with `…Material(` in it fails `materials`.

### The craft rules

- **One object, one idea.** No second object, no props, no text.
- **Silhouette first.** It reads at 64 px or it doesn't read.
- **Polished light on every icon.** The studio has broad soft boxes and two thin hard strips: the strips draw crisp lines of light along bevels and edges. Give the icon at least two finishes so those lines change character across it (a gloss top over a matte skirt, a brushed frame around a speckled body). The icon should read by how its surfaces take the light, not only by its outline.
- **The accent only as light.** The body stays black (dark) or white (light). The accent appears as glow, as the pool under the tile and on the rim. Never paint a surface the accent colour.
- **Fit in the 58% box.** The solid mass sits in the safe area, centred a touch above the middle, and never comes within 4% of the tile edge. Use `scene.fit`, not the object's own position, to place it.
- **Loop without a jump.** Every term of `update` is a function of `phase · TAU` with integer harmonics, or a `smoothstep` envelope that is 0 at both ends of the loop. Phase 1 must look exactly like phase 0.
- **Light stays in the tile.** Glow and halos that spill past the tile edge fail validation.
- **Never edit `runtime/`.**

## 4. Sheet → read → fix

```
node <skill>/sheet.mjs <piece...> [--frames 0,60,120,180] [--guide] [--pt] [--out sheet.png]
```

It renders raster frames 0, 60, 120 and 180 (or `--frames`) as 256 px cells, a dark row and a light row per piece, with `--guide` drawing the 58% safe box in violet. `--pt` adds a fifth cell to each row: frame 0 path traced and denoised. A raster run takes a few seconds per piece; `--pt` adds about half a minute per piece. Pass an example after your piece to compare them row by row.

Read the PNG. Check: the silhouette reads, the mass sits in the box in every frame, the light row reads as well as the dark one (glow visible on white, nothing grey and muddy), the motion is visible across the frames. Fix and repeat until it would sit beside the examples. Run `--pt` at least once before the full render: the raster cells are brighter than the final, and a black part that reads in raster can sink into the dark tile once path traced. To inspect a detail at 256 px, sheet a throwaway copy with a larger `fit.scale` in the scratch directory, never in the person's project.

## 5. Validate

```
node <skill>/validate.mjs <name>.specimen.js
```

It prints each failed rule with its reason and a number, and exits 1 on any failure. Repeat until it prints `ok`.

| Rule | What fails it |
|---|---|
| `contract` | no `scene` or `object` export; `accent` not a hex colour; `duration` outside 4–12; `object()` throws or returns no `mesh` |
| `materials` | a `…Material(` constructor in the source |
| `seam` | raster phase 0 against phase 1 differs by more than 0.5 on average (0–255) |
| `fit` | the solid mass (the middle 90% of the object's silhouette, with transparent meshes such as flames and halos left out; opaque `mat.glow` parts count) leaves the safe box by more than 3% of the tile, or the whole silhouette comes within 4% of the tile edge, on frames at 0, ¼, ½ and ¾ of the loop |
| `light-in-tile` | anything outside the tile is more than 2/255 brighter than the page |
| `one-texture` | `texture()` called twice |

## 6. Render and hand over

Announce the time before you start, from the size table in §0: at `--size 768` it is about 4 s a frame on a recent Mac, so an 8 s loop (240 frames) is about 17 minutes per theme, about 35 for both. Live alone renders only the two posters, a minute or so. A video render outlasts any foreground command timeout, so run it in the background and watch its progress lines (`30/240 · 666 s left`, every 30 frames) until it prints the files; never run it in the foreground, where a timeout kills it halfway.

```
node <skill>/render.mjs <name>.specimen.js --out public/icons --size 768            # video, both themes
node <skill>/render.mjs <name>.specimen.js --out public/icons --live     # live
node <skill>/render.mjs <name>.specimen.js --out public/icons --live --video   # both
```

`--themes dark` renders one theme. It prints the files with their sizes and the snippet; the snippet's paths assume the folder is served at `/<folder name>`: set the prefix to where it is really served.

Hand over the files and the snippet, then ask whether the site follows the OS theme or has a toggle (`[data-theme]`). The printed video snippet follows the OS:

```html
<video autoplay muted loop playsinline poster="/icons/bolt-dark-poster.jpg">
  <source src="/icons/bolt-light.webm" type="video/webm" media="(prefers-color-scheme: light)">
  <source src="/icons/bolt-light.mp4" type="video/mp4" media="(prefers-color-scheme: light)">
  <source src="/icons/bolt-dark.webm" type="video/webm">
  <source src="/icons/bolt-dark.mp4" type="video/mp4">
</video>
```

For a site with a `[data-theme]` toggle, give two videos and the CSS that picks one:

```html
<video class="specimen-dark" autoplay muted loop playsinline poster="/icons/bolt-dark-poster.jpg">
  <source src="/icons/bolt-dark.webm" type="video/webm">
  <source src="/icons/bolt-dark.mp4" type="video/mp4">
</video>
<video class="specimen-light" autoplay muted loop playsinline poster="/icons/bolt-light-poster.jpg">
  <source src="/icons/bolt-light.webm" type="video/webm">
  <source src="/icons/bolt-light.mp4" type="video/mp4">
</video>
<style>
  .specimen-light { display: none; }
  [data-theme="light"] .specimen-light { display: block; }
  [data-theme="light"] .specimen-dark { display: none; }
</style>
```

Live:

```html
<specimen-icon src="/icons/bolt.specimen.js" poster="/icons/bolt-dark-poster.jpg" poster-light="/icons/bolt-light-poster.jpg"></specimen-icon>
<script type="module" src="/icons/specimen.js"></script>
```

`<specimen-icon>` follows `prefers-color-scheme` unless it has `theme="dark|light"` (set it from the toggle on a `[data-theme]` site), pauses off screen, and keeps the poster when WebGPU is missing or reduced motion is set: `poster-light` in the light theme, `poster` otherwise. Size it with CSS `width` (it stays square; 160 px by default).

Outside the tile every frame is exactly the page colour (black or white). On a section of another colour, blend it in: `mix-blend-mode: screen` for dark, `multiply` for light.

## 7. The bar

- **`examples/rocket.specimen.js`** — a rocket flying up-right, one barrel roll per loop; a flame from `gradient` that lights the tile; chrome band and nozzle; `mat.light` porthole.
- **`examples/bolt.specimen.js`** — a thick bevelled bolt; the one dynamic texture runs a charge down it and pools it in the tip.
- **`examples/bell.specimen.js`** — a lathed bell that rings twice per loop, a chrome clapper lagging behind; a `mat.glow` badge that pops when it rings.
- **`examples/lock.specimen.js`** — a padlock whose chrome shackle lifts and swings open once per loop while the keyhole lights; `fit.y` keeps the lifted shackle off the top.
- **`examples/chip.specimen.js`** — a chip with chrome pins on every side; a `mat.glass` die where square pulses of light, drawn through the dynamic texture, ripple outward twice per loop.
- **`examples/cube.specimen.js`** — a colourless puzzle cube: 26 cubies, every sticker a different finish of the same black (white in light), layers that snap a quarter turn four times per loop and close solved. The neutral palette: it reads by finishes alone.
- **`examples/key.specimen.js`** — a keyboard keycap on a perforated chrome plate, a speckled top over a matte skirt, a lit return-arrow legend; it presses twice per loop with a bounce while the light under it flares.
- **`examples/gears.specimen.js`** — two meshed chrome gears, the large one with lightening holes, that tick one tooth at a time four times per loop while the hub flares. Rotating parts with symmetric geometry keep plain chrome: a textured finish would turn with them and break the loop.

## 8. Never

- Never edit `runtime/`, and never ship a changed copy of `specimen.js`.
- Never construct a material or pick a colour in the piece; every surface comes from `mat.*`.
- Never call `texture()` twice, or import anything in the piece.
- Never run `npm install`, add a dependency, or create a folder of your own in the person's project.
- Never call live "path traced": it is raster.
- Never render before `validate.mjs` prints `ok`.
