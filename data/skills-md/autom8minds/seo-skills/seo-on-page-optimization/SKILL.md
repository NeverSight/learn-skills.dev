---
name: seo-on-page-optimization
description: Expert guide for on-page SEO optimization. Use when analyzing meta tags, title tags, headings (H1-H6), content optimization, image alt text, internal linking, URL structure, or improving on-page SEO signals for any web page.
---

# On-Page SEO Optimization

---

## Title Tag

The title tag is the single most important on-page ranking factor.

### Rules
| Rule | Value |
|------|-------|
| Length | 50-60 characters (Google truncates at ~580px) |
| Primary keyword | Place within first 60 chars, ideally near the start |
| Brand | Append at end with separator: `Primary Keyword - Brand` |
| Uniqueness | Every page must have a unique title |
| Format | `Primary Keyword - Secondary Keyword | Brand` |

### Common patterns
```
Blog post:    "How to [Action] [Topic] in [Year] | Brand"
Product:      "[Product Name] - [Key Feature] | Brand"
Category:     "[Category] - Shop [Subcategory] Online | Brand"
Homepage:     "Brand - [Primary Value Proposition]"
Service:      "[Service] in [Location] | Brand"
```

**MCP Tool:** Use `analyze_page` to extract and evaluate the current title tag, or `generate_meta_suggestions` to get AI-powered title recommendations.

---

## Meta Description

Not a direct ranking factor, but directly impacts CTR (click-through rate) from search results.

### Rules
| Rule | Value |
|------|-------|
| Length | 150-160 characters (Google truncates at ~920px) |
| Primary keyword | Include naturally — Google bolds matching query terms |
| CTA | Include a call-to-action (Learn, Discover, Shop, Get) |
| Uniqueness | Every page must have a unique description |
| No quotes | Avoid double quotes — Google truncates at `"` |

### Pattern
```
[Value proposition with keyword]. [Supporting detail]. [CTA].
```

**MCP Tool:** Use `analyze_page` or `generate_meta_suggestions` for current analysis + suggestions.

---

## Heading Structure (H1-H6)

Headings define content hierarchy and help search engines understand page structure.

### Rules
- **One H1 per page** — must contain primary keyword, should match search intent
- **H2s** for major sections — include secondary keywords naturally
- **H3-H6** for subsections — maintain strict hierarchy (no skipping levels)
- Never use headings for styling — use CSS instead
- Never leave headings empty

### Correct hierarchy
```
H1: Primary Topic (one only)
  H2: Major Section 1
    H3: Subsection
    H3: Subsection
  H2: Major Section 2
    H3: Subsection
      H4: Detail
  H2: Major Section 3
```

### Bad hierarchy (skipped levels)
```
H1: Topic
  H3: Section (skipped H2!)
    H5: Detail (skipped H4!)
```

**MCP Tool:** Use `analyze_headings` with `targetKeyword` parameter to validate structure and keyword presence.

---

## Content Optimization

### Keyword placement signals
| Location | Priority | Notes |
|----------|----------|-------|
| Title tag | Critical | First 60 chars |
| H1 | Critical | Primary keyword |
| First 100 words | High | Natural mention early |
| H2/H3 headings | High | Secondary/related keywords |
| URL slug | High | Hyphenated, concise |
| Meta description | Medium | For CTR, not ranking |
| Image alt text | Medium | Describe image with keyword if relevant |
| Last paragraph | Low | Natural mention |

### Content quality signals
- **Word count by type:**
  - Blog post: 1,500-2,500+ words (topic-dependent)
  - Product page: 300-1,000 words
  - Category page: 500-1,000 words
  - Landing page: 500-1,500 words
  - Homepage: 400-800 words
- **Readability:** Flesch-Kincaid grade 6-8 for general audience
- **Originality:** 100% unique content, no thin/duplicate content
- **Multimedia:** Include images, videos, tables, lists to enhance engagement
- **Freshness:** Update content regularly, especially for time-sensitive topics

### Keyword density
- No exact target — write naturally
- Primary keyword: 0.5-2% is typical for well-ranking pages
- Avoid keyword stuffing (repeating the same phrase unnaturally)
- Use semantic variations and related terms (LSI keywords)

**MCP Tool:** Use `analyze_page` with `includeContent: true` to get word count and content analysis.

---

## Image SEO

### Rules
| Element | Best Practice |
|---------|--------------|
| Alt text | Descriptive, 125 chars max, include keyword where relevant. Decorative images: `alt=""` |
| File name | Descriptive with hyphens: `blue-running-shoes.webp` not `IMG_4532.jpg` |
| Format | WebP or AVIF preferred, JPEG for photos, PNG for transparency, SVG for icons |
| File size | Under 200KB per image, use compression tools |
| Dimensions | Specify `width` and `height` attributes to prevent CLS |
| Lazy loading | Add `loading="lazy"` to below-the-fold images |
| Responsive | Use `srcset` and `sizes` for responsive images |

