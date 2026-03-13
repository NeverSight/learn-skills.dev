---
name: design-system-management
description: Cyberpunk theme design system with CSS custom properties, component library, and visual consistency standards
license: Apache-2.0
---

# Design System Management

## Purpose

Maintain a consistent, scalable design system for riksdagsmonitor using CSS custom properties, component patterns, and the cyberpunk aesthetic theme across all 14 language versions.

## Core Principles

1. **Single Source of Truth**: All design tokens in CSS custom properties
2. **Component-Based**: Reusable, composable UI components
3. **Theme Consistency**: Cyberpunk aesthetic across all pages
4. **Accessibility Built-In**: WCAG 2.1 AA compliant by default
5. **Responsive**: Mobile-first, fluid scaling
6. **Performance**: Minimal CSS, efficient selectors

## Cyberpunk Theme

### Color Palette
```css
:root {
  /* Primary Colors - Neon accents */
  --primary-cyan: #00d9ff;
  --primary-magenta: #ff006e;
  --primary-yellow: #ffbe0b;
  
  /* Background Colors - Dark base */
  --dark-bg: #0a0e27;
  --mid-bg: #1a1e3d;
  --light-bg: #2a2e4d;
  
  /* Text Colors */
  --light-text: #e0e0e0;
  --mid-text: #a0a0a0;
  --dim-text: #606060;
  
  /* Semantic Colors */
  --success: #00ff88;
  --warning: --primary-yellow;
  --error: #ff0055;
  --info: --primary-cyan;
}
```

### Typography Scale
```css
:root {
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-heading: 'Orbitron', 'Courier New', monospace;
  --font-mono: 'Fira Code', 'Courier New', monospace;
  
  /* Fluid Typography */
  --text-xs: clamp(0.75rem, 1vw, 0.875rem);
  --text-sm: clamp(0.875rem, 1.5vw, 1rem);
  --text-base: clamp(1rem, 2vw, 1.125rem);
  --text-lg: clamp(1.125rem, 2.5vw, 1.25rem);
  --text-xl: clamp(1.25rem, 3vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 4vw, 2rem);
  --text-3xl: clamp(2rem, 5vw, 3rem);
  --text-4xl: clamp(3rem, 6vw, 4rem);
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### Spacing Scale
```css
:root {
  /* Fluid Spacing */
  --space-xs: clamp(0.25rem, 0.5vw, 0.5rem);
  --space-sm: clamp(0.5rem, 1vw, 0.75rem);
  --space-md: clamp(0.75rem, 1.5vw, 1rem);
  --space-lg: clamp(1rem, 2vw, 1.5rem);
  --space-xl: clamp(1.5rem, 3vw, 2rem);
  --space-2xl: clamp(2rem, 4vw, 3rem);
  --space-3xl: clamp(3rem, 5vw, 4rem);
}
```

### Borders & Shadows
```css
:root {
  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;
  
  /* Borders */
  --border-width: 2px;
  --border-color: var(--primary-cyan);
  
  /* Shadows - Cyberpunk glow effects */
  --shadow-sm: 0 0 10px rgba(0, 217, 255, 0.3);
  --shadow-md: 0 0 20px rgba(0, 217, 255, 0.5);
  --shadow-lg: 0 0 40px rgba(0, 217, 255, 0.7);
  --shadow-glow-magenta: 0 0 20px rgba(255, 0, 110, 0.6);
  --shadow-glow-yellow: 0 0 20px rgba(255, 190, 11, 0.6);
}
```

## Component Library

### Button Components
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-md) var(--space-xl);
  font-size: var(--text-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  border: var(--border-width) solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  min-height: 44px; /* Touch target */
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-magenta), var(--primary-cyan));
  color: white;
  border-color: var(--primary-cyan);
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover,
.btn-primary:focus {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: var(--primary-cyan);
  border-color: var(--primary-cyan);
}

.btn-secondary:hover {
  background: var(--primary-cyan);
  color: var(--dark-bg);
}
```

### Card Components
```css
.card {
  background: var(--mid-bg);
  border: var(--border-width) solid var(--primary-cyan);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
  border-color: var(--primary-magenta);
}

.card-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: var(--space-md);
  margin-bottom: var(--space-md);
}

.card-title {
  font-family: var(--font-heading);
  font-size: var(--text-xl);
  color: var(--primary-cyan);
  margin: 0;
}

.card-body {
  color: var(--light-text);
  line-height: var(--leading-relaxed);
}
```

### Navigation Components
```css
.nav {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--dark-bg);
  border-bottom: var(--border-width) solid var(--primary-cyan);
}

.nav-link {
  color: var(--light-text);
  text-decoration: none;
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover,
.nav-link:focus {
  color: var(--primary-cyan);
  box-shadow: var(--shadow-glow-magenta);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-magenta), var(--primary-cyan));
}
```

## When to Use

- **New Page Creation**: Apply design system tokens
- **Component Development**: Use or extend component library
- **UI Refactoring**: Standardize inconsistent styles
- **Theme Updates**: Modify CSS custom properties
- **Responsive Design**: Use fluid spacing/typography
- **Accessibility Enhancements**: Leverage built-in WCAG compliance

## Remember

- **Use CSS custom properties** - never hard-code colors/sizes
- **Component-first approach** - reuse existing components
- **Mobile-first** - design for smallest screen first
- **Accessibility built-in** - 4.5:1 contrast, 44x44px touch targets
- **Cyberpunk theme** - neon accents, dark backgrounds, glow effects
- **Fluid scaling** - use clamp() for responsive typography
- **Performance** - minimal CSS, efficient selectors
- **Consistency** - same patterns across all 14 languages

## References

- [Design Systems Handbook](https://www.designbetter.co/design-systems-handbook)
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Design Tokens (W3C)](https://www.w3.org/community/design-tokens/)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Maintained by**: Hack23 AB
