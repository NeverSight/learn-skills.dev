---
name: threejs-dynamic-surface-effects
description: State-transition screen-space surface effects for Three.js WebGPU/TSL. Use for persistent touch, frost, or thaw history; full-field or sparse accumulation; static crystalline fields; reduced-resolution blur; or history-gated normal refraction.
---

# State-Transition Dynamic Surface Effects

Own viewport-locked appearance history and its composite. Route world/object
residue to `$threejs-particles-trails-and-effects`, weather accumulation to
`$threejs-rain-snow-and-wet-surfaces`, bounded water to
`$threejs-water-optics`, and shared full-frame output decisions to
`$threejs-image-pipeline`.

When temperature, phase, loading, wetness, contact, or weather drives the
appearance, close this local handoff before step 1:

- name the physical quantity and units, producer frame/origin, transform and
  origin generations, and projection into screen UV;
- name the source interval, cadence, sample phase, immutable producer/version,
  and renderer consumer;
- declare support/filter, validity, staleness, error, and missing-signal policy;
- bind the GPU resource generation, producing and consuming passes, and
  completion dependency;
- keep the physical source read-only and give screen history its own appearance
  version; reset it on incompatible clock, origin, transform, projection, or
  resource-generation changes.

Invoke `$threejs-choose-skills` when feedback or additional system owners are
required. The physical owner retains authority; screen-UV history remains
renderer-owned appearance state.
Then read [external appearance signals](references/ping-pong-accumulation.md#external-appearance-signals)
for local projection and reset rules.

## Process

### 1. Define the state transition and ownership

Write one contract for:

- each history channel and its dimensionless meaning;
- the screen-space event shape, timestamp, pressure/strength, and UV origin;
- evolution terms such as decay, deposition, diffusion, or no change;
- the state clock, suspension/seek policy, and reset dependencies;
- the one history writer, composite consumer, and final output owner;
- any external physical signal and the decorative overlay kept separate from it.

For touch/frost history, a useful split is visible coverage in `R` and a
smoother tilt/refraction response in `A`; `G/B` remain unused or explicitly
diagnostic. The step is complete when every channel has one equation, writer,
unit domain, clock, and consumer.

### 2. Select update topology

Choose from the state transition rather than the visual theme:

| Transition | Update topology |
| --- | --- |
| Decay, diffusion, or forcing changes most texels | Full-field ping-pong compute |
| Deposits are sparse and untouched texels are invariant | Event bounds or dirty tiles |
| Sparse state also decays | Timestamped tiles with analytic catch-up on every visible/filter sample, or materialize every visible tile |
| Many events overlap | Bin events to tiles; bound/compact lists or rasterize one aggregate deposit field |
| State and inputs are unchanged | Idle: retain history and dispatch nothing |

Diffusion uses a full field or halo-expanded active domain. Read
[update topologies](references/ping-pong-accumulation.md#update-topologies)
for overlap cost and diffusion stability. The step is complete when untouched
texels evolve exactly as the chosen model requires and idle frames schedule no
state work.

### 3. Make time and event integration invariant

Derive `dt` from two ordered samples on the same clock. Treat equal samples as
zero elapsed time. A missing previous sample, reversal, seek, invalid mapping,
or discontinuity follows the declared freeze, reset, analytic catch-up, or
bounded-substep policy.

Rasterize timestamped pointer motion as swept capsules with aspect from the
history texture. Integrate decay and saturating deposition together so a held
pointer and a swept gesture converge independently of render-frame count.
Subdivide event intervals only when their pressure or coverage variation
exceeds the declared error gate.

Read [dt-correct history](references/ping-pong-accumulation.md#dt-correct-history)
before implementing decay, deposition, or diffusion. The step is complete when
the same timed input yields equivalent history at 30, 60, and 120 Hz and a
suspension does not silently discard elapsed evolution.

### 4. Allocate the ping-pong graph

Use `WebGPURenderer` from `three/webgpu`, call `await renderer.init()`, and
require `renderer.backend.isWebGPUBackend === true` for this canonical path.
Route explicit WebGPU-unavailable teaching to
`$threejs-compatibility-fallbacks`.
Allocate two renderer-owned `StorageTexture` histories at the lowest measured
extent/format that passes reconstruction and quantization tests. Keep history,
scene color, blur intermediates, and static structure fields as separate
resources.

Order the graph:

```text
immutable external appearance signals + timestamped UI events
  -> write next history from previous history
  -> publish/swap the completed history generation
single scene pass
  -> optional separable blur at its owned reduced extent
  -> static structure + current history composite
  -> optional history-gated normal refraction
  -> one RenderPipeline output transform
```

Use `Fn().compute(...)`, `storageTexture()`, and `textureStore()` for history
updates. Enqueue with `renderer.compute(...)`; r185 `computeAsync()` is not a
GPU-completion fence. Keep the steady path readback-free. Mark/rebuild the
render graph when the output node, diagnostic route, resource extent/format, or
quality branch changes.

Read [resources and r185 execution](references/ping-pong-accumulation.md#resources-and-r185-execution)
before allocating or swapping textures. The step is complete when every pass
reads a committed generation, no pass samples the texture it writes, and the
scene is rendered once.

### 5. Compose blur, structure, and refraction

Generate static crystalline/noise fields once at startup or when their extent
or quality changes. Treat them as data with `NoColorSpace`. Use separable blur
at a pass-owned reduced resolution and alpha-aware normalization when alpha
participates. Build the composite and refraction as TSL nodes feeding
`RenderPipeline.outputNode`.

Keep scene and working buffers linear/HDR until the single output conversion.
Use screen-period uniforms as periods; derive texel dimensions from the actual
resource. Gate refraction by structural coverage and current history, define
normal wrap and source-edge behavior, and apply Fresnel in linear light.

Read [composite and refraction](references/ping-pong-accumulation.md#composite-and-refraction)
when either branch is active. The step is complete when blur extent, texture
domains, UV conventions, refraction bounds, and output conversion are each
owned and visible in diagnostics.

### 6. Close the lifecycle

Choose one resize policy: clear both histories, remap, or depth/camera-aware
reprojection. Reset or reproject on incompatible clock, origin, transform,
projection, resource generation, representation, or quality changes. Ordinary
continuous source-version advances are sampled rather than reset.

On idle, retain persistent state and stop update work. On resume, apply the
declared time policy before accepting new input. On disposal or device loss,
invalidate the history generation and release both histories, blur/static
resources, compute/pipeline nodes, and input/resize listeners; create a fresh
generation before the next draw.

Read [resize, reset, and disposal](references/ping-pong-accumulation.md#resize-reset-and-disposal).
The step is complete when resize, seek, quality change, idle/resume, disposal,
and device loss each have an explicit state transition and resource result.

### 7. Prove state and presentation

Expose previous history, deposit, next history, dirty tiles/active texels,
scene color, blur axes, static fields, pre/post-history mask, refraction offsets,
final-without-refraction, and final. Add pause and single-step controls.

Measure event count, tile-list occupancy, dispatched texels, history and
intermediate bytes, traffic lower bound, dispatch/draw timing, and whole-frame
p50/p95. Scale by stopping idle work, choosing a valid sparse path, then
reducing history/blur extent or precision after state-equivalence tests.

Read [resource accounting](references/ping-pong-accumulation.md#resource-accounting)
and [diagnostics and failure signatures](references/ping-pong-accumulation.md#diagnostics-and-failure-signatures).
The skill is complete when timed inputs match across 30/60/120 Hz; full,
sparse, and idle transitions behave as selected; ping-pong generations never
alias; resize/reset/disposal controls pass; physical inputs remain read-only;
the frame loop performs zero history readbacks; the scene renders once; output
conversion has one owner; and the complete scene meets its named memory,
traffic, and timing budget.
