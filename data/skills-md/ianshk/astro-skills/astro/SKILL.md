---
name: astro
description: Skill for building static sites with the Astro web framework. Helps create Astro components and pages, set up content collections, optimize images, configure SEO, and deploy static builds. Use when the user needs to work with Astro, mentions .astro files, asks about static site generation (SSG), islands architecture, content collections, or deploying an Astro project.
license: MIT
compatibility: Astro v5+ with static output (output 'static'). Framework-agnostic — supports React, Svelte, Vue, or any UI framework.
metadata:
  author: 'Ian Callaghan'
  version: '1.0.0'
---

# Astro Skill

Reference for building static Astro sites (output: `'static'`). Covers architecture decisions, content collections, SEO, image optimization, pagination, and deployment patterns.

**Consult [docs.astro.build](https://docs.astro.build) and [llms.txt](https://docs.astro.build/llms.txt) for latest APIs when needed.**

---

## References

Read these files for detailed patterns and templates:

| Reference | What it covers |
|---|---|
| [`content-collections.md`](./references/content-collections.md) | Schemas (`z.image`, `z.enum`, `reference()`), querying, dynamic routes, `entry.body` |
| [`image-optimizations.md`](./references/image-optimizations.md) | `<Image />` component, downscaling tip, SVG components, aspect ratios |
| [`seo-checklist.md`](./references/seo-checklist.md) | Head component, per-page checklist, structured data (JSON-LD), hreflang, content rules |
| [`pagination.md`](./references/pagination.md) | `paginate()`, nested pagination, `page` prop |

---

## Architecture Rules

### 1. Astro-first

- `.astro` files for everything presentational — zero JS shipped to client.
- Framework components (`.tsx`, `.svelte`, `.vue`, etc.) only when interactivity is needed.

### 2. Minimal hydration

Use the lightest `client:*` directive that works:

| Directive | Use case |
|---|---|
| `client:load` | Critical above-the-fold interactivity |
| `client:idle` | Non-critical (modals, popovers) |
| `client:visible` | Below-the-fold widgets |
| `client:media` | Screen-size-specific UI (e.g. mobile sidebar toggle) |
| `client:only="<framework>"` | Browser-only APIs (e.g. localStorage, WebGL) |

### 3. Keep islands small

- Wrap **only** the interactive subtree in a framework component. Surrounding static markup stays in `.astro`.
- Pass data via props from the `.astro` parent — never refetch inside islands.

### 4. Fonts via Fontsource

Always install fonts locally via [Fontsource](https://fontsource.org/) npm packages — never Google Fonts CDN links.

Example if using Inter
```bash
npm install @fontsource-variable/inter
```

---

## Key Patterns

### Layout & Head

Use `src/layouts/Layout.astro` as the base layout. Import with `@/layouts/Layout.astro`.

Use `src/components/Head.astro` for SEO meta tags, Open Graph, Twitter Cards, canonical URLs, and JSON-LD structured data. Import it inside your layout — see [`seo-checklist.md`](./references/seo-checklist.md) for the full component and per-page checklist.

### Sitemap

Always include `@astrojs/sitemap` — it auto-generates `sitemap-index.xml` at build time. Install and add it to `integrations` in `astro.config.mjs`:

```bash
npx astro add sitemap
```

Exclude admin pages, API routes, and utility pages from the sitemap.

### robots.txt

Create `src/pages/robots.txt.ts` — Astro will build it into a static `robots.txt` file at the site root. It dynamically references the sitemap URL using `Astro.site`:

```typescript
import type { APIRoute } from 'astro';

const getRobotsTxt = (sitemapURL: URL) => `\
User-agent: *
Allow: /

Sitemap: ${sitemapURL.href}
`;

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL('sitemap-index.xml', site);
  return new Response(getRobotsTxt(sitemapURL));
};
```

This requires `site` to be set in `astro.config.mjs` so the sitemap URL resolves correctly.

### Image optimization

Always use `<Image />` from `astro:assets` — not `<img>` tags. Set explicit `width`/`height` to downscale large source images (e.g., 10000×10000 → 1024×1024 = smaller WebP output).

### Content collections (v5+)

- Config at `src/content.config.ts` (NOT `src/content/config.ts`)
- Every collection needs a `loader` (use `glob` from `astro/loaders`)
- Use `z.image()` for validated, optimized image fields
- Use `z.enum()` for constrained values instead of booleans
- Use `reference()` for relations between collections

### Static output

- Always use `output: 'static'` (the default) — all pages are pre-rendered to HTML at build time.
- Do NOT use `output: 'hybrid'` — removed in Astro v5.
- Do NOT use `output: 'server'` or SSR adapters.

### Trailing slashes

- Set `trailingSlash: 'always'` in `astro.config.mjs` to enforce trailing slashes on all generated URLs.
- Always use trailing slashes in internal links (`/about/` not `/about`) to avoid duplicate content issues.
