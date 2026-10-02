---
name: web-shaders
description: Use when writing, debugging, or reviewing shaders for the web — GLSL or WGSL, raw WebGL2/WebGPU, Three.js (ShaderMaterial/RawShaderMaterial/TSL), or React Three Fiber. Covers the language/platform matrix, correct boilerplate, common effects (SDF/raymarching, noise, post-processing), and the pitfalls that make browser shaders fail silently.
---

# Web Shaders

You are writing shaders that run in a browser. Get the platform and language right first, then the technique, then verify visually.

## 1. Establish the target before writing a line

Ask (or infer from the codebase) which of these you are in — the boilerplate and language differ:

| Target | Language | Notes |
|---|---|---|
| Raw WebGL 2 | GLSL ES 3.00 (`#version 300 es`) | You declare everything. `in/out`, `texture()`, custom `out vec4`. |
| Raw WebGL 1 | GLSL ES 1.00 | `attribute/varying`, `texture2D()`, `gl_FragColor`. Legacy — avoid for new work. |
| WebGPU (raw) | WGSL | `@vertex`/`@fragment`, bind groups, uniform buffers with strict alignment. |
| Three.js `ShaderMaterial` | GLSL ES 1.00 by default | Three injects camera/model matrices and attributes (see §2). Set `glslVersion: THREE.GLSL3` for GLSL 3. |
| Three.js `RawShaderMaterial` | whatever you declare | No injected uniforms/attributes or `precision`. You write the full header. |
| Three.js TSL (WebGPURenderer) | JavaScript nodes | Author with `tslFn`/node ops; compiles to **both** WGSL and GLSL. No raw shader strings. |
| React Three Fiber | GLSL via drei `shaderMaterial` | Wraps `ShaderMaterial`; uniforms become material props. |

If the project uses `WebGPURenderer`, prefer **TSL** over raw WGSL strings — it is the supported path and cross-compiles.

## 2. Three.js ShaderMaterial: what is already provided

`ShaderMaterial` (not `RawShaderMaterial`) auto-injects, so do **not** redeclare them:

- Vertex attributes: `position`, `normal`, `uv`.
- Uniforms: `modelMatrix`, `modelViewMatrix`, `projectionMatrix`, `viewMatrix`, `normalMatrix`, `cameraPosition`.
- `precision` is set for you.

A minimal correct pair:

```glsl
// vertex
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```
```glsl
// fragment
varying vec2 vUv;
uniform float uTime;
void main() {
  gl_FragColor = vec4(vUv, 0.5 + 0.5 * sin(uTime), 1.0);
}
```

For GLSL 3 (`glslVersion: THREE.GLSL3`): replace `varying`→`in/out`, `texture2D`→`texture`, and declare `out vec4 fragColor;` instead of `gl_FragColor`.

In R3F, prefer drei's `shaderMaterial(uniforms, vertex, fragment)` + `extend`, then drive uniforms from a `useFrame` ref, not React state (avoid re-renders).

## 3. WGSL essentials (WebGPU)

- Entry points: `@vertex fn vs(...) -> @builtin(position) vec4f` and `@fragment fn fs(...) -> @location(0) vec4f`.
- Uniforms live in a `struct` bound via `@group(g) @binding(b) var<uniform> u: U;` — respect **std140-like alignment** (a `vec3<f32>` occupies 16 bytes; pad explicitly).
- No implicit conversions: `1` is `i32`, `1.0` is `f32`, `1u` is `u32`. Be explicit.
- Texture sampling: `textureSample(tex, samp, uv)` in fragment stage only.

## 4. Coordinate and color correctness (the usual bugs)

