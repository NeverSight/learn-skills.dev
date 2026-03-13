---
name: seo-keywords
description: |
  Revenue-focused keyword research and strategy for SEO campaigns. Handles keyword discovery,
  clustering, search intent mapping, difficulty assessment, competitor gap analysis, topical
  authority mapping, SERP feature analysis, competitor content strategy reverse engineering,
  and programmatic SEO template generation.

  USE FOR:
  - "keyword research", "find keywords", "keyword strategy"
  - "competitor keywords", "keyword gap analysis"
  - "search intent", "keyword clustering"
  - "what should I rank for", "content opportunities"
  - "topic map", "topical authority", "pillar content"
  - "SERP features", "SERP analysis"
  - "competitor content strategy", "content reverse engineering"
  - "programmatic SEO", "location pages", "comparison pages"
  - Any request about finding or analyzing search terms

  Supports two workflows: local/service businesses and SaaS/online companies.
  Multi-client: stores results in .seo/clients/{client}/keywords/
---

# SEO Keyword Strategy

Always load client context first. See [rules/client-setup.md](rules/client-setup.md) for the client loading pattern.

## File Organization

Save all output to `.seo/clients/{slug}/keywords/`:

```
keywords/
├── research-{date}.json           # Raw keyword research
├── clusters.json                  # Keyword clusters
├── competitor-gap.json            # Gap analysis
├── topic-map.json                 # Topical authority map
├── serp-features-{date}.json      # SERP feature analysis
├── competitor-strategy.json       # Competitor content RE
└── programmatic-templates/        # Template patterns
    ├── location-template.json
    └── comparison-template.json
```

## Workflow A: Local/Service Business Keywords

For clients with `business_type: "local"`.

### Step 1: Seed Keyword Discovery

```bash
# Search for core service + location combinations
firecrawl search "{service} {city}" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/seed-{service}.json --json
firecrawl search "{service} near me" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/seed-nearme.json --json
firecrawl search "best {service} in {city}" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/seed-best.json --json
```

Run in parallel for each service and service area from client config.

### Step 2: Competitor Keyword Extraction

```bash
# Map competitor sites to find all their pages
firecrawl map {competitor-domain} --search "{industry}" -o .seo/clients/{slug}/keywords/.firecrawl/comp-{name}-urls.txt &
# Repeat for each competitor in parallel
wait

# Scrape competitor service pages for keyword patterns
firecrawl scrape {competitor-url} --format markdown,links -o .seo/clients/{slug}/keywords/.firecrawl/comp-{name}-page.json
```

Extract from competitor pages: title tags, H1s, H2s, service names, location modifiers, URL slugs. These reveal the keywords they target.

### Step 3: Local Keyword Expansion

Generate geo-modified variants for each core service:
- `{service} {city}` — primary
- `{service} {city} {state}` — long-tail
- `{service} near {neighborhood}` — hyperlocal
- `{service} in {zip_code}` — zip-targeted
- `best {service} {city}` — commercial intent
- `{service} cost {city}` — transactional
- `emergency {service} {city}` — urgent intent
- `{service} reviews {city}` — social proof

### Step 4: Revenue Mapping

Classify each keyword by revenue potential:
- **High**: directly leads to service booking (e.g., "emergency plumber austin")
- **Medium**: research phase but close to conversion (e.g., "plumber cost austin")
- **Low**: informational, builds authority (e.g., "how to fix a leaky faucet")

Prioritize high-revenue keywords first. Low-revenue informational keywords support topical authority.

## Workflow B: SaaS/Online Business Keywords

For clients with `business_type: "saas"` or `"ecommerce"`.

### Step 1: Product-Led Discovery

```bash
# Search for product category and feature keywords
firecrawl search "{product-category} software" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/product-cat.json --json
firecrawl search "{product-name} alternatives" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/alternatives.json --json
firecrawl search "{problem-solved} tools" --limit 20 -o .seo/clients/{slug}/keywords/.firecrawl/problem-tools.json --json
```

### Step 2: Funnel-Stage Classification

