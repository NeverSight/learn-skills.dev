---
name: threejs-black-holes-and-space-effects
description: Build curved-ray space effects in Three.js WebGPU/TSL. Use for artistic ray bending, Ellis wormholes, Schwarzschild black-hole lensing, accretion disks, physical thin-disk transport, or requests that need the Kerr/rotating-black-hole support boundary.
---

# Curved-Ray Space Effects

This skill owns three native claims: an artistic deformation, an Ellis
null-geodesic solution, or a Schwarzschild null-geodesic solution. A Kerr
result is owned by an independently validated external solver; without one,
return `unsupported-model`. Numerical integration alone does not turn an
artistic field into a metric solution.

## 1. Select the claim

| Requested observable | Select | Conditional reference | Completion criterion |
| --- | --- | --- | --- |
| Stylized bending, bounded glow, or a decorative disk | Artistic bounded ray | Read [artistic-rays-and-disks.md](references/artistic-rays-and-disks.md). | The implementation and its documentation say `artistic`, and fixed-view refinement bounds the visible change. |
| Traversal or turning through an ultrastatic spherical throat | Ellis wormhole | Read the Ellis section of [metric-rays.md](references/metric-rays.md). | The throat scale, exterior mapping, invariant, and `B < 1`, `B = 1`, `B > 1` regimes are explicit. |
| Nonrotating black-hole lensing or a physical thin-disk image | Schwarzschild | Read the Schwarzschild and physical-transfer sections of [metric-rays.md](references/metric-rays.md). | The mass scale, horizon, photon sphere, critical impact, invariant, continuous events, and observer/emitter frames are explicit. |
| Rotating black hole | Unsupported here | Integrate an independently validated Kerr solver as an external ray/transfer producer; a lens map is an optional reuse form. | The solver supplies its metric/sign conventions, constants of motion, tetrads, event semantics, and independent convergence evidence; otherwise return an unsupported-model result. |

**Complete when:** exactly one claim owns the ray path, and every visual claim
is no stronger than that branch's evidence.

## 2. Declare the numerical domain

Define before authoring the march:

- the effect-to-world transform and a finite local integration bound;
- the camera event, ray origin, normalized direction, and exterior side;
- one length basis for positions, steps, horizons/cores, and medium
  coefficients;
- the state vector, its integration parameter, its owner, and its valid time;
- the environment orientation and the orthonormal frame used for escaped-ray
  lookup;
- the pre-march results `miss`, `setup-rejected`, and `unsupported-model`;
  applicable continuous horizon, core, disk, shell, and proxy-exit surfaces;
  and the invalid-state, opacity, step-cap, and attempt-cap outcomes.

For metric rays, nondimensionalize with the Ellis throat radius `a` or the
Schwarzschild mass length `M = G M_SI / c^2`, while retaining the conversion
back to metres. Render delta never becomes a ray step. Preserve either spherical
metric through a similarity transform: translation, rotation, and uniform
scale. A nonuniform transform requires an explicitly derived transformed
metric and frame plus renewed invariant, event, and convergence validation;
otherwise reject it at setup.

Nonstationary metrics require an external solver that integrates or recovers
coordinate time and samples or interpolates metric and emitter state, with
validity and error, at every mapped integration evaluation. A frozen metric is
a quasi-static approximation only when its declared evolution-error gate
passes; otherwise report the model unsupported.

**Complete when:** every state component and event surface has a declared
basis, owner, and finite validity domain, and world-to-solver-to-render round
trips preserve the chosen scale and exterior. Each spherical metric uses a
similarity transform or supplies validated transformed-metric evidence, and
every nonstationary claim uses mapped coordinate-time sampling, is explicitly
labeled quasi-static with a passing evolution-error gate, or is unsupported.

## 3. Build one bounded march

Use `WebGPURenderer` with TSL node functions. Initialize the renderer and
confirm the WebGPU backend before selecting compute, storage, or MRT resources.
The canonical march is:

1. Transform the camera ray into effect space and intersect the finite bound.
   A miss returns `miss` before numerical work. An inadmissible initial state,
   unsupported transform, or invalid frame/domain returns `setup-rejected`
   before the march. A requested model without a supported native branch or
   admitted external solver returns `unsupported-model`.
