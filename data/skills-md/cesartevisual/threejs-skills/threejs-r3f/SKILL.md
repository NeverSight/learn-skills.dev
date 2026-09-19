---
name: threejs-r3f
description: "Build or fix React Three Fiber scenes, Drei helpers, Suspense loading, events, and React lifecycle integration."
---

# React Three Fiber and Drei

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect React, react-dom, Fiber, Drei, and Three.js versions and peer dependencies together. Match the reconciler to React; do not assume every Fiber major supports every React major. Read helper APIs from the installed Drei version.

Let Canvas own the renderer and loop unless an intentional custom integration requires otherwise. Use Fiber hooks within Canvas descendants. Keep browser-only canvas code behind the framework's client boundary; preserve server-rendered product content outside it.

Use declarative scene ownership and refs for continuous mutations in useFrame. Avoid React setState for per-frame motion; reserve state for meaningful UI transitions. Memoize expensive imperative resources when needed, with explicit release rules. Hook selectors reduce irrelevant subscriptions but do not make nested mutable Three.js values reactive.

Place appropriate Suspense and error boundaries around async content. Loader caches may share geometry, textures, and materials; do not mutate or dispose shared entries as if they were instance-owned. Primitives and externally supplied resources need explicit lifecycle handling. Clone scene instances, and use skeleton-aware clones for skinned models.

Use demand rendering for mostly static scenes only when all imperative changes and ongoing damping trigger invalidation. Inspect Drei helper behavior before adding a duplicate loop or control update. Positive useFrame priority takes over rendering; account for who renders afterward.

Test Strict Mode mounting, route transitions, rapid asset switching, loading failure, pointer propagation through overlapping meshes, and an idle demand-rendered scene. Keep equivalent HTML actions available.

## API reference

Consult the [official documentation](https://r3f.docs.pmnd.rs/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
