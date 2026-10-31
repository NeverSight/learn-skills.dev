---
name: design-token-presets
description: "20+ ready-to-deploy token systems by industry vertical, each in W3C DTCG JSON, CSS custom properties, and Tailwind v4 @theme, with Style Dictionary config and Figma Variables mapping. Use when you want a vetted starting token set. For architecting your own, use design-systems-architecture."
---

# Design Token Presets — 20+ Ready-to-Deploy Token Systems

## Philosophy

Design tokens are the DNA of your UI. These presets are complete, production-ready token systems that you can deploy immediately and customize later. Each preset is opinionated by design — opinionated defaults ship faster than blank canvases.

"The best design system is the one that's actually used. Ship an opinionated preset today, customize tomorrow."

## Token Architecture (3-Tier)

Every preset follows the W3C Design Tokens Community Group (DTCG) standard:

### Tier 1: Primitive Tokens (Raw Values)
The foundational palette — colors, sizes, raw numbers.
```json
{ "color": { "blue": { "500": { "$value": "oklch(0.55 0.2 260)", "$type": "color" } } } }
```

### Tier 2: Semantic Tokens (Meaning)
Map primitives to purpose — what the color MEANS.
```json
{ "color": { "primary": { "$value": "{color.blue.500}", "$type": "color" } } }
```

### Tier 3: Component Tokens (Context)
Map semantics to specific components — where the color IS USED.
```json
{ "button": { "primary": { "background": { "$value": "{color.primary}", "$type": "color" } } } }
```

## Token Categories in Every Preset

| Category | Tokens | Description |
|----------|--------|-------------|
| Color | 80-120 tokens | 10-step scales per hue, semantic mapping, dark mode |
| Typography | 20-30 tokens | Font family, size scale, weight, line-height, letter-spacing |
| Spacing | 16-20 tokens | Base-4 scale from 0 to 96 |
| Border Radius | 6-8 tokens | none through full |
| Shadow | 5-6 tokens | sm through 2xl |
| Motion | 8-10 tokens | Duration + easing |
| Breakpoint | 5-7 tokens | xs through 2xl |
| Z-index | 8-10 tokens | Layer scale |
| Opacity | 5-6 tokens | Transparency scale |

## Color Generation Methodology

All colors use **oklch** color space for perceptual uniformity:
1. Choose a hue (0-360)
2. Set chroma (saturation intensity)
3. Generate 10 lightness steps: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
4. Validate APCA contrast for all text/background combinations
5. Map to semantic roles: background, surface, text, primary, secondary, success, warning, error, info

## Available Presets

### SaaS / Productivity (5 presets)
1. **"Linear"** — Minimal, monochromatic, violet accent. For precision tools
2. **"Notion"** — Warm neutrals, readable, content-first. For knowledge tools
3. **"Stripe"** — Premium blue-to-purple gradient, high-trust. For financial tools
4. **"Slack"** — Colorful, friendly, communication-focused. For social tools
5. **"Figma"** — Purple-accent, dense, productive. For creative tools

### Fintech / Healthcare (4 presets)
6. **"Mercury"** — Navy + clean accent, high trust. For banking
7. **"Robinhood"** — Black + green, action-oriented. For trading
8. **"Calm Health"** — Soft blues/greens, accessible. For patient-facing health
9. **"Clinical"** — High contrast, data-dense. For medical professionals

### E-commerce / Social (4 presets)
10. **"Shopify"** — Merchant-friendly green, versatile. For commerce
11. **"Premium Commerce"** — Elegant type, minimal color. For luxury retail
12. **"Social Warm"** — Warm gradients, engaging. For social platforms
13. **"Community"** — Dark-first, vibrant accents. For forums/communities

### Creative / Luxury / Dev (4 presets)
14. **"Studio"** — Bold type, minimal palette. For portfolios
15. **"Luxury"** — Serif type, gold/black, elegant. For premium brands
16. **"Playful"** — Bright colors, rounded, fun. For consumer apps
17. **"Developer"** — Mono-forward, syntax colors, dark-first. For dev tools

## Preset Structure (Example: "Linear")

