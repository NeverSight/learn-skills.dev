---
name: typography
description: >
  Typography for web and UI: modular type scales, font pairing, heading hierarchy,
  readable body text, fluid clamp() sizing, variable fonts, font loading, and text
  effects. Use when the task is about fonts or text styling. Trigger phrases:
  "typography", "font pairing", "type scale", "heading sizes", "responsive text",
  "font combination", "text style", "variable fonts", "fluid typography", "google fonts",
  "line height", "font loading". For a full token system (spacing, color, components)
  use design-system, which consumes the scale defined here.
license: MIT
---

# Typography Mastery

Create beautiful, readable, and systematic typography for any web project.

## Prerequisites

Before setting typography, check for existing design context:
- Read `.agents/design-context.md` (see `design-context`): Heading/Body/Mono Font, Base Size, Scale Ratio, Heading/Body Weight. Use them unless the user is explicitly changing them.
- If a design system exists in the codebase, align with its type scale and font stack.
- Note: the design-context "Type Scale Reference" (12/14/16/18/20/24/30/36/48/60/72) is Tailwind's hand-tuned scale, not a strict 1.25 progression. If the project already uses it, keep it; for new work, generate a true modular scale from the saved Scale Ratio (Step 1) and say which one you used.

---

## Step 1: Choose a Type Scale Ratio

The type scale ratio determines the mathematical relationship between sizes. Pick based on the content density and visual character of the project.

| Ratio           | Nickname | Value | Best for                           |
|-----------------|----------|-------|------------------------------------|
| Minor second    | Tight   | 1.067 | Dense data UIs, dashboards         |
| Major second    | Compact | 1.125 | Apps, tools, compact layouts       |
| Minor third     | Default | 1.200 | General web, blogs, marketing      |
| Major third     | Relaxed | 1.250 | Editorial, magazines               |
| Perfect fourth  | Bold    | 1.333 | Marketing sites, landing pages     |
| Augmented fourth| Impact  | 1.414 | Bold headlines, creative sites     |
| Perfect fifth   | Drama   | 1.500 | High-impact hero sections          |
| Golden ratio    | Grand   | 1.618 | Art, luxury, editorial             |

### Generate a Scale

```css
:root {
  --type-ratio: 1.25;   /* major third */
  --type-base: 1rem;    /* 16px */

  /* Each step = previous * ratio, so changing --type-ratio updates the whole scale */
  --text-xs:   max(0.75rem, calc(var(--text-sm) / var(--type-ratio))); /* 0.64rem = 10.24px -> floored to 12px */
  --text-sm:   calc(var(--type-base) / var(--type-ratio));  /* 0.8rem   = 12.8px */
  --text-base: var(--type-base);                             /* 1rem     = 16px   */
  --text-lg:   calc(var(--text-base) * var(--type-ratio));   /* 1.25rem  = 20px   */
  --text-xl:   calc(var(--text-lg) * var(--type-ratio));     /* 1.563rem = 25px   */
  --text-2xl:  calc(var(--text-xl) * var(--type-ratio));     /* 1.953rem = 31.25px */
  --text-3xl:  calc(var(--text-2xl) * var(--type-ratio));    /* 2.441rem = 39px   */
  --text-4xl:  calc(var(--text-3xl) * var(--type-ratio));    /* 3.052rem = 48.8px */
  --text-5xl:  calc(var(--text-4xl) * var(--type-ratio));    /* 3.815rem = 61px   */
}
```

Formula: `size(n) = base × ratio^n`. Comments above are for ratio 1.25; recompute them if you change the ratio. Keep functional text (captions, labels) at 12px or larger.

---

## Step 2: Font Pairing Rules

### Core Pairing Strategies

