---
name: google-material-design
description: Design interfaces following Google's Material Design system, the unified visual language bridging digital and physical worlds. Emphasizes bold graphic design, intentional motion, adaptive layouts, and the material metaphor. Use when building modern, accessible, delightful user interfaces across platforms.
tags: material-design, ui, ux, design-system, components, animation, accessibility, responsive, mobile, web, visual
---

# Google Material Design⁠‍⁠​‌​‌​​‌‌‍​‌​​‌​‌‌‍​​‌‌​​​‌‍​‌​​‌‌​​‍​​​​​​​‌‍‌​​‌‌​‌​‍‌​​​​​​​‍‌‌​​‌‌‌‌‍‌‌​​​‌​​‍‌‌‌‌‌‌​‌‍‌‌​‌​​​​‍​‌​‌‌‌‌‌‍​‌​​‌​‌‌‍​‌‌​‌​​‌‍‌​‌​‌‌‌​‍​​‌​‌​​​‍‌‌‌​‌​‌‌‍‌​‌‌​​‌​‍‌​​‌​​​​‍​​​​​​‌​‍​​‌‌‌​​‌‍​​​​‌​​‌‍‌‌‌​​‌‌‌⁠‍⁠

## Overview

Material Design is Google's open-source design system that bridges the gap between the physical and digital worlds. Introduced in 2014 and evolved through Material Design 2 (2018) and Material Design 3 (2021), it provides a comprehensive framework for building beautiful, functional, and accessible interfaces across all platforms.

## References

- **Guidelines**: https://m3.material.io/
- **Foundations**: https://m3.material.io/foundations
- **Components**: https://m3.material.io/components
- **Theming**: https://m3.material.io/styles
- **GitHub**: https://github.com/material-components

## Core Philosophy

> "Material is the metaphor."

> "Bold, graphic, intentional."

> "Motion provides meaning."

> "Adaptive design, delightful experiences."

Material Design creates a visual language that synthesizes classic principles of good design with the innovation and possibility of technology and science.

## The Material Metaphor

### Physical World Inspiration

```
┌─────────────────────────────────────────────────────────┐
│  MATERIAL = DIGITAL PAPER + INK + PHYSICAL PROPERTIES   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐     Light                                  │
│  │ Surface │ ◄── casts shadows                          │
│  │  (z=2)  │     based on elevation                     │
│  └─────────┘                                            │
│       │                                                 │
│       │ Elevation                                       │
│       ▼                                                 │
│  ╔═════════════════════════════════════════════════╗   │
│  ║              Ground Plane (z=0)                 ║   │
│  ╚═════════════════════════════════════════════════╝   │
│                                                         │
│  • Surfaces exist in 3D space with depth               │
│  • Material has physical properties and affordances    │
│  • Shadows communicate spatial relationships           │
│  • Content is printed on material, not within it       │
└─────────────────────────────────────────────────────────┘
```

### Elevation System

```
Elevation (dp)    Component Examples           Shadow Intensity
─────────────────────────────────────────────────────────────
    0dp           Background, disabled         None
    1dp           Card (resting), Search bar   Subtle
    2dp           Card (raised), Button        Light
    3dp           Refresh indicator            Light-Medium
    4dp           App Bar                      Medium
    6dp           FAB (resting), Snackbar      Medium
    8dp           Bottom sheet, Menu           Pronounced
   12dp           FAB (pressed), Dialog        Strong
   16dp           Nav drawer                   Strong
   24dp           Modal bottom sheet           Maximum
```

## Design Principles

### 1. Material is the Metaphor

```css
/* Material surfaces have consistent properties */
.surface {
  /* Surfaces are opaque and cast shadows */
  background: var(--md-sys-color-surface);
  
  /* Elevation creates depth */
  box-shadow: var(--md-sys-elevation-level2);
  
  /* Corners define character */
  border-radius: var(--md-sys-shape-corner-medium);
}

/* Content rests ON material, not inside it */
.content-on-surface {
  /* Ink metaphor - content is printed on surface */
  color: var(--md-sys-color-on-surface);
}
```

### 2. Bold, Graphic, Intentional

