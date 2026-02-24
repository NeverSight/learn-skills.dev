---
name: cloudwerk-config
description: Configuration reference for Cloudwerk applications. Use when setting up cloudwerk.config.ts, choosing a renderer, configuring Vite plugins, or setting up path aliases. Triggers on tasks involving project configuration, renderer selection (hono-jsx vs react), Vite configuration, or Tailwind CSS setup.
license: MIT
metadata:
  author: squirrelsoft
  version: "0.1.0"
---

# Cloudwerk Configuration

Reference for `cloudwerk.config.ts` — the main configuration file for Cloudwerk applications.

## When to Apply

Reference these guidelines when:
- Creating a new Cloudwerk project
- Choosing between hono-jsx and react renderers
- Configuring Vite plugins (Tailwind CSS, etc.)
- Setting up path aliases
- Troubleshooting build or rendering issues

## Configuration File

Every Cloudwerk app has a `cloudwerk.config.ts` at the project root:

```typescript
import { defineConfig } from '@cloudwerk/core'

export default defineConfig({
  // Configuration options here
})
```

## Renderer Selection

### hono-jsx (Default)

Lightweight server-side rendering using Hono's built-in JSX. No client-side hydration or React hooks.

```typescript
import { defineConfig } from '@cloudwerk/core'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  ui: {
    renderer: 'hono-jsx',
  },
  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        '@': resolve(__dirname, './'),
      },
    },
  },
})
```

**Use hono-jsx when:**
- Building server-rendered pages without client interactivity
- Minimizing bundle size
- Building API-heavy applications with minimal UI

**JSX differences with hono-jsx:**
- Use `class` instead of `className`
- Use `for` instead of `htmlFor`
- No React hooks (`useState`, `useEffect`, etc.)
- No `'use client'` directive support

### react

Full React SSR with hydration support. Enables client components, React hooks, and interactive UIs.

```typescript
import { defineConfig } from '@cloudwerk/core'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  ui: {
    renderer: 'react',
  },
  vite: {
    plugins: [tailwindcss()],
  },
})
```

**Use react when:**
- Building interactive UIs with client-side state
- Using React hooks (`useState`, `useEffect`, `useRef`)
- Need `'use client'` components
- Using React component libraries

**JSX conventions with react:**
- Use `className` instead of `class`
- Use `htmlFor` instead of `for`
- Full React hooks support
- `'use client'` directive for client components

## Vite Configuration

The `vite` key accepts any Vite configuration:

```typescript
export default defineConfig({
  vite: {
    // Vite plugins
    plugins: [tailwindcss()],

    // Path aliases
    resolve: {
      alias: {
        '@': resolve(__dirname, './'),
        '@components': resolve(__dirname, './app/components'),
      },
    },

    // Build options
    build: {
      sourcemap: true,
    },
  },
})
```

## Quick Comparison

| Feature | hono-jsx | react |
|---------|----------|-------|
| CSS classes | `class` | `className` |
| Client components | No | Yes (`'use client'`) |
| React hooks | No | Yes |
| Bundle size | Smaller | Larger |
| Hydration | No | Yes |
| Best for | Content sites, APIs | Interactive apps |
