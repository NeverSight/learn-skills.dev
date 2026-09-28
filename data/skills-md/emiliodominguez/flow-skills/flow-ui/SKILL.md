---
name: flow-ui
description: "Production UI built in a render, compare and fix loop. Use for new pages, screens or components, or to match a mockup or screenshot. Hands off to `flow-a11y` or `flow-review`."
metadata:
  stage: build
---

# UI

Ship interface code that looks intended, works in every state, and holds up at every width. The
rendered page is the source of truth, not the code or a description of it.

## Phase 1: Gather the contract

- **Inputs:** the brief, a design direction or DESIGN.md (`flow-design`), and any reference
  (screenshot, mockup, design-file export). No direction for a new surface? Run `flow-design` first.
- **Stack:** framework, styling approach, component library, tokens, icon set, fonts and existing
  patterns for similar screens. Reuse components before creating new ones; follow the existing
  conventions even if you would choose differently.
- **Content:** real copy and data from the user or the domain. Draft specific copy when none
  exists, never lorem ipsum. Label mock data as mock; never invent testimonials, customer logos
  or metrics presented as real.
- **Scope:** viewports (default 375, 768, 1280, 1920), themes, locales and the states to build.

## Phase 2: Structure before style

1. Break the screen into regions, then components, from the reference or brief. Name what repeats.
2. Write semantic HTML first: landmarks, heading order, real buttons, links and form controls.
3. Lay out with the grid and spacing scale from the tokens. Mobile-first, intrinsic sizing,
   `gap`, `minmax()`, `clamp()` for fluid type and space, container queries where a component
   lives in different widths.
4. Apply tokens for type, color, radius, shadow and motion. Add a token only when a value
   repeats; keep one-offs local.

## Phase 3: Build every state

Each interactive or data-driven element gets, where relevant: default, hover, focus-visible,
active, disabled, loading (skeletons shaped like the content), empty (with a next action),
error (specific message and recovery), success, overflow (long names, many items, missing
images) and right-to-left or long translations. See [references/states.md](references/states.md).

## Phase 4: Render, compare, fix

Render the page with whatever browser or screenshot tooling is available and loop until clean.

- **Against a reference:** compare at the reference's width. Check layout grid and alignment,
  spacing rhythm, type size, weight and line height, color and contrast, radius and shadow,
  imagery crop, and icon weight. Fix the largest structural differences first; see
  [references/fidelity-loop.md](references/fidelity-loop.md).
- **Across widths:** no horizontal overflow, readable line length (about 45-75 characters),
  sensible reflow rather than squashing, tap targets at least 24px, nothing hidden under sticky UI.
- **Quality bar:** a clear hierarchy (one primary action per view), consistent spacing, aligned
  edges and baselines, and no generic template tells (see `flow-design`).
- **Loading cost:** no layout shift while fonts or images load (reserved dimensions, fallback font
  metrics), responsive images with explicit sizes, the largest above-the-fold element not lazy
  loaded, and no heavy dependency for a small effect. Measure with `flow-benchmark` when a
  Core Web Vitals budget applies.
- Stop when two consecutive passes find nothing material, or name what remains.

Without rendering access, say which visual claims are unverified instead of implying they pass.

## Anti-patterns

- Building from memory of "what sites look like" instead of the brief, tokens and reference.
- Pixel-matching a mockup at one width while every other width breaks.
- Happy-path-only screens with no loading, empty or error state.
- Adding a UI library, animation framework or font the project doesn't use without asking.
- Divs as buttons, placeholder-only labels, or icon buttons without names.

## Done when

- The screen renders correctly at every scoped width and theme, with screenshots or a named gap.
- Every relevant state exists and was exercised.
- Code follows local conventions, reuses existing components and passes the repository gates.

Run `flow-a11y` for an accessibility pass, `flow-animate` for motion, then `flow-review`.
