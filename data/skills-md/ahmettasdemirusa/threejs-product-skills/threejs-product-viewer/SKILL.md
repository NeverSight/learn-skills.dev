---
name: threejs-product-viewer
description: Build an interactive 3D product viewer for a website with three.js. The viewer loads a glTF/GLB model, frames it automatically, lights it like a studio and lets shoppers orbit and zoom. Use when the user wants a 3D product view, "show our product in 3D", a GLB/glTF viewer, a three.js product page, an e-commerce 3D model, or a rotatable model of furniture, shoes, bottles, electronics, cabinets or any physical product. Includes a tested starter template. For color/material options see product-configurator; for a no-code embed with AR see model-viewer-ar.
license: MIT
metadata:
  version: 1.0.0
  author: Ahmet Tasdemir
  three: "0.186.1"
---

# Three.js Product Viewer

Build a viewer that is **fast on phones, accurate in color, and framed well for any model**. Start from the tested template, then adapt it:

`templates/product-viewer.html` is one self-contained file. It uses three.js r186 from a CDN import map, so it needs no build step.

## Decide first: three.js or `<model-viewer>`?

| Need | Use |
|---|---|
| Just show a model, maybe with AR, with minimal code | `<model-viewer>` (model-viewer-ar skill) |
| Custom UI, a configurator, animations, several models in one scene, brand-specific effects | **three.js** (this skill) |
| No 3D model, only photos | A 360° image sequence (360-product-spin skill) |

## What the template already does, and why

1. **Import map** for `three` and `three/addons/`, pinned to one exact version.
   - Never mix versions.
   - Addons live under `three/addons/…`, which maps to `examples/jsm/`.
2. **Renderer**
   - `antialias: true` and `alpha: true`, so the page background shows through.
   - `setPixelRatio(Math.min(devicePixelRatio, 2))`. Uncapped DPR 3 phones render 2.25× the pixels for no visible gain.
3. **Color**
   - `toneMapping = THREE.NeutralToneMapping`, which keeps product colors close to the source.
   - ACES shifts saturated colors noticeably. AgX is available too.
   - `outputColorSpace` stays at the default sRGB.
4. **Lighting:** an environment map from `RoomEnvironment` through `PMREMGenerator`, set as `scene.environment`. PBR materials (the glTF default) look flat without an environment map; a single directional light is not enough.
5. **Shadow**
   - A `ShadowMaterial` ground plane that receives the shadow of one directional light. The shadow camera is fitted to the model's size.
   - Use `THREE.PCFShadowMap` and soften it with `shadow.radius`. **`PCFSoftShadowMap` was removed in r18x**; three.js warns and falls back.
6. **Auto-framing**
   - It computes a `Box3`, moves the model so it sits centered on the floor, and places the camera at a distance of `radius / sin(fov/2)`.
   - It sets `near`, `far`, `minDistance` and `maxDistance` from the model's size.
   - This works for a 5 cm ring or a 3 m sofa, and for models exported in centimetres.
7. **Controls:** `OrbitControls` with damping, panning off and `maxPolarAngle` just under 90° (no looking from under the floor). It auto-rotates until the first interaction, and not at all under `prefers-reduced-motion`.
8. **Render on demand:** inside `setAnimationLoop`, it renders only when `controls.update()` returns `true` (the camera moved) or something requested a render. An idle product page then uses almost no GPU or battery.
9. **Compressed assets:** `GLTFLoader` with `DRACOLoader`, `KTX2Loader` (with `detectSupport(renderer)`) and `MeshoptDecoder`, so optimized files load. See the 3d-asset-optimization skill.
10. **UX and accessibility:** a loading bar from the progress events, and an error message on failure. The canvas has `role="img"` and an `aria-label`.

## Adapting it

- **Model:** change `MODEL_URL`. Files must be served over HTTP; `file://` fails because of CORS. For quick tests use `?model=path/to/file.glb`.
- **Embedding in a page:** put the canvas in a sized container. The template uses a `ResizeObserver` on the container, not `window.resize`, so it works in grids, tabs and modals.
- **Several viewers on one page:**
  - Each needs its own renderer.
  - Lazy-init them with an `IntersectionObserver`, because browsers cap the number of live WebGL contexts, typically around 16.
  - Dispose renderers you remove.
- **Hotspots or annotations:** project a 3D point with `vector.project(camera)` into CSS pixels, and update it when rendering.
- **Branding:** change the ground shadow opacity, the environment intensity (`scene.environmentIntensity`) and the background (a CSS gradient behind the transparent canvas).

## Cleanup (SPAs, modals)

When removing the viewer, call:
- `renderer.setAnimationLoop(null)`
- `controls.dispose()`
- `renderer.dispose()`

Also traverse the model and dispose every geometry, material and texture. Otherwise GPU memory leaks with each open and close.

## Performance budget for product pages

| Item | Target on mid-range phones |
|---|---|
| Model download | < 2–3 MB compressed (optimize first) |
| Triangles | ≲ 100k for a single product |
| Textures | ≤ 2048², KTX2 or WebP; share materials |
| Draw calls | ≲ 50 (merge meshes that share a material) |
| Idle GPU | ~0 (render on demand) |

## Verify before shipping

1. Serve over HTTP and open the page. There must be no errors in the console.
2. Check it on a real phone. Rotate, then pinch to zoom: the controls must not scroll the page. The template sets `touch-action: none` on the canvas.
3. Compare the rendered color with the product photo. Adjust `NeutralToneMapping` exposure (`renderer.toneMappingExposure`) rather than editing the materials.
4. Check with reduced motion enabled: there should be no auto-rotation.

## Common mistakes

- **Loading from `file://`:** use a local server such as `npx serve` or `python -m http.server`.
- **Mixing three.js versions** between the core and the addons.
- **No environment map,** so PBR materials look black or dull.
- **An uncapped pixel ratio,** or rendering every frame while idle.
- **The camera at a fixed position,** so large or small models appear clipped or tiny. Frame with the bounding box instead.
- **Forgetting that glTF units are metres.** A model that looks 100× too big was exported in centimetres. Framing hides this, but lighting and shadow sizes depend on it.

## References

- three.js manual: https://threejs.org/manual/
- GLTFLoader docs: https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- glTF 2.0 specification: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
