---
name: ux-design-from-scratch
description: Orchestrated, build-from-zero UX workflow. Establishes context once, then composes the generative ladder in order — foundations (color, type, spacing) → components → screens → flows — applying each skill with relevance gating, and hands the result to design-review. Trigger when the user is starting a new product/app/UI from scratch, "help me design an app", "set up a design system and screens", "I'm starting a new product", or any multi-artifact design build — but NOT when they ask for one specific screen or component (let that skill trigger directly).
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Design From Scratch (UX Creation Orchestrator) Skill

## How this skill behaves (read first)

This is the **front door for building a new design from zero**, and the generative twin of
`ux-design-review`. Where design-review orchestrates the *validation* direction
(generative → audit), this skill orchestrates the *compositional* direction
(generative → generative): it sequences the **scope ladder** — foundations → components →
screens → flows — pulling in each lower-scope skill as the work needs it, then hands the result
to design-review for validation.

It is the executable form of the **compositional orchestration** section of
`docs/orchestration-policy.md`. Its whole job is to avoid two failures: building a single screen
with no system underneath it, and over-building everything (all foundations, all 12 components)
when the product only needs a few.

**When NOT to use this skill:** if the user asks for one specific artifact ("design a pricing
page", "build a date-picker"), let that skill trigger directly. This orchestrator is for
multi-artifact, from-scratch builds. Explicit scope overrides orchestration.

---

## Step 0 — Establish the context profile (once)

The single most important field here is the inverse of the review case:

- **Design system in play?** For a true from-scratch build the answer is usually **no** → the
  **foundation skills are in scope and come first**. If the user *does* have tokens/a styleguide
  already, **skip the foundations** and start at components/screens, inheriting their system (the
  suppression matrix, applied to creation).
- **What's being built** — a single screen with its system, a small flow, or a whole product
  surface? This sets how far down the ladder to go and how many screens/components to compose.
- **Platform** — mobile vs. web (changes layout, touch targets, navigation patterns).
- **Brand / audience / industry** — drives the gated decisions inside the foundation and screen
  skills (color emotion, tone, security posture).

State the assumptions you're proceeding with, then build in order.

---

## Step 1 — Compose the ladder, gating at each rung

Walk the ladder top-down. At each rung, classify the child skills into **core / offer / skip**
(see the policy's compositional model) — don't apply every skill at a rung by default.

> Child skills are named by their installable skill `name`. Compose one only if it's installed;
> if a named skill isn't present, apply that rung's intent inline with general best practice and
> note the gap rather than blocking the build.

### Rung 1 — Foundations (only if no design system)
Establish the system first so everything above is consistent:

- **Core:** `ux-color`, `ux-typography`,
  `ux-layout-spacing-grids` — a product needs a palette, type scale, and spacing
  system before screens are meaningful.
- **Offer:** `ux-iconography` (if the product is icon-heavy).
- **Skip entirely** if a design system already exists — inherit its tokens.

Each foundation skill still **gates** its own context-dependent decisions (don't auto-pick dark
mode, brand saturation, etc.).

### Rung 2 — Components (only those the screens need)
Pull in component skills **on demand**, driven by the screens being built — not all of them:

- A form-bearing screen → `ux-inputs-and-forms`, `ux-buttons`,
  `ux-selection-controls`.
- A data screen → `ux-tables`, `ux-search`.
- Overlays/feedback → `ux-modals-and-dialogs`,
  `ux-notifications-and-toasts`, `ux-loaders-and-progress`.
- Navigation → `ux-navigation`, `ux-menus`.

Building every component skill "to be safe" is the bandwagon failure — only compose what a
requested screen actually contains.

### Rung 3 — Screens (the artifacts the user asked for)
Build the requested screens with the relevant skill (`ux-login-signup`,
`ux-pricing`, `ux-dashboard`, `ux-settings`, `ux-empty-states`,
`ux-landing-page`, `ux-activity-feed`, `ux-contact-support`). Each
screen skill gates its own context-dependent levers and reuses the foundations/components above
rather than re-deciding them.

### Rung 4 — Flows (if the build spans multiple screens as a journey)
If the product needs a journey, compose the flow skill (`ux-onboarding`,
`ux-checkout-payment`, `ux-error-recovery`, `ux-offboarding`), which sequences
the screens into a coherent path.

> **Consistency rule:** decisions made at a lower rung propagate up. A color/spacing decision
> made once in foundations is reused by every component and screen — don't re-litigate it per
> screen. This is the whole point of building bottom-up.

---

## Step 2 — Validate via design-review

When the artifacts exist, hand them to **`ux-design-review`** (if installed), which applies the
audit policy (Tier A auto-runs; Tier B offered; and since you just *built* the foundations, the
visual-foundation audits are **in scope here**, not suppressed — the design system is brand-new
and worth checking). Resolve any findings back toward the primary task. If `ux-design-review`
isn't installed, run whichever audit lenses *are* present directly, or self-review against the
policy.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Jump straight to screens with no color/type/spacing system | Establish foundations first (when there's no existing design system) |
| Build all 12 component skills "to be safe" | Compose only the components the requested screens contain |
| Re-decide color/spacing inside every screen | Decide once in foundations; reuse upward |
| Run this orchestrator for a single named screen/component | Let that skill trigger directly (explicit scope wins) |
| Skip foundations because "the screen looks fine" | A screen with no system underneath isn't a design — it's a mockup |
| Declare done after generating | Hand to design-review for validation |

---

## Relationship to the policy

This skill *is* the compositional-orchestration section of `docs/orchestration-policy.md` in
executable form. If the two diverge, the policy governs; update this skill to match it. Its
validation twin is `ux-design-review`.

## Source lessons (Uxcel)

This is an orchestrator — its substance lives in the skills it composes. See the source lessons
in each foundation, component, screen, and flow skill it routes to (e.g.
`ux-color`, `ux-inputs-and-forms`, `ux-pricing`,
`ux-onboarding`).
