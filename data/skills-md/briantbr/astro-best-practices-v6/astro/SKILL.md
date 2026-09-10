---
name: astro
description: >
  Astro framework patterns for Islands Architecture, client directives (client:load, client:visible, client:idle, client:only, client:media), integrations (MDX, Tailwind, React/Vue/Svelte), View Transitions API, and deployment strategies.
  Use when building content-focused sites, implementing partial hydration with islands, setting up multi-framework projects, optimizing performance with zero-JS by default, or deploying static/SSR sites.
---

# Astro Framework

Astro 5.x framework for building fast, content-focused websites with Islands Architecture and zero JavaScript by default.

## Core Principles

### 1. Zero JavaScript by Default

Astro ships ZERO JavaScript unless you explicitly add a client directive.

```astro
<!-- Static HTML (no JS) -->
<Header />
<Footer />

<!-- Interactive island (JS loaded) -->
<Counter client:idle />
```

**Rule**: Only use client directives when components need hooks, state, or browser APIs.

### 2. Client Directives

| Directive | When to Use | Behavior |
|-----------|-------------|----------|
| `client:load` | Critical interaction needed immediately | Hydrates on page load |
| `client:idle` | Non-critical interactivity | Hydrates when browser idle |
| `client:visible` | Below the fold content | Hydrates when scrolled into view |
| `client:media="(query)"` | Responsive components | Hydrates when media query matches |
| `client:only="framework"` | Breaks during SSR | Skips SSR, client-only render |

**Decision tree**: Needs immediate interaction? → `client:load` | Non-critical? → `client:idle` | Below fold? → `client:visible` | Only on mobile/desktop? → `client:media` | Breaks SSR? → `client:only`

### 3. Multi-Framework Support

Mix React, Vue, Svelte in the same project:

```bash
npx astro add react vue svelte
```

```astro
---
import ReactForm from './Form.jsx';
import VueChart from './Chart.vue';
import SvelteCounter from './Counter.svelte';
---
<ReactForm client:idle />
<VueChart client:visible />
<SvelteCounter client:load />
```

---

## Quick Start

```bash
npm create astro@latest my-project
cd my-project
npx astro add tailwind react
npm run dev
```

---

## Project Structure

```
src/
├── components/       # .astro, .jsx, .vue, .svelte
├── layouts/          # Page layouts
├── pages/            # File-based routing
│   └── blog/[slug].astro
├── content/          # Content Collections (Markdown/MDX)
│   └── blog/         # Collection folders
├── styles/           # Global CSS
└── content.config.ts # Content collections schema (Astro 5+)
```

---

## Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://example.com',
  output: 'static',  // or 'server'
  integrations: [tailwind(), react()],
});
```

**Output modes (Astro 5):**
- `static` - Blog, docs, marketing (default). Use `export const prerender = false` for SSR pages.
- `server` - All pages SSR (requires adapter)

> **Astro 5 Change**: `output: 'hybrid'` was removed. The hybrid behavior is now the default in `static` mode.

---

## View Transitions

Enable SPA-like navigation with the Client Router:

```astro
---
import { ClientRouter } from 'astro:transitions';
---
<html>
  <head>
    <ClientRouter />
  </head>
  <body><slot /></body>
</html>
```

**Note**: In Astro 5, `ViewTransitions` was renamed to `ClientRouter`.

---

## Commands

```bash
npm run dev              # Start dev server (localhost:4321)
npm run build            # Build for production
npm run preview          # Preview production build
npx astro check          # TypeScript checks
```

---

## Core Patterns

Organized by priority - load on-demand as needed:

### High Priority (Common Use Cases)

- **[Content Collections](references/content-collections.md)** - Type-safe CMS for Markdown/MDX
- **[Image Optimization](references/images.md)** - Built-in Image and Picture components
- **[Server-Side Rendering](references/ssr.md)** - Dynamic routes, cookies, headers
- **[API Endpoints](references/api-endpoints.md)** - Server-side API routes, RSS, sitemap

### Medium Priority (Specific Features)

- **[Middleware](references/middleware.md)** - Request interception for auth, logging
- **[Pagination](references/pagination.md)** - Paginate large collections
- **[Environment & Config](references/environment-config.md)** - Environment variables, TypeScript helpers

### Low Priority (Advanced)

- **[Custom Integrations](references/integrations.md)** - Extend Astro's build process

---

## Real-World Recipes

Complete examples for common scenarios:

- **[Blog Setup](references/recipe-blog.md)** - Full blog with tags, RSS, layouts
- **[Multi-Step Forms](references/recipe-forms.md)** - React form with API integration
- **[Authentication](references/recipe-auth.md)** - Cookie-based auth with protected routes
- **[SEO](references/recipe-seo.md)** - Open Graph, Twitter Cards, structured data
- **[i18n](references/recipe-i18n.md)** - Multi-language support
- **[Dark Mode](references/recipe-dark-mode.md)** - Theme toggle with localStorage

---

## External Resources

- **Official Documentation**: https://docs.astro.build
- **Islands Architecture**: https://docs.astro.build/en/concepts/islands/
- **Client Directives**: https://docs.astro.build/en/reference/directives-reference/#client-directives
