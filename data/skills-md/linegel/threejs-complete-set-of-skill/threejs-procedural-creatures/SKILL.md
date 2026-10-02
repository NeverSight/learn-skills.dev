---
name: threejs-procedural-creatures
description: Compile procedural creatures for Three.js WebGPU/TSL. Use for generated body surfaces, semantic rigs or creature locomotion, or repeated procedural populations.
---

# Procedural Creatures

Build a creature as a compiler: a dimensioned spec produces stable body, rig,
pose, and population identities; runtime work advances only selected state. The
canonical path uses Three.js r185 `WebGPURenderer`, TSL, `NodeMaterial`, and
workload-selected storage. Imported skinned animation assets are a separate
pipeline rather than an extension of this skill.

## 1. Define the body contract

Name the requested observable, closest/farthest projected extent, morphology
envelope, pose/topology update frequency, visible population, target adapter,
world units/frame, final-output owner, and any habitat/support/water/weather
providers.

Classify the request into one or more branches:

| Branch | Creature owns |
| --- | --- |
| generated body | spec, field or segment compiler, shipping surface, materials |
| rig/locomotion | semantic slots, local pose, fixed-step or analytic motion, support-relative targets |
| repeated population | compatible geometry/material identities, pose pages, bounds, culling, LOD |

This step is complete when every requested observable has one owner, every
external input names its producer and sampling contract, and the topology,
pose, and population change regimes are explicit.

## 2. Select the shipping representation

Choose from connectivity, deformation, reuse, and projected error:

| Workload | Representation | Required proof |
| --- | --- | --- |
| fixed connectivity with changing pose | one extracted reference mesh plus validated skinning | topology, weights, deformation, bidirectional surface error |
| fixed connectivity with bounded morphology change | reference mesh, skinning, optional bounded local field correction | full-envelope Jacobian, inversion, correction and surface error |
| components may merge, split, open, or close | budgeted dynamic extraction or explicit unsupported result | topology events, cadence, transition and complete mesh validity |
| body is visibly separate rigid plates/links | closed articulated segment hierarchy | closed geometry, joint gaps/limits, transform parity |
| many bodies share topology | shared geometry/material plus fixed pose pages | compatible identity, dirty traffic, bounds and visible submission |
| small projected body | simplified mesh or orientation-aware impostor | view-cone silhouette error and transition hysteresis |

A concatenated capsule/primitive shell is a field diagnostic, not proof of a
manifold body. Choose one primary representation per range and state which
features or topology changes it cannot represent.

This step is complete when each range has one shipping representation, its
geometry/cache identity is defined, and every transition has a physical-pixel
error gate, hysteresis/dwell, simultaneous-memory budget, and reset action.

## 3. Compile the generated body

When a selected branch needs a field-derived body, extracted skin, skinning,
correction, semantic rig, creature locomotion, or repeated pose storage, open
only its applicable sections of [creature-body-systems.md](references/creature-body-systems.md):

