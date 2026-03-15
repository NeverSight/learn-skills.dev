---
name: material-design-3-typography
description: Applies Material Design 3 Expressive typography principles including variable fonts, type scales, and hierarchy. Use this when working on text styling, type hierarchy, readable interfaces, or when the user asks to apply Material Design 3 typography guidelines.
license: Apache-2.0
---

# Material Design 3 Typography

## Overview

This skill guides the implementation of Material Design 3 (M3) typography — from the baseline Material You type scale through to M3 Expressive's 30-style expanded type system — to create clear, readable, and emotionally engaging text hierarchies.

**Keywords**: Material Design 3, M3, typography, type scale, variable fonts, text hierarchy, readability, font weights, line height, letter spacing, emphasized type, medium contrast, Material You

## Core Principles

### Typography Philosophy

M3 typography focuses on:

1. **Variable Fonts**: Support dynamic weight and width adjustments for expressive text
2. **Clear Hierarchy**: Distinct type scales that guide users through content
3. **Readability**: Optimized for legibility across devices and contexts
4. **Flexibility**: Adaptable to different content needs and screen sizes
5. **Expression**: Typography that conveys personality and emotion
6. **Emphasis**: Baseline and emphasized variants for every type role (M3 Expressive)

## Type Scale

### Baseline Type Scale (15 styles)

M3 defines a comprehensive type scale with specific roles for different UI elements. These 15 baseline styles form the foundation of all M3 typography:

#### Display Styles (Large, attention-grabbing text)

**Display Large**:
- Font: Roboto (or brand font)
- Size: 57px / 3.562rem
- Line Height: 64px / 4rem
- Weight: 400 (Regular)
- Letter Spacing: -0.25px
- Use: Largest headlines, hero text

**Display Medium**:
- Size: 45px / 2.812rem
- Line Height: 52px / 3.25rem
- Weight: 400
- Letter Spacing: 0
- Use: Large section headers

**Display Small**:
- Size: 36px / 2.25rem
- Line Height: 44px / 2.75rem
- Weight: 400
- Letter Spacing: 0
- Use: Smaller headers, card titles

#### Headline Styles (Structural headings)

**Headline Large**:
- Size: 32px / 2rem
- Line Height: 40px / 2.5rem
- Weight: 400
- Letter Spacing: 0
- Use: Page titles, major sections

**Headline Medium**:
- Size: 28px / 1.75rem
- Line Height: 36px / 2.25rem
- Weight: 400
- Letter Spacing: 0
- Use: Subsection headers

**Headline Small**:
- Size: 24px / 1.5rem
- Line Height: 32px / 2rem
- Weight: 400
- Letter Spacing: 0
- Use: Component headers, dialog titles

#### Title Styles (Emphasis within components)

**Title Large**:
- Size: 22px / 1.375rem
- Line Height: 28px / 1.75rem
- Weight: 400
- Letter Spacing: 0
- Use: Large list items, emphasized text

**Title Medium**:
- Size: 16px / 1rem
- Line Height: 24px / 1.5rem
- Weight: 500 (Medium)
- Letter Spacing: 0.15px
- Use: Card titles, list headers

**Title Small**:
- Size: 14px / 0.875rem
- Line Height: 20px / 1.25rem
- Weight: 500
- Letter Spacing: 0.1px
- Use: Compact card titles, tabs

#### Body Styles (Main content)

**Body Large**:
- Size: 16px / 1rem
- Line Height: 24px / 1.5rem
- Weight: 400
- Letter Spacing: 0.5px
- Use: Long-form content, articles

**Body Medium**:
- Size: 14px / 0.875rem
- Line Height: 20px / 1.25rem
- Weight: 400
- Letter Spacing: 0.25px
- Use: Default body text

**Body Small**:
- Size: 12px / 0.75rem
- Line Height: 16px / 1rem
- Weight: 400
- Letter Spacing: 0.4px
- Use: Captions, helper text

#### Label Styles (UI elements)

**Label Large**:
- Size: 14px / 0.875rem
- Line Height: 20px / 1.25rem
- Weight: 500
- Letter Spacing: 0.1px
- Use: Button text, navigation items

