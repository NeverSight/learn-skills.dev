---
name: threejs-product-viewer
description: "Build Three.js product viewers with material variants, camera presets, hotspots, configuration state, and image export."
---

# Product Viewers and Configurators

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the model's mesh/material names, units, variant structure, camera targets, and business options. Define a stable mapping from product choices to render changes rather than coupling UI labels to arbitrary mesh array positions.

Build a state model for selected options, availability, reset, and any URL persistence. Keep price/availability authority in the existing application data layer. Do not infer commercial facts from the model. Provide equivalent semantic HTML controls and selected-value summaries.

Apply variants to instance-owned material state while sharing immutable textures safely. Guard async texture/model switches against stale completion. Frame each preset for both wide and narrow layouts; constrain orbit/zoom only enough to keep the subject useful.

Place hotspots using stable anchors and handle occlusion/behind-camera states. Give users a reset view and a clear escape from dragging. Match materials under controlled lighting before adding dramatic effects that obscure product details.

For screenshots, render explicitly at the capture size and restore renderer/camera state afterward. Capture immediately after rendering or use a suitable target/readback pipeline; preserveDrawingBuffer is not universally required. Handle cross-origin restrictions and decide whether HTML overlays belong in the export.

Verify all valid option combinations or representative boundary combinations, rapid switching, reset, deep links, export framing, mobile controls, and failed assets.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/WebGLRenderer.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
