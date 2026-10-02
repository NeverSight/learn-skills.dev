---
name: remotion-2d
description: 2D scene craft in Remotion — animation tuning with spring/interpolate, kinetic typography, stagger choreography, layout grids, and per-scene structure. Use when building or polishing any non-3D scene.
---

# 2D Scene Craft

## Scene anatomy

- Each scene is a component receiving no props (reads `useCurrentFrame()` inside its own `<Sequence>` local timeline) or a `from` offset prop for cross-scene choreography.
- `<AbsoluteFill>` for full-bleed; explicit `backgroundColor` always (it defaults to transparent).
- Build scenes in layers: background (gradients/particles) → midground (cards/media) → foreground (text/captions) → vignette/grain overlay. Each layer is one component for easy tuning.

## Animation tuning

- `spring({frame, fps, config})` for entrances; `interpolate()` with `extrapolateRight: "clamp"` for everything mapped from progress. One spring drives many derived values (opacity, translateY, scale) — they stay in sync automatically.
- Presets (starting points, tune per project):
  - Punchy UI pop: `{ damping: 12, mass: 0.8, stiffness: 200 }`
  - Soft drift / ambient: `{ damping: 20, mass: 1, stiffness: 60 }`
  - Overshoot/bouncy: `{ damping: 8, mass: 1, stiffness: 180 }`
  - Heavy cinematic settle: `{ damping: 26, mass: 1.6, stiffness: 120 }`
- Easings: use `Easing.out(Easing.cubic)` for exits from screen, `Easing.inOut(Easing.sin)` for loops (breathing, floating). Reserve springs for things that should feel physical.
- Stagger lists by index: `spring({ frame: frame - i * stagger })`, stagger 2–6 frames per item. Reverse stagger (last first) reads as "reveal from the end" — good for lists where the punchline is last.
- Exit choreography: mirror the entrance (reverse translateY + fade) but faster (~60–70% of entrance duration). Never let exits overlap scene cuts unless the transition owns them (see remotion-transitions).
- Loop-friendly ambient motion: `Math.sin(frame * f + phase)` with f between 0.004 (slow drift) and 0.02 (noticeable bob). Combine two sines with different frequencies for organic motion.
- Overshoot/anticipation: pull back before a move (interpolate progress through [0, -0.1, 1] with keyframes) for cartoon emphasis; use sparingly (once per scene).
- Mask reveal (premium entrances): parent `overflow: hidden`, child springs `translateY(150%→0)` — text rises from a clip line instead of fading in. Combine with per-word stagger for kinetic titles.
- 3D card flip (hero move): container `perspective: 900–1200`, card `transform: rotateY(deg)` from a slow spring (damping 12, stiffness 60, mass 1.2 → ~40-frame flip). Render front content when `deg < 90`, back content after (avoids mirrored text). Peak a radial glow and box-shadow at 90° via `interpolate(deg, [0, 90, 180], [0.2, 1, 0.3])` — the flip "charges" the room at the edge-on moment. Add a constant slight `rotateX(tilt)` tilt + sine float so the card never sits flat.
- CSS-3D orbit rings: a square div rotated `rotateX(70–75deg) rotateZ(frame * speed)` with `transformStyle: preserve-3d`, dots positioned by cos/sin on its edge — reads as a spinning orbital ring at near-zero cost. Stack 2 rings at different radii/speeds for depth.
- Typewriter: reveal `text.slice(0, Math.floor((frame - start) / charsPerFrame))` with a blinking block cursor (`frame % 30 < 15`). Gate follow-up animations on typing completion (`typingDoneFrame = start + len * charsPerFrame`) so springs fire after the text lands.
- Blueprint grid: `backgroundImage` of two 1px linear-gradients at 40–50px background-size, alpha ≤ 0.05 — adds technical depth behind cards without noise. Pair with a mid-screen radial glow that breathes.
- State-machine scenes: derive phase from frame (`typing → clicked → pulse`), each phase gating different springs — gives UI-demos a believable interaction feel (press ripple, button pulse, cursor state changes).

## Kinetic typography

