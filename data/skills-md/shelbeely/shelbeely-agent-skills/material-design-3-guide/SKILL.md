---
name: material-design-3-guide
description: Master guide for Material Design 3 — covering the full specification from Material You foundations through M3 Expressive. Explains when to use each Material Design 3 skill subset (color, motion, typography, shape, layout, components, icons). Use this when starting a Material Design 3 project, when you need to understand which M3 skill to apply, or when the user asks about Material Design 3 in general.
license: Apache-2.0
---

# Material Design 3 Guide

## Overview

This is the master guide for implementing Material Design 3 (M3) — covering the full specification from Material You foundations through M3 Expressive enhancements. It explains the overall system and directs you to specialized skills for each aspect.

**Keywords**: Material Design 3, M3, Material Design, design system, Google design, Material You, expressive design, UI design, M3 Expressive, React, MUI, Angular Material, Vue, Vuetify, Svelte, SMUI, Tailwind CSS, Next.js, Flutter, Jetpack Compose, web components, Beer CSS, Ink, CLI, terminal UI

## What is Material Design 3?

Material Design 3 is Google's open-source design system for creating digital products. It has evolved through two major phases:

### Material You (M3 Baseline)
The foundational M3 system introduced:
- **Dynamic Color**: Adaptive themes derived from user wallpapers and preferences
- **Tonal Palettes**: Five key palettes with systematic tonal generation
- **Type Scale**: 15 baseline type styles across five roles
- **Shape System**: Semantic corner radius scale from none to full
- **Elevation System**: Five levels with tinting for depth
- **Component Library**: Complete set of accessible, themed components
- **Token System**: CSS custom properties for consistent theming

### M3 Expressive (Latest Evolution)
Building on Material You, M3 Expressive adds:
- **30-Style Type Scale**: 15 emphasized variants alongside the 15 baseline styles
- **35 Expressive Shapes**: Decorative shape library with smooth morphing
- **Physics-Based Motion**: Spring parameters (stiffness, damping, velocity) replacing traditional easing
- **Fixed Accent Colors**: Colors that stay constant across light and dark themes
- **Contrast Levels**: Standardized standard, medium, and high contrast modes
- **New Components**: Split buttons, button groups, floating toolbars, FAB menus
- **Background Blur**: Depth effects for overlays and navigation
- **Haptic Integration**: Coordinated vibration with spring animations

## The Seven Pillars of Material Design 3

Material Design 3 is built on seven interconnected design pillars:

### 1. Color and Dynamic Theming
**What**: Vibrant, adaptive color systems with 26+ roles, proper contrast, and accessibility
**Use the `material-design-3-color` skill when**:
- Setting up color palettes or themes
- Implementing dynamic color (Material You)
- Working with primary, secondary, tertiary color roles
- Ensuring color accessibility and contrast
- Creating light and dark themes
- Defining color tokens and variables
- Applying state layers (hover, focus, pressed)
- Implementing elevation tinting
- Setting up fixed accent colors for branding (M3 Expressive)
- Configuring contrast levels (standard, medium, high) (M3 Expressive)
- Defining surface container hierarchy

**Key concepts**: Tonal palettes, color roles, dynamic color, accessibility, theming, fixed accents, contrast levels, surface containers

### 2. Motion and Animation
**What**: Physics-based, natural animations that guide attention and provide feedback
**Use the `material-design-3-motion` skill when**:
- Adding transitions between screens or states
- Implementing micro-interactions (hover, focus, press)
- Creating page or view transitions
- Animating component states
- Building loading states or progress indicators
- Implementing ripple effects
- Creating stagger animations for lists
- Morphing containers or shapes
- Choosing between expressive and standard motion (M3 Expressive)
- Integrating haptic feedback with animations (M3 Expressive)

**Key concepts**: Spring physics, stiffness/damping/velocity, easing curves, duration, transitions, haptics

### 3. Typography
**What**: Clear, readable type hierarchy using variable fonts and defined scales
**Use the `material-design-3-typography` skill when**:
- Setting up text styles and hierarchy
- Defining font families and weights
- Implementing the type scale (display, headline, title, body, label)
- Working with variable fonts
- Ensuring text readability and accessibility
- Setting line heights and letter spacing
- Creating responsive typography
- Using emphasized type styles for key moments (M3 Expressive)

