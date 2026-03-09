---
name: tailwind-best-practices
description: |
  WHEN: User is writing HTML/templates with Tailwind CSS classes, styling components,
  configuring Tailwind themes, asking about utilities or patterns, or working with any
  project that uses Tailwind CSS. Also trigger when user mentions "responsive design",
  "dark mode", "custom colors", "spacing", "flex/grid layout" in a Tailwind project,
  asks about v4 migration, @theme vs @apply, or is editing CSS/HTML files in a project
  with tailwind in its dependencies. Activate whenever tailwind.config.* or @tailwind
  directives are present.
  WHEN NOT: Projects not using Tailwind, questions about Bootstrap/Bulma/other CSS frameworks
---

<!-- cache:start -->

# Tailwind CSS v4 Best Practices

You have access to up-to-date Tailwind CSS documentation via MCP tools. Use these tools to provide accurate, current information.

## Available MCP Tools

Use these tools for dynamic, up-to-date Tailwind information:

### `mcp__tailwindcss__search_tailwind_docs`

Use when user asks about any Tailwind feature, utility, or concept.

**Examples:**
- "How do I use dark mode in Tailwind?"
- "What are container queries?"
- "How do responsive breakpoints work?"

### `mcp__tailwindcss__get_tailwind_utilities`

Use when user needs utility classes for a specific CSS property.

**Examples:**
- "What utilities are available for flexbox?"
- "Show me spacing utilities"
- "What text alignment classes exist?"

### `mcp__tailwindcss__get_tailwind_colors`

Use when user asks about colors, palettes, or color-related utilities.

**Examples:**
- "What colors are available?"
- "Show me the blue palette shades"
- "How do I use custom colors?"

### `mcp__tailwindcss__convert_css_to_tailwind`

Use when user has CSS they want to convert to Tailwind utility classes.

**Examples:**
- "Convert this CSS to Tailwind: display: flex; justify-content: center;"
- "What's the Tailwind equivalent of margin: 0 auto?"

### `mcp__tailwindcss__generate_component_template`

Use when user needs a component template with Tailwind styling.

**Examples:**
- "Generate a button component"
- "Create a card template"
- "Show me a navbar example"

---

## Official Documentation URLs

When MCP tools are unavailable, use WebFetch with these URLs to get current documentation:

### Getting Started
| Topic | URL |
|-------|-----|
| Installation | https://tailwindcss.com/docs/installation |
| Using Vite | https://tailwindcss.com/docs/installation/using-vite |
| Using PostCSS | https://tailwindcss.com/docs/installation/using-postcss |
| Tailwind CLI | https://tailwindcss.com/docs/installation/tailwind-cli |
| Editor Setup | https://tailwindcss.com/docs/editor-setup |
| Upgrade Guide | https://tailwindcss.com/docs/upgrade-guide |

### Core Concepts
| Topic | URL |
|-------|-----|
| Utility Classes | https://tailwindcss.com/docs/styling-with-utility-classes |
| Hover, Focus, States | https://tailwindcss.com/docs/hover-focus-and-other-states |
| Responsive Design | https://tailwindcss.com/docs/responsive-design |
| Dark Mode | https://tailwindcss.com/docs/dark-mode |
| Theme Variables | https://tailwindcss.com/docs/theme |
| Colors | https://tailwindcss.com/docs/colors |
| Custom Styles | https://tailwindcss.com/docs/adding-custom-styles |
| Functions & Directives | https://tailwindcss.com/docs/functions-and-directives |

### Layout
| Topic | URL |
|-------|-----|
| Display | https://tailwindcss.com/docs/display |
| Flexbox | https://tailwindcss.com/docs/flex |
| Grid | https://tailwindcss.com/docs/grid-template-columns |
| Gap | https://tailwindcss.com/docs/gap |
| Container | https://tailwindcss.com/docs/container |
| Position | https://tailwindcss.com/docs/position |
| Z-Index | https://tailwindcss.com/docs/z-index |

### Spacing
| Topic | URL |
|-------|-----|
| Padding | https://tailwindcss.com/docs/padding |
| Margin | https://tailwindcss.com/docs/margin |
| Space Between | https://tailwindcss.com/docs/space |

### Sizing
| Topic | URL |
|-------|-----|
| Width | https://tailwindcss.com/docs/width |
| Height | https://tailwindcss.com/docs/height |
| Min/Max Width | https://tailwindcss.com/docs/min-width |
| Min/Max Height | https://tailwindcss.com/docs/min-height |

