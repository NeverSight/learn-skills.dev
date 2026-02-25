---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use when building or refining web components, pages, or apps (HTML/CSS/JS/React) with bold aesthetics, purposeful layouts, motion, and accessibility. Avoid generic AI-looking output.
---

# Frontend Design

## Overview

Build memorable, functional interfaces with a clear aesthetic direction (no generic templates). Focus on bold typography, cohesive palettes, purposeful motion, semantic structure, and accessibility.

## Quick Start
- Collect intent: purpose, audience, platform constraints, framework, delivery format (HTML/React/Vue).
- Choose an aesthetic direction and signature move (stripe, glow, grain, magazine stack). See `references/aesthetic-playbook.md`.
- Define tokens: fonts, palette, shadows, radii, spacing scale. Load fonts early.
- Plan layout: hero + supporting sections, data/timeline rails, cards; pick grid system and motion plan.
- Build semantic markup, wire CSS variables, add motion with staggered reveals, then run accessibility and responsive checks.

## Workflow

### 1) Define intent and aesthetic
- Ask for: target users, tone (brutalist, editorial, neon, soft craft, industrial, etc.), content types (cards, forms, charts), performance constraints.
- Pick a single memorable gesture and stick to it. Avoid mixed-font chaos unless the style calls for it.
- If the user is vague, propose 2–3 aesthetic directions from `references/aesthetic-playbook.md` and confirm.

### 2) Plan structure and tokens
- Establish CSS variables for palette, shadows, radii, spacing, and motion curve. Keep accent count to 1–2.
- Choose font pairing (display + body, optional mono). Provide fallbacks after custom fonts.
- Map sections and micro-interactions. For vanilla builds, start from semantic HTML; for React, break into composable pieces (Hero, FeatureList, Timeline, CTA Rail).
- Reference `references/implementation-patterns.md` for layout, motion, accessibility, and responsive patterns.

### 3) Build and animate
- Markup: semantic headings, skip links, ARIA labels for interactive elements, descriptive alt text.
- Layout: prefer CSS Grid for macro and Flexbox for clusters. Break the grid deliberately (asymmetry, overlaps) while preserving readability.
- Styling: use custom backgrounds (gradient meshes, grain, hatch) to avoid flat color; design buttons and cards with intentional borders/shadows.
- Motion: orchestrate a few meaningful animations (page-load stagger, hover magnetic lift, scroll reveals). Guard with `prefers-reduced-motion`.
- Data-driven UI: define arrays of content (cards, metrics, steps) to keep components DRY and easy to restyle.

### 4) Polish and QA
- Responsive: collapse grids, maintain padding, ensure CTAs remain prominent on mobile, swap hover cues for focus/active styles.
- Accessibility: one `h1`, logical heading order, focus styles, contrast AA+, labeled inputs, `aria-live` where status changes.
- Performance: avoid heavy shadows on mobile, compress/limit assets, use font-display swap, prefer CSS animations over JS-heavy effects.

## References
- `references/aesthetic-playbook.md`: Pick strong aesthetic directions with fonts, colors, layout, and motion cues.
- `references/implementation-patterns.md`: HTML/React patterns, tokens, motion recipes, responsive and accessibility guidance.

## Assets
- `assets/vanilla-starter/`: Ready-to-run vanilla HTML/CSS/JS concept (avant studio theme) with gradients, grain, staggered reveals, skip link, and accessible structure. Copy and retheme by updating CSS variables, fonts, and content.
