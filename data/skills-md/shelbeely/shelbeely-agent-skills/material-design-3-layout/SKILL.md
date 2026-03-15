---
name: material-design-3-layout
description: Applies Material Design 3 Expressive layout, spacing, and size hierarchy principles including grid systems, responsive design, and elevation. Use this when working on page layouts, spacing, grids, responsive design, or when the user asks to apply Material Design 3 layout guidelines.
license: Apache-2.0
---

# Material Design 3 Layout and Size Hierarchy

## Overview

This skill guides the implementation of Material Design 3 (M3) Expressive layout and spacing principles to create clear, organized, and responsive interfaces.

**Keywords**: Material Design 3, M3, layout, spacing, grid, responsive design, breakpoints, size hierarchy, elevation, padding, margin

## Core Principles

### Layout Philosophy

M3 layout — from Material You foundations to M3 Expressive — focuses on:

1. **Clear Hierarchy**: Size and spacing create visual importance
2. **Responsive Adaptability**: Layouts work across all screen sizes
3. **Strategic Spacing**: Consistent spacing creates rhythm and flow
4. **Size-Based Emphasis**: Larger elements naturally draw attention
5. **Elevation Depth**: Layered surfaces show relationships
6. **Explicit and Implicit Containment**: Visual grouping through both borders and proximity
7. **Background Blur and Layering**: Depth effects that guide focus (M3 Expressive)

## Spacing Scale System

M3 uses a consistent 4dp spacing scale for all layout spacing:

### Base Scale (Increments of 4dp)

```css
:root {
  /* Spacing scale */
  --md-sys-spacing-0: 0px;
  --md-sys-spacing-1: 4px;
  --md-sys-spacing-2: 8px;
  --md-sys-spacing-3: 12px;
  --md-sys-spacing-4: 16px;
  --md-sys-spacing-5: 20px;
  --md-sys-spacing-6: 24px;
  --md-sys-spacing-7: 28px;
  --md-sys-spacing-8: 32px;
  --md-sys-spacing-9: 36px;
  --md-sys-spacing-10: 40px;
  --md-sys-spacing-12: 48px;
  --md-sys-spacing-14: 56px;
  --md-sys-spacing-16: 64px;
  --md-sys-spacing-20: 80px;
  --md-sys-spacing-24: 96px;
}
```

### Semantic Spacing

Define semantic spacing for common patterns:

```css
:root {
  /* Component spacing */
  --md-sys-spacing-component-gap: var(--md-sys-spacing-2); /* 8px */
  --md-sys-spacing-component-padding: var(--md-sys-spacing-4); /* 16px */
  
  /* Layout spacing */
  --md-sys-spacing-section-gap: var(--md-sys-spacing-6); /* 24px */
  --md-sys-spacing-page-margin: var(--md-sys-spacing-4); /* 16px */
  
  /* List spacing */
  --md-sys-spacing-list-item-gap: var(--md-sys-spacing-2); /* 8px */
  --md-sys-spacing-list-padding: var(--md-sys-spacing-4); /* 16px */
}
```

## Responsive Grid System

### Breakpoints

M3 defines standard breakpoints for responsive design:

```css
:root {
  /* Breakpoints */
  --md-sys-breakpoint-xs: 0px;      /* Extra small (phones) */
  --md-sys-breakpoint-sm: 600px;    /* Small (tablets portrait) */
  --md-sys-breakpoint-md: 905px;    /* Medium (tablets landscape) */
  --md-sys-breakpoint-lg: 1240px;   /* Large (laptops) */
  --md-sys-breakpoint-xl: 1440px;   /* Extra large (desktops) */
}
```

### Grid Columns

**Mobile (0-599px)**:
- Columns: 4
- Margin: 16px
- Gutter: 16px

**Tablet (600-904px)**:
- Columns: 8
- Margin: 24px
- Gutter: 24px

**Desktop (905px+)**:
- Columns: 12
- Margin: 24px
- Gutter: 24px

### CSS Grid Implementation

```css
.layout-grid {
  display: grid;
  gap: var(--md-sys-spacing-4);
  padding: var(--md-sys-spacing-4);
  
  /* Mobile: 4 columns */
  grid-template-columns: repeat(4, 1fr);
}

@media (min-width: 600px) {
  .layout-grid {
    gap: var(--md-sys-spacing-6);
    padding: var(--md-sys-spacing-6);
    /* Tablet: 8 columns */
    grid-template-columns: repeat(8, 1fr);
  }
}

@media (min-width: 905px) {
  .layout-grid {
    /* Desktop: 12 columns */
    grid-template-columns: repeat(12, 1fr);
  }
}
```

## Component Spacing

### Buttons

