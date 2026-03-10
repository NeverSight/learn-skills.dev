---
name: pseo-discovery
description: Analyze a codebase and business context to discover programmatic SEO opportunities, identifying what page types to generate, what data assets exist, and what search intent can be matched at scale. Use when starting a new pSEO project, when the user isn't sure what to build programmatically, or when exploring what structured data exists in the codebase or business that could power scalable pages.
argument-hint: "[focus: codebase | business | keywords | all]"
allowed-tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
---

# pSEO Discovery

Analyze the codebase, business context, and market to determine what programmatic SEO pages can and should be built. This skill answers the question: **"What should we generate, and do we have the data to do it?"**

This skill runs BEFORE pseo-audit. The audit checks if the codebase is ready; this skill figures out what to build.

## Core Principles

1. **Data-first**: Only propose page types backed by structured data that exists or can be sourced
2. **Intent-matched**: Every proposed page type must target a real search intent with volume
3. **Differentiated**: Each page must be able to produce genuinely unique content — not just variable swaps
4. **Feasible**: Proposals must be realistic given the current data, codebase, and team capacity
5. **Business-aligned**: pSEO pages should serve the business's actual audience and goals

## Discovery Procedure

### 1. Explore the Codebase for Data Assets

Search the codebase for existing structured data that could power pages:

**Database/ORM models:**
- Search for schema definitions (Prisma, Drizzle, TypeORM, Mongoose, SQL migrations)
- Identify entities with many records (products, locations, services, users, listings, articles)
- Note which entities have rich attributes (descriptions, categories, images, metadata)

**CMS content types:**
- Check for headless CMS configs (Contentful, Sanity, Strapi, etc.)
- Identify content types and their field schemas
- Count records per content type

**API endpoints:**
- Map all API routes and their response shapes
- Identify list endpoints that return collections of entities
- Check for paginated endpoints (signals large datasets)

**Static data files:**
- Search for JSON, CSV, YAML, MDX files in `data/`, `content/`, `src/data/` directories
- Count records and inspect field richness
- Check for categorization or taxonomy structures

**What to extract per data source:**
- Entity name and count (e.g., "2,500 products", "150 cities", "80 services")
- Available fields (especially: name, description, category, attributes, images)
- Relationships between entities (product → category, service → location)
- Data freshness (how often updated, is there a lastModified field)

### 2. Map Business Entities to Page Types

For each data asset found, evaluate whether it can power a pSEO page type:

| Question | Must answer "yes" |
|----------|-------------------|
| Are there 50+ unique records? | Minimum for pSEO to make sense |
| Does each record have enough data for a full page? | Title, description, 3+ unique attributes |
| Would someone search for this? | Real search intent exists |
| Can each page be meaningfully different? | Not just variable swaps |
| Does this serve the business? | Drives traffic the business can convert |

**Common pSEO page patterns by business type:**

- **E-commerce**: Product pages, category pages, brand pages, `[product] vs [product]` comparisons, `best [category] for [use-case]`
- **SaaS**: Feature pages, integration pages, `[tool] alternative`, `[tool] vs [competitor]`, use-case pages
- **Marketplace**: Listing pages, location pages, `[service] in [city]`, category + location combinations
- **Content/Media**: Topic pages, tag pages, author pages, `[topic] guide`, glossary/definition pages
- **Local business**: Service + location pages, `[service] in [neighborhood]`, FAQ pages per service
- **Directory**: Profile pages, category pages, comparison pages, `top [category] in [location]`

### 3. Identify Keyword Patterns and Search Intent

For each proposed page type, validate that search demand exists:

**Keyword pattern analysis:**
- Identify the base keyword pattern (e.g., `[service] in [city]`, `best [product] for [use-case]`)
- Estimate volume per pattern using keyword research tools or inferred demand
- Check for long-tail variations that indicate intent depth
- Verify that existing top results are not exclusively high-authority domains

**Intent classification per page type:**
- **Informational**: User wants to learn (guides, definitions, how-tos)
- **Commercial investigation**: User is comparing options (comparisons, reviews, "best X")
- **Transactional**: User wants to buy/sign up (product pages, pricing, service pages)
- **Navigational**: User wants a specific entity (brand pages, location pages)

Each pSEO page type should clearly map to one intent category.

### 4. Evaluate Data Sufficiency for Content Uniqueness

For each proposed page type, assess whether the data produces genuinely unique pages:

**The Content Differentiation Test:**
Take 5 random records. For each, write out what the page would contain:
- Title
- H1
- Intro paragraph
- Main content sections
- FAQ questions

If 3+ of these elements are essentially the same text with different proper nouns, the data is insufficient. Either:
- Enrich the data (add more attributes, descriptions, FAQs per record)
- Combine data sources (e.g., product data + user reviews + competitor data)
- Narrow the page type to records with richer data
- Abandon the page type as a pSEO candidate

**Minimum data requirements per page:**
- 2+ unique text fields beyond title and description (for body content)
- 3+ structured attributes (for data tables, stat highlights)
- Category or taxonomy data (for hub-spoke linking)
- Ideally: 3-5 FAQ pairs per record (for FAQ schema and content depth)

