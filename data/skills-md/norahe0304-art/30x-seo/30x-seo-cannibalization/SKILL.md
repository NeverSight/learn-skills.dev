---
name: 30x-seo-cannibalization
description: >
  Detect keyword cannibalization - multiple pages competing for the same keyword.
  Identifies cannibalizing URLs and provides resolution strategies (merge, redirect,
  differentiate, or delete).
metadata:
  version: 1.0.0
  category: content
  dependencies: [WebFetch]
allowed-tools:
  - WebFetch
  - Read
---

# Keyword Cannibalization Detection

> Find pages competing for the same keyword

## What is Keyword Cannibalization

**Problem**: Multiple pages on your site targeting the same keyword.

```
/blog/best-crm-software     → Target: "best crm"
/guide/crm-comparison       → Target: "best crm"
/products/crm               → Target: "best crm"
```

**Consequences**:
- Google doesn't know which to rank → none rank well
- Internal link equity is diluted
- Confusing user experience
- Wasted crawl budget

---

## Detection Methods

### Method A: With GSC Data (Recommended)

```
Import GSC "Queries" report
↓
Group by keyword
↓
Find keywords with multiple URLs
↓
Analyze each URL's:
- Impressions
- Clicks
- Average position
- Position fluctuation
↓
Identify cannibalization
```

**Cannibalization Signals**:
- Same keyword has 2+ URLs with impressions
- Ranking fluctuates frequently (Google is indecisive)
- Both pages stuck at positions 5-15

### Method B: Without GSC Data

```
Input target keyword list
↓
For each keyword:
- site:domain.com "keyword" search
- Analyze multiple results returned
↓
Check content overlap between pages
↓
Identify potential cannibalization
```

---

## Output Format

```markdown
# Keyword Cannibalization Report

## Found X Cannibalization Groups

### Group #1: "best crm software"

| URL | Position | Impressions | Clicks | Content Angle |
|-----|----------|-------------|--------|---------------|
| /blog/best-crm-2024 | #8 | 5,000 | 120 | Review article |
| /guide/crm-comparison | #12 | 3,200 | 45 | Comparison guide |
| /products/crm | #15 | 1,800 | 30 | Product page |

**Diagnosis**: Three pages have different angles but titles/H1s all target "best crm"

**Recommendation**: Differentiation strategy
- /blog/best-crm-2024 → Keep, primary target for "best crm software"
- /guide/crm-comparison → Retarget to "crm comparison guide"
- /products/crm → Retarget to brand term "YourBrand CRM features"

---

### Group #2: "how to use crm"

| URL | Position | Content Overlap |
|-----|----------|-----------------|
| /blog/crm-tutorial | #11 | 80% |
| /help/getting-started | #14 | 75% |

**Diagnosis**: Two pages with highly overlapping content

**Recommendation**: Merge strategy
- Merge into /blog/crm-tutorial (higher traffic)
- 301 redirect /help/getting-started to merged page
- Or: Rewrite /help/getting-started as product-specific tutorial

---

## Solution Summary

| Keyword | Strategy | Keep URL | Action for Others |
|---------|----------|----------|-------------------|
| best crm software | Differentiate | /blog/best-crm-2024 | Update titles |
| how to use crm | Merge | /blog/crm-tutorial | 301 redirect |
| ... | ... | ... | ... |
```

---

## Four Resolution Strategies

### 1. Merge

**When**: Content overlap >70%

```
A + B → A (the better one)
B → 301 to A
```

**Steps**:
- Pick the page with better traffic/ranking
- Merge unique content from the other page
- Set up 301 redirect
- Update internal links

### 2. Redirect

**When**: One page is clearly weaker

```
Weak page → 301 to strong page
```

**Steps**:
- 301 redirect directly, no content merge
- Ensure strong page covers weak page's intent

### 3. Differentiate

**When**: Two pages serve different intents

```
A → Keyword X
B → Keyword Y (related but different)
```

**Steps**:
- Modify title, H1, meta description
- Adjust content angle
- Update internal link anchor text

### 4. Delete

**When**: Page has no value

```
Low-quality page → Delete or noindex
```

**Steps**:
- 410 delete (explicitly tell Google)
- Or noindex (keep but don't rank)

---

## Usage

```bash
# With GSC data
/seo cannibalization --gsc [csv-file]

# With keyword list
/seo cannibalization --keywords "keyword1, keyword2, ..."

# Analyze entire site
/seo cannibalization https://example.com
```

---

## Prevention

### Keyword Mapping

Before writing new content, check if existing pages cover that keyword:

```markdown
| Target Keyword | Existing Page | Status |
|----------------|---------------|--------|
| best crm | /blog/best-crm-2024 | Covered |
| crm pricing | — | Available |
| crm vs erp | /blog/crm-erp-difference | Covered |
```

### Content Planning Principles

1. **One keyword = One page**
2. Check keyword mapping before new content
3. Run cannibalization detection regularly
4. Keep internal link anchors consistent with target keywords

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| 30x-seo-keywords | Build mapping during keyword research |
| 30x-seo-internal-links | Update links after fixing |
| 30x-seo-redirects | Execute 301 redirects |
| 30x-seo-content-writer | Rewrite for differentiation |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
