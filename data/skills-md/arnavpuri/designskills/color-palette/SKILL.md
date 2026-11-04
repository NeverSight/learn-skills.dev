---
name: color-palette
description: >
  Generate accessible color palettes: OKLCH shade scales (50-950), tinted neutrals,
  semantic colors, WCAG contrast checks, dark-mode color remaps, gradients, and
  CSS/Tailwind color output. Use when the task is ONLY about color. Trigger phrases:
  "color palette", "color scheme", "generate colors", "shade scale", "color tokens",
  "color system", "accessible colors", "contrast ratio", "semantic colors", "palette from hex".
  For logo + fonts + guidelines use brand-identity; for full token/component systems
  (spacing, radius, components) use design-system; for complete dark themes use dark-mode.
license: MIT
---

# Color Palette Generation

Generate harmonious, accessible, and production-ready color systems from any starting point.

## Prerequisites

Before generating colors, check for existing design context:
- Read `.agents/design-context.md` (see the `design-context` skill). If it has a Color System, treat those hex values as the source of truth and extend them rather than replacing them.
- If a design system already exists in the codebase (CSS variables, Tailwind theme, `tokens.json`), extend it rather than replacing it.

**Naming convention (shared with design-system, layout-composition, etc.):** primitive scales are `--brand-50 … --brand-950`, `--gray-50 … --gray-950`, `--success-*`, `--warning-*`, `--error-*`, `--info-*`; semantic tokens are `--bg-*`, `--text-*`, `--border-*`, `--interactive-*`, plus the brand aliases `--color-primary`, `--color-secondary`, `--color-accent`.

---

## Step 1: Understand Color Theory Fundamentals

Generate palettes in **OKLCH**. Its lightness channel is perceptually even, so a fixed L step looks like the same visual step at every hue (in HSL, `hsl(60 100% 50%)` yellow is far lighter than `hsl(240 100% 50%)` blue at the "same" lightness). Use HSL only when a legacy tool forces it. Note that high-chroma OKLCH values can fall outside sRGB; reduce chroma (keep L and H) when converting to hex.

### Color Wheel Relationships

| Harmony        | Angle(s) from base | Feel                        |
|----------------|--------------------|-----------------------------|
| Complementary  | 180°               | High contrast, energetic    |
| Analogous      | ±30°               | Harmonious, natural         |
| Triadic        | 120°, 240°         | Vibrant, balanced           |
| Split-comp.    | 150°, 210°         | Contrast with less tension  |
| Tetradic       | 90°, 180°, 270°    | Rich, needs careful balance |

### Generating Harmonies in OKLCH

```css
:root {
  /* Base brand color in oklch */
  --brand-hue: 250;         /* hue angle */
  --brand-chroma: 0.15;     /* chroma (not HSL saturation) */
  --brand-l: 0.55;          /* lightness */

  --color-primary:       oklch(var(--brand-l) var(--brand-chroma) var(--brand-hue));
  --color-complement:    oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 180));
  --color-analogous-1:   oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 30));
  --color-analogous-2:   oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) - 30));
  --color-triadic-1:     oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 120));
  --color-triadic-2:     oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 240));
  --color-split-comp-1:  oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 150));
  --color-split-comp-2:  oklch(var(--brand-l) var(--brand-chroma) calc(var(--brand-hue) + 210));
}
```

---

## Step 2: Generate a Full Shade Scale (50-950)

From a single brand color, generate an 11-step lightness scale (50, 100-900, 950). In OKLCH, vary lightness while keeping hue stable and slightly reducing chroma at extremes.

### Lightness Map

| Token | OKLCH Lightness | Usage                    |
|-------|-----------------|--------------------------|
| 50    | 0.97            | Tinted background        |
| 100   | 0.93            | Hover background         |
| 200   | 0.87            | Active background        |
| 300   | 0.78            | Borders                  |
| 400   | 0.68            | Placeholder text         |
| 500   | 0.55            | Base / primary actions   |
| 600   | 0.48            | Hover on primary         |
| 700   | 0.40            | Active on primary        |
| 800   | 0.32            | Headings on light bg     |
| 900   | 0.24            | Body text on light bg    |
| 950   | 0.16            | High-contrast text       |