**Label Medium**:
- Size: 12px / 0.75rem
- Line Height: 16px / 1rem
- Weight: 500
- Letter Spacing: 0.5px
- Use: Small buttons, chips

**Label Small**:
- Size: 11px / 0.687rem
- Line Height: 16px / 1rem
- Weight: 500
- Letter Spacing: 0.5px
- Use: Tiny labels, timestamps

### Emphasized Type Scale (15 additional styles — M3 Expressive)

M3 Expressive adds 15 emphasized variants — one for each baseline style. Emphasized styles are bolder, larger, or more dynamic for highlighting key moments, calls to action, and editorial emphasis:

| Role | Baseline | Emphasized |
|------|----------|------------|
| Display Large | 57px / 400 | 57px / 700 |
| Display Medium | 45px / 400 | 45px / 700 |
| Display Small | 36px / 400 | 36px / 700 |
| Headline Large | 32px / 400 | 32px / 700 |
| Headline Medium | 28px / 400 | 28px / 700 |
| Headline Small | 24px / 400 | 24px / 600 |
| Title Large | 22px / 400 | 22px / 700 |
| Title Medium | 16px / 500 | 16px / 700 |
| Title Small | 14px / 500 | 14px / 700 |
| Body Large | 16px / 400 | 16px / 700 |
| Body Medium | 14px / 400 | 14px / 700 |
| Body Small | 12px / 400 | 12px / 700 |
| Label Large | 14px / 500 | 14px / 800 |
| Label Medium | 12px / 500 | 12px / 800 |
| Label Small | 11px / 500 | 11px / 800 |

**When to use emphasized styles**:
- Calls to action and primary buttons with strong visual weight
- Important headlines or numbers that users should notice immediately
- Editorial emphasis in content layouts
- Key data points in dashboards or summaries
- Onboarding screens and feature highlights

**Pairing baseline and emphasized**:
- Use emphasized sparingly alongside baseline styles to create rhythm and momentum
- Never use all emphasized styles on a single screen — the contrast between baseline and emphasized is what creates hierarchy

### Medium Contrast (M3 Expressive Default)

M3 Expressive introduces "medium contrast" as the default typography approach:
- Balances legibility with visual flair
- More accessible than low-contrast approaches while more expressive than high-contrast
- Ensures expressive type choices remain highly accessible across device types
- Achieved through careful weight/size pairing in the baseline vs emphasized type scale

## Font Recommendations

### System Fonts

**Roboto** (Default for M3):
- Versatile, highly readable
- Available in variable font format
- Weights: 100-900
- Use for both display and body text

**Roboto Flex** (Variable font):
- Supports width and weight axes
- Ideal for M3 Expressive
- Enables dynamic adjustments

### Brand Fonts

Consider these characteristics when choosing brand fonts:

**Display Fonts**:
- Distinctive personality
- High readability at large sizes
- Consider: Poppins, Montserrat, Work Sans, DM Sans

**Body Fonts**:
- Excellent readability at small sizes
- Good for long-form content
- Consider: Inter, Open Sans, Source Sans Pro, Noto Sans

### Variable Font Implementation

```css
@font-face {
  font-family: 'Roboto Flex';
  src: url('RobotoFlex-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-stretch: 75% 125%;
}

.dynamic-text {
  font-family: 'Roboto Flex', sans-serif;
  font-variation-settings: 
    'wght' 400,
    'wdth' 100;
}
```

## Implementation Guidelines

### CSS Type Tokens

Define typography tokens using CSS custom properties. M3 Expressive adds emphasized variants alongside baseline:

