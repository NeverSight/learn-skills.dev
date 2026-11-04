---
name: brand-identity
description: >
  Build a complete visual identity from scratch or refresh one: logo mark and
  variations (SVG), brand color roles, brand fonts, patterns, favicons/app icons,
  social avatars, and a brand guidelines page. Use when the user needs the brand
  itself, not just one ingredient. Trigger phrases: "brand identity", "logo design",
  "brand guidelines", "visual identity", "brand system", "favicon", "logo variations",
  "brand pattern", "rebrand". For only a palette use color-palette; only fonts use
  typography; UI tokens/components use design-system.
license: MIT
---

# Brand Identity

Create cohesive visual identity systems that communicate brand values through code.

## Prerequisites

Before building a brand identity, check for existing design context:
- Read `.agents/design-context.md` (see `design-context`) for existing brand name, colors, fonts, style archetype, audience, and Brand Marks. Refresh only what the user wants changed.
- Identify the brand's industry, target audience, and personality traits (3-5 adjectives).
- Delegate depth: generate the full shade scale with the `color-palette` skill and the type scale with `typography`. Variables below (`--brand-100`, `--brand-500`, ...) are that shared primitive scale.

---

## Step 1: Logo Design Principles

### Core Rules

1. **Simplicity**: Must be recognizable at 16x16px (favicon size). Strip away every element that does not add meaning.
2. **Memorability**: One distinctive feature. Not three. Not five. One.
3. **Scalability**: Must work from 16px favicon to billboard. Avoid thin strokes that disappear at small sizes.
4. **Versatility**: Must work on light backgrounds, dark backgrounds, and photos.
5. **Timelessness**: Avoid trends (current gradients, specific illustration styles). Flat, geometric forms endure.

### CSS/SVG Logo Techniques

Use simple geometric SVG marks (48x48 viewBox, rounded rect + inner shape). For CSS-only marks: `display: grid; place-items: center` on a colored rounded square, `::after` pseudo-element for the inner shape.

Ship final logos as SVG with text converted to paths (or drawn as shapes) -- never depend on a web font or `<text>` inside a logo file. AI image generation (`image-generation` skill, Gemini) is useful for exploring concept directions and moodboards, but it produces raster images with unreliable lettering; redraw the chosen direction as clean SVG.

---

## Step 2: Logo Variations

Every brand needs at minimum 4 logo forms:

1. **Primary (Lockup)**: Icon + wordmark side by side (`flex, gap: 0.75rem`). Icon 40px, wordmark in heading font 1.25rem/700.
2. **Secondary (Stacked)**: Icon above wordmark (`flex-direction: column, text-align: center`).
3. **Icon Mark**: Symbol only -- for favicons, app icons, avatars.
4. **Wordmark Only**: Text-only version for inline use.

**Responsive pattern**: Show full logo by default, swap to icon-only at `max-width: 480px`.

---

## Step 3: Brand Color System

A brand color system is more than a palette. Structure it as:

### Color Roles

| Role       | Count | Purpose                                  |
|------------|-------|------------------------------------------|
| Primary    | 1     | Main brand color. CTAs, key UI elements. |
| Secondary  | 1     | Supporting accent. Complementary.        |
| Neutral    | 1 scale| Grays for text, borders, backgrounds.   |
| Semantic   | 4     | Success, warning, error, info.           |
| Surface    | 2-3   | Background layers.                       |

### Implementation

```css
:root {
  /* Brand */
  --color-primary: oklch(0.55 0.15 250);
  --color-primary-light: oklch(0.70 0.10 250);
  --color-primary-dark: oklch(0.40 0.15 250);

  --color-secondary: oklch(0.60 0.18 330);
  --color-secondary-light: oklch(0.75 0.12 330);

  /* Surfaces (semantic names shared with design-system) */
  --bg-primary: oklch(0.99 0.005 250);
  --bg-secondary: oklch(0.97 0.005 250);
  --bg-raised: oklch(1.00 0 0);

  /* Text */
  --text-primary: oklch(0.20 0.02 250);
  --text-secondary: oklch(0.50 0.01 250);  /* ~5.8:1 on bg-primary */
  --text-inverse: oklch(0.97 0.005 250);
}
```

