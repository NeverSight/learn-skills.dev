---
name: manim-idea-to-export
description: Convert plain-language concepts into ManimCE scene plans, runnable code, preview renders, and final export commands. Use when a user provides narration, bullet points, or storyboard notes and wants end-to-end ManimCE output. Do not use for ManimGL/manimlib codebases.
---

# Manim Idea to Export

## Overview

Use this skill to turn user text ideas into production-ready ManimCE output through a strict pipeline:

1. parse idea text,
2. map to scene plan,
3. generate Manim code,
4. render and fix,
5. export final media.

Prefer this skill for requests like “animate this explanation”, “turn this paragraph into a video”, or “convert these bullet points into Manim and export”.

## Idea-to-Export Workflow

1. Intake and normalize intent.
- Extract objective, audience, visual style, duration target, and output format.
- Resolve ambiguity by making minimal explicit assumptions in code comments or summary.
- If user requests “beautiful”, “clean”, “cinematic”, or “3B1B-like”, apply the visual clarity and pacing playbook.
- Unless user asks for minimal motion, apply the animation philosophy directives by default.

2. Preflight mini-blueprint + preference handshake (required on first pass).
- Return a short mini blueprint (about 4-7 bullets, high-level only).
- Ask focused preference questions before detailed planning:
- visual theme (dark/light/custom),
- motion intensity (calm/medium/high),
- camera behavior (no zoom / selective zoom-pan / cinematic),
- 2D vs 3D usage,
- pacing preference (slow/readable vs faster/condensed),
- style target (3B1B-like vs clean-minimal vs other),
- desired duration range.
- If user does not answer, choose conservative defaults and state them.
- Do not start full code generation until the user confirms or explicitly says “proceed”.

3. Build detailed scene blueprint from confirmed preferences.
- Convert narrative into ordered beats.
- For each beat define: on-screen objects, transition, duration, and emphasis.
- Split into one or more `Scene` classes if conceptually distinct.
- For process diagrams, define directed dependencies and a topological animation order before writing code.
- Include a reflow plan per beat: what moves/shrinks/fades to create space for incoming objects.
- Include camera intent per beat (hold, pan, zoom in, zoom out) when layout is dense.

4. Generate runnable ManimCE code.
- Use `from manim import *`.
- Keep `construct()` orchestration-focused.
- Use helper builders for repeated objects/layouts.
- Add layout guard helpers for text-fit, label-fit, and collision-safe spacing.
- Prefer transformations over object spawning when provenance can be shown.
- Use `ValueTracker`/`always_redraw` for interdependent visuals instead of disconnected static states.

5. Render in a fast feedback loop.
- Layout check: `-ql -s`
- Timing check: `-ql -n a,b`
- Preview export (required): `-ql -p` (480p preview pass)
- Final export: `-qh` (or higher as needed) only after user confirmation on preview
- Add an overlap pass: verify no text overflows containers and no labels collide with arrows/axes.
- Add a movement pass: verify the scene is not visually static and includes purposeful transitions between beats.
- Add a frame-fit pass: verify all active content stays within visible frame margins.

6. Export and report deliverables.
- Return exact render command used.
- Return output path(s) and file format.
- Note assumptions and next tweak knobs (timing/style/text density).
- Always show preview artifact first and ask for confirmation before high-quality export.

## Implementation Contract

For every idea-to-code request, produce:

- Mini blueprint + preference questions (first pass) or a note that preferences were previously confirmed.
- `Scene` class code implementing the described idea.
- A suggested file location (for example `scenes/idea_scene.py`).
- A concrete render command.
- The expected output location/filename.
- A short “edit knobs” list (what to change for speed/style/detail).
- A short pacing rationale (why key beats are fast/slow).
- A short layout-fit note (how text/labels were constrained to avoid overflow/clutter).
- A short logic-order note for process flows (for example: `L1->L2` then `L2->L3`).
- A short motion rationale (where transformations, tracker-driven motion, and camera moves were used).

## Code Quality Rules

- Use semantic names (`claim_text`, `curve_group`, `highlight_box`).
- Favor composable primitives (`VGroup`, `Axes`, `MathTex`, `Text`, `Transform`).
- Keep updaters minimal and scoped.
- Avoid hidden global mutation.
- Ensure every visual beat is intentional and readable.
- Make pacing explicit for key beats (`run_time`, `rate_func`, and pauses), not implicit defaults.
- Default to a clean dark scene (`config.background_color = "#000000"` unless the user requests otherwise).
- Never leave raw overflow: scale/wrap/reflow text to container width before rendering.
- Keep scene content centered and frame-safe (no critical content outside visible bounds).
- Keep arrow labels outside arrowheads and with consistent buffer, then resolve collisions.
- Avoid low-motion output: each explanatory beat should include meaningful motion unless intentionally a pause beat.
- Before introducing new objects, create spatial room by moving/reframing existing content.
- Use semantic color mapping consistently across equations and matching visual objects.
- Keep text on screen long enough to read using a words-per-minute pacing rule.
- Treat confirmed user preferences as locked constraints unless user asks to change them.

## Environment Assumptions

- Target runtime is Manim Community Edition (`manim`), not `manimgl`.
- Assume a project-local virtual environment is active before render commands are run.
- For `Tex/MathTex`, assume `latex` and `dvisvgm` are required.
- Assume `ffmpeg` is required for video export.

## Execution Boundaries

- Keep command guidance scoped to the current workspace/project path.
- Do not suggest destructive commands (for example force-delete, history rewrite, or reset-hard flows).
- Do not suggest global dependency mutation unless the user explicitly asks for global installation.
- If required tooling is missing, stop and return concrete remediation commands before proceeding.

## Safety and Validation

- Keep commands non-destructive and scoped to the current project.
- Prefer deterministic commands and explicit paths in export guidance.
- Validate syntax/runtime with at least one render pass before final handoff.
- When TeX is used, verify `latex` and `dvisvgm` availability or report a concrete remediation command.

## Export Rules

- Default output: `mp4` unless user asks otherwise.
- Use transparent renders only when explicitly required (`-t`).
- If user asks for preview artifacts, include still frame via `-s`.
- For multiple sections, use `next_section()` and `--save_sections` where useful.
- Always render a preview pass first with `-ql` (480p-equivalent workflow) and share it.
- Do not run `-qm/-qh` final export until the user confirms the preview.

## Failure Handling

1. If `Tex/MathTex` fails, fix LaTeX toolchain first (`latex`, `dvisvgm`).
2. If rendering is slow, reduce quality and isolate animation ranges.
3. If visuals are cluttered, reduce simultaneous motion and split into more beats.
4. If text or labels collide/overflow, rerun with stricter fit constraints and spacing buffers.
5. If process logic appears out of order, enforce staged dependency animation (no downstream motion before upstream state exists).
6. If output feels static, add tracker-driven motion, transformation continuity, and camera emphasis beats.
7. If content is off-screen or not centered, reflow groups and camera framing before any final export.
8. If style or preference fit is unclear, pause after mini blueprint and ask targeted preference questions.

## References

Load only what is needed.

- `references/idea-to-scene-blueprint.md`
- `references/code-generation-patterns.md`
- `references/render-and-export-playbook.md`
- `references/quality-checklist.md`
- `references/visual-clarity-and-aesthetics.md`
- `references/logic-and-layout-guardrails.md`
- `references/animation-philosophy-directives.md`
- `references/preflight-brief-and-preferences.md`
- `references/troubleshooting.md`
