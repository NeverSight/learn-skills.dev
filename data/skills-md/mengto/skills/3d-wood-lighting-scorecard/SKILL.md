---
name: 3d-wood-lighting-scorecard
description: Light carved wood in a dark room in three.js, with procedural grain and pores, one warm key through a window, soft shadows that touch, light shafts, background rays and dust, then score the render out of 10 on an anchored rubric with a runnable headless scorecard and iterate until each item reaches the target. Use for oiled timber, kumiko, joinery and workshop scenes; wood that reads flat, plastic or washed out; volumetrics that lift the blacks; "score this out of 10"; or "get the lighting to 8".
---

# 3D Wood Lighting Scorecard

Wood only looks like wood under one directional key raking across a dark room, so the grain, the shadow seam and the light shafts are lit by the same window, tone-mapped once at the end, and each is measured on the finished frame instead of judged by mood.

Verified stack: Three.js r169 (unpkg), WebGL2, GLSL patched into `MeshPhysicalMaterial.onBeforeCompile`, a half-float MSAA target and a hand-written ACES pass. The demo is `demo.html`; the numbers are `references/`.

Boundaries. This is the lighting-and-material layer for one lit interior. For sun shafts that must be cut by real trees and rooflines use `3d-sky-rays` (screen-space occlusion); here the shafts are authored planes. For scanned or painted PBR maps, texel budgets and delivery use `3d-high-resolution-textures`; here the wood is procedural from one shared 1024 noise field. For a bright rim on dark metal use `3d-specular-rim-glow`; for glass use the studio-box ladder, not this. For the scoring habit alone use `workflow-score-to-target`; this skill supplies the wood rubric and the machine that measures it.

Extracted from Kibori (木彫), a scroll-driven WebGL woodworking page: its `woodMat`, `buildEnvironment`, key rig, shaft planes, dust and final pass are ported, with the window moved to where the shafts need it.

## Build order

1. Renderer: `NoToneMapping`, `LinearSRGBColorSpace`, `HalfFloatType` target with `samples: 4`, `autoClear = false`. Draw everything, additive shafts and dust included, into that target. Tone-map once in a last full-screen pass.
2. One window. Put the emissive paper, the key light's direction, the shaft planes, and the window card in the PMREM environment on the same line. Nothing else.
3. Key `DirectionalLight` 0xfff2df, intensity 2.0, 4096 shadow map (2048 under 820 px), `normalBias` 0.0045 (0.0085 at 2048), `bias` -0.00025, `shadowMap.autoUpdate = false` for a static room. Let a real wall with a real opening cast: the pool of light on the bench is then the window's shape.
4. Fill 0xaec7df 0.60-0.76 from the camera side, rim 0xffdeb4 0.72 from behind, hemisphere 0xb5c5d7 / 0x35281c 0.19. These only keep the shaded flank alive; they are not the look.
5. Wood: `MeshPhysicalMaterial` `ior 1.43`, `specularIntensity 0.72`, roughness `clamp(base * W.rough, 0.35, 1)`, procedural albedo/roughness/bump from one periodic noise field baked once (1024x1024 RGBA8, 64 cells, three octaves, mipmapped, repeat).
6. Shafts, then dust, then the last pass, then run `references/scorecard.mjs`.

## Rules, each with the failure it prevents

**Grain vanishes under flat light.** A hemisphere or environment that is bright enough to see the room fills every pore and the board reads as painted. Keep the key at 2.0 and the ambient terms low; measured here, turning the studio reflections off raised the total score by 0.14 because they lifted the shadows. Per-material `envMapIntensity` 0.25 for the bench, 0.45 for the carved board, 0.40 default.

**`envMapIntensity` does nothing and tuning "works" on paper.** With three r163+ the material value is only read when `material.envMap` is set; `scene.environment` alone ignores it. Set `mat.envMap = env` on every wood material, and toggle a layer through the intensity, not by nulling the map (that recompiles).

