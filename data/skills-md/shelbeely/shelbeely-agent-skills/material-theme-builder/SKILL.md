---
name: material-theme-builder
description: Generate Material Design 3 color themes programmatically from a source color using @material/material-color-utilities, the same engine that powers the Material Theme Builder. Use this when the user asks to generate an M3 color palette, create a custom theme from a brand color, or export M3 tokens to CSS, JSON, or framework configs.
license: Apache-2.0
---

# Material Theme Builder

## Overview

Generate complete Material Design 3 color themes programmatically from any source color. This skill uses `@material/material-color-utilities` — the same color algorithm library that powers Google's [Material Theme Builder](https://material-foundation.github.io/material-theme-builder/) — to produce accessible light/dark palettes, tonal ranges, and design tokens ready for CSS, JSON, or any framework.

**Keywords**: Material Theme Builder, color generation, dynamic color, theme export, @material/material-color-utilities, HCT, tonal palette, source color, brand color, CSS tokens, JSON export

## When to Use

- "Generate an M3 theme from my brand color"
- "Create M3 color tokens from #FF9800"
- "Export M3 palette as CSS custom properties"
- Creating a new M3 project and need a complete color token set
- Converting a hex brand color into a full M3 palette
- Generating both light and dark theme tokens programmatically

## How It Works

Material Color Utilities uses the **HCT color space** (Hue, Chroma, Tone) — a perceptually uniform color model built on CAM16 and L* — to generate five tonal palettes from a single source color:

1. **Primary** — derived from the source color's hue
2. **Secondary** — desaturated variant of the source hue
3. **Tertiary** — complementary hue for contrast
4. **Neutral** — very low chroma for surfaces and backgrounds
5. **Neutral Variant** — slightly chromatic neutral for outlines

Each palette contains tones 0–100. Specific tones are mapped to semantic color roles (e.g., `primary` = tone 40 in light, tone 80 in dark).

## Install

```bash
npm install @material/material-color-utilities
```

## Generate a Theme

Use the `generate-theme.mjs` script in this skill's directory:

```bash
node generate-theme.mjs "#FF9800"                     # CSS output (default tonal-spot)
node generate-theme.mjs "#FF9800" --json               # JSON output
node generate-theme.mjs "#FF9800" --scheme expressive   # Expressive scheme variant
```

### Available Scheme Variants

