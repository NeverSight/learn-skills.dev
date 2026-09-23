---
name: dark-mode
description: >
  Dark theme design patterns with proper color adaptation, surface hierarchy, and CSS implementation.
  Trigger: user asks to "add dark mode", "create a dark theme", "dark mode support",
  "implement dark/light toggle", "design for dark background", "night mode",
  or any dark theme design work.
license: MIT
---

# Dark Mode Design

## Pre-Flight: Check Design Context

Before generating dark mode code:
1. Use `get_design_context` to check for existing color tokens, theme variables, or design system.
2. If a Figma URL is provided, pull screenshots for both light and dark variants.
3. Determine: Is this a full dark theme, a dark-first design, or adding dark mode to an existing light UI?

---

## 1. Core Rule: Don't Just Invert

Inverting colors produces harsh, unreadable interfaces. Dark mode requires intentional design decisions.

### What Changes
| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Background | White (#fff) | Dark gray (NOT pure black) |
| Text | Near-black | Near-white (NOT pure white) |
| Borders | Gray-200 | White at 8–12% opacity |
| Shadows | Black at 5–15% | Nearly invisible or none |
| Primary color | Full saturation | Reduced saturation |
| Images | Full brightness | Slightly dimmed |
| Elevation | Shadows | Lighter surface color |

### Never Use
- Pure black `#000` as background (too harsh, OLED smearing).
- Pure white `#fff` for text (too much contrast, eye strain).
- The same shadow values from light mode.

---

## 2. Elevation Through Luminance

In light mode, elevation is shown with shadows. In dark mode, elevated surfaces are lighter.

### Surface Hierarchy
```css
:root {
  /* Light mode */
  --bg-base: oklch(100% 0 0);         /* white */
  --bg-surface: oklch(100% 0 0);      /* white */
  --bg-elevated: oklch(100% 0 0);     /* white + shadow */
  --bg-overlay: oklch(100% 0 0);      /* white + deeper shadow */
}

[data-theme="dark"] {
  /* Dark mode — each level gets progressively lighter */
  --bg-base: oklch(13% 0.01 265);     /* darkest: page background */
  --bg-surface: oklch(18% 0.01 265);  /* cards, sidebar */
  --bg-elevated: oklch(23% 0.01 265); /* dropdowns, popovers */
  --bg-overlay: oklch(28% 0.01 265);  /* modals, tooltips */
}
```

### Practical Example
```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
}
.dropdown {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
}
.modal {
  background: var(--bg-overlay);
}
```

### Material Design Overlay Model
Each elevation level adds white at increasing opacity:
- Level 0 (base): 0% white overlay
- Level 1 (card): 5% white overlay
- Level 2 (nav bar): 7% white overlay
- Level 3 (drawer): 8% white overlay
- Level 4 (modal): 12% white overlay

---

## 3. Color Saturation Rules

### Reduce Saturation for Dark Backgrounds
Bright, saturated colors on dark backgrounds cause visual vibration and eye strain.

```css
:root {
  --color-primary: oklch(60% 0.25 265);   /* Light mode: full saturation */
  --color-success: oklch(55% 0.20 155);
  --color-error: oklch(55% 0.22 25);
}

[data-theme="dark"] {
  --color-primary: oklch(72% 0.18 265);   /* Dark mode: lighter, less saturated */
  --color-success: oklch(70% 0.15 155);
  --color-error: oklch(70% 0.16 25);
}
```

### Rules
- Increase lightness by 10–15% for dark mode.
- Decrease chroma (saturation) by 15–25%.
- Backgrounds with color (e.g., badges) should use lower opacity.

```css
/* Light mode badge */
.badge-success {
  background: oklch(95% 0.05 155);
  color: oklch(35% 0.15 155);
}

/* Dark mode badge */
[data-theme="dark"] .badge-success {
  background: oklch(35% 0.08 155);
  color: oklch(80% 0.12 155);
}
```

---

## 4. Text Contrast Levels

### White-on-Dark Opacity Scale
Use white at different opacities for text hierarchy on dark backgrounds.

| Role | Opacity | Use Case |
|------|---------|----------|
| High emphasis | 87% (`oklch(100% 0 0 / 0.87)`) | Headings, primary text |
| Medium emphasis | 60% (`oklch(100% 0 0 / 0.60)`) | Body text, secondary |
| Disabled / Hint | 38% (`oklch(100% 0 0 / 0.38)`) | Placeholders, disabled |

### Implementation
```css
[data-theme="dark"] {
  --text-primary: oklch(95% 0 0);      /* Not pure white */
  --text-secondary: oklch(70% 0 0);
  --text-muted: oklch(50% 0 0);
  --text-disabled: oklch(38% 0 0);
}
```

### Tailwind Approach
```html
<!-- High emphasis -->
<h1 class="text-white/90">Main Heading</h1>

<!-- Medium emphasis -->
<p class="text-white/60">Body text content here.</p>

<!-- Low emphasis -->
<span class="text-white/40">Last updated 2 hours ago</span>
```

---

## 5. Border & Divider Treatment

### Light Borders on Dark
Borders in dark mode should use semi-transparent white, not gray values.

```css
[data-theme="dark"] {
  --border: oklch(100% 0 0 / 0.08);       /* subtle */
  --border-strong: oklch(100% 0 0 / 0.15); /* emphasized */
  --divider: oklch(100% 0 0 / 0.06);       /* section dividers */
}
```

This ensures borders adapt correctly regardless of the underlying surface color.

---

## 6. Image Handling in Dark Mode

### Reduce Image Brightness
```css
[data-theme="dark"] img:not([data-no-dim]) {
  filter: brightness(0.85);
}

/* Restore on hover for galleries */
[data-theme="dark"] img:hover {
  filter: brightness(1);
}
```

### Dark Overlay for Hero Images
```html
<div class="relative">
  <img src="/hero.jpg" alt="" class="w-full" />
  <div class="absolute inset-0 bg-gray-950/30 dark:bg-gray-950/50"></div>
</div>
```

### SVG Icon Adaptation
Icons should use `currentColor` so they inherit text color automatically:
```html
<svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="currentColor">
  <!-- icon paths -->
</svg>
```

### Logo Handling
Provide separate logos for light and dark modes:
```html
<img src="/logo-dark.svg" alt="Logo" class="dark:hidden" />
<img src="/logo-light.svg" alt="Logo" class="hidden dark:block" />
```

---

## 7. CSS Implementation

### Method 1: `prefers-color-scheme` (System Preference)
```css
:root {
  --bg: oklch(100% 0 0);
  --text: oklch(15% 0 0);
  --surface: oklch(100% 0 0);
  --border: oklch(90% 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: oklch(13% 0.01 265);
    --text: oklch(95% 0 0);
    --surface: oklch(18% 0.01 265);
    --border: oklch(100% 0 0 / 0.08);
  }
}
```

### Method 2: CSS Custom Properties + Class Toggle (User Preference)
```css
:root {
  --bg: oklch(100% 0 0);
  --text: oklch(15% 0 0);
}

[data-theme="dark"] {
  --bg: oklch(13% 0.01 265);
  --text: oklch(95% 0 0);
}

body {
  background: var(--bg);
  color: var(--text);
}
```

```javascript
// Toggle implementation
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

// Initialize on page load (prevent flash)
function initTheme() {
  const saved = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (systemPrefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
}
```

### Method 3: Tailwind `dark:` Variant
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100
  border-gray-200 dark:border-white/10">
  <h2 class="text-gray-950 dark:text-white">Title</h2>
  <p class="text-gray-600 dark:text-gray-400">Description</p>
</div>
```

Tailwind config for class-based dark mode:
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'selector' for data-attribute
}
```

### Prevent Flash of Wrong Theme (FOUC)
Add this script in `<head>` before any CSS:
```html
<script>
  (function() {
    var theme = localStorage.getItem('theme');
    if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  })();
</script>
```

---

## 8. Component-Specific Dark Mode Patterns

### Input Fields
```html
<input class="bg-white border-gray-300 text-gray-900 placeholder:text-gray-400
  focus:border-indigo-500 focus:ring-indigo-500/20
  dark:bg-white/5 dark:border-white/10 dark:text-white dark:placeholder:text-gray-500
  dark:focus:border-indigo-400 dark:focus:ring-indigo-400/20" />
```

### Cards
```html
<div class="bg-white border border-gray-200 shadow-sm
  dark:bg-white/5 dark:border-white/8 dark:shadow-none">
```

### Buttons
```html
<!-- Primary: stays bold in both modes -->
<button class="bg-indigo-600 text-white hover:bg-indigo-500
  dark:bg-indigo-500 dark:hover:bg-indigo-400">
  Primary
</button>

<!-- Secondary: adapts background -->
<button class="bg-gray-100 text-gray-700 hover:bg-gray-200
  dark:bg-white/10 dark:text-gray-200 dark:hover:bg-white/15">
  Secondary
</button>
```

### Dropdowns / Popovers
```html
<div class="bg-white border border-gray-200 shadow-lg rounded-xl
  dark:bg-gray-800 dark:border-white/10 dark:shadow-2xl dark:shadow-black/20">
```

### Tables
```html
<tr class="border-b border-gray-100 hover:bg-gray-50
  dark:border-white/5 dark:hover:bg-white/5">
```

---

## 9. Smooth Mode Transition

### CSS Transition Between Modes
```css
/* Apply to root — transitions all custom property changes */
:root {
  transition: background-color 200ms ease, color 200ms ease;
}

/* Or apply broadly */
*,
*::before,
*::after {
  transition: background-color 200ms ease,
    border-color 200ms ease,
    color 200ms ease,
    fill 200ms ease,
    stroke 200ms ease;
}
```

### Important: Exclude animations
```css
/* Don't transition transforms, opacity, or layout properties */
* {
  transition-property: background-color, border-color, color, fill, stroke, box-shadow;
  transition-duration: 200ms;
  transition-timing-function: ease;
}
```

### Toggle Button UI
```html
<button onclick="toggleTheme()" class="relative w-14 h-7 rounded-full
  bg-gray-200 dark:bg-indigo-600 transition-colors"
  aria-label="Toggle dark mode">
  <span class="absolute top-0.5 left-0.5 w-6 h-6 rounded-full bg-white shadow
    transform transition-transform dark:translate-x-7 flex items-center justify-center">
    <!-- Sun icon (light mode) -->
    <svg class="w-4 h-4 text-amber-500 dark:hidden" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/>
    </svg>
    <!-- Moon icon (dark mode) -->
    <svg class="w-4 h-4 text-indigo-200 hidden dark:block" fill="currentColor" viewBox="0 0 20 20">
      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
    </svg>
  </span>
</button>
```

---

## Complete Token System

### Recommended Dark Mode Palette
```css
[data-theme="dark"] {
  /* Surfaces */
  --bg-base: oklch(13% 0.01 265);
  --bg-surface: oklch(18% 0.01 265);
  --bg-elevated: oklch(23% 0.01 265);
  --bg-overlay: oklch(28% 0.01 265);

  /* Text */
  --text-primary: oklch(95% 0 0);
  --text-secondary: oklch(70% 0 0);
  --text-muted: oklch(50% 0 0);

  /* Borders */
  --border: oklch(100% 0 0 / 0.08);
  --border-strong: oklch(100% 0 0 / 0.15);

  /* Interactive */
  --color-primary: oklch(72% 0.18 265);
  --color-primary-hover: oklch(78% 0.16 265);

  /* Status */
  --color-success: oklch(70% 0.15 155);
  --color-warning: oklch(75% 0.15 80);
  --color-error: oklch(70% 0.16 25);
  --color-info: oklch(72% 0.15 230);
}
```

---

## Dark Mode Checklist

- [ ] Background is dark gray (not pure black)
- [ ] Text is off-white (not pure white)
- [ ] Elevation uses lighter surfaces, not shadows
- [ ] Primary colors are desaturated and lightened
- [ ] Borders use semi-transparent white
- [ ] Images are slightly dimmed
- [ ] Logos have light variants
- [ ] No FOUC (flash of unstyled content) on page load
- [ ] System preference is detected and respected
- [ ] User preference is persisted in localStorage
- [ ] Transition between modes is smooth (200ms)
- [ ] Contrast ratios still meet WCAG AA (4.5:1)
- [ ] All components tested in both modes