Convert every final color to hex for the guidelines page and design-context (the color-palette skill has a conversion + contrast script), and verify each text/background pair.

---

## Step 4: Typography System

### Brand Font Selection

| Brand personality | Font style           | Examples                        |
|-------------------|---------------------|---------------------------------|
| Traditional       | Serif               | Playfair Display, Lora          |
| Modern / Clean    | Neo-grotesque / geometric sans | Inter, DM Sans, Manrope |
| Friendly / Warm   | Rounded sans        | Nunito, Quicksand               |
| Technical         | Monospace or grotesk| JetBrains Mono, Space Grotesk  |
| Luxury            | Thin serif/sans     | Cormorant, Outfit               |
| Playful           | Display or handwritten| Bricolage Grotesque, Caveat   |

### Font Stack Definition

```css
:root {
  --font-heading: 'Playfair Display', Georgia, 'Times New Roman', serif; /* design-context: Heading Font */
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
}
```

Always include system fallbacks. Always include generic family last.

---

## Step 5: Brand Pattern and Texture Elements

Subtle patterns add visual richness and brand recognition.

### Dot Grid Pattern

```css
.brand-pattern-dots {
  background-image: radial-gradient(
    circle,
    var(--brand-200) 1px,
    transparent 1px
  );
  background-size: 24px 24px;
}
```

### Diagonal Lines

```css
.brand-pattern-lines {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    var(--brand-100) 10px,
    var(--brand-100) 11px
  );
}
```

### Grid Pattern

```css
.brand-pattern-grid {
  background-image:
    linear-gradient(var(--brand-100) 1px, transparent 1px),
    linear-gradient(90deg, var(--brand-100) 1px, transparent 1px);
  background-size: 32px 32px;
}
```

### Gradient Noise Texture

```css
.brand-texture {
  position: relative;
}

.brand-texture::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}
```

---

## Step 6: Logo Spacing and Clear Zone

### Minimum Clear Space

The clear zone around a logo should equal the height of the logo mark (or a specific letter like the "x" in the wordmark).

```css
.logo-container {
  /* Clear zone = logo height on all sides */
  padding: var(--logo-clearzone, 2rem);
}

/* Minimum size constraints */
.logo-primary {
  min-width: 120px;  /* Never render smaller than this */
}

.logo-icon-mark {
  min-width: 24px;   /* Absolute minimum for icon-only */
}
```

### Usage Rules (Document These)

1. Do not rotate the logo.
2. Do not change the logo colors outside the approved set.
3. Do not stretch or distort.
4. Do not place on busy backgrounds without a container.
5. Maintain minimum clear space equal to the mark height.

---

## Step 7: Brand Guidelines Document Structure

When building a brand guidelines page or system, include these sections:

### Sections

1. **Brand Story**: Mission, vision, values (1 paragraph each).
2. **Logo**: All variations, clear zone rules, minimum sizes, misuse examples.
3. **Color**: Primary, secondary, semantic palettes with hex/oklch/rgb values.
4. **Typography**: Font families, scale, pairing rules.
5. **Imagery**: Photography style, illustration style, icon style.
6. **Voice & Tone**: Writing guidelines (though this is beyond visual design).
7. **Patterns & Textures**: Background treatments.
8. **Application Examples**: How everything comes together.

Structure as semantic sections (`<section id="logo">`, `<section id="colors">`, etc.) within a `<main class="brand-guide">`. Use specimen blocks (light/dark bg variants, `display: grid; place-items: center; min-height: 200px`) for logo display. Color swatches in auto-fit grid (`minmax(160px, 1fr)`).

---

## Step 8: Favicon and App Icon Generation