### Typography
| Topic | URL |
|-------|-----|
| Font Family | https://tailwindcss.com/docs/font-family |
| Font Size | https://tailwindcss.com/docs/font-size |
| Font Weight | https://tailwindcss.com/docs/font-weight |
| Line Height | https://tailwindcss.com/docs/line-height |
| Text Color | https://tailwindcss.com/docs/text-color |
| Text Align | https://tailwindcss.com/docs/text-align |

### Backgrounds & Borders
| Topic | URL |
|-------|-----|
| Background Color | https://tailwindcss.com/docs/background-color |
| Background Image | https://tailwindcss.com/docs/background-image |
| Border Radius | https://tailwindcss.com/docs/border-radius |
| Border Width | https://tailwindcss.com/docs/border-width |
| Border Color | https://tailwindcss.com/docs/border-color |
| Box Shadow | https://tailwindcss.com/docs/box-shadow |

### Effects
| Topic | URL |
|-------|-----|
| Opacity | https://tailwindcss.com/docs/opacity |
| Shadow | https://tailwindcss.com/docs/box-shadow |
| Blur | https://tailwindcss.com/docs/blur |

### Transforms & Animation
| Topic | URL |
|-------|-----|
| Transform | https://tailwindcss.com/docs/transform |
| Scale | https://tailwindcss.com/docs/scale |
| Rotate | https://tailwindcss.com/docs/rotate |
| Translate | https://tailwindcss.com/docs/translate |
| Transition | https://tailwindcss.com/docs/transition-property |
| Animation | https://tailwindcss.com/docs/animation |

### Interactivity
| Topic | URL |
|-------|-----|
| Cursor | https://tailwindcss.com/docs/cursor |
| User Select | https://tailwindcss.com/docs/user-select |
| Scroll Behavior | https://tailwindcss.com/docs/scroll-behavior |

---

## Tailwind CSS v4 Core Syntax

**CRITICAL**: Tailwind v4 changed significantly from v3. Always use v4 syntax.

### CSS Entry Point

```css
@import "tailwindcss";
```

This single import replaces the old `@tailwind base; @tailwind components; @tailwind utilities;` directives.

### Theme Configuration (@theme directive)

All theme customization is done in CSS, not JavaScript:

```css
@theme {
  /* Colors - use oklch for better color manipulation */
  --color-primary: oklch(0.6 0.2 250);
  --color-primary-foreground: oklch(1 0 0);
  --color-secondary: oklch(0.5 0.02 250);
  --color-secondary-foreground: oklch(1 0 0);

  /* Semantic colors */
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-muted: oklch(0.95 0 0);
  --color-muted-foreground: oklch(0.4 0 0);
  --color-border: oklch(0.9 0 0);
  --color-destructive: oklch(0.55 0.25 25);

  /* Font families */
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "Fira Code", ui-monospace, monospace;

  /* Custom spacing (extends default scale) */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  /* Custom border radius */
  --radius-4xl: 2rem;
}
```

### Source Detection (@source directive)

Tailwind auto-detects most template files. Use `@source` for custom paths:

```css
@source "./templates/**/*.templ";
@source "./components/**/*.html";
@source "./src/**/*.{js,jsx,ts,tsx,vue,svelte}";
```

### Dark Mode (@variant directive)

```css
@variant dark {
  --color-background: oklch(0.145 0 0);
  --color-foreground: oklch(0.985 0 0);
  --color-muted: oklch(0.25 0 0);
  --color-muted-foreground: oklch(0.6 0 0);
  --color-border: oklch(0.3 0 0);
  --color-card: oklch(0.205 0 0);
}
```

### Component Layer (@layer components)

Extract repeated patterns:

```css
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors;
  }
  .btn-primary {
    @apply btn bg-primary text-primary-foreground hover:bg-primary/90;
  }
  .btn-secondary {
    @apply btn bg-secondary text-secondary-foreground hover:bg-secondary/90;
  }
  .card {
    @apply p-6 bg-card rounded-xl border border-border shadow-sm;
  }
}
```

### Plugins (@plugin directive)

```css
@plugin "@tailwindcss/typography";
```

---

## Best Practices

### Class Ordering Convention

Order utilities consistently for readability:

**Order:** layout → spacing → sizing → typography → colors → effects → interactive

```html
<!-- Good: Logical order -->
<div class="flex items-center gap-4 p-4 w-full text-sm text-gray-700 bg-white shadow-sm hover:bg-gray-50 transition-colors">

<!-- Bad: Random order -->
<div class="hover:bg-gray-50 flex bg-white p-4 text-sm shadow-sm w-full gap-4 items-center text-gray-700 transition-colors">
```