### CSS Implementation

```css
:root {
  --brand-hue: 250;
  --brand-chroma: 0.15;

  --brand-50:  oklch(0.97 calc(var(--brand-chroma) * 0.3) var(--brand-hue));
  --brand-100: oklch(0.93 calc(var(--brand-chroma) * 0.4) var(--brand-hue));
  --brand-200: oklch(0.87 calc(var(--brand-chroma) * 0.5) var(--brand-hue));
  --brand-300: oklch(0.78 calc(var(--brand-chroma) * 0.7) var(--brand-hue));
  --brand-400: oklch(0.68 calc(var(--brand-chroma) * 0.85) var(--brand-hue));
  --brand-500: oklch(0.55 var(--brand-chroma) var(--brand-hue));
  --brand-600: oklch(0.48 var(--brand-chroma) var(--brand-hue));
  --brand-700: oklch(0.40 var(--brand-chroma) var(--brand-hue));
  --brand-800: oklch(0.32 calc(var(--brand-chroma) * 0.9) var(--brand-hue));
  --brand-900: oklch(0.24 calc(var(--brand-chroma) * 0.8) var(--brand-hue));
  --brand-950: oklch(0.16 calc(var(--brand-chroma) * 0.7) var(--brand-hue));
}
```

---

## Step 3: Define Semantic Colors

Map purpose-driven tokens to your palette or define independent hues.

### Recommended Semantic Hues

| Role    | Hue (OKLCH) | Rationale              |
|---------|-------------|------------------------|
| Success | 145         | Green, universal "go"  |
| Warning | 85          | Amber/yellow, caution  |
| Error   | 25          | Red, urgency           |
| Info    | 230         | Blue, neutral info     |

```css
:root {
  /* Semantic: success */
  --success-50:  oklch(0.97 0.04 145);
  --success-400: oklch(0.68 0.15 145);  /* dark-mode foreground */
  --success-500: oklch(0.55 0.16 145);
  --success-700: oklch(0.40 0.14 145);

  /* Semantic: warning */
  --warning-50:  oklch(0.97 0.04 85);
  --warning-400: oklch(0.72 0.15 85);
  --warning-500: oklch(0.60 0.16 85);   /* ~4:1 on white: use dark text ON it, 700 for warning TEXT */
  --warning-700: oklch(0.45 0.14 85);

  /* Semantic: error */
  --error-50:  oklch(0.97 0.04 25);
  --error-400: oklch(0.68 0.16 25);
  --error-500: oklch(0.55 0.18 25);
  --error-700: oklch(0.40 0.16 25);

  /* Semantic: info */
  --info-50:  oklch(0.97 0.04 230);
  --info-400: oklch(0.68 0.12 230);
  --info-500: oklch(0.55 0.14 230);
  --info-700: oklch(0.40 0.12 230);
}
```

Generate the full 50-950 scale for a semantic hue only if the product needs it (alerts, badges, charts); 50/400/500/700 covers most UI.

---

## Step 4: Generate a Neutral Scale

Neutrals are the backbone. Add a slight hue tint from the brand for warmth.

```css
:root {
  --neutral-hue: var(--brand-hue);
  --neutral-chroma: 0.01; /* barely tinted */

  --gray-50:  oklch(0.98 var(--neutral-chroma) var(--neutral-hue));
  --gray-100: oklch(0.96 var(--neutral-chroma) var(--neutral-hue));
  --gray-200: oklch(0.90 var(--neutral-chroma) var(--neutral-hue));
  --gray-300: oklch(0.83 var(--neutral-chroma) var(--neutral-hue));
  --gray-400: oklch(0.71 var(--neutral-chroma) var(--neutral-hue));
  --gray-500: oklch(0.55 var(--neutral-chroma) var(--neutral-hue));
  --gray-600: oklch(0.45 var(--neutral-chroma) var(--neutral-hue));
  --gray-700: oklch(0.37 var(--neutral-chroma) var(--neutral-hue));
  --gray-800: oklch(0.27 var(--neutral-chroma) var(--neutral-hue));
  --gray-900: oklch(0.20 var(--neutral-chroma) var(--neutral-hue));
  --gray-950: oklch(0.13 var(--neutral-chroma) var(--neutral-hue));
}
```

