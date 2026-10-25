---
name: blender-procedural-geometry
description: Create editable Geometry Nodes or Python generators in Blender with controlled parameters and reproducible output.
---

# blender-procedural-geometry

## Inputs and scope

Accept output geometry, exposed controls and ranges; choose Geometry Nodes for artist editing or Python for batch structure. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and define the generated geometry contract.
2. Choose named parameters, units, safe ranges and output-size limits.
3. Select Geometry Nodes or Python based on editability and dependencies.
4. Prototype the simplest valid output inside an owned collection.
5. Expose useful controls and document interactions rather than every internal constant.
6. Make randomness explicit and record a seed.
7. Exercise minimum, normal and maximum supported inputs; reject invalid counts before allocating objects.
8. Inspect topology, evaluated bounds, instance realization and execution cost. Inspect the generated result at the actual camera too: valid parameter ranges can still produce repetitive silhouettes, intersecting assemblies, or detail below the pixel scale. Keep construction rules separate from style choices so reusable generators do not impose one visual treatment.
9. Rerun with the same parameters; replace only owned output or create a distinct named run, never accumulate accidental duplicates.
10. Deliver the editable node group/script, parameter examples, seed and validation results.

## Execution notes

Test zero/one counts if supported, negative dimensions, and very large requested counts. Preserve node sockets by identifiers where practical; inspect the installed Blender API before constructing version-sensitive nodes.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