### Responsive Design

Mobile-first: base styles for mobile, add breakpoints for larger screens.

```html
<!-- Mobile first -->
<div class="w-full md:w-1/2 lg:w-1/3">

<!-- Breakpoints -->
sm: 640px   <!-- Small devices -->
md: 768px   <!-- Medium devices -->
lg: 1024px  <!-- Large devices -->
xl: 1280px  <!-- Extra large -->
2xl: 1536px <!-- 2X large -->
```

### Component Extraction Rule

Extract when a class combination appears **3+ times**:

```css
/* Instead of repeating in HTML */
@layer components {
  .flex-center {
    @apply flex items-center justify-center;
  }
  .text-muted {
    @apply text-sm text-muted-foreground;
  }
}
```

### Use Theme Variables

Always prefer theme variables over hardcoded values:

```html
<!-- Good: Uses theme variable -->
<div class="bg-primary text-primary-foreground">

<!-- Bad: Hardcoded color -->
<div class="bg-[#3b82f6] text-white">
```

### Accessibility

```html
<!-- Focus states -->
<button class="focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none">

<!-- Screen reader only -->
<span class="sr-only">Close menu</span>

<!-- Ensure contrast -->
<!-- Use oklch colors with sufficient lightness difference -->
```

---

## v4 Anti-Patterns to Avoid

### DO NOT USE (v3 patterns):

| Wrong (v3) | Correct (v4) |
|------------|--------------|
| `tailwind.config.js` | CSS `@theme { }` directive |
| `@tailwind base;` | `@import "tailwindcss";` |
| `@tailwind components;` | (included in import) |
| `@tailwind utilities;` | (included in import) |
| `darkMode: 'class'` in config | `@variant dark { }` in CSS |
| `theme.extend.colors` in JS | `--color-*` in @theme |
| `content: [...]` in JS | `@source "..."` in CSS |

### Common Mistakes

```html
<!-- Wrong: Inline styles when utility exists -->
<div style="display: flex; gap: 1rem;">
<!-- Correct -->
<div class="flex gap-4">

<!-- Wrong: px values when scale exists -->
<div class="p-[16px]">
<!-- Correct -->
<div class="p-4">

<!-- Wrong: Duplicate utilities -->
<div class="p-4 p-6">
<!-- Correct -->
<div class="p-6">

<!-- Wrong: Conflicting utilities -->
<div class="flex block">
<!-- Correct: Choose one -->
<div class="flex">
```

---

## Response Guidelines

When helping with Tailwind CSS:

1. **Always use v4 syntax** - No tailwind.config.js, use @theme in CSS
2. **Use MCP tools first** - Get current documentation before answering
3. **Prefer theme variables** - `bg-primary` not `bg-blue-500`
4. **Include accessibility** - Add focus-visible, sr-only where appropriate
5. **Show complete examples** - Include all necessary classes
6. **Explain class choices** - Help users understand why

### Example Response Flow

**User:** "How do I create a button with hover effect?"

**Response:**
1. Use `mcp__tailwindcss__get_tailwind_utilities` for button-related utilities
2. Provide example with proper class ordering:

```html
<button class="px-4 py-2 rounded-lg font-medium bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none transition-colors">
  Click me
</button>
```

3. Explain the classes used
4. Suggest extracting to component if used multiple times

---

## Quick Reference

### Spacing Scale
| Class | Size |
|-------|------|
| 1 | 0.25rem (4px) |
| 2 | 0.5rem (8px) |
| 3 | 0.75rem (12px) |
| 4 | 1rem (16px) |
| 5 | 1.25rem (20px) |
| 6 | 1.5rem (24px) |
| 8 | 2rem (32px) |
| 10 | 2.5rem (40px) |
| 12 | 3rem (48px) |
| 16 | 4rem (64px) |

### Common Patterns

```html
<!-- Centered content -->
<div class="flex items-center justify-center">

<!-- Card -->
<div class="p-6 bg-card rounded-xl border border-border shadow-sm">

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- Truncated text -->
<p class="truncate">Long text that will be truncated...</p>

<!-- Gradient background -->
<div class="bg-gradient-to-r from-primary to-secondary">

<!-- Fixed header -->
<header class="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-sm">
```

---

*For the latest documentation, always refer to https://tailwindcss.com/docs*

<!-- cache:end -->
