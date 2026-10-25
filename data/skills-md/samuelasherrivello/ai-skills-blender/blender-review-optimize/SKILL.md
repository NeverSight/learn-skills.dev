---
name: blender-review-optimize
description: Audit and optimize Blender asset cost while measuring appearance and downstream behavior.
---

# blender-review-optimize

## Inputs and scope

Accept target collection, budget and permitted changes; default to audit before edits. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Parallel visual target and feedback

At the start of a new top-level 3D task, launch one subagent using `blender-create-visual-target-2d` with the exact prompt, constraints, supplied references/current-scene preview, unchanged features, task ID and an exclusive target directory. Continue Blender inspection and construction immediately while it prepares the prompt-specific target. Nested skills reuse the same pending/completed worker; do not launch one per skill. The target worker must not mutate Blender or recursively delegate.

When it returns, inspect the target and compare a genuine current preview, prioritize visible gaps, apply in-scope corrections and inspect again against the same target version. Use the requested iteration budget, otherwise up to two focused correction passes; report remaining gaps. Preserve render/export/audit-only scope and existing-asset identity. Follow the target skill's parallel-feedback reference when available. If delegation or image generation is unavailable, use parent-side preparation or a supplied target, disclose any prompt-only fallback, and never claim an unperformed comparison. Pure setup checks and explicit user opt-outs bypass this default.

## Workflow

1. Verify readiness and define scoped assets and optimization goals.
2. Capture baseline views and measured counts using the same camera/settings.
3. Audit evaluated geometry, materials, image sizes, modifiers and animation.
4. Rank findings by measured impact and visible risk. Separate technical validity, requested style fidelity, and runtime: a fast valid render can still miss the brief. Inspect the full image and a few final-resolution details, then fix the largest visible mismatch before adding samples or geometry indiscriminately.
5. Checkpoint the source before destructive optimization.
6. Apply focused fixes to the owned scope; preserve silhouette and deformation where required.
7. Remeasure using the baseline method.
8. Compare before/after renders at intended display size. Record which visible mismatch improved, stayed unchanged, or regressed; higher object counts are not evidence of better results. If small detail produces little improvement, revisit primary/secondary form and composition rather than continuing the same detail pass.
9. Check affected exports, modifiers and animation for regressions.
10. Deliver source, before/after measurements, visual evidence and unresolved findings. When feedback changes reusable guidance, state the supporting observation and its scope; test a different subject or style when practical. One improved example does not demonstrate general success, and architectural realism lessons must not erase intentional stylization.

## Execution notes


Use [scripts/audit_scene.py](scripts/audit_scene.py) inside Blender for selected-object counts; pass objects explicitly to audit(). Evaluated geometry can be much larger than base geometry. Texture memory estimates are estimates, not GPU profiler measurements.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.

## Editor screenshot readiness

Before capturing genuine editor evidence, verify Blender has an open, visible, non-minimized editor window; maximization is unnecessary. Minimized full-window and area captures have returned black on the tested workstation. If minimized, report the solution: restore Blender from the taskbar. Capture permission is already included in requested Blender work; this is a technical readiness issue. Inspect captured pixels and never label a failed capture, prior screenshot, or clean render as fresh editor evidence. Do not change the user's window state without authorization.

Before **every** Blender editor/window/area screenshot call, freshly check that the relevant Blender process has a visible, non-minimized editor window; do not reuse an earlier setup result. If Blender is closed, prompt the user to open it. If minimized or hidden, prompt the user to restore/show it (maximization is unnecessary). If inspection is unavailable, report the unknown state and ask the user to make the editor visible. Pause screenshot attempts until the issue is resolved, then repeat the window-state check before capturing. Do not automatically restore/focus the window. This prerequisite applies to editor screenshots, not saved render output. A passing check still requires inspection of the captured pixels; if the image is black or stale, report the failure and prompt the user to restore/show the editor before a fresh check and retry.