### Alt text patterns
```
Good:  "Blue Nike running shoes on a trail"
Good:  "SEO audit dashboard showing Core Web Vitals scores"
Bad:   "image1"
Bad:   "shoes shoes running shoes blue shoes nike shoes"  (keyword stuffing)
Bad:   (empty alt on non-decorative image)
```

**MCP Tool:** Use `analyze_images` to audit all images on a page for alt text, size, format, and lazy loading.

---

## Internal Linking

Internal links distribute link equity (PageRank) and help search engines discover and understand your site structure.

### Strategy
- **Hub-and-spoke model:** Pillar pages link to cluster pages and vice versa
- **Contextual links:** Link within body content (not just navigation) — these carry more weight
- **Descriptive anchors:** Use keyword-rich, descriptive anchor text (not "click here" or "read more")
- **Limit per page:** Reasonable number (under 100-150 total links; focus on quality)
- **Fix orphan pages:** Every indexable page should have at least one internal link pointing to it
- **Link to deep pages:** Don't just link to the homepage — distribute equity to important pages
- **Prioritize above-the-fold:** Links higher on the page may carry more weight

### Anchor text rules
```
Good:  "Learn about technical SEO auditing"
Good:  "our guide to keyword research"
Bad:   "click here"
Bad:   "this article"
Bad:   "https://example.com/page"  (naked URL)
```

**MCP Tool:** Use `analyze_internal_links` to map all links, evaluate anchor text quality, and detect broken links.

---

## URL Structure

### Rules
- Keep URLs short and descriptive: `/seo-audit-checklist` not `/p?id=123&cat=seo`
- Use hyphens, not underscores: `/technical-seo` not `/technical_seo`
- Lowercase only
- Include primary keyword
- Limit depth: 3-4 levels max (`/category/subcategory/page`)
- Avoid parameters when possible (use canonical if unavoidable)
- No stop words: `/seo-audit` not `/the-complete-guide-to-seo-audit`
- Stable URLs — don't change URLs without 301 redirects

---

## Open Graph & Twitter Cards

Essential for social sharing appearance and click-through from social platforms.

### Required Open Graph tags
```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

### Twitter Card tags
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### Image requirements
- **Minimum:** 1200x630px for `summary_large_image`
- **Aspect ratio:** 1.91:1
- **File size:** Under 5MB
- **Format:** JPG, PNG, WebP, GIF

---

## Canonical Tags

Prevent duplicate content issues by specifying the preferred version of a page.

### Rules
- Every indexable page should have a self-referencing canonical: `<link rel="canonical" href="https://example.com/page">`
- Use absolute URLs (not relative)
- Point to the HTTPS version
- Point to the non-www or www version (whichever is preferred)
- Don't canonical to a different page unless content is truly duplicate/very similar
- Don't canonical to a 404 or redirected URL

---

## Quick Reference: On-Page Audit Checklist

| Element | Check | Pass Criteria |
|---------|-------|---------------|
| Title tag | Present, unique, correct length | 50-60 chars, contains keyword |
| Meta description | Present, unique, correct length | 150-160 chars, includes CTA |
| H1 | Present, single, contains keyword | Exactly one H1 with primary keyword |
| Heading hierarchy | No skipped levels | H1 > H2 > H3 (no jumps) |
| Images | Alt text present | All non-decorative images have descriptive alt |
| Internal links | Descriptive anchors | No "click here", relevant anchors |
| Canonical | Present, self-referencing | Absolute HTTPS URL |
| OG tags | Present | og:title, og:description, og:image, og:url |
| URL | Clean, keyword-rich | Hyphens, lowercase, concise |
| Content | Sufficient, original | Meets word count for page type |

---

## Related Skills
- **seo-technical-audit** — for crawlability, speed, and indexing issues
- **seo-schema-structured-data** — for adding JSON-LD markup
- **seo-content-strategy** — for keyword research and content planning
- **seo-mcp-tools-expert** — for using MCP tools effectively

## Key MCP Tools for On-Page SEO
| Tool | Use For |
|------|---------|
| `analyze_page` | Comprehensive on-page analysis with scoring |
| `analyze_headings` | Heading structure validation |
| `analyze_images` | Image alt text and optimization audit |
| `analyze_internal_links` | Link mapping and anchor text analysis |
| `generate_meta_suggestions` | AI-powered meta tag improvement suggestions |

See [COMMON_MISTAKES.md](COMMON_MISTAKES.md) for the 15 most frequent on-page SEO mistakes.
See [CHECKLISTS.md](CHECKLISTS.md) for step-by-step audit checklists.
See [EXAMPLES.md](EXAMPLES.md) for before/after optimization examples.