**The sheen mirrors a window that is not there.** Kibori hung its environment window at front-left; a scene whose window is behind-left reflects a light that does not exist. Place the environment window pane group where the real window is (here `(-2.3, 4.3, -3.2)`, scale 0.5, 12 panes 1.24x1.38 at radiance 3.8/3.55/3.05). Tilt the board so the mirror direction lands a little off the window (0.27 rad here; at exactly the mirror angle the whole board turns milky).

**Volumetrics wash the blacks and the grain.** Additive planes add light to everything behind them, including the top of the timber they cross. Fade each shaft by world height (`smoothstep(0.02, 0.34, y)`), keep the gain at 0.13 (Kibori 0.12) and the brightness above the reference strip under 35 levels, and read the black point: `p1` must stay under 7. Before the height fade, gain 0.14 laid a milky haze across the plaque and the grain went with it.

**A hard wedge where a shaft plane cuts a solid.** The plane intersects the bench or the post and draws a bright line. Kibori kept planes behind the benches; the height fade above does it without moving them. Also `clamp` before `pow`: `pow(1.0 - across, 2.2)` with a hair-negative edge coordinate is NaN and NaN through additive blending is a black wedge.

**God rays clip.** If the renderer tone-maps, or the shaft pass is added after ACES, the beams either double-map or hit 1.0 flat. Sum them in linear HDR, then run ACES once (`a=2.51 b=0.03 c=2.43 d=0.59 e=0.14`). The window paper is `toneMapped:false` linear (1.15, 0.86, 0.52); at (3.9, 3.35, 2.55) it clipped to white paper.

**Additive alpha.** `AdditiveBlending` adds alpha too. On an opaque canvas it is invisible; if the scene is ever drawn into an alpha-composited layer, use `CustomBlending` with `blendSrc One, blendDst One, blendSrcAlpha Zero, blendDstAlpha One`.

**Shadow acne on the bench, or a gap under the plaque.** Acne comes from a small negative `bias` alone; use `normalBias` scaled to the map (0.0045 at 4096, 0.0085 at 2048). A gap between object and shadow (peter-panning) is `normalBias` too high. The scorecard reads it as `contactGap`. Add a baked contact pool under each object (radial alpha 0.78, r = 0.30..1.0 smoothstep, y 0.0012); the shadow map alone leaves the seam light.

**A single-band texture shimmers at grazing angles.** Fine bands (pores at 96/88 cycles per metre, fibres 230, rays 13/115) must fade with `fwidth` of their own coordinate, and the bump must give up before the colour does (`1 - smoothstep(0.05, 0.18, vesselPx)`), or `dFdx(h)` beats into moire. The scorecard's `shimmer` is a half-pixel view shift; 1.1 here, 3+ is aliasing.

**A carved relief turns to noise.** Grooves under 12 px per period alias in the bump and sparkle against a bright environment. The seigaiha carving here uses 0.15 m cells and two rings per circle (about 16 px at 1440 wide); at 0.062 m it was noise at 1x and fine at 2x. Size carving to the pixel budget, not the model.

**Bricks in the grain.** Medullary-ray flecks (`rays`) on a flat-sawn top face read as a tiled grid. Kibori's 0.8 default is for quartersawn faces; on the plaque it is 0, on others 0.15.

**Banding in the dark wall.** 8-bit steps in a vignetted gradient. A +-0.0015 hash dither (`(hash - 0.5) * 0.003`) after the sRGB encode removes it; the scorecard counts runs of 6+ identical pixels (`flatRun` 0.019).

**The metric moves when the camera does.** Freeze the sway and time (`KiboriScore.freeze(true)`), render and read the canvas in the same task (no `preserveDrawingBuffer`), capture at a fixed size and DPR, and use headless Chromium; the in-app pane backgrounds itself and shares the GPU.

## Constants

