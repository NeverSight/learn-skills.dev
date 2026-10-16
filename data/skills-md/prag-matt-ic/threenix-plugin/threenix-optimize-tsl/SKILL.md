---
name: threenix-optimize-tsl
description: Review and refactor TSL shader node graphs for performance, clarity, and portability. Use when the user invokes $threenix-optimize-tsl or asks to optimize Three.js Shading Language (TSL) code.
---

# Review and refactor TSL node graphs for performance, clarity, and portability

## Goal

Review and refactor the provided **TSL TypeScript** shader logic (nodes + material slots) to reduce GPU cost and improve readability **without visible regressions**.

For full TSL documentation refer to: https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language

**Success criteria**

- Visual output is indistinguishable under normal viewing (small numeric drift is acceptable).
- No feature regressions; public APIs (uniforms, exported functions, material slot assignments) remain compatible unless explicitly justified.
- Fewer or cheaper instructions in the bottleneck stage and no added texture fetches unless justified.
- Code stays in TSL (no raw GLSL strings).

## Inputs

- Current TSL sources (TypeScript) and where they are bound (material slots, post-processing pass, compute).
- (Optional) Active light count, material flags, pipeline notes, target backend (WebGL2/WebGPU).

## Procedure (follow in order)

1. **Establish evidence + stage mapping**
   - State the suspected bottleneck and the evidence for it. Treat vertex/fragment/bandwidth limits as hypotheses until profiling supports them; pass timing alone does not identify the limiting stage.
   - Map the heavy work to stage: `material.positionNode`/`geometryNode` is vertex-stage, `material.colorNode`/`fragmentNode`/postprocessing is fragment-stage.
   - Note any `vertexStage()` / `varying()` usage and whether it matches the actual consumption site.
   - When benchmarking is requested or a suitable local fixture is available, use the standalone `$threenix-benchmark-webgpu` skill to measure the actual target graph. Capture its baseline **before editing** and an unchanged repeat to establish noise. If that skill or a faithful fixture is unavailable, state the limitation and keep performance estimates unmeasured.