1. **Serif headings + Sans body**: Classic editorial feel. High contrast in structure.
2. **Geometric sans headings + Humanist sans body**: Modern but warm.
3. **Slab serif headings + Sans body**: Bold, confident.
4. **Mono headings + Sans body**: Technical, developer-oriented.
5. **Same family, different weights**: Safest option. Use 700+ for headings, 400 for body.

### What to Avoid

- Two fonts from the same category with similar proportions (e.g., two geometric sans).
- More than 2 typefaces on a single page (3 max if one is monospace for code).
- Decorative/display fonts for body text.

---

## Step 3: Curated Google Fonts Pairings

These are tested, production-ready combinations.

### Editorial / Content-heavy

1. **Playfair Display + Source Sans 3**
   Elegant serif headings, clean sans body. Great for magazines, blogs.

2. **Lora + Inter**
   Warm transitional serif + neutral modern sans. Excellent readability.

3. **Fraunces + Commissioner**
   Variable "soft" serif with personality + low-contrast humanist sans. Distinctive editorial.

### Modern / SaaS

4. **Inter + Inter**
   Single-family system. Use 700 for headings, 400 for body. Extremely versatile.

5. **DM Sans + DM Sans**
   Geometric, modern. Slightly more personality than Inter.

6. **Manrope + Source Sans 3**
   Semi-condensed geometric grotesque + humanist sans. Friendly tech feel.

### Bold / Marketing

7. **Space Grotesk + General Sans** (Fontshare, self-host) or **Space Grotesk + DM Sans**
   Monospace-influenced sans + clean geometric. Techy and bold.

8. **Bricolage Grotesque + Inter**
   Quirky variable sans for headings + reliable body text. Playful but professional.

9. **Cabinet Grotesk + Satoshi** (both Fontshare, self-host -- see Licensing)
   Modern geometric pair. Premium startup aesthetic.

### Specialized

10. **JetBrains Mono + Inter**
    Monospace headings/code + sans body. Developer tools, documentation.

11. **Instrument Serif + Instrument Sans**
    Companion serif/sans designed together. Low-risk pairing (Instrument Serif is display-weight only -- headings, not body).

12. **Sora + Newsreader**
    Geometric sans headings + readable serif body. Inverted classic pattern.

