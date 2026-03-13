---
name: website-analysis
description: Crawl any website in a single pass to produce both a complete structural map and full content extraction. Discovers all pages, routes, navigation, multilingual variants, and issues while simultaneously extracting all text, images, metadata, and assets. Use before any migration, redesign, or audit.
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

This skill crawls an entire website **once** and produces both the structural map and the full content extraction in a single pass. Every page visit yields structure (links, nav, redirects, issues) AND content (text, images, metadata, assets).

The user provides: the root URL of the site to analyze, and optionally the output format (TypeScript, JSON, Markdown).

## Why a Single Pass

Running structure discovery and content extraction separately means visiting every page twice. Since the crawler already navigates each page, waits for load, scrolls for lazy content, and snapshots the DOM — it should extract everything in that same visit.

```
OLD (two passes):
  website-structure  →  visits every page  →  extracts links only
  content-extraction →  visits every page AGAIN  →  extracts content

NEW (single pass):
  website-analysis   →  visits every page ONCE  →  extracts links + content together
```

## What Gets Extracted Per Page

On every page visit, extract BOTH structural data and content:

### Structure (links, navigation, metadata)
| Data | Output |
|------|--------|
| Internal links | URL, anchor text, source page |
| External links | URL, anchor text, source page |
| Navigation position | Main nav, footer, breadcrumb, or body-only |
| Redirects | Requested URL vs final URL, status code |
| Language variants | URLs from language switcher |
| Page metadata | `<title>`, `<meta description>`, canonical, `lang` |

### Content (text, images, assets)
| Data | Output |
|------|--------|
| Text | Headings (h1-h6), paragraphs, lists, quotes — preserved with hierarchy |
| Images | Downloaded to `public/images/` with alt text cataloged |
| PDFs & assets | Downloaded to `public/assets/` with original URLs |
| Forms | Field names, types, labels, validation rules, action URLs |
| Structured data | JSON-LD, microdata, schema.org markup |
| OG tags | og:title, og:description, og:image |

## Analysis Process

### Step 1: Pre-Scan and Size Estimate

Before the full crawl, run a quick pre-scan to understand the site's scope:

```
1. Navigate to the homepage with agent-browser
2. Dismiss any cookie consent banners before extracting links
3. Extract all links from the main navigation (including dropdowns — click "More" buttons)
4. Extract all links from the footer
5. Check for a language switcher — note all language prefixes (e.g., /de, /it, /fr)
6. Try to fetch sitemap.xml — if 403/404, skip and rely on link discovery
7. Try to fetch robots.txt for referenced sitemaps — if 403/404, skip
8. Count unique internal URLs discovered so far
9. Estimate total pages: (nav pages + footer-only pages) × language count + expected detail pages
10. Report the estimate to the user before proceeding
```

**Adaptive path probing:** Instead of checking hardcoded paths (/about, /contact, etc.), extract likely pages from the nav and footer first. Only probe for utility pages not already discovered (e.g., /404, /sitemap, /robots.txt).

The pre-scan output determines the crawl strategy for Step 2.

### Step 2: Crawl with Section-Based Teammates

After the pre-scan, the lead agent spawns **section-based crawler teammates** to crawl in parallel. Each teammate is responsible for a specific section of the site.

**Team topology:**

```
Lead Agent (pre-scan + merge)
├── Crawler: Main pages (/about, /services, /contact, /privacy, etc.)
├── Crawler: Portfolio / Case studies (/case-studies/*, /projects/*, /work/*)
├── Crawler: Blog / News / Events (/blog/*, /news/*, /articles/*)
└── Crawler: Language variants (/de/*, /it/*, /fr/*, etc.)
```

**How it works:**
1. Lead runs the pre-scan (Step 1) and identifies the site sections from the navigation
2. Lead creates tasks for each crawler with their assigned URL list
3. Each crawler navigates its pages, extracts BOTH structure and content, and reports back
4. Lead merges all results, deduplicates, and generates the final output files