**Key concepts**: Type scale (15 baseline + 15 emphasized), variable fonts, hierarchy, readability, medium contrast

### 4. Shape and Containment
**What**: Rounded corners, morphing shapes, and expressive decorative forms
**Use the `material-design-3-shape` skill when**:
- Defining border radius for components
- Creating rounded corners on cards, buttons, dialogs
- Implementing shape tokens (updated: Large 20dp, XL 32dp, XXL 48dp)
- Morphing shapes between states
- Working with containers and containment
- Styling buttons, FABs, chips, or input fields
- Using the 35 expressive shape library (M3 Expressive)
- Implementing expressive shape morphing (M3 Expressive)

**Key concepts**: Border radius, shape scale, morphing, containment, 35 expressive shapes, rounded corners

### 5. Layout and Size Hierarchy
**What**: Strategic use of spacing, size, containment, and depth to create visual flow
**Use the `material-design-3-layout` skill when**:
- Setting up page layouts and grids
- Defining spacing systems
- Creating responsive layouts
- Implementing size-based hierarchy
- Working with breakpoints
- Positioning components
- Creating visual emphasis through size
- Implementing elevation and depth
- Using background blur for overlays (M3 Expressive)
- Defining explicit vs implicit containment
- Implementing interaction states (hover, focus, pressed, disabled)

**Key concepts**: Spacing scale, grid systems, responsive design, visual hierarchy, background blur, containment, state layers

### 6. Components
**What**: Complete library of accessible, themed UI components
**Use the `material-design-3-components` skill when**:
- Building buttons, cards, dialogs, navigation, or any UI component
- Looking up component specifications (sizing, spacing, colors)
- Implementing new M3 Expressive components (split buttons, button groups, toolbars)
- Understanding component interaction states
- Choosing the right component for a use case
- Implementing FABs, chips, text fields, tabs, or menus

**Key concepts**: Action, containment, communication, navigation, selection, text input components

### 7. Icons
**What**: Material Symbols variable font icon system with 2,500+ icons
**Use the `material-design-3-icons` skill when**:
- Adding icons to an interface
- Configuring Material Symbols (fill, weight, grade, optical size)
- Implementing icon accessibility
- Using icon fill transitions for selection state
- Sizing icons correctly for different components
- Choosing an icon style (outlined, rounded, sharp)

**Key concepts**: Material Symbols, variable font axes (FILL, wght, GRAD, opsz), icon accessibility

## When to Use Which Skill

### Starting a New Material Design 3 Project

**Step 1: Color Foundation**
- Use `material-design-3-color` first
- Set up your color palette and theme
- Define all color tokens (primary, secondary, tertiary, surfaces, fixed accents)
- Implement both light and dark themes
- Configure contrast levels

**Step 2: Typography System**
- Use `material-design-3-typography`
- Define your type scale and font families (baseline + emphasized)
- Set up typography tokens
- Choose Roboto or custom brand fonts

**Step 3: Shape System**
- Use `material-design-3-shape`
- Define shape tokens for all corner radii (updated values)
- Set up component-specific shapes

**Step 4: Icons**
- Use `material-design-3-icons`
- Load Material Symbols (choose one style)
- Configure default variable font axes

**Step 5: Layout Foundation**
- Use `material-design-3-layout`
- Set up spacing scale and grid system
- Define breakpoints for responsive design
- Set up containment patterns and interaction states

**Step 6: Build Components**
- Use `material-design-3-components`
- Build all UI components using the established tokens
- Follow component-specific specifications

**Step 7: Add Motion**
- Use `material-design-3-motion`
- Implement transitions and animations (choose expressive vs standard)
- Add micro-interactions to interactive elements
- Integrate haptic feedback where appropriate

### Working on Specific Components

**Buttons**:
- Components: `material-design-3-components` (specs, variants, button groups)
- Shape: `material-design-3-shape` (full radius, pill shape)
- Color: `material-design-3-color` (primary/secondary/tertiary)
- Typography: `material-design-3-typography` (label-large)
- Motion: `material-design-3-motion` (hover, focus, press states)
- Layout: `material-design-3-layout` (spacing, sizing)
- Icons: `material-design-3-icons` (button icons)