---

## Step 5: Ensure WCAG Accessibility

### Contrast Requirements (WCAG 2.2 -- the current legal/industry standard)

| Level    | Normal text | Large text (≥24px, or ≥18.66px / 14pt bold) | Non-text UI (icons, borders, focus rings, chart marks) |
|----------|-------------|---------------------------------------------|--------------------------------------------------------|
| WCAG AA  | 4.5:1       | 3:1                                         | 3:1 against adjacent colors (SC 1.4.11)               |
| WCAG AAA | 7:1         | 4.5:1                                       | --                                                     |

Contrast ratio = `(L1 + 0.05) / (L2 + 0.05)`, where L1/L2 are the lighter/darker **relative luminance** (`0.2126 R + 0.7152 G + 0.0722 B` on linearized sRGB). Ratios are not rounded up: 4.49:1 fails. APCA (Lc values) is a draft candidate for WCAG 3 -- useful as a second opinion, especially for dark mode, but never report it as the compliance standard.

### Practical Rules

- **Body text on light bg**: use 900 or 950 shade (passes AA comfortably with the lightness map above).
- **Body text on dark bg**: use 50 or 100 shade.
- **Primary buttons**: white text on 500+ shade *usually* passes (L 0.55 blue ≈ 4.9:1), but yellows/ambers/cyans at L 0.55-0.65 often fail -- use dark text on those. Always measure.
- **Disabled states**: use 400 shade on light bg. Disabled elements are exempt from WCAG but should still be distinguishable.
- **Links**: must be distinguishable from surrounding text by more than color alone -- underline them, or give them 3:1 contrast against the surrounding text *plus* a non-color cue on hover/focus.

### Quick Contrast Check via OKLCH Lightness

For near-neutral colors, relative luminance ≈ L³, so a lightness gap of about **0.42-0.45+** is needed for 4.5:1 at the extremes (and more in the mid-range). Use it only to pick candidates, then measure.

```
text L 0.20 | bg L 0.97 | diff 0.77 -> ~16.6:1, passes AAA
text L 0.55 | bg L 0.97 | diff 0.42 -> ~4.5:1, borderline AA -- measure; safe for large text
text L 0.57 | bg L 0.97 | diff 0.40 -> ~4.1:1, FAILS AA for normal text
```

### Measure, Don't Guess

