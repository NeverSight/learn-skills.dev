---
name: seo-technical-audit
description: Expert guide for technical SEO auditing. Use when checking crawlability, indexing issues, page speed, Core Web Vitals, mobile-friendliness, HTTPS configuration, robots.txt, XML sitemaps, canonical tags, hreflang, redirect chains, HTTP status codes, or diagnosing technical SEO problems.
---

# Technical SEO Audit

---

## Crawlability

Search engines must be able to discover and access your pages. Crawlability issues block indexing entirely.

### Robots.txt
Controls which URLs crawlers can access.

```
# Allow all crawlers access to everything
User-agent: *
Allow: /

# Block specific paths
User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /staging/
Disallow: /*?sort=
Disallow: /*?filter=

# Sitemap reference (always include)
Sitemap: https://example.com/sitemap.xml
```

**Critical rules:**
- Never block CSS/JS files (Google needs them to render pages)
- Never block important content paths accidentally
- Test with `analyze_robots_txt` before deploying changes
- `Crawl-delay` is ignored by Google (honored by Bing/Yandex)

### Meta Robots & X-Robots-Tag
Page-level crawl and index directives.

| Directive | Effect |
|-----------|--------|
| `index` | Allow indexing (default) |
| `noindex` | Prevent indexing — removes from search results |
| `follow` | Follow links on this page (default) |
| `nofollow` | Don't follow any links on this page |
| `noarchive` | Don't show cached version |
| `nosnippet` | Don't show text snippet in results |
| `max-snippet:N` | Limit snippet to N characters |
| `max-image-preview:large` | Allow large image previews |

```html
<!-- In HTML head -->
<meta name="robots" content="noindex, follow">

<!-- Via HTTP header (for non-HTML files) -->
X-Robots-Tag: noindex, nofollow
```

**MCP Tool:** `analyze_page` extracts both meta robots and HTTP header directives.

---

## Indexing

### Canonical Tags
The definitive way to tell search engines which URL is the preferred version.

**Rules:**
- Every indexable page: self-referencing canonical
- Absolute URLs only (`https://example.com/page`, not `/page`)
- Must be consistent: canonical URL must return 200 (not redirect or 404)
- One canonical per page (if multiple, Google uses the first)
- HTTP header canonical overrides HTML canonical if both present

### Noindex vs Canonical
| Scenario | Use |
|----------|-----|
| Page should never appear in search | `noindex` |
| Duplicate page, prefer another version | `canonical` to preferred version |
| URL parameter variants | `canonical` to clean URL |
| Paginated content | Self-referencing canonical on each page |

### Sitemap Submission
- Submit via Google Search Console
- All indexable pages should be in the sitemap
- Noindex pages should NOT be in the sitemap
- Keep sitemaps under 50,000 URLs / 50MB per file (use sitemap index for larger sites)

**MCP Tools:** `analyze_sitemap` validates structure, `gsc_sitemaps` checks submission status.

---

## Core Web Vitals

Google's page experience signals. Measured from real user data (CrUX) and lab data (Lighthouse).

### Thresholds (2024+)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

### LCP Optimization
Largest Contentful Paint measures when the largest visible element finishes rendering.

**Common causes of poor LCP:**
1. Slow server response (TTFB > 800ms) → optimize server, use CDN
2. Render-blocking resources → defer non-critical CSS/JS
3. Slow resource load → optimize/compress LCP image, use `preload`
4. Client-side rendering → server-side render critical content

**Quick wins:**
- Preload LCP image: `<link rel="preload" href="hero.webp" as="image">`
- Use CDN for static assets
- Optimize server response (caching, database queries)
- Avoid lazy-loading the LCP element

### INP Optimization
Interaction to Next Paint measures responsiveness to user input.

**Common causes of poor INP:**
1. Long JavaScript tasks blocking main thread → break into smaller tasks
2. Heavy event handlers → debounce, use `requestAnimationFrame`
3. Large DOM size → reduce DOM nodes (target < 1,500)
4. Third-party scripts → defer or lazy-load

### CLS Optimization
Cumulative Layout Shift measures visual stability.

**Common causes of poor CLS:**
1. Images without dimensions → always set `width` and `height`
2. Ads/embeds without reserved space → use `aspect-ratio` or `min-height`
3. Web fonts causing FOIT/FOUT → use `font-display: swap` + preload
4. Dynamically injected content → reserve space before injection

**MCP Tool:** `check_core_web_vitals` returns all metrics with specific optimization suggestions.

---

## Page Speed Optimization

Beyond Core Web Vitals, overall page speed impacts user experience and crawl budget.

### Critical rendering path
1. Minimize render-blocking resources (critical CSS inline, defer JS)
2. Enable compression (Brotli preferred, gzip minimum)
3. Set cache headers (`Cache-Control: max-age=31536000` for static assets)
4. Use HTTP/2 or HTTP/3
5. Minimize main-thread work (reduce JS execution time)

### Image optimization
- Use modern formats (WebP/AVIF)
- Serve responsive images (`srcset`)
- Lazy load below-the-fold images
- Compress aggressively (80-85% quality)

