---
name: shadow-elevation-density
description: "Elevation, shadow, depth, and density systems: shadow scales, elevation hierarchy, glassmorphism, blur effects, border-radius systems, and compact, comfortable, and spacious density modes with production CSS. Use when surfaces look flat or float wrongly, or when tuning information density."
---

# Shadow, Elevation and Density

## Mental model

Elevation is a lie the interface tells consistently. It works only when every
element agrees on where the light is and how far off the surface it sits.

Three rules carry most of the weight:

- **One light source.** Top-center, slightly left in LTR. Every element at the
  same elevation casts the same direction of shadow. Two light sources destroy
  spatial coherence faster than any other single mistake.
- **Layer, don't darken.** A realistic shadow is two or three stacked shadows —
  a tight dark one for contact, a wide soft one for ambience. A single large
  blurred shadow reads as a sticker, not a raised surface.
- **Never pure black.** `oklch(0 0 0 / a)` at low alpha, or better, a shadow
  tinted toward the surface's own hue. Pure black at high alpha is the single
  most common reason a UI looks cheap.

Density is the same discipline applied to space rather than depth: pick one of
three modes and hold it, because a screen that mixes compact and comfortable
reads as unfinished rather than flexible.

Shadow anatomy, for reading the values below: `x-offset y-offset blur spread
color`. Y-offset places it, blur softens it, spread tightens or expands it.
Higher elevation means larger y-offset, larger blur, lower alpha.

## Constants

Every reference file in this skill writes against these tokens. They must be in
context for the recipes to be usable.

```css
:root {
  --shadow-0: none;
  --shadow-1: 0 1px 2px oklch(0 0 0 / 0.06), 0 1px 3px oklch(0 0 0 / 0.10);
  --shadow-2: 0 2px 4px oklch(0 0 0 / 0.04), 0 4px 8px oklch(0 0 0 / 0.06), 0 12px 24px oklch(0 0 0 / 0.06);
  --shadow-3: 0 4px 8px oklch(0 0 0 / 0.04), 0 8px 16px oklch(0 0 0 / 0.06), 0 20px 40px oklch(0 0 0 / 0.10);
  --shadow-4: 0 8px 16px oklch(0 0 0 / 0.06), 0 16px 32px oklch(0 0 0 / 0.08), 0 32px 64px oklch(0 0 0 / 0.12);

  --z-base:           0;
  --z-raised:         1;
  --z-dropdown:       100;
  --z-sticky:         200;
  --z-fixed:          300;
  --z-drawer:         400;
  --z-modal-backdrop: 500;
  --z-modal:          510;
  --z-popover:        600;
  --z-toast:          700;
  --z-tooltip:        800;
  --z-drag:           900;
  --z-max:            9999;
}
```

The z-index scale uses 100-step intervals so sub-layers fit between named
levels without renumbering. `--z-max` is for debug overlays only; reaching for
it in product code means a stacking context is wrong somewhere above.

## Index

| Concern | Level / mode | Reference |
|---|---|---|
| Resting surface, card at rest | `--shadow-1` | `shadow-system-recipes.md` |
| Raised card, hover state | `--shadow-2` | `shadow-system-recipes.md` |
| Dropdown, popover, sticky header | `--shadow-3` | `shadow-system-recipes.md` |
| Modal, drawer, command palette | `--shadow-4` | `shadow-system-recipes.md` |
| Minimal system (Linear, Vercel) | — | `shadow-system-recipes.md` |
| Layered system (Stripe) | — | `shadow-system-recipes.md` |
| Material system (Google) | — | `shadow-system-recipes.md` |
| Brand-tinted / colored shadows | — | `shadow-system-recipes.md` |
| Dark-mode ambient glow | — | `shadow-system-recipes.md` |
| Neumorphic | — | `shadow-system-recipes.md` |
| Z-index conflicts, stacking contexts | — | `elevation-hierarchy.md` |
| Surface layer architecture | — | `elevation-hierarchy.md` |
| Compact / comfortable / spacious | — | `density-modes.md` |
| Component-specific density rules | — | `density-modes.md` |
| Radius scale, nested radius rule | — | `border-radius-systems.md` |
| Sharp / rounded / pill systems | — | `border-radius-systems.md` |
| Frosted glass, acrylic, blur | — | `glassmorphism-effects.md` |
| Animating elevation on hover | — | `shadow-animation.md` |
| Depth without shadow; materials | — | `depth-and-materials.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/shadow-system-recipes.md` | 11 complete shadow systems | 1016 |
| `references/glassmorphism-effects.md` | 10 glass and blur recipes | 1101 |
| `references/border-radius-systems.md` | radius scale, nested rule, 5 systems | 934 |
| `references/density-modes.md` | full token specs for 3 modes | 923 |
| `references/elevation-hierarchy.md` | z-index, stacking, surfaces | 608 |
| `references/depth-and-materials.md` | depth cues, surface materials | 145 |
| `references/shadow-animation.md` | transitioning elevation | 86 |

## What every reference file contains

1. The philosophy — what the treatment is for and when it is wrong
2. Complete CSS custom properties, ready to paste
3. Named variants with the condition that selects each
4. Light and dark values, not light only
5. Component-specific application notes
6. Performance cost, where the technique has one
7. Anti-patterns specific to that treatment

## Routing

For **a shadow system** — minimal (Linear/Vercel), layered (Stripe), Material,
colored/brand-tinted, dark-mode ambient glow, and neumorphic, each as complete
CSS: read `references/shadow-system-recipes.md`.

For **stacking and z-index** — the scale, stacking-context management, surface
layer architecture, elevation-to-shadow mapping, and the common z-index bugs:
read `references/elevation-hierarchy.md`.

For **density** — full token specifications for compact, comfortable and
spacious, the side-by-side comparison, implementation strategies and
component-specific rules: read `references/density-modes.md`.

For **corner radius** — the scale, the nested radius rule, component
conventions, and five named systems from sharp/corporate to fully rounded: read
`references/border-radius-systems.md`.

For **glass and blur** — glassmorphism fundamentals and ten recipes including
frosted glass (Apple) and acrylic (Windows): read
`references/glassmorphism-effects.md`.

For **animating elevation** — what to transition, what it costs, and the
compositor-friendly alternatives to animating `box-shadow` directly: read
`references/shadow-animation.md`.

For **depth without shadow** — overlap, scale, blur, parallax, borders, and the
surface material treatments: read `references/depth-and-materials.md`.

## Performance

`box-shadow` is painted, not composited. Animating it forces repaint on every
frame. Transition `opacity` on a stacked pseudo-element instead, or accept the
cost only on small elements. `backdrop-filter` is expensive on large surfaces
and on low-end Android; always ship a solid-color fallback behind an
`@supports` query.

## Cross-References

- `ui-visual-design-system` — where elevation sits in the wider visual language
- `platform-visual-standards` — iOS and Material 3 have their own elevation models
- `animation-recipe-library` — the easing tokens shadow transitions use
- `design-systems-architecture` — how these tokens fit the three-tier model
- `figma-design-tool-workflows` — setting these up as Figma effect styles
