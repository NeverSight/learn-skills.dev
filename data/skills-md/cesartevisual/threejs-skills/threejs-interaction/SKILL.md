---
name: threejs-interaction
description: "Implement Three.js pointer picking, orbit controls, object dragging, selection, and synchronized HTML controls."
---

# Picking and Controls

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Choose controls based on the task and preserve ordinary page scrolling outside the interactive area. Define pointer, touch, keyboard, and HTML equivalents for important actions. Keep selection in application state keyed by stable IDs rather than temporary mesh indices alone.

Convert client coordinates using the actual event viewport rectangle: x = 2 * (clientX - left) / width - 1; y = 1 - 2 * (clientY - top) / height. For scissored views use that view's rectangle. Ignore zero-sized views. Raycast only relevant roots/layers and account for descendants, instance IDs, and front/back-face behavior.

Distinguish a click from a drag using travel thresholds. Use pointer capture when dragging beyond the canvas; handle pointercancel and lost capture. Temporarily suspend orbit controls while object manipulation owns the gesture, then restore them on every exit path.

For drag planes and transform gizmos, convert world results into the object's parent space. Scale constraints and hit tolerances to the use case. Visible shader deformation may not match CPU raycasting; use proxy geometry or another picking method when needed.

Throttle expensive hover work to rendered frames, reuse allocations, and dispose controls/listeners. Verify an offset canvas, touch cancellation, nested transforms, occlusion, keyboard selection, and selecting an instance after list updates.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/Raycaster.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
