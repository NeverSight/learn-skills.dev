---
name: threejs-debugging
description: "Diagnose Three.js black canvases, missing meshes, wrong colors, flicker, picking bugs, and context loss."
---

# Rendering Diagnostics

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Capture the visible symptom, console errors, failed requests, installed versions, backend, and a minimal reproduction before editing. Use [the symptom tree](references/diagnostics.md) to narrow likely causes.

For a blank canvas, first verify nonzero container/drawing dimensions, a live render loop, successful renderer creation, camera projection/framing, object visibility/layers, and valid finite transforms. Replace only the subject material with an unlit diagnostic material to distinguish lighting from geometry problems.

For asset failures inspect HTTP status, response content, CORS, decoder paths, and build base path. An HTML fallback response with status 200 is not a valid GLB. For color, trace texture classification through lighting, tone mapping, and output conversion.

For flicker inspect coplanar geometry, near/far precision, transparency sorting, duplicate render loops, and competing transform writers. For picking verify canvas/view-relative coordinates, matrices, layers, instancing, and shader deformation mismatch.

Reduce the failing scene one feature at a time while preserving evidence. Avoid unrelated dependency upgrades or disabling all error checks to make symptoms disappear. When context/device loss occurs, provide a clear recovery path rather than an unbounded renderer recreation loop.

Verify the original failing action after the fix and check adjacent states that share the same code. Explain the cause and evidence, not just the changed line.

## API reference

Consult the [official documentation](https://threejs.org/docs/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
