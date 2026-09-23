---
name: threejs-particles
description: "Build Three.js particle systems, point clouds, large repeated datasets, and CPU or GPU simulations."
---

# Particles and Large Data

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Define particle count, lifetime, spawn rate, interaction, and target devices before choosing Points, instanced geometry, or a GPU simulation. Choose representation based on appearance and measured bottlenecks; many transparent pixels can cost more than many vertices.

Allocate fixed-capacity buffers, recycle slots, and update typed arrays without per-frame object churn. Use deterministic seeds when reproducibility or visual tests matter. Keep application identifiers independent of reused buffer slots.

Budget point size and transparent overdraw. Point-size limits vary by device; use quads when larger sprites are necessary. Sort or approximate transparency intentionally. For GPU deformation, maintain conservative bounds and matching interaction behavior.

For GPU simulation, define ping-pong resources, initial conditions, precision requirements, and backend support. Reset both simulation state and presentation time. Avoid unnecessary readbacks; if CPU interaction is needed, use coarse proxies or a deliberate sampling strategy.

For point-cloud datasets, stream spatial chunks, cull by chunk, and adjust detail to projected size. Preserve coordinate origins and units rather than uploading huge world coordinates blindly.

Verify count changes, maximum lifetime, resizing, reset reproducibility, sustained memory use, mobile fill rate, and fallback behavior without the compute path.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/Points.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
