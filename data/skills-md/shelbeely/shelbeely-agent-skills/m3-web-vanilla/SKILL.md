---
name: m3-web-vanilla
description: Implement Material Design 3 using only vanilla CSS custom properties and semantic classes. Zero dependencies. Use this when building M3-styled static sites, simple web apps, or when you need full control over every design token without a framework.
license: Apache-2.0
---

# Material Design 3 — Vanilla CSS

## Overview

Implement Material Design 3 using only CSS custom properties and semantic classes. No framework dependency. This is the canonical approach used by all other M3 skills in this repository.

**Keywords**: Material Design 3, M3, vanilla CSS, CSS custom properties, design tokens, Beer CSS, CSS framework, no framework

## When to Use

- Static sites or simple web apps
- Any project where you want zero dependencies
- When you need full control over every design token
- As a reference implementation for other frameworks
- Rapid prototyping without build tools

## Setup

Define M3 tokens as CSS custom properties:

```css
/* m3-tokens.css */
:root {
  /* Color tokens */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-on-surface: #1D1B20;
  --md-sys-color-surface-variant: #E7E0EC;
  --md-sys-color-on-surface-variant: #49454F;
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;

  /* Shape tokens */
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-full: 9999px;

  /* Typography tokens */
  --md-sys-typescale-label-large-font: 'Roboto', sans-serif;
  --md-sys-typescale-label-large-size: 14px;
  --md-sys-typescale-label-large-weight: 500;
  --md-sys-typescale-label-large-tracking: 0.1px;
  --md-sys-typescale-body-medium-font: 'Roboto', sans-serif;
  --md-sys-typescale-body-medium-size: 14px;
  --md-sys-typescale-body-medium-weight: 400;
  --md-sys-typescale-title-medium-font: 'Roboto', sans-serif;
  --md-sys-typescale-title-medium-size: 16px;
  --md-sys-typescale-title-medium-weight: 500;
}

/* Dark theme */
[data-theme="dark"] {
  --md-sys-color-primary: #D0BCFF;
  --md-sys-color-on-primary: #381E72;
  --md-sys-color-surface: #141218;
  --md-sys-color-on-surface: #E6E0E9;
  --md-sys-color-surface-variant: #49454F;
  --md-sys-color-on-surface-variant: #CAC4D0;
  --md-sys-color-outline: #938F99;
}
```

## Component Examples

### Filled Button

```css
.md3-button-filled {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  padding: 10px 24px;
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  letter-spacing: var(--md-sys-typescale-label-large-tracking);
  cursor: pointer;
  min-height: 40px;
  position: relative;
  overflow: hidden;
}

.md3-button-filled:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--md-sys-color-on-primary);
  opacity: 0.08;
}

.md3-button-filled:disabled {
  background: color-mix(in srgb, var(--md-sys-color-on-surface) 12%, transparent);
  color: color-mix(in srgb, var(--md-sys-color-on-surface) 38%, transparent);
  cursor: default;
}
```

### Card

```css
.md3-card-elevated {
  background: var(--md-sys-color-surface);
  border-radius: var(--md-sys-shape-corner-medium);
  padding: 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15);
}

.md3-card-filled {
  background: var(--md-sys-color-surface-variant);
  border-radius: var(--md-sys-shape-corner-medium);
  padding: 16px;
}

.md3-card-outlined {
  background: var(--md-sys-color-surface);
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-medium);
  padding: 16px;
}
```

### Text Field

```css
.md3-text-field-outlined {
  position: relative;
  border: 1px solid var(--md-sys-color-outline);
  border-radius: var(--md-sys-shape-corner-extra-small);
  padding: 16px;
  font-family: var(--md-sys-typescale-body-medium-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  background: transparent;
  color: var(--md-sys-color-on-surface);
}

.md3-text-field-outlined:focus {
  border-color: var(--md-sys-color-primary);
  border-width: 2px;
  outline: none;
}
```

```html
<button class="md3-button-filled">Click me</button>

<div class="md3-card-elevated">
  <h3 style="font-family: var(--md-sys-typescale-title-medium-font)">Title</h3>
  <p style="font-family: var(--md-sys-typescale-body-medium-font)">Content</p>
</div>

<input class="md3-text-field-outlined" placeholder="Email" />
```

## CSS-only Frameworks

If you want M3 styling without writing all the CSS yourself:

- **Beer CSS** (`beercss`): First CSS framework fully based on M3. Zero dependencies, semantic HTML, very small bundle. https://www.beercss.com/
- **Material Design Light**: Lightweight SCSS framework compiled to plain CSS. https://github.com/mdlightdev/material-design-light
- **GMX.css**: Minimal-JS M3 CSS implementation with predefined color schemes. https://www.cssscript.com/material-design-framework-gmx/

## Checklist

- [ ] All M3 color tokens defined as CSS custom properties
- [ ] Dark theme variant using `[data-theme="dark"]` or `prefers-color-scheme`
- [ ] Shape tokens use the M3 shape scale
- [ ] Typography tokens follow the M3 type scale
- [ ] Components use semantic token names (not hard-coded hex)
- [ ] Interaction states (hover, focus, pressed, disabled) implemented
- [ ] Touch targets meet 48×48dp minimum
- [ ] Focus indicators visible with adequate contrast

## Resources

- `m3-tokens.css` — Complete M3 token foundation (color, shape, typography, motion, spacing, elevation) included in this skill's directory. Copy into your project as a starting point.
- `material-theme-builder` skill — Generate a custom token set from any source color.
- Material Theme Builder: https://material-foundation.github.io/material-theme-builder/
- M3 Design Tokens: https://m3.material.io/foundations/design-tokens/overview
- Beer CSS: https://www.beercss.com/
