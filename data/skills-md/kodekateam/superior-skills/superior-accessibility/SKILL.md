---
name: superior-accessibility
description: Review or implement interface accessibility for semantics, keyboard operation, focus, contrast, status communication, zoom, and assistive technology. Use when accessibility is explicitly requested, required by the product contract, or a changed interaction creates substantial accessibility risk. Do not activate for every visual edit or use it as a generic design audit.
---

# Superior Accessibility

Preserve the user's ability to perceive, understand, navigate, and operate the changed interface. Prefer native semantics and observable behavior over ARIA-heavy patches.

Establish the affected journey, interaction model, supported platform, and available verification tools before choosing a fix. Preserve product behavior unless an inaccessible interaction contract must change.

## Structure and names

- Use the native element whose behavior matches the control.
- Give controls an accessible name that matches or includes the visible label.
- Keep heading order, landmarks, lists, tables, and form relationships meaningful.
- Use alternative text for informative images; keep decorative imagery out of the accessibility tree.
- Add ARIA only when native HTML cannot express the necessary relationship or state, and keep it synchronized.

## Keyboard and focus

- Make every essential action reachable and operable without a pointer.
- Preserve a logical focus order that matches the reading and interaction sequence.
- Show a visible focus indicator against every surface it crosses.
- Move focus only for a real context change such as opening a modal; restore it when that context closes.
- Ensure overlays trap focus when appropriate, close predictably, and do not leave background content interactive.

## Contrast and non-color cues

Use `scripts/contrast_check.py` for known solid sRGB colors when Python is available:

```text
python scripts/contrast_check.py "#1f2937" "#ffffff"
```

Resolve the script relative to this `SKILL.md`. For gradients, images, opacity, filters, or compositing, inspect the actual rendered result; two source hex values may not represent the final contrast.

- Target at least 4.5:1 for normal text and 3:1 for large text under WCAG 2.x.
- Check meaningful component boundaries and focus indicators against adjacent colors.
- Pair color with text, iconography, shape, or another cue for status and validation.
- Do not assume muted text is exempt because it is secondary.

## Dynamic states

- Expose validation errors near their fields and summarize them when the form needs it.
- Announce important asynchronous results without repeatedly interrupting the user.
- Keep loading, expanded, selected, pressed, checked, current, invalid, and disabled states programmatically accurate.
- Do not disable an action without explaining the prerequisite when it is not otherwise obvious.

Read [references/interaction-and-assistive-technology.md](references/interaction-and-assistive-technology.md) when the task includes dialogs, composite widgets, custom controls, drag and drop, live updates, route changes, virtualized content, or screen-reader-specific behavior.

## Zoom, motion, and touch

- Reflow at supported zoom without losing information or actions.
- Keep focused inputs visible above virtual keyboards and fixed UI.
- Provide comfortable touch targets and spacing.
- Respect reduced-motion preferences and avoid motion that is required to understand the result.

## Verify behavior

Use keyboard-only navigation through the changed journey. Inspect accessible names and states with available platform tools, test relevant zoom and narrow layouts, and check contrast at the rendered colors. Automated checks are useful coverage, not proof of usability; report both automated and manual evidence.

Do not claim screen-reader compatibility without naming the browser, assistive technology, platform, and journey actually exercised. When that environment is unavailable, verify semantics and accessibility-tree output where possible, then report the untested combination explicitly.

Use `superior-code-review` when accessibility is only one risk area in a broader change-set review, `superior-responsive` for space-driven re-composition, and `superior-ui` for visual or interaction implementation outside the accessibility contract.
