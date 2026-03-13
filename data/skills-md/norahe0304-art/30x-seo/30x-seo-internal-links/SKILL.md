---
name: 30x-seo-internal-links
description: >
  Internal link analysis AND generation. Analyzes orphan pages, link equity,
  anchor text. Also generates link suggestions for new content. Use when
  user says "internal linking", "orphan pages", "link suggestions", "where
  should I link", or "internal link recommendations".
allowed-tools:
  - WebFetch
  - Read
---

# Internal Link Analysis + Generation

## What This Skill Does

**Two functions**:

| Mode | Input | Output |
|------|-------|--------|
| **Analysis Mode** | Website URL | Internal link issues report |
| **Generation Mode** | New article + site structure | Link suggestions (where to link, anchor text) |

Good internal linking:
- Helps Google find all your pages
- Distributes "link juice" (ranking power) to important pages
- Guides users through your content

## Why Internal Links Matter

- **Orphan pages** (no internal links) = Google can't find them = not indexed
- **Deep pages** (6+ clicks from homepage) = Google thinks they're not important
- **Link hoarding** (homepage links to everything) = diluted equity per link
- **Poor anchor text** = Google doesn't understand what the linked page is about

## Check Categories

### 1. Orphan Pages
Pages with ZERO internal links pointing to them.

**How to find:**
1. Crawl entire site to find all pages
2. Check which pages have no inbound internal links
3. Cross-reference with sitemap (orphan pages often only accessible via sitemap)

**Severity:**
- Orphan + in sitemap = Medium (Google can find via sitemap, but weak)
- Orphan + not in sitemap = Critical (Google may never find it)

### 2. Click Depth Analysis

| Depth | Meaning | SEO Impact |
|-------|---------|------------|
| 1 click | Linked from homepage | Highest priority |
| 2 clicks | Linked from main sections | High priority |
| 3 clicks | Standard content | Normal priority |
| 4+ clicks | Buried content | Lower priority |
| 6+ clicks | Too deep | Likely not indexed well |

**Rule**: Important pages should be within 3 clicks of homepage.

### 3. Internal Link Distribution

**PageRank flow analysis:**
- Which pages receive the most internal links?
- Which pages receive the fewest?
- Does distribution match business priority?

**Common problems:**
| Problem | Description | Fix |
|---------|-------------|-----|
| Homepage hoarding | Homepage has 500 outlinks | Consolidate navigation, use hub pages |
| Orphan cluster | Group of pages only link to each other | Add links from main site sections |
| Dead ends | Pages with no outbound internal links | Add contextual links to related content |
| Link silos | Sections don't link between each other | Add cross-section contextual links |

### 4. Anchor Text Analysis

**Good anchor text:**
- Descriptive of target page content
- Contains relevant keywords naturally
- Varies across different linking pages

**Bad anchor text patterns:**
| Pattern | Example | Problem |
|---------|---------|---------|
| Generic | "click here", "read more" | No keyword signal |
| Over-optimized | Every link = "best SEO tool" | Looks spammy |
| Naked URLs | "https://site.com/page" | Wastes keyword opportunity |
| Mismatched | Anchor = "dogs", target = cat page | Confusing signal |

### 5. Broken Internal Links
Links pointing to 404 pages within your own site.

**Impact:**
- Wastes link equity
- Bad user experience
- Wastes crawl budget

### 6. Nofollow on Internal Links
Using `rel="nofollow"` on internal links = bad practice.

**When it's wrong:**
- Regular content links marked nofollow
- Navigation links marked nofollow

**When it's acceptable:**
- User-generated content (comments)
- Login/signup pages (PageRank sculpting is dead, but still ok)

### 7. Link Equity Sinks
Pages that receive lots of internal links but provide no value:
- Thank you pages
- Login pages
- Terms of service (linked from every page footer)

**Solution:** Add `nofollow` or reduce links to low-value pages.

### 8. Contextual vs Navigation Links

| Type | Description | SEO Value |
|------|-------------|-----------|
| Navigation | Header, footer, sidebar | Lower (same on every page) |
| Contextual | Within article content | Higher (unique, topically relevant) |

**Goal:** Important pages should have BOTH navigation AND contextual links.