### 5. Assess URL Structure and Taxonomy

Propose a URL hierarchy for the pSEO pages:

```
/{category}/{slug}                     # standard
/{location}/{service}                  # location-based
/{product-type}/{product-slug}         # e-commerce
/{topic}/{subtopic}                    # content-based
```

Check:
- Will all slugs be unique within their URL namespace?
- Does the hierarchy create natural hub-spoke relationships?
- Is the URL structure human-readable and keyword-inclusive?
- How deep is the hierarchy? (Maximum 3 levels recommended)

### 6. Competitive Landscape Check

Identify whether competitors are already doing pSEO for the same patterns:

- Search for the target keyword patterns and see what ranks
- Check if competitors have programmatic pages (signs: similar URL patterns, templated content, large indexed page counts)
- Assess competitor content quality — can you do meaningfully better?
- Look for gaps they haven't covered (long-tail variations, underserved locations, new categories)

### 7. Propose a pSEO Strategy

Compile findings into a ranked list of pSEO opportunities.

## Output Format

```
## pSEO Discovery Report

### Data Assets Found
| Entity | Record Count | Key Fields | Source |
|--------|-------------|------------|--------|
| [entity] | [count] | [fields] | [DB/CMS/API/files] |

### Proposed Page Types (ranked by opportunity)

#### 1. [Page Type Name]
- **Pattern**: [URL pattern, e.g., /services/[service]-in-[city]]
- **Record count**: [number of pages this would generate]
- **Search intent**: [informational / commercial / transactional]
- **Keyword pattern**: [e.g., "[service] in [city]"]
- **Data source**: [where the data comes from]
- **Content uniqueness**: [High / Medium / Low — with justification]
- **Data gaps**: [what fields are missing or need enrichment]
- **Feasibility**: [Ready / Needs data enrichment / Needs new data source]

#### 2. [Next page type...]

### Rejected Candidates
| Entity | Reason Rejected |
|--------|----------------|
| [entity] | [too few records / insufficient data / no search intent / ...] |

### Recommended URL Structure
[Proposed hierarchy with examples]

### Data Enrichment Needed
[List of data fields that need to be added to unlock page types]

### Next Steps
1. [Confirm page types with stakeholder]
2. [Enrich data where needed]
3. [Run pseo-audit on the codebase]
4. [Begin implementation with pseo-data]
```

## Scope Parameter

If `$ARGUMENTS` specifies a focus:
- `all` (default): Full discovery
- `codebase`: Only analyze existing data assets in the code (steps 1-2)
- `business`: Focus on business entity mapping and page type proposals (steps 2-4)
- `keywords`: Focus on keyword patterns and competitive landscape (steps 3, 6)

## YMYL Risk Assessment

Google's September 2025 Quality Rater Guidelines expanded YMYL (Your Money or Your Life) to include civic information alongside health, finance, and legal content. pSEO in YMYL verticals carries elevated risk.

**YMYL categories (as of September 2025):**
- Health and medical information
- Financial information (investing, taxes, loans, insurance)
- Legal information
- Civic information (voting, government, public trust)
- Safety information (product safety, emergency procedures)
- News about major events

**If the proposed page types fall into ANY YMYL category:**

1. **Flag the risk explicitly** in the discovery report
2. **Elevate content quality requirements**: Every page needs cited authoritative sources, expert attribution, and review processes
3. **Evaluate if pSEO is appropriate at all**: YMYL content often requires human expert review per page, which conflicts with the "programmatic" approach. Be honest about this tension.
4. **Recommend stricter quality guard thresholds**: Higher minimum word counts, stricter uniqueness requirements, mandatory E-E-A-T fields
5. **Consider hybrid approach**: Programmatic data structure + human-reviewed content per page

**Discovery output should include a YMYL assessment:**
```
### YMYL Assessment
- YMYL category: [None | Health | Finance | Legal | Civic | Safety]
- Risk level: [Low | Medium | High]
- Recommendation: [Standard pSEO OK | Needs elevated quality standards | Human review per page required | pSEO not recommended for this vertical]
```

## Output Artifact

Save the discovery report to `.pseo/discovery-report.md` in the project root. This file is consumed by pseo-audit and pseo-orchestrate to inform subsequent phases. The file must include at minimum:

- Confirmed page types with their URL patterns
- Data source locations (file paths, API endpoints, CMS content types)
- YMYL assessment (if applicable)
- Data gaps that need enrichment before implementation

If running within a single Claude Code session, the report can also be kept in conversation context. The file serves as a persistent artifact for multi-session workflows.

## Important Constraints

- This is a research-only skill. Do NOT modify code or create files.
- Be honest about data gaps. Don't propose page types the data can't support.
- Quantity of pages is not the goal. 200 genuinely unique pages beats 5,000 thin pages.
- If the codebase has no usable structured data, say so. The answer may be "build the data layer first" or "this business isn't a good fit for pSEO."
- If a page type would produce thin or near-identical pages, flag it as rejected with a clear reason.

## Relationship to Other Skills

- **Runs before**: All other pseo-* skills
- **Feeds into**: pseo-audit (what to look for), pseo-data (what models to build)
- **Independent of**: All implementation skills — this is pure research
