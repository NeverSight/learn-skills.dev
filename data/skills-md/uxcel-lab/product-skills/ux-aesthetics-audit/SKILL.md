---
name: ux-aesthetics-audit
description: Audit the visual quality of a UI against established visual-design principles — hierarchy, emphasis, contrast, spacing, alignment, grouping, consistency, and depth. Produces a severity-rated issue list with concrete fixes. Specializes in catching overdesign, clutter, and competing focal points. Use when reviewing whether a screen looks professional, or as a validation step after generating UI.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Visual Aesthetics Audit Skill


## How this skill behaves (read first)

This is an **evaluative** skill — it reviews existing work, it doesn't generate. It auto-runs and is built to be **called as a validation step** by generative skills. It's the **visual-quality backbone** of the repo: generators that produce UI (`pricing`, `login-signup`, `dashboard`, `onboarding`, component skills) hand off here to confirm they didn't tip into clutter or break hierarchy.

It owns **visual composition**. Two deliberate deferrals so it doesn't duplicate:

- **Color-contrast ratios, and any accessibility concern** (keyboard, screen readers, alt text) → the **accessibility audit**. This skill judges *visual* contrast/emphasis and harmony, not WCAG ratios.
- **Usability, flow, and interaction logic** → the **heuristics audit**. This skill judges how it *looks*, not how it *works*.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier B — offered (and suppressed when a design system already defines visual harmony)**. Explicit scope always wins.

---

## What this skill changes vs. default behavior

By default, visual feedback is vague and subjective — "make it cleaner", "add more spacing", "looks a bit busy" — with no principle, no severity, and no fix. This skill forces:

1. **Every finding names the violated principle** (hierarchy, emphasis, proximity, etc.).
2. **Severity rated** by whether it breaks scanning/comprehension or is just polish.
3. **A concrete fix**, not a vibe.
4. **An explicit overdesign pass** — the failure mode generators most need caught, and the one "more best practices" tends to cause.

It is **not** taste-policing: flag principle violations that cost scanning, comprehension, or perceived quality — not personal style preferences.

---

## The evaluation framework — what to check and what a violation looks like

Work through each. Flag with **principle**, **severity**, **fix**.

### 1. Visual hierarchy & eye-flow
Users should have one clear entry point and a guided path through the content (scale, weight, color, spacing, position). Hierarchy is achieved through movement, contrast, and proportion.

**Flag when:** no obvious place the eye lands first; the primary action isn't the most prominent element; everything is the same visual weight; reading order fights the layout.

- ❌ Three cards, three "primary" buttons, a big hero image, and a banner all competing — eye doesn't know where to go.
- ✅ One dominant focal point (the primary action / key message); everything else recedes.

### 2. Emphasis & contrast
Emphasis makes *one* element the focal point (Von Restorff). Contrast is the difference *between* elements — aim for **more than one point** of contrast (size + color, shape + position), and pair a bold accent with a **neutral anchor** so the eye has somewhere to rest.

**Flag when:** everything is emphasized (so nothing is); a single weak contrast dimension; high-saturation colors everywhere with no neutral to absorb tension ("Willy Wonka" palette).

- ❌ Every section uses a bright accent color → visual noise, no focal point.
- ✅ Mostly neutral surface with one accent reserved for the key action.

### 3. Spacing & negative space
White space is breathing room, not waste. *Passive* space separates within groups; *active* space deliberately spotlights an element. You don't notice passive space "until there's too little."

**Flag when:** cramped, content jammed edge-to-edge; uneven/inconsistent gaps between similar elements; *or* the opposite — so much empty space the content feels disconnected and aimless.

- ❌ Form fields and labels packed with no breathing room → feels stressful, hard to scan.
- ✅ Consistent, generous spacing that groups related items and gives the focal point room.

### 4. Alignment & grid
Elements should sit on a common axis / shared grid. Alignment creates a structured, professional, calm impression.

**Flag when:** ragged edges, elements off the grid, inconsistent margins/gutters, headers that don't align to the column structure.

- ❌ Labels left-aligned, inputs centered, button floating off-axis.
- ✅ One consistent alignment system; intentional breaks only.

### 5. Grouping & proximity
Related items sit close; unrelated items are separated (Gestalt proximity). Similarity (shared shape/size/color) unifies items of equal importance.

**Flag when:** related items are far apart or divided by a border while unrelated items crowd together; equal-importance items (e.g. a row of cards) are styled inconsistently.

- ❌ A field's helper text sits closer to the *next* field than its own.
- ✅ Spacing encodes the grouping; a row of cards shares one consistent treatment.

### 6. Consistency & repetition
Repeating elements (color, shape, type, spacing) creates unity and a learnable rhythm. The color system should be deliberate — *one* blue, not three near-identical ones.