### CSS Import Pattern

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
```

```css
:root {
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

---

## Step 4: Heading Hierarchy

### Recommended Defaults (1.25 ratio, base 16px)

```css
h1 {
  font-family: var(--font-heading);
  font-size: var(--text-5xl);   /* ~3.8rem / 61px */
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.025em;
  margin-bottom: 0.5em;
}

h2 {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);   /* ~3.05rem / 49px */
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  margin-bottom: 0.5em;
}

h3 {
  font-family: var(--font-heading);
  font-size: var(--text-3xl);   /* ~2.44rem / 39px */
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.015em;
  margin-bottom: 0.5em;
}

h4 {
  font-size: var(--text-2xl);   /* ~1.95rem / 31px */
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.01em;
}

h5 {
  font-size: var(--text-xl);    /* ~1.56rem / 25px */
  font-weight: 600;
  line-height: 1.3;
}

h6 {
  font-size: var(--text-lg);    /* ~1.25rem / 20px */
  font-weight: 600;
  line-height: 1.4;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Key Rules

- Negative letter-spacing for large headings (-0.01em to -0.03em).
- Tighter line-height for headings (1.1-1.3) than body text.
- Never skip heading levels to get a smaller size (h1 -> h3). Heading levels are document structure for screen readers; decouple looks with classes (`<h2 class="h4">`).

---

## Step 5: Body Text Optimization

### The Golden Rules

- **Font size**: 16px minimum, 18px preferred for long-form content.
- **Line height**: 1.5 for UI, 1.6-1.75 for long-form reading.
- **Line length**: 45-75 characters per line (65ch is ideal).
- **Paragraph spacing**: 1em-1.5em between paragraphs.

```css
body {
  font-family: var(--font-body);
  font-size: 1.125rem;        /* 18px */
  line-height: 1.65;
  color: var(--text-primary, var(--gray-900)); /* design-context: Neutral 800 body / 900 headings */
  -webkit-font-smoothing: antialiased;  /* macOS only; harmless elsewhere */
  text-rendering: optimizeLegibility;
}

.prose {
  max-width: 65ch;
  margin-inline: auto;
}

.prose p + p {
  margin-top: 1.25em;
}

.prose > * + * {
  margin-top: 1em;
}
```

---

## Step 6: Responsive Typography with clamp()

Use `clamp()` for fluid scaling between breakpoints without media queries.

### Formula

```
clamp(min, preferred, max)
slope     = (maxSize - minSize) / (maxViewport - minViewport)      e.g. (24 - 20) / (1280 - 360) = 0.004348
preferred = (slope * 100)vw + (minSize - slope * minViewport)/16 rem
          = 0.4348vw + 1.152rem   ->  clamp(1.25rem, 0.4348vw + 1.152rem, 1.5rem)
```

Always keep a `rem` term in the preferred value: pure `vw` sizes do not grow with browser zoom and fail WCAG 1.4.4 (Resize Text).

### Practical Fluid Scale

This **replaces** the static scale from Step 1 (use one or the other, not both). Max values approximate a 1.25-1.33 progression at desktop widths; min values stay close to the mobile static scale.

```css
:root {
  --text-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --text-lg:   clamp(1.125rem, 0.75vw + 0.9rem, 1.35rem);
  --text-xl:   clamp(1.25rem, 1vw + 0.95rem, 1.75rem);
  --text-2xl:  clamp(1.5rem, 1.5vw + 1rem, 2.25rem);
  --text-3xl:  clamp(1.875rem, 2vw + 1.1rem, 3rem);
  --text-4xl:  clamp(2.25rem, 3vw + 1rem, 4rem);
  --text-5xl:  clamp(2.75rem, 4vw + 1rem, 5.5rem);
}
```

### Hero Headline Pattern

```css
.hero-title {
  font-size: clamp(2.5rem, 5vw + 1rem, 6rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-wrap: balance; /* evens out line lengths in short headings */
}
```

---

## Step 7: Text Treatments and Effects

### Gradient Text

```css
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Outlined / Stroke Text

```css
.outlined-text {
  -webkit-text-stroke: 2px currentColor;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  font-size: 5rem;
}
```

### Text Shadow and Text Over Images

```css
.text-shadow-soft { text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.text-shadow-hard { text-shadow: 3px 3px 0 rgba(0,0,0,0.15); }
.text-over-image  { text-shadow: 0 2px 16px rgba(0,0,0,0.5); } /* or a backdrop: */
.text-backdrop    { background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); padding: 0.5em 1em; border-radius: 0.25em; }
```

Gradient, outlined, and image-backed text must still meet contrast: measure the lightest part of the gradient/photo behind the text, and keep outlined text to display sizes.

---

## Step 8: Variable Fonts

### Common Axes

| Axis  | CSS property      | Range (typical) |
|-------|-------------------|-----------------|
| wght  | font-weight       | 100-900         |
| wdth  | font-stretch      | 75%-125%        |
| slnt  | font-style: oblique Xdeg | -12 to 0 (varies) |
| ital  | font-style: italic | 0 or 1         |
| opsz  | font-optical-sizing: auto | varies (Inter 14-32) |

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/InterVariable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}

.heading {
  font-family: 'Inter Variable', sans-serif;
  font-weight: 750;           /* precise weight */
  font-optical-sizing: auto;  /* uses Inter's opsz axis automatically */
}

/* Width only works if the font HAS a wdth axis (e.g. Roboto Flex, Mona Sans; Inter has none) */
.heading-wide { font-stretch: 110%; }
```

Prefer the high-level properties (`font-weight`, `font-stretch`, `font-style`, `font-optical-sizing`) over `font-variation-settings`, which overrides all axes at once and does not inherit per-axis. Check a font's axes on its Google Fonts page before using them.

---

## Step 9: Letter-Spacing and Word-Spacing Guidelines

| Context              | letter-spacing | Rationale                    |
|----------------------|----------------|------------------------------|
| Large headings (3rem+)| -0.02 to -0.03em | Tighten for visual density|
| Small headings        | -0.01em        | Slight tightening            |
| Body text             | normal (0)     | Default is optimized         |
| All-caps text         | +0.05 to +0.1em| Caps need room to breathe   |
| Small/caption text    | +0.01 to +0.02em| Improve legibility at small sizes|
| Monospace             | normal         | Already evenly spaced        |

```css
.caps-label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: var(--text-sm);
  font-weight: 600;
}
```

---

## Step 10: Font Loading Strategy

### Recommended Approach

Pick ONE: Google Fonts CDN (Option A) or self-hosting (Option B, better for performance and privacy/GDPR).

```html
<!-- Option A: Google Fonts CDN -- preconnect, then the stylesheet from Step 3 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Option B: self-hosted -- preload only the 1-2 files needed above the fold -->
<link rel="preload" as="font" type="font/woff2"
      href="/fonts/inter-var.woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;  /* Show fallback immediately, swap when loaded */
}
```

### font-display Values

| Value    | Behavior                              | Use when                      |
|----------|---------------------------------------|-------------------------------|
| swap     | Fallback shown immediately, swaps     | Body text, most cases         |
| optional | Brief block, may skip custom font     | Non-critical decorative fonts |
| fallback | Short block, short swap period        | Balance of swap + optional    |
| block    | Invisible text for up to 3s           | Icon fonts only               |

### System Font Stack Fallback

```css
:root {
  --font-system: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}