```css
/* Linear Preset — CSS Custom Properties */

/* Primitives */
--color-gray-50: oklch(0.98 0.005 280);
--color-gray-100: oklch(0.95 0.005 280);
--color-gray-200: oklch(0.90 0.008 280);
--color-gray-300: oklch(0.82 0.010 280);
--color-gray-400: oklch(0.70 0.012 280);
--color-gray-500: oklch(0.55 0.015 280);
--color-gray-600: oklch(0.45 0.015 280);
--color-gray-700: oklch(0.35 0.012 280);
--color-gray-800: oklch(0.25 0.010 280);
--color-gray-900: oklch(0.18 0.008 280);
--color-gray-950: oklch(0.12 0.008 280);

--color-violet-500: oklch(0.55 0.20 290);

/* Semantic — Light Mode */
--color-bg: var(--color-gray-50);
--color-surface: white;
--color-surface-raised: white;
--color-text-primary: var(--color-gray-900);
--color-text-secondary: var(--color-gray-500);
--color-primary: var(--color-violet-500);
--color-border: var(--color-gray-200);

/* Semantic — Dark Mode */
--color-bg-dark: var(--color-gray-950);
--color-surface-dark: var(--color-gray-900);
--color-text-primary-dark: var(--color-gray-50);

/* Typography */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
--text-xs: 0.75rem; /* 12px */
--text-sm: 0.875rem; /* 14px */
--text-base: 1rem; /* 16px */
--text-lg: 1.125rem; /* 18px */
--text-xl: 1.25rem; /* 20px */
--text-2xl: 1.5rem; /* 24px */
--text-3xl: 1.875rem; /* 30px */
--text-4xl: 2.25rem; /* 36px */

/* Spacing (base-4) */
--space-0: 0; --space-1: 4px; --space-2: 8px;
--space-3: 12px; --space-4: 16px; --space-5: 20px;
--space-6: 24px; --space-8: 32px; --space-10: 40px;
--space-12: 48px; --space-16: 64px; --space-20: 80px;
--space-24: 96px;

/* Border Radius */
--radius-none: 0; --radius-sm: 4px; --radius-md: 8px;
--radius-lg: 12px; --radius-xl: 16px; --radius-full: 9999px;

/* Shadow */
--shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
--shadow-md: 0 4px 6px oklch(0 0 0 / 0.07);
--shadow-lg: 0 10px 15px oklch(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px oklch(0 0 0 / 0.1);

/* Motion */
--duration-instant: 50ms; --duration-fast: 150ms;
--duration-normal: 250ms; --duration-slow: 400ms;
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in: cubic-bezier(0.55, 0.055, 0.675, 0.19);
--ease-in-out: cubic-bezier(0.87, 0, 0.13, 1);
```

## Customization Guide

### Changing the Primary Color
1. Choose your brand hue in oklch (e.g., hue 200 for teal)
2. Generate 10 lightness steps maintaining chroma
3. Replace `--color-primary` semantic mapping
4. Validate APCA contrast ratios

### Making a Preset Warmer
- Shift gray hue from 280 (cool) toward 40-60 (warm)
- Increase chroma slightly on grays (0.005 → 0.015)
- Choose warmer accent hues (amber, coral, warm violet)

### Making a Preset Darker
- Set default mode to dark
- Reduce surface lightness
- Increase text lightness for contrast

## Reference Files

Detailed presets are available in the `references/` directory:
- `saas-fintech-presets.md` — Linear, Stripe, Notion, Slack, Figma, Mercury, Robinhood presets (CSS `:root` + Tailwind v4 `@theme`)
- `ecommerce-social-presets.md` — Shopify, Premium Commerce, Social Warm, Community presets (CSS `:root` + Tailwind v4 `@theme`)
- `creative-dev-health-presets.md` — Studio, Luxury, Playful, Developer, Calm Health, Clinical presets (CSS `:root` + Tailwind v4 `@theme`)
- `dtcg-json-presets.md` — W3C DTCG JSON format for 6 flagship presets (Linear SaaS, Stripe Fintech, Shopify E-commerce, Discord Social, Creative Agency, Healthcare). 3-tier structure (primitive/semantic/component). Style Dictionary 4.x config. Figma Variables mapping.

## Cross-References

- **design-systems-architecture** — Token architecture deep-dive
- **sector-style-intelligence** — Industry visual direction
- **color-palette-library** — 500+ color palettes
- **ui-visual-design-system** — Typography and spacing theory
- **visual-design-mastery** — Complete visual scoring
