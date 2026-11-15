---
name: frontend-design
description: Use when building web components, pages, artifacts, or applications — especially when high design quality is needed. Generates creative, polished code that avoids generic AI aesthetics (purple gradients, Inter font, card-in-card layouts).
---

# Frontend Design

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. Before doing any design work, confirm:

- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**Gathering order:**
1. **Check current instructions**: If your loaded instructions contain a Design Context section, proceed immediately.
2. **Check `.impeccable.md`**: If it exists in the project root and has context, use it.
3. **Ask the user**: If neither source has context, ask these 3 questions before proceeding.

---

## Design Direction

Commit to a **BOLD** aesthetic direction before writing any code:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme — brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing users remember?

**CRITICAL**: Choose a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work — the key is **intentionality**, not intensity.

Implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

---

## Frontend Aesthetics Guidelines

### Typography
→ *See [typography reference](reference/typography.md) for scales, pairing, and loading strategies.*

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (`clamp()`)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts — Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes
**DON'T**: Put large icons with rounded corners above every heading

### Color & Theme
→ *See [color reference](reference/color-and-contrast.md) for OKLCH, palettes, and dark mode.*

**DO**: Use modern CSS color functions (`oklch`, `color-mix`, `light-dark()`) for perceptually uniform palettes
**DO**: Tint your neutrals toward your brand hue
**DON'T**: Use gray text on colored backgrounds — looks washed out; use a shade of the bg color instead
**DON'T**: Use pure black (`#000`) or pure white (`#fff`) — always tint
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon on dark
**DON'T**: Use gradient text for "impact" on metrics or headings
**DON'T**: Default to dark mode with glowing accents without real design decisions

### Layout & Space
→ *See [spatial reference](reference/spatial-design.md) for grids, rhythm, and container queries.*

**DO**: Create visual rhythm through varied spacing — tight groupings, generous separations
**DO**: Use fluid spacing with `clamp()` that breathes on larger screens
**DO**: Use asymmetry and unexpected compositions; break the grid intentionally
**DON'T**: Wrap everything in cards — not everything needs a container
**DON'T**: Nest cards inside cards — visual noise
**DON'T**: Use identical card grids (same-sized card with icon + heading + text, repeated)
**DON'T**: Center everything — left-aligned text with asymmetric layouts feels more designed
**DON'T**: Use the same spacing everywhere

### Visual Details
**DO**: Use intentional, purposeful decorative elements that reinforce brand
**DON'T**: Use glassmorphism everywhere — blur/glass/glow as decoration rather than purpose
**DON'T**: Use rounded rectangles with generic drop shadows — forgettable
**DON'T**: Use sparklines as decoration
**DON'T**: Use modals unless there's truly no better alternative

### Motion
→ *See [motion reference](reference/motion-design.md) for timing, easing, and reduced motion.*

**DO**: Use motion to convey state changes — entrances, exits, feedback
**DO**: Use exponential easing (`ease-out-quart/quint/expo`) for natural deceleration
**DO**: For height animations, use `grid-template-rows` transitions instead of animating `height`
**DON'T**: Animate layout properties (width, height, padding, margin) — use `transform` and `opacity` only
**DON'T**: Use bounce or elastic easing — dated and tacky

### Interaction
→ *See [interaction reference](reference/interaction-design.md) for forms, focus, loading patterns.*

**DO**: Use progressive disclosure — start simple, reveal sophistication through interaction
**DO**: Design empty states that teach the interface, not just say "nothing here"
**DON'T**: Make every button primary — use ghost buttons, text links, secondary styles
**DON'T**: Repeat the same information redundantly

### Responsive
→ *See [responsive reference](reference/responsive-design.md) for mobile-first, fluid design.*

**DO**: Use container queries (`@container`) for component-level responsiveness
**DO**: Adapt the interface for different contexts — don't just shrink it
**DON'T**: Hide critical functionality on mobile

### UX Writing
→ *See [UX writing reference](reference/ux-writing.md) for labels, errors, and empty states.*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

Review the DON'T guidelines above — they are the fingerprints of AI-generated work from 2024-2025.

---

## Implementation Principles

Match implementation complexity to the aesthetic vision:
- **Maximalist designs** → elaborate code, extensive animations, rich effects
- **Minimalist designs** → restraint, precision, careful spacing, subtle details

Interpret creatively and make unexpected choices that feel genuinely designed for the context. **No design should be the same.** Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

---

## Quick Reference: What to Avoid

| Category | DON'T |
|----------|-------|
| **Fonts** | Inter, Roboto, Arial, Open Sans |
| **Colors** | Pure black/white, purple gradients, gray on color |
| **Layout** | Cards in cards, centered everything, identical grids |
| **Motion** | Bounce/elastic easing, animating height/width |
| **Visual** | Glassmorphism everywhere, gradient text, generic shadows |
| **Writing** | "OK", "Submit", redundant copy, vague errors |