2. Initialize position, tangent or canonical momentum, radiance,
   transmittance, event state, accepted-step count, and termination ID.
3. Propose one candidate segment. An error-controlled rejection changes only
   the next attempted step size.
4. Locate every applicable event continuously on the segment. Root-refine the
   earliest event; preserve ordered disk crossings when several contribute.
5. Accumulate the accepted segment's transfer, then commit exactly one state
   advance and increment the accepted-step count once.
6. After the march starts, terminate as `escaped`, `horizon`, `core`, `opaque`,
   `invalid`, `unresolved-critical`, `minimum-step`, `step-cap`, or
   `attempt-cap`.

The attempt cap bounds divergent work independently of the accepted-step cap.
`step-cap` bounds committed accepted steps; `attempt-cap` bounds accepted plus
rejected attempts. A curvature or distance heuristic may propose a step;
refinement against a tighter solution decides whether it is accurate.

**Complete when:** a trace proves one committed advance per accepted step,
rejected attempts leave physical and event state unchanged, every input
receives `miss`, `setup-rejected`, `unsupported-model`, or an explicit march
termination ID, and event residuals meet their declared bounds.

## 4. Resolve transfer and the escaped direction

Sample an exterior environment only for `escaped` rays. Reconstruct its lookup
direction from the integrated outgoing tangent in the declared orthonormal
frame; orbital position angle alone is not a direction. Bound or integrate any
far-field tail truncated by the proxy.

Keep transfer aligned with the claim:

- An artistic disk declares a scene-length basis and a linear-HDR source
  basis. Integrate extinction/emission front-to-back and label the result
  artistic.
- A physical disk uses ordered geodesic crossings, a named emitter
  four-velocity and observer tetrad, and invariant frequency transfer. Its
  geometry and orbital model must match the selected Schwarzschild claim.

Accumulate into linear HDR. One pipeline stage owns tone mapping and output
conversion; diagnostics that replace the output mark the pipeline graph dirty.

**Complete when:** misses and non-escaped terminations cannot sample an
exterior, the escaped tangent is finite and normalized, disk crossings retain
their order, and transfer units reduce to radiance.

## 5. Select direct work or reuse

Use a direct bounded march for changing lenses, sparse probes, or artistic
fields whose per-pixel work meets the target. Use a critical-split transfer
map for a static spherical Ellis or Schwarzschild lens when coherent reuse
beats direct integration. Use a local high-accuracy map near separatrices when
GPU `float32` direct rays miss the angular gate.

When a lens map, compute cache, or temporal reconstruction is selected, read
[lens-cache-and-history.md](references/lens-cache-and-history.md) before
allocating it. Keep the opaque scene and required depth at their required
resolution; scale only the effect pass whose error was measured.

**Complete when:** each cache or history resource has a reuse reason, a stable
identity, an invalidation rule, a completion/lifetime rule, and measured
benefit over the direct path.

## 6. Verify the selected claim

Use a deterministic, seeded environment with high-frequency directional
features so angular, critical-curve, and history errors remain visible. It is a
validation input generated by the project, not a bundled visual preset.

For every branch:

- capture termination, accepted/rejected attempts, event count/location,
  remaining transmittance, final direction, and invalid-state diagnostics;
- compare `h`, `h/2`, and `h/4` or an equivalent tolerance sequence at fixed
  rays and cameras;
- compare final angular error against the environment footprint and compare
  event residuals against the relevant geometric thickness;
- verify moved, uniformly scaled, camera-inside, miss, and far-from-origin
  bounds, plus nonuniform-scale rejection or the explicitly transformed metric;
- verify the required Three.js revision, backend, final-output owner, resize,
  reset, and disposal behavior.

Artistic rays pass when refinement preserves fixed-view silhouette,
termination class, ordered disk events, and radiance within declared bounds.
Ellis and Schwarzschild rays additionally require an independent CPU `float64`
reference, invariant drift, critical-regime classification, exterior/escape
agreement, and convergence of the final tetrad direction. A capped,
minimum-step, invalid, or unresolved-critical ray is diagnostic output rather
than physical evidence.

**Complete when:** every requested observable has a passing branch-specific
gate, every failure class is visible in diagnostics, and the final claim lists
the numerical and domain limits that remain.
