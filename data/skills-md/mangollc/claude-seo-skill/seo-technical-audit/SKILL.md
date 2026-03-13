---
name: seo-technical-audit
description: |
  Full technical SEO site audit: crawlability, indexability, speed, mobile, schema markup
  validation with JSON-LD generation, internal linking analysis, Core Web Vitals, page speed
  optimization, crawl budget analysis, cannibalization detection, international SEO.

  USE FOR:
  - "technical SEO audit", "site audit", "SEO health check"
  - "check my site", "crawl errors", "indexing issues"
  - "schema markup", "JSON-LD", "structured data"
  - "core web vitals", "page speed", "mobile friendly"
  - "robots.txt", "sitemap", "canonical tags"
  - "internal linking", "meta tags audit"
  - "crawl budget", "thin content", "duplicate content"
  - "cannibalization", "keyword cannibalization"
  - "hreflang", "international SEO", "multilingual"
  - "page speed optimization", "render blocking"

  Uses firecrawl for crawling/scraping, curl for HTTP header checks.
  Multi-client: stores results in .seo/clients/{client}/technical/
---

# Technical SEO Audit

Load client context first. See seo-keywords [rules/client-setup.md](../seo-keywords/rules/client-setup.md).

## File Organization

```
technical/
├── audit-{date}.json              # Full audit results
├── sitemap-urls.txt               # All discovered URLs
├── homepage.md                    # Homepage content
├── crawl-data/                    # Raw crawl data
├── schema-markup/                 # Generated JSON-LD files
│   ├── homepage.jsonld
│   └── {page-slug}.jsonld
├── core-web-vitals-{date}.json    # CWV results
├── internal-links.json            # Link graph
├── cannibalization.json           # Cannibalization report
└── speed-audit-{date}.json        # Speed optimization report
```

## Full Audit Workflow

Run these sub-audits in parallel where possible, then compile into a single scored report.

### 1. Crawlability & URL Discovery

```bash
# Discover all URLs
firecrawl map {domain} -o .seo/clients/{slug}/technical/sitemap-urls.txt

# Check robots.txt
curl -sI "{domain}/robots.txt" -o .seo/clients/{slug}/technical/crawl-data/robots-headers.txt
firecrawl scrape "{domain}/robots.txt" -o .seo/clients/{slug}/technical/crawl-data/robots.txt

# Check XML sitemap
firecrawl scrape "{domain}/sitemap.xml" -o .seo/clients/{slug}/technical/crawl-data/sitemap.xml
```

**Check for:**
- Robots.txt blocks important pages
- Sitemap exists and is referenced in robots.txt
- Sitemap URLs match crawled URLs (missing pages = orphans or blocked)
- Status codes: sample 20-30 URLs with `curl -sI -o /dev/null -w "%{http_code}" {url}`
- Redirect chains: follow redirects with `curl -sIL {url}` — flag chains > 2 hops

### 2. HTTP Headers Audit

For homepage + 5-10 key pages:

```bash
curl -sI "{url}" -o .seo/clients/{slug}/technical/crawl-data/headers-{slug}.txt
```

**Check for:**
- `X-Robots-Tag` — any noindex/nofollow directives in headers
- `Link: <url>; rel="canonical"` — HTTP canonical vs HTML canonical conflicts
- `Content-Type` — proper charset (UTF-8)
- `Cache-Control` / `Expires` — caching configured
- `Strict-Transport-Security` — HTTPS enforcement
- `Content-Security-Policy` — security header present
- Redirect type: 301 (permanent) vs 302 (temporary) — 302s waste link equity

### 3. Meta Tags Audit

Scrape 10-20 key pages:

```bash
firecrawl scrape {url} --format markdown,links -o .seo/clients/{slug}/technical/crawl-data/page-{slug}.json
```

**For each page check:**

| Meta Tag | Check | Issue If |
|----------|-------|----------|
| `<title>` | Length 50-60 chars, keyword present, unique | Missing, too long/short, duplicate |
| `<meta name="description">` | Length 120-155 chars, keyword, CTA | Missing, too long/short, duplicate |
| `<link rel="canonical">` | Self-referencing, matches actual URL | Missing, points elsewhere, conflicts |
| `<meta name="robots">` | noindex/nofollow directives | Accidentally blocking important pages |
| `<meta property="og:title">` | Present, matches title | Missing for shareable pages |
| `<meta property="og:description">` | Present, compelling | Missing for shareable pages |
| `<meta property="og:image">` | Present, proper dimensions | Missing (no social preview) |
| `<meta name="twitter:card">` | Present (summary_large_image) | Missing Twitter Card data |
| `<link rel="alternate" hreflang>` | Correct language codes, reciprocal | Wrong codes, missing return tags |
| `<meta name="viewport">` | Present with `width=device-width` | Missing (not mobile-friendly) |

