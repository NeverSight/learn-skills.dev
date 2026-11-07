---
name: blender-game-export
description: Export Blender assets for a specified game engine with scale, pivot, material and animation checks.
---

# blender-game-export

## Inputs and scope

Accept target engine, format and budgets; ask when target differences materially affect output. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and choose the destination engine/format.
2. Inspect source geometry, transforms, materials and actions.
3. Set budgets from actual target constraints rather than universal polygon limits.
4. Create an export copy or isolate selection; preserve editable source.
5. Normalize units, orientation, pivots and transforms intentionally.
6. Adapt materials and texture channels to supported target features.
7. Prepare requested clips, collision proxies and LODs with explicit naming.
8. Export only scoped content to a fresh output path.
9. Reimport into an isolated collection/scene; compare size, pivot, materials and clips, then test target engine if available.
10. Deliver source/export files and separate structural verification from unavailable engine checks.

## Execution notes

GLB is a useful default only when the destination accepts glTF. Blender procedural shaders may need baking. Do not claim collision/LOD naming is engine-compatible without checking that engine's importer.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.


For glTF in a multi-scene file, use both selected-object and active-scene export scoping; verify the reimported object set. Parent skinned meshes to their armature while preserving world transforms before exporting, and review the exporter warnings.

Compare animation duration in seconds as well as clip names: reimport into a different scene FPS can change frame numbers while preserving timing. Distinguish imported scene meshes from auxiliary bone display shapes. Normalize the intended skinned-mesh origin to the rig root before export if the destination bakes mesh transforms.