```
Typography Hierarchy (Material 3)
═══════════════════════════════════════════════════════════

Display Large    57sp    Headlines for hero moments
Display Medium   45sp    Large display text
Display Small    36sp    Smaller display text
─────────────────────────────────────────────────────────
Headline Large   32sp    High-emphasis text
Headline Medium  28sp    Medium emphasis headers
Headline Small   24sp    Smaller headlines
─────────────────────────────────────────────────────────
Title Large      22sp    Prominent titles
Title Medium     16sp    Medium titles
Title Small      14sp    Smaller titles, tabs
─────────────────────────────────────────────────────────
Label Large      14sp    Buttons, prominent labels
Label Medium     12sp    Navigation labels
Label Small      11sp    Timestamps, hints
─────────────────────────────────────────────────────────
Body Large       16sp    Primary body text
Body Medium      14sp    Secondary body text
Body Small       12sp    Captions, annotations
```

### 3. Motion Provides Meaning

```javascript
// motion_principles.js
// Motion in Material Design is choreographed and meaningful

const MaterialMotion = {
  // Duration tokens (Material 3)
  duration: {
    short1: 50,    // Micro-interactions
    short2: 100,   // Simple selections
    short3: 150,   // Checkbox, switch
    short4: 200,   // Small expand/collapse
    medium1: 250,  // Standard enter/exit
    medium2: 300,  // Card expand
    medium3: 350,  // Complex animations
    medium4: 400,  // Page transitions
    long1: 450,    // Large area transitions
    long2: 500,    // Complex choreography
    long3: 550,    // Elaborate animations
    long4: 600,    // Maximum duration
  },
  
  // Easing curves
  easing: {
    // Emphasized - for prominent elements
    emphasized: 'cubic-bezier(0.2, 0.0, 0, 1.0)',
    emphasizedDecelerate: 'cubic-bezier(0.05, 0.7, 0.1, 1.0)',
    emphasizedAccelerate: 'cubic-bezier(0.3, 0.0, 0.8, 0.15)',
    
    // Standard - for most transitions
    standard: 'cubic-bezier(0.2, 0.0, 0, 1.0)',
    standardDecelerate: 'cubic-bezier(0, 0, 0, 1)',
    standardAccelerate: 'cubic-bezier(0.3, 0, 1, 1)',
  },
  
  // Transition patterns
  patterns: {
    // Container transform - element becomes new screen
    containerTransform: {
      use: 'Element expands into a new screen',
      duration: 'medium2',
      easing: 'emphasized',
    },
    
    // Shared axis - elements share spatial relationship
    sharedAxis: {
      use: 'Navigation between related destinations',
      duration: 'medium1',
      easing: 'emphasized',
    },
    
    // Fade through - unrelated content transition
    fadeThrough: {
      use: 'Switching between unrelated content',
      duration: 'medium1',
      easing: 'emphasized',
    },
    
    // Fade - simple appearance/disappearance
    fade: {
      use: 'UI elements appearing or disappearing',
      duration: 'short4',
      easing: 'standard',
    },
  },
};

// Example: Container transform animation
function containerTransform(element, options) {
  const { duration, easing } = MaterialMotion.patterns.containerTransform;
  
  return element.animate([
    { transform: 'scale(0.85)', opacity: 0 },
    { transform: 'scale(1)', opacity: 1 },
  ], {
    duration: MaterialMotion.duration[duration],
    easing: MaterialMotion.easing[easing],
    fill: 'forwards',
  });
}
```

## Color System (Material 3 Dynamic Color)

### Tonal Palettes

```
Source Color → Tonal Palette → Color Scheme
═══════════════════════════════════════════════════════════

Primary Source (#6750A4)
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Tonal Palette: Primary                                  │
│ ─────────────────────────────────────────────────────── │
│ 0    10   20   30   40   50   60   70   80   90   95 100│
│ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ ▓▓▓▓ ████ ████ ░░░░ ░░░░ ░░░░ ░░░░ ░░░░ │
│ Darkest ◄─────────────────────────────────► Lightest   │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Light Scheme:               Dark Scheme:
  primary: tone40             primary: tone80
  onPrimary: tone100          onPrimary: tone20
  primaryContainer: tone90    primaryContainer: tone30
  onPrimaryContainer: tone10  onPrimaryContainer: tone90
```

### Color Roles

```css
/* Material 3 Color Tokens */
:root {
  /* Primary - Key color, brand identity */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  
  /* Secondary - Supporting color */
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-on-secondary-container: #1D192B;
  
  /* Tertiary - Accent, contrast */
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #FFD8E4;
  --md-sys-color-on-tertiary-container: #31111D;
  
  /* Error - Alerts and errors */
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #F9DEDC;
  --md-sys-color-on-error-container: #410E0B;
  
  /* Surface - Backgrounds */
  --md-sys-color-surface: #FFFBFE;
  --md-sys-color-on-surface: #1C1B1F;
  --md-sys-color-surface-variant: #E7E0EC;
  --md-sys-color-on-surface-variant: #49454F;
  
  /* Outline - Borders, dividers */
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;
}
```