### 4. Schema Markup Validation

Scrape page HTML to find existing structured data:

```bash
firecrawl scrape {url} --html -o .seo/clients/{slug}/technical/crawl-data/html-{slug}.html
```

**Check for:**
- JSON-LD blocks in `<script type="application/ld+json">`
- Microdata attributes (`itemscope`, `itemtype`, `itemprop`)
- Valid schema.org types for page type
- Required properties present for each schema type
- No errors that would prevent rich results

### 5. JSON-LD Generation

Generate schema markup based on page type. Save to `schema-markup/` directory.

**LocalBusiness:**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{business_name}",
  "image": "{logo_url}",
  "address": { "@type": "PostalAddress", "streetAddress": "", "addressLocality": "", "addressRegion": "", "postalCode": "" },
  "telephone": "{phone}",
  "url": "{domain}",
  "openingHours": "Mo-Fr 08:00-17:00",
  "priceRange": "$$",
  "sameAs": ["{social_urls}"]
}
```

**Article:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": { "@type": "Person", "name": "{author}" },
  "datePublished": "{date}",
  "dateModified": "{modified_date}",
  "publisher": { "@type": "Organization", "name": "{brand}", "logo": { "@type": "ImageObject", "url": "{logo}" } },
  "image": "{featured_image}",
  "description": "{meta_description}"
}
```

**FAQPage:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "{question}", "acceptedAnswer": { "@type": "Answer", "text": "{answer}" } }
  ]
}
```

**Also generate when appropriate:** Product, HowTo, BreadcrumbList, WebSite (with SearchAction), Organization, Review/AggregateRating.

### 6. Internal Linking Analysis

```bash
# Get links from key pages
firecrawl scrape {url} --format links -o .seo/clients/{slug}/technical/crawl-data/links-{slug}.json
```

Repeat for homepage + top 20 pages. Build a link graph and check:

- **Orphan pages**: pages with 0 internal links pointing to them
- **Link depth**: pages should be reachable within 3 clicks from homepage
- **Link distribution**: flag pages with < 3 internal links or > 100
- **Anchor text**: over-optimized (same exact-match anchor) vs descriptive
- **Broken internal links**: 404s found in link extraction
- **Nofollow on internal links**: shouldn't nofollow your own pages

### 7. Core Web Vitals

If PageSpeed Insights API key is available:

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={api_key}" -o .seo/clients/{slug}/technical/crawl-data/psi-{slug}.json
```

If no API key, instruct user to get one (free) at https://developers.google.com/speed/docs/insights/v5/get-started.

**Metrics to extract:**
- **LCP (Largest Contentful Paint)**: Good < 2.5s, Poor > 4.0s
- **CLS (Cumulative Layout Shift)**: Good < 0.1, Poor > 0.25
- **INP (Interaction to Next Paint)**: Good < 200ms, Poor > 500ms
- **FCP (First Contentful Paint)**: Good < 1.8s
- **TTFB (Time to First Byte)**: Good < 800ms

### 8. Page Speed Optimization Playbook

Based on CWV results, provide specific fixes:

| Issue | Fix | Impact |
|-------|-----|--------|
| Render-blocking CSS/JS | Inline critical CSS, defer non-critical JS, use `async`/`defer` attributes | High (LCP) |
| Unoptimized images | Convert to WebP/AVIF, add width/height attributes, use responsive srcset, lazy-load below-fold | High (LCP, CLS) |
| No font display swap | Add `font-display: swap` to @font-face, preload key fonts | Medium (LCP, CLS) |
| Third-party script bloat | Audit and remove unused scripts, defer analytics/chat widgets | Medium (INP) |
| No server caching | Set Cache-Control headers, enable CDN | Medium (TTFB) |
| Large DOM size | Simplify markup, virtualize long lists | Medium (INP) |
| Layout shifts | Set explicit dimensions on images/ads/embeds, avoid inserting content above fold | High (CLS) |
| No compression | Enable gzip/brotli compression | Medium (TTFB) |

