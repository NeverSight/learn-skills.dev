---
name: css-workflow
description: CSS and styling workflow guidelines. Activate when working with CSS files (.css), Tailwind CSS, Stylelint, or styling-related tasks.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# CSS Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | Stylelint | `npx stylelint "**/*.css"` |
| Format | Prettier | `npx prettier --write "**/*.css"` |
| Dead code | PurgeCSS | `npx purgecss --css *.css --content *.html` |

## Tailwind CSS

RECOMMENDED over custom CSS for consistency and maintainability.

- SHOULD use utility classes for most styling needs
- MUST configure `tailwind.config.js` for project design tokens
- SHOULD use `@apply` sparingly - prefer utilities in markup
- MUST NOT use arbitrary values (`[123px]`) when design token exists
- SHOULD extend theme rather than override

**Class order:** Layout > Sizing > Spacing > Typography > Colors > Effects > Interactivity

## Native CSS Features

SHOULD prefer native CSS over Sass/preprocessors.

```css
/* CSS Variables */
:root { --color-primary: #3b82f6; }
.component { color: var(--color-primary, #3b82f6); }

/* Native Nesting */
.card {
  & .title { font-weight: bold; }
  &:hover { box-shadow: 0 4px 6px rgb(0 0 0 / 0.1); }
}

/* Container Queries */
.card-container { container-type: inline-size; }
@container (min-width: 400px) { .card { display: grid; } }
```

## Naming Conventions

SHOULD use BEM for custom CSS:

```css
.card { }           /* Block */
.card__title { }    /* Element */
.card--featured { } /* Modifier */
```

- MUST use lowercase `kebab-case`
- SHOULD use semantic names (`btn-primary` not `btn-blue`)
- MUST prefix utilities with `u-`, JS hooks with `js-`

## Organization

**Property order:** Positioning > Display/Box Model > Typography > Visual > Misc

**Mobile-first:** MUST use `min-width` media queries.

```css
.component {
  padding: 1rem;
  @media (min-width: 768px) { padding: 2rem; }
}
```

## Modern Features

```css
/* Grid - 2D layouts */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }

/* Flexbox - 1D layouts */
.flex { display: flex; align-items: center; gap: 1rem; }

/* Logical properties - i18n support */
.component { margin-inline: auto; padding-block: 1rem; }
```

## Dark Mode

MUST support via `prefers-color-scheme`:

```css
:root { --color-bg: #fff; --color-text: #1a1a1a; }
@media (prefers-color-scheme: dark) {
  :root { --color-bg: #1a1a1a; --color-text: #fff; }
}
```

Optional class toggle: `[data-theme="dark"] { --color-bg: #1a1a1a; }`

## Performance

- SHOULD inline critical above-the-fold CSS
- MUST NOT use `@import` in production (blocks parallel downloads)
- MUST remove unused CSS (PurgeCSS, Tailwind purge)
- SHOULD limit selector specificity (max 3 levels)
- MUST NOT use `!important` except for utilities

## Accessibility

### Focus States (REQUIRED)

```css
:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

### Reduced Motion (REQUIRED)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Color & Visibility

- MUST meet WCAG 2.1 AA contrast (4.5:1 text, 3:1 large text)
- SHOULD NOT rely on color alone to convey information

```css
.visually-hidden {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}
```
