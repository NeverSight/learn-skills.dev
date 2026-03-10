---
name: pseo-data
description: Design and implement the structured data architecture that powers programmatic SEO pages, including content models, data sources, slug generation, and data-fetching layers. Use when setting up or refactoring the data foundation for pSEO, designing content models, or building the data pipeline that feeds page templates.
argument-hint: "[source: cms | json | database | api | mdx]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Data Architecture

Design and implement the structured data layer that feeds all programmatic SEO pages. This is the foundation every other pSEO skill depends on.

## Core Principles

1. **Single source of truth**: All page data flows from one data layer
2. **SEO-complete models**: Every content model includes all fields needed for metadata, schema markup, and linking
3. **Unique slugs by construction**: Slug generation enforces uniqueness at the data level
4. **Type safety**: All data models are fully typed (TypeScript interfaces/types)
5. **Separation of concerns**: Data fetching is decoupled from page rendering

## Implementation Steps

### 1. Define Content Models

Create TypeScript interfaces for each page type using a two-tier model. The lightweight index tier is safe to hold in memory for all pages; the heavy full tier is loaded per-page only.

```typescript
// Index tier: safe to load all at once (~1KB per page)
interface PageIndex {
  slug: string;               // unique, URL-safe
  title: string;              // page title (50-60 chars target)
  metaDescription: string;    // meta description (150-160 chars target)
  h1: string;                 // primary heading (can differ from title)
  canonicalPath: string;      // canonical URL path
  category: string;           // for hub-spoke and breadcrumbs
  lastModified: string;       // ISO date for sitemap
}

// Full tier: extends PageIndex with heavy fields (~50-500KB per page)
interface BaseSEOContent extends PageIndex {
  introText: string;
  bodyContent: string;
  faqs?: FAQ[];
  relatedSlugs?: string[];
  featuredImage?: SEOImage;
}
```

Extend `BaseSEOContent` for each page type with domain-specific fields. The interfaces above show the minimum required fields. See `references/content-models.md` for the full definitions (which add `subcategory`, `tags`, `publishedDate`, `status`, and more) and extended type examples (LocationPage, ProductPage, ComparisonPage, CategoryPage).

### 2. Build the Data-Fetching Layer

Create a centralized data module (e.g., `lib/data.ts` or `src/data/index.ts`) that exports:

- `getAllSlugs()` - Returns all valid slugs for static generation. Must handle pagination internally when the data source has 1000+ records (fetch in batches, return the complete list).
- `getPageData(slug)` - Returns full content for a single page
- `getPagesByCategory(category, opts?)` - Returns pages in a category for hub pages. Accept optional `limit` and `offset` for paginated hub pages.
- `getRelatedPages(slug, limit?)` - Returns related pages for internal linking
- `getAllCategories()` - Returns all categories for navigation and hubs
- `getPageCount()` - Returns total page count (useful for sitemap splitting and build diagnostics)

All functions must be:
- Cached or memoized during build to avoid redundant reads
- Typed with explicit return types
- Guarded against missing or malformed data
- Internally paginated when the data source imposes limits (e.g., CMS APIs with 100-item pages). The consumer should never need to handle pagination — the data layer abstracts it.

### 3. Implement Slug Generation

Design a slug strategy that:
- Produces URL-safe, lowercase, hyphenated strings
- Guarantees uniqueness across the entire dataset
- Is deterministic (same input always produces same slug)
- Includes a collision detection mechanism
- Follows a consistent URL hierarchy (e.g., `/category/page-slug`)

### 4. Validate Data Integrity

Build a validation function or script that checks:
- No duplicate slugs exist
- All required fields are present and non-empty
- Title and description lengths are within SEO targets
- All category references resolve to valid categories
- No orphan pages (pages not reachable through any category)

### 5. Set Up Data Source Integration

Based on the data source (`$ARGUMENTS` or detected):

**JSON files**: Create a `data/` directory with typed JSON, a loader, and build-time validation.

**CMS (headless)**: Create API client with typed responses, implement caching, handle pagination for 1000+ items.

**Database**: Create a query layer with connection pooling, implement cursor-based pagination, add query caching.

**MDX files**: Set up frontmatter schema validation, create a content loader with gray-matter parsing.

**API**: Create a typed API client, implement rate limiting and retry logic, add response caching.

## Scale Limits

The in-memory and file-based patterns in this skill work up to ~10K pages. Beyond that:

- **10K-50K pages**: Requires a database (PostgreSQL, MySQL). In-memory index tier becomes borderline at 50K (~50MB). File-based data sources are too slow.
- **50K-100K+ pages**: Requires database + cache layer (Redis) + cursor-based pagination. `getAllSlugs()` must use cursor iteration, not array return. Data sufficiency gating prevents generating thin pages.

See **pseo-scale** for the complete database-backed data layer, sufficiency scoring, and scale-specific patterns.

## Memory-Conscious Data Patterns

At 1000+ pages, how data is loaded matters more than what is loaded. A full content model with body text, FAQs, and images can be 50-500KB per page. Loading all pages into memory simultaneously will OOM.

**Two-tier data model:**

Split the data layer into lightweight index data and full page data. The `PageIndex` and `BaseSEOContent` interfaces from section 1 define the two tiers:

- `getAllSlugs()`, `getRelatedPages()`, `getPagesByCategory()` — return `PageIndex[]` (lightweight, ~1KB per page)
- `getPageData()` — returns `BaseSEOContent` (or an extended type) for a single page (heavy, ~50-500KB per page, only one at a time)

**Never do this:**
```typescript
// Loads ALL full content into memory — will OOM at scale
const allPages = await Promise.all(slugs.map(s => getPageData(s)));
```

**Instead:**
```typescript
// Process pages one at a time or in small batches
for (const slug of slugs) {
  const page = await getPageData(slug);
  await processPage(page);
  // page is GC'd after each iteration
}
```

**CMS/API pagination:**
- Fetch in batches of 100-250 records
- Yield or push to an array incrementally — don't hold all API responses in memory simultaneously
- If using GraphQL, only request index fields in list queries, full fields in single-item queries

## File Organization

```
lib/
  data/
    index.ts          # public API (re-exports)
    types.ts          # TypeScript interfaces
    fetcher.ts        # data source integration
    slugs.ts          # slug generation and validation
    validation.ts     # data integrity checks
    cache.ts          # build-time caching utilities
```

## Quality Checks

Before considering this complete:
- [ ] All content models extend BaseSEOContent (which extends PageIndex)
- [ ] `getAllSlugs()` returns 0 duplicates
- [ ] Data validation passes with zero errors
- [ ] Data layer exports are fully typed with no `any`
- [ ] Fetching is memoized for build performance
- [ ] A test or script can validate the full dataset
- [ ] Two-tier data model implemented (index data vs. full page data)
- [ ] No function loads all full page content into memory simultaneously
- [ ] CMS/API fetching uses batched pagination internally

## Relationship to Other Skills

This skill provides the data foundation for:
- **pseo-templates**: Consumes `getPageData()` and `getAllSlugs()`
- **pseo-metadata**: Reads title, description, canonical from content models
- **pseo-schema**: Uses structured fields for JSON-LD generation
- **pseo-linking**: Uses `getRelatedPages()` and category data
- **pseo-quality-guard**: Validates against the content models
