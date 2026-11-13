---
name: ux-design-review
description: Orchestrated, holistic UX review of a screen, flow, or component. Establishes context once, auto-runs the always-relevant lenses (usability, microcopy, dark patterns), offers the context-dependent ones (accessibility, aesthetics, IA, mobile, visual foundations), and returns one prioritized report. Trigger when the user asks for a full design review, "review my UI/screen/flow", "is this good UX", "audit this design", or general design feedback — but NOT when they name a single specific lens.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Design Review (UX Orchestrator) Skill

## How this skill behaves (read first)

This is the **front door for holistic UX review**. It is the executable form of
`docs/orchestration-policy.md` — it decides *which* audit lenses run, which are offered, and
which are suppressed, then returns **one** prioritized report instead of a pile of separate
audits.

Its whole job is to avoid two opposite failures: doing a flat "looks good" review with no
framework, and firing every audit in the repo regardless of relevance (the bandwagon).

**When NOT to use this skill:** if the user named a specific lens ("run the accessibility
audit", "check this for dark patterns"), skip this orchestrator and invoke that one skill
directly. Explicit scope overrides orchestration.

---

## Step 0 — Establish the context profile (once)

Infer these from what the user gave you; ask only the one that's unknown *and* changes what
runs. Persist for the session — don't re-ask.

- **Design system in play?** Infer **yes** if they provided tokens, a styleguide, a component
  library, a Figma library, themed component code, or said "our design system / our brand
  guidelines." Otherwise ask once: *"Are you working from an established design system, or
  designing from scratch?"* — this is the single biggest driver of what gets skipped.
- **Platform** — mobile or web (decides whether mobile-responsiveness is relevant).
- **Primary task** — what the user actually came to do (used to resolve conflicts later).

State the assumptions you're proceeding with in one line.

---

## Step 1 — Determine the traits of the work

Look at the artifact and note which are true:

- **Interactive UI?** (almost always yes)
- **Contains user-facing copy?**
- **Involves conversion / pricing / sign-up friction / opt-ins / cancellation?**
- **Multi-screen or structures content?**
- **Targets mobile?**

---

## Step 2 — Auto-run the always-relevant lenses (Tier A)

Run these whenever their trait is present. They don't depend on the visual system and almost
always earn their keep:

- **`ux-heuristics-audit`** — any interactive UI. Usability behavior, feedback, error recovery.
- **`ux-microcopy-audit`** — any user-facing copy. Clarity, tone, error/empty/CTA wording.
- **`ux-dark-patterns-audit`** — any conversion/pricing/opt-in/cancellation surface.

These run unprompted. The design-system profile does **not** suppress them.

> Each lens is named by its installable skill `name`. Invoke a lens only if that skill is installed; if one isn't, list it under "available but not run" in the report and don't block — this orchestrator degrades to whichever lenses are present.

---

## Step 3 — Offer the context-dependent lenses (Tier B)

These are relevant but should be **offered**, not fired — and several are suppressed when a
design system is in play. Apply the suppression matrix from the policy:

| Lens | Offer when | If design system in play |
|---|---|---|
| `ux-accessibility-audit` | any UI | **Narrow to usage** — custom color combos, focus order, alt text, labels; don't re-audit the token palette |
| `ux-aesthetics-audit` | any visual UI | **Suppress** — visual harmony is already defined |
| `ux-information-architecture-audit` | multi-screen / structured content | Unaffected — offer |
| `ux-mobile-responsiveness-audit` | platform = mobile | Unaffected — offer |
| `ux-color` (as lens) | palette is being defined/changed | **Suppress** — tokens own color |
| `ux-typography` (as lens) | type is being defined/changed | **Suppress** — tokens own type |
| `ux-layout-spacing-grids` (as lens) | spacing/grid is being defined/changed | **Suppress** — the scale owns spacing |

Say the suppression out loud, briefly: *"Your design system owns color, type, and spacing, so
I'm skipping those and checking how the system is applied (accessibility-in-use, IA, copy)."*

Then offer the rest: *"Want me to also run accessibility-in-use and an IA pass?"* If the user
opts in, run them; otherwise leave them listed as available.

---

## Step 4 — Merge into one prioritized report

De-duplicate findings across lenses (if heuristics and accessibility both flag the same
unlabeled control, report it once, tagged with both). Resolve any cross-lens conflicts toward
the **primary task** from Step 0. Output a single severity-ordered list:

```
## Design Review — [target]
Context: [platform · design system: yes/no · primary task]
Lenses run: [heuristics, microcopy, …]   Lenses available but not run: [aesthetics, …]

### Critical
- [Issue] — what's wrong → fix. (heuristic / a11y / dark-pattern / …)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest-impact fixes across all lenses.
Offered, not run: accessibility-in-use, IA — say the word and I'll add them.
```

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Fire all seven UX audits because the work "is a UI" | Auto-run Tier A; offer Tier B; suppress what the design system owns |
| Re-audit color/type/spacing when the user has a design system | Skip them out loud; check application instead |
| Return one report per audit | Merge into a single prioritized, de-duplicated list |
| Run this orchestrator when the user asked for one named lens | Defer to that lens directly (explicit scope wins) |
| Silently skip accessibility because there's a design system | Narrow it to usage checks — never drop it entirely |

---

## Relationship to the policy

This skill *is* `docs/orchestration-policy.md` in executable form. If the two ever diverge,
the policy governs; update this skill to match it.

## Source lessons (Uxcel)

This is an orchestrator — its substance lives in the lenses it routes to. See the source
lessons in each: `ux-heuristics-audit`, `ux-microcopy-audit`, `ux-dark-patterns-audit`,
`ux-accessibility-audit`, `ux-aesthetics-audit`, `ux-information-architecture-audit`,
`ux-mobile-responsiveness-audit`.
