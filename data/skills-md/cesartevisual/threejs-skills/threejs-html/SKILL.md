---
name: threejs-html
description: "Integrate Three.js with responsive HTML, Next.js or other frameworks, scroll sections, overlays, and multiple views."
---

# Web and Framework Integration

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the framework's client/server boundary, routing lifecycle, stacking contexts, and layout before inserting a canvas. Create the renderer only in a browser lifecycle. Do not access window or WebGL at server module evaluation time.

Reserve a stable canvas area in CSS and observe its container. Keep semantic headings, controls, forms, and searchable product information in HTML. Use the existing design system for loading, error, and fallback states. Lazy-load heavy 3D code when it is not needed for the initial view.

Define pointer routing explicitly between overlays and the scene. Avoid a full-page invisible canvas intercepting links or touch scrolling. For scene-anchored labels, project world positions and handle behind-camera, occlusion, viewport clipping, and readable placement.

For multiple product thumbnails, consider one shared renderer with scoped viewports or static previews instead of a context per card. Scissor rectangles and event coordinates must use the same view bounds. Pause or invalidate offscreen content according to actual motion requirements.

Keep route cleanup safe during async loading and development remounts. Verify page scrolling, browser zoom, nested scroll containers, layout shifts, navigation away and back, reduced motion, and content availability when rendering fails.

## API reference

Consult the [official documentation](https://threejs.org/manual/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
