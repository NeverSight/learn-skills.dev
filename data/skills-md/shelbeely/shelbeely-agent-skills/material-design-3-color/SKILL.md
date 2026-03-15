---
name: material-design-3-color
description: Applies Material Design 3 Expressive dynamic color and theming principles to user interfaces. Use this when working on color palettes, themes, dynamic color systems, accessibility, or when the user asks to apply Material Design 3 color guidelines to a design or application.
license: Apache-2.0
---

# Material Design 3 Color and Dynamic Theming

## Overview

This skill guides the application of Material Design 3 (M3) Expressive color and theming principles to create vibrant, accessible, and emotionally engaging user interfaces.

**Keywords**: Material Design 3, M3, dynamic color, theming, color palette, Material You, accessibility, color tokens, surface colors, accent colors, fixed accent colors, emphasis colors, contrast levels

## Core Principles

### Dynamic Color System

Material Design 3's color system is built on the concept of dynamic color, allowing interfaces to adapt to user preferences and contexts:

1. **Tonal Palettes**: Use five key tonal palettes (Primary, Secondary, Tertiary, Neutral, Neutral Variant) with multiple tones (0-100)
2. **Color Roles**: Map 26+ color roles to UI elements (e.g., primary, onPrimary, primaryContainer, onPrimaryContainer)
3. **Adaptive Theming**: Support both light and dark themes with appropriate contrast
4. **User Personalization**: Allow color schemes to adapt based on user wallpaper or preferences (Material You)
5. **Fixed Accent Colors**: Provide color tokens that remain consistent across light and dark themes for brand identity
6. **Emphasis Colors**: Use bolder, more vibrant color roles for key UI elements to improve clarity and emotional resonance

### Color Palette Structure

When creating color palettes, follow this structure:

**Primary Palette** (Main brand color):
- Primary: Main interactive elements (buttons, active states)
- On Primary: Text/icons on primary color
- Primary Container: Standout fill color for key components
- On Primary Container: Text/icons on primary container
- Primary Fixed: Stays constant across light and dark themes
- On Primary Fixed: Text/icons on primary fixed
- Primary Fixed Dim: Dimmed variant for secondary emphasis on fixed surfaces

**Secondary Palette** (Complementary accent):
- Secondary: Less prominent components
- On Secondary: Text/icons on secondary
- Secondary Container: Tinted backgrounds
- On Secondary Container: Text/icons on secondary container
- Secondary Fixed: Stays constant across light and dark themes
- On Secondary Fixed: Text/icons on secondary fixed
- Secondary Fixed Dim: Dimmed variant for fixed surfaces

**Tertiary Palette** (Contrasting accent — now a prominent expressive accent for branding and highlights):
- Tertiary: Contrasting accents and highlights
- On Tertiary: Text/icons on tertiary
- Tertiary Container: Input elements
- On Tertiary Container: Text/icons on tertiary container
- Tertiary Fixed: Stays constant across light and dark themes
- On Tertiary Fixed: Text/icons on tertiary fixed
- Tertiary Fixed Dim: Dimmed variant for fixed surfaces

**Neutral Palettes** (Surfaces and backgrounds):
- Surface: Default background for components
- On Surface: Text on surface
- Surface Variant: Alternate surface color
- On Surface Variant: Text on surface variant
- Surface Dim: Dimmed surface for reduced emphasis
- Surface Bright: Brighter surface for increased emphasis
- Surface Container Lowest: Lowest-emphasis container surface
- Surface Container Low: Low-emphasis container surface
- Surface Container: Default container surface
- Surface Container High: High-emphasis container surface
- Surface Container Highest: Highest-emphasis container surface
- Outline: Borders and dividers
- Outline Variant: Decorative elements
- Inverse Surface: Inverted surface for contrast elements (e.g., snackbars)
- Inverse On Surface: Text on inverse surface
- Inverse Primary: Primary color used on inverse surfaces

**Error/Warning/Success** (Feedback colors):
- Error, Warning, Success with corresponding "On" colors and containers

### Accessibility Guidelines

1. **Contrast Levels** (M3 Expressive standardizes three levels):
   - **Standard**: Default contrast suitable for most users
   - **Medium**: Enhanced contrast for improved readability
   - **High**: Maximum contrast for users with low vision or high-contrast preferences
   - All three levels are tokenized for easy implementation

