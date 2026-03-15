---
name: material-design-3-shape
description: Applies Material Design 3 Expressive shape and containment principles including rounded corners, morphing shapes, and container design. Use this when working on component shapes, borders, containment, or when the user asks to apply Material Design 3 shape guidelines.
license: Apache-2.0
---

# Material Design 3 Shape and Containment

## Overview

This skill guides the implementation of Material Design 3 (M3) Expressive shape and containment principles to create friendly, approachable, and visually distinct interfaces.

**Keywords**: Material Design 3, M3, shape, rounded corners, border radius, containment, containers, morphing shapes, component shapes

## Core Principles

### Shape Philosophy

M3 Expressive uses shape to:

1. **Create Personality**: Distinctive shapes make interfaces memorable and approachable
2. **Establish Hierarchy**: Different corner radii indicate importance and containment levels
3. **Express Brand**: Shape language can be customized to match brand identity
4. **Guide Attention**: Rounded corners naturally draw the eye and feel inviting
5. **Support Interaction**: Shape morphing provides visual feedback

### Shape Characteristics

**Rounded Corners** (Primary characteristic):
- M3 favors rounded corners over sharp angles
- Corners create a friendly, modern aesthetic
- Different radii for different component types

**Morphing Shapes**:
- Shapes can transform dynamically between states
- Corner radius can animate smoothly
- Supports expressive interactions

**Asymmetry** (When appropriate):
- Not all corners need the same radius
- Strategic asymmetry adds interest
- Use sparingly for special emphasis

## Shape Scale System

M3 Expressive defines an updated shape scale with semantic naming and expanded corner radius tokens:

### Shape Families

**None** (0dp):
- Full-bleed surfaces
- App backgrounds
- No rounding needed

**Extra Small** (4dp):
- Small buttons
- Chips
- Badges
- Input fields

**Small** (8dp):
- Text buttons
- Outlined buttons
- Small cards

**Medium** (12dp):
- Standard buttons
- Cards
- Bottom sheets

**Large** (20dp — updated from 16dp):
- Large cards
- Featured content
- FABs (Floating Action Buttons)

**Extra Large** (32dp — updated from 28dp):
- Hero cards
- Featured images
- Special containers
- Dialogs

**Extra Extra Large** (48dp — new in M3 Expressive):
- Modal sheets
- Full-screen overlays
- Major hero elements

**Full** (100% of corner radius — now defined as 100% rather than 50%):
- Pills
- Circular buttons
- Profile avatars
- Fully rounded elements

### Shape Tokens

Define shape tokens using CSS custom properties:

```css
:root {
  /* Corner radii — updated for M3 Expressive */
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 20px;
  --md-sys-shape-corner-extra-large: 32px;
  --md-sys-shape-corner-extra-extra-large: 48px;
  --md-sys-shape-corner-full: 9999px;
  
  /* Component-specific shapes */
  --md-sys-shape-button: var(--md-sys-shape-corner-full);
  --md-sys-shape-card: var(--md-sys-shape-corner-medium);
  --md-sys-shape-dialog: var(--md-sys-shape-corner-extra-large);
  --md-sys-shape-fab: var(--md-sys-shape-corner-large);
  --md-sys-shape-chip: var(--md-sys-shape-corner-small);
  --md-sys-shape-text-field: var(--md-sys-shape-corner-extra-small);
  --md-sys-shape-bottom-sheet: var(--md-sys-shape-corner-extra-extra-large);
}
```

## Expressive Shape Library

M3 Expressive introduces a library of 35 decorative and functional shapes that go beyond simple rounded rectangles. These shapes can be applied to components, backgrounds, and decorative elements, and they support smooth morphing between one another.

### Complete Shape Catalog

**Geometric Shapes**:
- Circle, Square, Slanted Square, Oval, Pill, Semi Circle, Triangle, Diamond, Pentagon, Gem, Arch

**Organic and Playful Shapes**:
- Flower, Puffy, Puffy Diamond, Clover 4, Clover 8, Bun, Heart, Ghostish, Clam Shell

**Burst and Star Shapes**:
- Sunny, Very Sunny, Burst, Soft Burst, Boom, Soft Boom, Fan, Arrow

**Cookie Shapes** (scalloped edges):
- Cookie 4, Cookie 6, Cookie 7, Cookie 9, Cookie 12

