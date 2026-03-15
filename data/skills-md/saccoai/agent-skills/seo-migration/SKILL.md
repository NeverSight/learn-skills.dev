---
name: seo-migration
description: SEO preservation during website migrations — redirect mapping, canonical URLs, sitemap generation, structured data, meta tags, and Search Console verification. Use when rebuilding a site to ensure zero SEO loss from URL changes, content moves, or domain switches.
---

This skill ensures zero SEO loss during a website migration. It maps old URLs to new ones, generates redirects, preserves metadata, creates sitemaps, and validates structured data.

The user provides: the original site URL, the new site URL (or route structure), and the type of migration (same domain redesign, domain change, or platform migration).

## Migration Types

| Type | What changes | SEO risk |
|------|-------------|----------|
| **Redesign** (same domain) | URLs may change, content restructured | Medium — redirects critical |
| **Domain change** | Entire domain moves (old.com → new.com) | High — 301s + Search Console change of address |
| **Platform migration** | CMS/framework change (WordPress → Next.js) | High — URL patterns often change completely |
| **HTTPS migration** | HTTP → HTTPS | Low — but every URL needs redirect |

## SEO Migration Checklist

### Step 1: Crawl & Map URLs

Crawl the original site and build a complete URL inventory:

```
1. Fetch sitemap.xml (and any sitemap index files)
2. Crawl all pages recursively from the homepage
3. Check Google Search Console for indexed URLs (if available)
4. Check robots.txt for disallowed paths

Output: url-inventory.csv
| Original URL | Status | Title | Indexable | New URL | Redirect Type |
```

**For each original URL, determine:**
- Keep as-is (same URL on new site)
- Redirect to new URL (301 permanent)
- Merge into another page (301 to merged page)
- Remove intentionally (410 Gone, or 301 to nearest relevant page)

### Step 2: Generate Redirect Map

Create the redirect configuration for the target platform:

#### Next.js (next.config.ts)
```typescript
async redirects() {
  return [
    { source: '/old-page', destination: '/new-page', permanent: true },
    { source: '/blog/:slug', destination: '/articles/:slug', permanent: true },
    // ... all redirects
  ];
}
```

#### Vercel (vercel.json)
```json
{
  "redirects": [
    { "source": "/old-page", "destination": "/new-page", "permanent": true }
  ]
}
```

#### Nginx
```nginx
location /old-page { return 301 /new-page; }
```

**Rules:**
- Always use **301** (permanent) for SEO migrations, never 302
- Use pattern matching for bulk redirects (e.g., `/blog/:slug` → `/articles/:slug`)
- Never redirect to a page that itself redirects (no chains)
- Never create redirect loops
- Redirect old sitemap.xml URL to new sitemap location

### Step 3: Preserve Metadata

For **every page** on the new site, ensure:

```
✅ <title> — Preserve original or improve (50-60 chars)
✅ <meta name="description"> — Preserve original or improve (150-160 chars)
✅ <link rel="canonical"> — Points to the correct canonical URL
✅ <html lang="xx"> — Correct language attribute
✅ Open Graph tags — og:title, og:description, og:image, og:url
✅ Twitter Card tags — twitter:card, twitter:title, twitter:description
✅ Heading hierarchy — H1 present and unique per page, no skipped levels
```

Generate a metadata comparison report:

```markdown
| Page | Original Title | New Title | Match |
|------|---------------|-----------|-------|
| / | "Site — Home" | "Site — Home" | ✅ |
| /about | "About Us" | "Chi Siamo" | ⚠️ Changed |
```

### Step 4: Structured Data

Preserve or add schema.org structured data:

```
1. Extract existing JSON-LD / microdata from original site
2. Map to equivalent structured data on new site
3. Add missing structured data where beneficial:
   - Organization (homepage)
   - BreadcrumbList (all pages)
   - Article (blog posts)
   - LocalBusiness (contact page)
   - Person (biography)
   - Book (publications)
```

Validate with Google's Rich Results Test or Schema.org validator.

### Step 5: Sitemap & Robots

#### sitemap.xml
Generate a new sitemap with all pages on the new site:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-02-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- ... all pages -->
</urlset>
```

For Next.js, generate via `app/sitemap.ts`:
```typescript
import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://example.com', lastModified: new Date(), priority: 1 },
    // ...
  ];
}
```

#### robots.txt
```
User-agent: *
Allow: /
Sitemap: https://example.com/sitemap.xml
```

For Next.js, generate via `app/robots.ts`:
```typescript
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

### Step 6: Validation

After deployment, verify:

```
1. Test EVERY redirect — curl -I each old URL, confirm 301 to correct new URL
2. Verify no redirect chains (A→B→C should be A→C)
3. Verify no redirect loops
4. Verify no 404s for previously indexed URLs
5. Confirm sitemap.xml is accessible and valid
6. Confirm robots.txt allows crawling
7. Test canonical URLs resolve correctly
8. Validate structured data with Rich Results Test
9. Check Google Search Console for crawl errors (after a few days)
```

Generate `seo-migration-report.md`:

```markdown
# SEO Migration Report

## Redirects
- Total: 47
- Tested: 47
- Passing: 45
- ❌ /old-blog/post-3 → 404 (redirect target missing)
- ❌ /events → /events → /events/archive (chain detected)

## Metadata
- Pages with matching titles: 12/12
- Pages with descriptions: 12/12
- Pages with canonical: 12/12
- Pages with OG tags: 12/12

## Structured Data
- Organization: ✅
- BreadcrumbList: ✅ (all pages)
- LocalBusiness: ✅ (contact page)

## Sitemap
- sitemap.xml accessible: ✅
- Pages in sitemap: 12
- All pages return 200: ✅

## Robots
- robots.txt accessible: ✅
- Sitemap referenced: ✅
```

## Agent Team Integration

When used as a teammate in `website-refactor`:

- Runs as part of the Lead's coordination, typically in Phase 2 (setup) and Phase 6 (validation)
- **Owns**: `seo-migration-report.md`, redirect configuration, `app/sitemap.ts`, `app/robots.ts`
- **Inputs**: URL inventory from `content-extractor`, new route structure from `designer`
- **Outputs**: Redirect config, sitemap, robots.txt, structured data, validation report

## Standalone Usage

Invoke independently for:
- **Pre-migration planning**: "Map all URLs from old site and plan redirects"
- **Post-migration validation**: "Verify all redirects work and no SEO was lost"
- **SEO audit**: "Check this site's metadata, structured data, sitemap, and robots.txt"
- **Domain change**: "Generate redirect map from old-domain.com to new-domain.com"

## Common Pitfalls

- **Missing redirects**: Every indexed URL MUST redirect somewhere. Even obscure pages. Check Search Console for the full list of indexed URLs.
- **Redirect chains**: A→B→C loses link equity. Always redirect directly to the final destination.
- **Soft 404s**: Pages that return 200 but show "not found" content. Search engines treat these poorly.
- **Losing backlinks**: High-authority pages with external backlinks MUST redirect. Check backlink profiles (Ahrefs, Moz) to prioritize.
- **Canonical confusion**: If both old and new sites are live temporarily, canonicals on the new site must point to new URLs, not old ones.
- **Sitemap with old URLs**: The new sitemap must only contain new URLs. Don't include redirected URLs.
- **Forgetting trailing slashes**: `/about` and `/about/` are different URLs. Be consistent and redirect the non-canonical version.