**Cards**:
- Components: `material-design-3-components` (elevated, filled, outlined)
- Shape: `material-design-3-shape` (medium radius, 12dp)
- Color: `material-design-3-color` (surface container variants)
- Typography: `material-design-3-typography` (title + body text)
- Motion: `material-design-3-motion` (elevation change on hover)
- Layout: `material-design-3-layout` (padding, content flow)

**Dialogs/Modals**:
- Components: `material-design-3-components` (dialog specs)
- Shape: `material-design-3-shape` (extra-large radius, 32dp)
- Color: `material-design-3-color` (surface-container-high)
- Typography: `material-design-3-typography` (headline + body)
- Motion: `material-design-3-motion` (enter/exit animations)
- Layout: `material-design-3-layout` (centered, max-width, background blur)

**Navigation**:
- Components: `material-design-3-components` (bar, rail, drawer, tabs)
- Color: `material-design-3-color` (surface variant, active states)
- Typography: `material-design-3-typography` (label-large)
- Shape: `material-design-3-shape` (indicators, pills)
- Motion: `material-design-3-motion` (transition animations)
- Layout: `material-design-3-layout` (nav structure)
- Icons: `material-design-3-icons` (navigation icons with fill toggle)

**Forms/Inputs**:
- Components: `material-design-3-components` (text fields, selectors)
- Shape: `material-design-3-shape` (extra-small radius, 4dp)
- Color: `material-design-3-color` (surface variant, outlines)
- Typography: `material-design-3-typography` (body text, labels)
- Motion: `material-design-3-motion` (focus animations)
- Layout: `material-design-3-layout` (field spacing, alignment)

### Common Scenarios

**"Make it look Material Design 3"**:
1. Start with `material-design-3-color` - set up the color system
2. Apply `material-design-3-shape` - add rounded corners
3. Use `material-design-3-typography` - implement the type scale
4. Load `material-design-3-icons` - set up Material Symbols
5. Build with `material-design-3-components` - use M3 component specs
6. Add `material-design-3-motion` - implement spring animations
7. Apply `material-design-3-layout` - ensure proper spacing

**"Make it M3 Expressive"**:
1. Follow the standard M3 setup above
2. Add emphasized type styles from `material-design-3-typography`
3. Use expressive shapes from `material-design-3-shape` for decorative moments
4. Switch to expressive motion mode from `material-design-3-motion`
5. Implement new components (split buttons, button groups, toolbars) from `material-design-3-components`
6. Add fixed accent colors and contrast levels from `material-design-3-color`
7. Use background blur from `material-design-3-layout`

**"Add Material Design animations"**:
- Primarily use `material-design-3-motion`
- May need `material-design-3-color` for state layers
- May need `material-design-3-shape` for morphing shapes

**"Fix Material Design colors"**:
- Use `material-design-3-color` exclusively
- Focus on color roles, contrast, and theming

**"Style this button/card/dialog"**:
- Start with `material-design-3-components` for specs
- Then apply shape + color + typography as needed

**"Make it responsive"**:
- Primarily `material-design-3-layout`
- May need `material-design-3-typography` for responsive text
- May need `material-design-3-shape` for responsive radii

**"Implement dark mode"**:
- Use `material-design-3-color` for theme switching
- Ensure all color tokens are defined for both themes
- Adjust icon grade for dark mode via `material-design-3-icons`

**"Add icons"**:
- Use `material-design-3-icons` for Material Symbols setup
- Use `material-design-3-color` for icon color tokens

## Integration Principles

### All Skills Work Together

Material Design 3 is a holistic system - the skills are designed to be used together:

- **Color** defines the palette
- **Typography** defines the text
- **Shape** defines the form
- **Motion** defines the behavior
- **Layout** defines the structure
- **Components** define the building blocks
- **Icons** define the visual language

### Consistency is Key

When using multiple skills:
- Use tokens/variables defined in each skill
- Don't hard-code values
- Maintain consistency across all design aspects
- Test the combined result, not just individual parts

### Example: Complete Button Implementation