```css
:root {
  /* Font families */
  --md-sys-typescale-font-family-brand: 'Roboto', sans-serif;
  --md-sys-typescale-font-family-plain: 'Roboto', sans-serif;
  
  /* Display Large — Baseline */
  --md-sys-typescale-display-large-font: var(--md-sys-typescale-font-family-brand);
  --md-sys-typescale-display-large-size: 3.562rem;
  --md-sys-typescale-display-large-line-height: 4rem;
  --md-sys-typescale-display-large-weight: 400;
  --md-sys-typescale-display-large-tracking: -0.25px;
  
  /* Display Large — Emphasized (M3 Expressive) */
  --md-sys-typescale-display-large-emphasized-weight: 700;
  
  /* Headline Large — Baseline */
  --md-sys-typescale-headline-large-font: var(--md-sys-typescale-font-family-brand);
  --md-sys-typescale-headline-large-size: 2rem;
  --md-sys-typescale-headline-large-line-height: 2.5rem;
  --md-sys-typescale-headline-large-weight: 400;
  --md-sys-typescale-headline-large-tracking: 0;
  
  /* Headline Large — Emphasized (M3 Expressive) */
  --md-sys-typescale-headline-large-emphasized-weight: 700;
  
  /* Body Large — Baseline */
  --md-sys-typescale-body-large-font: var(--md-sys-typescale-font-family-plain);
  --md-sys-typescale-body-large-size: 1rem;
  --md-sys-typescale-body-large-line-height: 1.5rem;
  --md-sys-typescale-body-large-weight: 400;
  --md-sys-typescale-body-large-tracking: 0.5px;
  
  /* Body Large — Emphasized (M3 Expressive) */
  --md-sys-typescale-body-large-emphasized-weight: 700;
  
  /* Label Large — Baseline */
  --md-sys-typescale-label-large-font: var(--md-sys-typescale-font-family-plain);
  --md-sys-typescale-label-large-size: 0.875rem;
  --md-sys-typescale-label-large-line-height: 1.25rem;
  --md-sys-typescale-label-large-weight: 500;
  --md-sys-typescale-label-large-tracking: 0.1px;
  
  /* Label Large — Emphasized (M3 Expressive) */
  --md-sys-typescale-label-large-emphasized-weight: 800;
}
```

### Type Classes

Create reusable type classes for both baseline and emphasized styles:

```css
/* Baseline styles */
.display-large {
  font-family: var(--md-sys-typescale-display-large-font);
  font-size: var(--md-sys-typescale-display-large-size);
  line-height: var(--md-sys-typescale-display-large-line-height);
  font-weight: var(--md-sys-typescale-display-large-weight);
  letter-spacing: var(--md-sys-typescale-display-large-tracking);
}

.headline-large {
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  line-height: var(--md-sys-typescale-headline-large-line-height);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  letter-spacing: var(--md-sys-typescale-headline-large-tracking);
}

.body-large {
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  font-weight: var(--md-sys-typescale-body-large-weight);
  letter-spacing: var(--md-sys-typescale-body-large-tracking);
}

/* Emphasized styles (M3 Expressive) */
.display-large-emphasized {
  font-family: var(--md-sys-typescale-display-large-font);
  font-size: var(--md-sys-typescale-display-large-size);
  line-height: var(--md-sys-typescale-display-large-line-height);
  font-weight: var(--md-sys-typescale-display-large-emphasized-weight);
  letter-spacing: var(--md-sys-typescale-display-large-tracking);
}

.headline-large-emphasized {
  font-family: var(--md-sys-typescale-headline-large-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  line-height: var(--md-sys-typescale-headline-large-line-height);
  font-weight: var(--md-sys-typescale-headline-large-emphasized-weight);
  letter-spacing: var(--md-sys-typescale-headline-large-tracking);
}

.body-large-emphasized {
  font-family: var(--md-sys-typescale-body-large-font);
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  font-weight: var(--md-sys-typescale-body-large-emphasized-weight);
  letter-spacing: var(--md-sys-typescale-body-large-tracking);
}

.label-large-emphasized {
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  letter-spacing: var(--md-sys-typescale-label-large-tracking);
}
```

## Typography Best Practices

### Hierarchy

1. **Use the Scale**: Don't create custom sizes—use the defined scale
2. **Skip Levels Sparingly**: Can skip one level, but maintain clear hierarchy
3. **Consistent Application**: Same content type should use same style
4. **Color for Emphasis**: Use color roles for text (on-surface, on-primary, etc.)

### Readability

1. **Line Length**: 50-75 characters per line for body text
2. **Line Height**: 1.4-1.6 for body text (already built into scale)
3. **Contrast**: Minimum 4.5:1 for body text, 3:1 for large text
4. **Text Color**: Use semantic color tokens (on-surface, on-background)

