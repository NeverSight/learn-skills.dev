---
name: compact-landing
description: >-
  Build compact, distinctive landing pages and product skeletons without repeating
  one visual template. Use for package demos, developer tools, documentation intros,
  focused product pages, and micro-SaaS sites that should feel small, polished,
  tactile, product-specific, and visually different on each run. Vary composition,
  palette, typography, radius, surfaces, motifs, and safe motion while preserving
  clear actions, accessibility, responsive behavior, and zero layout shift.
---

# Compact Landing

Build a small, finished product world—not a generic marketing template. Preserve compactness and clarity; reinvent the visible design language for each product.

## Workflow

1. Inspect the product, supplied content, current stack, and existing design language. Reuse installed tools and components.
2. Ask for button size first—compact, medium, or large—unless the user already answered or asked you to choose.
3. Ask at most two adaptive questions only when their answers would materially change the result. Good subjects: brand mood, content depth, corner character, or motion level.
4. Create a design fingerprint before coding. If this skill includes scripts and Node is available, run `node scripts/pick-direction.mjs`. Otherwise choose from `references/style-dna.md` without taking the first option in every list.
5. Adapt the fingerprint to product meaning. Treat picker output as a creative constraint, not a command to make incoherent choices.
6. Identify one product-native signature artifact: a real demo, visualized output, interactive sample, comparison, miniature workflow, data specimen, or useful control. This should create identity more than decoration does.
7. Implement the smallest complete page. Prefer HTML/CSS and existing dependencies. Add JavaScript only for behavior the page actually needs.
8. Verify mobile layout, keyboard focus, reduced motion, stable dynamic states, and the real primary action.

If the user wants immediate execution, choose the button size and fingerprint yourself. Do not stop for a questionnaire.

## Design Fingerprint

Define these axes before implementation:

- **Composition:** field note, offset rail, split pamphlet, framed console, compact catalogue, stacked specimen, or another product-specific silhouette.
- **Measure:** choose a fitting compact width, usually `420-720px`; do not default to `440px` every time.
- **Palette:** warm paper, cool fog, monochrome ink, dark charcoal, product-tinted, or playful light.
- **Typography:** grotesk + mono, humanist sans + mono, editorial serif + sans, rounded sans + mono, condensed + sans, or purposeful all-mono.
- **Geometry:** sharp, machined, balanced, friendly, soft, or mixed/concentric radii.
- **Surface grammar:** whitespace, flat dividers, inset hairlines, layered rings, tinted panels, paper rules, or technical frames. Pick one dominant grammar.
- **Motif:** emoji punctuation, ASCII marks, indices, stamps, doodles, colored dots, tiny object icons, or none.
- **Motion:** choose one entrance behavior and one or two interaction behaviors.

Variation must change the first-screen silhouette, not merely colors or labels. Ensure at least four axes differ from the old canonical recipe: centered `440px` column, neutral white/zinc, Geist + Geist Mono, `6-10px` radii, inset hairline cards, Instrument order, staggered rise.

Do not randomize components independently. Choose one coherent art direction, then derive tokens from it. Use only one or two surprising details; repetition inside the page creates coherence.

Read `references/style-dna.md` for compatible ranges, direction families, motion patterns, and review checks.

## Invariants

- Keep the page compact in scope and information density, even when its canvas is wider or split.
- Put the primary action in the first viewport. Repeat it only when doing so removes friction.
- Use clear type hierarchy, concrete copy, and enough contrast.
- Use real product content. Avoid fake metrics, vague claims, filler testimonials, and decorative dashboards.
- Extend visually tiny controls to at least a `40px` hit area without making them look oversized.
- Show a visible `:focus-visible` state and preserve semantic HTML.
- Use tabular numerals for changing numbers.
- Respect `prefers-reduced-motion` and keep the reduced experience fully usable.
- Never add a dependency for a small effect CSS or the current stack can handle.

## Zero-Shift Motion

- Animate only `transform`, `opacity`, and `filter`. Never use `transition: all`.
- Reserve dimensions before animation: fixed/min heights, `aspect-ratio` for media, fixed icon slots, width-locked changing labels, and tabular numerals.
- Overlay alternate labels, icons, tabs, and panels in the same grid area or fixed box. Do not insert delayed content into document flow.
- Keep padding, borders, font size, font weight, line height, grid tracks, and flex sizing stable across hover and state changes.
- Prefer transforms for toggles, drawers, traces, and decorative motion. Absolute-position decorative particles so they never affect flow.
- Self-host fonts when practical. Otherwise use metric-compatible fallbacks and avoid hiding the page while fonts load.
- Gate hover-only effects behind `(hover: hover) and (pointer: fine)`.

## Buttons

Apply one scale consistently:

- **Compact:** `24-28px` visual height, `11-12px` label.
- **Medium:** `32-36px` visual height, `12.5-13px` label.
- **Large:** `40-44px` visual height, `13.5-14px` label.

Use `scale(0.96)` for press feedback. For wide command controls, use `0.98`. Keep label and icon slots stable during copied/loading/success states.

For `llms.txt` or assistant-copy actions, use a small mono button only when the product needs it. Reuse the project's icon system or a CSS glyph; do not embed SVG examples in skill output.

## Purposeful Personality

Emoji are allowed when they fit the product. Use `1-3` as punctuation, labels, tiny stickers, or state cues—not as a substitute for structure or iconography. Reserve their boxes so platform glyph differences do not move layout.

Color may be playful, dark, editorial, or product-tinted. Give every accent a role and repeat it. Avoid default purple-blue AI gradients, uncontrolled rainbows, and random decorative color.

Motion should explain state, focus attention, or express the product metaphor. A fixed-size trace, ambient floating mark, slot swap, clipped reveal, or state color wash can feel alive without causing reflow. Avoid perpetual motion everywhere.

## Avoid

- Reusing one section order, narrow width, palette, radius family, or component set across unrelated products.
- Generic oversized heroes, three equal feature cards, badge clouds, and feature grids by reflex.
- Copying the Cuelume waveform, cream palette, confetti trio, or exact layout unless the product genuinely calls for them.
- Making every surface a card or every control a pill.
- Decorative animation that competes with the primary action.
- Heavy animation libraries for opacity, transforms, tabs, counters, or simple reveals.

## Final Check

- Fingerprint chosen before code; at least four high-salience axes differ from the canonical recipe.
- Product-native signature artifact is visible and useful.
- First viewport has a distinct silhouette and clear primary action.
- Radius, palette, type, surface, motif, and motion form one coherent direction.
- Mobile becomes a clean single column without horizontal overflow.
- Dynamic content, media, icons, labels, and panels have reserved geometry.
- Keyboard, focus, contrast, touch targets, and reduced motion work.
- Build and the primary interaction pass using the project's existing verification path.
