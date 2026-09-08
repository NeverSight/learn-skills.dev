---
name: verify-pixels
description: Use when changing PlayCanvas rendering code that must not visibly change the rendered image — draw-call optimization, hardware instancing, shader or material refactors, noise or lightmap bakes, or asset pipeline swaps — before shipping.
---

# Prove pixels unchanged

Choose the gate before building the capture harness. Both classes require controlled captures
that cover the affected surfaces.

## Classify the change

| Change | Gate |
| --- | --- |
| Batching, instancing, mesh indexing, chunking, pooling that preserves RNG order, an asset format swap with identical decoded data | Byte-exact matrix |
| Re-rolled or re-sampled procedural noise, a changed RNG consumption order, math moved between CPU and GPU, changed precision, fewer octaves or samples | Not byte-gateable: side-by-side review |

For the second class, sampled values or precision can change. Report it as "not byte-gateable" and
use the side-by-side gate after the shared capture setup below; do not invent uncalibrated perceptual
thresholds to approve it.

## Cover every touched surface

List every touched material or surface and a capture pose it dominates. Use at least two
representative poses, adding as many as coverage requires; a horizon strip does not cover a water
shader change. For animated surfaces, include a second phase mid-animation.

## Make the frame deterministic

For both gates, load assets fully and match the scene state, camera, canvas size, lighting, and
animation time between builds. Seed incidental randomness so only the intended change varies.

- Drive every animated shader or vertex effect from one app-owned time value, never `Date.now()` or
  `performance.now()` read inside the render path, so a captured phase is exactly reproducible.
- Freeze the clock with `app.timeScale = 0` before capturing; nothing should advance between frames
  you did not explicitly step.
- Step frames explicitly: set `app.autoRender = false` once, then set `app.renderNextFrame = true`
  before each frame you want rendered. The engine renders exactly that frame and clears the flag —
  do not rely on the free-running render loop plus a timed screenshot.

## Gate and report the byte-exact class

Read the exact backbuffer with `await device.readPixelsAsync(x, y, w, h, pixels)`. In the installed
engine this method lives on `WebglGraphicsDevice`, so narrow to it; WebGPU needs an equivalent
readback. An existing capture path must preserve raw pixels without colour conversion or lossy
encoding before comparison.

Before trusting any diff between the old and new build, capture the same pose × phase matrix twice
from the *unmodified* build. Two captures of identical, frozen state must be bit-identical. If they
are not, the capture path itself is the source of noise — an unseeded animation, an asset still
loading, a GPU timing race — and must be fixed before it can say anything about the real change.

Byte-compare each pose × phase pair between the two builds; do not diff by looking. Zero differing
pixels passes outright. Any nonzero diff must be reviewed on-screen, and its cause and extent stated
in the change description — never merged silently. Report the actual count every time, for example
"0 of 65536 pixels differ" or "312 of 65536 pixels differ, confined to the object's silhouette edge".
"Looks the same" or "no visible difference" is not a result.

## Review the other class side by side

For each planned pose and phase, show the controlled old and new captures together in one image
for the user's accept or reject. State what differs and why, for example "noise tile replaces
runtime fbm: pattern period changed, tint and amplitude match". If no difference is visible, report
that. Skip the cross-build byte comparison for this class.

## Keep the harness small

Reuse the project's capture harness when available. Keep harness code out of the shipped bundle,
behind a dev-only import or in a tools directory, and list its files in the change description.
Capture with a headless browser and return images only at accept-or-reject points, not after every edit.
