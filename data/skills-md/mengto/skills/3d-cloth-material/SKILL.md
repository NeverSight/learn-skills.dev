---
name: 3d-cloth-material
description: Build convincing woven cloth in Three.js, with a thread-level weave normal map, sheen and anisotropic highlights, folds that never stretch the texture, hems with thickness, stitches, seams, frayed edges, fold occlusion, dye and wear variation, and light passing through thin fabric. Use for linen, silk, wool, canvas, curtains, banners, cloaks, tablecloths, tapestries or any 3D drape that currently looks like a plastic sheet, a stretched texture, or a flat coloured plane.
---

# 3D Cloth Material

**Mechanism:** hang the cloth as rows whose *tangent angle* is the fold signal, so arc length equals the rest coordinate `s` and the weave never stretches. Then let a thread-level weave, sheen, hem thickness and light through the gaps do the reading of "fabric".

Nearest neighbours: `3d-high-resolution-textures` chooses texel density, mipmaps and delivery for any material; use it for the budget and stay here for what makes *cloth* different (weave interlacement, folds, sheen, hems). `3d-wood-material`, `3d-paper-material` and `3d-metal-material` cover their own surfaces; this skill owns woven and sewn fabric only. It is not a cloth *simulation*: for a character's flowing cape or a flag that collides, simulate (Verlet or Blender cloth) and bake, then keep the material rules below.

Extracted from KIBORI 木彫, a dark WebGL workshop where a roll of indigo canvas (the dōgu-maki) lies under a warm key light and had to survive a macro close-up. Ported from there: the weave bake, the stitch shader, half-circle hem turn-under, wear on thread tops, the sheen constants. Newly built for this skill (Kibori has one indigo canvas, not three fabrics): the tangent-angle fold curve, satin and twill interlacements, silk/wool/linen tables, tabs on the rod, raw-edge fray, fold AO, backlit transmission, wind. `demo.html` is the reference.

Demo: Three.js r169 · WebGL · GLSL (`MeshPhysicalMaterial` + `onBeforeCompile`), vanilla JavaScript, no post chain.

## The rules, each with the failure it prevents

1. **Integrate folds from an angle, not a height.** `α(s) = a·(sinθ + 0.16 sin(2θ+0.8)) + …`, then `x += ds·cos α`, `z += ds·sin α`. Failure: a height field `z = A·sin(kx)` gives arc length 1 + slope², so the weave swims and stretches 30–80% on every fold. With the angle form `uv = (s, v)` in metres is exact. Keep `|α| < 1.45` rad; past that it clamps into flat plateaus and folds become tubes with black seams.
2. **Uv is material metres, never re-fitted per frame.** Do not recompute uv from the moving surface. Failure: weave shimmers and crawls in wind. Set `texture.repeat = 1/(threads × pitch)` so one texel tile is `NT` threads; linen 1.6 mm, silk 0.7 mm, wool 2.6 mm pitch.
3. **Bake interlacement, not noise.** Each thread has its own width (0.80–0.97), tone and a slub (Gaussian thickening up to 0.34). Warp height blends over/under across cell borders by `0.5·smoothstep(0.05, 0.5, |t|)`. Plain = `(A+B)&1`, twill 2/1 = `(A+B)%3 < 2`, 5-harness satin = `(2A+B)%5 != 0` warp-over. `NT` must be a multiple of the repeat (32, 24, 40) or the tile shows a seam. Failure: a tiled noise normal map reads as stucco or leather.
4. **Spun yarn gets a twist.** Add `0.22·twist·sin(2π(5·along + 1.3·across))` to each thread height (twist 0.10–0.14 for linen and wool, 0 for silk). Failure: linen looks like wire mesh.
5. **Two dyes, per-thread tone.** Colour `mix(warpDye, weftDye, weftOnTop·shot)`; silk uses shot 1.0 (madder red warp, gold weft), the rest 0. Tone `mix(0.86, 1.14, threadTone)`, cavity `mix(0.5, 1, smoothstep(0.05, 0.85, height))`, blotch + warp-direction streaks `1 + var·((blot−0.5)·0.62 + (streak−0.5)·0.22)`. Failure: one flat albedo on a woven map looks printed.
6. **Sheen is the fabric, and it must be small.** `sheen 0.5–1.0`, `sheenRoughness 0.28 (silk) – 0.82 (wool)`, and `sheenColor = dye lightened × 0.62`. Failure: near-white `sheenColor` blows out to a milky rim under a warm key. Never set `sheen` to exactly 0 at runtime (0.0001); crossing zero recompiles the program and hitches 200+ ms.
7. **Silk gets anisotropy, wool gets fuzz.** Silk `anisotropy 0.85, roughness 0.36`; linen `0.90` rough with sheen 0.55; wool `0.96` rough with sheen 1.0. Keep `anisotropy` above 0 at creation (0.0001) so the define never flips.
8. **Fold occlusion is not optional.** Cast and receive the key's shadow map (`normalBias 0.012`, `bias −0.0004`, `DoubleSide` shadows) and add a vertex AO from the fold depth `0.62 + 0.38·smoothstep(−0.075, 0.035, zFold)` on indirect light. Failure: without both, valleys light up like the crests and the folds look painted.
9. **Edges have thickness.** Turn every free edge under on a half circle, `P = edge + out·r·sinφ − N·r(1−cosφ)`, `φ ∈ [0, 0.94π]`, `r` = 1.1 mm silk, 2.2 mm linen, 4.6 mm wool. Return the bottom hem up the back at `2r + 0.2 mm` with flipped normals. Failure: a zero-thickness cut edge is the loudest tell for CG cloth in a close-up.
10. **Stitch in the shader, in cloth metres.** Thread arches between holes (`4·x(1−x)` over 74% of the pitch), the needle groove and pucker feed the normal by finite difference, faded by `fwidth`. Hem 3 cm up, sides 2.2 cm in, seam `±7 mm` with a proud ridge that puckers every 4 pitches. Failure: geometry stitches z-fight and alias; texture-painted ones do not follow the folds.
11. **Raw edge: draw out the weft.** Beyond the cut, discard fragments except the warp threads (`|fract(u/pitch)−0.5| < 0.36`), each with a random length `F·(0.3+0.7·hash)`. Failure: an alpha fringe texture has no thread structure.
12. **Thin cloth passes light.** `emissive += trans · lightColour · dye·(1.7,1.2,0.85) · pow(max(0, −N·L), 1.15) · gap · thin` with `gap = mix(1, 0.42, height)` so threads block and gaps pass. Silk 1.05, linen 0.6, wool 0.06. Failure: without it a lit window behind a curtain does nothing.
13. **Wear where cloth is touched.** `wear = clamp(aWear·(0.25+height) + (fbm−0.5)·0.3, 0, 1)` → mix dye toward a pale colour by `wear·threadTop`. Hems +0.4, crests +0.3. Failure: uniform dye reads brand new.

