---
name: ux-mobile-responsiveness-audit
description: Run a structured mobile-responsiveness audit on a design, screen, or component — viewport adaptation and reflow, orientation, touch-target size and spacing, thumb reachability, mobile input ergonomics, gesture safety, and mobile readability/content priority. Produces a severity-rated issue list with concrete fixes. Use when reviewing whether a UI works on phones/tablets, or as a validation step after generating mobile or responsive UI.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Mobile Responsiveness Audit Skill

## How this skill behaves (read first)

This is an **evaluative** skill — it reviews existing work against mobile/touch standards, it doesn't generate. Flagging is safe, so it **auto-runs** and is built to be **called as a validation step** by generative skills whenever the target is mobile or responsive (the component family, screens, and flows all hand off here for their mobile context).

It **owns the mobile/touch-adaptation concern** in this repo. To avoid duplicating its sibling audits, it defers:

- **WCAG ratios, screen-reader/assistive-tech, keyboard operability, alt text, captions** → the **accessibility audit**. This skill judges *physical touch ergonomics and layout adaptation*, not AT compatibility or contrast math.
- **Visual composition** — hierarchy, spacing aesthetics, emphasis → the **aesthetics audit**.
- **Usability, flow, and interaction logic** → the **heuristics audit**.
- **Content structure / navigation scheme** → the **information-architecture audit**; **type scale** → `ux-typography`.

> **Applicability gate:** this audit only applies when the target is meant to work on mobile or across breakpoints. If a design is explicitly desktop-only (e.g. a complex internal admin tool with no mobile support), say so and skip — don't manufacture mobile findings.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier B — offered (only when the platform is mobile)**. Explicit scope always wins.

---

## What this skill changes vs. default behavior

By default, "is it mobile-friendly?" gets a vague answer — "make the buttons bigger," "it should be responsive" — with no threshold, no severity, and no systematic sweep. This skill forces:

1. **Every finding names the violated principle** (reflow, touch-target size, thumb reach, etc.) and gives the **concrete threshold** (44pt / 48dp, ≥8dp spacing, ≥16px body).
2. **Severity rated** by whether it *blocks the task on the device* vs. adds friction vs. polish.
3. **A specific fix**, not "optimize for mobile."
4. **A systematic sweep** of all seven areas, so issues beyond "small tap targets" — orientation locks, wrong keyboard types, gesture dead-ends, non-reflowing layouts — actually get caught.

---

## The framework — what to check and what a violation looks like

Work through each. Flag with **principle**, **severity**, **fix**.

### 1. Viewport adaptation & reflow
The layout must adapt to the viewport — fluid grids, flexible images, content that reflows and reorganizes — rather than a fixed-width desktop layout squeezed onto a small screen. (Responsive = one fluid layout with breakpoints; adaptive = distinct layouts per breakpoint. Either is fine; *not adapting* is the failure.)

**Flag when:** horizontal scrolling or content cut off at the edges; a fixed-width (px) container that doesn't shrink; tiny zoomed-out desktop layout; elements overlapping or colliding between common breakpoints; images that don't resize proportionally; multi-column layouts kept on narrow screens instead of stacking vertically.

- ❌ A 1200px content frame on a 390px phone → user must pinch-zoom and scroll sideways to read.
- ✅ Content reflows to a single fluid column; images scale; nothing exceeds the viewport width.

### 2. Orientation resilience
Users hold devices both ways. Essential features must work in portrait *and* landscape; orientation changes should be purposeful, not breaking.

**Flag when:** the layout breaks, clips, or leaves dead space when rotated; core functionality is locked to one orientation without a real reason; a keyboard-heavy or video screen is forced to portrait when landscape would serve better; auto-rotation fires where it disrupts the task.

- ❌ Rotating to landscape hides the submit button below an un-scrollable fold.
- ✅ Portrait is the primary design; landscape reflows and keeps every essential action reachable.

### 3. Touch-target size & spacing
Fingers and thumbs are imprecise. Targets must be large enough and spaced enough to hit reliably — especially for adjacent contradictory actions (Save vs. Delete).

**Flag when:** interactive targets below the platform minimum — **iOS 44×44pt, Material 48×48dp** (WCAG floor 24px, but the platform minimums are the working target); less than **~8dp/16px spacing** between tappable elements; corner targets the same size as central ones (corners are harder — aim larger, ~12mm vs ~7mm center); destructive and confirming actions tiny and adjacent.

- ❌ A 28px icon button row with 2px gaps; "Delete" sits flush against "Save."
- ✅ ≥44pt/48dp targets, ≥8dp spacing, extra size for corner/contradictory actions.

### 4. Thumb reachability & one-handed use
People operate phones one-handed and prefer the screen center; hands obscure the interface and shift grip constantly.

**Flag when:** primary actions stranded in hard-to-reach top corners; destructive actions in the easy-tap thumb zone where they're hit by accident; key content jammed against the top edge; no bottom padding so content can't scroll to the comfortable center; right-edge-only button placement.

- ❌ The main CTA pinned top-right; a "Delete account" button in the bottom-center thumb sweet spot.
- ✅ Primary actions within thumb reach (lower-center / bottom sheet); destructive actions guarded or out of the accidental-tap zone; content scrollable to center.

### 5. Mobile input ergonomics
Typing on mobile is slow and error-prone (≈41% type two-thumbed). Match the input method to the data and minimize manual entry.

