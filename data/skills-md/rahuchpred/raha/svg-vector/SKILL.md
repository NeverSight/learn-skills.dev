---
name: svg-vector
description: >-
  SVG Vector. Draw any object as a Linear-style isometric line illustration
  (the Fig 0.1 to 0.3 figures on linear.app), as plain inline SVG with
  Linear's motion. 2:1 isometric, solids filled with the page colour and
  painted back to front, a silhouette / crease / lip line hierarchy at 0.5px,
  background fog for depth, dot-matrix loaders on faces, hover lifts and a
  pointer wave on a spring. Use whenever the user asks for an isometric
  illustration, an iso line drawing, "those Linear (or Modal) feature
  vectors", a feature-row figure, a technical line drawing of a product or
  object, or wants any object drawn in that style. Input is the object; output
  is a scene file, its SVG, and wired motion.
---

# SVG Vector

Linear's feature figures are not 3D. They are inline SVG drawn by React:
each solid is its own silhouette filled with the page colour, painted back
to front so nearer solids hide farther ones, then outlined in three tones
of grey at half a pixel. Motion is a CSS transform transition, CSS
`steps()` keyframes, and one framer-motion spring rewriting path data.
`reference/linear-notes.md` has every number as shipped.

This skill is an engine that does the same for any object you can build
from convex solids.

| File | What it is |
|---|---|
| `reference/iso.js` | **The engine.** Primitives, projection, sorting, line tones, fog, decals, dot grids, `render()` to an SVG string. Zero deps, Node or browser. |
| `reference/iso-motion.js` | `liftStack` (Fig 0.1), `pointerWave` (Fig 0.3), `spinObject` (globes), `hoverMove` (fans, presses, slides), `springField` (any solids springing to pointer-driven values). Dot grids and pulses need no JS. |
| `reference/examples/*.mjs` | Scenes: Linear's three figures rebuilt; Fig 0.4 to 0.8 (triage, command, rack, sync, insights) each with its own hover motion; database, laptop, chart, chip, earth. Each exports `default` (the scene), optional `meta` ({ fig, title, text }) and `motion(svg)`. Start from the closest one. |
| `reference/data/land-dots-{3,4}.json` | Land as `[lat, lon]` points every 3 or 4 degrees (Natural Earth 110m, public domain). `tools/land-dots.mjs` regenerates them from any land GeoJSON. |
| `reference/render.mjs` | `node render.mjs scene.mjs [--theme light] [--out x.svg]` |
| `reference/gallery.mjs` | `node gallery.mjs out.html [--big] [--only a,b] [--row a,b,c]`: examples in both themes with motion live; `--row` lays them out as a Linear feature row (FIG label, art, title, text). Use it to check work. |
| `reference/IsoFigure.tsx` | Next.js mount: SVG string plus client motion. |
| `reference/tools/record.mjs` | A demo video: a title card, then the figures. Default `--layout sequence` is square (1080x1080) and shows one figure at a time: it fades in, a scripted cursor plays its gesture, it fades out. `--layout grid` is 16:9 with all figures at once. `PROBE_AT`/`PROBE_JS` print a page value at a moment, for debugging. `--byline` adds a quieter second line under the title. `--music [drift|rain|dusk]` mixes in an original lofi bed from `tools/lofi.mjs`, synthesized so it is free to post. `drift` (default) is the calm one and suits these figures: felt piano with slow attacks, a muffled kick, brushed swells, a smooth rain wash, dark and quiet. `rain` (plucks, rimshot, shaker) and `dusk` (electric piano, kick and snare) are busier. The user found sharp transients (plucks, clicks, shakers, drops) too aggressive under slow line art, so keep the music soft and change preset or `--seed` between videos. Frame-exact (an injected clock drives rAF, CSS and Web Animations), piped into ffmpeg. Needs `puppeteer-core` and ffmpeg; usage at the top of the file. Scenes can export `targets` (world points per item) for the cursor. |
| `reference/linear-notes.md` | The reverse engineering: paths, palette, CSS, constants. |

## 1. The look (keep all of these)

- **2:1 isometric.** World x runs right-down, y left-down, z up. The seen
  faces are always +x (right), +y (left), +z (top). `ZS = sqrt(1.5)` is the
  true vertical scale.
- **Occlusion by fill.** Every solid's silhouette is filled with `--iso-bg`,
  which must equal the page background. A transparent page breaks the trick.
- **Three tones, one weight.** Silhouette `hi`, creases `lo`, lip `faint`,
  all 0.5 viewBox units. Render near 1:1 so 0.5 lands as one retina pixel.
  One or two solids may go `mid` or `lo` to push them back; never add a
  fourth weight or a coloured stroke.
- **The lip** (`bevel`) is what makes it read as Linear rather than a
  wireframe: a faint line just under the top-front contour.
- **Rounded corners**, small. `radius` 4 to 8 on a 120 unit slab.
- **Fog** (`fog: 6..16`) on a solid that sits in front of others. It fades
  the lines behind it near its edge.