**Pixel Shapes**:
- Pixel Circle, Pixel Triangle

### When to Use Expressive Shapes

1. **Moments of Delight**: Use decorative shapes to create visual surprise (loading states, celebrations, onboarding)
2. **Brand Expression**: Choose shapes that reflect brand personality
3. **State Feedback**: Morph shapes to communicate state changes (e.g., a circle morphing into a burst on completion)
4. **Visual Tension**: Combine sharp and rounded, symmetrical and asymmetrical forms for dynamic interest
5. **Sparingly for Clarity**: Abstract shapes (Burst, Puffy, Flower) should be used for emphasis — not as primary containers for content

### CSS Implementation of Expressive Shapes

```css
/* Using clip-path for expressive shapes */
.shape-flower {
  clip-path: polygon(
    50% 0%, 61% 11%, 75% 0%, 80% 15%,
    100% 15%, 90% 30%, 100% 50%, 85% 55%,
    100% 75%, 80% 75%, 75% 100%, 61% 85%,
    50% 100%, 39% 85%, 25% 100%, 20% 75%,
    0% 75%, 15% 55%, 0% 50%, 10% 30%,
    0% 15%, 20% 15%, 25% 0%, 39% 11%
  );
}

/* Using border-radius for organic shapes */
.shape-bun {
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
}

/* Heart shape */
.shape-heart {
  clip-path: path('M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z');
}
```

## Component Shape Guidelines

### Buttons

**Filled Buttons**:
- Border radius: Full (50%)
- Completely rounded ends
- Standard height: 40dp

```css
.button-filled {
  border-radius: var(--md-sys-shape-corner-full);
  padding: 10px 24px;
  height: 40px;
}
```

**Outlined Buttons**:
- Border radius: Full (50%)
- Same as filled buttons
- 1px outline

**Text Buttons**:
- Border radius: Full (50%)
- No background until hover
- Slightly less padding

**FABs** (Floating Action Buttons):
- Medium FAB: 40×40dp, 12dp radius (replaces deprecated Small FAB)
- Regular FAB: 56×56dp, 20dp radius
- Large FAB: 96×96dp, 32dp radius

### Cards

**Standard Cards**:
- Border radius: 12dp (medium)
- Consistent on all corners
- Elevation with shadow

```css
.card {
  border-radius: var(--md-sys-shape-corner-medium);
  padding: 16px;
  background: var(--md-sys-color-surface);
}
```

**Elevated Cards**:
- Same radius as standard
- Additional elevation (shadow)

**Outlined Cards**:
- 1px outline instead of elevation
- Same corner radius

### Dialogs and Sheets

**Dialogs**:
- Border radius: 32dp (extra-large — updated from 28dp)
- Creates distinctive, modern appearance
- Centered on screen

```css
.dialog {
  border-radius: var(--md-sys-shape-corner-extra-large);
  padding: 24px;
  max-width: 560px;
}
```

**Bottom Sheets**:
- Top corners: 48dp (extra-extra-large — new)
- Bottom corners: 0dp (none)
- Slides up from bottom

```css
.bottom-sheet {
  border-radius: var(--md-sys-shape-corner-extra-extra-large) 
                 var(--md-sys-shape-corner-extra-extra-large) 
                 0 0;
}
```

**Side Sheets**:
- Leading corners: 32dp
- Trailing corners: 0dp

### Input Fields

**Text Fields** (Filled):
- Top corners: 4dp (extra-small)
- Bottom corners: 0dp
- Creates input well appearance

```css
.text-field-filled {
  border-radius: var(--md-sys-shape-corner-extra-small)
                 var(--md-sys-shape-corner-extra-small)
                 0 0;
  background: var(--md-sys-color-surface-variant);
}
```

**Text Fields** (Outlined):
- All corners: 4dp
- Consistent roundness

```css
.text-field-outlined {
  border-radius: var(--md-sys-shape-corner-extra-small);
  border: 1px solid var(--md-sys-color-outline);
}
```

### Chips

**Input Chips**:
- Border radius: 8dp (small)
- With or without leading icon

**Filter Chips**:
- Border radius: 8dp (small)
- Toggle selection state

**Suggestion Chips**:
- Border radius: 8dp (small)
- Single action