**Flag when:** the same component styled differently across the screen; near-duplicate colors/radii/shadows that should be one token; buttons of the same importance looking different.

- ❌ Three slightly different grays and two button radii with no reason.
- ✅ A small, consistent set of styles applied repeatably.

### 7. Typographic hierarchy
Build hierarchy with size, weight, style, color, case — but **use no more than ~3 of those instruments**, keep to **2–3 heading levels**, and body text **≥16px**. Color in type used sparingly.

**Flag when:** a heading stacks big + bold + colored + uppercase + italic all at once; more than ~3 heading levels; tiny body text; color applied to too much type.

- ❌ Headline that is huge, bold, red, AND all-caps → cluttered, shouting.
- ✅ Size + weight alone separates levels cleanly; color reserved for one accent.

### 8. Depth & elevation
Shadows signal elevation and draw the eye to lifted surfaces (cards, modals, FABs). A single, consistent light direction and a defined elevation scale keep depth readable.

**Flag when:** shadows fall in different directions on the same screen; every element has a shadow (so elevation means nothing); shadows stacked on a card *and* its inner buttons/icons.

- ❌ Card has a shadow, its button has a shadow, its icon has a shadow → muddy, no real hierarchy.
- ✅ One elevation level per surface; shadows share a light direction.

> **The overdesign pass (cross-cutting).** After the eight checks, step back: are there multiple competing focal points? More than a couple of accent colors? Stacked shadows? >3 type treatments? Decorative elements that don't serve the task? If the screen feels busy, name *which* principles are over-applied — this is the specific signal generators rely on.

---

## Severity rating

| Severity | Meaning |
|---|---|
| **Critical** | Hierarchy collapses — no discernible focal point / the primary action doesn't stand out, or clutter is severe enough that the user can't tell what matters. The visual design fails its job. |
| **Major** | Competing emphasis, inconsistent component styling, cramped or uneven spacing, misalignment, >3 type instruments, clashing/stacked shadows — slows scanning and erodes perceived quality. |
| **Minor** | Polish — slightly off proportions, one small inconsistency, a subtle-contrast element that reads as a near-mistake. |

Rate by impact on **scanning, comprehension, and perceived quality** — not by how subjective the fix feels. Note the **aesthetic-usability effect**: a polished look earns tolerance for minor usability issues, but never let "it looks nice" excuse a broken hierarchy.

---

## Audit output format

```
## Visual Aesthetics Audit — [Screen / Component]
Context: [platform · primary task / focal action, if known]

### Critical
- [Issue] — what's wrong → fix. (Principle: …)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Overdesign verdict:** [clean / borderline / overdesigned] — the 1–3 over-applied principles to pull back.
**Top 3 priorities:** the highest-impact fixes.
```

End with the overdesign verdict and the prioritized top 3 — that's what a calling generator acts on.

---

## How to run a good audit

1. **Establish context** — platform and the screen's *primary task / focal action*. Hierarchy can only be judged against what's supposed to be most important.
2. **Serve the task, not decoration.** Every element should earn its visual weight; flag decoration that competes with content.
3. **Don't taste-police.** Flag principle violations that cost scanning/comprehension/quality, not style you'd personally choose differently.
4. **Run the overdesign pass explicitly** — it's the highest-value output and the reason generators call this skill.
5. **Defer** contrast-ratio/accessibility to the accessibility audit and usability/flow to the heuristics audit; don't re-derive them here.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Make it cleaner / less busy" | Name the over-applied principle + the specific fix |
| Treat every nit as equal | Rate by impact on hierarchy/scanning; surface top 3 |
| Emphasize everything | One focal point; everything else recedes |
| One weak contrast dimension | More than one point of contrast + a neutral anchor |
| Accent color everywhere | Mostly neutral; accent reserved for the key action |
| Stack big+bold+color+caps on a heading | ≤3 type instruments; 2–3 heading levels; body ≥16px |
| Shadow on the card and its inner button and icon | One elevation level per surface; consistent light direction |
| Re-derive WCAG contrast or keyboard issues | Defer to the accessibility audit |
| Flag subjective style preferences | Flag only principle violations that cost the user |

---

## Source lessons (Uxcel)

- [13 Core Visual Design Principles](https://uxcel.com/lessons/definitions-593)
- [Visual Design Analysis](https://uxcel.com/lessons/visual-design-analysis-723)
- [Positive & Negative Space in Design](https://uxcel.com/lessons/dc--lesson-552)
- [Contrast in Design Composition](https://uxcel.com/lessons/dc--lesson-766)
- [Typographic Hierarchy](https://uxcel.com/lessons/typographic-hierarchy-107)
- [Elevation & Shadows in Design Systems](https://uxcel.com/lessons/elevation-shadows-272)
- [Establishing Relationships in Design Composition](https://uxcel.com/lessons/dc--lesson-112)