- **One gesture per figure.** Each figure does exactly one thing on hover
  (lift, fan, press, slide, rise, turn, send). Never stack independent
  effects. A Sync figure with four dot grids looping on their own plus
  looping pulses was rejected; the single-gesture figures were "amazing".
- **Dot grids are detail, not a second effect.** Keep them: like Linear's
  cubes, a still grid on a top (frame one, a dot or two lit) makes a figure
  feel finished, and stripping them all left Sync "really empty". What is
  wrong is a grid looping on its own. Use `grid({ once: true, frames, delay })`:
  still at rest, played once by `playGrids()` as part of the figure's one
  gesture (timed to the arrival, the press, the lift), reset by
  `resetGrids()` on leave. A globe's land dots are texture and are fine.
- **Restraint.** 1 to 15 solids. The figure is a still life, not a diagram.
  No labels inside the art, no arrows, no colour except Modal-style node
  markers if the user asks.

## 2. Workflow

1. **Name the object and decompose it** into convex solids (table below).
   Concave shapes are several convex parts. Sketch the plan on a grid in
   world units; 100 to 150 units across is the usual scale.
2. **Write a scene module** in `examples/` style: `export default { objects: [...] }`.
3. **Render and look**: build the gallery (`node gallery.mjs <scratch>/g.html --big`),
   serve it, screenshot both themes. Check occlusion first, then tones,
   then proportions.
4. **Add motion** only if the figure earns it (section 5).
5. **Integrate**: inline the SVG string, or `IsoFigure.tsx`. Set the
   theme tokens from the page (section 6).

## 3. API in one screen

```js
import { render, box, cylinder, prism, ngon, rect, circle, line, marker } from './iso.js'

box({ at: [x, y, z], size: [w, d, h], radius, round: 'z'|'x'|'y', ... })
cylinder({ at, r, h, axis: 'z'|'x'|'y', ... })          // at = min corner of its bounds
prism({ at, outline: ngon(6, 18, 2), h, axis, ... })     // any convex outline in local (u, v)
sphere({ at: centre, r, rot, tilt, graticule: { lat, lon }, dots: [[lat, lon]], dotR,
         rings: [{ r, incline, lean, markers: [deg] }], fog })
line({ points: [[x,y,z], ...], dash: true, tone: 'lo', pulse: { len, dur, delay } })
marker({ at: [x,y,z], size: 2.5, color })                // Modal-style node square

render({ objects, theme: 'dark'|'light'|{...}, pad: 16, stroke: 0.5, uid })
```

Shared solid options: `item` (hover target index for `hoverMove`), `bevel` (lip depth), `fog` (blur), `tone: { edge, crease, base }`,
`xray` (hidden edges dashed, a blueprint read), `decals: [{ face, svg }]`,
`grid: { face, n, gap, r, at, frames, interval }`, `id`, `lift`, `order`.

- **Faces** for decals and grids: box `'+z'` top, `'+x'` right, `'+y'` left;
  any prism `'cap'`. Face-local coords: on `'+x'` and `'+y'` u runs
  left to right and v top to bottom, origin at the face's top-left; on
  `'+z'` u runs along x, v along y, origin at the back corner. A decal is raw SVG in those units (lines and
  circles; it inherits the `lo` stroke).
- **Sorting** is automatic and exact for solids whose bounds do not
  interpenetrate. If any object sets `order`, the whole scene sorts by it
  instead; use that only when lines must sit between solids (Fig 0.1).
- **Spheres** are the one non-prism. `rot` is the longitude facing the
  viewer, `tilt` leans the axis in the picture plane, east is to the right.
  `dots` become foreshortened discs that fade into the limb. A ring's back
  half is painted dashed before the globe and its front half after, so the
  globe hides what it should. Sorted by their bounding cube.
- **Nothing moves at rest.** `render({ playOnHover: true })` is the default: dot grids and
  pulses hold still (pulses hidden) until the figure is hovered or has `.iso-active`.
  `FRAMES.scan/ring/fill/rain/beat(n)` are ready-made dot-matrix frame sets.
- **`overflow="visible"`** is set on every SVG so moving parts are never clipped; give a
  scene `pad` when its motion travels far (triage uses 44).
- **Theme** colours are CSS variables (`--iso-bg/hi/mid/lo/faint/dot`) with
  the theme as fallback, so the page can retune them.

## 4. Decomposing objects

| Object | Parts |
|---|---|
| Stack, layers, a platform | `box` slabs, same plan, `H` apart; lid lifted with dotted `line`s in the gap |
| Database, storage | 3 `cylinder` discs, top one lifted and fogged, dot grid on its `cap` |
| Server, rack | tall `box`, thin `box` drawers on its `+x` face (`decals` for slots) |
| Chip, hardware | substrate `box` + die `box` + `ngon` core, pin `box`es on all four edges |
| Laptop, device | base slab, thin standing lid (`round: 'y'`), screen as a `+y` decal |
| Phone | thin `box` with `radius` 8 standing on `round: 'y'`, screen decal |
| Chart, growth | plinth + `box` bars, the last one `hi`, the rest `mid` |
| Speed, momentum | thin standing plates in a row, heights as a curve; `pointerWave` |
| Team, agents, many | cubes clustered with gaps, fog on each, dot loaders on some tops |
| Document, page | very thin `box`es fanned with small offsets |
| Earth, globe, global | `sphere` with `data/land-dots-3.json`, a ring with a satellite marker, floating over a plinth with a dotted axis (`examples/earth.mjs`) |
| Network, nodes | `cylinder` puck + `marker`s + dashed `line`s between them |
| Gear, hex, bolt | `prism` with `ngon` outline; teeth as small `box`es around it |