### Resource hints
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" href="/critical.css" as="style">
<link rel="prefetch" href="/next-page.html">
<link rel="dns-prefetch" href="https://analytics.example.com">
```

---

## Mobile-Friendliness

Google uses mobile-first indexing — the mobile version of your site is what gets indexed.

### Requirements
- Viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Responsive design (content adapts to screen size)
- No horizontal scrolling
- Tap targets: minimum 48x48px with 8px spacing
- Font size: minimum 16px for body text
- No intrusive interstitials (popups covering content)
- Content parity: mobile version has same content as desktop

**MCP Tool:** `check_mobile_friendly` evaluates all mobile usability factors.

---

## HTTPS & Security

### HTTPS requirements
- All pages served over HTTPS (no HTTP pages in index)
- Valid SSL certificate (not expired, correct domain)
- No mixed content (HTTPS page loading HTTP resources)
- HSTS header recommended: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- HTTP pages 301 redirect to HTTPS

### Common HTTPS issues
| Issue | Impact | Fix |
|-------|--------|-----|
| Mixed content | Medium | Update all resource URLs to HTTPS |
| Expired certificate | Critical | Renew SSL certificate immediately |
| HTTP pages indexed | High | 301 redirect HTTP → HTTPS + update canonical |
| Missing HSTS | Low | Add HSTS header |

---

## Redirects

### Redirect types
| Code | Type | When to Use | SEO Impact |
|------|------|-------------|------------|
| 301 | Permanent | URL changed permanently, content moved | Passes ~95% link equity |
| 302 | Temporary | Temporary move (A/B test, maintenance) | Does not pass link equity |
| 307 | Temporary (strict) | Same as 302 but preserves HTTP method | Does not pass link equity |
| 308 | Permanent (strict) | Same as 301 but preserves HTTP method | Passes link equity |

### Redirect issues
- **Redirect chains:** A → B → C → D. Maximum 2 hops recommended. Fix by pointing A directly to D.
- **Redirect loops:** A → B → A. Critical error — page becomes inaccessible.
- **Soft 404s:** Page returns 200 but shows "not found" content. Should return actual 404.
- **302 where 301 needed:** Temporary redirect for permanent move wastes link equity.

---

## XML Sitemaps

### Requirements
- Located at `/sitemap.xml` (or referenced in robots.txt)
- Valid XML format
- Only indexable pages (no noindex, no 404s, no redirects)
- Include `<lastmod>` with accurate dates (ISO 8601)
- Maximum 50,000 URLs per sitemap file
- Maximum 50MB uncompressed per file
- Use sitemap index for larger sites

### Validation
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**MCP Tool:** `analyze_sitemap` parses, validates, and reports issues.

---

## Hreflang (International SEO)

For multi-language or multi-region sites. Tells Google which language/region version to show.

### Syntax
```html
<link rel="alternate" hreflang="en-us" href="https://example.com/page">
<link rel="alternate" hreflang="en-gb" href="https://example.co.uk/page">
<link rel="alternate" hreflang="es" href="https://example.com/es/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```

### Rules
- **Bidirectional:** If page A references page B, page B must reference page A
- **Self-referencing:** Each page must include a hreflang pointing to itself
- **x-default:** Include for the fallback/language selector page
- **Return tags:** Every referenced URL must return the same hreflang set
- Use ISO 639-1 language codes, optionally with ISO 3166-1 region codes

---

## HTTP Status Codes (SEO Impact)

| Code | Meaning | SEO Action |
|------|---------|------------|
| 200 | OK | Expected for all indexable pages |
| 301 | Moved Permanently | Passes link equity. Use for permanent URL changes |
| 302 | Found (Temporary) | Does NOT pass link equity. Use only for temporary moves |
| 304 | Not Modified | Good — efficient caching |
| 404 | Not Found | Remove from sitemap, fix internal links pointing here |
| 410 | Gone | Permanently removed. Stronger signal than 404 for deindexing |
| 500 | Server Error | Fix immediately — blocks crawling and indexing |
| 503 | Service Unavailable | Temporary. Google retries. Use for planned maintenance |

---

## Technical Audit Workflow

Recommended order for a complete technical audit:

1. **Crawlability:** `analyze_robots_txt` → check for blocking issues
2. **Sitemap:** `analyze_sitemap` → validate structure and URLs
3. **Page-level:** `analyze_page` → meta robots, canonical, redirects, status
4. **Performance:** `check_core_web_vitals` → LCP, INP, CLS scores
5. **Mobile:** `check_mobile_friendly` → viewport, tap targets, fonts
6. **Schema:** `extract_schema` → structured data validation
7. **GSC data:** `gsc_index_coverage` → real indexing status from Google

See [ERROR_CATALOG.md](ERROR_CATALOG.md) for the complete issue catalog.
See [AUDIT_WORKFLOW.md](AUDIT_WORKFLOW.md) for detailed audit methodology.
See [HTTP_STATUS_REFERENCE.md](HTTP_STATUS_REFERENCE.md) for complete status code reference.
