---
name: threejs-shaders
description: "Write and debug Three.js GLSL shaders, custom material effects, uniforms, and shader deformation."
---

# Custom Shaders

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Identify the renderer, installed revision, shader language, and material extension mechanism before writing shader code. Use GLSL ShaderMaterial/RawShaderMaterial in a compatible pipeline; do not assume a WebGL shader is a drop-in WebGPU material.

Write down spaces for every position, normal, light vector, and varying. Transform normals correctly under nonuniform scale. Keep uniforms stable and update their values rather than rebuilding materials per frame. Avoid unnecessary per-fragment work and dynamic shader permutations.

Build effects incrementally: constant output, coordinates, texture sample, then the effect. Check compile/link logs with full errors enabled. Guard normalization of zero vectors, divisions near zero, and undefined smoothstep ranges. Derivatives require the appropriate stage and support.

When displacing vertices, update normals or calculate suitable shading, expand bounds for culling, and consider matching depth/distance materials for shadows. CPU raycasting still sees CPU geometry unless a matching solution is provided.

Treat onBeforeCompile and shader chunks as revision-sensitive. Use an appropriate custom program cache key when custom compile variations need distinct programs, and retain a reproducible shader fixture for upgrades. Verify display color/tone mapping at the output boundary.

Check extreme parameter values, resizing, mobile precision, transparent overlap, shadows, and picking. Preserve an ordinary material fallback when the feature is optional.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/ShaderMaterial.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
