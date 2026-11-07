---
name: 3d-paper-material
description: Build a paper sheet in Three.js that reads as paper up close — washi, cotton rag or kraft with baked fibre and tooth relief, laid and chain lines, a torn deckle edge with frayed fibres, four-layer thickness, a rolled corner and crease, ink that wicks along the fibres, toasted aged edges, contact shadows and back-lit translucency. Use for a hung sheet, scroll, page, label, shoji pane or card that must survive a macro close-up, or when paper looks like a flat white plane, has ruler-straight edges, no thickness, or does not glow when lit from behind. Use 3d-wood-material, 3d-cloth-material or 3d-metal-material for those materials, and paper-cinder-transition for burning paper.
---

# 3D Paper Material

Paper is a fibre field cut out by a torn outline: a height map of laid fibres and formation clouds gives the surface, an alpha mask with pulled-out fibres gives the edge, offset copies give the thickness, and the back light is transmitted by how thin the formation is at each pixel. Drop any one and the sheet is a white plane.

Reach for `paper-cinder-transition` when the paper burns or is revealed by fire; this skill is the unburnt sheet. It is a hung or laid sheet in a scene. A page-turning book needs a bend rig this skill does not provide.

Read `demo.html` for a working build: MeshPhysicalMaterial patched with `onBeforeCompile`, maps baked once into half-float targets, masks painted with Canvas 2D. Its `NOISE` GLSL, formation, kozo-fibre and bark-fleck expressions, back-light transmission, `tearLine` and the fray loop are ported unchanged from the Kibori workshop page (`kibori.html`, `washiMat`, `footTear`).

## The pipeline

1. **Bake fibres (GPU, once).** One full-screen pass writes `R height, G formation, B fibre, A fleck` to a half-float target. Height is `0.5 + fibre*0.34 + (tooth-0.5)*0.1 - fleck*0.2 - crease*0.55`. Keep `samples: 0` on the target and mipmaps on.
2. **Warp the lattice.** Domain-warp the fibre coordinates by 0.014 unit and rotate them by `(gnoise(q*2.1)-0.5)*1.5` rad. Add a finer, fainter fibre set at 2.7x frequency (max 0.55).
3. **Paint the mask (Canvas 2D, on stock change).** `R` thin strip inside the tear, `G` silhouette plus fray fibres, `B` ink with a low-alpha bleed halo, `A` the silhouette blurred by a shadow drawn off to the side (edge age). Read back with `getImageData` and write into a `DataTexture`, rows flipped, alpha as data.
4. **Shape the sheet.** A 168 x 240 plane: hung bow, a mountain crease, pin dimples, and a cylinder roll (radius 0.23, angle `2.6*curl`) that keeps length. Add three copies offset along the normal by `thick/3`, `2thick/3`, `thick`.
5. **Shade.** Albedo from formation and fibre, ink over it, toast and foxing by the age mask. Height goes through a world-unit bump (see gotchas). Alpha is coverage, not a cut.
6. **Transmit.** `emissive += L * tr`, where `tr = 0.74 + (0.5-form)*0.85 + (0.5-lowfbm)*0.45 - fibre*0.22 - fleck*0.45`, times stock gain, plus the thin strip, minus ink. `L` is the garden behind: sky, sun patch, black bamboo stems sampled through a mip bias of 1.4.
7. **Macro.** Re-bake a second height target and mask over a 0.5 unit window at the focus point and blend it over the base by window edge. Never tile a small texture.

## Constants that landed

| | washi | cotton rag | kraft |
| --- | --- | --- | --- |
| tint | `#f0e8d2` | `#f0eee6` | `#a88f70` |
| fibre lattice A / B (per unit) | 1.9x54 / 44x2.3 | 15x17 / 16x14 | 7x26 / 26x7 |
| fibre relief, bump height (unit) | 0.55, 0.0017 | 0.32, 0.0024 | 0.8, 0.0034 |
| tooth freq, amp | 230, 0.09 | 430, 0.17 | 300, 0.20 |
| laid lines /unit, amp, chain | 110, 0.28, 0 | 150, 0.55, 0.5 | none |
| tear amplitude (T,R,B,L), fray scale | 64,72,60,76; x12 | 3,58,3,54; x6 | 96,3,4,3; x8 |
| thickness (unit), transmission | 0.0045, 1.0 | 0.0085, 0.42 | 0.011, 0.16 |
| roughness, sheen | 0.93, 0.4 | 0.9, 0.25 | 0.96, 0.10 |

Scale: 1 unit = 134.8 mm (A4 is 1.55 x 2.2). Base bake 990 px/unit = 7.3 px/mm; macro window 1536 px over 0.5 unit = 22.8 px/mm. Tear samples 3400 per unit. Camera 28 degree FOV; macro distance 0.46-0.50.

## Rules and the failure each prevents

