---
name: threejs-scalable-real-time-shadows
description: Fit scalable directional cast shadows in Three.js r185 WebGPU/TSL. Use when choosing one bounded shadow, CSM, tiled arrays, or cached clipmaps; stabilizing projection, filtering, or bias; or fixing invalidation, caster parity, bindings, or sustained cost.
---

# Scalable Real-Time Shadows

Directional shadows are a fit problem: fit the smallest light-space
representation that covers required caster-to-receiver rays, then spend work on
the projection, filter, and updates receivers actually use.

`$threejs-choose-skills` is an optional multi-system coordinator. Use
`$threejs-visual-validation` for capture/readback evidence.

## 1. Choose one topology

Compare the same seeded workload, projection, filter, and receiver policy:

| Gate | First r185 WebGPU branch | Cost topology |
| --- | --- | --- |
| A bounded receiver/caster volume passes world-texel and depth-precision gates | one `DirectionalLight` shadow | one view, one depth texture, one filter evaluation |
| Camera-depth coverage changes continuously | `CSMShadowNode` | `L` shadow views/maps; normally one active filter, two in a fade |
| One fixed orthographic footprint is partitioned spatially | `TileShadowNode` | one depth array, `N` backend layer passes, `N` containment tests, and a union render list that can draw each caster in every layer |
| Very large coverage persists and measured reuse survives invalidation | custom cached clipmap | `L` persistent levels; selected updates; `L` portable filters or one/two target-proven array/atlas filters |
| Casters deform or change broadly each frame | one fitted shadow, CSM, or a same-light static/dynamic split | Cache invalidation approaches full redraw. |

Core and Tile shadow targets retain color-bearing attachments beside depth; VSM
adds distribution/blur resources and passes. `TileShadowNode` updates all layers
together and is not a persistent tile cache.

Classify consequential numbers as **Derived** from bounds/equations,
**Authored** intent, **Gated** limits, or target **Measured** evidence.

**Complete when:** one topology is selected from measured draw/raster/receiver/
binding/reuse pressure, every rejected branch has a failed gate, and no copied
map size, level count, bias, or millisecond promise drives the choice.

## 2. Fit projection, texels, filtering, and bias

- Fit XY to required biased receiver coordinates plus filter, snap, and coverage
  guards. Fit Z independently to receivers and every occluder on their light
  rays; XY texel width does not define a valid Z quantum.
- Use one stable directional-light basis and global/light anchor. Snap each
  committed center to its fixed `dx/dy` grid with one deterministic quantizer.
  A basis/sign/anchor change starts a new content epoch.
- Derive filter support from the actual Basic/PCF/PCFSoft/VSM implementation and
  backend. Reserve that support inside containment and match world footprints
  across blends.
- Treat `normalBias` as a world-space normal offset and `bias`/`biasNode` as a
  normalized comparison-depth offset. Derive and validate them separately.

