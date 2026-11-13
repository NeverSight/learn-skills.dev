---
name: ux-tooltips
description: Design or critique tooltips and contextual hints — decide when a tooltip clarifies vs. when it's a crutch for unclear design, and apply placement, styling, and brevity rules. Trigger when the user asks to design or review tooltips, hover hints, info icons, contextual help bubbles, or asks whether something needs a tooltip.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Tooltips Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **tooltip-as-crutch** (an unclear interface "fixed" by sprinkling hover hints everywhere), **redundancy** ("Submit" button + "Click to submit" tooltip), and **vital info in hover space** (content users *must* see, hidden behind an interaction many will never perform — and that touch devices can't perform reliably). A tooltip is a *supplement for genuinely ambiguous elements* — never a load-bearing part of the flow. This skill gates:

1. **Gate each tooltip's existence** — is the element actually ambiguous, or is the design unclear?
2. **Apply the always-true core** — placement, brevity, styling, cursor signaling.
3. **Surface the escalation decisions** — when a tooltip is the wrong tool entirely.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Gate each tooltip's existence

Three questions per tooltip:

- **Is the element genuinely ambiguous?** A camera icon that could mean "take photo" or "open gallery" → tooltip earns its place. A button labeled "Submit" → no tooltip; it would only repeat the label.
- **Is the information vital to the task?** Tooltips are user-triggered — many users never hover, and touch devices have no hover. Anything required to complete the flow goes *in the interface* (label, helper text, inline message), never in a tooltip.
- **Is this papering over a design problem?** If a screen needs many tooltips, the labels, icons, or layout are failing. Fix the element; don't annotate it. (Better universal icon, visible label, or icon + label — see `ux-buttons` and `ux-menus`.)

---

## The always-apply core (for tooltips that survive the gate)

- **Concise, essentials-only content** — a bite-sized clarification ("Capture photo"), no redundancy, nothing users must strain to read.
- **Placement never blocks** — the tooltip and its trigger element both stay fully visible; never cover the input or button it describes, never get cut off at screen edges.
- **Pointer cursor on hoverable triggers** — signals that more information is available and ties the cursor to the pop-up.
- **Left-aligned text** (LTR), modest styling, no decorative frames, **≥4.5:1 contrast** between text and tooltip background.
- **Consistent treatment product-wide** — one tooltip style, one trigger behavior.

---

## The escalation decisions (when a tooltip is the wrong tool)

| Situation | Don't reach for | Use instead |
|---|---|---|
| Information needed to complete a form field | Tooltip on an info icon | Helper text below the input (→ `ux-inputs-and-forms`) |
| Visual question (where's the CVV?) | Text-only tooltip on mobile | Inline icon/graphic, tooltip as desktop supplement |
| First-run feature education | Permanent tooltips everywhere | Onboarding walkthrough patterns (→ `ux-onboarding`) |
| Anything on touch-first products | Hover-dependent tooltips | Visible labels, helper text, or tap-triggered popovers (→ `ux-modals-and-dialogs` for popovers) |
| Rich content (images, multiple actions) | An overstuffed tooltip | A popover |
| Truncated text needing full display | Hoping users guess | Tooltip is right here — truncation + tooltip is a legitimate pairing (→ tables, menus, breadcrumbs) |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — recognition over recall (is the interface self-explanatory without the tooltips?), consistency of treatment.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — keyboard/focus access to tooltip content, touch alternatives, contrast, no hover-only vital information.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — styling restraint, placement cleanliness.
- **`ux-microcopy-audit`** *(Tier A)* — tooltip text brevity and clarity.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: hover-dependence is a defect there by default.

If the audits surface a conflict, resolve back toward the primary task: a user who needs a tooltip is already slightly lost — the goal is an interface where they rarely need one.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Click to submit" on a Submit button | Tooltips only where meaning is genuinely ambiguous |
| Required instructions hidden in hover | Vital info in the interface; tooltips are optional extras |
| Ten tooltips patching an unclear screen | Fix labels/icons; tooltips as rare supplements |
| Tooltip covering the field it explains | Placement that keeps trigger + tooltip both visible |
| Tooltip cut off at the viewport edge | Edge-aware positioning |
| Decorative frames, low-contrast text | Modest styling, ≥4.5:1 contrast, left-aligned |
| A paragraph in a tooltip | One bite-sized clarification |
| Hover-only help on touch products | Visible labels or tap-triggered popovers |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [Tooltips & When to Use Them](https://uxcel.com/lessons/contextual-568)
