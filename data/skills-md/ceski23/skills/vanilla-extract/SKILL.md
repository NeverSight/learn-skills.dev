---
name: vanilla-extract
description: Comprehensive guide for styling React components with Vanilla Extract (Vite integration, typed styles, theming, composition, global APIs, recipes, dynamic runtime theming, and optional sprinkles). Use this skill when user tasks involve implementing or refactoring React component styling with Vanilla Extract, especially when emphasizing zero-runtime CSS generation, strong TypeScript ergonomics, scalable variants, and safe theming patterns.
license: MIT
---

# Vanilla Extract for React Components

Use this skill when implementing or refactoring React component styling with **Vanilla Extract**. It emphasizes zero-runtime CSS generation, strong TypeScript ergonomics, scalable variants, and safe theming patterns.

## When to Apply

Use this skill when tasks include:

- Setting up Vanilla Extract with **Vite + React**
- Creating component styles in `.css.ts` files
- Building typed variant systems (`styleVariants`, `recipes`)
- Implementing design tokens and themes (`createTheme`, `createThemeContract`)
- Runtime variable updates (`@vanilla-extract/dynamic`)
- Global/reset styles (`globalStyle`, `createGlobalTheme`)
- Utility-first typed atoms with optional `@vanilla-extract/sprinkles`

## Core Mental Model

Vanilla Extract generates static CSS at build time from TypeScript style definitions.

- `style(...)` => one scoped class
- `style([ ... ])` => composed class list, but still selector-safe inside Vanilla Extract
- Theme helpers create typed CSS variable contracts, then classes/selectors assign values
- Runtime theming via `@vanilla-extract/dynamic` only assigns values to pre-defined vars; it does **not** generate new CSS rules

## Setup (React + Vite)

1. Install base package:
   - `@vanilla-extract/css`
2. Install Vite integration:
   - `@vanilla-extract/vite-plugin` (dev dependency)
3. Add plugin in `vite.config.ts`:
   - `vanillaExtractPlugin()`

### Vite plugin identifiers

Choose identifier strategy depending on environment:

- `short`: compact hashes (smaller output)
- `debug`: human-readable class/var names in development
- custom function: fully custom naming based on `{ hash, filePath, debugId, packageName }`

Use `debug` during active development and switch to `short` for production when needed.

## File Conventions

- Put styles in `*.css.ts`
- Export class names and theme contracts from style modules
- Keep component logic in `*.tsx` and import classes/contracts from style files
- Co-locate styles next to components when component-specific; centralize tokens/themes in shared modules

## Authoring Styles Correctly

### Base style API

Use `style({ ... })` for scoped styles:

- CSS properties are camelCase
- numeric values get `px` unless property is unitless
- CSS vars must be nested inside `vars`
- media/supports/container/layer queries are nested (`@media`, `@supports`, `@container`, `@layer`)

### Selectors and pseudo-rules

- Simple pseudos (`:hover`, `::before`) can be top-level
- Complex selectors go under `selectors`
- Every complex selector must target `&` (current class)
- Don’t target unrelated descendants/classes from a style block; move relationship to the correct owner class
- If targeting global descendants is required (e.g. `"& a"`), use `globalStyle`

### Composition

Prefer `style([base, override])` for reuse. Composed classes can still be referenced in VE selectors safely.

## Variants for React Components

### `styleVariants`

Use `styleVariants` for simple named variants and prop mapping:

- Great for low-complexity variant axes
- Supports composition arrays
- Supports mapping form: `styleVariants(map, mapFn)`

Pattern:

- `variant: keyof typeof styles.variant`
- `className={styles.variant[variant]}`

### `@vanilla-extract/recipes`

Use recipes for richer component variants:

- `base`
- `variants`
- `compoundVariants`
- `defaultVariants`

Also use:

- `RecipeVariants<typeof recipeName>` for typed component props
- `recipeName.classNames` for introspection/debug tooling
- `recipeName.variants()` for metadata-like variant lists

Choose recipes when component API has multiple axes and combinations.

## Theming Strategy

### 1) Simple local themes: `createTheme`

Use when one file can define contract + theme values together.

Returns:

- theme class
- typed contract (`vars`) of CSS variable references

### 2) Code-splittable themes: `createThemeContract` + `createTheme`

Use for multiple themes loaded separately.

- `createThemeContract` defines variable shape without emitting theme CSS
- each theme file implements same contract via `createTheme(contract, values)`
- enables cleaner CSS code splitting for alternative themes

### 3) Global tokens/themes

Use for app-wide/global selectors:

- `createGlobalTheme(':root', ...)` for globally applied theme values (with locally scoped var names unless using global contract)
- `createGlobalThemeContract(...)` when stable variable names are needed across JS/non-JS boundaries
- optional variable naming formatter can enforce naming scheme/prefixing

### 4) Responsive/partial theme assignment

Use `assignVars` to assign all or partial contract sections, including within media queries.

This is ideal for responsive token values without defining separate full theme classes.

## Runtime Theming (`@vanilla-extract/dynamic`)

Use runtime APIs only when values are not known until runtime.

### `assignInlineVars`

- React-friendly inline style object for pre-defined vars/contracts
- with a **theme contract**, all contract vars must be provided (typed)
- without contract, `null`/`undefined` values can be omitted

### `setElementVars`

- imperative DOM assignment for dynamic updates
- same contract completeness behavior as above

Use this for user-customizable themes, CMS-driven colors, tenant branding, etc.

