---
name: mantine-ui
description: Build React UIs with Mantine components, theming, and hooks. Use when adding or using Mantine UI, @mantine/core, MantineProvider, Mantine forms, dates, or when the user mentions Mantine, mantine.dev, or Mantine components.
---

# Mantine UI

React-only component library (120+ components, 70+ hooks). Use for forms, overlays, dates, charts, notifications, and theming. Docs: [mantine.dev](https://mantine.dev). Pre-built examples: [ui.mantine.dev](https://ui.mantine.dev).

## Quick setup (new or existing app)

1. **Install core packages**
   - Required: `@mantine/core` and `@mantine/hooks`
   - Optional by feature: `@mantine/form`, `@mantine/dates`, `@mantine/notifications`, etc. (see [reference.md](reference.md))

2. **PostCSS** (required for Mantine styles)
   - Install: `postcss`, `postcss-preset-mantine`, `postcss-simple-vars` (as devDependencies)
   - Add `postcss.config.cjs` at project root:
   ```js
   module.exports = {
     plugins: {
       'postcss-preset-mantine': {},
       'postcss-simple-vars': {
         variables: {
           'mantine-breakpoint-xs': '36em',
           'mantine-breakpoint-sm': '48em',
           'mantine-breakpoint-md': '62em',
           'mantine-breakpoint-lg': '75em',
           'mantine-breakpoint-xl': '88em',
         },
       },
     },
   };
   ```

3. **Import styles once** (e.g. in `_app.tsx`, `main.tsx`, or root layout)
   ```ts
   import '@mantine/core/styles.css';
   // Add per-package only if used: '@mantine/dates/styles.css', etc.
   ```

4. **Wrap app with MantineProvider**
   ```tsx
   import { createTheme, MantineProvider } from '@mantine/core';

   const theme = createTheme({ /* optional overrides */ });

   export default function App() {
     return (
       <MantineProvider theme={theme}>
         {/* app */}
       </MantineProvider>
     );
   }
   ```

5. **SSR (Next.js app router, etc.)** – avoid hydration flash: add `ColorSchemeScript` in `<head>` and spread `mantineHtmlProps` on `<html>`:
   ```tsx
   import { ColorSchemeScript, mantineHtmlProps } from '@mantine/core';

   <html lang="en" {...mantineHtmlProps}>
     <head>
       <ColorSchemeScript />
       {/* ... */}
     </head>
     <body>...</body>
   </html>
   ```

## Conventions

- **Single MantineProvider** at the root; do not nest another MantineProvider unless intentionally overriding theme.
- **Component styling**: Prefer theme/settings (e.g. `createTheme`, component props). Use [Styles API](https://mantine.dev/styles/styles-api/) for targeting internal parts; use [responsive styles](https://mantine.dev/styles/responsive/) for breakpoints.
- **Polymorphic components**: Many components accept a root element via props (e.g. `component`, `renderRoot`) – see [Polymorphic components](https://mantine.dev/guides/polymorphic/).
- **Forms**: Use `@mantine/form` with Mantine inputs for validation and state; see [Form documentation](https://mantine.dev/form/).
- **Extra packages**: Install only the packages you use; each may need its own CSS import (e.g. `@mantine/dates/styles.css`).

## Framework notes

- **Next.js**: Prefer the [Next.js guide](https://mantine.dev/guides/next/) (app or pages router). Use templates from [getting started](https://mantine.dev/getting-started/) when starting from scratch.
- **Vite**: See [Vite guide](https://mantine.dev/guides/vite/). Do not use Create React App for new projects; Mantine recommends Vite or Next.js.

## When in doubt

- Check the component’s page on mantine.dev (e.g. Button, TextInput, Modal).
- For full examples and copy-paste snippets: [ui.mantine.dev](https://ui.mantine.dev).
- For package list and CSS imports: [reference.md](reference.md).