2. **Contrast Requirements**:
   - Text contrast: Minimum 4.5:1 for body text, 3:1 for large text (WCAG AA)
   - Interactive elements: Minimum 3:1 contrast with background
   - Use "On" colors to ensure proper contrast

3. **Color Independence**:
   - Never rely solely on color to convey information
   - Use icons, text labels, or patterns alongside color
   - Ensure color-blind friendly combinations

4. **Dynamic Range**:
   - Light theme: Higher tones (90-99) for surfaces, lower tones (10-40) for emphasis
   - Dark theme: Lower tones (10-20) for surfaces, higher tones (80-90) for emphasis

## Implementation Guidelines

### Color Token System

Use CSS custom properties (variables) for all colors. M3 Expressive introduces 26+ color roles:

```css
:root {
  /* Primary */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  
  /* Primary Fixed (consistent across themes) */
  --md-sys-color-primary-fixed: #EADDFF;
  --md-sys-color-on-primary-fixed: #21005D;
  --md-sys-color-primary-fixed-dim: #D0BCFF;
  --md-sys-color-on-primary-fixed-variant: #4F378B;
  
  /* Secondary */
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-on-secondary-container: #1D192B;
  
  /* Secondary Fixed */
  --md-sys-color-secondary-fixed: #E8DEF8;
  --md-sys-color-on-secondary-fixed: #1D192B;
  --md-sys-color-secondary-fixed-dim: #CCC2DC;
  --md-sys-color-on-secondary-fixed-variant: #4A4458;
  
  /* Tertiary */
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #FFD8E4;
  --md-sys-color-on-tertiary-container: #31111D;
  
  /* Tertiary Fixed */
  --md-sys-color-tertiary-fixed: #FFD8E4;
  --md-sys-color-on-tertiary-fixed: #31111D;
  --md-sys-color-tertiary-fixed-dim: #EFB8C8;
  --md-sys-color-on-tertiary-fixed-variant: #633B48;
  
  /* Surface and Surface Containers */
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-on-surface: #1D1B20;
  --md-sys-color-surface-variant: #E7E0EC;
  --md-sys-color-on-surface-variant: #49454F;
  --md-sys-color-surface-dim: #DED8E1;
  --md-sys-color-surface-bright: #FEF7FF;
  --md-sys-color-surface-container-lowest: #FFFFFF;
  --md-sys-color-surface-container-low: #F7F2FA;
  --md-sys-color-surface-container: #F3EDF7;
  --md-sys-color-surface-container-high: #ECE6F0;
  --md-sys-color-surface-container-highest: #E6E0E9;
  
  /* Inverse */
  --md-sys-color-inverse-surface: #322F35;
  --md-sys-color-inverse-on-surface: #F5EFF7;
  --md-sys-color-inverse-primary: #D0BCFF;
  
  /* Outlines */
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;
  
  /* Error */
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #F9DEDC;
  --md-sys-color-on-error-container: #410E0B;
  
  /* Scrim and Shadow */
  --md-sys-color-scrim: #000000;
  --md-sys-color-shadow: #000000;
}

[data-theme="dark"] {
  /* Primary */
  --md-sys-color-primary: #D0BCFF;
  --md-sys-color-on-primary: #381E72;
  --md-sys-color-primary-container: #4F378B;
  --md-sys-color-on-primary-container: #EADDFF;
  
  /* Primary Fixed (same as light — these don't change) */
  --md-sys-color-primary-fixed: #EADDFF;
  --md-sys-color-on-primary-fixed: #21005D;
  --md-sys-color-primary-fixed-dim: #D0BCFF;
  --md-sys-color-on-primary-fixed-variant: #4F378B;
  
  /* Secondary */
  --md-sys-color-secondary: #CCC2DC;
  --md-sys-color-on-secondary: #332D41;
  --md-sys-color-secondary-container: #4A4458;
  --md-sys-color-on-secondary-container: #E8DEF8;
  
  /* Secondary Fixed (same as light) */
  --md-sys-color-secondary-fixed: #E8DEF8;
  --md-sys-color-on-secondary-fixed: #1D192B;
  --md-sys-color-secondary-fixed-dim: #CCC2DC;
  --md-sys-color-on-secondary-fixed-variant: #4A4458;
  
  /* Tertiary */
  --md-sys-color-tertiary: #EFB8C8;
  --md-sys-color-on-tertiary: #492532;
  --md-sys-color-tertiary-container: #633B48;
  --md-sys-color-on-tertiary-container: #FFD8E4;
  
  /* Tertiary Fixed (same as light) */
  --md-sys-color-tertiary-fixed: #FFD8E4;
  --md-sys-color-on-tertiary-fixed: #31111D;
  --md-sys-color-tertiary-fixed-dim: #EFB8C8;
  --md-sys-color-on-tertiary-fixed-variant: #633B48;
  
  /* Surface and Surface Containers */
  --md-sys-color-surface: #141218;
  --md-sys-color-on-surface: #E6E0E9;
  --md-sys-color-surface-variant: #49454F;
  --md-sys-color-on-surface-variant: #CAC4D0;
  --md-sys-color-surface-dim: #141218;
  --md-sys-color-surface-bright: #3B383E;
  --md-sys-color-surface-container-lowest: #0F0D13;
  --md-sys-color-surface-container-low: #1D1B20;
  --md-sys-color-surface-container: #211F26;
  --md-sys-color-surface-container-high: #2B2930;
  --md-sys-color-surface-container-highest: #36343B;
  
  /* Inverse */
  --md-sys-color-inverse-surface: #E6E0E9;
  --md-sys-color-inverse-on-surface: #322F35;
  --md-sys-color-inverse-primary: #6750A4;
  
  /* Outlines */
  --md-sys-color-outline: #938F99;
  --md-sys-color-outline-variant: #49454F;
  
  /* Error */
  --md-sys-color-error: #F2B8B5;
  --md-sys-color-on-error: #601410;
  --md-sys-color-error-container: #8C1D18;
  --md-sys-color-on-error-container: #F9DEDC;
  
  /* Scrim and Shadow */
  --md-sys-color-scrim: #000000;
  --md-sys-color-shadow: #000000;
}
```