**Section assignment rules:**
- Assign sections based on URL prefixes discovered in the nav (e.g., all `/case-studies/*` go to one crawler)
- If a section has fewer than 3 pages, merge it into the main pages crawler
- The language variant crawler receives the full primary-language page list and checks each language prefix
- If new URLs are discovered during crawling (e.g., related content links), the crawler adds them to its own queue

**Per-page crawl procedure (each crawler follows this):**

```
For each page:
1. Navigate to the URL
2. Wait for full load (networkidle)
3. Scroll the FULL page to trigger lazy-loaded content
4. Click any expandable elements (accordions, tabs, "show more" buttons)
5. EXTRACT STRUCTURE:
   - All <a href="..."> links with anchor text
   - JavaScript navigation targets (onClick route changes)
   - Classify links: internal page, internal asset, external, anchor, mailto/tel
   - Language switcher URLs for this page
   - Detect redirect (compare requested URL vs final URL)
   - Record page metadata (title, description, H1, canonical, lang)
6. EXTRACT CONTENT (in the same visit):
   - All headings (h1-h6) with hierarchy
   - All paragraphs and text blocks
   - All lists (ordered/unordered)
   - All images (src, alt, dimensions) → download to public/images/{page-slug}/
   - All forms (fields, labels, actions)
   - Structured data (JSON-LD, schema.org)
   - OG tags
7. Take a full-page screenshot for visual reference
8. Add new internal links to the crawl queue (if not already visited)
```

