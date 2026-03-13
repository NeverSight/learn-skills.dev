---
name: pseo-metadata
description: Implement fully dynamic SEO metadata including title tags, meta descriptions, canonical URLs, Open Graph tags, and Twitter cards for programmatic SEO pages. Use when setting up or fixing metadata, adding OG/Twitter tags, implementing canonical URLs, or when metadata is static, duplicated, or missing across pSEO pages.
argument-hint: "[scope: all | titles | descriptions | canonical | opengraph | twitter]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Dynamic Metadata

Implement a metadata system that generates unique, accurate SEO tags for every programmatic page.

## Core Principles

1. **Every page gets unique metadata**: No two pages share the same title or description
2. **Data-driven generation**: Metadata is constructed from structured content fields, not hardcoded
3. **Canonical by default**: Every page declares its canonical URL
4. **Social-ready**: Open Graph and Twitter cards are complete on every page
5. **Framework-native**: Use the framework's built-in metadata API

## Implementation Steps

### 1. Create the Metadata Generator

Build a centralized function that constructs metadata from page data:

**Next.js App Router pattern:**
```typescript
// lib/metadata.ts
import type { Metadata } from "next";

export function generatePageMetadata(data: PageData, baseUrl: string): Metadata {
  const title = buildTitle(data);
  const description = buildDescription(data);
  const canonicalUrl = `${baseUrl}${data.canonicalPath}`;

  return {
    title,
    description,
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title,
      description,
      url: canonicalUrl,
      type: "article",
      siteName: "Site Name",
      // images: [{ url, width, height, alt }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      // images: [url],
    },
  };
}
```

### 2. Build Title Construction Logic

Titles must be:
- **Unique** across all pages (validate with pseo-quality-guard)
- **50-60 characters** target length (hard cap at 70)
- **Front-loaded** with the primary keyword
- **Multi-dimensional**: Use 2+ data fields to construct, not just one variable

```typescript
function buildTitle(data: PageData): string {
  // Combine multiple data dimensions
  // e.g., "{primary keyword} - {differentiator} | {brand}"
  // NOT just "{keyword} | Brand" for every page
}
```

### 3. Build Description Construction Logic

Descriptions must be:
- **Unique** across all pages
- **150-160 characters** target length
- **Action-oriented**: Include a value proposition or call to action
- **Keyword-inclusive**: Naturally incorporate the page's target keyword

### 4. Implement Canonical URLs

- Every page must set a self-referencing canonical URL
- Use absolute URLs (include protocol and domain)
- Canonicals must match the actual URL path exactly (no trailing slash mismatches)
- For paginated content, each page gets its own canonical
- If a page has query parameters, the canonical should point to the clean URL

### 5. Configure Open Graph Tags

Required OG tags for every pSEO page:
- `og:title` - Can differ from the HTML title (no brand suffix needed)
- `og:description` - Can differ from meta description
- `og:url` - Must match canonical
- `og:type` - Usually "article" for content pages, "website" for hubs
- `og:site_name` - Consistent across all pages
- `og:image` - Page-specific or category-specific image with alt text
- `og:locale` - Language/locale setting

### 6. Configure Twitter Card Tags

Required Twitter tags:
- `twitter:card` - Usually "summary_large_image"
- `twitter:title` - Can match OG title
- `twitter:description` - Can match OG description
- `twitter:image` - Can match OG image

### 7. Add Supplementary Meta Tags

Where appropriate:
- `robots`: Default to `index, follow`; set `noindex` for thin/utility pages
- `author`: If content has an author
- `article:published_time` / `article:modified_time`: For article-type pages

### 8. Export Metadata in Page Files

Wire the metadata generator into every page route:

```typescript
// app/[category]/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const data = await getPageData(params.slug);
  if (!data) return {};
  return generatePageMetadata(data, process.env.NEXT_PUBLIC_BASE_URL);
}
```

### 9. Internationalization (i18n) Metadata

For multi-language pSEO sites, add language-specific metadata:

- **hreflang tags**: Declare all language variants of each page. Every page must link to all its translations including itself.
  ```typescript
  alternates: {
    canonical: canonicalUrl,
    languages: {
      "en": `${baseUrl}/en/${data.canonicalPath}`,
      "de": `${baseUrl}/de/${data.canonicalPath}`,
      "x-default": `${baseUrl}/en/${data.canonicalPath}`,
    },
  }
  ```
- **x-default**: Always include an `x-default` hreflang pointing to the primary language or a language selector page
- **Canonical per language**: Each language version gets its own canonical (e.g., `/en/service/slug` and `/de/service/slug` are each self-canonical)
- **og:locale**: Set to the page's language (e.g., `en_US`, `de_DE`)
- **og:locale:alternate**: List all other available locales
- **URL structure**: Use path prefixes (`/en/`, `/de/`), not query params or subdomains, for best crawlability
- **Title and description**: Must be translated, not just the body. Templated metadata in the target language.

## Metadata Validation Rules

Run these checks (or integrate with pseo-quality-guard):
- No two pages produce the same title
- No two pages produce the same description
- All titles are between 30-70 characters
- All descriptions are between 100-170 characters
- All canonical URLs resolve to 200 status
- All OG tags are present on every page
- No page is missing metadata entirely

## File Organization

```
lib/
  metadata.ts          # generatePageMetadata() and helpers
  metadata.test.ts     # validation tests for metadata generation
```

## Relationship to Other Skills

- **Depends on**: pseo-data (content models provide metadata fields)
- **Works with**: pseo-templates (metadata is exported alongside page components)
- **Validated by**: pseo-quality-guard (checks uniqueness and completeness)
