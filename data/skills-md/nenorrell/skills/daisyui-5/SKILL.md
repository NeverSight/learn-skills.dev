---
name: daisyui-5
description: >
  DaisyUI 5 component library best practices, patterns, and usage for Tailwind CSS 4.
  Use when building UI with daisyUI class names, creating daisyUI-based layouts,
  styling HTML with daisyUI components, creating React wrapper components for daisyUI,
  or any task involving daisyUI (.html, .jsx, .tsx, .vue, .svelte files). Triggers on:
  daisyUI components (btn, card, modal, drawer, navbar, etc.), daisyUI color names
  (primary, secondary, base-100, etc.), daisyUI config (@plugin "daisyui"), daisy-meta.ts,
  generate-daisy-safelist, compound components wrapping daisyUI, or any UI task in a
  project using daisyUI/Tailwind CSS 4.
---

# daisyUI 5

CSS component library for Tailwind CSS 4. Provides semantic class names for common UI components.

## Install

1. Requires Tailwind CSS 4. No `tailwind.config.js` (deprecated in v4).
2. Install: `npm i -D daisyui@latest`
3. CSS file:
```css
@import "tailwindcss";
@plugin "daisyui";
```
4. CDN alternative:
```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

## Usage Rules

1. Style elements by combining: component class + part classes + modifier classes
2. Customize with Tailwind utility classes when daisyUI classes aren't sufficient (e.g. `btn px-10`)
3. Use `!` suffix on utilities as last resort for specificity (e.g. `btn bg-red-500!`)
4. If a component doesn't exist in daisyUI, build it with Tailwind utilities
5. Use Tailwind responsive prefixes for `flex`/`grid` layouts
6. Only use daisyUI class names or Tailwind utility classes — no custom CSS
7. Use `https://picsum.photos/{w}/{h}` for placeholder images
8. Don't add custom fonts unless necessary
9. Don't add `bg-base-100 text-base-content` to body unless necessary
10. Follow Refactoring UI best practices for design decisions

## Class Name Categories

- `component`: Required component class
- `part`: Child part of a component
- `style`: Sets specific style
- `behavior`: Changes behavior
- `color`: Sets specific color
- `size`: Sets specific size
- `placement`/`direction`: Sets position/direction
- `modifier`: Modifies component
- `variant`: Conditional prefix (`variant:utility-class`)

## Colors

### Semantic Color Names
| Color | Purpose |
|-------|---------|
| `primary` / `primary-content` | Main brand color / foreground on primary |
| `secondary` / `secondary-content` | Secondary brand color / foreground |
| `accent` / `accent-content` | Accent brand color / foreground |
| `neutral` / `neutral-content` | Non-saturated UI / foreground |
| `base-100/200/300` / `base-content` | Surface colors (light to dark) / foreground |
| `info` / `info-content` | Informative messages / foreground |
| `success` / `success-content` | Success messages / foreground |
| `warning` / `warning-content` | Warning messages / foreground |
| `error` / `error-content` | Error messages / foreground |

### Color Rules
1. Use daisyUI color names in Tailwind utilities: `bg-primary`, `text-base-content`
2. Colors change automatically per theme — no `dark:` prefix needed
3. Avoid Tailwind color names (e.g. `text-gray-800`) — they don't adapt to themes
4. Use `base-*` colors for page majority, `primary` for important elements
5. `*-content` colors must contrast well against their associated colors

## Config

```css
@plugin "daisyui"; /* no config */

@plugin "daisyui" {
  themes: light --default, dark --prefersdark;
  root: ":root";
  include: ;
  exclude: ;
  prefix: ;
  logs: true;
}
```

Config options: `themes` (enable/set default), `root`, `include`/`exclude` (components), `prefix` (e.g. `daisy-`), `logs`.

## Custom Themes

