---
name: 3d-wood-material
description: Build convincing timber for Three.js as one procedural MeshPhysicalMaterial with growth rings, cathedral figure, pores, medullary rays, checks, tool marks, end grain, and oil, wax, or lacquer finishes, so the grain follows the form and survives macro close-ups without image textures. Use for wood boards, benches, carved panels, tool handles, joinery, floors, and any request to make 3D wood look real, detailed, or less like a tiled photo or plastic.
---

# 3D Wood Material

**Mechanism:** one small periodic noise field, mip-filtered, is read at several different stretches and scales inside the fragment shader, so ring position, latewood, pores, fibres, rays and tool marks all come from the same wandering grain and feed colour, roughness and relief together, each fading out by its own screen footprint.

Boundary. This skill is the wood surface itself. For whole-scene light, rays and scoring wood renders, use `3d-wood-lighting-scorecard`. For image-based PBR sets (downloaded maps, texel budgets, KTX2 delivery) use `3d-high-resolution-textures`; reach for it when you need a photographed or scanned species. For silhouette, bevel and LOD geometry use `3d-high-poly-models`; this skill only needs a rounded arris (below). Cloth, metal and paper have their own siblings.

Run `demo.html` first (Kibori bench, four species, four finishes, macro views, and a switch that swaps in the failure). `PROMPT.md` recreates it.

## Recipe

1. **Patch, do not replace.** Build `MeshPhysicalMaterial({color:0xffffff, roughness:max(0.43,r), ior:1.43, specularIntensity:0.72})` and edit it in `onBeforeCompile`: `#include <map_fragment>` multiplies `diffuseColor` by the wood colour, `#include <roughnessmap_fragment>` sets `roughnessFactor=clamp(roughness*W.rough,0.35,1)`, `#include <normal_fragment_maps>` replaces the normal with a screen-space bump of the wood height `W.h`. Lighting, shadows, IBL and tone-mapping stay stock. The vertex stage only passes object-space position `vOP` and the object normal.
2. **Bake one field.** A 1024² `RepeatWrapping`, `LinearMipmapLinear`, `NoColorSpace` render target of periodic gradient noise (period 64, three octaves: `.r` base, `.g` fbm 0.60/0.27/0.13, `.b` a shifted copy). Reading it as `texture(p/64)` costs one tap. All timber shares it; per-board difference is a seed offset, not a texture.
3. **Grain axis.** `uAxis` 0/1/2 picks the log axis; `along` is that coordinate and `cross2` the other two. `endgrain = pow(|n·axis|, 6)` flips pores from streaks to open cells and dulls the colour on cut faces.
4. **Rings.** Drift the pith with two slow fields, `radius=|(cross2+(-drift, offAxis+0.48))*(1,0.56)|`, `growth=radius*ringFreq` plus fbm wobble (`±1.25` rings), `ring=floor(growth)`, `phase=fract`. Each ring draws its own width from `annual` noise: `lateWidth=0.065+annual*0.21`. Latewood is a steep `smoothstep(0.94-w, 0.97-w, phase)` cut off by `1-smoothstep(0.965,1,phase)`. Small `offAxis` gives cathedral arcs; large `offAxis` gives straight quarter-sawn lines.
5. **Detail layers**, each faded by its own footprint (`fwidth` of growth, `length(dFdx,dFdy)` of the pore, fibre and ray coordinates):

| layer | coordinates | strength |
| --- | --- | --- |
| pores (vessels) | `(fiberX*96, along*7.5)`, cells at end grain `cross2*88`, `smoothstep(0.59,0.75)` | tone +0.25, rough +0.19, height -0.42 |
| fibres | `(fiberX*230, along*2.4)` | tone -0.16, height +0.09, x0.25 at end grain |
| rays | `(across*13, along*115)`, `smoothstep(0.64,0.78)` | tone +0.26 towards pale, rough -0.075 |
| checks | curl.b `smoothstep(0.70,0.82)` x uChecks | tone toward `dark*0.68`, height -0.20 |
| knots | hash cell 1.85 x 4.6, 29% occupied, influence dies at the cell edge | tone +0.44 core, deflects fibres |
| tool marks | `(along*17, across*0.4)` | height +0.045 x uTool |

