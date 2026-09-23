---
name: threejs-accessibility
description: "Make Three.js interactions usable with keyboards, assistive technology, reduced motion, and non-3D fallbacks."
---

# Accessible 3D Experiences

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Identify what information and actions the 3D view communicates. Decorative scenes can be hidden from assistive technology; meaningful scenes need an accessible name/description and an equivalent way to obtain essential information.

Expose meaningful actions as native HTML buttons, inputs, lists, and status text synchronized with the same application state. A canvas label alone does not make individual 3D objects accessible. For configurators, expose options and selected values outside the canvas; for charts, provide a table or textual summary.

Implement visible focus, logical tab order, keyboard alternatives for rotate/zoom/reset/select, and an escape from captured interaction. Avoid hijacking page keys when focus is outside the viewer. Pointer-only drag should have an alternative when needed to accomplish the task.

Respect prefers-reduced-motion and changes to that preference. Remove nonessential camera travel, parallax, auto-rotation, and flashing; offer stable states and pause controls. Use contrast, text labels, and shape in addition to color.

Provide useful loading, failure, and unsupported-device HTML. Announce significant state changes without announcing every frame or hover. Test with keyboard alone, browser zoom, reduced motion, a screen reader where available, and WebGL unavailable. Report untested assistive technology explicitly.

## API reference

Consult the [official documentation](https://www.w3.org/WAI/WCAG22/quickref/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
