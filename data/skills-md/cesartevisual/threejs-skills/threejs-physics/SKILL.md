---
name: threejs-physics
description: "Integrate Rapier or another physics engine with Three.js, including colliders, fixed timesteps, and render synchronization."
---

# Physics Integration

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the existing engine and its version; preserve it unless the requested behavior requires a change. Initialize its WASM/runtime before creating the world. Establish units, gravity direction, collider scale, and authority over each transform.

Advance simulation with a fixed timestep and a bounded accumulator. Cap substeps and explicitly choose whether to discard excess elapsed time after a stall. Interpolate previous/current physics poses for rendering when needed. Avoid stepping the simulation from multiple loops.

Prefer primitive or compound colliders where they reproduce the interaction adequately. Check engine restrictions for dynamic triangle meshes, scaling, and convex hulls. A visual mesh is not automatically a stable collider. Use continuous collision detection selectively for fast bodies after measuring its cost.

Move kinematic bodies through engine APIs; do not write render transforms and expect physics to follow. Apply forces/impulses at the intended cadence, and handle sleeping and collision event lifetime. Keep event processing from triggering duplicate UI actions.

Release world objects and listeners on teardown. Test collisions at the highest expected velocity, resting stability, low frame rates, tab resume, scale changes, and repeated resets. Do not promise deterministic cross-platform replay without testing the selected engine and configuration.

## API reference

Consult the [official documentation](https://rapier.rs/docs/user_guides/javascript/integration_parameters/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
