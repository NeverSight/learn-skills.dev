---
name: typography-pairing-recipes
description: "100+ font pairing recipes and type scale systems covering Google Fonts, system stacks, variable fonts, fluid clamp() scales, and platform-native type, each with display, body, and mono picks at exact weights and line-heights. Use when choosing fonts or building a type scale."
---

# Typography Pairing Recipes — 100+ Font Combinations

## Pairing Principles

Great typography pairings follow two rules:
1. **Contrast**: The two fonts should be visually distinct (serif + sans-serif, geometric + humanist)
2. **Complement**: Despite contrast, they should share a quality (similar x-height, era, mood)

### Font Classification Quick Reference
- **Geometric sans**: Clean, circular forms (Inter, Geist, Futura, Montserrat)
- **Humanist sans**: Organic, calligraphic influence (Source Sans, Fira Sans, Open Sans)
- **Neo-grotesque sans**: Neutral, uniform (Helvetica, Roboto, SF Pro)
- **Old-style serif**: Classic, calligraphic (Garamond, Libre Baskerville, Newsreader)
- **Transitional serif**: Refined, higher contrast (Georgia, Charter, Merriweather)
- **Modern serif**: High contrast, elegant (Playfair Display, Didot)
- **Slab serif**: Strong, sturdy (Roboto Slab, Zilla Slab)
- **Monospace**: Fixed-width, technical (JetBrains Mono, Fira Code, SF Mono)
- **Display**: Decorative, large sizes only (Fraunces, Instrument Serif)

## Top 20 Pairings (Curated)

### Minimal/Modern
1. **Inter + Inter** — Monofamily. Weight contrast creates hierarchy. The safest choice.
2. **Geist Sans + Geist Mono** — Vercel's stack. Clean, technical, modern.
3. **Inter + JetBrains Mono** — Standard modern pairing. Works for everything.
4. **Plus Jakarta Sans + JetBrains Mono** — Slightly warmer than Inter.
5. **DM Sans + DM Mono** — Geometric, clean, cohesive family.

### Premium/Editorial
6. **Instrument Serif + Instrument Sans** — Matched pair. Editorial elegance.
7. **Playfair Display + Source Sans 3** — Classic luxury. Serif headlines, clean body.
8. **Fraunces + Commissioner** — Variable fonts, expressive range.
9. **Newsreader + Inter** — Editorial headlines, neutral body.
10. **Cormorant Garamond + Montserrat** — High contrast elegance.

### Friendly/Warm
11. **Nunito + Nunito Sans** — Rounded, approachable, matched pair.
12. **Poppins + Inter** — Geometric warmth meets neutral clarity.
13. **Quicksand + Roboto** — Playful headlines, readable body.
14. **Outfit + Inter** — Modern rounded geometric.
15. **Sora + Inter** — Japanese-inspired geometric.

### Corporate/Enterprise
16. **IBM Plex Sans + IBM Plex Mono** — Corporate precision. Full family.
17. **Noto Sans + Noto Serif** — Google's universal family. All scripts supported.
18. **Source Sans 3 + Source Serif 4** — Adobe's workhorse pair.
19. **Roboto + Roboto Mono** — Android ecosystem standard.
20. **SF Pro + SF Mono** — Apple ecosystem (system fonts).

## Type Scale Recipes

### Minimal App Scale (6 sizes)
```css
--text-sm: 0.875rem;    /* 14px — captions, helper text */
--text-base: 1rem;      /* 16px — body text */
--text-lg: 1.125rem;    /* 18px — large body, card titles */
--text-xl: 1.25rem;     /* 20px — section headings */
--text-2xl: 1.5rem;     /* 24px — page headings */
--text-3xl: 1.875rem;   /* 30px — hero subheading */
```

### Marketing Page Scale (9 sizes)
```css
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
--text-5xl: 3rem;       /* 48px */
--text-6xl: 3.75rem;    /* 60px — hero headline */
```

### Fluid Type Scale
```css
--text-base: clamp(1rem, 0.5rem + 0.75vw, 1.125rem);
--text-lg: clamp(1.125rem, 0.75rem + 1vw, 1.25rem);
--text-xl: clamp(1.25rem, 0.5rem + 2vw, 1.5rem);
--text-2xl: clamp(1.5rem, 0.5rem + 2.5vw, 2.25rem);
--text-3xl: clamp(1.875rem, 0.5rem + 3.5vw, 3rem);
--text-display: clamp(2.25rem, 0.5rem + 5vw, 4.5rem);
```

## Line-Height Rules

| Size | Line-Height | Use |
|------|------------|-----|
| 12-14px | 1.5-1.6 | Small text, captions |
| 16-18px | 1.5 | Body text (golden standard) |
| 20-24px | 1.3-1.4 | Subheadings |
| 30-48px | 1.1-1.2 | Headings |
| 48px+ | 1.0-1.1 | Display/hero text |

**Rule**: As size increases, line-height decreases. Large text needs tighter leading.

## Letter-Spacing Rules
- **Body text**: 0 (default tracking)
- **Small text (< 14px)**: +0.01-0.02em (slightly open for readability)
- **Headings (> 24px)**: -0.01 to -0.02em (tighten for visual density)
- **Display (> 48px)**: -0.02 to -0.04em (tight for impact)
- **ALL CAPS labels**: +0.05 to +0.1em (open for legibility)
- **Monospace**: 0 (fixed-width handles spacing)

## Routing

For **choosing a pairing** — 105 pairings across seven categories
(minimal/modern, premium/editorial, friendly/warm, corporate/enterprise,
creative/expressive, monospace, serif-only) plus the decision matrix: read
`references/font-pairing-catalog.md`.

For **building the scale** — type scale theory, complete scale recipes,
line-height by size, letter-spacing adjustments, measure, and responsive scaling
strategies: read `references/type-scale-systems.md`.

For **shipping the fonts** — system stacks per platform, web-safe fallback
chains, variable font technology, loading strategies, performance, and 2025
format support: read `references/platform-font-stacks.md`.

## Cross-References
- **ui-visual-design-system** — Typography system theory
- **visual-design-mastery** — Typography scoring and mastery
- **design-token-presets** — Typography tokens in presets
- **platform-visual-standards** — Platform-specific font stacks