2. **Static audit (find issues)**
   - Unused or redundant nodes, uniforms, varyings, or cached vars (`toVar`).
   - Implicit or unclear type conversions; prefer explicit `float/vec*` or `.to*()`.
   - Hot ops in fragment: trig (`sin/cos`), `pow`, `exp`, divisions, conditionals/loops, multiple texture fetches.
   - Recomputation: repeated expressions or UV transforms; missing `toVar()`/`toConst()` where reuse matters.
   - Interface bloat: `varying()` created but only used in vertex stage (use `vertexStage()` instead).
   - Particle storage: audit buffer bindings, padded strides, and compatible `vec3` + scalar pairs using [Particle buffer management](#particle-buffer-management).

3. **Plan (write before changing code)**
   - List concrete edits you will make, ordered by expected impact (largest -> smallest), tied to the identified bottleneck.
   - Note any quality trade-offs and why they are acceptable.

4. **Refactor (apply changes)**
   - **Move work out of fragment when acceptable:** use `vertexStage()`; use `varying()` only when fragment truly needs it.
   - **Cache and reuse:** use `.toVar()` for repeated expressions; `.toConst()` or `float/vec*` for literals.
   - **Explicit conversions:** use `float/vec2/vec3/vec4` or `.toVec*()` for clear types.
   - **Reduce branching:** replace `If/Else` with `mix/step/smoothstep` when visually safe.
   - **Texture discipline:** sample once and reuse; keep UV math minimal; avoid duplicate `texture()` calls.
   - **Function hygiene (TS safe + pure):**
     - Use `Fn()` for reusable node functions.
     - Prefer typed tuple/object params (e.g., `[t, a]: [t: VarNode, a: VarNode]`).
     - Add `/*#__PURE__*/` (or `/*@__PURE__*/`) to exported `Fn()` for tree-shaking.
     - Use `.setLayout({ name, type, inputs })` for exported helpers to lock in typings.
   - **Uniform updates:** use `uniform()` for dynamic values; prefer `uniform.onFrameUpdate/onRenderUpdate/onObjectUpdate` over captured mutable JS state.
   - **Keep interfaces lean:** only emit nodes/varyings that are actually consumed; preserve slot semantics.

5. **Output (deliverables)**
   - **Measured comparison, when captured:** use `$threenix-benchmark-webgpu` with the same fixture/settings and saved baseline after edits. Inspect output differences and repeat A/B runs before claiming a win. Report GPU pass timing separately from stage hypotheses and application FPS; include artifact paths and any inconclusive result.
   - **Findings table**
     | Issue | Location | Severity | Fix summary |
     | ----- | -------- | -------- | ----------- |
   - **Refactor plan** (bulleted, 5-10 lines).
   - **Refactored code**: updated **TSL TypeScript** node code.
   - **Change diff**: minimal unified diff or `changes` tool entries.
   - **Impact estimate**: which stage should get cheaper and why (e.g., removed N trig ops per fragment), clearly distinguished from measured results and compiler-dependent assumptions.
   - **TODOs**: further safe optimizations or optional quality dials.

## Checks (single consolidated checklist)

- **Bottleneck-aligned:** Optimization focuses on the limiting stage (vertex vs fragment).
- **Stage-correct:** `vertexStage()`/`varying()` usage matches where results are consumed.
- **Type clarity:** conversions are explicit; no accidental JS math or type drift.
- **Redundancy removed:** repeated work cached or hoisted with `toVar()`/`toConst()`.
- **Branching minimized:** replaced with branchless math where safe.
- **Texture fetches minimized:** no duplicate samples; UV math kept light.
- **Function hygiene:** `Fn()` usage is pure, typed, and layouted when exported.
- **Interface stable:** material slots, uniforms, and public function signatures remain compatible.
- **Particle buffers:** packed lanes preserve initialization/reset semantics, CPU strides match GPU layout, and each stage fits the device's binding limits.
- **Readability maintained:** clear naming; minimal noise; portable across WebGL2/WebGPU where possible.

## Notes & guardrails

- Do **not** change color spaces, tonemapping, or gamma unless explicitly requested.
- Preserve semantic behavior; call out any intentional approximations.
- Avoid raw GLSL strings or `onBeforeCompile`; keep logic in TSL nodes.
- If a backend limitation applies (WebGL2 vs WebGPU), document it explicitly.

## Particle buffer management

### Pack related data into existing lanes

For 32-bit floats, a WGSL storage `array<vec3<f32>>` has a **16-byte element stride**, despite each vector containing only 12 bytes of data. `array<vec4<f32>>` also has a 16-byte stride. A separate scalar storage array adds 4 bytes per particle and another binding: packing `vec3` + `float` into one `vec4` reduces their combined storage from **20 to 16 bytes per particle** and two bindings to one. This follows [WGSL alignment and size rules](https://www.w3.org/TR/WGSL/#alignment-and-size); it is a layout saving, not a measured frame-time improvement.

- Prefer position `.xyz` + lifetime `.w`, velocity `.xyz` + scale `.w`, or colour `.rgb` + palette/sprite index `.w` when the values share a particle count and compatible access patterns.
- Document every lane at allocation. Update all initialization, spawn, reset, compute, rendering, and CPU upload/readback consumers together. Mutate `.xyz` when changing position so a whole-vector assignment cannot erase lifetime in `.w`.
- Allocate CPU-packed data as `Float32Array(count * 4)` with offsets `index * 4`; changing only the TSL type from `vec3` to `vec4` reinterprets the data incorrectly. Three's WebGPU backend pads three-component storage attributes, but padding does not populate your extra semantic lane.
- Keep geometric math on `.xyz`: distance, length, normalization, and dot products must not include lifetime or metadata. Explicitly pass `.xyz` to `positionNode` and `.rgb` to `colorNode` when `.w` has another meaning.
- Pack small metadata fields into `vec2`/`vec4` when it removes bindings. Do not promote every scalar or `vec2` to `vec4`: storage arrays of `f32` and `vec2<f32>` already have 4- and 8-byte strides. Nor does changing a lone `vec3` to an unused `vec4` save memory.
- Preserve integer semantics: float lanes can represent small palette/batch indices exactly, but are not a substitute for arbitrary 32-bit integer IDs or flags. Use integer storage or an explicit bit-preserving representation when required.

TSL pattern, with `particleCount` supplied by the owning component:

```ts
import { Fn, instanceIndex, instancedArray, vec4 } from 'three/tsl'

// xyz = position, w = remaining lifetime
const positionLifeBuffer = instancedArray(particleCount, 'vec4')
const initialize = Fn(() => {
  positionLifeBuffer.element(instanceIndex).assign(vec4(0, 0, 0, 1))
})().compute(particleCount)

// Inside compute: use element(instanceIndex).xyz and .w separately.
const positionNode = positionLifeBuffer.toAttribute().xyz
```

### Budget bindings per shader stage

**8 is the default `maxStorageBuffersPerShaderStage` limit in core WebGPU, not a universal maximum number of buffers per program or scene.** It counts storage-buffer binding entries visible to a stage across the pipeline layout's bind groups, including read-only storage. Initialization and update compute pipelines have separate budgets. Uniform buffers, vertex buffers, and textures have separate limits. See [WebGPU limits](https://gpuweb.github.io/gpuweb/#limits).

- Inspect the actual `GPUDevice.limits.maxStorageBuffersPerShaderStage`; an adapter advertising more does not mean the created device enabled more. Higher limits must be supported and requested at device creation (`requiredLimits`; also supported by Three's WebGPU renderer). Prefer packing before raising the application's hardware requirements.
- Count generated bindings for each compute/render pipeline, including non-particle storage used by helpers or renderer features. Keep headroom instead of treating all eight slots as particle-owned. Compatibility mode can impose lower vertex/fragment storage limits; verify the target backend rather than assuming core limits everywhere.
- Check `count * stride` against `maxStorageBufferBindingSize` and the allocation against `maxBufferSize`. Packing reduces binding pressure but does not remove buffer-size limits.
- Reuse the same storage node for compute and drawing through `.toAttribute()` when appropriate; do not copy GPU results back to the CPU to feed a second render buffer. Verify generated vertex inputs and bindings: vertex attributes have their own budget, and moving a read to a different stage changes where it counts.

### Preserve ownership and update behavior

- Keep allocations stable until count or source data changes. Seed static data once; update mutable state on the GPU. Copy cached source arrays before exposing them as mutable storage, but retain a separate immutable rest-position buffer when the simulation needs it.
- Initialize a new allocation before updates or drawing consume it, and reset initialization state when buffers are replaced. Audit disposal on replacement/unmount through the project's existing resource ownership mechanism; `useMemo` alone does not free GPU storage.
- In-place writes are suitable when each invocation owns its particle and reads only stable inputs. For neighbor reads, use a stable input snapshot/separate output or separate dispatches as appropriate; packing does not fix cross-invocation read/write races. Avoid merging fields written by different invocations without checking ownership of the resulting vector stores.
- Skip or throttle dispatches only when stored render values remain valid. Hiding a mesh does not stop compute. Preserve queued events and the final update that settles opacity/position; use elapsed simulation time rather than one render-frame delta when updates skip frames.

### Retrieve particle references through MCP

The installed skill does not include the Threenix monorepo or component sources. When a concrete reference would help, call `get_component_reference` on the `threenix` MCP server with one of the following arguments and inspect the returned `files[]`. Fetch only the reference relevant to the optimization; do not assume local `packages/` or `apps/` paths exist or copy a component into the user's project just to review it.

| Tool arguments                                 | Pattern to inspect                                                                                                                                                                                                 |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `{ "slug": "fireworks" }`                      | Position/life, velocity/scale, RGB/sprite frame, and batch/seed/phase/scale-fade metadata packed into `vec4`s; lane-specific initialization, spawning, and updates; elapsed simulation time for throttled updates. |
| `{ "slug": "linked-particles" }`               | Position/life packing; opportunities to combine velocity and seed after auditing all readers/writers. Include link-output storage in binding counts and review neighbor reads during position writes for races.    |
| `{ "slug": "mesh-surface-sampled-particles" }` | Separate initial and mutable positions preserve the rest shape; do not remove the immutable buffer merely to reduce the buffer count.                                                                              |

Treat returned sources as authoritative: inspect their current layout rather than assuming these patterns are unchanged or fully optimized. If the tool or server is unavailable, report that the reference could not be retrieved; do not reconstruct it from local or bundled sources. The self-contained guidance above can still be applied to the user's supplied code.

For buffer refactors, verify initialization, respawn/reset, count changes, lane preservation, binding validation, and visual parity. Measure performance with the same fixture before claiming a speedup.