The `--scheme` flag selects from 9 dynamic color strategies defined in [material-color-utilities](https://github.com/material-foundation/material-color-utilities/tree/main/typescript/scheme):

| Scheme | Description |
|--------|-------------|
| `tonal-spot` | Default — balanced, versatile (used by Android Material You) |
| `content` | Colors derived with fidelity to the source, good for photo-based themes |
| `expressive` | Intentionally detached from source for bold, playful palettes |
| `fidelity` | High fidelity to source hue, chroma-capped for accessibility |
| `fruit-salad` | Vibrant, playful secondary and tertiary from offset hues |
| `monochrome` | Achromatic — all palettes have zero chroma |
| `neutral` | Near-achromatic — very low chroma for subtle, muted themes |
| `rainbow` | Wide hue spread across primary, secondary, and tertiary |
| `vibrant` | Saturated, colorful variant of tonal-spot |

### Quick Start (Node.js)

```js
import {
  argbFromHex,
  hexFromArgb,
  themeFromSourceColor,
} from "@material/material-color-utilities";

// Generate from any hex source color
const theme = themeFromSourceColor(argbFromHex("#FF9800"));

// Extract light scheme
const light = theme.schemes.light.toJSON();
for (const [role, argb] of Object.entries(light)) {
  console.log(`${role}: ${hexFromArgb(argb)}`);
}
```

### Full Theme with Surface Containers

The base `themeFromSourceColor` provides core roles. Surface container tones are derived from the neutral palette at specific tones:

```js
import {
  argbFromHex,
  hexFromArgb,
  themeFromSourceColor,
} from "@material/material-color-utilities";

const theme = themeFromSourceColor(argbFromHex("#FF9800"));
const neutral = theme.palettes.neutral;
const primary = theme.palettes.primary;
const secondary = theme.palettes.secondary;
const tertiary = theme.palettes.tertiary;

// Light surface containers (tone values per M3 spec)
const lightSurfaces = {
  surface:                 neutral.tone(98),
  surfaceDim:              neutral.tone(87),
  surfaceBright:           neutral.tone(98),
  surfaceContainerLowest:  neutral.tone(100),
  surfaceContainerLow:     neutral.tone(96),
  surfaceContainer:        neutral.tone(94),
  surfaceContainerHigh:    neutral.tone(92),
  surfaceContainerHighest: neutral.tone(90),
};

// Dark surface containers
const darkSurfaces = {
  surface:                 neutral.tone(6),
  surfaceDim:              neutral.tone(6),
  surfaceBright:           neutral.tone(24),
  surfaceContainerLowest:  neutral.tone(4),
  surfaceContainerLow:     neutral.tone(10),
  surfaceContainer:        neutral.tone(12),
  surfaceContainerHigh:    neutral.tone(17),
  surfaceContainerHighest: neutral.tone(22),
};

// Fixed colors (consistent across light and dark)
const fixed = {
  primaryFixed:              primary.tone(90),
  onPrimaryFixed:            primary.tone(10),
  primaryFixedDim:           primary.tone(80),
  onPrimaryFixedVariant:     primary.tone(30),
  secondaryFixed:            secondary.tone(90),
  onSecondaryFixed:          secondary.tone(10),
  secondaryFixedDim:         secondary.tone(80),
  onSecondaryFixedVariant:   secondary.tone(30),
  tertiaryFixed:             tertiary.tone(90),
  onTertiaryFixed:           tertiary.tone(10),
  tertiaryFixedDim:          tertiary.tone(80),
  onTertiaryFixedVariant:    tertiary.tone(30),
};
```

## Export Formats

### CSS Custom Properties

```js
function schemeToCss(scheme, selector = ":root") {
  const entries = Object.entries(scheme.toJSON());
  const props = entries
    .map(([key, argb]) => {
      const token = key.replace(/([A-Z])/g, "-$1").toLowerCase();
      return `  --md-sys-color-${token}: ${hexFromArgb(argb)};`;
    })
    .join("\n");
  return `${selector} {\n${props}\n}`;
}

console.log(schemeToCss(theme.schemes.light));
console.log(schemeToCss(theme.schemes.dark, '[data-theme="dark"]'));
```

### JSON

```js
function schemeToJson(scheme) {
  const result = {};
  for (const [key, argb] of Object.entries(scheme.toJSON())) {
    result[key] = hexFromArgb(argb);
  }
  return result;
}

const output = {
  source: "#FF9800",
  light: schemeToJson(theme.schemes.light),
  dark: schemeToJson(theme.schemes.dark),
};
console.log(JSON.stringify(output, null, 2));
```

### Apply to DOM

```js
import { applyTheme } from "@material/material-color-utilities";

const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
applyTheme(theme, { target: document.body, dark: systemDark });
```

## Custom Colors (Extended Palette)

Add brand-specific colors that harmonize with the generated theme:

```js
const theme = themeFromSourceColor(argbFromHex("#FF9800"), [
  {
    name: "brand-green",
    value: argbFromHex("#4CAF50"),
    blend: true, // harmonize with the source color
  },
  {
    name: "warning",
    value: argbFromHex("#FFC107"),
    blend: false, // keep exact hue
  },
]);

// Access custom colors
for (const custom of theme.customColors) {
  console.log(`${custom.color.name}:`);
  console.log(`  light: ${hexFromArgb(custom.light.color)}`);
  console.log(`  dark:  ${hexFromArgb(custom.dark.color)}`);
}
```

## Platform Libraries

| Platform    | Package |
|-------------|---------|
| TypeScript  | `@material/material-color-utilities` (npm) |
| Dart        | `material_color_utilities` (pub.dev) |
| Java/Kotlin | Built into MDC-Android |
| Swift       | Source in `material-color-utilities` repo |
| C++         | Source in `material-color-utilities` repo |

## Checklist

- [ ] Source color chosen (brand primary or user-provided hex)
- [ ] `@material/material-color-utilities` installed
- [ ] Light and dark schemes generated via `themeFromSourceColor`
- [ ] Surface container tokens derived from neutral palette tones
- [ ] Fixed accent colors derived from primary/secondary/tertiary palette tones
- [ ] Tokens exported in the target format (CSS, JSON, or framework config)
- [ ] Custom/extended colors added if needed (with harmonization)
- [ ] Both light and dark themes tested for WCAG contrast compliance

## Resources

- Material Theme Builder (web): https://material-foundation.github.io/material-theme-builder/
- Material Theme Builder (repo): https://github.com/material-foundation/material-theme-builder
- Material Color Utilities: https://github.com/material-foundation/material-color-utilities
- Official M3 CSS tokens (baseline): https://github.com/material-foundation/material-tokens
- npm: https://www.npmjs.com/package/@material/material-color-utilities
- M3 design tokens overview: https://m3.material.io/foundations/design-tokens/overview
- M3 color system: https://m3.material.io/styles/color/overview
- HCT color space: https://material.io/blog/science-of-color-design
