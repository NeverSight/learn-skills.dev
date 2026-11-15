---
name: antislop-designsystem
description: "Design-system and consistency rules: real tokens, a spacing scale, radius/shadow hierarchy, theme parity, and no page-wide uniform treatment. Map to antislop-master section I and D. Use when building or auditing a design system or multi-screen app."
allowed-tools: Read Write Edit Glob Grep
---
# antislop-designsystem

> Design-system consistency rules for anti-ai-slop. Map to **I-1 … I-5** (P2/P3) and **D-1, D-6** (components) in `antislop-master`.
>
> The point of a system is **hierarchy, not uniformity.** A page where everything is treated the same has no hierarchy — and uniform is the deep AI tell (I-3).

---

## Tokens are real, not decorative

- **Radius**: a small set (e.g. 2/6/10/16) and a rule for when each applies — never `rounded-2xl` on everything. (D-1)
- **Spacing**: one scale (4/8/12/16/24/32/48/64). **No ad-hoc values.** (I-2)
- **Color**: 2–3 core + 1 accent, with an explicit role for each. Not the same family everywhere. (I-1)
- **Shadow**: elevation markers only — a small set, applied by elevation, not on every card. (D-6)
- **Type**: a scale and a weight hierarchy that respond to content, not a single size on repeat. (B-7)

## The uniformity trap

- **Same visual treatment on the entire page** = nothing is special = nothing is important. Break it deliberately. (I-3)
- **Components that contradict the tokens** in `DESIGN.md` are findings, even if they look fine in isolation. (I-4)

## Themes

- **Light and dark must both be complete.** A toggle where one mode is visibly unfinished is a P4/P3 fail. (I-5)
- **Choose the theme from brand identity**, not "dark looks tech". (see A-7)

## Hierarchy over consistency

The system serves **decision-making**, not sameness:
- A **primary** action is visually heavier than a **secondary**, which is heavier than a **tertiary**.
- A **focus** element (the one thing to click) is distinct from supporting cards.

If the system makes every element equal, the system is wrong, not just the page.

---

## Audit checklist

- [ ] Radius, spacing, color come from tokens. (I-1, I-2)
- [ ] One accent role, not the same family everywhere. (I-1)
- [ ] Shadows mark elevation, not default. (D-6)
- [ ] Both themes are complete. (I-5)
- [ ] The page has hierarchy, not uniform treatment. (I-3)

Findings cite the code from `antislop-master` plus one honest reason.