```css
/* Uses all seven pillars */
.md3-button {
  /* Shape */
  border-radius: var(--md-sys-shape-corner-full);
  
  /* Color */
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  
  /* Typography */
  font-family: var(--md-sys-typescale-label-large-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  letter-spacing: var(--md-sys-typescale-label-large-tracking);
  
  /* Layout */
  padding: var(--md-sys-spacing-2) var(--md-sys-spacing-6);
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  gap: var(--md-sys-spacing-2);
  
  /* Motion */
  transition: 
    background-color var(--md-sys-motion-duration-short2) var(--md-sys-motion-easing-standard),
    box-shadow var(--md-sys-motion-duration-short2) var(--md-sys-motion-easing-standard),
    transform var(--md-sys-motion-duration-short2) var(--md-sys-motion-easing-standard);
}

.md3-button:hover {
  /* Color - state layer */
  background-color: var(--md-sys-color-primary);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  
  /* Motion */
  transform: translateY(-1px);
}

/* Icons in button */
.md3-button .material-symbols-outlined {
  font-size: 18px;
  font-variation-settings: 'opsz' 20;
}
```

## Quick Reference

### Which Skill for Which Property?

| Property | Skill |
|----------|-------|
| `color`, `background-color` | material-design-3-color |
| `font-size`, `font-family`, `line-height`, `font-weight`, `letter-spacing` | material-design-3-typography |
| `border-radius`, `clip-path` | material-design-3-shape |
| `transition`, `animation`, `@keyframes` | material-design-3-motion |
| `margin`, `padding`, `gap`, `width`, `height`, `display`, `grid` | material-design-3-layout |
| `box-shadow` (elevation) | material-design-3-layout (+ motion for transitions) |
| `backdrop-filter` (blur) | material-design-3-layout |
| `font-variation-settings` (icons) | material-design-3-icons |
| Component-specific specs | material-design-3-components |

### Which Skill for Which Component?

| Component | Primary Skill | Supporting Skills |
|-----------|--------------|-------------------|
| Buttons | components | color, shape, typography, motion |
| Cards | components | color, shape, layout |
| Dialogs | components | color, shape, layout, motion |
| Navigation | components | color, icons, layout, motion |
| Text Fields | components | color, shape, typography |
| FABs | components | color, shape, icons, motion |
| Chips | components | color, shape, typography |
| Tabs | components | color, typography, icons, motion |
| Lists | components | color, typography, layout |
| Menus | components | color, shape, layout |

### File Organization

When implementing M3, organize your code:

```
styles/
├── tokens/
│   ├── color.css          # From material-design-3-color
│   ├── typography.css     # From material-design-3-typography
│   ├── shape.css          # From material-design-3-shape
│   ├── motion.css         # From material-design-3-motion
│   ├── layout.css         # From material-design-3-layout
│   └── icons.css          # From material-design-3-icons
├── components/
│   ├── button.css         # Uses all skills
│   ├── card.css           # Uses all skills
│   ├── dialog.css         # Uses all skills
│   ├── navigation.css     # Uses all skills
│   └── text-field.css     # Uses all skills
└── main.css               # Imports all tokens
```

## Best Practices

### Do's

1. ✅ **Use all seven pillars** - M3 works best when all aspects are implemented
2. ✅ **Start with tokens** - Define all design tokens before building components
3. ✅ **Follow the skills** - Each skill provides tested, research-backed guidelines
4. ✅ **Test accessibility** - All skills include accessibility requirements
5. ✅ **Support both themes** - Always implement light and dark modes
6. ✅ **Use semantic names** - Use token names, not hard-coded values
7. ✅ **Be consistent** - Apply the same patterns across all components
8. ✅ **Cover the full spec** - Include Material You baseline and M3 Expressive additions

### Don'ts

1. ❌ **Don't cherry-pick** - Using only color without shape/motion isn't really M3
2. ❌ **Don't hard-code** - Always use the defined tokens and variables
3. ❌ **Don't skip accessibility** - Contrast, sizing, and motion preferences matter
4. ❌ **Don't ignore dark mode** - It's a core part of M3
5. ❌ **Don't improvise values** - Use the scales provided in each skill
6. ❌ **Don't mix design systems** - Don't combine M3 with other design languages
7. ❌ **Don't forget motion** - Static M3 misses the "expressive" part
8. ❌ **Don't skip icons** - Material Symbols are integral to the M3 visual language

