---
name: m3-web-svelte
description: Implement Material Design 3 in Svelte using SMUI (Svelte Material UI) or @material/web directly. Covers component usage, theming, and Svelte 5 compatibility. Use this when building M3-styled Svelte or SvelteKit applications.
license: Apache-2.0
---

# Material Design 3 — Svelte / SMUI

## Overview

SMUI (Svelte Material UI) wraps Google's MDC-Web foundation logic in Svelte-native components. Evolving towards M3 with MDC v10 integration. Svelte 5 compatible (v8+). Alternatively, use `@material/web` directly — Svelte has excellent Custom Elements support.

**Keywords**: Material Design 3, M3, Svelte, SMUI, Svelte Material UI, SvelteKit, web components, MDC

## When to Use

- Svelte or SvelteKit projects
- When you want Svelte-native Material components
- Projects that can also use `@material/web` directly (Svelte handles Custom Elements well)

## Install (SMUI)

```bash
npm install svelte-material-ui
```

Individual packages:
```bash
npm install @smui/button @smui/card @smui/textfield @smui/top-app-bar
```

## Install (@material/web — alternative)

```bash
npm install @material/web
```

## SMUI Component Examples

### Buttons

```svelte
<script>
  import Button from '@smui/button';
</script>

<Button variant="raised">Filled</Button>
<Button variant="outlined">Outlined</Button>
<Button>Text</Button>
```

### Cards

```svelte
<script>
  import Card from '@smui/card';
</script>

<Card>
  <div class="card-content">
    <h2>Card Title</h2>
    <p>Card content</p>
  </div>
</Card>
```

### Text Fields

```svelte
<script>
  import Textfield from '@smui/textfield';
</script>

<Textfield variant="outlined" label="Email" />
<Textfield variant="filled" label="Name" />
```

## Using @material/web in Svelte

Svelte handles web components natively:

```svelte
<script>
  import '@material/web/button/filled-button.js';
  import '@material/web/textfield/outlined-text-field.js';
  import '@material/web/checkbox/checkbox.js';
</script>

<md-filled-button>Click me</md-filled-button>
<md-outlined-text-field label="Email"></md-outlined-text-field>
<md-checkbox></md-checkbox>
```

Theme via CSS custom properties in your global stylesheet:
```css
:root {
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-ref-typeface-brand: 'Roboto';
}
```

## Checklist

- [ ] Choose between SMUI and @material/web based on project needs
- [ ] M3 color tokens applied via CSS custom properties or SMUI theming
- [ ] Components use M3-aligned variants
- [ ] Both light and dark themes supported
- [ ] Svelte 5 compatibility verified (SMUI v8+)

## Resources

- SMUI: https://sveltematerialui.com/
- SMUI GitHub: https://github.com/hperrin/svelte-material-ui
- @material/web (works in Svelte): https://material-web.dev/
- @material/web GitHub: https://github.com/material-components/material-web