## Constants

| | linen | silk | wool |
|---|---|---|---|
| weave / NT / pitch | plain / 32 / 1.6 mm | 5-harness satin / 40 / 0.7 mm | twill / 24 / 2.6 mm |
| normal strength S · normalScale | 2.6 · 1.15 | 1.5 · 0.6 | 2.9 · 1.45 |
| roughness · sheen · sheenR | 0.90 · 0.55 · 0.55 | 0.36 · 0.5 · 0.28 | 0.96 · 1.0 · 0.82 |
| fold λ · amax · wind gain | 0.34 m · 0.98 · 1.0 | 0.40 · 1.02 · 1.9 | 0.32 · 0.86 · 0.55 |
| edge | raw fray 3 cm | hem 3.5 cm | hem 5 cm |

Cloth 2.0 × 1.95 m, grid 160 × 120 (≈ 21k verts, 45k tris). Key SpotLight 0xffd0a0 × 3.0, angle 0.44, decay 0; cool fill 1.0; window back light 0.2–1.8; environment intensity 0.42; ACES, exposure 1.0.

## Gotchas, symptom first

- **Weave crawls or shimmers when it moves** → uv was rebuilt from arc length or scrolled; keep it as the rest metres.
- **Horizontal moire stripes at wide view** → bump/crease term uses `dFdx` of a high-frequency noise; keep crease octaves below 17 cycles/m and scale by 0.016. Mipmaps + 16× anisotropy handle the weave itself.
- **Folds are flat panels with black slits** → `|α|` clamped. Lower `amax` so `a·env·1.28 < 1.45`, do not add more darkness.
- **Everything glows orange when backlit** → transmission colour multiplied by a warm light *and* a warm dye. Tint by `(1.7,1.2,0.85)`, not `(2.1,1.35,0.72)`.
- **envMapIntensity does nothing** → in r163+ it only applies with `material.envMap`; with `scene.environment` use `scene.environmentIntensity`.
- **`onBeforeCompile` shader is shared between two meshes with different uniforms** → set `customProgramCacheKey`, and put uniforms on the material, not the mesh.
- **Winding wrong on a hem strip (lit inside-out)** → pick each strip's index order from the sign of its first triangle normal against the attribute normal, once, after the first update.
- **Turn-under leaves a dark gap** → the return strip must sit at `2r + 0.2 mm`, not `r`.
- **Shadow acne on a double-sided sheet** → `normalBias`, not a bigger `bias`; a large bias detaches the fold shadows.

## Lifecycle

`prefers-reduced-motion`: render one designed still at `t = 7.3` (gust mid-swell), stop the loop, keep every control live and re-render on change. Pause on `document.hidden`; reset `last` on resume. Clamp `dt` to 1/30 s, cap DPR at 2 and step it down by 0.25 when a 60-frame average exceeds 26 ms. Size from a `ResizeObserver`. Expose no per-frame allocation in the cloth loop: reuse typed arrays and update `position`/`normal` only.

## Cost (measured, headless Chrome for Testing, Apple GPU, 1440×900 at DPR 2)

- Cloth CPU (folds + normals + hems + tabs + fringe): 3.7–4.9 ms at 160×120. Halving the row count (190 → 120) bought −40%, and no fold was lost, because folds vary slowly down the drop.
- Whole frame: 10–11 ms wide, 15 ms macro. The macro's extra 4 ms is the fragment shader (weave + stitch + fbm) over the whole screen, not geometry.
- Boot: 0.8 s to first frame including three 512² weave bakes. Fabric switch 25 ms. Layer toggles 14 ms.
- Not the bottleneck: triangle count, the 2048 shadow map, tabs, fringe (520 strands).

## Score against the rubric (0 = flat coloured plane, 5 = convincing at arm's length, 10 = photographic macro)

Weave structure 7 · Sheen and dye 6.5 · Fold shape and drape 6 (a hanging curtain, not free cloth with self-contact) · Edges, stitches, seams 7.5 · Light transmission 6 · Wear 5.5 · Motion 5.5 (wind is analytic, no collision) · Performance 8. Overall 6.5. What would lift it: real self-collision folds (simulate and bake), fibre halo geometry on wool, a second normal scale for creases.