```css
.chip {
  border-radius: var(--md-sys-shape-corner-small);
  padding: 6px 12px;
  height: 32px;
}
```

## Containment Principles

### Container Hierarchy

**Level 0** (Backgrounds):
- No border radius or minimal (0-4dp)
- Full-screen surfaces
- App background

**Level 1** (Primary containers):
- 12dp radius
- Cards, list items
- Primary content areas

**Level 2** (Secondary containers):
- 12-16dp radius
- Nested cards
- Grouped content

**Level 3** (Tertiary containers):
- 16-28dp radius
- Dialogs, modals
- Overlay content

### Grouped Components

When grouping multiple components:

**Adjacent Buttons**:
- Maintain individual radii or
- Merge into single container with shared radius

**Segmented Buttons**:
- First: rounded on left, square on right
- Middle: square on both sides
- Last: square on left, rounded on right

```css
.segmented-button:first-child {
  border-radius: var(--md-sys-shape-corner-full) 0 0 var(--md-sys-shape-corner-full);
}

.segmented-button:last-child {
  border-radius: 0 var(--md-sys-shape-corner-full) var(--md-sys-shape-corner-full) 0;
}

.segmented-button:not(:first-child):not(:last-child) {
  border-radius: 0;
}
```

**Toolbars and App Bars**:
- Top app bar: 0dp (or small radius on bottom)
- Bottom app bar: 0dp (or small radius on top)
- FAB can extend beyond app bar

## Morphing Shapes

### State Transitions

Shapes can morph between states to show relationships:

**Button Press**:
```css
.button {
  border-radius: var(--md-sys-shape-corner-full);
  transition: border-radius 200ms cubic-bezier(0.2, 0, 0, 1);
}

.button:active {
  border-radius: var(--md-sys-shape-corner-medium);
}
```

**Container Expansion**:
```css
.card {
  border-radius: var(--md-sys-shape-corner-medium);
  transition: border-radius 300ms cubic-bezier(0.2, 0, 0, 1);
}

.card.expanded {
  border-radius: var(--md-sys-shape-corner-extra-large);
}
```

**Shape Transform**:
```css
/* FAB morphing into sheet */
.fab-to-sheet {
  transition: 
    border-radius 400ms cubic-bezier(0.2, 0, 0, 1),
    width 400ms cubic-bezier(0.2, 0, 0, 1),
    height 400ms cubic-bezier(0.2, 0, 0, 1);
}

.fab-to-sheet.expanded {
  border-radius: var(--md-sys-shape-corner-extra-extra-large);
  width: 100%;
  height: 400px;
}
```

### Expressive Shape Morphing

M3 Expressive supports smooth morphing between any of the 35 expressive shapes. This creates moments of delight and communicates state changes visually:

**Loading State Morph**:
```css
/* Circle morphing to burst on completion */
.loading-indicator {
  clip-path: circle(50%);
  transition: clip-path 400ms cubic-bezier(0.05, 0.7, 0.1, 1.0);
}

.loading-indicator.complete {
  clip-path: polygon(/* burst shape coordinates */);
}
```

**Interactive Shape Feedback**:
```javascript
// Using Web Animations API for shape morphing
element.animate([
  { clipPath: 'circle(50%)' },
  { clipPath: 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)' }
], {
  duration: 400,
  easing: 'cubic-bezier(0.05, 0.7, 0.1, 1.0)',
  fill: 'forwards'
});
```

**Guidelines for Expressive Shape Morphing**:
1. Use morphing to connect user actions with interface feedback
2. Shapes should not carry literal meanings — they add aesthetic variety and direct attention
3. Combine sharp and rounded forms for dynamic visual tension
4. Use abstract shapes sparingly to preserve clarity and usability
5. Pair shape morphing with the M3 motion physics system for natural-feeling transitions

## Advanced Shape Techniques

### Asymmetric Shapes

Use for special emphasis:

```css
.asymmetric-card {
  border-radius: 28px 12px 28px 12px;
}
```

### Custom Shapes

Beyond circles and rounded rectangles:

**Cutout Shapes**:
```css
.cutout-card {
  border-radius: var(--md-sys-shape-corner-large);
  clip-path: polygon(
    0 0, 
    calc(100% - 40px) 0, 
    100% 40px, 
    100% 100%, 
    0 100%
  );
}
```