## Material Design 3 for Different Web Stacks

M3 can be implemented across many web stacks. Each framework has a **dedicated library-specific skill** with full setup, theming, and component examples. Use the overview table below to find the right skill for your project.

### Web Stack Overview

| Stack | Primary Library | M3 Support | Skill |
|-------|----------------|------------|-------|
| **Vanilla CSS** | CSS custom properties | Full (manual) | `m3-web-vanilla` |
| **Web Components** | `@material/web` (Lit) | Full M3 | `m3-web-webcomponents` |
| **React / Next.js** | MUI (`@mui/material`) | M3 theming | `m3-web-react` |
| **Angular** | `@angular/material` | Full M3 (official) | `m3-web-angular` |
| **Vue** | Vuetify 3 | Full M3 | `m3-web-vue` |
| **Svelte** | SMUI / `@material/web` | Partial M3 | `m3-web-svelte` |
| **Tailwind CSS** | `tailwind-material-3` plugin | Token-based M3 | `m3-web-tailwind` |
| **Ink (React CLI)** | `ink` + `@inkjs/ui` | Token-based M3 | `m3-web-ink` |
| **Flutter** | `material` / `m3e_design` | Full M3 | `m3-web-flutter` |
| **Android** | Jetpack Compose Material 3 | Full M3 + Expressive | `m3-web-android` |

### Choosing the Right Stack

| If your project uses... | Recommended Skill | Why |
|-------------------------|------------------|-----|
| No framework (vanilla) | `m3-web-vanilla` | Full control, zero dependencies |
| React or Next.js | `m3-web-react` | Largest ecosystem, SSR support |
| Angular | `m3-web-angular` | Official, best M3 integration |
| Vue | `m3-web-vue` | Enterprise-ready, excellent docs |
| Svelte / SvelteKit | `m3-web-svelte` | Best available for Svelte |
| Tailwind CSS | `m3-web-tailwind` | Utility-first with M3 tokens |
| Any framework | `m3-web-webcomponents` | Official, framework-agnostic |
| CLI / Terminal | `m3-web-ink` | React-based, themeable |
| Flutter | `m3-web-flutter` | Official, cross-platform |
| Android | `m3-web-android` | Official, most complete M3 |

**Tips for choosing**:
1. **Angular projects**: Use `m3-web-angular` — best official M3 support of any web framework
2. **React projects**: Use `m3-web-react` for MUI, or `m3-web-webcomponents` for Google's official components
3. **Vue projects**: Use `m3-web-vue` — Vuetify 3 is mature and well-documented
4. **Framework-agnostic**: Use `m3-web-webcomponents` or `m3-web-vanilla`
5. **Prototype quickly**: Use `m3-web-vanilla` (Beer CSS) or `m3-web-webcomponents` via CDN
6. **Need Tailwind**: Use `m3-web-tailwind` to map M3 tokens to Tailwind config
7. **Mobile + Web**: Use `m3-web-flutter` for cross-platform M3
8. **CLI / Terminal**: Use `m3-web-ink` with M3 color tokens mapped to terminal colors

## Resources

### Material Design 3 Core Skills

- `material-design-3-color` - Color palettes, theming, accessibility, fixed accents, contrast levels
- `material-design-3-motion` - Animations, transitions, micro-interactions, spring physics, haptics
- `material-design-3-typography` - Type scale (30 styles), fonts, hierarchy, emphasized variants
- `material-design-3-shape` - Border radius, containment, morphing, 35 expressive shapes
- `material-design-3-layout` - Spacing, grids, responsive design, background blur, interaction states
- `material-design-3-components` - Complete component catalog with specs and implementation
- `material-design-3-icons` - Material Symbols, variable font axes, icon accessibility

### Library-Specific Skills