6. **Tone**: `tone=0.075+late*0.40+early*0.070+pores*0.25-fibres*0.16+(broad.g-0.5)*0.23+knotCore*0.44`, colour `mix(pale,dark,clamp(tone,0.035,0.83))`, then `*(0.93+annual*0.095+…)`. Roughness `0.91+late*0.13+pores*0.19+(broad.b-0.5)*0.20-rays*0.075+endgrain*0.14`.
7. **Bump, not normal map.** `bumpNormal` uses the derivative-based Mikkelsen bump and clamps the gradient to `0.38*|det|`, so a steep step never flips the normal. `uBump=bump*0.020`.
8. **Finishes are parameters, not textures.** Raw: `clearcoat 0`. Oil: `pow(rgb,1.16)` and `rough*0.88`, `clearcoat 0.10 / 0.55`. Wax: `clearcoat 0.22 / 0.38`. Urushi: luminance curve `pow(l,0.5)`, end grain darkened `*(1-eg*0.55)`, warm tint, worn arrises rubbed back to the pale colour, `clearcoat 0.42 / 0.40`.
9. **Round the arris.** `chamferBox` on every board, radius `min(w,h,d)*0.055` (at most 0.24 of any side), 3 to 5 segments, with normals set from the rounded corner. A sharp box edge has no highlight and reads as a cut-out.
10. **Give every board its own seed**, and keep it stable when species or finish changes (save and restore `woodMaterialSerial` around the build, seed `n*7.113`). Offset the geometry through the field (`woodBox(..., ox,oy,oz)`) so merged or shared materials still differ.

## Species constants (from the workshop)

| species | pale / dark | rough | grain | ringFreq | offAxis | notes |
| --- | --- | --- | --- | --- | --- | --- |
| keyaki | `#8a5f38` / `#3d2412` | 0.62 | 1.5 | 20 to 34 | 0.75 | rays 0.35, bump 0.10 |
| sugi | `#c8a579` / `#9b774d` | 0.58 | 1.8 | 8 to 30 | 2.8 | crisp latewood, tool 0.30 |
| hinoki | `#d8c096` / `#8a6b40` | 0.44 to 0.50 | 2.2 | 6 to 42 | 1.6 | close-grained, low contrast |
| kuri | `#6f4d2c` / `#2c1a0b` | 0.55 | 3.0 | 5 to 22 | 1.4 | rays 0.5, checks 0.10 |
| charred siding | `#1a1511` / `#0e0b08` | 0.97 | 0.8 | 9 | 0.55 | rays 0, checks 0.30 |

`ringFreq` is per unit of the model, so set it from real ring spacing (about 2 to 5 mm at the scale you are modelling) rather than copying a number between scenes: the workshop's 7 to 8 read as bold stripes at demo scale until raised to 20 to 42.

## Anchored failures

