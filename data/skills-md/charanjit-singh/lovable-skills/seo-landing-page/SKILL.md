---
name: seo-landing-page
description: >-
  Use when building or auditing public marketing pages, landing pages, blogs,
  or SEO metadata (title, description, OG, headings). Not for authenticated
  app dashboards behind login.
---

# SEO landing page

Apply to **public** routes only (not app shell behind login). This skill is the **entry point** for marketing-page SEO.

Deep dives:

- [`seo-meta-tags-spa`](../seo-meta-tags-spa/) — per-route titles, OG, canonicals in a SPA
- [`seo-structured-data`](../seo-structured-data/) — Schema.org JSON-LD
- [`seo-ssr-and-prerendering`](../seo-ssr-and-prerendering/) — populated HTML for crawlers
- [`seo-sitemap-generation`](../seo-sitemap-generation/) — `sitemap.xml` + `robots.txt`
- [`seo-core-web-vitals`](../seo-core-web-vitals/) — LCP, INP, CLS
- [`programmatic-seo-pages`](../programmatic-seo-pages/) — templates at scale

## Per-page metadata

- Unique `<title>` (50–60 chars), meta description (150–160 chars).
- `og:title`, `og:description`, `og:image` (1200×630), `twitter:card`.
- Canonical URL when duplicates exist.
- One clear `h1`; logical `h2`/`h3` hierarchy (no skipped levels for styling).

## Content

- Primary keyword in `h1` and first paragraph naturally — no stuffing.
- Internal links to product, pricing, docs where relevant.
- Alt text on meaningful images.

## Technical

- Semantic HTML: `header`, `main`, `footer`, `article`.
- Fast LCP: optimize hero image (WebP, dimensions, lazy below fold).
- `/sitemap.xml` and `/robots.txt` for indexable sites.
- `json-ld` `Organization` or `WebSite` on homepage when appropriate.

## SPA metadata

Vite + React SPAs render an empty shell by default. For each public route, either:

- Set `<title>` and meta tags via React 19's built-in tags (or `react-helmet-async` on older versions), OR
- Use a pre-render/SSG step so crawlers see populated HTML.

Verify with `curl -A "Googlebot" https://example.com/ | grep -i '<title'` — title must be present in the raw HTML.

## Avoid

- Duplicate titles across routes.
- `h1` hidden for SEO only.
- Blocking render with huge unoptimized assets.

## Deliverable

When auditing, return a table: URL | issue | fix priority (high/medium/low).