- **Cut the outline from four independent tear lines, never a rectangle with a wobble.** A single sine or noise edge reads as a CSS wave; `tearLine` runs straight, turns, runs again. Give cut sides amplitude 3-4, torn sides 60-100.
- **Pull fibres past the edge and paint them as partial coverage.** A hard alpha edge reads as scissors. Fibres are 0.3-0.7 px wide at 30-75% alpha; on a dark wall they show as pale hairs.
- **Stack three offset copies behind the front layer, tinted 0.8-0.94 of the paper.** One quad has no thickness and shows nothing side-on. Keep the offset at 0.0045-0.011 unit; more reads as cardboard.
- **Warp and rotate the fibre lattice.** Two orthogonal ridged families read as scratched glass or a crosshatch, especially raking-lit.
- **Drive transmission from the same fields as the albedo.** A flat emissive constant reads as a lamp inside a card; thin formation must glow, fibre bundles and ink must hold light back.
- **Fade the toast band to zero beyond the edge.** Toasting the fray turns pulled-out fibres brown-black against a dark wall.
- **Bleed ink with a halo below the ink threshold and let fibre and formation carry it over.** A blurred halo alone is out-of-focus ink; `smoothstep(0.62,0.85, halo + fibre*0.4 + (0.5-form)*0.5)` wicks along strands. Guard the term with `smoothstep(0.03,0.16, halo)` or fibres far from any ink go black.
- **Round the bark flecks.** Kibori's cell hash gives squares at macro; multiply by an ellipse `smoothstep(0.5,0.12,length((fract(q*cell)-0.5)*vec2(1,1.9)))`.
- **Bake a window for macro.** A base map at 7 px/mm turns to fog at 22 px/mm; a tiled 512 px paper tile shows its seam.

## Gotchas, symptom first

- **Fringe fibres vanish or a solid black fringe appears beyond the edge.** `alphaTest` cuts anything under 0.5. Use `alphaToCoverage: true` with `alphaTest` 0 and antialias on; four MSAA samples dither the partial alpha. Give the shadow depth material its own `alphaMap` and `alphaTest: 0.5`.
- **A big black hairy shape beside the paper is not a bug.** It is the sheet's shadow on the wall. Light the wall with a fill or a faint emissive so the shadow reads brown.
- **Relief looks stronger far away and vanishes in macro.** three's `perturbNormalArb` normalises the surface derivatives, so slope depends on pixel size. Replace `bumpmap_pars_fragment` with the un-normalised Mikkelsen form and give the height in world units.
- **Edge-age or ink texture arrives premultiplied and dark.** Never upload data through a canvas texture with alpha. Merge four canvases through `getImageData` into a `DataTexture` (rows reversed, `flipY` false).
- **A blurred edge band is missing on Safari.** `ctx.filter` is unreliable; draw the shape offset by 20000 px with `shadowOffsetX = -20000` so only its blur lands.
- **Half-float target resolves to blocky tiles.** MSAA on it; use `samples: 0`.
- **The rolled corner shows nothing.** Face-on, a 65 degree roll is foreshortened; sway the camera by 0.3 unit at distance 6 or rake the key to about 54 degrees.
- **Fibre swirls read as marbling at overview.** The rotation field is too strong; 1.5 rad is the cap, 1.9 reads as floral.

## Playback and lifecycle

The demo idles with a slow camera sway; `prefers-reduced-motion` renders one composed still and only re-renders on control input. It pauses on `document.hidden` and resets its time base on resume, clamps `dt` to 1/30 s, caps device pixel ratio at 2, sizes from a `ResizeObserver`, and eases back-light and macro with `1 - exp(-dt*k)`. Controls are real radios, checkboxes and ranges with focus rings and a live status line.

## Cost (measured, 1440x900 headless Chrome on Metal, DPR 1)

Idle sway about 85 fps; 325k triangles in 7 draw calls (front plus three layers is 4x81k); stock switch rebuilds in about 320 ms (masks 4 canvases, bake, geometry); macro window in about 150 ms. GPU memory about 100 MB (base target 40, macro target 25, masks 33). What costs: the four mask canvases and the tens of thousands of fray strokes. What does not: the bake pass and the normal taps. The cheap lever: base density (`PPU_B`); 660 px/unit halves memory and keeps overview sharp.

## Provenance

Extracted from the Kibori 木彫 launch page, where washi is the back-lit shoji panes, the torn footer sheet and the paper lantern; this build restages those generators on one sheet with a macro mode.

## Self-score against the anchored rubric (0 = flat plane, 5 = tileable noise texture, 8 = directional fibre with real edge, 10 = passes a macro test against a photograph)

| item | score | why |
| --- | --- | --- |
| fibre structure | 8 | warped, rotating strands, two scales; no fibre cross-overs in depth |
| deckle edge | 8 | four independent tears, fray fibres, feather strip; fibres do not shadow |
| thickness | 6 | three stepped layers; steps show at extreme rake, no cross-section fibres |
| translucency | 8 | formation-driven, stems, amber sun patch; no scattering blur by thickness |
| curl and crease | 6 | roll is convincing, crease reads faint at overview |
| ink | 6 | fibre wicking narrow; no pooling at stroke ends |
| aged edges and shadow | 6 | toast and foxing good; shadow on the wall is a hard shape |
| texel density | 8 | 22.8 px/mm in macro, 7.3 px/mm overview |
