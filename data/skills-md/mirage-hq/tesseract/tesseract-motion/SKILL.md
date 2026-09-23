---
name: tesseract-motion
description: Create editable motion graphics locally in Tesseract, including full-frame animated scenes, typography, diagrams, lower thirds, and overlays on supplied footage. Use for focused motion-design work; use tesseract-video for assembling or revising a complete footage edit.
---

# Design motion with Tesseract

The CLI may send basic usage telemetry for some commands. You can provide optional attribution via `TESSERACT_SKILL=tesseract-motion` and the [other attribution variables](references/telemetry.md). Respect the CLI's telemetry opt-out setting; never enable telemetry on the user's behalf.

Create a moving composition with a clear visual idea. Establish what the motion communicates, its rhythm, the destination canvas, and whether this is a full scene or an overlay that must leave footage visible.

When designing an ad opening, read [ad hooks](references/ad-hooks.md): develop a clear visual idea tied to the actual product/message, align its key arrival to confirmed opening music cues when available, and preview it together with the next scene. Sound and transitions strengthen the idea; they are not a required effects stack.

1. Resolve this skill's root from the directory containing this `SKILL.md`. Read [CLI installation](references/installation.md) and check the required Tesseract version once per session. Use the resolved executable path throughout the task. Read [local operation](references/local-operation.md) and [native authoring](references/native-authoring.md).
2. Read [motion design](references/motion-design.md). Use the supplied brand/style references. For an overlay, inspect the actual footage at the intended placement and timing; design around the subject, text, and action.
3. Choose a useful mechanism—typography, paths, masks, precomps, a diagram, or a media treatment. Use native layers and a coordinated AnimationGraph. Existing footage and graphic assets are welcome; a single prerendered image of the design defeats editable motion.
4. Retrieve the specific definitions needed from `tsrct project schema` or `tsrct project schema --document`. [FX authoring](references/fx-authoring.md) and [motion](references/motion.md) show working wire shapes and local rendering, not mandatory designs. For subject occlusion use actual person mattes when supported, not an approximate hand-drawn silhouette.
5. When supplied or previously generated music sets the rhythm, read [waveform editing](references/waveform-editing.md): open a music waveform, listen to confirm accents and phrase changes, and map animation arrivals/reveals to the selected music events before authoring timing. Preserve the chosen track; do not mistake every peak for a beat or sync every movement mechanically. Read [sound design](references/sound-design.md) when the graphic is part of an audible video. Add a local accent or transition sound when it strengthens the movement; leave it quiet when speech or the existing mix already carries the moment. Keep sound in separate Audio layers, and use [audio and timing](references/audio-and-timing.md) for importing files, placement, and envelopes. A silent-overlay request stays silent.
6. Use [filmstrip review](references/filmstrip-review.md) to inspect and correct the saved animation during construction. Finish with [review and delivery](references/review-and-delivery.md), including playback in context.

Output an editable composition in a portable `.tsrct` document and a rendered preview. Composite overlays over the supplied footage as native layers. For a transparent overlay, use `export --format prores --fx-solo compositionId:layerId --output overlay.mov` and verify the alpha channel. Solo export covers the target’s active window without audio; full-project MOV export preserves the project mix.

Prefer supported effects and native text/shape animation. For an unusual visual treatment use custom WGSL only after reading the [custom shader contract](references/custom-shader.md). Never invent API fields, keyframe formats, or a capability such as arbitrary 3D mesh import that this runtime does not provide.
