---
name: pseo-linking
description: Build an intelligent internal linking system using hub-and-spoke structures, related page suggestions, breadcrumb navigation, and topical clustering for programmatic SEO. Use when implementing or improving internal linking, adding breadcrumbs, building category hub pages, or creating related-pages components.
argument-hint: "[component: all | breadcrumbs | related | hubs | sitemap]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Internal Linking

Build an internal linking system that creates strong topical authority, distributes link equity, and ensures every page is discoverable.

## Core Principles

1. **Hub-and-spoke architecture**: Category hubs link to all child pages; child pages link back to their hub
2. **Topical clustering**: Pages within the same topic cluster interlink
3. **Every page reachable**: No orphan pages — every page is linked from at least 2 other pages
4. **Crawl depth <= 3**: Any page reachable within 3 clicks from the homepage
5. **Descriptive anchor text**: Link text describes the target page, not generic "click here"

## Architecture

```
Homepage
├── Category Hub A ──→ Page A1, A2, A3, ...
│   ├── Page A1 ──→ Hub A, A2, A3 (related)
│   ├── Page A2 ──→ Hub A, A1, A3 (related)
│   └── Page A3 ──→ Hub A, A1, A2 (related)
├── Category Hub B ──→ Page B1, B2, B3, ...
│   └── ...
└── Sitemap (links all hubs)
```

## Implementation Steps

### 1. Breadcrumb Navigation

Build a breadcrumb component that:
- Renders the full path: Home > Category > Current Page
- Uses semantic HTML (`<nav>` with `<ol>`)
- Generates BreadcrumbList schema markup (coordinate with pseo-schema)
- Appears on every pSEO page

```typescript
interface BreadcrumbItem {
  label: string;
  href: string;
}

function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, i) => (
          <li key={item.href}>
            {i < items.length - 1 ? (
              <a href={item.href}>{item.label}</a>
            ) : (
              <span aria-current="page">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
```

### 2. Related Pages Component

Build a component that displays links to related pages:

- Pull related pages from the data layer's `getRelatedPages(slug, limit)` function
- Show 3-6 related pages per page
- Prioritize pages in the same category, then adjacent categories
- Use the page's H1 or title as anchor text
- Include a brief description or differentiator for each link

Relatedness signals (in priority order):
1. Same category
2. Shared tags or attributes
3. Similar content type
4. Alphabetically adjacent (fallback)

### 3. Hub Pages (Category Landing Pages)

Hub page creation is owned by **pseo-templates** (section 7). From a linking perspective, ensure every hub page:
- Links to all child pages in the category (or paginates if >50)
- Is linked from the homepage or global navigation
- Has CollectionPage or ItemList schema markup (coordinate with pseo-schema)

### 4. Cross-Category Linking

Identify and implement cross-category linking opportunities:
- "See also" sections linking to related pages in other categories
- Comparison pages that bridge categories
- Tag-based linking (pages sharing the same tag link to each other)

### 5. Footer/Sidebar Navigation

Add persistent navigation that links to:
- All category hub pages
- Most popular or cornerstone content pages
- This ensures hubs are reachable from every page (crawl depth = 2)

### 6. XML Sitemap

Generate a dynamic sitemap that:
- Includes all pSEO pages with lastmod dates
- Groups URLs by category using sitemap index
- Updates automatically when pages are added
- Handles 1000+ URLs (split into multiple sitemaps at 50,000 limit)

```typescript
// app/sitemap.ts (Next.js App Router)
export default async function sitemap() {
  const categories = await getAllCategories();
  const entries = [];

  // Hub pages (higher priority)
  for (const cat of categories) {
    entries.push({
      url: `${baseUrl}/${cat.slug}`,
      lastModified: cat.lastModified,
      changeFrequency: "weekly" as const,
      priority: 0.8,
    });
  }

  // Child pages (PageIndex has lastModified)
  for (const cat of categories) {
    const pages = await getPagesByCategory(cat.slug);
    for (const page of pages) {
      entries.push({
        url: `${baseUrl}/${cat.slug}/${page.slug}`,
        lastModified: page.lastModified,
        changeFrequency: "weekly" as const,
        priority: 0.6,
      });
    }
  }

  return entries;
}
```

### 7. Redirect Management

At 1000+ pages, slug and URL changes are inevitable. Build a redirect system:

- Maintain a redirect map (JSON file, database table, or framework config) that maps old paths to new paths
- All redirects must be 301 (permanent) to preserve link equity
- When a slug changes, automatically add the old URL to the redirect map
- When a category is renamed, redirect all child URLs under the old category path
- Implement a redirect middleware or config that processes the map on every request
- Validate: no redirect chains (A → B → C), no redirect loops, no redirects to 404s

**Next.js pattern:**
```typescript
// next.config.js
async redirects() {
  const map = await loadRedirectMap();
  return map.map(({ source, destination }) => ({
    source,
    destination,
    permanent: true,
  }));
}
```

**Build-time validation:**
- All redirect sources must not match any current live slug
- All redirect destinations must resolve to a live page
- Log warnings for redirects older than 12 months (consider removing)

### 8. robots.txt and AI Crawler Access

Create or update robots.txt to:
- Allow all pSEO pages for traditional crawlers (Googlebot, Bingbot)
- Allow AI retrieval crawlers needed for LLM citation (GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot)
- Optionally block AI training crawlers (Google-Extended, CCBot)
- Reference both the sitemap and llms.txt
- Block utility/admin pages

**Critical**: Blocking Bingbot or GPTBot means zero visibility in ChatGPT. See pseo-llm-visibility for full AI crawler configuration.

### 9. llms.txt

llms.txt creation is owned by **pseo-llm-visibility** (section 1). From a linking perspective, ensure llms.txt references all category hub pages and the sitemap. The robots.txt should include a comment pointing to llms.txt.

## Link Health Checks

Verify:
- [ ] No orphan pages (every page linked from at least 2 others)
- [ ] Hub pages link to all their child pages
- [ ] Child pages link back to their hub
- [ ] Breadcrumbs are present on every page
- [ ] Related pages section shows 3-6 links
- [ ] No broken internal links (all hrefs resolve to 200)
- [ ] Sitemap includes all public pages
- [ ] Crawl depth from homepage <= 3 for any page
- [ ] Redirect map exists and covers all historical URL changes
- [ ] No redirect chains or loops
- [ ] All redirect destinations resolve to live pages
- [ ] robots.txt allows AI retrieval crawlers (GPTBot, PerplexityBot, ClaudeBot, Bingbot)
- [ ] llms.txt exists at site root with category hubs and page type descriptions

## Relationship to Other Skills

- **Depends on**: pseo-data (category data, related page queries)
- **Provides to**: pseo-schema (breadcrumb items for BreadcrumbList schema)
- **Works with**: pseo-templates (linking components are rendered in templates)