### Dynamic Color from Content

```javascript
// dynamic_color.js
// Extract color scheme from images or user preference

class MaterialColorScheme {
  constructor(sourceColor) {
    this.source = sourceColor;
    this.palette = this.generateTonalPalette(sourceColor);
  }
  
  generateTonalPalette(color) {
    // HCT (Hue, Chroma, Tone) color space for perceptual uniformity
    const hct = rgbToHct(color);
    
    return {
      0: hctToRgb({ ...hct, tone: 0 }),
      10: hctToRgb({ ...hct, tone: 10 }),
      20: hctToRgb({ ...hct, tone: 20 }),
      30: hctToRgb({ ...hct, tone: 30 }),
      40: hctToRgb({ ...hct, tone: 40 }),
      50: hctToRgb({ ...hct, tone: 50 }),
      60: hctToRgb({ ...hct, tone: 60 }),
      70: hctToRgb({ ...hct, tone: 70 }),
      80: hctToRgb({ ...hct, tone: 80 }),
      90: hctToRgb({ ...hct, tone: 90 }),
      95: hctToRgb({ ...hct, tone: 95 }),
      99: hctToRgb({ ...hct, tone: 99 }),
      100: hctToRgb({ ...hct, tone: 100 }),
    };
  }
  
  getLightScheme() {
    return {
      primary: this.palette[40],
      onPrimary: this.palette[100],
      primaryContainer: this.palette[90],
      onPrimaryContainer: this.palette[10],
      // ... remaining roles
    };
  }
  
  getDarkScheme() {
    return {
      primary: this.palette[80],
      onPrimary: this.palette[20],
      primaryContainer: this.palette[30],
      onPrimaryContainer: this.palette[90],
      // ... remaining roles
    };
  }
}
```

## Component Architecture

### Anatomy of a Material Component

```
┌─────────────────────────────────────────────────────────┐
│                    BUTTON ANATOMY                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    ┌─────────────────────────────────────────┐         │
│    │  [Icon]  Label Text                     │         │
│    └─────────────────────────────────────────┘         │
│    │         │                               │         │
│    │         │                               │         │
│    │    Leading Icon (optional)              │         │
│    │                                         │         │
│    │    Label text (required)           Container      │
│    │                                    (required)     │
│    │                                         │         │
│    └─────────────────────────────────────────┘         │
│                                                         │
│    States: Enabled, Disabled, Hovered,                 │
│            Focused, Pressed                            │
└─────────────────────────────────────────────────────────┘
```

### Button Variants

```tsx
// MaterialButton.tsx
// Material 3 button implementations

interface ButtonProps {
  variant: 'elevated' | 'filled' | 'tonal' | 'outlined' | 'text';
  icon?: React.ReactNode;
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: () => void;
}

// Elevated - For secondary actions requiring emphasis
const ElevatedButton = styled.button`
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-primary);
  box-shadow: var(--md-sys-elevation-level1);
  border: none;
  border-radius: 20px;
  padding: 10px 24px;
  font: var(--md-sys-typescale-label-large);
  
  &:hover {
    box-shadow: var(--md-sys-elevation-level2);
    background: color-mix(
      in srgb,
      var(--md-sys-color-primary) 8%,
      var(--md-sys-color-surface-container-low)
    );
  }
  
  &:focus-visible {
    outline: none;
    box-shadow: var(--md-sys-elevation-level1);
    background: color-mix(
      in srgb,
      var(--md-sys-color-primary) 12%,
      var(--md-sys-color-surface-container-low)
    );
  }
  
  &:active {
    box-shadow: var(--md-sys-elevation-level1);
    background: color-mix(
      in srgb,
      var(--md-sys-color-primary) 12%,
      var(--md-sys-color-surface-container-low)
    );
  }
`;

// Filled - For primary actions, high emphasis
const FilledButton = styled.button`
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  border-radius: 20px;
  padding: 10px 24px;
  
  &:hover {
    box-shadow: var(--md-sys-elevation-level1);
    background: color-mix(
      in srgb,
      var(--md-sys-color-on-primary) 8%,
      var(--md-sys-color-primary)
    );
  }
`;

// Tonal - For secondary actions, medium emphasis
const TonalButton = styled.button`
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  border: none;
  border-radius: 20px;
  padding: 10px 24px;