```

### Preventing Layout Shift

Use `size-adjust`, `ascent-override`, and `descent-override` to match fallback metrics:

```css
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body { font-family: 'Inter', 'Inter Fallback', sans-serif; }
```

These override values are for Inter over Arial; for other fonts generate them (e.g. Fontaine, Capsize, or `next/font`, which does it automatically).

### Licensing

- Google Fonts families are open source (almost all SIL OFL 1.1, a few Apache 2.0): free for commercial use, embedding, and self-hosting.
- Fontshare fonts (Satoshi, General Sans, Cabinet Grotesk) are free for commercial use under the ITF Free Font License, but are not on Google Fonts; download and self-host them.
- Commercial foundry fonts need a web license (often priced by pageviews). Never self-host a font file pulled from a design tool or OS without confirming the license.

---

## Quick Reference Checklist

1. Pick a type scale ratio appropriate to the project.
2. Choose max 2 typefaces (3 if including monospace).
3. Set body text to 16-18px with 1.5-1.75 line-height.
4. Constrain line length to 45-75 characters.
5. Use `clamp()` for fluid responsive sizing.
6. Apply negative letter-spacing to large headings.
7. Use positive letter-spacing for uppercase text.
8. Preload critical fonts; use `font-display: swap`.
9. Set up a system font fallback stack.
10. Use `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs to avoid orphans.

## Verify and Save

1. **Render a type specimen**: write an HTML page (scratchpad) showing h1-h6, body paragraph (~3 lines at real width), caption, label, code, and a long unbroken heading, using the actual fonts. Screenshot at 375px and 1280px wide (`npx playwright screenshot --viewport-size=375,800 --full-page "file://$PWD/specimen.html" mobile.png`) and look at both with Read. Check: fonts actually loaded (not fallback), clear step between each level, body line length 45-75 characters, no heading wider than the viewport.
2. **Offer to write back** to `.agents/design-context.md`: update only the changed Typography fields (Heading Font, Body Font, Mono Font, Base Size, Scale Ratio, Heading Weight, Body Weight) as full font stacks. Show the diff and ask before saving.