## Global Styling API Rules

### `globalStyle(selector, styleObject)`

Use **only for general styling and browser resets**.

**Appropriate for global styles:**
- `body`, `html` reset styles
- `::selection` styling
- Generic browser resets (margins, padding, box-sizing, etc.)
- Link underlines and basic resets applied globally

**NOT for global styles** (create component-specific styles instead):
- Headings (`h1`–`h6`) - style in dedicated heading components
- Buttons - use component recipes or `styleVariants`
- Links - style in dedicated link components or use `globalStyle` only for minimal resets, not visual styling
- Navigation elements - create nav-specific components

Component-specific styling ensures flexibility, prevents style conflicts, and makes design intent explicit.

Important constraint:

- `globalStyle` style object cannot use simple pseudo keys or `selectors` key (to avoid selector merge ambiguity)

Valid pattern:

- `globalStyle(`${container} a`, { ... })`

## Optional: Sprinkles Integration

Use `@vanilla-extract/sprinkles` when you need typed atomic utilities.

- define utility sets with `defineProperties`
- compose sets with `createSprinkles`
- combine sprinkle classlists with `style([sprinkles(...), {...custom}])`
- export `type Sprinkles = Parameters<typeof sprinkles>[0]` for typed utility props
- ensure `defineProperties` results are created in separate variables before passing to `createSprinkles` for correct typing

Useful advanced helpers:

- `createMapValueFn`
- `createNormalizeValueFn`
- `ConditionalValue`
- `RequiredConditionalValue`

## Practical Decision Tree

1. Need one-off scoped component style? -> `style`
2. Need simple named variants? -> `styleVariants`
3. Need multi-axis variants + compound/default behavior? -> `recipes`
4. Need compile-time themes? -> `createTheme` or `createThemeContract` + `createTheme`
5. Need global root tokens? -> `createGlobalTheme` / `createGlobalThemeContract`
6. Need runtime user/tenant values? -> `@vanilla-extract/dynamic`
7. Need utility prop system? -> `sprinkles`

## Common Pitfalls to Avoid

- Writing styles in non-`.css.ts` files
- Trying to place CSS variable assignments outside `vars`
- Invalid complex selectors that do not reference `&`
- Forcing global descendant targeting in `selectors` instead of `globalStyle`
- Using runtime theming APIs to create new CSS rules (they only assign existing vars)
- Accidentally coupling all themes in one bundle when code splitting is required (use contracts)
- Styling headings, buttons, or links globally instead of creating component-specific styles

## Suggested Component Pattern (React)

- `Component.css.ts`
  - base class(es)
  - variants (`styleVariants` or recipe)
  - exported variant type(s)
- `Component.tsx`
  - typed props
  - map props to classes
  - compose external `className`

## Simple Example: Button with 2 Recipe Variants + Theme Variables

Use this as a starter pattern for a themed React button.

```ts
// theme.css.ts
import { createTheme } from '@vanilla-extract/css';

export const vars = createGlobalTheme(':root', {
  color: {
    primaryBg: '#2563eb',
    primaryText: '#ffffff',
    secondaryBg: '#e5e7eb',
    secondaryText: '#111827',
  },
  radius: {
    md: '8px',
  },
  font: {
    sans: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  }
});
```

> [!IMPORTANT]
> Import this stylesheet as a side effect to include the styles in your CSS bundle.

```ts
// index.tsx
import './theme.css.ts';
```

```ts
// button.css.ts
import { recipe, type RecipeVariants } from '@vanilla-extract/recipes';
import { vars } from './theme.css';

export const button = recipe({
  base: {
    border: 0,
    borderRadius: vars.radius.md,
    cursor: 'pointer',
    fontFamily: vars.font.sans,
    fontWeight: 600,
    padding: '10px 14px',
  },
  variants: {
    variant: {
      primary: {
        background: vars.color.primaryBg,
        color: vars.color.primaryText,
      },
      secondary: {
        background: vars.color.secondaryBg,
        color: vars.color.secondaryText,
      },
    },
  },
  defaultVariants: {
    variant: 'primary',
  },
});

export type ButtonVariants = RecipeVariants<typeof button>;
```

```tsx
// Button.tsx
import type { ButtonHTMLAttributes } from 'react';
import { clsx } from 'clsx';
import { button, type ButtonVariants } from './button.css';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & ButtonVariants;

export const Button = ({ variant, className, ...props }: Props) => (
  <button
    className={clsx(button({ variant }), className)}
    {...props}
  />
);

// Usage:
// <Button>Primary</Button>
// <Button variant="secondary">Secondary</Button>
```

Notes:

- Keep `vars` in style modules, then reference them in recipes for fully typed tokens.
- Attach `themeClass` (if using `createTheme`) at app/root level if the whole app shares one theme or use `createGlobalTheme`.
- **Keep global styles minimal and reserved for resets only.** Never style headings (`h1`–`h6`), buttons, or other interactive elements globally. Instead, create component-specific styles via recipes, `styleVariants`, or dedicated style modules. This ensures consistent design and prevents cascade conflicts.

## Review Checklist

Before finalizing implementation, verify:

- Vite plugin configured and working
- Styles are in `.css.ts`
- Variant props are typed from style source (`keyof typeof` or `RecipeVariants`)
- Theme approach matches runtime/static requirements
- No invalid selector/global API usage
- No unnecessary runtime logic for styles that can be static