```css
@plugin "daisyui/theme" {
  name: "mytheme";
  default: true;
  prefersdark: false;
  color-scheme: light;
  --color-base-100: oklch(98% 0.02 240);
  --color-base-200: oklch(95% 0.03 240);
  --color-base-300: oklch(92% 0.04 240);
  --color-base-content: oklch(20% 0.05 240);
  --color-primary: oklch(55% 0.3 240);
  --color-primary-content: oklch(98% 0.01 240);
  --color-secondary: oklch(70% 0.25 200);
  --color-secondary-content: oklch(98% 0.01 200);
  --color-accent: oklch(65% 0.25 160);
  --color-accent-content: oklch(98% 0.01 160);
  --color-neutral: oklch(50% 0.05 240);
  --color-neutral-content: oklch(98% 0.01 240);
  --color-info: oklch(70% 0.2 220);
  --color-info-content: oklch(98% 0.01 220);
  --color-success: oklch(65% 0.25 140);
  --color-success-content: oklch(98% 0.01 140);
  --color-warning: oklch(80% 0.25 80);
  --color-warning-content: oklch(20% 0.05 80);
  --color-error: oklch(65% 0.3 30);
  --color-error-content: oklch(98% 0.01 30);
  --radius-selector: 1rem;
  --radius-field: 0.25rem;
  --radius-box: 0.5rem;
  --size-selector: 0.25rem;
  --size-field: 0.25rem;
  --border: 1px;
  --depth: 1;
  --noise: 0;
}
```

All CSS variables above are required. Colors can be OKLCH, hex, or other formats.

## Creating DaisyUI Components

Follow this workflow when creating or extending React components that wrap daisyUI. See [references/creating-components.md](references/creating-components.md) for detailed patterns, compound component examples, and test templates.

### 1. Resolve the components directory
Check `AGENTS.md` or `CLAUDE.md` for a `DAISY_COMPONENTS_DIR` variable. If not found, use `src/components/daisy`.

### 2. Ensure foundational files exist
Before creating any component, verify the project has the required infrastructure. If any are missing, create them from the bundled `scripts/` templates. See [references/creating-components.md](references/creating-components.md) for the full bootstrapping checklist and file contents.

Required files:
- `<DAISY_COMPONENTS_DIR>/daisy-meta.ts` — from bundled `scripts/daisy-meta.ts`
- `generators/daisy/generate-daisy-safelist.ts` — from bundled `scripts/generate-daisy-safelist.ts` (update the import path to point to daisy-meta.ts)
- `src/app/styles/daisy.css` — must import daisyUI plugin and the generated safelist
- `package.json` script `"generate:safelist"` — must run the generator
- The `daisy.css` file must be imported in the root layout or global CSS entry point

### 3. Register in daisy-meta.ts
Add the new component's capabilities to `COMPONENT_CAPABILITIES` in `<DAISY_COMPONENTS_DIR>/daisy-meta.ts`. Reference the daisyUI docs (see Component Reference below) for which modifiers it supports.

### 4. Create the component
- Follow patterns in existing `<DAISY_COMPONENTS_DIR>/daisy*` files
- Prefer compound components for multi-part daisyUI components (card, modal, dropdown, etc.)
- Each sub-component in a compound component gets its own file
- See [references/creating-components.md](references/creating-components.md) for compound component structure

### 5. Generate safelist
```bash
npm run generate:safelist
```
Generates `src/app/styles/daisy-safelist.css`.

### 6. Add tests
Use the project's test framework (check `package.json` for jest/vitest). Default to Jest + React Testing Library. Test: rendering, prop variations (colors, sizes, variants), compound component composition, and accessibility.

### 7. Extend the safelist generator
If the new component introduces a capability modifier not yet handled in `generate-daisy-safelist.ts`, update `buildClassList()` to iterate over it.

## Component Reference

Component docs are split by category. Read only the relevant file:

- **Layout components**: See [references/layout.md](references/layout.md)
  drawer, navbar, footer, hero, dock, divider, indicator, join, stack, fab
- **Data display**: See [references/data-display.md](references/data-display.md)
  card, list, table, stat, badge, avatar, chat, timeline, countdown, diff, carousel, hover-3d, hover-gallery, text-rotate
- **Input components**: See [references/input.md](references/input.md)
  button, input, textarea, select, checkbox, radio, toggle, range, rating, file-input, filter, fieldset, label, validator, calendar
- **Feedback & overlay**: See [references/feedback.md](references/feedback.md)
  alert, modal, toast, loading, skeleton, progress, radial-progress, status, steps, swap, tab
- **Navigation & chrome**: See [references/navigation.md](references/navigation.md)
  accordion, collapse, breadcrumbs, dropdown, tooltip, link, kbd, menu, mask, mockup-browser, mockup-code, mockup-phone, mockup-window, pagination, theme-controller