### Responsive Typography

```css
/* Mobile-first base sizes */
:root {
  --fluid-display-large: clamp(2.5rem, 5vw + 1rem, 3.562rem);
  --fluid-headline-large: clamp(1.5rem, 3vw + 0.5rem, 2rem);
}

.display-large {
  font-size: var(--fluid-display-large);
}

/* Or use container queries for component-level responsiveness */
@container (min-width: 600px) {
  .card-title {
    font-size: var(--md-sys-typescale-title-large-size);
  }
}
```

### Accessibility

1. **Zoom Support**: Use relative units (rem, em) for all sizes
2. **Clear Hierarchy**: Visual hierarchy should be clear without color
3. **Focus States**: Ensure text links have visible focus indicators
4. **Screen Readers**: Use semantic HTML (h1-h6, p, etc.)

### Performance

1. **Font Loading**: Use `font-display: swap` to prevent text blocking
2. **Subset Fonts**: Load only needed characters and weights
3. **Variable Fonts**: Use single variable font file instead of multiple weights
4. **System Fonts**: Consider system font stack for performance

```css
@font-face {
  font-family: 'Roboto';
  src: url('roboto.woff2') format('woff2');
  font-display: swap;
  /* Subset to Latin characters */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}
```

## Advanced Typography

### Expressive Text Effects

**Variable Font Animations**:
```css
@keyframes weight-shift {
  from { font-variation-settings: 'wght' 300; }
  to { font-variation-settings: 'wght' 700; }
}

.animated-heading {
  animation: weight-shift 2s ease-in-out infinite alternate;
}
```

**Gradient Text**:
```css
.gradient-headline {
  background: linear-gradient(
    90deg,
    var(--md-sys-color-primary),
    var(--md-sys-color-tertiary)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Text Truncation

```css
/* Single line truncation */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Multi-line truncation */
.truncate-multi {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

## Common Type Patterns

### Card Title and Body
```html
<div class="card">
  <h3 class="title-large">Card Title</h3>
  <p class="body-medium">Card description text goes here.</p>
</div>
```

### Page Header with Subheader
```html
<header>
  <h1 class="headline-large">Page Title</h1>
  <p class="body-large">Supporting description or subtitle</p>
</header>
```

### Button Text
```html
<button class="label-large">Action</button>
```

### List Item
```html
<li>
  <span class="title-medium">List Item Title</span>
  <span class="body-small">Supporting text</span>
</li>
```

## Checklist for Typography Implementation

When implementing M3 typography, ensure:

- [ ] All 15 baseline type styles from the scale are defined as CSS tokens
- [ ] All 15 emphasized type styles are defined (M3 Expressive)
- [ ] Roboto or appropriate brand font is loaded
- [ ] Variable fonts are used when available
- [ ] Font display swap is set to prevent blocking
- [ ] All text uses semantic color tokens
- [ ] Proper hierarchy is established (display > headline > title > body)
- [ ] Emphasized styles are used sparingly for key moments and calls to action
- [ ] Line height and letter spacing match the specification
- [ ] Responsive scaling is implemented for different screen sizes
- [ ] Relative units (rem/em) are used for all sizes
- [ ] Text contrast meets WCAG requirements (4.5:1 minimum)
- [ ] Font weights are used consistently (400 baseline, 500 labels, 700+ emphasized)
- [ ] Semantic HTML tags match visual hierarchy
- [ ] Long-form content has appropriate line length (50-75 characters)
- [ ] All text is readable at default and zoomed sizes
- [ ] Performance is optimized (font subsetting, loading strategy)
- [ ] Medium contrast approach is followed for balance of legibility and expression

## Resources

- `examples/type-scale.html` — Interactive HTML example showing the complete M3 type scale (display, headline, title, body, label) with correct sizes, weights, and line heights. Open in a browser to preview the hierarchy.
- M3 typography overview: https://m3.material.io/styles/typography/overview
- Material Design Tokens (typography): https://github.com/material-foundation/material-tokens
- Google Fonts: https://fonts.google.com/
