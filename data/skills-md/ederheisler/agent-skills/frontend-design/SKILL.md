---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
metadata:
  author: anthropic
  version: "1.0"
---

# Frontend Design

> **Note**: This skill is based on [Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design), enhanced with progressive disclosure and extensive reference materials.

Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Core Workflow

### 1. Understand Context

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

### 2. Design Thinking

Before coding, understand context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme aesthetic direction (see [references/aesthetics.md](references/aesthetics.md) for full list):
  - Brutally minimal
  - Maximalist chaos
  - Retro-futuristic
  - Organic/natural
  - Luxury/refined
  - Playful/toy-like
  - Editorial/magazine
  - Brutalist/raw
  - Art deco/geometric
  - Soft/pastel
  - Industrial/utilitarian
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

### 3. Implement with Excellence

Create working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Key Design Elements

Focus on these areas (details in [references/aesthetics.md](references/aesthetics.md)):

### Typography

Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics. Pair a distinctive display font with a refined body font.

### Color & Theme

Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Motion

Use animations for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

### Spatial Composition

Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details

Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

## What to Avoid

NEVER use generic AI-generated aesthetics:

- ❌ Overused font families (Inter, Roboto, Arial, system fonts)
- ❌ Cliched color schemes (particularly purple gradients on white backgrounds)
- ❌ Predictable layouts and component patterns
- ❌ Cookie-cutter design that lacks context-specific character

See [references/anti-patterns.md](references/anti-patterns.md) for detailed examples of what not to do.

## Implementation Complexity

**Match implementation complexity to the aesthetic vision:**

- **Maximalist designs** need elaborate code with extensive animations and effects
- **Minimalist or refined designs** need restraint, precision, and careful attention to spacing, typography, and subtle details

Elegance comes from executing the vision well, regardless of direction.

## Design Variation

Interpret creatively and make unexpected choices that feel genuinely designed for the context:

- No design should be the same
- Vary between light and dark themes, different fonts, different aesthetics
- NEVER converge on common choices (Space Grotesk, for example) across generations

## Reference Documentation

- [references/aesthetics.md](references/aesthetics.md) - Comprehensive aesthetic directions with color palettes, typography, layouts, and implementation details
- [references/examples.md](references/examples.md) - Real-world examples across aesthetic directions with complete code
- [references/anti-patterns.md](references/anti-patterns.md) - Generic patterns to avoid with transformation examples

## Remember

The agent is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