Browsers render OKLCH directly, but design-context stores hex and contrast must be computed on sRGB. Use the bundled scripts (`<color-palette>` and `<design-context>` are those skills' directories):

```bash
python <color-palette>/scripts/palette.py --from "#2563eb"                 # scale around a brand color
python <color-palette>/scripts/palette.py 250 0.15 --name brand --css      # hue + chroma -> CSS vars
python <color-palette>/scripts/palette.py 250 0.02 --name gray --json      # neutrals as JSON
python <design-context>/scripts/contrast.py "#ffffff" "#2563eb"             # any real pairing
```

`palette.py` prints each step's hex and contrast on white/black, marked `AA` (4.5:1), `large/UI` (3:1) or `-`. Out-of-gamut steps lose chroma, never lightness or hue. `contrast.py` exits 1 on a failure and suggests the nearest passing shade.

Also check every real text/background pairing you ship (text on `--bg-*`, button label on `--interactive-*`, dark-mode pairs), not just against pure white/black.

---

## Step 6: Dark Mode Adaptation

Do NOT simply invert the scale. Instead, remap semantic usage.

### Dark Mode Strategy

```css
[data-theme="dark"] {
  /* Backgrounds: use 900/950 instead of 50/white */
  --bg-primary:   var(--gray-950);
  --bg-secondary: var(--gray-900);
  --bg-tertiary:  var(--gray-800);

  /* Text: use 50/100 instead of 900/950 */
  --text-primary:   var(--gray-50);
  --text-secondary: var(--gray-300);
  --text-tertiary:  var(--gray-400);

  /* Surfaces: slightly lighter than bg */
  --surface:       var(--gray-900);
  --surface-hover: var(--gray-800);

  /* Borders: use 700 instead of 200 */
  --border-default: var(--gray-700);

  /* Brand colors: increase lightness for dark bg */
  --interactive-primary: var(--brand-400); /* lighter than 500 */

  /* Semantic: bump to lighter shades */
  --color-success: var(--success-400);
  --color-warning: var(--warning-400);
  --color-error:   var(--error-400);
}
```

These names must match the light-mode Layer 2 tokens in Step 10 -- dark mode only remaps them. For a full dark theme (elevation surfaces, images, toggles) hand off to the `dark-mode` skill.

### Key Principles

1. Reduce contrast slightly -- pure white on pure black is harsh. Use gray-50 on gray-950.
2. Reduce chroma slightly in dark mode -- saturated colors glow on dark backgrounds.
3. Elevations in dark mode use lighter surfaces (opposite of light mode shadows).

---

## Step 7: Color Psychology by Industry

| Industry      | Primary colors          | Why                               |
|---------------|------------------------|------------------------------------|
| Finance       | Navy, dark blue, green | Trust, stability, growth           |
| Health        | Blue, teal, white      | Calm, cleanliness, trust           |
| Food          | Red, orange, yellow    | Appetite, energy, warmth           |
| Tech/SaaS     | Blue, violet, cyan     | Innovation, reliability            |
| Luxury        | Black, gold, deep purple| Elegance, exclusivity             |
| Eco/Green     | Green, earth tones     | Nature, sustainability             |
| Education     | Blue, orange, green    | Trust, enthusiasm, growth          |
| Creative      | Bold primaries, neons  | Energy, expression, fun            |

---

## Step 8: Gradient Combinations

### Rules for Effective Gradients

1. Stay within 60 degrees of hue rotation for subtle gradients.
2. Use 90-180 degrees for vibrant, energetic gradients.
3. Writing stops in `oklch()` does NOT make the gradient interpolate in OKLCH. Without an interpolation hint, browsers use Oklab for modern colors and sRGB for hex/rgb/hsl stops -- both go straight through the color space and can pass through gray between distant hues. Add `in oklch` to interpolate around the hue wheel (add `longer hue` for rainbow sweeps).
4. Or add a mid stop with a slight chroma boost to avoid the "gray dead zone."

```css
/* Subtle brand gradient */
.gradient-subtle {
  background: linear-gradient(
    135deg in oklch,
    oklch(0.55 0.15 250),
    oklch(0.55 0.15 280)
  );
}

/* Vibrant hero gradient */
.gradient-vibrant {
  background: linear-gradient(
    135deg in oklch,
    oklch(0.65 0.20 280),
    oklch(0.60 0.22 330),
    oklch(0.65 0.20 20)
  );
}

/* Mesh gradient (modern trend) */
.gradient-mesh {
  background:
    radial-gradient(at 0% 0%, oklch(0.70 0.15 280) 0%, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.70 0.15 200) 0%, transparent 50%),
    radial-gradient(at 100% 100%, oklch(0.70 0.15 330) 0%, transparent 50%),
    oklch(0.97 0.01 250);
}
```

---

## Step 9: Tailwind Config Generation

**Tailwind v4** (CSS-first) -- put the scale in `@theme`, which generates `bg-brand-500`, `text-brand-900`, etc.:

```css
@import "tailwindcss";
@theme {
  --color-brand-50:  oklch(0.97 0.045 250);
  --color-brand-500: oklch(0.55 0.15 250);
  --color-brand-900: oklch(0.24 0.12 250);
  /* ...every step 50-950, plus success/warning/error/info */
}
```

**Tailwind v3** (`tailwind.config.js`):

```js
// tailwind.config.js
const brand = {
  50:  'oklch(0.97 0.045 250)',
  100: 'oklch(0.93 0.06 250)',
  200: 'oklch(0.87 0.075 250)',
  300: 'oklch(0.78 0.105 250)',
  400: 'oklch(0.68 0.1275 250)',
  500: 'oklch(0.55 0.15 250)',
  600: 'oklch(0.48 0.15 250)',
  700: 'oklch(0.40 0.15 250)',
  800: 'oklch(0.32 0.135 250)',
  900: 'oklch(0.24 0.12 250)',
  950: 'oklch(0.16 0.105 250)',
};

module.exports = {
  theme: {
    extend: {
      colors: {
        brand,
        success: { /* ... same pattern, hue 145 */ },
        warning: { /* ... same pattern, hue 85 */ },
        error:   { /* ... same pattern, hue 25 */ },
        info:    { /* ... same pattern, hue 230 */ },
      },
    },
  },
};
```

---

## Step 10: CSS Custom Properties Architecture

Structure tokens in three layers:

```css
/* Layer 1: Primitive (raw values) */
:root {
  --brand-500: oklch(0.55 0.15 250);
  --error-500: oklch(0.55 0.18 25);
  /* ...full --brand-*, --gray-*, semantic scales from Steps 2-4 */
}

/* Layer 2: Semantic (purpose) -- same names design-system uses */
:root {
  --color-primary:       var(--brand-500);
  --interactive-primary: var(--brand-500);
  --color-error:         var(--error-500);
  --bg-primary:          var(--gray-50);
  --text-primary:        var(--gray-900);
  --border-default:      var(--gray-200);
}

/* Layer 3: Component (scoped) */
.btn-primary {
  background: var(--interactive-primary);
  color: white; /* verified >= 4.5:1 against brand-500 */
}
```

This three-layer approach makes theming and dark mode trivial -- you only remap Layer 2.

---

## Step 11: Verify Visually and Save to Design Context

1. **Render a swatch sheet**: write a small HTML file (scratchpad) showing each scale as a row of swatches labeled with token, hex, and contrast vs white/black, plus sample text/button pairings in light AND dark mode. Screenshot it (e.g. `npx playwright screenshot --full-page "file://$PWD/swatches.html" swatches.png`; add `--color-scheme=dark` for the dark pass) and look at the image with Read. Check that steps look evenly spaced, no step is muddy or neon, and neutrals read as neutral.
2. **Offer to write back** to `.agents/design-context.md` (the `design-context` skill's file). Update only the Color System rows that changed; never rewrite the whole file. Map the scale to the design-context roles as hex:

| design-context role | Take from |
|---------------------|-----------|
| Primary | `--brand-500` (or 600 if 500 fails 4.5:1 with white text) |
| Primary Light / Primary Dark | `--brand-400` / `--brand-700` |
| Secondary / Accent | 500 step of the secondary / accent hue |
| Neutral 50 / 100 / 200 / 500 / 800 / 900 | matching `--gray-*` steps |
| Success / Warning / Error | `--success-500` / `--warning-500` / `--error-500` |

Show the user a before/after diff of the changed rows and ask before saving.

---

## Quick Reference: Palette from a Single Hex

1. Read `.agents/design-context.md`; convert the brand hex to OKLCH.
2. Extract hue. This is your brand hue.
3. Generate 50-950 scale using the lightness map in Step 2.
4. Generate neutrals tinted with brand hue (Step 4).
5. Pick semantic hues (Step 3).
6. Measure contrast with `palette.py` / `contrast.py` (Step 5) -- fix failures before continuing.
7. Build dark mode remap (Step 6).
8. Export as CSS custom properties or Tailwind config.
9. Render and inspect a swatch sheet; offer to save hex values to design-context (Step 11).
