---
name: material-design-3-icons
description: Applies Material Design 3 icon guidelines using Material Symbols — Google's variable font icon system. Use this when working with icons, Material Symbols, icon sizing, icon accessibility, or when the user asks to apply Material Design 3 icon guidelines.
license: Apache-2.0
---

# Material Design 3 Icons and Material Symbols

## Overview

This skill guides the implementation of Material Design 3 (M3) icons using Material Symbols — Google's variable font icon system that provides 2,500+ icons with dynamic customization through font variation axes.

**Keywords**: Material Design 3, M3, icons, Material Symbols, variable font icons, icon guidelines, icon accessibility, icon sizing, filled icons, outlined icons

## Core Principles

### Icon Philosophy

M3 icons are designed to:

1. **Communicate Clearly**: Icons should be instantly recognizable and universally understood
2. **Adapt Dynamically**: Variable font technology enables real-time customization
3. **Support Theming**: Icons adapt to M3 color and sizing systems
4. **Enhance Accessibility**: Icons supplement (never replace) text labels for critical actions
5. **Express Brand**: Icon weight, fill, and style can be tuned to match brand personality

## Material Symbols

### Three Icon Styles

Material Symbols are available in three styles, each with its own visual character:

| Style | Character | Use |
|-------|-----------|-----|
| Outlined | Clean, lightweight | Default for most interfaces |
| Rounded | Soft, friendly | Approachable, casual contexts |
| Sharp | Precise, geometric | Technical, professional contexts |

### Variable Font Axes

Material Symbols use four variable font axes for dynamic customization:

| Axis | Property | Range | Default | Effect |
|------|----------|-------|---------|--------|
| FILL | Fill | 0–1 | 0 | Outline (0) to filled (1) |
| wght | Weight | 100–700 | 400 | Stroke thickness |
| GRAD | Grade | -25–200 | 0 | Fine weight without size change |
| opsz | Optical Size | 20–48 | 24 | Stroke optimization for size |

### Implementation

#### Loading Material Symbols