- Split text into words or chars; wrap each in a span animated with the stagger pattern. Word-level for readability, char-level for display headlines only.
- Mask reveal: parent `overflow: hidden`, child `translateY(110%) → 0` — reads as "rising from a line", more premium than fade.
- Emphasis: scale + color shift on the single most important word; animate weight via separate font files only if preloaded (variable fonts cause layout shift mid-render).
- Text glow: `textShadow: 0 0 Npx color` — keep N ≈ fontSize/3 and alpha ≤ 0.6, else it reads cheap.
- Fonts load via `@remotion/google-fonts` `loadFont()` awaited at module scope, or `@fontsource/*` CSS imports in the root file. Verify with a still render before long renders.

## Layout

- 12-column mental grid; safe margins of ~5% width per side (larger, 8–10%, for 9:16 vertical).
- Hierarchy via scale jumps of 1.5–2x (not 1.2x) between levels; a video frame is seen for seconds, not read.
- Center is the default focal point; use rule-of-thirds (33%/66%) for diagrams and split layouts.
- All lengths relative: derive from `width`/`height` of `useVideoConfig()`, or use a scale factor `const s = width / 1920` applied to font sizes and spacing so the design survives resolution changes (see remotion-rendering).
- Cards/panels: border-radius ≈ 1/12 of card width; shadow `0 20px 60px rgba(0,0,0,0.3)` reads as depth without blur cost.

## Slow push-in over large bitmaps (Ken Burns shimmer)

Symptom: stills are clean but text edges crawl/shimmer during a slow scale push-in over a heavily downscaled screenshot (e.g. a 4K capture shown at ~460px). Cause: every frame the browser re-resamples the huge source at a non-integer ratio with no mipmaps — resampling aliasing on fine text. It is a resampling artifact, NOT an animation/determinism bug (stills clean + motion shimmer is the signature). Recipe:

1. **Pre-downscale assets at build time** to at most ~2x their maximum on-screen size (display width x the largest scale factor of the animation), with a high-quality filter (`sharp` lanczos, or `sips`). Never let the browser downscale more than ~2x per frame; an 8x per-frame downscale of fine UI text will shimmer no matter what.
2. **Snap translate to integer px** (quantize the interpolated offset); keep the scale the only subpixel value, and prefer scaling from the element's own center so translate isn't compensating for scale origin.
3. **Codec**: render text-heavy masters with `--image-format=png`, or `--jpeg-quality >= 95` if size matters — JPEG ringing compounds the shimmer but is not its root cause.
4. **Separate shimmer from judder.** Shimmer = texture edges crawl (aliasing, fixed by 1-3). Judder = the whole card advances unevenly frame to frame — a motion-sampling problem: on a very slow move the per-frame displacement is sub-pixel, and if the element is not on a composited layer Chrome quantizes the transform to layout pixels, so steps come out as 0,1,0,1 px instead of 0.5 each. Fixes: animate `transform` only (never width/height/top/left); force a composited layer (`willChange: "transform"` or `translateZ(0)`) so scale/translate stay subpixel-smooth; keep the interpolation continuous (no rounding of the scale value, no keyframe kinks — one linear or one eased curve across the whole move); and if displacement per frame is still < ~0.3px, either shorten the move, increase its range, or render at 60fps — a 1.03→1.12 push over 12s at 30fps moves a 460px card ~0.1px/frame, which no resampler can make look smooth.
5. Alternative for very slow moves: keep the image at a fixed size inside an `overflow:hidden` frame and pan with integer-px translate instead of scaling — rock-stable, at the cost of visible stepping at very slow speeds (test at 30fps).

## Charts and data (no library needed)

- Bars/lines/donuts as SVG driven by spring progress: line reveals via `strokeDasharray`/`strokeDashoffset = length * (1 - progress)`; bar heights `interpolate(progress, [0,1], [0, value])`.
- Animate data, not CSS. Count-up numbers: `Math.round(interpolate(progress, [0,1], [0, target]))`.

## Gotchas

- `interpolate` throws on non-monotonic input ranges; guard `frame - delay` values that can go negative (`Math.max(0, ...)`).
- `filter: blur()` and large `box-shadow` are the most expensive CSS — test render speed early.
- Elements mounted mid-composition (inside later Sequences) crash at first-mount frame, not at bundle time; keep imports/props valid.
