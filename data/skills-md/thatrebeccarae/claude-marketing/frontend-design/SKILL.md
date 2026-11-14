---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Covers design thinking, typography pairing, color theory, motion design, spatial composition, and code quality. Generates real working code — HTML/CSS/JS or React — with intentional aesthetic direction, not generic AI output."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: creative
  domain: frontend
  updated: 2026-03-13
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Frontend Design

Create distinctive, production-grade web interfaces that avoid generic AI aesthetics.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/frontend-design ~/.claude/skills/
```

## Design Thinking Process

### 1. Understand Context

Before writing code, answer:
- **Purpose:** What problem does this interface solve? Who uses it?
- **Audience:** Technical sophistication, expectations, emotional state when arriving
- **Constraints:** Framework requirements, browser support, performance budget, accessibility needs

### 2. Commit to an Aesthetic Direction

Choose a specific point of view — not "clean and modern" but a real aesthetic:

| Direction | Characteristics |
|-----------|----------------|
| Brutally minimal | Monochrome, system fonts, stark spacing, no decoration |
| Maximalist | Dense, layered, multiple type scales, rich texture |
| Retro-futuristic | Neon accents, dark backgrounds, grid lines, monospace |
| Organic/natural | Soft shapes, earth tones, hand-drawn elements, warm |
| Luxury/refined | Thin serifs, generous whitespace, muted palette, restrained |
| Playful/toy-like | Rounded shapes, bright primaries, bouncy animations |
| Editorial/magazine | Strong grid, dramatic type hierarchy, pull quotes |
| Brutalist/raw | Exposed structure, monospace, raw HTML feeling |
| Art deco/geometric | Symmetry, metallic accents, decorative borders, angular |
| Soft/pastel | Light palette, gentle gradients, rounded, approachable |
| Industrial/utilitarian | Exposed grid, status indicators, dense information |

### 3. Identify the Memorable Thing

Every interface should have one element someone remembers:
- An unexpected interaction
- A distinctive type treatment
- A bold color choice
- An animation that surprises
- A layout that breaks convention

### 4. Execute with Intentionality

The key is commitment, not intensity. Maximalism executed fully works. Minimalism executed with precision works. The mushy middle does not.

## Typography

### Principles

- Choose distinctive fonts, NOT defaults (avoid Arial, Inter, Roboto for display use)
- Pair a display font (personality) with a body font (readability)
- Size hierarchy: display (48-96px), heading (24-36px), body (16-18px), small (12-14px)
- Tight letter-spacing on large display text (-0.02 to -0.04em)
- Normal or slightly loose spacing on body text

### Free Font Sources

| Source | Best For |
|--------|----------|
| Google Fonts | Widest selection, easy CDN |
| Fontshare | High-quality display fonts |
| Fontsource | Self-hosted, npm installable |
| Atipo Foundry | Distinctive display faces |

### Pairing Strategy

| Display | Body | Vibe |
|---------|------|------|
| Serif (dramatic) | Sans-serif (clean) | Editorial, luxury |
| Geometric sans | Humanist sans | Modern, friendly |
| Monospace | System sans | Technical, brutalist |
| Slab serif | Neutral sans | Bold, structured |
| Handwritten/display | Geometric sans | Playful, creative |

## Color & Theme

### Building a Palette

1. Start with one dominant color (the mood-setter)
2. Add 1-2 accent colors (for interaction, emphasis)
3. Define neutral scale (backgrounds, borders, text)
4. Add semantic colors (success, warning, error)
5. Store everything in CSS custom properties

```css
:root {
  --color-primary: #...;
  --color-accent: #...;
  --color-bg: #...;
  --color-surface: #...;
  --color-text: #...;
  --color-text-secondary: #...;
  --color-border: #...;
}
```

### Rules

- Dominant + accent, not evenly distributed
- WCAG AA contrast minimum (4.5:1 for text, 3:1 for large text)
- Dark vs. light: commit fully. Do not hedge.
- Test with real content, not lorem ipsum

## Motion & Animation

### CSS Transitions (Micro-interactions)

```css
.button {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

### CSS @keyframes (Ambient)

```css
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.floating-element { animation: float 3s ease-in-out infinite; }
```

### Scroll-Triggered (IntersectionObserver)

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
```

### Staggered Reveals

```css
.stagger-item { opacity: 0; transform: translateY(20px); transition: all 0.5s ease; }
.stagger-item.visible { opacity: 1; transform: translateY(0); }
.stagger-item:nth-child(1) { transition-delay: 0s; }
.stagger-item:nth-child(2) { transition-delay: 0.1s; }
.stagger-item:nth-child(3) { transition-delay: 0.2s; }
```

### Performance

- Animate only `transform` and `opacity` (GPU-composited)
- Avoid animating `width`, `height`, `margin`, `padding` (trigger layout)
- Use `will-change` sparingly and only on elements that will animate
- Prefer CSS over JS for simple animations
- Use `prefers-reduced-motion` media query for accessibility

## Spatial Composition

- Break out of the centered-content-column default
- Use asymmetry and grid-breaking elements intentionally
- Overlap elements with z-index for depth
- Generous negative space OR controlled density — commit to one
- CSS Grid for complex layouts, Flexbox for component alignment

## Code Quality

- Semantic HTML (nav, main, article, section, aside, footer)
- Accessible: ARIA labels, keyboard navigation, focus management
- Responsive: mobile-first or fluid, tested at 320-1440px
- Performance: lazy loading images, efficient selectors, minimal JS
- No external dependencies unless essential (CDN fonts are fine)

## Anti-Patterns

- Generic AI aesthetics (purple gradients everywhere, glassmorphism on everything)
- Cookie-cutter component libraries used without customization
- Predictable layouts (hero → 3-column → testimonials → CTA)
- "Clean and modern" as the entire design direction
- Overused fonts (Inter, Poppins for display)
- Decorative elements without purpose
- Rounded everything (a specific choice is fine, but default rounding is lazy)
- Dark mode with neon accents (overdone)

For typography pairings, color construction, animation library, and accessibility checklist, see [REFERENCE.md](REFERENCE.md).

## Brand Context (Optional)

If `brand-profile.json` exists in the working directory, read it before designing. Use colors (primary, secondary, background, text) for the design system, typography (heading and body fonts) for type selections, aesthetic (mood keywords, texture, negative space) for layout decisions, and imagery (style, composition) for hero sections and visual elements. This profile is produced by the `brand-dna` skill.
