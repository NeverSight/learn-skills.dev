---
name: threejs-performance
description: "Profile and optimize Three.js frame time, GPU workload, asset memory, and resource leaks."
---

# Performance and Memory

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Reproduce on a representative device and record scene state, viewport, pixel ratio, backend, asset sizes, and frame-time distribution. Distinguish first-load/decode/compile stalls from steady-state frame cost. Read [the profiling worksheet](references/profile.md) for a repeatable before/after record.

Determine whether the bottleneck is CPU work, submission/draw calls, GPU shading/fill, transfers, or memory. Reduce resolution to probe pixel cost; isolate shadows/effects; compare static versus animated updates. Change one major variable at a time.

Use instancing/batching when draw calls dominate, reduce overdraw/effect resolution when fill dominates, and simplify animation or move appropriate work off-thread when CPU-bound. Lowering triangles will not fix every bottleneck. Avoid per-frame allocations and repeated shader recompilation.

Define resource ownership across shared caches and instances. Release owned geometries, materials, textures, targets, controls, mixers, observers, and listeners. Disposing a material does not dispose its textures; disposing a renderer does not free all scene-owned objects. Do not dispose cache entries still in use.

Measure repeated mount/unmount and model replacement after warmup. Internal caches can leave nonzero counters; look for an unexplained rising trend rather than demanding zero. CPU heap and renderer.info are partial evidence, not exact GPU memory.

Accept an optimization only when the measured improvement preserves required appearance and interaction. Report device, method, before/after values, and limits of the measurements.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/WebGLRenderer.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
