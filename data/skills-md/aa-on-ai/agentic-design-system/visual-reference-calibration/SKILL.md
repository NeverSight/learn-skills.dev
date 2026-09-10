---
name: visual-reference-calibration
description: Use before implementing UI/design from an artifact supplied as a desired visual reference, such as a screenshot, CodePen, Dribbble shot, website, or “make it feel like this” request. Screenshots used only to point out a defect stay in the normal review path. Prevents cargo-culting mechanics, fake UI chrome, and code-first misses by forcing reference breakdown, user-question calibration, visual target approval, and side-by-side review before implementation.
---

# Visual Reference Calibration

Use this when the user points to a visual reference and wants a UI to borrow its feel, quality, interaction, surface treatment, motion, or style.

Do not use this merely because a screenshot is attached. If the screenshot only marks a bug, awkward edge, or region to review, treat it as evidence for the existing UI and continue with design-review.

This skill exists because we badly missed the Jhey CodePen portfolio-card task by translating a visual reference into implementation mechanics instead of design judgment.

## Core rule

Do not code first.

First identify what the reference is actually contributing, confirm that with the user when ambiguous, then create or inspect a visual target before implementation.

## Failure pattern to avoid

- Treating a reference as vague “inspiration” when the user expects close spirit/fidelity.
- Copying incidental structure from the reference, e.g. fake icons, overflow menus, app chrome.
- Implementing the mechanism while missing the visual quality.
- Making isolated component hover polish when the reference is a system-level effect.
- Shipping preview attempts before comparing side-by-side with the reference.
- Saying “I’m aligned” before being able to describe the reference in the user’s terms.

## Required workflow

### 1. Build a reference contract

Before implementation, write a short contract. Use `templates/reference-intake-contract.md` when available:

```markdown
Reference contract:
- Source/reference:
- What we are borrowing:
- What we are not borrowing:
- Fidelity target: close mimic / same spirit / loose cue
- Existing product constraints:
- Hard no’s:
- Review gate before code:
```

If any line is uncertain, ask the user before coding.

Hard rule: if you cannot state what to borrow, what not to borrow, and the fidelity target, you cannot build.

### 2. Ask the right calibration questions

Ask the smallest set that resolves ambiguity. Usually 1-3 questions, not a survey.

Use these in priority order:

1. “What is the part you want me to preserve: layout, color/surface, motion/behavior, density, typography, or overall vibe?”
2. “Should this closely mimic the reference, or just borrow the spirit while staying native to the current product?”
3. “What should I explicitly not copy from the reference?”
4. “Should the existing component/content hierarchy stay intact, or is the reference allowed to change the structure?”
5. “Do you want a static visual target first, or a throwaway interactive prototype first?”

If the user is frustrated or says we are missing the point, stop and ask:

> “Say the part you like in one sentence. I’ll restate it before touching code.”

### 3. Separate visual layers

Break the reference into layers before deciding what to copy:

- Composition/layout
- Surface/color/material
- Border/shadow/glow treatment
- Typography/density
- Motion/interaction model
- Content metaphor/chrome
- System behavior, e.g. shared hover field vs per-card hover

Only copy the layers the user wants. Do not copy incidental UI chrome.

### 4. Make a visual target before production-quality implementation

For nuanced visual-reference work, produce one of:

- a static mock/screenshot target,
- a tiny isolated prototype,
- or a preview branch with screenshot evidence,

then compare side-by-side with the reference before shipping or merging.

Required self-check before showing the user:

- Does it look good without explaining the implementation?
- Does the reference comparison reveal the same visual language?
- Did we copy any incidental artifacts that do not belong in the user’s product?
- Is this tasteful in the product context, not merely technically similar?

### 5. Implementation guardrails

- Use a worktree/preview branch for code.
- No production deploy until the user approves the visual direction.
- Preserve existing hierarchy unless the user approved structural change.
- Add reduced motion and keyboard/focus equivalents for interaction work.
- If a reference effect is system-level, implement system-level state; do not fake it with local hover polish.

### 6. Stop rule

After two rejected passes, stop coding.

Say plainly:

> “This is not converging. I need to reset to a visual target/spec before more implementation.”

Then produce a reference contract and ask the calibration questions again.

## Jhey CodePen lesson

For `https://codepen.io/jh3y/pen/WbwZaNa`, the important lesson was not “add cards with icons.” The reference’s value was a shared proximity field, thick chromatic borders, saturated blurred material, and glow that affects neighboring cards. Copying fake app chrome, initials, or overflow menus was wrong.

Generalize the lesson: identify the core visual system, not the incidental demo content.
