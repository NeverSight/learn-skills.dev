---
name: threejs
description: 'Builds 3D web experiences with Three.js, WebGPU rendering, TSL shaders, and React Three Fiber. Covers scene setup, asset optimization, performance tuning, and React 19 integration. Use when creating 3D scenes, setting up WebGPU rendering, writing TSL shaders, optimizing draw calls, or integrating Three.js with React and Next.js.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://threejs.org/docs'
user-invocable: false
---

# Three.js

## Overview

Guides building high-performance 3D web experiences with Three.js, WebGPU-first rendering, TSL (Three Shader Language), and React Three Fiber. Covers scene architecture, asset compression, draw call budgets, and React 19 / Next.js integration patterns.

**When to use:** Creating 3D scenes, WebGPU rendering setup, TSL shader authoring, asset optimization (Draco/KTX2), React Three Fiber composition, Next.js streaming for 3D content, loading GLTF models, setting up lighting and shadows, animation playback and blending.

**When NOT to use:** 2D canvas animations (use Canvas API), simple SVG graphics, server-side rendering without client hydration, projects targeting pre-2022 hardware exclusively.

## Quick Reference

| Pattern           | API / Approach                                     | Key Points                                             |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------ |
| WebGPU renderer   | `import * as THREE from 'three/webgpu'`            | Must `await renderer.init()` before first render       |
| R3F canvas        | `<Canvas gl={...}>` with Suspense                  | Wrap in `<Suspense>` for streaming support             |
| Frame updates     | `useFrame((state, delta) => ...)`                  | Mutate refs directly; never use `setState`             |
| TSL shaders       | `import { ... } from 'three/tsl'`                  | Node-based; compiles to WGSL or GLSL                   |
| Instancing        | `<instancedMesh>` with matrix updates              | Single draw call for repeated geometry                 |
| Batched mesh      | `BatchedMesh` (r156+)                              | Different geometries sharing one material              |
| Draco compression | `gltf-pipeline -i in.gltf -o out.glb -d`           | Up to 90% geometry size reduction                      |
| KTX2 textures     | Basis Universal via `toktx`                        | Stays compressed in VRAM                               |
| LOD               | `THREE.LOD` with distance thresholds               | Swap detail levels by camera distance                  |
| On-demand render  | `<Canvas frameloop="demand">`                      | Only render when scene state changes                   |
| Cleanup           | `.dispose()` on unmount                            | Geometries, materials, and textures                    |
| Compute shaders   | `Fn(() => {...})().compute(count)`                 | GPU-side physics, particles, flocking                  |
| Lighting          | `DirectionalLight`, `SpotLight`, `HemisphereLight` | Enable `shadowMap` on renderer + `castShadow` on light |
| GLTF loading      | `GLTFLoader` + `DRACOLoader`                       | Draco for geometry compression; traverse for shadows   |
| Animation         | `AnimationMixer` + `clipAction()`                  | Update with `clock.getDelta()` every frame             |
| Crossfade         | `action.fadeOut()` / `action.fadeIn()`             | Weight-based blending between walk/run/idle            |
| Environment maps  | `RGBELoader` + `PMREMGenerator`                    | Set `scene.environment` for PBR reflections            |
| Raycasting        | `Raycaster.setFromCamera(pointer, cam)`            | Mouse/touch picking; use `recursive: true` for GLTF    |
| Morph targets     | `mesh.morphTargetInfluences[index]`                | Facial animation, blend shapes from GLTF               |

## Common Mistakes

| Mistake                                                                   | Correct Pattern                                                                 |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Allocating `new THREE.Vector3()` or `new THREE.Color()` inside `useFrame` | Pre-allocate outside the loop to avoid GC pressure every frame                  |
| Using `requestAnimationFrame` manually in React projects                  | Use R3F's `useFrame` hook for frame-by-frame updates                            |
| Not awaiting `renderer.init()` for WebGPU                                 | Always `await renderer.init()` before the first render to avoid race conditions |
| Loading assets without `<Suspense>` boundaries                            | Wrap `<Canvas>` in `<Suspense>` to prevent main thread blocking                 |
| Using high-poly models for background or distant elements                 | Use LOD (Level of Detail) or Impostors to reduce draw calls                     |
| Using `setState` inside render loop for animations                        | Mutate refs directly via `useFrame` for frame-by-frame updates                  |
| Speed tied to frame rate (`rotation += 0.01`)                             | Multiply by `delta` for frame-rate-independent motion                           |
| Not using `clock.getDelta()` for `mixer.update()`                         | Always pass delta time to `mixer.update(delta)` for correct animation speed     |
| Forgetting to dispose loaded GLTF models                                  | Traverse and dispose geometries, materials, and textures on removal             |
| Shadow map enabled on renderer but not on the light                       | Set both `renderer.shadowMap.enabled` and `light.castShadow = true`             |
| Large `far/near` ratio on camera                                          | Keep ratio small to avoid z-fighting; set `near` as large as possible           |

## Delegation

- **Asset and scene graph exploration**: Use `Explore` agent
- **Multi-file scene refactoring and optimization passes**: Use `Task` agent
- **3D architecture and rendering pipeline planning**: Use `Plan` agent

## References

- [Scene, lighting, and model loading](references/scene-and-lighting.md)
- [Animation system and blending](references/animation.md)
- [Performance and asset optimization](references/performance.md)
- [WebGPU and TSL shader patterns](references/webgpu-tsl.md)
- [React Three Fiber patterns and Next.js integration](references/r3f-patterns.md)