### Favicon Sizes

| Format    | Size    | Usage                          |
|-----------|---------|--------------------------------|
| ICO       | 32x32   | Browser tab (legacy)           |
| PNG       | 180x180 | Apple touch icon               |
| PNG       | 192x192 | Android home screen            |
| PNG       | 512x512 | Android splash, PWA            |
| SVG       | any     | Modern browsers, scalable      |

### SVG Favicon (Best Modern Approach)

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><!-- 180x180, no transparency -->
<link rel="manifest" href="/site.webmanifest">
```

```svg
<!-- favicon.svg - supports dark mode! -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>
    rect { fill: #4f46e5; }
    @media (prefers-color-scheme: dark) {
      rect { fill: #818cf8; }
    }
  </style>
  <rect width="32" height="32" rx="6"/>
  <!-- Letterform as a path, not <text>: fonts render differently per OS -->
  <path d="M11 8h6a4 4 0 0 1 0 8h-6zm0 8h7a4 4 0 0 1 0 8h-7z" fill="none" stroke="white" stroke-width="3" stroke-linejoin="round"/>
</svg>
```

Use the design-context Primary hex (and Primary Light for dark mode) instead of the example colors.

### Web Manifest

```json
{
  "name": "Brand Name",
  "short_name": "Brand",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "theme_color": "#4f46e5",
  "background_color": "#ffffff"
}
```

---

## Step 9: Social Media Avatar Consistency

### Rules for Platform Consistency

1. Use the icon mark (not the full logo) for square/circular avatars.
2. Add padding so the mark does not touch the circular crop edge.
3. Use the primary brand color as background.

```css
/* Avatar-safe logo layout */
.social-avatar {
  width: 400px;
  height: 400px;
  background: var(--brand-500);
  display: grid;
  place-items: center;
  border-radius: 50%; /* Preview circular crop */
}

.social-avatar .logo-mark {
  width: 55%;  /* Leave ~22.5% padding on each side */
  height: 55%;
  color: white;
}
```

### Platform Sizes

| Platform   | Recommended upload size |
|------------|------------------------|
| X/Twitter  | 400x400px              |
| LinkedIn   | 400x400px              |
| Instagram  | 320x320px              |
| GitHub     | 500x500px              |
| Slack      | 512x512px              |

---

## Step 10: Brand Application Examples

### Business Card
3.5x2in, flex column, `justify-content: space-between`. Name in display font 14pt/700, title 9pt uppercase in brand color, contact 8pt gray.

### Email Signature
Table-based: logo mark (48px) with brand-color `border-right`, name/title/contact stacked in adjacent cell. Use Arial, inline styles only.

---

## Step 11: Verify and Save

1. **Render a proof sheet** (scratchpad HTML): every logo variation on light, dark, and brand-color backgrounds; the icon mark at 16, 32, 48, and 180px; the favicon in a mock browser tab; the avatar inside a circle crop. Screenshot it (`npx playwright screenshot --full-page "file://$PWD/brand-proof.html" proof.png`) and view it with Read. Check: mark still recognizable at 16px, no strokes vanish, contrast holds on every background, nothing touches the circular crop.
2. **Offer to write back** to `.agents/design-context.md`, updating only changed fields: Brand Identity (name, tagline), Color System rows (hex), Typography fonts, Design Style archetype, and Brand Marks (Logo description, Icon Style). Show the diff and ask before saving.

---

## Quick Reference: Brand Identity Checklist

1. Define brand personality (3-5 adjectives).
2. Choose primary and secondary brand colors.
3. Select font pairing (heading + body).
4. Design logo mark, create all 4 variations.
5. Define clear zone and minimum sizes.
6. Generate full color system (shades, semantics, neutrals).
7. Create brand patterns/textures.
8. Build favicons and app icons.
9. Create social media avatar.
10. Document everything in a brand guidelines page.
11. Render a proof sheet, inspect it, and save the brand to design-context.
