---
name: iblai-marketing-programmatic-seo
description: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "integration pages," "building many pages for SEO," "pSEO," "generate 100 pages," "data-driven pages," or "templated landing pages." Use this whenever someone wants to create many similar pages targeting different keywords or locations. For auditing existing SEO issues, see iblai-marketing-seo-audit. For content strategy planning, see iblai-marketing-content-strategy.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-programmatic-seo

Build SEO-optimized pages at scale with templates and data. Pages must
rank, deliver value, and dodge thin-content penalties.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pin down before designing:

1. **Business context**
   - Product/service
   - Target audience
   - Conversion goal for these pages

2. **Opportunity assessment**
   - Search patterns that exist
   - Potential page count
   - Search volume distribution

3. **Competitive landscape**
   - Who ranks for these terms now
   - What their pages look like
   - Whether you can realistically compete

---

## Core Principles

1. **Unique value per page.** Every page provides value specific to it. Not just swapped variables in a template. Maximize unique content.
2. **Proprietary data wins.** Hierarchy of data defensibility:
   1. Proprietary (you created it)
   2. Product-derived (from your users)
   3. User-generated (your community)
   4. Licensed (exclusive access)
   5. Public (anyone can use — weakest)
3. **Clean URL structure.** **Use subfolders, not subdomains** — subfolders consolidate domain authority while subdomains split it:
   - Good: `yoursite.com/templates/resume/`
   - Bad: `templates.yoursite.com/resume/`
4. **Genuine search intent match.** Pages actually answer what people are searching for.
5. **Quality over quantity.** 100 great pages beat 10,000 thin ones.
6. **Avoid Google penalties.** No doorway pages. No keyword stuffing. No duplicate content. Genuine utility for users.

---

## The 12 Playbooks

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[Type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "$10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[product A] [product B] integration" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in multiple languages | Localized content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

Detailed playbook implementation: [references/playbooks.md](references/playbooks.md).

---

## Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

Layer multiple playbooks (e.g., "Best coworking spaces in San Diego").

---

## Implementation Framework

### 1. Keyword Pattern Research

**Identify the pattern:**
- Repeating structure?
- Variables?
- Number of unique combinations?

**Validate demand:**
- Aggregate search volume
- Volume distribution (head vs. long tail)
- Trend direction

### 2. Data Requirements

- What data populates each page?
- First-party, scraped, licensed, or public?
- How is it updated?

### 3. Template Design

**Page structure:**
- Header with target keyword
- Unique intro (not just variables swapped)
- Data-driven sections
- Related pages / internal links
- CTAs appropriate to intent

**Ensuring uniqueness:**
- Unique value per page
- Conditional content based on data
- Original insights/analysis per page

### 4. Internal Linking Architecture

**Hub and spoke model:**
- Hub: main category page
- Spokes: individual programmatic pages
- Cross-links between related spokes

**Avoid orphan pages:**
- Every page reachable from the main site
- XML sitemap for all pages
- Breadcrumbs with structured data

### 5. Indexation Strategy

- Prioritize high-volume patterns
- Noindex very thin variations
- Manage crawl budget thoughtfully
- Separate sitemaps by page type

---

## Quality Checks

### Pre-Launch Checklist

**Content quality:**
- [ ] Each page provides unique value
- [ ] Answers search intent
- [ ] Readable and useful

**Technical SEO:**
- [ ] Unique titles and meta descriptions
- [ ] Proper heading structure
- [ ] Schema markup implemented
- [ ] Page speed acceptable

**Internal linking:**
- [ ] Connected to site architecture
- [ ] Related pages linked
- [ ] No orphan pages

**Indexation:**
- [ ] In XML sitemap
- [ ] Crawlable
- [ ] No conflicting noindex

### Post-Launch Monitoring

Track: indexation rate, rankings, traffic, engagement, conversion.

Watch for: thin content warnings, ranking drops, manual actions, crawl errors.

---

## Common Mistakes

- **Thin content** — just swapping city names in identical content
- **Keyword cannibalization** — multiple pages targeting the same keyword
- **Over-generation** — creating pages with no search demand
- **Poor data quality** — outdated or incorrect information
- **Ignoring UX** — pages exist for Google, not users

---

## Output Format

### Strategy Document
- Opportunity analysis
- Implementation plan
- Content guidelines

### Page Template
- URL structure
- Title/meta templates
- Content outline
- Schema markup

---

## Task-Specific Questions

1. Keyword patterns you're targeting?
2. Data you have (or can acquire)?
3. How many pages are you planning?
4. Site authority?
5. Who currently ranks for these terms?
6. Technical stack?

---

## Related Skills

- **iblai-marketing-seo-audit**: Auditing programmatic pages after launch
- **iblai-marketing-schema-markup**: Adding structured data
- **iblai-marketing-site-architecture**: Page hierarchy, URL structure, internal linking
- **iblai-marketing-competitor-alternatives**: Comparison page frameworks