- **BOFU (Bottom of Funnel)**: "{product} pricing", "{product} vs {competitor}", "buy {product}", "{product} demo"
- **MOFU (Middle of Funnel)**: "best {category} software", "how to {solve problem}", "{category} comparison"
- **TOFU (Top of Funnel)**: "what is {concept}", "{industry} trends", "{problem} guide"

### Step 3: Feature vs Problem Keywords

- **Feature keywords**: "{feature-name} software", "tool with {feature}"
- **Problem keywords**: "how to {solve problem}", "{pain point} solution"
- **Use-case keywords**: "{product-category} for {industry}", "{product-category} for {team-size}"

## Keyword Clustering

Group keywords into clusters by semantic similarity and shared SERP results.

### Method

For each seed keyword group, search Google via firecrawl and compare the top 10 results. Keywords that share 3+ of the same top 10 URLs belong to the same cluster.

```bash
# Search for each keyword to see SERP overlap
firecrawl search "{keyword}" --limit 10 -o .seo/clients/{slug}/keywords/.firecrawl/serp-{keyword-slug}.json --json
```

### Output Format

```json
{
  "clusters": [
    {
      "name": "Cluster Name",
      "pillar_keyword": "main keyword",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "intent": "commercial",
      "estimated_volume": "high|medium|low",
      "recommended_page_type": "service-page|blog-post|landing-page|comparison-page",
      "current_url": null,
      "gap": true
    }
  ]
}
```

## Search Intent Classification

For each keyword, classify intent based on SERP analysis:

| Intent | SERP Signals | Examples |
|--------|-------------|----------|
| **Transactional** | Product pages, pricing, buy buttons dominate | "buy X", "X pricing", "X coupon" |
| **Commercial** | Comparison pages, reviews, listicles dominate | "best X", "X vs Y", "X reviews" |
| **Informational** | Blog posts, how-tos, Wikipedia dominate | "what is X", "how to X", "X guide" |
| **Navigational** | Brand homepages, login pages dominate | "X login", "X website", brand names |

## Difficulty Assessment

For each target keyword, analyze the top 10 SERP results:

```bash
firecrawl search "{keyword}" --scrape --limit 10 -o .seo/clients/{slug}/keywords/.firecrawl/difficulty-{slug}.json --json
```

Score difficulty (1-10) based on:
- **Content depth**: avg word count of top 10 results
- **Domain authority signals**: well-known brands vs niche sites
- **Content freshness**: how recently updated
- **SERP feature presence**: featured snippets, PAA boxes (more features = more competition)
- **Content type match**: can you create the same content type as top results?

## Competitor Keyword Gap Analysis

Compare client's content against 2-3 competitors:

```bash
# Map all pages for client and each competitor
firecrawl map {client-domain} -o .seo/clients/{slug}/keywords/.firecrawl/client-urls.txt &
firecrawl map {competitor1-domain} -o .seo/clients/{slug}/keywords/.firecrawl/comp1-urls.txt &
firecrawl map {competitor2-domain} -o .seo/clients/{slug}/keywords/.firecrawl/comp2-urls.txt &
wait
```

Compare URL structures and page titles to identify topics competitors cover that the client does not. Output as prioritized gap list.

## Topical Authority Mapping

Build a content architecture around topic clusters:

### Step 1: Identify Pillar Topics

From keyword clusters, identify 3-5 broad pillar topics that the client should own. Each pillar becomes a comprehensive page (2000+ words).

### Step 2: Map Cluster Content

For each pillar, identify 8-15 supporting cluster articles that link back to the pillar page. Use keyword clusters to assign one cluster per article.

### Step 3: Internal Link Map

Define the linking structure:
- Each cluster article links to its pillar page
- Pillar page links to all cluster articles
- Related cluster articles interlink where natural

### Output Format

```json
{
  "pillars": [
    {
      "topic": "Pillar Topic Name",
      "pillar_keyword": "main keyword",
      "pillar_url": "/pillar-page-slug",
      "clusters": [
        {
          "title": "Cluster Article Title",
          "target_keyword": "cluster keyword",
          "url": "/cluster-slug",
          "status": "exists|gap",
          "links_to_pillar": true,
          "interlinks": ["/related-cluster-1", "/related-cluster-2"]
        }
      ]
    }
  ]
}
```

