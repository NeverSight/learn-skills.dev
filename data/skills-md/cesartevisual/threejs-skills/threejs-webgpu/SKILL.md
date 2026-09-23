---
name: threejs-webgpu
description: "Build or migrate Three.js WebGPURenderer, TSL node materials, and GPU compute features."
---

# WebGPU and TSL

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Check the installed Three.js exports and matching renderer/TSL documentation first. These APIs evolve quickly; use the project's pinned revision rather than mixing current snippets into an older install.

List required features and backend constraints. WebGPURenderer can use a WebGL backend when supported, but backend selection does not guarantee every compute or effect feature works on both. Test the actual selected backend. Do not replace a working WebGLRenderer unless the requested feature or migration warrants it.

Follow the revision's asynchronous initialization contract before rendering or capability-dependent setup. Handle initialization failure and unsupported devices with an explicit fallback state. Keep imports consistent with the renderer build to avoid duplicate class/module instances.

Express materials through supported node/TSL mechanisms. Port custom GLSL, shader patches, and composer effects intentionally; they are not automatically compatible. For compute, define storage layouts, bounds checks, dispatch sizes, synchronization, and readback frequency. Avoid per-frame CPU readback when data can stay on the GPU.

Manage compute buffers, render targets, and backend device loss according to current APIs. Avoid unbounded workload retries after initialization failure.

Verify on the requested WebGPU device/browser and any promised fallback backend. Report backend and feature results separately; a browser exposing navigator.gpu is not proof that this scene rendered successfully.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/WebGPURenderer.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
