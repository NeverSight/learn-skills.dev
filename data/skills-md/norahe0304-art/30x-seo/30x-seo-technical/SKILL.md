---
name: 30x-seo-technical
description: >
  Technical SEO audit across 8 categories: crawlability, indexability, security,
  URL structure, mobile, Core Web Vitals, structured data, JS rendering.
  Schema deep validation → seo-schema. AI crawlers → seo-geo-technical.
  Use when user says "technical SEO", "crawl issues", "robots.txt", "Core Web Vitals".
allowed-tools:
  - WebFetch
  - Read
---

# Technical SEO Audit

## Categories

### 1. Crawlability
- robots.txt: exists, valid, not blocking important resources
- XML sitemap: exists, referenced in robots.txt, valid format
- Noindex tags: intentional vs accidental
- Crawl depth: important pages within 3 clicks of homepage
- JavaScript rendering: check if critical content requires JS execution
- Crawl budget: for large sites (>10k pages), efficiency matters

#### AI Crawler Management

> **For detailed checks, use `seo-geo-technical`**

This skill only checks basic robots.txt configuration. For detailed AI crawler checks (GPTBot, ClaudeBot, PerplexityBot), llms.txt generation, and SSR checks, use `seo-geo-technical`.

### 2. Indexability
- Canonical tags: self-referencing, no conflicts with noindex
- Duplicate content: near-duplicates, parameter URLs, www vs non-www
- Thin content: pages below minimum word counts per type
- Pagination: rel=next/prev or load-more pattern
- Hreflang: correct for multi-language/multi-region sites
- Index bloat: unnecessary pages consuming crawl budget

### 3. Security
- HTTPS: enforced, valid SSL certificate, no mixed content
- Security headers:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- HSTS preload: check preload list inclusion for high-security sites

### 4. URL Structure
- Clean URLs: descriptive, hyphenated, no query parameters for content
- Hierarchy: logical folder structure reflecting site architecture
- Redirects: no chains (max 1 hop), 301 for permanent moves
- URL length: flag >100 characters
- Trailing slashes: consistent usage

### 5. Mobile Optimization
- Responsive design: viewport meta tag, responsive CSS
- Touch targets: minimum 48x48px with 8px spacing
- Font size: minimum 16px base
- No horizontal scroll
- Mobile-first indexing: Google indexes mobile version. **Mobile-first indexing is 100% complete as of July 5, 2024.** Google now crawls and indexes ALL websites exclusively with the mobile Googlebot user-agent.

### 6. Core Web Vitals
- **LCP** (Largest Contentful Paint): target <2.5s
- **INP** (Interaction to Next Paint): target <200ms
  - INP replaced FID on March 12, 2024. FID was fully removed from all Chrome tools (CrUX API, PageSpeed Insights, Lighthouse) on September 9, 2024. Do NOT reference FID anywhere.
- **CLS** (Cumulative Layout Shift): target <0.1
- Evaluation uses 75th percentile of real user data
- Use PageSpeed Insights API or CrUX data if MCP available

### 7. Structured Data
- Detection: JSON-LD (preferred), Microdata, RDFa
- Validation against Google's supported types
- See seo-schema skill for full analysis

### 8. JavaScript Rendering
- Check if content visible in initial HTML vs requires JS
- Identify client-side rendered (CSR) vs server-side rendered (SSR)
- Flag SPA frameworks (React, Vue, Angular) that may cause indexing issues
- Verify dynamic rendering setup if applicable

#### JavaScript SEO — Canonical & Indexing Guidance (December 2025)

Google updated its JavaScript SEO documentation in December 2025 with critical clarifications:

1. **Canonical conflicts:** If a canonical tag in raw HTML differs from one injected by JavaScript, Google may use EITHER one. Ensure canonical tags are identical between server-rendered HTML and JS-rendered output.
2. **noindex with JavaScript:** If raw HTML contains `<meta name="robots" content="noindex">` but JavaScript removes it, Google MAY still honor the noindex from raw HTML. Serve correct robots directives in the initial HTML response.
3. **Non-200 status codes:** Google does NOT render JavaScript on pages returning non-200 HTTP status codes. Any content or meta tags injected via JS on error pages will be invisible to Googlebot.
4. **Structured data in JavaScript:** Product, Article, and other structured data injected via JS may face delayed processing. For time-sensitive structured data (especially e-commerce Product markup), include it in the initial server-rendered HTML.

**Best practice:** Serve critical SEO elements (canonical, meta robots, structured data, title, meta description) in the initial server-rendered HTML rather than relying on JavaScript injection.

### 9. IndexNow Protocol
- Check if site supports IndexNow for Bing, Yandex, Naver
- Supported by search engines other than Google
- Recommend implementation for faster indexing on non-Google engines

## Output

### Technical Score: XX/100

### Category Breakdown
| Category | Status | Score |
|----------|--------|-------|
| Crawlability | ✅/⚠️/❌ | XX/100 |
| Indexability | ✅/⚠️/❌ | XX/100 |
| Security | ✅/⚠️/❌ | XX/100 |
| URL Structure | ✅/⚠️/❌ | XX/100 |
| Mobile | ✅/⚠️/❌ | XX/100 |
| Core Web Vitals | ✅/⚠️/❌ | XX/100 |
| Structured Data | ✅/⚠️/❌ | XX/100 |
| JS Rendering | ✅/⚠️/❌ | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
