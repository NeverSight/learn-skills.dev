---
name: threejs-scene
description: "Build or correct Three.js scene hierarchies, camera framing, coordinate transforms, and responsive renderer lifecycles."
---

# Scenes, Cameras, and Math

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the host element size, renderer ownership, world scale, handedness, up axis, and camera type before changing the scene. Prefer a single renderer for one experience; use viewports/scissors when multiple views genuinely benefit from shared resources.

Separate imported model transforms from interaction pivots using groups. Distinguish local and world coordinates; update world matrices before synchronous bounds or coordinate queries when transforms just changed. Use quaternion interpolation for orientations and reusable vectors in hot paths. Avoid repeatedly converting between Euler angles and quaternions.

Fit a perspective camera against object bounds and both horizontal and vertical field of view; fitting only height can crop a wide subject. Choose a positive near plane and useful far plane for perspective depth precision. Orthographic cameras may use a zero near plane. Update the projection matrix after projection changes.

Size from the canvas container with ResizeObserver, skip zero dimensions, and keep CSS size separate from drawing-buffer size. Apply a deliberate pixel-ratio budget. Update camera, renderer, and size-dependent render targets together. Do not overwrite layout CSS with renderer sizing.

Use one render-loop owner. setAnimationLoop integrates with XR; an existing framework or requestAnimationFrame loop can be valid outside XR. Stop the loop, disconnect observers, remove listeners, and release owned GPU resources on teardown. Renderer disposal alone does not dispose scene resources.

Verify a non-square container, mobile orientation, hidden-to-visible transitions, repeated mounting, and framing of unusually wide or tall assets.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/PerspectiveCamera.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