**Flag when:** a generic keyboard where a contextual one fits (no numeric keypad for phone/PIN, no "@"-optimized keyboard for email, no URL keyboard for web addresses); no autofill/autocomplete for name, address, email, payment; free-text fields where selection controls (picker, radio, toggle) would do; long forms not chunked across steps; no OTP autofill / card-scan where available.

- ❌ Phone-number field opens the full QWERTY keyboard; address typed from scratch with no autofill.
- ✅ Numeric keypad for numbers, email keyboard for email; autofill and selection controls reduce typing.

### 6. Gesture safety & discoverability
Gestures are invisible — they have discoverability, consistency, and accessibility limits. They should *supplement*, never solely carry, an action.

**Flag when:** a critical action is reachable *only* by a hidden gesture (edge-swipe menu, long-press) with no visible control; non-standard gestures redefining system conventions; complex multi-finger gestures required (exclude users with motor/dexterity limits); activation on touch-start rather than touch-end-within-target (accidental triggers).

- ❌ The only way to delete an item is an undiscoverable left-swipe; no button alternative.
- ✅ Swipe offered as a shortcut *alongside* a visible control; only simple, conventional gestures are required.

### 7. Mobile readability & content priority
Small screens used outdoors and in motion demand readable text and a ruthless first-screen priority — adapt content for mobile, don't just shrink the desktop.

**Flag when:** body text below **16px**; mobile line length outside ~**30–40 characters**; display typefaces at small sizes; the screen tries to show everything instead of leading with the primary task; secondary/tertiary functions crowding the first view instead of living below the fold or behind menus; the mobile version feels like a different product from desktop (inconsistent patterns, colors, controls).

- ❌ 12px body text, four competing CTAs above the fold, a desktop-only color scheme.
- ✅ ≥16px body, one clear primary action first, secondary actions deferred, consistent with the desktop product.

> **Tension note:** mobile pushes toward *fewer, larger* elements (targets, type, one primary action) while product owners push to surface more. Resolve toward the device reality — limited space and imprecise touch — and defer extra density to progressive disclosure rather than cramming. Where a fix would collide with the accessibility audit (e.g. target size, gesture alternatives), state it once and let accessibility own the AT/WCAG framing.

---

## Severity rating

| Severity | Meaning |
|---|---|
| **Critical** | Unusable on the target device — content cut off / horizontal scroll, targets too small to tap reliably, a critical action only via an undiscoverable gesture, or a core feature locked to an unavailable orientation. Fix before ship. |
| **Major** | Significant friction users shouldn't have to absorb — targets below the platform minimum but still tappable, primary action outside thumb reach, wrong keyboard type, body text below 16px, layout that reflows poorly at a common breakpoint. |
| **Minor** | Noticeable polish — slightly tight spacing, a non-ideal landscape layout, mild over-density, corner targets not enlarged. |

Rate by **impact on completing the task on the actual device**, not by how easy the fix is. A one-line keyboard-type change can still be Major if it blocks fast entry.

---

## Audit output format

```
## Mobile Responsiveness Audit — [Screen / Component]
Context: [device class / breakpoints · orientation · primary task, if known]

### Critical
- [Issue] — what's wrong → fix. (Principle: …)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest-impact fixes for the target device.
```

End with the prioritized top 3 — that's what a calling generator acts on.

---

## How to run a good audit

1. **Establish context** — device class (phone/tablet/responsive web), the breakpoints in scope, orientation expectations, and the screen's primary task. Touch ergonomics can only be judged against the device and the action that matters most.
2. **Confirm applicability** — if it's genuinely desktop-only, skip rather than inventing findings.
3. **Sweep all seven areas** — the value over a default review is completeness; don't stop at touch-target size.
4. **Use the thresholds** — 44pt/48dp targets, ≥8dp spacing, ≥16px body, ~30–40 char lines — so findings are checkable, not vibes.
5. **Defer** contrast/AT/keyboard to accessibility, composition to aesthetics, flow to heuristics — don't re-derive them here.
6. **Prioritize, don't enumerate** — rate by whether it blocks the task on the device.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Make it responsive" / "buttons too small" | Name the principle + threshold (44pt/48dp, ≥16px) + the fix |
| Treat every nit as equal | Rate by whether it blocks the task on the device; surface top 3 |
| Shrink the desktop layout onto the phone | Reflow to a fluid single column; nothing exceeds viewport width |
| Lock core features to one orientation | Essential actions work in portrait *and* landscape |
| 28px targets with 2px gaps | ≥44pt/48dp targets, ≥8dp spacing, corners enlarged |
| Primary CTA top-corner; delete in the thumb zone | Primary within thumb reach; destructive guarded / out of easy reach |
| Full QWERTY for a phone-number field | Contextual keyboards; autofill; selection over typing |
| Hide the only path to an action behind a swipe | Gestures supplement a visible control, never replace it |
| Re-derive WCAG contrast or screen-reader issues | Defer to the accessibility audit |
| Report only tap-target size | Sweep all seven areas; cite the principle and threshold |

---

## Source lessons (Uxcel)

- [Responsive vs. Adaptive Design](https://uxcel.com/lessons/responsive-vs-adaptive-993)
- [Designing Mobile Layout](https://uxcel.com/lessons/mobile-layout-182)
- [Designing for Mobile Interfaces](https://uxcel.com/lessons/mobile-interfaces-244)
- [Platform Adaptivity & Scaling](https://uxcel.com/lessons/platform-adaptivity-scaling-217)
- [Ensuring Mobile Accessibility](https://uxcel.com/lessons/accessibility-779)
- [Mobile-Specific Functions & Interactions](https://uxcel.com/lessons/mobile-specific-functions--interactions-814)