Rules of thumb: put the hero solid nearest the viewer (largest x + y), give
it `fog`; keep gaps between parts at least 6 units so lips stay legible;
thin parts (h under 2) skip `bevel`.

## 5. Motion (all hover-driven: nothing moves at rest)

| Effect | How | Use when |
|---|---|---|
| **Stack lift** | `lift: index` on the layers (0 = top), then `liftStack(svg, { step: gap * ZS, max })`. CSS does the move: `.7s cubic-bezier(.32,.72,0,1)`, `0.05s` stagger. | Layers, versions, opening something |
| **Dot matrix** | `grid: { frames: ['○ ● ...', ...], interval: 200 }`. Pure CSS `steps()`. | Something alive, thinking, loading |
| **Globe spin** | `spinObject(svg, { id, make: (rot) => sphere({...}), rot, speed: -24 })`. Still at rest; hover eases it into a spin, leaving eases it to a stop (Linear's figures only move under the pointer). Grab and fling any time. Patches the existing dots and graticule each frame (about 3ms), never rebuilds markup. | A globe, anything round that should feel touchable |
| **Fan** | `item: i` on the solids, `hoverMove(svg, { mode: 'all', offset: (i) => [dx, dy], stagger })`. | A stack opening, options spreading (Fig 0.4) |
| **Press** | `hoverMove(svg, { mode: 'each', offset: (i, a) => i === a ? [0, d * ZS] : null, transition: 'transform .16s ...' })`. Float caps on stems so the press has travel. | Keys, buttons (Fig 0.5) |
| **Slide out** | `hoverMove` mode `'each'`, offset `[s, s / 2]` (s along +x). Wrap the items in a case (side panel + lid) so the opening reads as a slot. | Drawers, servers, files (Fig 0.6) |
| **Send** | `line({ pulse: { once: true, dur, delay } })` per link, `sendPulses(svg)` on pointerenter, plus `hoverMove` mode `'all'` lifting each receiver with `stagger` = its pulse's delay + travel. Receivers' still grids `playGrids()` into a check at the same moment; `resetGrids()` on leave. One pass per hover, no loop. Order lines between the solids they join. | Sync, delivery, a message reaching many (Fig 0.7) |
| **Spring field** | `springField(svg, { count, make, rest, target: (i, p, proj) => v })`. Pointer in viewBox units; project each solid's base to measure distance. | Terrain, heatmaps, any 2D response (Fig 0.8) |
| **Pointer wave** | Solids with `id: 'p0'..'pN'`, a `make(i, h)` factory, then `pointerWave(svg, { rest, make })`. Spring stiffness 100, damping 18. | Speed, response, a curve that reacts |

All of them honour `prefers-reduced-motion` (lift jumps, grids hold frame
one, the wave stays at rest, the globe ignores hover but can still be dragged). On touch there is no hover; the art must
stand without its motion.

## 6. Integrating

- Inline the SVG; never an `<img>` (the CSS variables and motion need DOM).
- Map tokens to the page: `.figure .iso-root { --iso-bg: var(--paper); --iso-hi: ...; }`.
  For a light page start from `THEMES.light` and nudge to the page's greys.
  The `bg` token must match the surface the figure sits on exactly.
- Size: `max-width: 100%; height: auto`. Keep render width near the
  viewBox width so strokes stay hairline.
- On raha's site, craft pieces follow `AGENTS.md`: site tokens for the
  page, `PieceLayout`, both themes, phones, reduced motion.

## 7. Pitfalls

- A concave outline (L, ring, star) fills its convex hull. Split it.
- Two solids whose bounds overlap in all three axes sort unreliably. Nudge
  them apart by 0.01 or use `order`.
- `fog` on every solid in a dense scene muddies it. Front solids only.
- Do not copy Linear's path strings or art into a product; the engine
  rebuilds the style from primitives.

## 8. Testing motion

- `hoverMove` items get static invisible hit copies (`.iso-hit`) of every
  solid in paint order, so the pointer lands on the solid you can see; non-item
  solids (a case, a lid, stems) are blockers. Verify with
  `document.elementFromPoint` at the centre and corners of each item's visible
  face: it must return that item's `data-i`. Trigger them in tests with
  `svg.querySelectorAll('.iso-hit [data-i]')[k].dispatchEvent(new PointerEvent('pointerenter'))`.
- CSS-gated motion: add `.iso-active` to the SVG and read `animationPlayState`.
- JS motion in a hidden browser pane: `requestAnimationFrame` stops and
  timers are throttled to about 1s, so swap in a manual frame pump with a
  fake clock (queue the callbacks, run them with `now += 16.67`) before any
  pointer event reaches the figure.