`;

// Outlined - For secondary actions, low emphasis
const OutlinedButton = styled.button`
  background: transparent;
  color: var(--md-sys-color-primary);
  border: 1px solid var(--md-sys-color-outline);
  border-radius: 20px;
  padding: 10px 24px;
`;

// Text - For lowest emphasis actions
const TextButton = styled.button`
  background: transparent;
  color: var(--md-sys-color-primary);
  border: none;
  border-radius: 20px;
  padding: 10px 12px;
`;
```

### State Layer System

```css
/* Material 3 State Layer Implementation */

.interactive-element {
  position: relative;
  overflow: hidden;
}

/* State layer overlay */
.interactive-element::before {
  content: '';
  position: absolute;
  inset: 0;
  background: currentColor;
  opacity: 0;
  transition: opacity 150ms var(--md-sys-motion-easing-standard);
}

/* State layer opacities */
.interactive-element:hover::before {
  opacity: 0.08;  /* Hover state */
}

.interactive-element:focus-visible::before {
  opacity: 0.12;  /* Focus state */
}

.interactive-element:active::before {
  opacity: 0.12;  /* Pressed state */
}

.interactive-element[data-dragged]::before {
  opacity: 0.16;  /* Dragged state */
}

/* Disabled states - no state layer, reduced opacity */
.interactive-element:disabled {
  opacity: 0.38;
  pointer-events: none;
}

.interactive-element:disabled::before {
  display: none;
}
```

## Shape System

### Corner Styles

```
Shape Scale (Material 3)
═══════════════════════════════════════════════════════════

None (0dp)        Extra Small (4dp)    Small (8dp)
┌──────────┐      ╭──────────╮        ╭──────────╮
│          │      │          │        │          │
│          │      │          │        │          │
│          │      │          │        │          │
└──────────┘      ╰──────────╯        ╰──────────╯

Medium (12dp)     Large (16dp)        Extra Large (28dp)
╭──────────╮      ╭──────────╮        ╭──────────╮
│          │      │          │        │          │
│          │      │          │        │          │
│          │      │          │        │          │
╰──────────╯      ╰──────────╯        ╰──────────╯

Full (50%)
    ╭────╮
   │      │
   │      │
    ╰────╯
```

```css
/* Shape tokens */
:root {
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-full: 9999px;
}

/* Shape application by component */
.chip { border-radius: var(--md-sys-shape-corner-small); }
.card { border-radius: var(--md-sys-shape-corner-medium); }
.dialog { border-radius: var(--md-sys-shape-corner-extra-large); }
.fab { border-radius: var(--md-sys-shape-corner-large); }
.button { border-radius: var(--md-sys-shape-corner-full); }
```

## Adaptive Layouts

### Responsive Grid System

```
Window Size Classes
═══════════════════════════════════════════════════════════

Compact (< 600dp)     Medium (600-839dp)   Expanded (840dp+)
┌─────────────┐       ┌────────────────┐   ┌───────────────────┐
│             │       │                │   │ Nav │             │
│   Content   │       │    Content     │   │ Bar │   Content   │
│             │       │                │   │     │             │
│             │       │                │   │     │             │
├─────────────┤       │                │   │     │             │
│  Nav Bar    │       ├────────────────┤   │     │             │
└─────────────┘       │    Nav Bar     │   │     │             │
                      └────────────────┘   └───────────────────┘
4 columns             8 columns (body)     12 columns (body)
16dp margins          24dp margins         24dp margins
8dp gutters           16dp gutters         24dp gutters
```

### Layout Implementation

```tsx
// AdaptiveLayout.tsx
// Material 3 adaptive scaffold

import { useWindowSize } from './hooks';

type WindowSizeClass = 'compact' | 'medium' | 'expanded' | 'large' | 'extraLarge';

function getWindowSizeClass(width: number): WindowSizeClass {
  if (width < 600) return 'compact';
  if (width < 840) return 'medium';
  if (width < 1200) return 'expanded';
  if (width < 1600) return 'large';
  return 'extraLarge';
}

interface AdaptiveLayoutProps {
  navigation: React.ReactNode;
  content: React.ReactNode;
  detail?: React.ReactNode;
}

export function AdaptiveLayout({ navigation, content, detail }: AdaptiveLayoutProps) {
  const { width } = useWindowSize();
  const sizeClass = getWindowSizeClass(width);
  
  // Compact: Bottom navigation bar
  if (sizeClass === 'compact') {
    return (
      <div className="layout-compact">
        <main className="content">{content}</main>
        <nav className="navigation-bar">{navigation}</nav>
      </div>
    );
  }
  
  // Medium: Navigation rail
  if (sizeClass === 'medium') {
    return (
      <div className="layout-medium">
        <nav className="navigation-rail">{navigation}</nav>
        <main className="content">{content}</main>
      </div>
    );
  }
  
  // Expanded+: Navigation drawer with optional detail pane
  return (
    <div className="layout-expanded">
      <nav className="navigation-drawer">{navigation}</nav>
      <main className="content">{content}</main>
      {detail && sizeClass !== 'expanded' && (
        <aside className="detail-pane">{detail}</aside>
      )}
    </div>
  );
}
```

