---
name: seo-optimization
description: SEO best practices including meta tags, structured data (Schema.org), semantic HTML, performance, and multilingual SEO with hreflang
license: Apache-2.0
---

# SEO Optimization Skill

## Purpose
Ensures websites are optimized for search engines following modern SEO best practices with focus on technical SEO, structured data, and multilingual support.

## Meta Tags (MUST HAVE)
- `<title>` — 50-60 characters, unique per page
- `<meta name="description">` — 150-160 characters, unique per page
- `<link rel="canonical">` — Canonical URL
- Open Graph tags (og:title, og:description, og:image, og:url)
- Twitter Card tags

## Structured Data (Schema.org)
- Organization, WebSite, BreadcrumbList
- NewsArticle for news content
- FAQPage for FAQ sections
- Person entities with sameAs links

## Multilingual SEO (hreflang)
```html
<link rel="alternate" hreflang="en" href="/index.html">
<link rel="alternate" hreflang="sv" href="/index_sv.html">
<link rel="alternate" hreflang="x-default" href="/index.html">
```

## Semantic HTML for SEO
- Use `<h1>` once per page
- Proper heading hierarchy (h1→h2→h3)
- Semantic elements (article, nav, header, footer)
- Descriptive alt text on all images
- Descriptive anchor text

## Performance Requirements
- Lighthouse Performance ≥ 90
- LCP < 2.5s, FCP < 1.5s
- WebP images with fallbacks
- Minify HTML/CSS/JavaScript
- Lazy loading for images

## Sitemap & Robots
- Complete sitemap.xml with lastmod and priority
- Include hreflang alternates in sitemap
- Proper robots.txt configuration

## SEO Checklist
- [ ] Unique title and description per page
- [ ] Canonical URLs specified
- [ ] Schema.org structured data
- [ ] hreflang tags for all 14 languages
- [ ] sitemap.xml complete and submitted
- [ ] Mobile-friendly responsive design
- [ ] HTTPS enforced
- [ ] No broken links
