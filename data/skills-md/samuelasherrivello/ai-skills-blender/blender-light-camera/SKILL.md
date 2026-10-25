---
name: blender-light-camera
description: Compose Blender shots and establish lighting, exposure and camera settings; use before final rendering.
---

# blender-light-camera

## Inputs and scope

Accept shot intent, framing, mood, aspect and projection; reuse a suitable existing camera. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and establish subject, mood and output framing.
2. Inspect scene bounds and important surfaces without altering geometry.
3. Select projection, focal length/orthographic scale and camera position deliberately.
4. Set and record color management and exposure baseline. For realistic work, check a neutral surface and dark region before tuning decorative lights; a flat world color or underlit environment can hide material differences even when direct shadows look plausible.
5. Place the key light to reveal shape and direct attention.
6. Add fill/rim/environment light only where it serves the shot.
7. Balance exposure and contrast; check highlights and dark regions.
8. Render a bounded preview using final aspect ratio. Fit the entire required subject or pose with an explicit margin; include raised limbs, handles, and protrusions in camera-space bounds. Account for aspect ratio when choosing orthographic scale or lens distance, and verify the actual image rather than assuming the numerical bounds guarantee framing.
9. Inspect clipping, silhouette, unwanted shadows and depth-of-field focus at output size. Recheck the camera after adding surrounding or reflection geometry: context must not unexpectedly obstruct the subject or flatten its hierarchy.
10. Save named camera/light settings and deliver the reviewed preview.

## Execution notes

Orthographic framing is useful for sprites and diagrams; perspective is a deliberate alternative. Avoid using exposure to conceal an incorrectly scaled light or material. Keep camera clipping planes appropriate to scene scale.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