### Navigation Patterns

```
Navigation Components by Screen Size
═══════════════════════════════════════════════════════════

           Compact         Medium          Expanded
           ─────────────────────────────────────────────
Primary    Bottom Bar      Rail            Drawer
           3-5 items       3-7 items       Full labels

Secondary  Modal Drawer    Modal Drawer    Persistent Drawer

Tertiary   Tabs           Tabs            Tabs
           Bottom Sheet   Side Sheet      Side Sheet
```

## Accessibility (A11y)

### Touch Targets

```css
/* Minimum touch target: 48x48dp */
.touch-target {
  min-width: 48px;
  min-height: 48px;
  
  /* Visual element can be smaller, but touch area must be 48dp */
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-button {
  /* Icon is 24dp, but touch target is 48dp */
  width: 48px;
  height: 48px;
  padding: 12px;
}

.icon-button svg {
  width: 24px;
  height: 24px;
}
```

### Color Contrast

```
Contrast Requirements (WCAG 2.1)
═══════════════════════════════════════════════════════════

Text Size        Minimum (AA)    Enhanced (AAA)
─────────────────────────────────────────────────
Normal text      4.5:1           7:1
Large text       3:1             4.5:1
(18sp+ or 14sp bold)

UI Components    3:1             Not defined
(borders, icons)

Material Design ensures:
• on-primary meets 4.5:1 against primary
• on-surface meets 4.5:1 against surface
• All semantic color pairs are accessible
```

### Focus Indicators

```css
/* Material 3 focus indicators */
.focusable {
  outline: none;
  position: relative;
}

.focusable:focus-visible {
  /* Focus ring using secondary color */
  outline: 3px solid var(--md-sys-color-secondary);
  outline-offset: 2px;
}

/* Alternative: Focus indicator within element */
.button:focus-visible {
  outline: none;
}

.button:focus-visible::after {
  content: '';
  position: absolute;
  inset: -4px;
  border: 3px solid var(--md-sys-color-secondary);
  border-radius: inherit;
  pointer-events: none;
}
```

## When Implementing

### Always

- Use the design token system for colors, typography, and shape
- Implement all interactive states (enabled, disabled, hover, focus, pressed)
- Ensure 48dp minimum touch targets
- Provide visible focus indicators
- Use semantic color roles (primary, secondary, error) not raw values
- Apply elevation system for spatial hierarchy
- Include meaningful motion for state changes

### Never

- Hard-code color values instead of tokens
- Ignore disabled states
- Create custom colors outside the tonal palette
- Skip focus states for keyboard users
- Use elevation without purpose
- Add motion that doesn't convey meaning
- Violate touch target minimums

### Prefer

- Filled buttons for primary actions, text buttons for tertiary
- Tonal palette for consistent, harmonious colors
- Standard easing for most transitions
- Surface color variants over opacity for overlays
- Component library over custom implementations
- Adaptive layouts over fixed breakpoints

## Mental Model

Material Design asks:

1. **Is it material?** Does it behave like a physical surface with depth?
2. **Is it intentional?** Does every element serve a clear purpose?
3. **Is it meaningful?** Does motion communicate state and guide attention?
4. **Is it accessible?** Can everyone use it regardless of ability?
5. **Is it adaptive?** Does it work across all screen sizes and devices?
6. **Is it delightful?** Does it create a positive emotional response?

## Signature Material Moves

- **Dynamic Color**: Personalized themes from user content
- **Tonal Palettes**: Harmonious color derived from single source
- **State Layers**: Consistent interaction feedback via overlays
- **Container Transform**: Seamless element-to-screen transitions
- **Elevation Hierarchy**: Shadows that communicate importance
- **Adaptive Scaffolds**: Navigation that transforms with screen size
- **Typography Scale**: 15 styles for clear content hierarchy
- **Shape System**: Corners that communicate component personality
