---
name: pseo-quality-guard
description: Validate programmatic SEO pages against quality standards to prevent thin content, duplicate content, and keyword cannibalization. Use when auditing pSEO output quality, before deploying new pages, when Google Search Console reports issues, or when checking if generated pages meet quality thresholds. This skill can also be used automatically to validate changes made by other pseo-* skills.
argument-hint: "[check: all | thin | duplicates | cannibalization | metadata | abuse | prune | delta]"
allowed-tools: Read, Glob, Grep, Bash
---

# pSEO Quality Guard

Validate generated pages against SEO quality standards. Detect and flag issues that would cause Google to devalue, deindex, or penalize programmatic pages.

## Core Principles

1. **No thin pages**: Every page must provide substantial, unique value
2. **No duplicate content**: No two pages should have the same or near-identical content
3. **No cannibalization**: No two pages should target the same keyword or intent
4. **Metadata uniqueness**: Every page has unique title and description
5. **Fail loudly**: Quality issues should block deployment, not slip through silently

## Quality Checks

### 1. Thin Content Detection

A page is thin if it:
- Has fewer than 300 words of unique text content (excluding navigation, footer, boilerplate)
- Is essentially a template with only 1-2 variable substitutions
- Contains no meaningful content beyond its metadata
- Has the same paragraph structure as other pages with only proper nouns changed

**How to check:**
- Extract text content from each rendered page (strip HTML tags, nav, footer)
- Count unique words per page
- Compare content across pages — compute similarity ratios
- Flag pages with < 300 unique words or > 80% similarity to another page

### 2. Duplicate Content Detection

Check for:
- **Exact duplicates**: Two pages with identical body content
- **Near duplicates**: Pages with > 80% text similarity (use Jaccard similarity on n-grams or cosine similarity)
- **Title duplicates**: Two pages with the same `<title>` tag
- **Description duplicates**: Two pages with the same meta description
- **URL-based duplicates**: Different URLs serving the same content (www vs non-www, trailing slash variants)

**How to detect:**

At small scale (< 200 pages), pairwise comparison is feasible:
```
For each pair of pages:
  similarity = intersection(ngrams(page_a), ngrams(page_b)) / union(ngrams(page_a), ngrams(page_b))
  if similarity > 0.8: FLAG as near-duplicate
```

At scale (200+ pages), pairwise is O(n²) and impractical. Use one of:
- **MinHash / LSH**: Hash n-gram sets into fixed-size signatures, use locality-sensitive hashing to find candidate pairs. Reduces comparisons from O(n²) to near-linear.
- **SimHash**: Compute a fingerprint per page, compare fingerprints (Hamming distance). Pages with similar fingerprints are candidates.
- **Sampling**: Compare each page against a random sample of 50 others + all pages in the same category. Not exhaustive but catches the common cases.
- **Template fingerprinting**: Hash the non-variable parts of each page. If two pages share the same template fingerprint, flag them — they differ only in variable slots.

### 3. Keyword Cannibalization Detection

Cannibalization occurs when multiple pages target the same search query.

**Detection method:**
- Extract the primary keyword/intent from each page (from title, H1, and first paragraph)
- Group pages that share the same primary keyword
- Flag groups with 2+ pages targeting the same keyword

**Resolution strategies:**
- Merge thin pages targeting the same keyword into one comprehensive page
- Differentiate intent (informational vs. transactional vs. navigational)
- Use canonical tags to point duplicates to the primary page
- Adjust titles and H1s to target distinct long-tail variations

### 4. Metadata Quality Validation

Check every page's metadata for:

| Field | Validation Rule |
|-------|----------------|
| Title | Present, 30-70 chars, unique across all pages |
| Description | Present, 100-170 chars, unique across all pages |
| H1 | Present, exactly one per page, unique across all pages |
| Canonical | Present, absolute URL, self-referencing |
| OG:title | Present |
| OG:description | Present |
| OG:url | Present, matches canonical |

### 5. Schema Markup Validation

- Every page has at least BreadcrumbList schema
- Content pages have Article or appropriate type schema
- FAQ pages have FAQPage schema with valid Q&A pairs
- No schema has empty or placeholder values
- All URLs in schema are absolute

### 6. Internal Link Health

- No orphan pages (pages with zero inbound internal links)
- No broken internal links (href targets that return 404)
- Every page links back to its category hub
- Breadcrumbs are present and correct

### 7. Scaled Content Abuse Detection (Google 2025)

Google's 2025 updates (March, June, August, December) increasingly target programmatic pages that exist primarily to manipulate rankings. The method (AI, templates, human) is irrelevant — only intent and value matter.

**Check for these specific patterns that trigger Google's SpamBrain system:**

- **Template repetitiveness ratio**: Extract the boilerplate (shared HTML structure and text) from all pages of a type. If boilerplate is 60-80%, flag as warning; if > 80%, flag as critical risk for scaled content abuse.
- **Variable-swap-only differentiation**: If the only differences between pages are proper nouns (city names, product names, keywords), flag as extremely high risk. Google specifically called out "location pages that use the same template in dozens of cities."
- **Filler content patterns**: Detect generic introductory paragraphs ("In today's world...", "When it comes to...", "If you're looking for...") that add no information. These patterns are specifically targeted by the December 2025 "Needs Met" enforcement.
- **Value-first test**: Check if the primary content/answer appears within the first 200 words. Pages that bury value below filler are devalued.
- **E-E-A-T signal presence**: Check for author attribution, data sources, last-updated dates. Absence of all trust signals on pSEO pages is a risk factor.
- **Publication velocity**: If 500+ pages were published within a single day or week, flag for review. Gradual rollout is safer.

