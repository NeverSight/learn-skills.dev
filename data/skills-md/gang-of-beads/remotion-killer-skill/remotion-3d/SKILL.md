---
name: remotion-3d
description: 3D content in Remotion with @remotion/three, React Three Fiber, and drei — deterministic animation, camera moves, lighting, particles, shaders, and headless-render pitfalls. Use when adding any 3D to a Remotion composition.
---

# 3D with @remotion/three

## Core determinism pattern

- Wrap 3D content in `<ThreeCanvas width height camera>` from `@remotion/three` (it bridges the Remotion frame clock into R3F).
- Drive ALL animation from `useCurrentFrame()` read in markup and passed as props: `<mesh rotation={[0, frame * 0.02, 0]}>`. Do NOT use R3F `useFrame()` for anything that must be frame-exact — it ticks on render loop timing, not the timeline.
- Positions/scatter via remotion's seeded `random(seed)`, never `Math.random()`. Any accumulation (sum over frames) is a determinism bug; compute absolute values from frame.
- Async assets (GLTF, HDRIs, fonts): `const handle = delayRender()` at load start, `continueRender(handle)` in the load completion callback. Otherwise frames render before assets exist.

## Camera work

- Programmatic camera only (`<OrbitControls>` is for Studio preview, disable/omit in final comps).
- Simple orbit: `camera` via `<PerspectiveCamera makeDefault>` + set `position` from frame: e.g. radius + angle `= frame * speed` around a lookAt target.
- Moves that read as expensive: slow dolly-in over the whole scene (z from 8→5), arcing reveal (angle sweep 30–60°), rack focus via `fov` or `focusDistance`. Keep FOV fixed unless doing a deliberate dolly-zoom.
- Eased keyframe paths (interpolate position vectors per axis) beat hand per-frame math.
- One camera move per scene; stacking moves reads chaotic in short videos.

## Lighting rig

- Baseline: ambient (0.3–0.5) + key directional (1.5–2.5, from upper side) + colored rim/point light from behind (complementary hue, intensity high for point lights — distance falloff) → reads "cinematic".
- Metallic/rough materials need an environment map to look good: drei `<Environment>` — but presets download remote HDRIs at render time; self-host the `.hdr` and gate with `delayRender`, or use `<Environment>` with local files.
- Shadows: `castShadow` per mesh + soft shadow map; expensive — enable selectively and test render time.

## Materials & postprocessing

- Hero object: `meshStandardMaterial` with `metalness 0.6–0.8, roughness 0.15–0.3` + emissive tint of the brand color at low intensity (0.1–0.2) so it never goes black in shadow.
- Custom shaders: `THREE.ShaderMaterial` with uniforms `{ uTime: frame / fps, ... }` — deterministic and fast. Great for flowing gradients, distortion, grid warps.
- `@react-three/postprocessing` Bloom makes glow real but each pass multiplies render cost; budget against frame count. CSS glow on a transparent overlay is often 90% as good.

## Particles

- 200–1000 points via `<points>` + `bufferGeometry` + seeded positions; rotate/move via frame math in props.
- Additive blending + small size (0.03–0.08) + low opacity (0.4–0.7) reads as dust/energy.
- Particles reacting to audio: precompute a per-frame amplitude array (see remotion-audio-sync) and scale positions/pulse material by it.

## Headless render pitfalls

- WebGL in headless Chrome needs a GL backend: pass `--gl=angle` (macOS/Windows) or `--gl=egl`/`--gl=swiftshader` (Linux/CI). SwiftShader always works but is slow.
- Symptom "Could not create a WebGL context ... BindToCurrentSequence failed" on macOS → use `--gl=angle`.
- High `--concurrency` can cause WebGL context loss ("context lost") — drop to 2–4 for 3D-heavy comps.
- Pre-bake what you can: merged geometry, compressed textures (KTX2), low-poly proxies. Per-frame cost × total frames is the real budget.
- Deprecation warnings (THREE.Clock) from drei internals are harmless; do not chase them.