- every selected branch reads [Spaces and state ownership](references/creature-body-systems.md#spaces-and-state-ownership)
  and [Spec and compiler](references/creature-body-systems.md#spec-and-compiler);
- generated-body work reads [Field and blend contract](references/creature-body-systems.md#field-and-blend-contract)
  and [Reference surface and correction](references/creature-body-systems.md#reference-surface-and-correction);
- rig or locomotion work reads [Pose and locomotion](references/creature-body-systems.md#pose-and-locomotion);
- repeated-population work reads [Repeated populations and rendering](references/creature-body-systems.md#repeated-populations-and-rendering);
- verification reads [Completion evidence](references/creature-body-systems.md#completion-evidence)
  for the selected branches.

When the body is a hierarchy of rigid shells or plates, read
[articulated-hard-shell-creatures.md](references/articulated-hard-shell-creatures.md).
Keep stable semantic segment/joint IDs, closed surfaces, parent-local pivots,
and one transform path for visible, shadow/depth, bounds, and motion vectors.

Compile heavy work before visibility: spec validation, topology, reference
surface or closed segments, weights, candidates, frames, geometry identities,
materials, and fixed page layouts. Spawning validates and writes active slots;
it does not construct geometry or compile pipelines.

This step is complete when all graph references and slots resolve, CPU/TSL
parity passes where applicable, emitted surfaces are valid over the declared
pose/morphology envelope, and every cached artifact resolves the complete
identity that affects it.

## 4. Build pose and locomotion only where requested

Pose remains creature-local; root motion is applied exactly once by the
instance transform. Use stable seeded variation and injected simulation time.
Closed-form motion samples time directly. Gait, springs, ropes, buoyancy, and
contact response advance at a fixed step owned locally or by the routed
simulation stage, with immutable previous/current states for presentation.
Reference-surface skinning applies pose times inverse bind in creature space.
Rigid joint-local segments follow their joint pose directly. Interpolate joint
rotations before hierarchy composition and keep previous-presented transforms
separate from fixed-step history for motion vectors.

For support-relative limbs:

1. batch required probes at one sample instant/version;
2. retain stable support/feature identity and the planted point in support-local
   coordinates;
3. form gait homes and swing arcs in the support tangent frame;
4. predict targets from body velocity relative to represented support-point
   velocity;
5. transform targets through the inverse root into body space;
6. solve IK with scale-relative reach/conditioning gates and publish any
   unresolved contact residual; recheck contacts after secondary writers, then
   update posed bounds.

When support, water, air, gravity, weather, or physical contacts participate,
define a handoff with units, frame/origin, interval or sample instant,
cadence/sample phase, producer/consumer/version, footprint/filter,
validity/staleness/error, and rate-versus-integrated meaning. Water-surface
motion and material current are distinct channels; missing represented data is
absence rather than a physical zero. Frame-critical decisions use an analytic
mirror, deterministic shared field, or batched provider with declared
latency/error rather than GPU readback.

One-way visual coupling returns no physical reaction. A two-way route sends
source/reaction quantities through the authoritative solver named by the
handoff. This skill owns creature pose and structural response, not private
terrain, water, wind, gravity, or contact state.

This step is complete when equal seed/tick/inputs reproduce pose, render cadence
cannot alter recurrent state, support-relative drift and limb-length residuals
pass, required provider channels are present with bounded error, and every pose
writer has a deterministic order with final contact/limit validation, not merely
a last-writer rule.

## 5. Scale the population and present once

Initialize the canonical renderer before allocating resources:

```js
import { WebGPURenderer } from 'three/webgpu';

const renderer = new WebGPURenderer({ antialias: false });
await renderer.init();
if (renderer.backend.isWebGPUBackend !== true) {
  throw new Error('WebGPU backend unavailable for the canonical creature path.');
}
```

- Share geometry only across compatible compiler/topology/geometry/tier
  identities. A species label alone is not a batch key.
- Store creature-local pose, root transform, bound, stable identity,
  representation, and history generation in fixed-capacity pages. Upload only
  coalesced dirty ranges.
- Use posed primitive/segment bounds or a proven conservative animation
  envelope. Cull pages and instances before submission.
- Bound shader loops by actual part/candidate count. Candidate evaluation keeps
  the authored blend ancestry and its omission certificates.
- Use one population ID/normal/depth edge pass for repeated outlines; reserve a
  duplicate iso-offset body for a measured hero branch.
- Reuse the same deformed local position in visible and cast-shadow paths;
  derive received-shadow lookup in world space.
- Decode authored sRGB once before linear uniform/storage use. One scene
  pipeline owns tone mapping and output conversion.
- Precompile every shipping display, depth/shadow, outline, and configured
  output variant before first visibility.

This step is complete when population pages have bounded capacity/lifetime,
static or unchanged poses cause no redundant recurrent work, bounds cull
correctly, visible/depth/shadow/motion consume one accepted pose generation,
and exactly one component owns final output conversion.

## 6. Verify representation, state, and lifecycle

Inspect final/no-post output plus the selected diagnostics:

```text
body: field/normal/candidate views, topology, skin weights, segment IDs,
      correction residual, inversions/intersections, silhouette
rig: slot/parent IDs, joint limits, radial frames, planted support and IK,
     previous/current pose and history generation
population: page occupancy, dirty ranges, posed bounds, culling, LOD/impostor,
            visible/shadow/depth/motion parity
```

Exercise fixed-seed replay; tick seek versus stepping; complete pose and
morphology envelopes; render hitches; sloped/moving support; missing, stale, or
discontinuous provider data; spawn/death/teleport/reparent/slot reuse;
topology/LOD change; resize; and disposal.

Report compiler/surface counts, field parity and surface error, locomotion drift
and convergence, visible/submitted pages and instances, dirty upload bytes,
field/correction evaluations, CPU fixed-step cost, whole-frame and paired-
marginal CPU/GPU p50/p95, peak live bytes, first-visible pipeline events, and
sustained target behaviour.

Failure signatures include primitive sheets shipped as a manifold body,
renaming parts changing a blend field, skin weights crossing touching limbs,
helper-axis frame flips, root transforms applied twice, render-dt gait,
support drift, water channels conflated, one mutable global population buffer,
unbounded shader loops, disabled culling, pose generations disagreeing across
passes, and resources/state surviving disposal.

Verification is complete when every selected representation, rig/locomotion,
population, output, reset, budget, and disposal gate passes; unselected branches
carry no required payload or evidence.

## Routing boundary

Use `$threejs-procedural-motion-systems` for general transform timelines and
springs, `$threejs-procedural-geometry` for generic mesh writers,
`$threejs-procedural-fields` for reusable fields/material coordinates,
`$threejs-procedural-vegetation` for plants, and
`$threejs-visual-validation` for target-scene visual contracts. This skill owns
procedural creature bodies, semantic rigs, creature locomotion, pose storage,
and repeated-population representation. Imported glTF clips, retargeting, and
VAT animation belong to an imported-asset character pipeline.