**Crawl rules:**
- Stay within the same domain (don't follow external links)
- Handle trailing slashes consistently (normalize URLs)
- Detect and skip infinite pagination / infinite scroll
- Respect a maximum depth limit (default: 10 levels)
- Detect redirect chains and note the final destination
- Handle URL parameters (ignore tracking params like utm_*)

### Step 3: Classify Pages

Group discovered pages into categories:

| Category | Detection |
|----------|----------|
| **Navigation pages** | Linked from main nav or header |
| **Content pages** | Individual articles, blog posts, case studies |
| **Gallery/collection pages** | Pages that primarily display a grid of images or items |
| **Detail pages** | Sub-pages of a parent (e.g., /what-we-do/ai-journey) |
| **Utility pages** | 404, privacy policy, terms, sitemap, search |
| **Asset pages** | PDFs, downloads, media files |
| **Orphan pages** | In sitemap but not linked from any other page |
| **Redirect pages** | Return 301/302 to another URL |

### Step 4: Build the Site Map

Generate a hierarchical tree showing the complete structure:

```
/ (Homepage) — "Site Title"
├── /what-we-do — "What We Do"
│   ├── /what-we-do/ai-journey — "AI Journey"
│   └── /what-we-do/ai-academy — "AI Academy"
├── /case-studies — "Case Studies" (3 paginated pages)
│   ├── /case-studies/project-alpha — "Project Alpha"
│   ├── /case-studies/project-beta — "Project Beta"
│   └── /case-studies/old-project → 301 → /news/announcement (BROKEN)
├── /news — "News" (12 articles)
│   ├── /news/article-1 — "First Article"
│   └── /news/article-2 — "Second Article"
├── /contact — "Contact Us"
└── /privacy — "Privacy Policy"
```

### Step 5: Map Multilingual Structure

If the site has language variants, build the complete cross-language URL map:

```
1. For each primary-language page, record the language switcher URLs
2. Build a mapping table: EN → DE, IT, FR, etc.
3. Detect localization inconsistencies:
   - Pages missing in some languages
   - Inconsistent URL slugs (e.g., EN singular vs IT/FR plural)
   - Untranslated slugs (e.g., /fr/career instead of /fr/carrieres)
   - Empty or broken hrefs in language switchers
   - Different URL structures across languages (e.g., /case-studies vs /casi-di-uso)
4. Note which languages have full coverage vs partial translation
```

**Output a multilingual URL map table:**

```markdown
| English | German (/de) | Italian (/it) | French (/fr) |
|---------|-------------|---------------|--------------|
| / | /de | /it | /fr |
| /about | /de/ueber-uns | /it/chi-siamo | /fr/about |
| /contact | /de/kontakt | /it/contatti | /fr/contact |
```

### Step 6: Detect and Classify Issues

Flag potential problems with **severity levels**:

#### Redirect Classification

| Type | Description | Severity |
|------|-------------|----------|
| **Intentional redirect** | Old URL → new equivalent page (e.g., /old-about → /about) | Info |
| **Broken redirect** | URL → completely unrelated page (e.g., /case-study → /news/ceo-announcement) | Critical |
| **Redirect chain** | A → B → C (should be A → C) | Warning |
| **404 redirect** | Missing page falls back to a generic page (e.g., /missing → /home) | Critical |

#### Link Issues

| Type | Description | Severity |
|------|-------------|----------|
| **Broken link (404)** | Internal link points to a non-existent page | Critical |
| **Empty href** | Link element has no destination (href="" or missing) | Critical |
| **Orphan page** | Page exists (in sitemap) but no internal links point to it | Warning |
| **Dead end** | Page has no outbound internal links | Warning |
| **Deep page** | Page is more than 3 clicks from the homepage | Warning |
| **Mixed HTTP/HTTPS** | Links using HTTP when the site is HTTPS | Warning |

#### Multilingual Issues

| Type | Description | Severity |
|------|-------------|----------|
| **Missing translation** | Page exists in some languages but not others | Warning |
| **Inconsistent slug** | Same page has mismatched slugs across languages | Info |
| **Untranslated URL** | Localized page keeps the primary-language slug (e.g., /fr/career) | Info |
| **Broken language switcher** | Language link is empty, broken, or points to wrong page | Critical |

### Step 7: Generate Content Data Files

After the crawl, generate structured data files from the extracted content:

#### src/data/pages.ts (TypeScript — default format)

```typescript
export interface Page {
  slug: string;
  url: string;
  title: string;
  description: string;
  h1: string;
  headings: { level: number; text: string }[];
  sections: Section[];
  images: ImageAsset[];
  links: { href: string; text: string; type: "internal" | "external" }[];
  forms: FormData[];
  structuredData: object[];
  ogTags: Record<string, string>;
}
```

#### src/data/navigation.ts

```typescript
export interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}

export const mainNav: NavItem[] = [/* extracted from header */];
export const footerNav: NavItem[] = [/* extracted from footer */];
```

#### src/data/images.ts

```typescript
export interface ImageAsset {
  originalUrl: string;
  localPath: string;
  alt: string;
  width?: number;
  height?: number;
  page: string;
}
```

**Supported output formats** (pass as argument):
- `typescript` (default) — `src/data/*.ts` with interfaces and typed exports
- `json` — `content/*.json` files
- `markdown` — `content/*.md` files with frontmatter

## Output Files

The skill produces these files:

| File | Purpose |
|------|---------|
| `site-structure.md` | Primary deliverable — site tree, nav structure, page inventory, multilingual map, issues |
| `site-tree.txt` | Quick-reference plain text tree for scanning |
| `content-inventory.md` | Per-page content summary (sections, word count, images, forms) |
| `src/data/*.ts` | Structured content data files ready for import |
| `public/images/` | Downloaded images organized by page slug |
| `public/assets/` | Downloaded PDFs and other assets |
| `screenshots/` | Full-page screenshots of every page |

### site-structure.md

```markdown
# Site Structure — {domain}

**Crawled**: {date}
**Total pages**: {count} (primary language) / {count} (all languages)
**Languages**: {list}
**External links**: {count}
**Issues found**: {critical} critical, {warning} warnings

## Site Tree
(hierarchical tree with redirects and issues marked)

## Navigation Structure
(main nav, footer nav, language switcher)

## Page Inventory
| URL | Title | Type | Links In | Links Out |
(table of all pages)

## Multilingual URL Map
| English | German | Italian | French |
(cross-language mapping)

## External Links
| URL | Context | Found On |
(all outbound links)

## Issues Found
### Critical
### Warning
### Info
```

### content-inventory.md

```markdown
# Content Inventory — {domain}

## Pages ({count})

### / (Homepage)
- Title: "Site Name — Tagline"
- Description: "Meta description here"
- H1: "Main Heading"
- Sections: Hero, Features (3), CTA, Testimonials (4)
- Images: 8 (hero.jpg, feature-1.png, ...)
- Word count: 450
- Links: 12 internal, 3 external
- Forms: none

### /about
...
```

### site-tree.txt

```
example.com
├── / (Homepage)
├── /about/
├── /blog/ (12 posts)
│   ├── /blog/post-1/
│   └── ... (11 more)
├── /contact/
└── /privacy/

Language Variants:
├── /de (German) — 8 pages
├── /it (Italian) — 8 pages
└── /fr (French) — 6 pages (2 missing)
```

## Troubleshooting

Common obstacles and how to handle them:

### Cookie Consent Banners
**Always dismiss cookie banners before extracting links.** They overlay the page and can block interaction with navigation elements. Use agent-browser to look for "Reject all" or "Accept" buttons and click them first.

### Sitemap.xml Returns 403 or 404
Skip it and rely entirely on link discovery from the homepage, navigation, and footer. Many sites block direct access to sitemap.xml or don't have one. The recursive crawl will find all linked pages regardless.

### Anti-Bot Protection (Cloudflare, etc.)
If the site returns a challenge page or CAPTCHA:
- agent-browser uses a real browser engine, which handles most JavaScript challenges automatically
- If still blocked, note it in the output and report which pages couldn't be accessed

### Lazy-Loaded Content
Scroll the full page before extracting links and content. Some sites load content sections, images, or "load more" buttons only when scrolled into view. Scroll to the bottom in increments, waiting for new content to appear.

### JavaScript SPAs
Single-page applications render content client-side. Never use `curl`, `fetch()`, or HTTP-only tools. Always use agent-browser to get the fully rendered DOM.

### Expandable Elements
Accordions, tabs, "show more" buttons, and collapsible FAQs may hide links and content. Click every expandable element on the page before extracting. Check for `cursor=pointer` elements that aren't standard links.

### Infinite Scroll / Pagination
- For pagination: follow all "next page" and numbered page links
- For infinite scroll: scroll to bottom repeatedly until no new content loads (max 10 scrolls)
- Record pagination URLs as separate entries (e.g., `/blog?page=2`)

### URL Normalization
Treat these as the same page and deduplicate:
- `/about` and `/about/` (trailing slash)
- `/About` and `/about` (case)
- `/about/index.html` and `/about/`

But treat these as different:
- `/blog` and `/blog?page=2` (pagination)
- `/blog` and `/blog#section` (anchor — same page, ignore the fragment)

Ignore tracking parameters: `utm_source`, `utm_medium`, `utm_campaign`, `fbclid`, `gclid`.

### Authentication Walls
Some content may be behind login. Note these pages as "requires auth" in the inventory and skip them.

### Relative URLs
Always resolve to absolute URLs before cataloging or downloading assets.

## Agent Team Integration

This skill runs as **Phase 1** of `website-refactor`:

```
Phase 1: Website Analysis (this skill)
    ↓ outputs site-structure.md, content-inventory.md, src/data/*.ts, public/images/
    ↓ single pass — no second crawl needed
Phase 2: Project Setup (Lead scaffolds)
Phase 3: Design & Implementation (designer)
Phase 4: Verify + Audit (qa-auditor, seo-manager)
```

In the `website-refactor` agent team, the lead runs the pre-scan and spawns section-based crawlers. Once all crawlers report back, the lead merges results and hands off to the designer with complete structural AND content data.

## Standalone Usage

- **Pre-migration**: "Map and extract the entire site before we rebuild"
- **Discovery**: "How many pages does this site actually have?"
- **Content audit**: "What content does this site have?"
- **Link audit**: "Find all broken links on our production site"
- **Multilingual audit**: "Check if all pages are translated across all languages"
- **Competitor analysis**: "Map the structure and content of competitor.com"
- **QA**: "Verify our new site has the same structure as the old one"
- **Archival**: "Save a complete copy of this site's content"