**Padding**:
- Horizontal: 24px
- Vertical: 10px
- Minimum height: 40px
- Gap between icon and text: 8px

```css
.button {
  padding: var(--md-sys-spacing-2) var(--md-sys-spacing-6);
  min-height: 40px;
  gap: var(--md-sys-spacing-2);
}
```

### Cards

**Padding**:
- Standard: 16px all sides
- Large cards: 24px all sides
- Compact: 12px all sides

**Spacing between elements**:
- Header to content: 8px
- Content to actions: 16px
- Between actions: 8px

```css
.card {
  padding: var(--md-sys-spacing-4);
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-2);
}

.card-actions {
  margin-top: var(--md-sys-spacing-4);
  display: flex;
  gap: var(--md-sys-spacing-2);
}
```

### Dialogs

**Padding**:
- All sides: 24px
- Content padding: 16px
- Title to content: 16px
- Content to actions: 24px

**Sizing**:
- Min width: 280px
- Max width: 560px
- Mobile: Full width with margin

```css
.dialog {
  padding: var(--md-sys-spacing-6);
  min-width: 280px;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-4);
}

@media (max-width: 599px) {
  .dialog {
    width: calc(100% - 32px);
    margin: var(--md-sys-spacing-4);
  }
}
```

### Lists

**Spacing**:
- Between list items: 0px (items touch)
- Item padding: 16px horizontal, 8px vertical
- Icon to text: 16px
- Text to secondary action: 16px

```css
.list-item {
  padding: var(--md-sys-spacing-2) var(--md-sys-spacing-4);
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-4);
  min-height: 56px;
}
```

### Navigation

**App Bar**:
- Height: 64px (desktop), 56px (mobile)
- Padding: 16px horizontal
- Gap between items: 24px

**Navigation Rail**:
- Width: 80px
- Item height: 56px
- Item spacing: 4px

**Bottom Navigation**:
- Height: 80px
- Item width: Equal distribution
- Icon to label: 4px

```css
.app-bar {
  height: 56px;
  padding: 0 var(--md-sys-spacing-4);
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-6);
}

@media (min-width: 600px) {
  .app-bar {
    height: 64px;
  }
}
```

## Size Hierarchy

### Use Size for Emphasis

M3 Expressive uses size strategically to create visual hierarchy:

**Hero Elements** (Largest):
- 2-3x larger than standard
- Use for main call-to-action or featured content
- Limited to 1-2 per view

**Primary Elements** (Large):
- 1.5x larger than standard
- Main content, featured items
- 3-5 per view

**Standard Elements** (Base):
- Default size for most content
- Maintains readability and usability

**Secondary Elements** (Small):
- 0.75x of standard
- Supporting information, metadata
- Can be numerous

**Tertiary Elements** (Smallest):
- 0.5x of standard
- Timestamps, captions, fine print
- Use sparingly

### Size Examples

```css
/* Hero button */
.button-hero {
  padding: var(--md-sys-spacing-4) var(--md-sys-spacing-10);
  min-height: 56px;
  font-size: 18px;
}

/* Standard button */
.button-standard {
  padding: var(--md-sys-spacing-2) var(--md-sys-spacing-6);
  min-height: 40px;
  font-size: 14px;
}

/* Small button */
.button-small {
  padding: var(--md-sys-spacing-1) var(--md-sys-spacing-4);
  min-height: 32px;
  font-size: 12px;
}
```

## Elevation System

M3 uses elevation to show depth and hierarchy:

### Elevation Levels

**Level 0** (On surface):
- No shadow
- Background elements

**Level 1** (Slight elevation):
- Shadow: `0 1px 2px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.15)`
- Cards, list items
- Use: 1dp

**Level 2** (Elevated):
- Shadow: `0 2px 4px rgba(0,0,0,0.3), 0 3px 4px rgba(0,0,0,0.15)`
- Raised buttons, FABs at rest
- Use: 3dp

**Level 3** (Floating):
- Shadow: `0 4px 8px rgba(0,0,0,0.3), 0 6px 8px rgba(0,0,0,0.15)`
- FABs on hover, app bars
- Use: 6dp

**Level 4** (Modal):
- Shadow: `0 8px 12px rgba(0,0,0,0.3), 0 12px 16px rgba(0,0,0,0.15)`
- Dialogs, navigation drawer
- Use: 8dp

**Level 5** (High modal):
- Shadow: `0 12px 16px rgba(0,0,0,0.3), 0 16px 24px rgba(0,0,0,0.15)`
- Modal bottom sheets
- Use: 12dp

### Elevation Tokens

