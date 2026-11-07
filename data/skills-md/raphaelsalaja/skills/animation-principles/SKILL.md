---
name: animation-principles
description: Reviews press scale, squash and stretch, stagger and staging so one motion holds the frame.
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: https://www.userinterface.wiki
---

# Animation principles

This skill reviews how motion is staged once the timing function is chosen. It checks press feedback, deformation, stagger and focus.

Every check is a pair. The broken line sits beside the line that replaces it.

Press scale, squash and stagger amounts below are exact. A project that omits press feedback on a control is a finding. A project that uses one consistent scale near `0.98` is not. Curves, the `300ms` cap and context-menu entrances belong to `timing-functions`. Exit mounting belongs to `exit-animations`.

## When to use

Use this when adding or reviewing animation on controls, lists, overlays or entrances. Use `timing-functions` first when the question is spring versus easing. Use `exit-animations` when a component fails to leave the tree.

## 1. Read the motion in scope

Read the files the user named. If none are named, ask which surfaces to review. Note each animated element and whether it is a press, a list entrance, an overlay or background decoration.

## 2. Check staging

Similar controls share one duration. A primary button at `200ms` and a secondary button at `150ms` is `timing-consistent`.

An interactive control needs an active scale. The published press scale is `0.98`. Squash and stretch stay inside `0.95` to `1.05`. `whileTap` of `0.8` is `physics-subtle-deformation`.

Stagger stays under `50ms` per item. `staggerChildren: 0.03` passes. `0.15` is `physics-no-excessive-stagger`.

Only one element animates prominently at a time. That is `staging-one-focal-point`. A modal or dialog dims what is behind it, as in `background: var(--black-a6)`, which is `staging-dim-background`. A tooltip or overlay that can paint underneath siblings is `staging-z-index-hierarchy`.

Springs used for overshoot, ease curves and the `300ms` cap are `timing-functions`. Cite that skill beside a duration finding. Do not restate its curve table here.

## 3. Report and stop

Write the findings, then the summary table. Do not restyle the motion while reporting unless the user asked for a fix.
## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `timing-consistent` | `.button-primary { transition: 200ms }` and `.button-secondary { transition: 150ms }` | Both controls at `transition: 200ms` |
| `physics-active-state` | `.button:hover { background: var(--gray-3) }` and no `:active` | `.button:active { transform: scale(0.98) }` |
| `physics-subtle-deformation` | `whileTap={{ scale: 0.8 }}` | `whileTap={{ scale: 0.98 }}` |
| `physics-no-excessive-stagger` | `staggerChildren: 0.15` | `staggerChildren: 0.03` |
| `staging-one-focal-point` | Two siblings both `animate={{ scale: 1.1 }}` | One element carries the entrance |
| `staging-dim-background` | `.overlay { background: transparent }` | `.overlay { background: var(--black-a6) }` |
| `staging-z-index-hierarchy` | `.tooltip {}` with no stacking | `.tooltip { z-index: 50 }` |

## Reporting

**Severity.** Use the ladder in this skill. Do not raise a preference to `HIGH`.

**Verification.** Read the declared values in the files in scope. A browser is optional. Mark any check you could not run as `Not verified`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a summary:

| Rule | Count | Severity |
| --- | --- | --- |

`Block` when any `HIGH` remains. `Approve` otherwise, and leave lesser rows in the table. Never `Approve` a file you did not read. With nothing to report, say "No actionable findings" and list what was not verified.
