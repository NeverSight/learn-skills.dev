---
name: erduo-broll-loop-engineering
description: Turn original SRT and design into editable B-roll through an independent Director, focused chapter creators, and visual review. Use for SRT-to-video production or revisions; preserve existing legacy projects and explicit Remotion choices.
---

# Erduo B-roll Loop Engineering

Make the spoken meaning visible, with considered composition and purposeful
motion. **Picture quality comes first.** Preserve fresh creative contexts and
independent visual review; save work through focused handoffs and deterministic
scripts, never by removing needed creative work or returning an inferior film.

## Route once

- New projects and existing `broll-plan.json` use the creative relay below.
- Existing Recipe/runtime-plan v1–v4, explicit Remotion/hybrid, or an explicit
  five-shot version comparison use [legacy production](references/legacy-production.md).
  Preserve original inputs and approvals; do not silently migrate projects.
- This relay uses pinned HyperFrames. Its role references replace the legacy
  stage Skills for this route; do not load both sets or the whole Skill catalog.

## Parent: prepare and dispatch

Keep the complete original SRT and original design in the project. If design is
missing, make a short brief from the user's request; preserve the original SRT.
Prepare known local assets/fonts and `assets/index.md` with paths and sources.
Add a material researcher only for real selection work; authorized search or
generation remains available when needed for the picture.

Read [production commands](references/lean-production.md). Resolve the installed
Skill root and runnable commands once. Use `scripts/prepare-creative-task.mjs`
to prepare each role's short `TASK.md`, then start it in a **new context** using
the host's delegation capability. Give the task file and any explicit user
constraints, not the parent conversation, previous agent logs, or all Skills.
Respect the user's model selection; do not silently substitute a cheaper model.
The helper prepares inputs; the host must actually start fresh contexts and may
still inject global instructions. Do not claim it enforces a context sandbox.

## Creative relay

1. **Independent Director** reads originals and chooses the visual world,
   meaningful shot boundaries, material, action development and seams. It writes
   one `broll-plan.json`, a short `direction.md`, and `direction/<id>.md` shot
   cards. Its role is [creative direction](references/creative-director.md).
2. **Fresh creators** each own a continuous passage and its editable HTML.
   Group shots by narrative continuity and complexity, not a fixed count.
   Give originals, shared direction/assets, owned shot cards and adjacent seam
   cards. Separate file ownership; run independent chapters in parallel where
   their visual contract is clear. Use [chapter creation](references/creative-creator.md).
3. **Parent runs the scripts** for plan checks, renders, decode, sheets and
   assembly. Return a concise failed-shot error to its owner. Environment
   failures belong to the parent; do not make every creator reinstall or search
   for the same executable. Creators can request a render and view their work.
4. **Independent visual reviewer** sees the originals, direction, actual media
   and relevant seams, without creator explanations or cost figures. Use
   [visual review](references/creative-reviewer.md). Technical success cannot
   approve aesthetics. Send specific time/shot feedback to the original creator,
   render only changed shots, and recheck affected shots and seams.

Keep these creative contexts separate even for a short film; a short film can
have one creator. If independent delegation is unavailable, disclose that the
relay cannot be completed as specified; do not label a same-context self-review
independent. Revisions of existing work retain its direction and shot ownership;
reopen directing only when the requested change affects meaning or the visual world.

## Quality and delivery

Use [visual direction](references/lean-visual-direction.md) and a few matching
[motion patterns](references/motion-patterns.md) to make the action concrete.
For an uncertain style or complex shared transition, make a representative
passage and view it before multiplying that treatment. Reuse accepted visual
source or frames as a reference, while varying composition with meaning. There
is no mandatory number of samples, material quota, or decorative element count.

Respect requested user review stops; existing authorization also covers normal
renders and repairs. Do not stop for a new approval form merely because a role
changed. Repair visible quality problems before delivery. If repeated local
repairs are not improving the picture, change the visual solution instead of
repeating the same layout or adding more decoration.

Deliver ordered shot files, editable source/assets, complete preview, actual
output facts and remaining limitations. A partial preview must identify missing
shots and cannot stand for the full film. State what was actually viewed; frame
sampling is not continuous playback. Report tokens only from actual host usage,
separating cached input and output. Do not turn file sizes into savings claims.
Follow [safe execution](references/safe-execution.md) for external commands.
