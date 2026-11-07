---
name: blender-convert-3d-2d
description: Convert Blender models into consistent 2D views, sprites or sprite sheets using fixed cameras and frame metadata.
---

# blender-convert-3d-2d

## Inputs and scope

Accept model/subject, directions, frames, pixel size, pivot and transparency; establish 3D first. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and specify still views, sprite frames or packed sheet requirements.
2. Create or reuse a scoped 3D model and preserve its editable source.
3. Define direction order, frame ranges and animation timing.
4. Fix projection, camera distance/scale, output pixel size and pivot convention across views.
5. Set stable lighting and alpha; avoid changing exposure between directions.
6. Render one representative frame.
7. Inspect at final pixel size for silhouette, cropping and lost detail; adjust geometry or perform intentional cleanup.
8. Render all named views/frames with consistent settings and explicit ordering.
9. Use the packing helper for equal-size RGBA frames and record direction/frame/pivot metadata.
10. Inspect sheet and sequence at intended size; deliver model, individual frames, sheet and metadata.

## Execution notes

Use [scripts/pack_sprites.py](scripts/pack_sprites.py) within Blender, where bpy is available. Read --help via Blender --background --python script -- --help. Packing does not turn a 3D render into polished pixel art automatically. Nearest-neighbor display and deliberate cleanup may be needed.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
