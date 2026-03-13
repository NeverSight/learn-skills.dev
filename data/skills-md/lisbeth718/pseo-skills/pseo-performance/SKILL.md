---
name: pseo-performance
description: Optimize a programmatic SEO application for Core Web Vitals, build performance, and scalability at 1000+ pages, including static generation, incremental regeneration, bundle optimization, and caching. Use when builds are slow, pages are large, Core Web Vitals scores are poor, or when scaling to many pages causes performance issues.
argument-hint: "[focus: all | build | cwv | bundle | caching]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Performance Optimization

Optimize the application for fast builds, excellent Core Web Vitals, and reliable performance at 1000+ page scale.

## Core Principles

1. **Static first**: Pre-render as many pages as possible at build time
2. **Incremental where needed**: Use ISR for pages that change frequently
3. **Minimal JavaScript**: Pages should be functional with minimal client-side JS
4. **Image optimization**: All images processed, sized, and lazy-loaded
5. **Cache aggressively**: Cache data fetches, API calls, and rendered output

## Optimization Areas

### 1. Static Generation Strategy

Choose the right rendering strategy for scale:

| Page Count | Strategy | Implementation |
|-----------|----------|----------------|
| < 500 | Full SSG | Generate all pages at build time |
| 500-5000 | SSG + ISR | Generate high-traffic pages at build, ISR for rest |
| 5000+ | ISR + on-demand | Generate on first request, revalidate periodically |

**Next.js App Router:**
```typescript
// Generate most important pages at build time
export async function generateStaticParams() {
  const topPages = await getTopPages(500);
  return topPages.map((p) => ({ slug: p.slug }));
}

// ISR for the rest
export const revalidate = 86400; // 24 hours
```

**Fallback handling:**
- Always configure a proper fallback (loading state, not blocking)
- Return `notFound()` for genuinely invalid slugs
- Set `dynamicParams = true` to allow ISR for pages not in `generateStaticParams`

### 2. Build Performance

For builds with many pages:

- **Parallelize data fetching**: Fetch all data once at the start, not per page
- **Memoize data access**: Use `React.cache()` or module-level caching to avoid redundant reads
- **Limit build concurrency**: If the build server has limited memory, configure worker limits
- **Incremental builds**: Use ISR to avoid rebuilding all pages on every deploy
- **Monitor build time**: Track build duration and set alerts for regressions

```typescript
// Memoize INDEX-TIER data at module level (lightweight: slug, title, category)
// NEVER cache full page content this way — see section 7 Memory Management
import { cache } from "react";

export const getAllIndexData = cache(async () => {
  // Returns PageIndex[] (~1KB per page) — safe to hold in memory
  return fetchAllIndexDataFromSource();
});
```

### 3. Core Web Vitals

**Largest Contentful Paint (LCP) < 2.5s:**
- Use `next/image` or equivalent for all images (automatic sizing, WebP, lazy loading)
- Preload the LCP image with `priority` prop or `<link rel="preload">`
- Minimize render-blocking CSS; inline critical CSS
- Serve from a CDN with edge caching

**Cumulative Layout Shift (CLS) < 0.1:**
- Set explicit `width` and `height` on all images and embeds
- Reserve space for dynamic content with CSS (min-height, aspect-ratio)
- Never inject content above the fold after initial render
- Use `font-display: swap` with size-adjusted fallback fonts

**Interaction to Next Paint (INP) < 200ms:**
- Minimize client-side JavaScript
- Defer non-critical scripts
- Avoid long tasks in event handlers
- Use `React.lazy()` for below-fold interactive components

### 4. Bundle Optimization

- **Analyze the bundle**: Run the framework's bundle analyzer
- **Tree-shake unused code**: Ensure imports are specific, not barrel imports
- **Code split by route**: Each page route should have its own chunk
- **Externalize large dependencies**: Move heavy libraries to CDN or dynamic imports
- **Remove unused dependencies**: Audit `package.json` for dead dependencies

```bash
# Next.js bundle analysis
ANALYZE=true next build
```

### 5. Caching Strategy

**Build-time caching:**
- Cache data source responses during build
- Use file-system or in-memory caching for computed values
- Cache static assets with immutable headers

**Runtime caching:**
- Set `Cache-Control` headers for static pages (e.g., `s-maxage=86400, stale-while-revalidate`)
- Use ISR revalidation to keep cached pages fresh
- Cache API responses with appropriate TTLs

**CDN caching:**
- Deploy behind a CDN (Vercel, Cloudflare, etc.)
- Configure cache keys to avoid unnecessary invalidation
- Use stale-while-revalidate for non-critical freshness

### 6. Image Optimization

- Use the framework's image component (next/image, etc.)
- Serve images in WebP/AVIF format
- Implement responsive `srcSet` for different viewports
- Lazy load below-fold images
- Set explicit dimensions to prevent layout shift
- Use a CDN image optimizer for dynamic images

### 7. Memory Management at Scale

Node.js default heap is ~1.5GB. At 1000+ pages with rich content, builds will OOM without explicit memory management.