## Analysis Method

### Step 1: Crawl Site
- Use crawler to discover all pages
- Record all internal links (source URL, target URL, anchor text)

### Step 2: Build Link Graph
- Create adjacency matrix of page relationships
- Calculate inbound/outbound link counts per page

### Step 3: Calculate Metrics
- **Click depth**: BFS from homepage
- **Internal PageRank**: Simplified PageRank calculation
- **Orphan detection**: Pages with 0 inbound links

### Step 4: Cross-Reference with Goals
- Which pages should rank? (money pages, pillar content)
- Do those pages have strong internal link support?

## Output Format

### Internal Link Health Score: XX/100

### Site Structure Overview
```
Total pages: XXX
Total internal links: XXX
Average links per page: XX
Max click depth: X

Link Distribution:
├── Depth 1: XX pages (XX%)
├── Depth 2: XX pages (XX%)
├── Depth 3: XX pages (XX%)
├── Depth 4+: XX pages (XX%)
└── Orphans: XX pages (XX%)
```

### Critical Issues

#### Orphan Pages (XX found)
| URL | In Sitemap? | Suggested Link From |
|-----|-------------|---------------------|

#### Deep Pages (6+ clicks) (XX found)
| URL | Current Depth | Suggested Link From |

#### Broken Internal Links (XX found)
| Source URL | Broken Link | Suggested Fix |

### Link Equity Analysis

#### Top 10 Pages by Internal Links
| URL | Inbound Links | Is Priority Page? |

#### Under-Linked Priority Pages
| URL | Current Links | Recommended Links |

### Anchor Text Report

#### Over-Optimized Anchors
| Anchor Text | Count | Target Pages |

#### Generic Anchors (fix these)
| Anchor Text | Count | Better Alternative |

### Recommendations
1. [Specific fix instructions based on findings]

---

## Part 2: Link Generation Mode

### When to Use

After writing a new article and unsure where to link.

### Input

1. **New article content** (or URL)
2. **Site existing page list** (or website URL to crawl)

### Process

#### Step 1: Analyze New Article
- Extract article topic, keywords
- Identify linkable concepts/terms

#### Step 2: Match with Existing Pages
- Find existing pages related to new article topic
- Sort by relevance

#### Step 3: Generate Suggestions

**Output 3 types of suggestions**:

| Type | Description |
|------|-------------|
| **Outbound** | Existing pages the new article should link to |
| **Inbound** | Existing pages that should add links to new article |
| **Anchor Text** | Suggested anchor text for each link |

### Output Format

```markdown
# Internal Link Suggestions

## New Article Info
- Title: [Article title]
- URL: [Article URL]
- Topic: [Main topic]
- Keywords: [Keyword list]

## Outbound Links (New Article → Existing Pages)

| Link Location | Target Page | Suggested Anchor | Reason |
|---------------|-------------|------------------|--------|
| Paragraph 2 "SEO optimization" | /seo-guide | "SEO optimization guide" | Topic related |
| Paragraph 5 "keyword research" | /keyword-research | "keyword research methods" | Deep reading |
| Ending CTA | /services | "our services" | Conversion |

## Inbound Links (Existing Pages → New Article)

| Source Page | Suggested Location | Suggested Anchor |
|-------------|-------------------|------------------|
| /seo-guide | "internal links" related paragraph | "internal link strategy" |
| /blog-index | Latest articles list | [Article title] |

## Implementation Checklist

- [ ] Add link to /seo-guide in new article paragraph 2
- [ ] Add link to /keyword-research in new article paragraph 5
- [ ] Update /seo-guide to add backlink
```

### Example

```
User: I wrote an article about "Core Web Vitals optimization", where should I link?

Claude: [Read article content]
        [Read site existing pages]
        [Match related pages]

Output:
- Link to /technical-seo ("technical SEO")
- Link to /page-speed ("page speed optimization")
- Link to /google-ranking-factors ("Google ranking factors")
- Suggest /technical-seo backlink to this new article
```

---

## Commands

| Command | Mode |
|---------|------|
| `/seo internal-links https://example.com` | Analysis mode |
| `/seo internal-links suggest [new-article]` | Generation mode |

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
