---
name: blender-create-model
description: Create or refine a Blender mesh from a subject and dimensions; use for individual props or characters, not whole environment assembly.
---

# blender-create-model

## Inputs and scope

Accept subject, scale, silhouette, intended use; default to editable source plus preview. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Establish official MCP readiness and turn the subject/style into a brief; identify what already exists.
2. Choose units, dimensions and proportion landmarks before detail.
3. Create a named task collection; record existing objects and checkpoint before replacing geometry.
4. Block out primary masses with primitives or a low-resolution mesh.
5. Inspect front, side and three-quarter views; resolve proportion errors before topology detail. For a grounded pose or placed prop, verify the actual lowest visible contact against its support surface; nominal centers or bounding boxes can leave rounded feet or bases floating. Preserve intentional hovering or airborne poses.
6. Refine silhouette and secondary forms; choose modifiers for editable construction.
7. Add only detail visible at the intended viewing distance; separate reusable parts. Check how secondary forms meet: supports, frames, trim, and accessories must not accidentally cross openings or conceal defining features. For containers and enclosed props, inspect the end panels, interior walls, lid closure and all sides after assembly; a hero angle can hide missing surfaces. Judge thickness and contact at final image size, not only in a close viewport.
8. Check normals, accidental internal faces, transforms and topology appropriate to deformation/export. Ngons are not universally invalid.
9. Render modest final views and inspect them against the brief at intended display size.
10. Save the editable blend and provide object names, dimensions, previews and unresolved limitations.

## Execution notes


Prefer scale-aware bevels and intentional shading. For characters, establish facial/body landmarks and pose requirements before adding accessories. A render-ready static model is not automatically animation-ready.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
