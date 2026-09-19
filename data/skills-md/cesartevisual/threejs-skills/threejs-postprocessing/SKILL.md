---
name: threejs-postprocessing
description: "Add or debug Three.js bloom, antialiasing, ambient occlusion, depth effects, and render-target composition."
---

# Postprocessing Pipelines

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Identify the existing renderer and composer family before adding passes. Three.js WebGL EffectComposer, pmndrs postprocessing, and WebGPU node pipelines have different contracts. Choose one coherent pipeline for the requested backend.

Write down the render order, intermediate color space, target precision, depth requirements, alpha behavior, and final display conversion. Apply tone mapping/output conversion once in the appropriate place. Compare against direct rendering before stacking effects.

Use HDR scene values and a deliberate threshold for selective bloom. Avoid making the entire interface glow to disguise weak lighting. Depth-dependent effects need compatible depth data and sensible camera planes. Antialiasing must fit the final composition rather than assuming canvas MSAA smooths offscreen targets.

Resize all passes and targets with viewport and quality changes. Budget full-resolution targets and reduce effect resolution or disable expensive passes on weaker devices. Preserve HTML readability and transparent-canvas composition if the design uses it.

Dispose owned passes and render targets, including replacement pipelines. Verify disabled/enabled comparison, bright and dark content, alpha edges, resize, and effect cost on the target device. Keep effect tuning separate from fixing incorrectly tagged textures.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/EffectComposer.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