- **UV origin**: GL textures are bottom-left origin. Three sets `texture.flipY = true` by default for images; for render targets it is false. Flip `vUv.y` if the image is upside down.
- **Aspect ratio**: correct with `uv.x *= resolution.x / resolution.y` (or `uv = (uv - .5) * vec2(aspect, 1.) + .5`) or circles become ellipses.
- **NDC vs UV**: `gl_Position` is clip space; `gl_FragCoord.xy` is in pixels — divide by resolution for 0..1.
- **Color space**: three renders linear then converts on output (`renderer.outputColorSpace = SRGBColorSpace`). Sample color textures as sRGB (`texture.colorSpace = SRGBColorSpace`); keep data textures (normals, roughness) linear. Do lighting math in linear space.
- **Tone mapping**: if `renderer.toneMapping` is set, raw emissive colors get remapped — account for it.
- **Premultiplied alpha / blending**: set `transparent: true` and the right `blending` mode; unmultiplied vs premultiplied changes edges.

## 5. Portability pitfalls that fail silently on some GPUs

- Always set `precision highp float;` in `RawShaderMaterial`/raw WebGL; test `mediump` behavior for mobile (banding, precision loss).
- WebGL 1 GLSL: **no dynamic (non-constant) array indexing**, no `while`/non-constant loop bounds; unroll or use textures.
- `mod(x, y)` and `%` differ for negatives; `pow(negative, y)` is undefined — clamp/abs first.
- Integer division truncates; write `1.0/3.0`, not `1/3`.
- Derivatives (`dFdx`/`dFdy`, `fwidth`) need `#extension GL_OES_standard_derivatives : enable` in WebGL 1 (built in for WebGL 2 / GLSL 3).
- Avoid heavy branching in fragment shaders; prefer `mix`/`step`/`smoothstep`. Both branches of a divergent `if` may execute.
- Never `normalize()` a possibly-zero vector without guarding.

## 6. Technique quick-reference

- **Shaping**: `step`, `smoothstep`, `mix`, `clamp`, `fract`, `mod` — the vocabulary of procedural graphics.
- **SDF / raymarching**: distance functions + sphere tracing. Reach for Inigo Quilez's primitives and the raymarching loop; use `Lygia` for ready functions.
- **Noise**: gradient/simplex (`glsl-noise`, `webgl-noise`, `lygia`). Value noise for cheap, simplex for smooth.
- **Post-processing**: render to a target, sample in a fullscreen pass; in three use `pmndrs/postprocessing` or `EffectComposer`.
- **GPGPU**: encode state in float textures, ping-pong render targets (three `GPUComputationRenderer`), or WebGPU compute shaders.

Pull ready-made functions from **Lygia** (cross-language GLSL/WGSL) instead of reimplementing noise, easing, SDFs, and color conversions.

## 7. Debugging workflow

1. **Isolate**: output a known value (`gl_FragColor = vec4(vUv, 0, 1)`) to confirm the pass runs and UVs are sane.
2. **Visualize the variable**: pipe any intermediate to color (`vec4(vec3(d), 1.0)`) rather than guessing.
3. **Check the console** for shader compile/link errors — WebGL reports the exact line; WebGPU logs validation errors. Read them.
4. **Confirm uniforms are actually set** (typos in uniform names fail silently — the value stays 0).
5. Use **Spector.js** (WebGL) or the **WebGPU Inspector** to capture the draw call, uniforms, and compiled shader.

## 8. Authoritative sources to consult

When unsure of an API, consult these rather than guessing (many are LLM-ingestible `llms.txt`):

- Three.js: https://threejs.org/docs/llms.txt (incl. WebGPURenderer + TSL)
- React Three Fiber: https://r3f.docs.pmnd.rs/llms.txt · drei: https://drei.docs.pmnd.rs/llms.txt
- WGSL spec: https://www.w3.org/TR/WGSL/ · WebGPU: https://www.w3.org/TR/webgpu/
- WebGL/WebGPU Fundamentals: https://webgl2fundamentals.org · https://webgpufundamentals.org
- SDFs & raymarching: https://iquilezles.org/articles/
- Lygia (reusable functions): https://lygia.xyz

## 9. Before you finish

- State the target you assumed (WebGL2/WebGPU, Three.js material type) if it was ambiguous.
- Verify it compiles (no console errors) and **describe or screenshot** the visual result — a shader that compiles can still render black.
- Keep uniforms named consistently between JS and GLSL; a mismatch is the most common "nothing happens" bug.