## SERP Feature Analysis

For target keywords, identify which SERP features appear and which the client can win:

```bash
firecrawl search "{keyword}" --scrape --limit 5 -o .seo/clients/{slug}/keywords/.firecrawl/serp-{slug}.json --json
```

Track these SERP features:
- **Featured Snippet** (paragraph, list, table) — optimize content format to match
- **People Also Ask** — create FAQ content for these questions
- **Image Pack** — optimize images with descriptive alt text and filenames
- **Video Carousel** — create video content for these queries
- **Local Pack** — requires GBP optimization (see seo-local skill)
- **Knowledge Panel** — requires entity optimization (see seo-aeo skill)
- **AI Overview** — requires AEO optimization (see seo-aeo skill)
- **Sitelinks** — requires clear site architecture and navigation

## Competitor Content Strategy Reverse Engineering

Analyze competitor content operations:

```bash
# Map all competitor content
firecrawl map {competitor-domain} --search "blog" -o .seo/clients/{slug}/keywords/.firecrawl/comp-blog-urls.txt
firecrawl map {competitor-domain} -o .seo/clients/{slug}/keywords/.firecrawl/comp-all-urls.txt
```

Then scrape a sample of pages to analyze:
- **Content types**: blog posts, landing pages, tools, comparisons, case studies
- **Publishing frequency**: estimate from URL dates, sitemap lastmod, or content dates
- **Content length patterns**: sample 10-15 pages, calculate avg word count by content type
- **Topic coverage**: map their content to your topic clusters to find their strengths/weaknesses
- **Update cadence**: look for "updated on" dates, fresh statistics, recent examples

## Programmatic SEO Templates

For SaaS/ecommerce clients with repeatable page patterns:

### Location Pages Template

```json
{
  "template_type": "location",
  "url_pattern": "/{service}-{city}-{state}",
  "title_pattern": "{Service} in {City}, {State} | {Brand}",
  "h1_pattern": "{Service} in {City}, {State}",
  "sections": [
    "Local intro paragraph with city-specific details",
    "Service description (shared, with local modifiers)",
    "Service area map / neighborhoods served",
    "Local testimonials / reviews",
    "FAQPage schema with city-specific FAQ",
    "CTA with local phone number"
  ],
  "schema_type": "LocalBusiness",
  "internal_links": ["pillar-service-page", "nearby-location-pages"]
}
```

### Comparison Pages Template

```json
{
  "template_type": "comparison",
  "url_pattern": "/{product}-vs-{competitor}",
  "title_pattern": "{Product} vs {Competitor}: {Year} Comparison",
  "h1_pattern": "{Product} vs {Competitor}",
  "sections": [
    "Quick verdict / summary table",
    "Feature-by-feature comparison",
    "Pricing comparison",
    "Pros and cons of each",
    "Who should choose which",
    "FAQPage schema"
  ],
  "schema_type": "Article",
  "internal_links": ["product-page", "pricing-page"]
}
```

### Category Pages Template

```json
{
  "template_type": "category",
  "url_pattern": "/best-{category}-{modifier}",
  "title_pattern": "Best {Category} for {Modifier} ({Year})",
  "sections": [
    "Quick picks / top 3 summary",
    "Evaluation criteria",
    "Detailed reviews of each option",
    "Comparison table",
    "How to choose guide",
    "FAQ section"
  ]
}
```

## Output Schema

All keyword data should follow this format:

```json
{
  "keyword": "emergency plumber austin",
  "cluster": "emergency-plumbing",
  "intent": "transactional",
  "difficulty": 6,
  "volume_estimate": "medium",
  "revenue_potential": "high",
  "funnel_stage": "bofu",
  "serp_features": ["local_pack", "paa", "ai_overview"],
  "recommended_page_type": "service-page",
  "current_url": null,
  "competitor_coverage": ["comp-a", "comp-b"],
  "priority": 1,
  "notes": ""
}
```
