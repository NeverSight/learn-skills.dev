---
name: flow-design
description: "Visual direction and design system: tokens plus a DESIGN.md. Use before building a new product, page or rebrand, or when a new surface has no design system yet. Hands off to `flow-ui` or `flow-prototype`."
metadata:
  stage: plan
---

# Design direction

Decide how the interface should look and feel before anyone writes components, and write it down
so every screen comes out consistent. Direction comes from the brief and the users, never from
the agent's defaults.

## Phase 1: Read the constraints

- **Existing system first.** Look for tokens, a component library, a brand guide, a DESIGN.md or
  shipped screens. If one exists, extend it; this skill then only fills gaps.
- **Established systems.** Government, regulated, enterprise or platform-native products usually
  have an official system (for example a national government design system, or a platform's own
  guidelines). Use the official package over imitation. One system per project.
- **Audience and context:** who uses it, on which devices, how often, and what they need to trust.
  Accessibility-first, public-sector and children's audiences override aesthetic preference.
- **Content:** what the screens actually show. Dense data and long-form reading want different systems.

## Phase 2: Choose a direction

1. Write the direction as one line: surface type, audience, visual language, and system or
   archetype. Example: "Pricing page for finance teams, calm editorial, serif display over a
   neutral grotesk, one deep green accent."
2. Set three dials from 1 to 10 and record them. Each band changes concrete choices:
   - **Density:** 1-3 airy marketing; 4-6 balanced product; 7-10 data-dense (tables, dividers
     instead of cards, tabular numbers, compact controls).
   - **Variance:** 1-3 conventional and predictable (trust, forms, public services); 4-6 some
     asymmetry and bolder type; 7-10 editorial layouts and unusual composition (portfolios,
     launches). Higher variance needs a stronger reason.
   - **Motion:** 1-3 state feedback only; 4-6 purposeful transitions; 7-10 choreographed sequences.
     Every level honors reduced motion.
3. When two readings of the brief lead to materially different designs, ask one question. Otherwise
   state your reading and proceed.

[references/directions.md](references/directions.md) describes common archetypes as starting
points with their tradeoffs. Blend or depart from them when the brief calls for it.

## Phase 3: Define the system

Write tokens in the project's format (CSS custom properties, theme config or token JSON) and a
DESIGN.md using [references/design-md.md](references/design-md.md). Cover:

- **Type:** at most two families plus an optional mono, a modular scale (ratio about 1.2 to 1.333),
  `clamp()` for display sizes, body at least 16px, line length 45-75 characters, weights actually used.
- **Color:** semantic roles (surface, text, muted, border, accent, danger, success, focus), one
  accent, one neutral family with a consistent tint, and pairs that meet contrast in every theme.
  Dark mode gets its own tuned values, with elevation shown by lightness.
- **Space and shape:** a 4 or 8px spacing scale, one radius system (inner radius smaller than outer),
  one shadow or elevation scale, a container width and grid.
- **Motion:** durations (fast 100-150ms, base 200-300ms, slow 400ms+), two or three easing curves,
  and what motion is for. Reduced-motion behavior is written down.
- **Consistency locks:** one accent, one radius system and one theme per page unless the direction
  says otherwise.

## Phase 4: Check for the generic default

Review the direction and a sample screen against [references/generic-tells.md](references/generic-tells.md).
Each tell is a default to question, not a ban: keep it when the brief justifies it, and say why.

## Anti-patterns

- Picking fonts and colors from habit, then justifying them afterward.
- Replacing a working design system because a different look was requested for one page.
- Style rules that can't be checked ("feels premium") instead of tokens and thresholds.
- Mixing archetypes until the result has no point of view.
- Decorative trust signals: invented logos, testimonials or metrics.

## Done when

- A one-line direction, dial values and the reasoning behind them are recorded.
- Tokens and a DESIGN.md exist in the project's format, with contrast checked in every theme.
- A sample screen or component shows the system applied, and the generic-tells review is noted.

Build with `flow-ui`, or test a risky direction first with `flow-prototype`.