| Item | Value |
|---|---|
| Camera | 34 deg vertical, (0.60, 1.25, 2.55) looking at (0.05, 0.50, -0.30); wider FOV below aspect 1 |
| Light direction | (0.40, -0.75, 0.45) normalised, window centre (-0.60, 1.40, -1.0), opening 1.5 x 1.5 |
| Target | HalfFloat, MSAA 4, DPR cap 2 |
| Key / fill / rim / hemi | 2.0 / 0.60 / 0.72 / 0.19 (Kibori fill 0.76) |
| Shafts | 5 planes 0.44-0.52 wide, length 2.75, gain 0.13, foot fade 0.22 (Kibori 0.30), fbm 3 octaves |
| Wall rays | 10 planes, 0.20-0.90 wide, length 2.2, gain 0.08 |
| Dust | 1900 points, size `17 / depth` px clamped 3.4-46, `1 - smoothstep` bokeh, gated to within ~0.33 m of a beam axis |
| Field | 1024^2 RGBA8, 64 periodic cells (`n`, `f`, second `n`), mipmapped; 16 px for the "low" toggle |
| Last pass | unsharp 0.10, vignette `0.42 + 0.58 v`, ACES, sRGB, dither 0.003 |

## Cost (measured, headless Chromium on Apple Silicon, Metal)

Full pipeline, one frame plus a 1 px readback: 7.4-7.9 ms at 1440x900 x1, 16.5 ms at 2880x1800 (DPR 2), 7.2 ms at 390x844 DPR 2. The shaft and wall-ray planes are the dearest layer (a 3-octave fbm per additive pixel: about 1 ms at x1, 5 ms at x2); the shadow map is free after the first frame because it is static; grain, env, key and dust are each about 0.2-0.7 ms. The cheap lever is the fbm octave count on the shafts (or drawing them at half resolution), not fewer planes. Do not conclude from one toggle: at 2x the noise between runs is about 1 ms.

## Scoring loop

1. Serve the page, `npm i playwright-core`, run `node references/scorecard.mjs` (`--url`, `--size 1440x900`, `--dpr 1`, `--target 8`, `--no-ablate`, `--sync`). It captures headless, freezes time, scores the eight items in `references/rubric.md`, ablates each layer and writes JSON; exit code 1 if any item is short.
2. Score the baseline before changing anything (all layers off: 3.7 here) and keep the file. The ablation is the check on the metrics: a layer whose removal raises the total is either measured wrongly or not earning its cost.
3. Fix the lowest item's cheapest sub-metric first, re-run at the same size and DPR, and keep only what the picture confirms. Look at a 2x crop after every metric-driven change; three of this demo's "improvements" raised a number and made the board look worse (full-board clearcoat, anisotropy 0.3, per-pixel tone gain 2.4) and were reverted.
4. For a score that means "looks right", hand the captures and the rubric to a fresh judge that has not seen the numbers, and take the lower of the two.
5. Report honestly. Demo, 1440x900 x1: 8.8 average; grain 8.1, key/fill 10, shadows 9.6, shafts 8.0, rays 8.8, tone 9.8, texture 9.7, specular 6.5 (short of 8: the sheen is broad, not a distinct highlight, and the fixes that added one damaged the grain). At DPR 2 the specular item is 7.4 and shafts 7.3 (dust specks finer than the measuring window).

## Accessibility and lifecycle

- `prefers-reduced-motion`: a designed still (time fixed at 5.2, no sway, no dust drift), rendered on demand; the layer switches and the score still work.
- Pause on `document.hidden` and when the canvas leaves the viewport; `dt` clamped to 1/30 s, and the first frame after a pause has `dt = 0`.
- Size from a `ResizeObserver`; DPR capped at 2; target and dust point size follow it.
- Layer switches are real checkboxes with visible focus; the score is an `aria-live` region.
- Below 820 px the panel moves under the canvas and a score chip sits on it.

## Verify

- The metrics block in `demo.html` equals `references/metrics.js` (`node scorecard.mjs --sync`).
- 1440x900 and 390x844, console clean, reduced motion shows a composed frame, tab order reaches every switch.
- A scorecard JSON with baseline, all-on, ablation and cost exists and matches the claims above.
