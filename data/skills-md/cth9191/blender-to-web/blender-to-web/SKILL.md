---
name: blender-to-web
description: Build interactive website sculptures from Blender assets, including the export-to-Three.js handoff, live motion, fallbacks, and visual verification. Use for Blender-backed living hero sections or adapting the included working reference.
---

# Blender to Web

Turn an art direction into an editable Blender scene and a working browser interaction. This skill adds the handoff to the browser; it does not replace general Blender modeling, rigging, or rendering guidance. Use available Blender specialist skills when those tasks need them.

## Start with the intended interaction

Decide what must respond to the visitor: whole-object rotation, separate moving parts, skeletal joints, soft deformation, or playback of a fixed animation. Read [the workflow](references/workflow.md) for the relevant route. A GLB does not carry Blender's simulation engine into a website. State which behavior is exported and which is implemented in the browser.

Resolve the user's concept, visual reference, product story, target viewport and mobile behavior from their brief. A concept image can establish composition, silhouette and materials before modeling; it is not proof that the 3D implementation will match it. Do not default every project to infinity, charcoal/yellow, tiles, or this demo's page layout.

## Preserve the durable source

Keep deterministic Blender Python, the editable .blend, the runtime export, material roles, part IDs and rest transforms. Record the exact Blender version and export settings. Model repeated elements as linked geometry where appropriate. Export stable part names and ordering when browser code uses them.

Inspect a fresh import of the actual exported asset and fixed views, then inspect the actual browser result. Cycles lighting and simulation are not automatically reproduced by glTF/Three.js.

## Use the reference selectively

- For the proven repeated-part path, read [infinity anatomy](references/infinity.md). The runnable reference is [assets/reference-project](assets/reference-project). Copy it into a new destination with `python scripts/new_project.py DESTINATION`; never edit the installed reference as a new project.
- For guide-driven fiber deformation, read [fiber lessons](references/fibers.md). Included source extracts illustrate the architecture; they are not a standalone second demo.
- For concept, modeling and implementation briefs, use [prompt recipes](references/prompts.md). Exact recovered image prompts are linked separately from newly written recipes.

The infinity adapter contains geometry-specific counts, material names, tile IDs and pulse ordering. When replacing geometry, explicitly update that contract. Do not feed an unrelated asset to it and assume it is a generic model viewer.

## Browser finish

Separate pointer intent: hover affects a local region, drag rotates after a movement threshold, click toggles only if no drag occurred. Keep rest transforms and bounded motion; for springs use a fixed simulation step with elapsed-time caps. For a moving assembly, transform the pointer ray into local coordinates.

Choose instancing, skeletal animation, shaders or a solver according to the asset. Preserve pause, offscreen/hidden-page suspension, context-loss cleanup and an appropriate fallback. APERTURE uses a still for coarse pointers, reduced motion and data saving; that is a useful precedent, not a requirement for every mobile product.

Compose the website around the sculpture. If it stays pinned while scrolling, give the text clear spatial progression unless the user prefers a stationary crossfade. Keep outgoing text out of keyboard focus and away from fixed navigation.

Verify representative idle, hover, drag, expanded, reset, paused, scroll and fallback states that the project actually implements. Measure draw calls, triangles, payload, frame time and device/GPU. A fast result on a desktop GPU is not evidence for phone or integrated-GPU performance. The reference measurements are historical examples, not universal budgets.

Deliver source, export, poster, runnable page, verified states and limitations. Repository publication, hosting and paid generation remain separate user-directed actions. Preserve dependency licenses.
