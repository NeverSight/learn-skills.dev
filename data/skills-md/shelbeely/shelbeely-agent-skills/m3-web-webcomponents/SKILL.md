---
name: m3-web-webcomponents
description: Implement Material Design 3 using Google's official @material/web library — Lit-based web components. Framework-agnostic, works with any framework that supports Custom Elements. Use this when you want the official M3 implementation or need cross-framework components.
license: Apache-2.0
---

# Material Design 3 — Web Components (`@material/web`)

## Overview

Google's official M3 web component library. Framework-agnostic — works with any framework that supports Custom Elements. Built on Lit for small bundle size and interoperability.

**Keywords**: Material Design 3, M3, web components, @material/web, Lit, custom elements, material-web, Google official

## When to Use

- When you want Google's official M3 implementation
- Need cross-framework components
- Want standardized web components
- Projects that value stability over cutting-edge features

**Status**: Maintenance mode — stable but not receiving major new features.

## Install

```bash
npm install @material/web
```

## Setup

Import components individually for tree-shaking:

```html
<script type="module">
  import '@material/web/button/filled-button.js';
  import '@material/web/button/outlined-button.js';
  import '@material/web/button/text-button.js';
  import '@material/web/textfield/outlined-text-field.js';
  import '@material/web/textfield/filled-text-field.js';
  import '@material/web/checkbox/checkbox.js';
  import '@material/web/radio/radio.js';
  import '@material/web/switch/switch.js';
  import '@material/web/icon/icon.js';
  import '@material/web/fab/fab.js';
  import '@material/web/dialog/dialog.js';
  import '@material/web/menu/menu.js';
  import '@material/web/tabs/tabs.js';
  import '@material/web/tabs/primary-tab.js';
  import '@material/web/chips/chip-set.js';
  import '@material/web/chips/filter-chip.js';
  import '@material/web/progress/linear-progress.js';
  import '@material/web/progress/circular-progress.js';
  import '@material/web/select/outlined-select.js';
  import '@material/web/slider/slider.js';
  import '@material/web/list/list.js';
  import '@material/web/list/list-item.js';
  import '@material/web/navigationbar/navigation-bar.js';
  import '@material/web/navigationtab/navigation-tab.js';
</script>
```

## Theming

Theme via CSS custom properties:

```css
:root {
  /* Color tokens */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-secondary: #625B71;
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-error: #B3261E;
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-on-surface: #1D1B20;

  /* Typography tokens */
  --md-ref-typeface-brand: 'Roboto';
  --md-ref-typeface-plain: 'Roboto';

  /* Shape tokens */
  --md-sys-shape-corner-full: 9999px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-small: 8px;
}
```

## Component Examples

### Buttons

```html
<md-filled-button>Filled</md-filled-button>
<md-outlined-button>Outlined</md-outlined-button>
<md-text-button>Text</md-text-button>
<md-filled-tonal-button>Tonal</md-filled-tonal-button>
<md-elevated-button>Elevated</md-elevated-button>
```

### Text Fields

```html
<md-outlined-text-field label="Email" type="email"></md-outlined-text-field>
<md-filled-text-field label="Name"></md-filled-text-field>
```

### Navigation

```html
<md-navigation-bar>
  <md-navigation-tab label="Home">
    <md-icon slot="active-icon">home</md-icon>
    <md-icon slot="inactive-icon">home</md-icon>
  </md-navigation-tab>
  <md-navigation-tab label="Search">
    <md-icon slot="active-icon">search</md-icon>
    <md-icon slot="inactive-icon">search</md-icon>
  </md-navigation-tab>
</md-navigation-bar>
```

### Other Components

```html
<md-checkbox></md-checkbox>
<md-switch></md-switch>
<md-slider></md-slider>

<md-fab label="Add">
  <md-icon slot="icon">add</md-icon>
</md-fab>

<md-linear-progress indeterminate></md-linear-progress>
<md-circular-progress indeterminate></md-circular-progress>

<md-chip-set>
  <md-filter-chip label="Option 1"></md-filter-chip>
  <md-filter-chip label="Option 2"></md-filter-chip>
</md-chip-set>
```

## Using with Other Frameworks

`@material/web` can be used inside React, Vue, Svelte, and Angular since web components work in any framework. See the framework-specific M3 skills for details on integration patterns.

## Checklist

- [ ] Import only the components you need (tree-shaking)
- [ ] Apply M3 color tokens via CSS custom properties
- [ ] Configure typography typeface tokens
- [ ] Handle custom element events appropriately for your framework
- [ ] Test theming in both light and dark modes
- [ ] Ensure proper font loading (Roboto, Material Symbols)

## Resources

- `m3-theme.css` — Complete @material/web theme template (color, typography, shape, elevation, state, motion tokens) included in this skill's directory. Copy into your project and customize.
- `material-theme-builder` skill — Generate a custom token set from any source color.
- M3 for Web: https://m3.material.io/develop/web
- Documentation: https://material-web.dev/
- Quick start: https://material-web.dev/about/quick-start/
- Theming: https://material-web.dev/theming/material-theming/
- SCSS color API: https://github.com/material-components/material-web/blob/main/color/_color.scss
- Token reference: https://github.com/material-components/material-web/tree/main/tokens
- GitHub: https://github.com/material-components/material-web
- npm: https://www.npmjs.com/package/@material/web