```css
:root {
  --md-sys-elevation-0: none;
  --md-sys-elevation-1: 0 1px 2px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.15);
  --md-sys-elevation-2: 0 2px 4px rgba(0,0,0,0.3), 0 3px 4px rgba(0,0,0,0.15);
  --md-sys-elevation-3: 0 4px 8px rgba(0,0,0,0.3), 0 6px 8px rgba(0,0,0,0.15);
  --md-sys-elevation-4: 0 8px 12px rgba(0,0,0,0.3), 0 12px 16px rgba(0,0,0,0.15);
  --md-sys-elevation-5: 0 12px 16px rgba(0,0,0,0.3), 0 16px 24px rgba(0,0,0,0.15);
}
```

### Elevation with Tinting

M3 adds a subtle color tint to elevated surfaces:

```css
.elevated-surface {
  background-color: var(--md-sys-color-surface);
  box-shadow: var(--md-sys-elevation-1);
  /* Add subtle tint using primary color */
  background-image: linear-gradient(
    rgba(var(--md-sys-color-primary-rgb), 0.05),
    rgba(var(--md-sys-color-primary-rgb), 0.05)
  );
}
```

## Responsive Layout Patterns

### Mobile-First Approach

Start with mobile layout, then enhance for larger screens:

```css
/* Mobile: Stack vertically */
.content-layout {
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-4);
  padding: var(--md-sys-spacing-4);
}

/* Tablet: Two columns */
@media (min-width: 600px) {
  .content-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--md-sys-spacing-6);
    padding: var(--md-sys-spacing-6);
  }
}

/* Desktop: Three columns with sidebar */
@media (min-width: 905px) {
  .content-layout {
    grid-template-columns: 250px 1fr 1fr;
  }
}
```

### Container Queries

Use for component-level responsiveness:

```css
.card-container {
  container-type: inline-size;
}

.card {
  display: flex;
  flex-direction: column;
}

@container (min-width: 400px) {
  .card {
    flex-direction: row;
    gap: var(--md-sys-spacing-4);
  }
}
```

### Common Layout Patterns

**Centered Content**:
```css
.centered-layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--md-sys-spacing-6);
}
```

**Sidebar Layout**:
```css
.sidebar-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: var(--md-sys-spacing-6);
}

@media (max-width: 904px) {
  .sidebar-layout {
    grid-template-columns: 1fr;
  }
}
```

**Dashboard Grid**:
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--md-sys-spacing-4);
}
```

## Containment Principles

### Explicit Containment

Use visible boundaries to group related content:

```css
/* Card containment with outline */
.contained-group {
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-medium);
  padding: var(--md-sys-spacing-4);
  background: var(--md-sys-color-surface-container);
}

/* Elevated containment */
.elevated-group {
  box-shadow: var(--md-sys-elevation-1);
  border-radius: var(--md-sys-shape-corner-medium);
  padding: var(--md-sys-spacing-4);
  background: var(--md-sys-color-surface-container-low);
}
```

### Implicit Containment

Use proximity, open space, and alignment to group items without visible borders:

```css
/* Implicit grouping through proximity */
.implicit-group {
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-1); /* Tight spacing implies grouping */
}

/* Separated groups use larger spacing */
.section-gap {
  margin-bottom: var(--md-sys-spacing-8); /* Larger gap separates groups */
}
```

### When to Use Each

| Containment Type | Use When |
|------------------|----------|
| Explicit (borders/cards) | Interactive content, distinct sections, actionable groups |
| Explicit (elevation) | Content that needs to feel "lifted" or modal |
| Implicit (proximity) | Related text blocks, label-value pairs, sequential content |
| Implicit (alignment) | Grid layouts, navigation items, consistent structure |

## Background Blur and Depth Effects

M3 Expressive introduces background blur and layering for improved depth and focus:

### Background Blur

Strategic blur behind overlays, modals, and navigation elements:

```css
/* Blur behind modal dialogs */
.dialog-backdrop {
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background-color: rgba(0, 0, 0, 0.32);
}

/* Blur behind floating toolbars */
.floating-toolbar {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  background-color: rgba(var(--md-sys-color-surface-rgb), 0.85);
}

/* Blur behind navigation drawers */
.nav-drawer-scrim {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  background-color: var(--md-sys-color-scrim);
  opacity: 0.32;
}
```

### When to Use Blur

1. **Behind modals and dialogs**: Creates focus on foreground content
2. **Behind floating toolbars**: Separates toolbar from content without heavy elevation
3. **Behind navigation drawers**: Softens the transition between drawer and content
4. **Behind bottom sheets**: Creates depth without fully obscuring content
5. **Never on content itself**: Blur is for scrims and backgrounds, not readable content

### Depth Layering

Combine elevation, blur, and surface tinting for clear layering:

```css
/* Layer 1: Base content */
.base-layer {
  background: var(--md-sys-color-surface);
}

