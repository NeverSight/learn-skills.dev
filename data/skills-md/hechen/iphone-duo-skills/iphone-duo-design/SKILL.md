---
name: iphone-duo-design
description: Review or design iPhone Duo app flows for coherent hierarchy, reachable controls, adaptive presentations, and continuity between the compact outer display and the larger inner display. Use when planning what each display shows, how a screen changes as the device opens, folds, or rotates, where controls go on the vertical axis or near the fold, or how a game or immersive screen fills every pose, before or alongside implementation.
license: MIT
---

# iPhone Duo design

Read [design evidence](references/design.md). Work from the actual user journey, current screens, and constraints. Prefer an annotated change to the existing experience over inventing an unrelated visual direction.

## Define continuity

Identify the primary task and what must survive a configuration change: selected item, draft, scroll location, playback, or an in-progress operation. Record which controls are needed to finish or escape the task. Keep these semantic relationships stable even when their visual positions change.

Sketch the compact and expanded compositions with realistic long content, empty states, and error states. Keep the same functionality and information hierarchy on both displays; the inner display can add one more level where the content supports it, such as a list beside its detail. Avoid adding panels solely to occupy space. Treat width, height, keyboard obstruction, and text size as independent pressures.

## Review transitions and presentations

Annotate where controls, sheets, selection, and focus go as available space changes. If a secondary panel disappears, make its content reachable through an existing navigation or presentation path. Define the return path before approving the composition.

Use system components as the baseline. Justify custom relocation by a concrete obstruction or usability problem, and prefer small moves over rearranging the screen as the device folds. Keep controls with the content they operate on, keep their relative positions similar across poses, and preserve their accessibility names when using compact representations.

Review large text, VoiceOver order, right-to-left content, Reduce Motion, and Reduce Transparency using the same core task. Do not assume a screenshot establishes accessibility or reachability. Validate with interaction when a running app is available; otherwise mark the proposal as untested.

## Output

Deliver annotated compact/expanded states, the key transition, and a prioritized list of changes tied to user consequences. Explain the expected hierarchy and the evidence needed to accept each change. When implementing, preserve existing visual conventions and review actual screenshots after layout changes.
