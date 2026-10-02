---
name: remotion-style-system
description: Visual style systems for Remotion videos — palette building, gradients and orb blobs, glassmorphism, grain/texture, glow, dark/light theme handling, and named style presets. Use when defining the look of a video or making scenes cohesive.
---

# Style System

## Tokens first

- One `tokens.ts` per project: `palette`, `spacing` scale, `typeScale`, `radius`, `easing/spring presets`, `shadow recipes`. Components never hardcode colors or sizes.
- Theme via object spread: `const theme = { ...darkTheme, accent: brand }`. Scenes receive the theme or import it — never branch on `useVideoConfig()` for style.

## Palette construction

- Anchor on one brand hue; build a ramp of 4–5 lightness steps (e.g. #021CD9 → #3854FE → #5E75FE → #BAC5FE → #E2E7FE). Use ramp steps for depth layers (far = dark, near = light) on dark themes.
- Add 2–3 functional accents (success/cyan, highlight/purple, warning/orange) used ONLY for their meaning.
- Dark themes: background near-black with hue (e.g. #05070F, not #000); text at 90–100% white; secondary text 60–70%.
- Light themes: warm-white background (#FAFAFC), text near-black, use saturated brand color only in accents — full-saturation large areas vibrate on screen.
- Contrast check text vs background ≥ 4.5:1; captions must clear it at video compression bitrate.

## Gradients & orb blobs

- Mesh-gradient look: 2–4 radial gradients (one per hue) on stacked absolute layers, each `filter: blur(60–140px)`, positions drifting with two-frequency sines. Opacity per layer 0.06–0.15 on light, 0.2–0.4 on dark.
- Linear gradients for surfaces: 135° hue-to-hue-shifted-hue (same hue family) reads premium; multi-hue linear reads promotional.
- Animated gradient: move the gradient center (not hue) over time — cheaper and smoother than animating colors (`interpolateColors` exists for hue shifts when needed).
- Rotating conic halo: a large square/circle div with `conic-gradient(from ${frame * 0.7}deg, colorA, colorB, colorC, colorA)` at low alpha, blurred 80–120px, behind a hero title — gives a slowly swirling aurora ring that reads as energy, not decoration. Conic gradients are also the standard "border glow spinner": conic ring + mask to a border shape.

## Glassmorphism

- Recipe: `background: rgba(255,255,255,0.05–0.08)`, `border: 1px solid rgba(255,255,255,0.12–0.2)`, `backdropFilter: blur(15–25px)`, radius ≈ 1/10–1/12 of width, plus a soft drop shadow.
- Only works over varied content (gradients/3D behind) — over flat color it is invisible. Always pair with a blob/scene background.
- Headless render handles `backdropFilter` correctly (verified), but nested backdrop-filter surfaces can double-blur; keep one glass layer per scene region.
- On light themes invert: rgba(0,0,0,0.04) fill, darker border.

## Texture & quality cues

- Film grain: overlay `<Noise>` from `@remotion/noise` at opacity 0.03–0.08 — hides banding in dark gradients (the #1 cheap-fix for gradient banding).
- Vignette: radial-gradient overlay `transparent 60% → rgba(0,0,0,0.25) 100%` focuses the eye and adds depth.
- Glow: `textShadow`/`boxShadow` with the accent hue; radius ≈ 1/3 of element size, alpha ≤ 0.6. Animate glow radius for beat pulses.
- Motion blur for fast moves: `@remotion/motion-blur` package (layers ghosted frames); otherwise increase move duration and ease-out.
- Depth: layered shadows (`0 1px 2px` + `0 20px 60px`) and slight parallax between layers (background moves at 0.5x foreground speed).

## Style presets (starting points)

- **Tech/dark**: near-black hue-tinted bg, blue-violet ramp, glass cards, cyan/purple accents, particle dust, soft glows.
- **Corporate/light**: warm white bg, single brand ramp, flat cards with hairline borders, minimal glow, generous whitespace.
- **Bold/social (9:16)**: high-saturation duotone, huge type (10–15% of frame height per line), hard shadows or thick strokes, fast cuts on beats, karaoke captions.
- **Editorial/cinematic**: desaturated palette + one accent, serif display + sans body, film grain, slow dolly/spring settles, letterboxed safe area.

## Gotchas

- Large blurred layers are the main render-time cost; cap blob count at 3–4.
- Banding in dark gradients: add grain, or raise gradient stop spacing.
- Pure #000/#fff flash on cut boundaries; ease backgrounds between scenes even when the transition handles the foreground.
