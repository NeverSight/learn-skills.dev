---
name: color-palette-library
description: "500+ ready-made color palettes with contrast scores, plus OKLCH palette generation, dark-mode luminance mapping, semantic color architecture, and data-viz scales. Use when picking or generating a specific palette. For color theory and hierarchy craft, use ui-visual-design-system."
---

# Color Palette Library — 500+ Curated Palettes

## Mental model

Colour decisions fail in a predictable order: people pick hues first, discover
the contrast is illegal, patch the lightness, and end up with a palette whose
steps are uneven and whose dark mode is an inversion.

Work the other way round. Fix the **lightness ramp** first — it is what makes a
scale usable — then set chroma, then choose hue last, because hue is the only
one of the three that is purely taste.

- **OKLCH, not HSL.** In HSL, two colours at the same `L` can differ in
  perceived brightness by a factor of three. OKLCH lightness is perceptual, so a
  ramp built in it looks even without hand-correction.
- **Chroma peaks in the middle.** Hold hue, run lightness 0.98 down to 0.18, and
  let chroma rise toward the mid-steps and fall at both ends. Flat chroma makes
  the light end muddy and the dark end neon.
- **Semantic names alias primitives.** Components consume `--color-bg-subtle`,
  never `--color-neutral-100`. This is what makes a theme swap one file.
- **Dark mode is not inversion.** Reduce luminance, desaturate, and raise
  elevation with lightness rather than shadow.

## Constants

Semantic token *names* — every reference file writes against these. The values
live in the palette catalogs.

```css
:root {
  --color-bg-base; --color-bg-subtle; --color-bg-raised; --color-bg-overlay;
  --color-text-strong; --color-text-default; --color-text-muted; --color-text-inverse;
  --color-border-subtle; --color-border-default; --color-border-strong;
  --color-brand-subtle; --color-brand-default; --color-brand-strong;
  --color-success; --color-warning; --color-error; --color-info;
}
```

Scale generation, for reading any catalog entry: hold hue, run lightness from
`0.98` to `0.18` across steps 50-950, peak chroma at steps 400-600.

## Index

| Need | Reference |
|---|---|
| Generate a scale from one brand colour | `accessible-palette-generator.md` |
| Check APCA / WCAG contrast properly | `accessible-palette-generator.md` |
| Colourblind-safe categorical series | `accessible-palette-generator.md` |
| A ready palette for fintech, healthcare, SaaS, e-commerce, social | `industry-palette-catalog.md` |
| Colour psychology by industry | `industry-palette-catalog.md` |
| Monochromatic, duotone, neutral+accent, jewel, pastel, neon | `color-combination-recipes.md` |
| Gradient recipes | `color-combination-recipes.md` |
| Map an existing light palette to dark | `dark-mode-color-science.md` |
| Elevation by lightness rather than shadow | `dark-mode-color-science.md` |
| How Stripe, Linear, Vercel, Notion, Figma, Shopify, GitHub do it | `brand-color-systems.md` |
| Extract a palette from an existing brand | `brand-color-systems.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/industry-palette-catalog.md` | 10 palettes x 10 industries | 928 |
| `references/color-combination-recipes.md` | 12 harmony categories + gradients | 889 |
| `references/brand-color-systems.md` | 20 real brands deconstructed | 786 |
| `references/dark-mode-color-science.md` | inversion is wrong; what to do instead | 685 |
| `references/accessible-palette-generator.md` | APCA, OKLCH generation, colourblind | 586 |

## What every reference file contains

1. The palette or recipe as OKLCH values, with hex fallbacks
2. Contrast scores for every foreground/background pair that matters
3. The semantic mapping — which primitive fills which semantic slot
4. The dark-mode counterpart, not just the light values
5. Where the combination fails, and what it should not be used for

## Routing

For **generating a palette** — the APCA contrast algorithm, step-by-step OKLCH
generation, and colorblind-safe categorical scales: read
`references/accessible-palette-generator.md`.

For **a ready-made palette by industry** — ten each for fintech, healthcare,
SaaS, e-commerce, social and more: read `references/industry-palette-catalog.md`.

For **combination theory** — monochromatic, duotone, neutral-plus-accent, and
the rest of the twelve categories including gradients: read
`references/color-combination-recipes.md`.

For **dark mode** — why it is not inversion, luminance reduction, desaturation
rules, and elevation-by-lightness: read `references/dark-mode-color-science.md`.

For **how real products do it** — Stripe, Linear, Vercel, Notion, Figma, Shopify
and GitHub deconstructed: read `references/brand-color-systems.md`.

For **odds and ends** — the patterns that had no home in the files above when this skill was converted to a router: read `references/color-supplementary.md`.

## Cross-References
- design-token-presets — complete token system templates by industry
- visual-design-mastery — color scoring on the 10-dimension Awwwards scale
- sector-style-intelligence — industry-specific color direction
- accessibility-inclusive-design — WCAG 2.2 + APCA compliance testing
- data-visualization-mastery — dataviz palette integration
- platform-visual-standards — iOS 26 Liquid Glass and M3 Expressive color details
- shadow-elevation-density — elevation-driven color in dark mode
- typography-pairing-recipes — text color and contrast pairing with type
