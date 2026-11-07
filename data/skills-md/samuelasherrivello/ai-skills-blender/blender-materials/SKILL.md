---
name: blender-materials
description: Create and tune Blender materials and shader nodes for requested surfaces or render styles.
---

# blender-materials

## Inputs and scope

Accept target objects, surface/style, physical scale and render engine; use neutral comparison lighting. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and identify the requested surface and target engine.
2. Inspect existing materials and make unique copies when shared users must not change.
3. Set a neutral comparison view with stable exposure.
4. Establish base color, roughness, metallic/transmission response before adding detail.
5. Load available textures with correct color spaces: color inputs versus Non-Color data maps.
6. Set texture scale and restrained bump/normal strength in scene units. Inspect every visible face for stretched or rotated mapping. Separate broad color variation, material grain, and joints; avoid making all three the same noise scale or adding large cloudy patches to otherwise uniform surfaces.
7. Name and organize nodes; keep important controls editable.
8. Compare the material under neutral and intended production lighting. For glass, inspect the whole optical setup: real opening, surface thickness, plausible interior/backing, and something meaningful to reflect. Do not compensate for an opaque backing or empty environment by tinting glass or making it metallic.
9. Check missing paths, packed assets when needed, material slots, shader cost and export compatibility.
10. Save the material/source and inspected comparison renders with limitations.

## Execution notes

Do not label a material physically accurate solely from a pleasing render. Avoid metallic response on ordinary dielectrics. Shader-to-RGB/outline techniques can be engine-specific; verify the selected engine and downstream export.

For worn realistic surfaces, tie variation to a cause: rain paths below ledges, handling at grips, contact near a base, or grain following manufacture. Keep the underlying material readable. Uniform dirt and random noise across every surface can make a scene less plausible; clean, stylized, and diagrammatic requests may need none.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
