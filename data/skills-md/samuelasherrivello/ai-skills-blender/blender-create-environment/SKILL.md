---
name: blender-create-environment
description: Build a coherent Blender environment or modular scene from a setting; use for rooms, landscapes and scene assembly.
---

# blender-create-environment

## Inputs and scope

Accept setting, real-world scale, camera or traversal needs; default to a representative small area first. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify official MCP readiness; interpret setting, style and intended shots. When references are supplied, identify the visible cues that serve the brief (proportions, depth, surface response, context); distinguish quality references from layouts to reproduce and preserve explicit prompt choices.
2. Set units, reference heights and modular dimensions.
3. Plan floor layout, focal points, circulation and visible boundaries.
4. Block out architecture/terrain in a scoped collection, preserving the existing scene.
5. Develop one representative area and inspect its camera view before scaling the scene. Resolve construction depth and contact at the intended viewing distance: openings need recesses, edge thickness, and plausible backing when visible. A pane placed over an opaque wall is not an opening.
6. Build a reusable kit with consistent origins and snapping dimensions.
7. Place or scatter instances with a recorded seed; avoid obstructing required sightlines. Establish a few coherent secondary families instead of copying the hero treatment everywhere. Vary supported dimensions, openings, and condition purposefully; random variation alone does not make context believable.
8. Assign material families and establish broad lighting without hiding layout problems.
9. Inspect camera views, collisions when requested, instance count and render/viewport cost.
10. Save the scene, kit, seeds, views and measured limitations.

## Execution notes


Use instancing for repeated pieces. Check joins and silhouette repetition from the actual camera. Do not imply traversal or collisions were verified unless exercised in the target context.

Treat surrounding geometry as part of the shot and reflective environment. A detailed subject surrounded by flat placeholder masses can still look like a miniature. Budget secondary detail by visible contribution; do not add unrelated props just because a reference contains them. For stylized scenes, keep simplification deliberate and consistent with the subject.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