When stabilizing crawl, seams, acne, or peter-panning, read
[projection, filter, and bias mechanics](references/cached-clipmap-shadows.md#projection-filter-and-bias).

**Complete when:** slow sub-texel motion is stable; every XY/Z boundary remains
covered; filter support cannot escape its domain; and front-facing, grazing,
thin-contact, and cross-level fixtures pass under the selected depth convention.

## 3. Gate the exact r185 implementation

Initialize WebGPU before inspecting capabilities:

```js
await renderer.init();
if ( renderer.backend.isWebGPUBackend !== true ) {
  throw new Error( 'Directional shadows require WebGPU.' );
}
```

Attach a custom node through `light.shadow.shadowNode` before the affected
material/light graphs build. A runtime change requires every affected graph and
pipeline to rebuild and pass disposal/recreation.

When using core, CSM, Tile, reversed depth, or custom shadow hooks, read the
[r185 source gates](references/cached-clipmap-shadows.md#r185-source-gates) for
clone omissions, depth comparisons, layer behavior, transform conventions, and
lifecycle caveats.

**Complete when:** revision/imports, backend/depth policy, camera ownership,
shadow target type, layer behavior, material bind layout, and every selected
built-in caveat have a fixed-scene diagnostic or a rejected configuration.

## 4. Build an explicit custom cache only when selected

Each level owns distinct state:

```text
desired  = next coverage request
rendered = center/range/content encoded into an inactive target
committed = exact valid target and parameters sampled by receivers
dirty    = desired coverage differs, while committed content may remain valid
invalid  = committed depth no longer represents required content
```

Receivers sample committed state only. Invalid levels contribute zero weight;
the next valid coarser level inherits the remainder, and unresolved outer
coverage is lit. Correctness invalidations outrank age/quality refreshes.

Freeze desired center, depth interval, basis epoch, and content epoch; render;
restore renderer state; then atomically commit center, interval, target/layer,
matrix, and rendered epoch only after rechecking that content, basis, and
resource versions were not superseded. Preserve newer invalidations. Filter,
normal-bias, and fade changes also revalidate guarded coverage and dependent
resources before reuse. Work encoded after the current presentation seal
uses an inactive resource generation and commits to the next presentation;
the prior committed generation remains immutable until its consumers finish.

When a custom cache is selected, read the
[cache state, scheduling, and sampling contract](references/cached-clipmap-shadows.md#cached-clipmap-state-and-sampling)
before implementing it.

**Complete when:** rendered metadata matches its inactive target; committed
metadata matches the resource receivers sample; desired state differs only
while committed coverage remains valid; first-use state is invalid; failed
updates preserve only still-correct commits; late updates cannot mutate a
sampled generation; and every invalid level is excluded until repaired.

## 5. Invalidate swept causes and preserve caster parity

Track light basis; caster previous/current transform; geometry/LOD; visibility,
layer, and cast flags; alpha/mask/coverage; deformation envelope; asset/chunk
generation; and resource identity. Union or sweep previous/current conservative
caster silhouettes so vacated and newly occupied shadow depths both invalidate.

A central change can intersect every nested full map. When that redraw is too
expensive, use non-overlapping ownership, paged residency, proxies, or a dynamic
overlay inside the same light/shadow node. A second directional light would
duplicate illumination.

Visible and shadow passes share local-space deformation and alpha/coverage.
`positionNode` and `castShadowPositionNode` are local-space hooks;
`receivedShadowPositionNode` is world-space receiver lookup and is validated
separately.

For the invalidation event table, swept receiver influence, and parity contract,
read [swept invalidation and caster parity](references/cached-clipmap-shadows.md#swept-invalidation-and-caster-parity).

When another system supplies light/caster motion, rebasing, or presentation
cadence, bind units, coordinate frame, current/previous sample times, authority,
version, resource generation, validity, staleness, and reset conditions before
use. The shadow cache remains sole writer of its desired, dirty, invalid,
rendered, and committed state.

**Complete when:** every content dependency maps to redraw, sampling-only update,
or no-op; every moved/deformed caster invalidates its swept old/new influence;
and visible/caster silhouette parity passes for morphing, skinning, instancing,
batching, sidedness, layers, and alpha coverage.

## 6. Validate sustained behavior and lifecycle

Capture committed coverage/weights, light depth, filter support, bias, invalid
fallback, caster parity, binding layout, target inventory, and fixed final views.
Exercise camera crawl; all XY/Z boundaries; cross-level fades; localized and
broad invalidation; light-basis changes; resize/DPR; multi-camera use; update
spikes/debt; and dispose/recreate.

Measure warmed, thermal-steady CPU/GPU frame quantiles, shadow view draws and
triangles, vertex/raster/alpha work, receiver filter evaluations, traversal,
allocations, bindings, invalid coverage, and update spikes. Optimize the
measured bottleneck rather than a topology proxy.

For binding/resource inventory, workload equations, and acceptance gates, read
[binding, workload, and validation](references/cached-clipmap-shadows.md#binding-workload-and-validation).

**Complete when:** rendered output matches the selected baseline and diagnostic
causes; stale invalid content is never sampled; adapter and product headroom
gates pass; sustained frame and spike gates pass; and detaching the node,
targets/textures, cloned shadows/lights, storage, listeners, and debug resources
returns counters to baseline.

## Ownership

This skill owns directional shadow projection, filtering/bias, caster parity,
cache state/invalidation, receiver sampling, and shadow diagnostics. The scene
owner supplies caster/light inputs; the pipeline owner controls shared output
and temporal-radiance rejection caused by changed shadow content.