```html
<!-- Via Google Fonts (recommended) -->
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

<!-- Or Rounded -->
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

<!-- Or Sharp -->
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

#### Basic Usage

```html
<span class="material-symbols-outlined">home</span>
<span class="material-symbols-outlined">search</span>
<span class="material-symbols-outlined">settings</span>
```

#### CSS Configuration

```css
/* Base icon styles */
.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-feature-settings: 'liga';
}
```

#### Customizing with Variable Font Axes

```css
/* Default icon (outlined, regular weight) */
.icon-default {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

/* Filled icon */
.icon-filled {
  font-variation-settings:
    'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

/* Bold icon */
.icon-bold {
  font-variation-settings:
    'FILL' 0,
    'wght' 700,
    'GRAD' 0,
    'opsz' 24;
}

/* Light icon */
.icon-light {
  font-variation-settings:
    'FILL' 0,
    'wght' 200,
    'GRAD' 0,
    'opsz' 24;
}

/* Small icon (optimized for 20dp) */
.icon-small {
  font-size: 20px;
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 20;
}

/* Large icon (optimized for 48dp) */
.icon-large {
  font-size: 48px;
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 48;
}
```

## Icon Sizing

### Standard Sizes

M3 defines standard icon sizes that pair with the optical size axis:

| Size | Use | Optical Size (opsz) |
|------|-----|---------------------|
| 20dp | Dense layouts, small controls | 20 |
| 24dp | Default, most components | 24 |
| 40dp | Large buttons, featured actions | 40 |
| 48dp | Hero icons, empty states | 48 |

### Sizing with Components

```css
/* Icon in a button */
.md3-button .material-symbols-outlined {
  font-size: 18px;
  font-variation-settings: 'opsz' 20;
}

/* Icon in navigation */
.md3-nav-item .material-symbols-outlined {
  font-size: 24px;
  font-variation-settings: 'opsz' 24;
}

/* Icon in FAB */
.md3-fab .material-symbols-outlined {
  font-size: 24px;
  font-variation-settings: 'opsz' 24;
}

/* Icon in large FAB */
.md3-fab-large .material-symbols-outlined {
  font-size: 36px;
  font-variation-settings: 'opsz' 40;
}
```

## Icon Color

Icons use M3 color tokens and inherit color from their parent:

```css
/* Default icon color */
.icon-default {
  color: var(--md-sys-color-on-surface);
}

/* Icon on primary background */
.icon-on-primary {
  color: var(--md-sys-color-on-primary);
}

/* Icon as interactive element */
.icon-interactive {
  color: var(--md-sys-color-on-surface-variant);
}

.icon-interactive:hover {
  color: var(--md-sys-color-on-surface);
}

/* Active/selected icon */
.icon-active {
  color: var(--md-sys-color-primary);
  font-variation-settings: 'FILL' 1;
}

/* Disabled icon */
.icon-disabled {
  color: var(--md-sys-color-on-surface);
  opacity: 0.38;
}

/* Error icon */
.icon-error {
  color: var(--md-sys-color-error);
}
```

## Fill Transitions

Use fill to indicate selection state — transitioning from outline to filled:

```css
/* Toggle fill on selection */
.icon-toggle {
  font-variation-settings: 'FILL' 0;
  transition: font-variation-settings 200ms var(--md-sys-motion-easing-standard);
}

.icon-toggle[aria-selected="true"],
.icon-toggle.selected {
  font-variation-settings: 'FILL' 1;
}
```

### Common Fill Patterns

| Component | Unselected | Selected |
|-----------|-----------|----------|
| Navigation icon | FILL 0 | FILL 1 |
| Favorite/like | FILL 0 | FILL 1, color: error |
| Checkbox icon | FILL 0 | FILL 1, color: primary |
| Bookmark | FILL 0 | FILL 1 |
| Tab icon | FILL 0 | FILL 1, color: primary |

## Grade for Emphasis

Grade adjusts weight without changing icon size — useful for emphasis without layout shift:

```css
/* Low emphasis icon */
.icon-low-emphasis {
  font-variation-settings: 'GRAD' -25;
}

/* High emphasis icon (dark text on light bg) */
.icon-high-emphasis {
  font-variation-settings: 'GRAD' 200;
}

/* Adjust grade for dark mode */
[data-theme="dark"] .material-symbols-outlined {
  font-variation-settings: 'GRAD' -25;
}
```

## Accessibility

### Requirements

1. **Decorative icons**: Use `aria-hidden="true"` when icons accompany text
2. **Standalone icons**: Provide `aria-label` or `title` when icons are used alone
3. **Interactive icons**: Wrap in `<button>` with accessible name
4. **Touch targets**: Ensure 48×48dp minimum touch target regardless of visual icon size

### Implementation

```html
<!-- Decorative icon (with text label) -->
<button>
  <span class="material-symbols-outlined" aria-hidden="true">delete</span>
  Delete
</button>

<!-- Standalone icon button (needs label) -->
<button aria-label="Delete item">
  <span class="material-symbols-outlined" aria-hidden="true">delete</span>
</button>

<!-- Informational icon (supplementary) -->
<span class="material-symbols-outlined" aria-hidden="true">info</span>
<span>More details available</span>
```

### Touch Target for Icon Buttons

```css
.md3-icon-button {
  width: 48px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--md-sys-shape-corner-full);
  border: none;
  background: transparent;
  cursor: pointer;
  position: relative;
}

/* The icon itself can be smaller than the touch target */
.md3-icon-button .material-symbols-outlined {
  font-size: 24px;
}
```

## Best Practices

### Do's

1. ✅ Use Material Symbols for consistent M3 icon styling
2. ✅ Match icon weight to surrounding typography weight
3. ✅ Use optical size (opsz) appropriate to rendered icon size
4. ✅ Use fill transitions to indicate selection state
5. ✅ Provide accessible labels for standalone interactive icons
6. ✅ Use `aria-hidden="true"` for decorative icons that accompany text
7. ✅ Adjust grade for dark mode (slightly negative for better contrast)
8. ✅ Use M3 color tokens for icon colors

### Don'ts

1. ❌ Don't use icons without text labels for primary navigation or critical actions
2. ❌ Don't mix Material Symbols styles (outlined, rounded, sharp) in the same interface
3. ❌ Don't resize icons with CSS `transform: scale()` — use font-size and opsz instead
4. ❌ Don't use inconsistent weights across an interface
5. ❌ Don't rely solely on icon color to communicate state
6. ❌ Don't use icons smaller than 20dp
7. ❌ Don't ignore touch target requirements for icon buttons

## Checklist for Icon Implementation

When implementing M3 icons, ensure:

- [ ] Material Symbols font is loaded (outlined, rounded, or sharp — pick one)
- [ ] Variable font axes are configured (FILL, wght, GRAD, opsz)
- [ ] Optical size matches rendered size (20dp → opsz 20, 24dp → opsz 24, etc.)
- [ ] Icon weight matches surrounding text weight
- [ ] Fill transitions indicate selection state in navigation and toggles
- [ ] Grade is adjusted for dark mode
- [ ] All standalone icons have accessible labels (aria-label)
- [ ] Decorative icons use aria-hidden="true"
- [ ] Interactive icons are wrapped in proper interactive elements (button, a)
- [ ] Touch targets are 48×48dp minimum for icon buttons
- [ ] Icons use M3 color tokens (on-surface, primary, error, etc.)
- [ ] Only one icon style is used throughout the interface
- [ ] Icons are supplemented with text labels where clarity demands it

## Resources

- Material Symbols: https://fonts.google.com/icons
- M3 icons overview: https://m3.material.io/styles/icons/overview