- `m3-web-vanilla` - Vanilla CSS custom properties, Beer CSS, zero-dependency M3
- `m3-web-webcomponents` - Google's official `@material/web` Lit-based components
- `m3-web-react` - React / MUI / Next.js M3 theming and SSR integration
- `m3-web-angular` - Angular Material M3 theming, SCSS mixins, schematics
- `m3-web-vue` - Vuetify 3 M3 theming, components, dark mode
- `m3-web-svelte` - SMUI + direct `@material/web` in Svelte/SvelteKit
- `m3-web-tailwind` - Tailwind CSS M3 token mapping and plugin setup
- `m3-web-ink` - Ink React CLI with `@inkjs/ui` M3 theming
- `m3-web-flutter` - Flutter M3 theming, dynamic color, M3 Expressive packages
- `m3-web-android` - Jetpack Compose Material 3, dynamic color, M3 Expressive

### External Resources

- **Official M3 Site**: https://m3.material.io/
- **M3 Components**: https://m3.material.io/components
- **M3 Styles**: https://m3.material.io/styles
- **M3 Foundations**: https://m3.material.io/foundations
- **M3 for Web**: https://m3.material.io/develop/web
- **M3 for Android**: https://m3.material.io/develop/android/jetpack-compose
- **M3 for Flutter**: https://m3.material.io/develop/flutter
- **M3 Design Kit (Figma)**: https://www.figma.com/community/file/1035203688168086460 — Official M3 component library with styles, variants, dynamic color, and expressive features
- **Material Web Components** (@material/web): https://github.com/material-components/material-web
- **Material Color Utilities**: https://github.com/material-foundation/material-color-utilities
- **Material Theme Builder**: https://github.com/material-foundation/material-theme-builder
- **Material Design Tokens**: https://github.com/material-foundation/material-tokens
- **Angular Material**: https://github.com/angular/components
- **Material Symbols**: https://fonts.google.com/icons
- **MUI** (React): https://mui.com/material-ui/
- **Vuetify** (Vue): https://vuetifyjs.com/
- **SMUI** (Svelte): https://sveltematerialui.com/
- **Beer CSS** (CSS-only M3): https://www.beercss.com/
- **Tailwind M3 Plugin**: https://github.com/rinturaj/tailwind-material-3

## Checklist for Material Design 3 Projects

Starting a new M3 project? Follow this checklist:

### Foundation
- [ ] Review this guide to understand the seven pillars
- [ ] Set up color system using `material-design-3-color`
- [ ] Define typography using `material-design-3-typography`
- [ ] Create shape tokens using `material-design-3-shape`
- [ ] Load Material Symbols using `material-design-3-icons`
- [ ] Establish spacing/layout system using `material-design-3-layout`

### Implementation
- [ ] Build components using `material-design-3-components` specs
- [ ] Implement both light and dark themes
- [ ] Add motion and transitions using `material-design-3-motion`
- [ ] Test on multiple screen sizes (responsive)
- [ ] Verify accessibility (contrast, sizing, motion preferences)

### M3 Expressive Enhancements (Optional)
- [ ] Add emphasized type styles for key moments
- [ ] Use expressive shapes for decorative delight
- [ ] Switch to expressive motion mode for hero interactions
- [ ] Implement fixed accent colors for branding
- [ ] Add contrast level support
- [ ] Use new components (split buttons, button groups, toolbars)
- [ ] Add background blur for overlays and navigation

### Quality Assurance
- [ ] All colors use semantic tokens (no hard-coded hex)
- [ ] All text uses the type scale (baseline or emphasized)
- [ ] All shapes use the shape scale
- [ ] All animations use spring physics
- [ ] All spacing uses the spacing scale
- [ ] All icons use Material Symbols with correct axes
- [ ] Dark mode works correctly
- [ ] Reduced motion is respected
- [ ] Touch targets are 48×48dp minimum
- [ ] Text contrast meets WCAG AA (4.5:1)
- [ ] All components have proper interaction states
- [ ] Fixed accent colors remain consistent across themes

## Summary

Material Design 3 is a complete design system covering the full specification from Material You foundations through M3 Expressive enhancements. It is built on seven interconnected pillars, each with a dedicated skill:

1. **Color** - The palette, themes, and accessibility
2. **Motion** - The behavior, physics, and haptics
3. **Typography** - The voice, hierarchy, and emphasis
4. **Shape** - The personality, form, and expression
5. **Layout** - The structure, depth, and containment
6. **Components** - The building blocks and interactions
7. **Icons** - The visual language and symbols

Use this guide to understand which skill to apply for your specific needs, and remember that M3 works best when all seven pillars work together in harmony.
