---
name: frontend-design
description: Create distinctive, memorable user interfaces that avoid generic AI aesthetics. Use when designing UI/UX, planning visual direction, or building pages and layouts.
---

# Frontend Design Skill

Create distinctive, memorable user interfaces that avoid generic AI aesthetics.

## Pre-Implementation Planning

Before writing code, establish:

1. **Purpose & Audience** - What problem does this solve? Who uses it?
2. **Tone** - Choose a deliberate aesthetic direction:
   - Brutalist, maximalist, retro-futuristic, luxury, playful, editorial, organic, industrial
3. **Constraints** - Framework requirements, performance budgets, accessibility needs
4. **Memorable Element** - What's the ONE thing users will remember?

## Design Principles

### Typography
- **Avoid**: Inter, Roboto, Arial, system-ui (generic AI look)
- **Prefer**: Distinctive typefaces with character
- Pair display fonts with refined body options
- Size hierarchy should be dramatic, not subtle

### Color & Theme
- Use CSS variables for cohesive theming
- Dominant colors with sharp accents > evenly-distributed palettes
- Commit fully to color choices - timid palettes look generic
- Dark mode should be designed, not just inverted

### Motion & Animation
- Prioritize high-impact moments (page load, key interactions)
- One well-orchestrated entrance > scattered micro-interactions
- Staggered reveals create rhythm and hierarchy
- Quality over quantity

### Spatial Composition
- Employ asymmetry, overlap, diagonal flow
- Break grids intentionally for emphasis
- Generous negative space OR controlled density (pick one)
- Avoid centered-everything layouts

### Visual Details
- Gradient meshes, noise textures, geometric patterns
- Layered transparencies, dramatic shadows
- Custom cursors, grain overlays, decorative borders
- Details should reinforce the chosen aesthetic

## Anti-Patterns

- Generic fonts (Inter, Roboto, Arial on white backgrounds)
- Purple/blue gradients on white (classic AI startup look)
- Predictable card grids with rounded corners
- Cookie-cutter component libraries without customization
- Designs that could belong to any product

## Implementation Approach

```
1. Establish design tokens (colors, typography, spacing)
2. Build distinctive hero/header first (sets the tone)
3. Let the hero aesthetic inform component design
4. Add motion and micro-interactions last
5. Review: "Would I remember this UI tomorrow?"
```

## Framework Notes

This skill is framework-agnostic. Apply these principles whether using:
- React/Next.js with Tailwind
- Vue/Nuxt with CSS
- Svelte with styled-components
- Plain HTML/CSS

The goal is distinctive design, not specific implementation.

---

## Version
- v1.0.0 (2025-12-05): Added YAML frontmatter, initial documented version