/* Layer 2: Elevated content */
.elevated-layer {
  background: var(--md-sys-color-surface-container);
  box-shadow: var(--md-sys-elevation-1);
}

/* Layer 3: Overlay with blur */
.overlay-layer {
  backdrop-filter: blur(16px);
  background: rgba(var(--md-sys-color-surface-container-high-rgb), 0.9);
  box-shadow: var(--md-sys-elevation-3);
}
```

## Interaction States

M3 defines consistent interaction states for all interactive elements:

### State Layer System

State layers are overlays using the content color at specific opacities:

| State | Opacity | Description |
|-------|---------|-------------|
| Enabled | 0% | Default, no overlay |
| Hovered | 8% | Pointer device hover |
| Focused | 12% | Keyboard/accessibility focus |
| Pressed | 12% | Touch/click press |
| Dragged | 16% | Active drag operation |
| Disabled | 0% | Non-interactive (content at 38%, background at 12%) |

```css
/* State layer implementation */
.interactive-element {
  position: relative;
}

.interactive-element::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: var(--md-sys-color-on-surface);
  opacity: 0;
  transition: opacity 200ms var(--md-sys-motion-easing-standard);
  pointer-events: none;
}

.interactive-element:hover::before { opacity: 0.08; }
.interactive-element:focus-visible::before { opacity: 0.12; }
.interactive-element:active::before { opacity: 0.12; }

/* Disabled state */
.interactive-element:disabled {
  opacity: 0.38;
  pointer-events: none;
}

.interactive-element:disabled::before {
  opacity: 0;
}
```

### State Priority

Only one state layer is visually applied at a time. Priority order:
1. Dragged (highest)
2. Pressed
3. Focused
4. Hovered
5. Enabled (lowest)

## Touch Targets and Accessibility

### Minimum Touch Target Size

All interactive elements must be at least 48×48dp:

```css
.touch-target {
  min-width: 48px;
  min-height: 48px;
  /* Visual size can be smaller with padding */
  padding: var(--md-sys-spacing-3);
}
```

### Focus Indicators

Ensure adequate spacing for focus rings:

```css
.focusable {
  position: relative;
}

.focusable:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
```

## Best Practices

### Do's

1. ✅ Use the 4dp spacing scale consistently
2. ✅ Define semantic spacing tokens for common patterns
3. ✅ Start mobile-first, then enhance for larger screens
4. ✅ Use size hierarchy to create visual emphasis
5. ✅ Maintain minimum 48×48dp touch targets
6. ✅ Use elevation to show component relationships
7. ✅ Test layouts at all breakpoints
8. ✅ Use CSS Grid and Flexbox for modern layouts

### Don'ts

1. ❌ Don't use arbitrary spacing values (stick to the scale)
2. ❌ Don't make layouts that only work on desktop
3. ❌ Don't use tiny touch targets on mobile
4. ❌ Don't overuse elevation (creates visual noise)
5. ❌ Don't ignore container queries for components
6. ❌ Don't create fixed-width layouts without max-width
7. ❌ Don't forget horizontal scrolling on mobile

## Performance Considerations

1. **Use CSS Grid/Flexbox**: Avoid float-based layouts
2. **Minimize Layout Shifts**: Define dimensions to prevent CLS
3. **Optimize Images**: Use responsive images with srcset
4. **Lazy Load**: Defer off-screen content
5. **Container Queries**: Better than media queries for components

## Checklist for Layout Implementation

When implementing M3 layout, ensure:

- [ ] Spacing scale is defined (4dp increments)
- [ ] Semantic spacing tokens are created
- [ ] Breakpoints are defined (600px, 905px, 1240px)
- [ ] Mobile-first responsive approach is used
- [ ] Grid system supports 4/8/12 columns
- [ ] Touch targets are minimum 48×48dp
- [ ] Elevation system is defined (5 levels)
- [ ] Size hierarchy is used for emphasis
- [ ] All spacing uses tokens (no hard-coded values)
- [ ] Layouts work on all screen sizes
- [ ] Focus indicators have adequate spacing
- [ ] Container queries are used for components
- [ ] Maximum content width is set for readability
- [ ] Elevation tinting is applied to raised surfaces
- [ ] Containment principles are applied (explicit and implicit grouping)
- [ ] Background blur is used for modals, drawers, and floating elements
- [ ] Interaction states are implemented with correct opacity values
- [ ] Disabled states use 38% content opacity and 12% background opacity
- [ ] State layers use on-surface color at appropriate opacities
- [ ] Performance is optimized (Grid/Flexbox, lazy loading)

## Resources

- M3 layout overview: https://m3.material.io/foundations/layout/understanding-layout/overview
- Material Design Tokens: https://github.com/material-foundation/material-tokens