**Increase Node.js heap when needed:**
```bash
# In build script or CI
NODE_OPTIONS="--max-old-space-size=4096" next build
```

**Limit build worker concurrency:**
```javascript
// next.config.js
module.exports = {
  experimental: {
    workerThreads: true,
    cpus: 2, // limit parallel workers to reduce total memory
  },
};
```

**Split data loading into light and heavy tiers:**
- **Index data** (slug, title, category, lastModified) — safe to hold all in memory. ~1KB per page = ~1MB for 1000 pages.
- **Full page data** (body content, FAQs, images) — load per-page, never cache the full set. ~50-500KB per page = 50MB-500MB for 1000 pages. This will OOM at scale if cached.

```typescript
// GOOD: Load full data per page
export async function getPageData(slug: string) {
  return fetchSinglePage(slug); // loads ~100KB, GC'd after render
}

// BAD: Cache all full data in memory
const ALL_DATA = await fetchAllPages(); // 500MB+ in memory for entire build
```

**Image processing concurrency:**
- Process images in batches, not all at once
- Use `sharp`'s built-in concurrency limiter: `sharp.concurrency(1)`
- If using `next/image` with remote images, limit simultaneous optimizations

**ISR cache eviction:**
- Next.js ISR caches rendered pages in memory (or disk). At 10,000+ pages, configure:
  - Disk-based cache (default in recent Next.js versions)
  - Set `isrMemoryCacheSize: 0` to disable in-memory ISR cache entirely if memory-constrained
  ```javascript
  // next.config.js
  module.exports = {
    experimental: {
      isrMemoryCacheSize: 0, // rely on disk cache only
    },
  };
  ```

**Sitemap generation:**
- For 50,000+ URLs, stream the sitemap XML to disk rather than building the full array in memory
- Use sitemap index files to split into chunks of 10,000-50,000 URLs each

**Monitor memory during builds:**
```bash
# Track peak memory usage
/usr/bin/time -v next build  # Linux
/usr/bin/time -l next build  # macOS
```

### 8. Publication Velocity and Rollout Strategy

Google's 2025 spam detection system (SpamBrain) monitors how fast pages are published. Dumping thousands of programmatic pages at once is a signal of scaled content abuse.

**Rollout strategy for new pSEO pages:**

| Page Count | Rollout Strategy |
|-----------|-----------------|
| < 100 | Deploy all at once — low risk |
| 100-500 | Deploy over 1-2 weeks in batches of 50-100 |
| 500-2000 | Deploy over 2-4 weeks, monitor Search Console for issues between batches |
| 2000-10K | Deploy over 4-8 weeks, validate indexing and ranking quality per batch |
| 10K-100K | ISR-only (don't pre-build). Submit sitemap in category waves over 8-16 weeks. Use data sufficiency gating to exclude thin pages. See **pseo-scale** for full strategy. |

**Implementation approaches:**

- **ISR with gradual seeding**: Generate pages on-demand via ISR but submit URLs to Google in batches via sitemap updates
- **Feature flag by category**: Launch one category at a time, monitor impact before launching the next
- **Draft/published status**: Mark pages as draft in the data layer, publish in batches by flipping status

**Monitor between batches:**
- Search Console: indexing status, manual actions, coverage issues
- Organic traffic: are existing pages maintaining rankings?
- Crawl stats: is Googlebot crawling the new pages?
- Core Web Vitals: are new pages performing well?

**Do NOT:**
- Publish 5,000+ pages in a single deploy
- Submit all URLs to Google Search Console at once via URL inspection
- Create all pages and then remove them quickly if they don't rank (signals low-quality churn)

### 9. Font Optimization

- Self-host fonts (or use `next/font`)
- Subset fonts to required character sets
- Use `font-display: swap` or `optional`
- Preload the primary font file

## Performance Checklist

- [ ] All pages can be reached within 3s on a 3G connection
- [ ] LCP < 2.5s on mobile
- [ ] CLS < 0.1
- [ ] INP < 200ms
- [ ] Build completes in reasonable time at current page count
- [ ] Build peak memory stays within server limits (check with `/usr/bin/time`)
- [ ] No full-dataset loading in memory (two-tier data pattern used)
- [ ] Bundle size per page < 200KB JS (compressed)
- [ ] Images use next-gen formats (WebP/AVIF)
- [ ] Cache-Control headers are set for all static assets
- [ ] No unused JavaScript in production bundle
- [ ] Publication rollout plan exists for 100+ new pages (not all at once)
- [ ] Search Console monitoring is configured between deployment batches

## Relationship to Other Skills

- **Optimizes**: pseo-templates (rendering strategy), pseo-data (fetch performance)
- **Independent of**: pseo-metadata, pseo-schema, pseo-linking (these are typically lightweight)
- **Extended by**: pseo-scale (CDN/edge architecture, build strategy at 100K, cache warm-up, crawl budget)
- **Validated by**: Lighthouse, WebPageTest, or framework-specific performance tools