**Notched Shapes** (for special components):
```css
.notched-container {
  border-radius: var(--md-sys-shape-corner-medium);
  position: relative;
}

.notched-container::before {
  content: '';
  position: absolute;
  top: -8px;
  right: 20px;
  width: 16px;
  height: 16px;
  background: var(--md-sys-color-surface);
  transform: rotate(45deg);
}
```

### Responsive Shapes

Adjust shape based on screen size:

```css
.card {
  border-radius: var(--md-sys-shape-corner-small);
}

@media (min-width: 600px) {
  .card {
    border-radius: var(--md-sys-shape-corner-medium);
  }
}

@media (min-width: 1024px) {
  .card {
    border-radius: var(--md-sys-shape-corner-large);
  }
}
```

## Best Practices

### Do's

1. ✅ Use semantic shape tokens (not hard-coded values)
2. ✅ Maintain consistency across similar components
3. ✅ Adjust radius based on component size (larger = more radius)
4. ✅ Animate shape transitions smoothly
5. ✅ Consider touch targets (min 48×48dp)
6. ✅ Use full radius for pill-shaped buttons
7. ✅ Apply larger radius to overlay content (dialogs, sheets)

### Don'ts

1. ❌ Don't mix sharp corners with rounded in same component family
2. ❌ Don't use too many different radii (stick to scale)
3. ❌ Don't make tiny components with huge radii
4. ❌ Don't forget to adjust padding with border radius
5. ❌ Don't use square corners unless specifically needed
6. ❌ Don't ignore the shape scale system
7. ❌ Don't animate border-radius without performance consideration

## Accessibility Considerations

### Touch Targets

Ensure interactive elements meet minimum size:

```css
.touch-target {
  min-width: 48px;
  min-height: 48px;
  border-radius: var(--md-sys-shape-corner-full);
}
```

### Focus Indicators

Shape should not obscure focus:

```css
.button:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
  border-radius: var(--md-sys-shape-corner-full);
}
```

### High Contrast

Ensure shape is visible:
- Use borders or outlines in high contrast mode
- Don't rely solely on subtle shadows

## Performance

### Optimization

1. Use `border-radius` for simple rounded corners (GPU accelerated)
2. Use `clip-path` sparingly (can be expensive)
3. Animate shape changes with `will-change` for complex morphs
4. Avoid animating `border-radius` on many elements simultaneously

```css
/* Optimize complex shape animations */
.morphing-container {
  will-change: border-radius;
}

.morphing-container.settled {
  will-change: auto;
}
```

## Checklist for Shape Implementation

When implementing M3 shape system, ensure:

- [ ] All shape tokens are defined (extra-small through extra-extra-large and full)
- [ ] Updated corner radius values are used (Large: 20dp, XL: 32dp, XXL: 48dp)
- [ ] Semantic shape tokens used (not hard-coded px values)
- [ ] Buttons use full radius (pill shape)
- [ ] Cards use medium radius (12dp)
- [ ] Dialogs use extra-large radius (32dp)
- [ ] Bottom sheets use extra-extra-large top radius (48dp)
- [ ] Input fields use extra-small radius (4dp)
- [ ] Chips use small radius (8dp)
- [ ] FABs use appropriate radius for size (Medium: 12dp, Regular: 20dp, Large: 32dp)
- [ ] Grouped components handle shared edges correctly
- [ ] Shape transitions are smooth and spring-based
- [ ] Expressive shapes from the 35-shape library are used for moments of delight
- [ ] Expressive shape morphing is applied for state feedback when appropriate
- [ ] Touch targets meet 48×48dp minimum
- [ ] Focus indicators respect rounded shapes
- [ ] Performance is optimized (GPU acceleration)
- [ ] Responsive adjustments for different screen sizes

## Resources

- `examples/shape-corners.svg` — Visual reference SVG showing the complete M3 shape system: corner radius scale (None → Full), corner styles (rounded, cut, squircle, asymmetric), expressive shape library samples, and component shape mapping. Based on https://m3.material.io/styles/shape/overview-principles.
- M3 shape overview: https://m3.material.io/styles/shape/overview
- Material Design Tokens (shape): https://github.com/material-foundation/material-tokens