### 9. Image Optimization Audit

From scraped pages, check all `<img>` tags:

- **Alt text**: present on all images, descriptive (not "image1.jpg")
- **File format**: using modern formats (WebP, AVIF) vs legacy (PNG, JPG)
- **Dimensions**: `width` and `height` attributes set (prevents CLS)
- **Lazy loading**: `loading="lazy"` on below-fold images
- **Responsive**: `srcset` attribute for different screen sizes
- **File size**: flag images likely > 200KB without compression

### 10. Mobile Friendliness

Check from scraped HTML:
- `<meta name="viewport" content="width=device-width, initial-scale=1">` present
- No fixed-width elements (tables, iframes without responsive wrapper)
- Font sizes readable (base >= 16px)
- Tap targets adequate (buttons/links >= 48px)
- No horizontal scroll indicators

### 11. SERP Feature Eligibility

For each key page, assess which rich results it could qualify for:

| Rich Result | Requirements | Page Types |
|-------------|-------------|------------|
| FAQ | FAQPage schema, Q&A content | Service, product, blog |
| How-To | HowTo schema, step-by-step content | Tutorial, guide |
| Review Stars | AggregateRating schema | Product, service |
| Breadcrumbs | BreadcrumbList schema | All pages |
| Sitelinks Search | WebSite + SearchAction schema | Homepage |
| Video | VideoObject schema, embedded video | Blog, tutorial |
| Product | Product schema with price, availability | Product pages |

### 12. Crawl Budget Analysis

From the full URL list, identify pages wasting crawl budget:
- **Thin content**: pages with < 300 words (scrape sample to estimate)
- **Duplicate content**: URLs that are parameter variants of the same page
- **Faceted navigation**: filter/sort URLs creating combinatorial explosion
- **Tag/category pages**: low-value taxonomy pages
- **Pagination**: proper rel=next/prev or load-more implementation

Recommend: noindex tag pages, consolidate thin content, use canonical tags for parameter URLs, implement robots.txt blocks for faceted navigation.

### 13. International SEO / Hreflang

If client has `languages` or `regions` in config:
- Check all pages for `<link rel="alternate" hreflang="x-default">` tag
- Verify hreflang values match ISO 639-1 (language) and ISO 3166-1 (region) codes
- Confirm reciprocal tags (if page A references page B, page B must reference page A)
- Check URL structure: recommend subdirectory (`/en/`, `/fr/`) over subdomain or ccTLD for most cases
- Verify `<html lang="">` attribute matches page language
- Check for missing return tags (most common hreflang error)

### 14. Cannibalization Detection

Compare all indexed pages to identify keyword overlap:

```bash
# Get all page titles from sitemap
firecrawl scrape {url} --format markdown -o .seo/clients/{slug}/technical/crawl-data/page-{n}.md
```

**Detection method:**
1. Extract title tag and H1 from each page
2. Identify pages with similar/identical title keywords
3. Search Google for those keywords via firecrawl and check if multiple client pages appear
4. If 2+ pages from the same domain rank for the same query = cannibalization

**Recommendations per case:**
- **Merge**: if both pages are thin, combine into one comprehensive page with 301 redirect
- **Differentiate**: if pages serve different intents, adjust titles/content to target distinct keywords
- **Canonical**: if one is clearly stronger, canonical the weaker to the stronger

## Scoring

Calculate overall technical SEO health score (0-100):

| Category | Weight | Checks |
|----------|--------|--------|
| Crawlability | 15 | Robots.txt, sitemap, status codes, redirect chains |
| Meta Tags | 15 | Title, description, canonical, OG, robots |
| Schema Markup | 10 | Valid JSON-LD, appropriate types, required properties |
| Internal Linking | 15 | Orphan pages, link depth, anchor text, broken links |
| Core Web Vitals | 15 | LCP, CLS, INP scores |
| Image Optimization | 10 | Alt text, format, lazy loading, dimensions |
| Mobile | 10 | Viewport, responsive, tap targets, font sizes |
| Security | 5 | HTTPS, HSTS, CSP headers |
| Internationalization | 5 | Hreflang (if applicable, otherwise redistribute) |

Output: overall score, category scores, prioritized fix list with effort (low/medium/high) and impact (low/medium/high) for each issue.