### Fixed Accent Colors

Fixed accent colors are new in M3 Expressive. They maintain the same value across light and dark themes, useful for brand identity elements:

```css
/* Fixed colors remain identical in both themes */
.brand-banner {
  background-color: var(--md-sys-color-primary-fixed);
  color: var(--md-sys-color-on-primary-fixed);
}

.brand-accent {
  background-color: var(--md-sys-color-tertiary-fixed);
  color: var(--md-sys-color-on-tertiary-fixed);
}

/* Fixed Dim for secondary emphasis on fixed surfaces */
.brand-banner-secondary {
  background-color: var(--md-sys-color-primary-fixed-dim);
  color: var(--md-sys-color-on-primary-fixed);
}
```

### Contrast Level System

M3 Expressive standardizes three contrast levels for accessibility:

```css
/* Standard contrast (default) */
:root {
  --md-sys-color-contrast-level: 0;
}

/* Medium contrast */
[data-contrast="medium"] {
  --md-sys-color-primary: #5640A0;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #7B68BA;
  --md-sys-color-on-primary-container: #FFFFFF;
}

/* High contrast */
[data-contrast="high"] {
  --md-sys-color-primary: #2D0F6E;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #4E3A87;
  --md-sys-color-on-primary-container: #FFFFFF;
}
```

### Color Application

1. **Interactive Elements**:
   - Filled buttons: Use primary color with on-primary text
   - Outlined buttons: Use outline with primary text
   - Text buttons: Use primary text only
   - FABs: Use primary-container with on-primary-container
   - Button Groups: Use surface-container with on-surface text

2. **Surfaces and Containers**:
   - Main background: surface
   - Elevated components (cards, dialogs): surface-container variants
   - Input fields: surface-container-highest
   - Snackbars: inverse-surface with inverse-on-surface text
   - Bottom sheets: surface-container-low

3. **State Layers**:
   - Hover: Apply 8% opacity layer of on-surface
   - Focus: Apply 12% opacity layer of on-surface
   - Pressed: Apply 12% opacity layer of on-surface
   - Dragged: Apply 16% opacity layer of on-surface

4. **Emphasis and Brand**:
   - Use fixed accent colors for brand elements that must remain consistent
   - Apply emphasis through color saturation and contrast, not just hue
   - Use tertiary as an expressive accent for onboarding, highlights, and branding

### Dynamic Color Generation

When generating color schemes from a source color:

1. **Extract Core Hue**: Identify the dominant hue from the source (e.g., user wallpaper)
2. **Generate Tonal Palettes**: Create five tonal palettes using HCT (Hue, Chroma, Tone) color space
3. **Assign Color Roles**: Map generated tones to semantic color roles (26+ roles)
4. **Generate Fixed Variants**: Create fixed accent colors that remain constant across themes
5. **Generate Surface Containers**: Create the five-level surface container hierarchy
6. **Generate Contrast Variants**: Produce standard, medium, and high contrast versions
7. **Validate Contrast**: Ensure all role pairs meet accessibility requirements
8. **Support Themes**: Generate both light and dark variants

### Best Practices

1. **Semantic Naming**: Always use semantic color tokens (e.g., `primary`, `error`) rather than literal colors (e.g., `blue`, `red`)
2. **Consistent Application**: Apply colors consistently across all components
3. **Elevation Tinting**: Add subtle tint to elevated surfaces using primary color at very low opacity
4. **Color Hierarchy**: Use primary for main actions, secondary for less important actions, tertiary for expressive accents
5. **Test Both Themes**: Always test in both light and dark modes
6. **Vibrant Expression**: In M3 Expressive, embrace richer, more vibrant colors while maintaining accessibility
7. **Context Awareness**: Adapt color intensity and palette based on app context and user preferences
8. **Use Fixed Colors for Branding**: Apply fixed accent tokens for logo colors or elements that must not change between themes
9. **Support Contrast Levels**: Implement standard, medium, and high contrast variants for accessibility
10. **Surface Container Hierarchy**: Use the five surface container levels to create clear visual depth

## Tools and Resources

- **`tokens.css`**: Ready-to-use M3 color tokens (light + dark) based on the orange baseline palette (#FF9800), included in this skill's directory. Copy into your project and customize.
- **`examples/color-roles.svg`**: Visual reference SVG showing M3 color roles (primary, secondary, tertiary, error), surface container tones, and the primary tonal palette. Use as a stakeholder reference or documentation asset.
- **`material-theme-builder` skill**: Use to generate a complete token set from any source color programmatically.
- **Material Color Utilities**: https://github.com/material-foundation/material-color-utilities — HCT color space, palette generation, and dynamic color algorithms
- **Material Theme Builder**: https://material-foundation.github.io/material-theme-builder/ — interactive web tool for generating color schemes
- **Official M3 CSS tokens**: https://github.com/material-foundation/material-tokens — baseline CSS token files (colors, typography, shape, motion, state, elevation)
- **M3 color system**: https://m3.material.io/styles/color/overview
- **M3 design tokens overview**: https://m3.material.io/foundations/design-tokens/overview
- **Color Contrast Checker**: Validate WCAG compliance for all text and interactive elements
- **HCT Color Space**: Leverage for perceptually uniform color generation
- **CSS Custom Properties**: Implement dynamic theming with CSS variables and data attributes

## Common Pitfalls to Avoid

1. ❌ Hard-coding color values instead of using tokens
2. ❌ Using only one color for all states (no hover, focus, pressed variations)
3. ❌ Ignoring dark theme or treating it as an afterthought
4. ❌ Insufficient contrast between text and background
5. ❌ Overusing accent colors (they should be used sparingly for emphasis)
6. ❌ Not testing with actual user-generated color schemes
7. ❌ Relying only on color to communicate state or information
8. ❌ Forgetting to define fixed accent colors for brand elements
9. ❌ Not implementing multiple contrast levels for accessibility
10. ❌ Using surface instead of the appropriate surface container variant

## Checklist for Color Implementation

When implementing M3 color systems, ensure:

- [ ] All five tonal palettes are defined (Primary, Secondary, Tertiary, Neutral, Neutral Variant)
- [ ] Both light and dark themes are implemented
- [ ] All color pairs meet WCAG contrast requirements
- [ ] Semantic color tokens are used throughout (no hard-coded hex values)
- [ ] State layers (hover, focus, pressed) are implemented with appropriate opacity
- [ ] Elevation tinting is applied to raised surfaces
- [ ] Color scheme can be dynamically generated from user source colors
- [ ] All components use color roles consistently
- [ ] Color is not the only indicator of state or information
- [ ] Fixed accent colors are defined for branding elements (primary-fixed, secondary-fixed, tertiary-fixed)
- [ ] Surface container hierarchy is implemented (lowest through highest)
- [ ] Inverse colors are defined for contrast elements (snackbars, tooltips)
- [ ] Three contrast levels are supported (standard, medium, high)
- [ ] Scrim and shadow tokens are defined
- [ ] Documentation includes color token reference and usage guidelines