**Severity:**
- Template repetitiveness > 80%: **Critical** — will likely trigger scaled content abuse penalty
- Template repetitiveness 60-80%: **Warning** — at risk, needs content enrichment
- No E-E-A-T signals on any page: **Warning**
- All pages published same day: **Warning**

### 8. Heading Hierarchy Validation

Check every page for correct heading structure:
- Exactly one `<h1>` per page
- No heading level skips (h1 → h3 without h2 is invalid)
- Headings follow a logical document outline (h1 > h2 > h3)
- No empty heading tags
- Heading content is meaningful (not generic like "Section 1")

### 9. Robots and Indexation

- Pages intended for indexing have `index, follow` (or no robots tag)
- Thin or utility pages have `noindex`
- No important pages accidentally blocked by robots.txt
- Sitemap includes all indexable pages and excludes noindexed ones

## Output Format

```
## pSEO Quality Report

### Summary
- Total pages checked: X
- Issues found: X (Y critical, Z warnings)

### Thin Content
- [list of pages with word counts below threshold]

### Duplicate Content
- [list of duplicate pairs with similarity scores]

### Keyword Cannibalization
- [list of keyword groups with competing pages]

### Metadata Issues
- [list of pages with metadata problems]

### Schema Issues
- [list of pages with schema problems]

### Linking Issues
- [list of orphan pages and broken links]

### Scaled Content Abuse Risk
- Template boilerplate ratio: X%
- Variable-swap-only pages: X
- Pages missing E-E-A-T signals: X
- Filler intro patterns detected: X pages
- Risk level: [Low | Medium | High | Critical]

### Pruning Recommendations
- Pages to remove: X
- Pages to merge: X
- Pages to noindex: X
- Pages to enrich: X
- [list of specific pages and recommended action]

### Action Required
1. [prioritized list of fixes]
```

## Memory Considerations

Quality checks load and compare page content across the full site. At scale this is the most memory-intensive operation in the pSEO pipeline.

**Do NOT load all full page content into memory at once.** Instead:

- **Stream-compare**: Load pages one at a time, compute a fingerprint (hash or MinHash signature), store only the fingerprint (~100 bytes per page). Compare fingerprints after all pages are processed.
- **Batch by category**: Run similarity checks within each category first (most duplicates are same-category). Only run cross-category checks on a sample.
- **Write intermediate results to disk**: For large sites, write per-page metrics (word count, fingerprint, title hash) to a JSON file, then process the file.

Memory budget estimate:
| Pages | Fingerprints only | Full content in memory |
|-------|-------------------|----------------------|
| 1,000 | ~100KB | ~100-500MB |
| 10,000 | ~1MB | ~1-5GB (will OOM) |
| 50,000 | ~5MB | ~5-25GB (impossible) |

Always use the fingerprint approach at 500+ pages.

## Content Pruning Recommendations

When quality checks find issues, don't just flag — recommend action. Google's own guidance: "If you're considering deleting entire sections of your site, that's likely a sign those sections were created for search engines first, and not people."

See `references/thresholds.md` → "Content Pruning Decision Thresholds" for the exact decision table (conditions and actions).

200 genuinely valuable pages outperform 5,000 thin pages. Pruning is not failure — it's quality control.

**After pruning:**
- Add 301 redirects from removed URLs to the best related page
- Update the sitemap to exclude removed pages
- Update internal links that pointed to removed pages
- Re-run quality guard to verify improved metrics

## Integration as Build Check

This skill can be turned into a build-time validation script:

```typescript
// scripts/validate-pseo.ts
// Run: npx tsx scripts/validate-pseo.ts
// CI/CD: exits with code 1 if critical issues found

import { getAllSlugs, getPageData } from "../lib/data";

async function validate() {
  const slugs = await getAllSlugs();
  const issues: { slug: string; level: "critical" | "warning"; message: string }[] = [];

  for (const { slug } of slugs) {
    const page = await getPageData(slug);
    if (!page) {
      issues.push({ slug, level: "critical", message: "Page data missing" });
      continue;
    }
    if (!page.title || !page.metaDescription || !page.h1) {
      issues.push({ slug, level: "critical", message: "Missing required metadata" });
    }
    if (page.title.length > 70) {
      issues.push({ slug, level: "warning", message: `Title too long: ${page.title.length} chars` });
    }
    // Add more checks: word count, duplicate titles, schema presence, etc.
  }

  const critical = issues.filter((i) => i.level === "critical");
  console.log(`Checked ${slugs.length} pages. ${issues.length} issues (${critical.length} critical).`);
  issues.forEach((i) => console.log(`[${i.level}] ${i.slug}: ${i.message}`));
  process.exit(critical.length > 0 ? 1 : 0);
}

validate();
```

## Scope Parameter

If `$ARGUMENTS` specifies a check:
- `all` (default): Run all checks
- `thin`: Thin content detection only
- `duplicates`: Duplicate content detection only
- `cannibalization`: Keyword cannibalization only
- `metadata`: Metadata validation only
- `abuse`: Scaled content abuse pattern detection only
- `prune`: Run all checks and output pruning recommendations
- `delta`: Run all checks on pages modified since last validation only (requires content hashing — see pseo-scale section 4)

## Relationship to Other Skills

- **Validates output of**: pseo-templates, pseo-metadata, pseo-schema, pseo-linking
- **Depends on**: pseo-data (needs access to all page data for cross-page comparisons)
- **Run after**: Any other pseo-* skill to verify quality
- **Extended by**: pseo-scale (incremental/delta validation, parallel category-partitioned checks, content hash storage)
