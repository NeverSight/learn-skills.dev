---
name: threejs-compatibility-fallbacks
description: Fallback unavailable WebGPU features through an isolated compatibility branch. Use only when the user explicitly requests a fallback after verified WebGPU unavailability; then classify canonical behavior as preserved, weakened, or removed.
---

# Three.js Compatibility Fallbacks

Treat fallback as an explicitly authorized product branch. Canonical WebGPU/TSL
work and native WebGPU quality tuning remain with their owning skills.

## 1. Activate the branch

Record all of the following before selecting an implementation:

- the user's explicit request for unavailable-WebGPU fallback;
- either a positively identified initialized non-WebGPU backend, or a
  reproducible capability-related initialization failure on the named target;
  record which state occurred, rather than inferring a backend from a missing
  `isWebGPUBackend` property;
- the canonical owner and exact feature;
- the accepted scope of visual, physical, temporal, interaction, performance,
  and maintenance loss;
- the compatibility branch's maintenance owner.

Inspect backend identity only after `await renderer.init()` succeeds. In r185,
`renderer.backend.isWebGLBackend === true` positively identifies the initialized
WebGL backend; an absent/unknown flag is not proof. When initialization rejects,
record its exact error and leave initialized-backend identity unknown. Route an
application/configuration exception through debugging instead of disguising it
as unavailable hardware. When WebGPU initializes, return to the canonical owner.
Without an explicit fallback request, report the canonical blocker. Clean up the
probe's resources/listeners using the installed API's initialized or partial-init
cleanup path, and use a separate fresh canvas for a different renderer stack.

This step is complete when the five activation facts are recorded and the
canonical implementation remains unchanged.

## 2. Classify canonical behavior

List the canonical feature's geometric, radiometric, color, temporal,
interaction, state-ownership, and lifecycle invariants. Classify each one:

- `preserved`: the same quantity and proof still apply;
- `weakened`: keep the quantity, name the changed error, support, cadence,
  staleness, or envelope, and freeze a new gate;
- `removed`: mark the capability unsupported and remove dependent claims.

At a cross-system boundary, preservation means retaining the same units,
frames/origin, time interval and sample phase, owner, producer/consumer version,
support/filter, validity/staleness/error, rate-versus-integrated semantics,
one-way or two-way reaction scope, stable identity, immutable previous/current
presentation state, reset behavior, and GPU completion dependency. An
approximation with different semantics is weakened or removed. Keep
steady-frame GPU-to-CPU readback outside frame-critical paths.

This step is complete when every canonical claim has exactly one disposition
and every weakened or removed row names its user-visible consequence.

## 3. Select the first honest representation

Use this order for each feature:

1. precomputed or static canonical output when interaction can be removed;
2. bounded CPU/offline generation with declared upload cadence, latency,
   allocation, and lost dynamics;
3. feature removal with matching UI/documentation and claim removal;
4. an isolated legacy branch after explicit maintenance acceptance.

Read
[the downgrade matrix](references/downgrade-decision-matrix.md) when selecting
among unavailable capabilities. Read the
[r185 API map](references/r185-api-map.md) only when implementing or verifying
the legacy/API branch; reverify each symbol against the installed revision.

This step is complete when the selected representation is the earliest row
that passes every `preserved` invariant and every `weakened` invariant's frozen
gate, and every remaining loss is explicit.

## 4. Isolate ownership

Give the compatibility branch separate imports, build/deployment entrypoint,
tests, artifacts, capability gate, and maintenance ownership. Keep one scene
signal graph and one tone-map/output-transform owner inside the branch. Record
color versus data texture domains, resource creation/reset/resize/disposal, and
the boundary between canonical and compatibility assets.

When a node-renderer branch needs GPU timestamps, construct it with
`trackTimestamp: true` before initialization. Classic `WebGLRenderer` has no
such option or `resolveTimestampsAsync()` API; it needs its own supported,
validated timer-query instrumentation or an insufficient-evidence verdict.
A legacy branch may use
`WebGPURenderer( { forceWebGL: true } )` only after activation; it remains a
compatibility product rather than the canonical renderer. Choose one coherent
stack: `WebGPURenderer` with its WebGL backend retains the node-material/TSL and
`RenderPipeline` model; `WebGLRenderer` uses classic `ShaderMaterial` and
`EffectComposer` APIs. `forceWebGL` does not turn the former into the latter.
Do not share incompatible materials, passes, render targets, or renderer-specific
resources between these stacks. Preserve application state and restore its
controls through explicit branch adapters, not by retaining old GPU objects.

This step is complete when disabling or deleting the compatibility entrypoint
leaves the canonical build and runtime graph unchanged, and every branch-owned
resource has one owner and disposal path.

## 5. Validate the changed claims

Invoke `$threejs-visual-validation` for every preserved or weakened claim when
it is installed. With that owner, use canonical evidence as truth, capture only
the views, traces, and diagnostics that produce the claim, and exercise its
applicable reset, resize/DPR, transition, teardown, and dispose/recreate paths.
Persistent resources must plateau after declared warm-up.

If the owner is absent, report it and return `INSUFFICIENT_EVIDENCE` for the
affected claims; do not construct replacement validation inside this skill.
Missing timestamps likewise make required GPU attribution
`INSUFFICIENT_EVIDENCE`; presentation or CPU duration is end-to-end evidence
only.

This step is complete when every surviving claim has a verdict, every removed
claim is absent from product language, output conversion has one owner, and
lifecycle/resource claims either plateau or fail under validation or remain
`INSUFFICIENT_EVIDENCE` with the missing evidence named.

## Output

Return one row per feature:

| Feature | Target | Preserved | Weakened | Removed | Representation | Validation |
| --- | --- | --- | --- | --- | --- | --- |

Also record the activation facts, isolated entrypoint and maintenance owner,
output owner, lifecycle result, unsupported claims, any missing verification
owner, and the exact evidence needed for each `INSUFFICIENT_EVIDENCE` verdict.