- **A repeated tile is visible at the second board.** A canvas tile with `repeat` prints identical rings on every board and shows its seam in a raking light. Sample object-space position, seed per material, offset geometry through the field.
- **Flat roughness looks like plastic.** Roughness must move with the grain: pores rougher (+0.19), latewood slightly rougher (+0.13), rays glossier (-0.075). A constant 0.3 gives a uniform bright sheen that never breaks along a ring.
- **Colour only, no relief.** Rings drawn only in albedo go flat when the light rakes. Feed the same `late`, `pores` and `fibres` into the height and bump it; and clamp the gradient or a hard ring edge turns the normal inside out.
- **Grain not following the form.** Take `along` from the member's real axis, not from UV. UV on a chamfered box stretches the pores at the rounded edge and turns a board into a stripe test. With object-space sampling the grain runs straight through corners and end faces switch pores to cells automatically.
- **Detail shimmers or crawls at distance and on grazing faces.** Every high-frequency layer must fade by its own screen footprint: `x *= 1 - smoothstep(a, b, fwidth-of-its-coordinate)`. Mip the field, and blend `late` and `early` toward their averages when `fwidth(growth)` passes `0.16..0.72`. Without this, rings moire into the wall of the board at 3 m.
- **Macro looks smeared, blobby, or a faint square lattice shows in the relief.** The 1024² field is being magnified past about 2,500 to 4,000 px per unit at `grain 1.0`: bilinear texel edges leak into the bump derivatives as a grid, pore cells go soft and ring edges dot at the boundary. Raise `uGrainScale` for a finer fibre size, or raise the bake to 2048 for hero surfaces; never rescale the mesh instead.
- **Colour-space slip.** The field is data: `NoColorSpace`, not sRGB. Tone-mapping is applied once at the end (the workshop does it in a hand-written final pass; the demo uses `ACESFilmicToneMapping`).
- **The oil finish lit the raw finish.** Materials that differ only by the `extra` snippet share one program cache key (`onBeforeCompile.toString()`), so the second material silently reuses the first program. Set a distinct `customProgramCacheKey` per finish; the Urushi wrapper does.
- **Environment lights no roughness variation.** `envMapIntensity` is ignored when only `scene.environment` is set (r163+); use `scene.environmentIntensity`. The wood needs a bright window card in the PMREM to show its roughness map; a grey dome hides it.
- **Cut faces read the same as the top.** Multiply cut faces by `1 - endgrain*(0.045+pores*0.10)` and raise their roughness `+0.14`: end grain drinks finish and stays matt, the fastest cue that this is a solid block.
- **Sharp boards float.** A box with no arris and no contact shadow looks pasted. Rest each part exactly on its support (`y = h/2`), bake the shadow map once (`shadowMap.autoUpdate=false`) and check the close-up for a gap.

## Budgets

- Bake once, 1024² RGBA8 with mips (about 5.6 MB GPU), shared by every timber.
- Measured on this Apple GPU in headless Chrome, 13 draw calls and about 2,000 triangles (chamfered boxes, bench, wall) with MSAA on: 1.0 to 1.5 ms per frame at 1440 by 900, 3.4 to 4.5 ms at 2880 by 1800, against 0.65 ms and 4.2 ms for a plain tiled `MeshStandardMaterial`. The procedural shader costs roughly 0.4 ms at 1x on this scene and vanishes into fill cost at 2x. Fill rate (DPR, MSAA) is the lever, not the noise.
- Cap DPR at 2. Bake shadows once when the boards are static. Pause on `document.hidden` and reset the clock. Clamp `dt` to 1/30 s.
- Under `prefers-reduced-motion` skip the slow orbit and snap camera moves; the still is the composed hero view. Controls stay live.

## Self-score of this material (0 to 10, anchored)

Anchors: 2 tiled photo with flat roughness. 4 procedural stripes with albedo only. 6 rings plus relief plus varied roughness, holds at arm's length. 8 pores, rays and end grain hold at 5 cm, finish and wear are believable, no shimmer. 10 scanned-species photograph at every distance.

| dimension | score | why |
| --- | --- | --- |
| grain structure at arm's length | 7.5 | per-ring widths, cathedral arcs and knots; keyaki at default still reads a little ruled |
| macro (3 to 5 cm) | 6.5 | pores, fibres and tool marks resolve; the 1024² field softens past 4,000 px per unit |
| roughness and finish | 7.5 | oil, wax and urushi respond to rings and pores; no anisotropic highlight |
| end grain and edges | 7 | open cells and matt cut faces; arris round, no true edge wear |
| shimmer and grazing | 8 | footprint fades leave grazing and distance clean |
| **overall** | **7.3** | |

## Provenance

Extracted from the Kibori 木彫 workshop page, where one `woodMat()` timber shader dresses the walls, benches, tool handles, kumiko lattice and lacquered chests; the generators in `demo.html` are copied from that file unchanged. The wood was tuned for a close inspect camera, so every constant above is the workshop's own.
