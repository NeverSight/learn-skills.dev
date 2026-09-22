---
name: seo-content-marketing-skill-factory
description: SEO & content marketing command suite with keyword research, content audits, SERP analysis, technical SEO and workflow automation
triggers:
  - analyze keywords for SEO
  - run content audit
  - check technical SEO issues
  - analyze competitor gaps
  - generate SEO content brief
  - create content calendar
  - audit backlinks and prospecting
  - monitor SERP rankings
---

# SEO & Content Marketing Skill Factory

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## What This Project Does

A specialized skill suite derived from `alirezarezvani/claude-code-skill-factory` that provides 10 SEO and content marketing commands plus 5 multi-step workflows. Handles keyword research, content audits, SERP analysis, technical SEO diagnostics, competitor analysis, and content strategy with structured output and progress tracking.

**Core capabilities:**
- Keyword clustering and opportunity scoring
- Full-site content quality audits
- Technical SEO crawl analysis
- Competitor gap analysis (backlinks, topics, snippets)
- AI-powered content brief generation
- Rank tracking with volatility alerts
- Link prospecting and outreach
- Page speed SEO diagnostics
- Local SEO audits
- Data-driven content calendars

## Installation

```bash
# Clone the repository
git clone https://github.com/JaguarPillage/r04-alirezarezvani-claude-code-skill-factory-seo.git

# Navigate to the project
cd r04-alirezarezvani-claude-code-skill-factory-seo

# Install as Claude Code skill
mkdir -p ~/.claude/skills/
cp -r . ~/.claude/skills/seo-content-marketing/

# Register the skill in Claude Code session
/read ~/.claude/skills/seo-content-marketing/SKILL.md
```

## Command Reference

### `/keyword-research`

Deep keyword analysis with clustering, intent mapping, and opportunity scoring.

**Usage:**
```bash
/keyword-research <target_keyword_or_domain>
/keyword-research "project management software" --market us --lang en
/keyword-research example.com --export csv
```

**Parameters:**
- `target` — seed keyword or domain to analyze
- `--market` — country code (default: us)
- `--lang` — language code (default: en)
- `--export` — output format (json, csv, md)
- `--depth` — cluster depth 1-3 (default: 2)

**Output structure:**
```
┌─────────────────────────┬────────┬──────┬────────┬───────────────┐
│ Keyword                 │ Volume │ KD   │ Intent │ Opportunity   │
├─────────────────────────┼────────┼──────┼────────┼───────────────┤
│ project management tool │ 18,100 │  67  │ Com    │ High (8.2/10) │
│ pm software comparison  │  2,400 │  42  │ Info   │ Med (6.1/10)  │
│ free project tracker    │  8,900 │  38  │ Trans  │ High (7.9/10) │
└─────────────────────────┴────────┴──────┴────────┴───────────────┘

Cluster: "Project Management Software" (47 keywords, 124k monthly vol)
  → Commercial intent: 62%
  → Avg difficulty: 54
  → Top opportunity: "project management tool" (KD 67, vol 18.1k)
```

### `/content-audit`

Full-site content quality analysis with duplication and cannibalization detection.

**Usage:**
```bash
/content-audit example.com --scope full
/content-audit example.com --scope /blog/ --min-words 300
/content-audit example.com --check-duplicates --output report.md
```

**Parameters:**
- `domain` — target domain
- `--scope` — path filter (default: full site)
- `--min-words` — minimum content length threshold
- `--check-duplicates` — enable duplicate content analysis
- `--cannibalization` — check keyword cannibalization
- `--output` — export path

**Output example:**
```
Content Quality Score: 67/100

Issues by Severity:
🔴 Critical (12):
  • 12 pages with duplicate title tags
  • 8 pages with thin content (<300 words)

🟠 High (34):
  • 34 pages missing meta descriptions
  • 18 pages with keyword cannibalization

🟡 Medium (56):
  • 56 pages with low readability scores
  • 23 pages with broken internal links

Cannibalization Report:
  "project management" — 4 pages competing:
    /blog/pm-guide/ (rank: 12)
    /resources/pm-tips/ (rank: 18)
    /what-is-pm/ (rank: 24)
    /pm-software/ (rank: 31)
  → Recommend: consolidate into /blog/pm-guide/
```

### `/technical-seo`

Crawl budget, Core Web Vitals, schema markup, and indexability audit.

**Usage:**
```bash
/technical-seo example.com
/technical-seo example.com --check-schema --crawl-depth 3
/technical-seo example.com --vitals-only
```

**Parameters:**
- `domain` — target domain
- `--check-schema` — validate structured data
- `--crawl-depth` — max crawl depth (default: 2)
- `--vitals-only` — focus on Core Web Vitals
- `--user-agent` — custom user agent

**Output structure:**
```
╔══════════════════════════════════════════════════╗
║  Technical SEO Audit  —  example.com             ║
╠══════════════════════════════════════════════════╣
║  Crawling …            [██████████] 100%  ✓      ║
║  Analyzing speed …     [██████████] 100%  ✓      ║
║  Validating schema …   [███████░░░]  70%  …      ║
╚══════════════════════════════════════════════════╝

Core Web Vitals:
  LCP: 1.8s  ✓ Good
  FID: 45ms  ✓ Good
  CLS: 0.18  ⚠ Needs improvement

Indexability:
  ✓ robots.txt valid
  ✓ XML sitemap found (1,204 URLs)
  ⚠ 34 pages blocked by robots.txt but in sitemap
  ✗ 12 pages return 404 but indexed in Google

Schema Markup:
  ✓ Organization schema valid
  ✓ Article schema on 89% of blog posts
  ⚠ Product schema missing structured reviews
```

### `/competitor-gap`

Backlink gap, topic gap, and featured snippet opportunity analysis.

**Usage:**
```bash
/competitor-gap example.com competitor1.com competitor2.com
/competitor-gap example.com --competitors auto --limit 5
/competitor-gap example.com competitor.com --focus backlinks
```

**Parameters:**
- `domain` — your domain
- `competitors` — list of competitor domains or `auto`
- `--limit` — max competitors (default: 3)
- `--focus` — analysis type (backlinks, topics, snippets, all)

**Output:**
```
Backlink Gap Analysis:
  competitor1.com has 1,247 linking domains you don't
  Top gap opportunities:
    • techcrunch.com → competitor1.com/feature-launch
    • producthunt.com → competitor1.com/announcement
    • forbes.com → competitor1.com/interview

Topic Gap (keywords competitor ranks for, you don't):
  "project management templates" (vol: 14,800, KD: 52)
  "agile project management" (vol: 9,900, KD: 61)
  "gantt chart software" (vol: 6,600, KD: 58)

Featured Snippet Opportunities:
  "what is project management" — competitor1.com owns snippet
    Your page: /what-is-pm/ (rank: 4)
    → Optimize for paragraph snippet format
```

### `/content-brief`

AI-generated SEO content brief with outline, NLP terms, and targets.

**Usage:**
```bash
/content-brief "best project management software 2024"
/content-brief "how to create a gantt chart" --format listicle
/content-brief "project management tips" --min-words 2000 --competitors 5
```

**Parameters:**
- `target_keyword` — primary keyword
- `--format` — content type (guide, listicle, comparison, how-to)
- `--min-words` — target word count
- `--competitors` — number of top-ranking pages to analyze

**Output structure:**
```
SEO Content Brief
Target Keyword: "best project management software 2024"
Search Intent: Commercial investigation
Format: Comparison / Listicle
Target Length: 2,500-3,200 words

Top-ranking Analysis (10 competitors):
  Avg length: 2,847 words
  Avg headings: 14
  Avg images: 8
  Common formats: comparison table + feature breakdown

Recommended Outline:
  H1: Best Project Management Software in 2024 (Reviewed & Compared)
  H2: Quick Comparison Table
  H2: How We Tested & Ranked PM Software
  H2: #1. [Software Name] – Best for [Use Case]
    H3: Key Features
    H3: Pricing
    H3: Pros & Cons
  [... repeat for top 7-10 tools]
  H2: What to Look for in PM Software
  H2: Frequently Asked Questions

NLP Terms to Include (top 20):
  • task management
  • team collaboration
  • gantt chart
  • resource allocation
  • time tracking
  • kanban boards
  • integrations
  [...]

Target Metrics:
  Word count: 2,500-3,200
  Headings: 12-16
  Images/screenshots: 8-12
  Internal links: 5-8
  External links: 3-5
```

### `/serp-monitor`

Daily rank tracking with volatility alerts and CTR optimization.

**Usage:**
```bash
/serp-monitor example.com --keywords keywords.txt
/serp-monitor example.com --auto-discover --limit 50
/serp-monitor example.com --alert-threshold 3
```

**Parameters:**
- `domain` — target domain
- `--keywords` — file path or comma-separated list
- `--auto-discover` — auto-detect ranking keywords
- `--limit` — max keywords to track
- `--alert-threshold` — position change alert threshold

### `/link-prospecting`

Quality backlink prospect discovery with outreach templates.

**Usage:**
```bash
/link-prospecting "project management" --da-min 40
/link-prospecting example.com/blog/article --similar-pages
/link-prospecting --niche "saas" --type guest-post
```

**Parameters:**
- `topic_or_url` — seed topic or content URL
- `--da-min` — minimum domain authority
- `--type` — prospect type (guest-post, resource-page, broken-link, unlinked-mention)
- `--similar-pages` — find pages linking to similar content

### `/page-speed-seo`

Page speed diagnostics mapped to SEO ranking impact.

**Usage:**
```bash
/page-speed-seo example.com
/page-speed-seo example.com/product --mobile
/page-speed-seo example.com --focus lcp
```

### `/local-seo`

NAP consistency, Google Business Profile optimization, local citations.

**Usage:**
```bash
/local-seo "Business Name" --location "New York, NY"
/local-seo --gmb-id BUSINESS_ID --audit-citations
```

### `/content-calendar`

Data-driven editorial calendar from search demand and seasonality.

**Usage:**
```bash
/content-calendar --niche "project management" --months 3
/content-calendar --domain example.com --analyze-gaps
/content-calendar --keywords keywords.csv --export calendar.csv
```

## Workflows

Multi-step orchestrated processes for end-to-end SEO campaigns.

### `full-seo-sprint`

Complete 12-step SEO sprint from audit to execution plan.

**Usage:**
```bash
/workflows:full-seo-sprint example.com --scope full
```

**Steps:**
1. Technical SEO audit
2. Content audit
3. Keyword research & clustering
4. Competitor gap analysis
5. SERP position baseline
6. Keyword mapping to pages
7. Content brief generation
8. Priority fix identification
9. Link prospecting
10. Content calendar creation
11. Implementation roadmap
12. KPI dashboard setup

### `launch-seo`

Pre-launch SEO validation checklist.

**Usage:**
```bash
/workflows:launch-seo example.com --pre-launch
```

**Validates:**
- Canonical tags
- Hreflang implementation
- XML sitemap
- Robots.txt
- Schema markup
- Meta tags
- Mobile-friendliness
- Page speed baseline

### `content-refresh`

Identify and refresh underperforming content.

**Usage:**
```bash
/workflows:content-refresh example.com --ranking-drop 5
```

### `authority-building`

End-to-end digital PR and link-building campaign.

**Usage:**
```bash
/workflows:authority-building --niche "saas" --target-links 50
```

### `ai-content-pipeline`

Automated keyword → brief → draft → optimize → publish pipeline.

**Usage:**
```bash
/workflows:ai-content-pipeline --keywords keywords.csv --output-dir ./content/
```

## Configuration

Create a `.seo-config.json` in your project root:

```json
{
  "domain": "example.com",
  "market": "us",
  "language": "en",
  "crawl_depth": 2,
  "api_keys": {
    "serp_api": "${SERP_API_KEY}",
    "ahrefs": "${AHREFS_API_KEY}",
    "semrush": "${SEMRUSH_API_KEY}"
  },
  "thresholds": {
    "min_word_count": 300,
    "max_page_speed_seconds": 3,
    "min_domain_authority": 30
  },
  "tracking": {
    "keywords_limit": 100,
    "check_frequency": "daily",
    "alert_threshold": 3
  }
}
```

**Environment variables:**
```bash
export SERP_API_KEY="your_api_key"
export AHREFS_API_KEY="your_api_key"
export SEMRUSH_API_KEY="your_api_key"
export GOOGLE_SEARCH_CONSOLE_CREDENTIALS="path/to/credentials.json"
```

## Common Patterns

### Pattern 1: New Site SEO Setup

```bash
# Run pre-launch validation
/workflows:launch-seo newsite.com --pre-launch

# Set up keyword research
/keyword-research "target niche" --depth 3 --export keywords.csv

# Create initial content calendar
/content-calendar --keywords keywords.csv --months 6 --export calendar.csv

# Generate content briefs for priority keywords
/content-brief "primary keyword 1" --format guide
/content-brief "primary keyword 2" --format listicle
```

### Pattern 2: Traffic Recovery

```bash
# Identify dropped rankings
/serp-monitor example.com --auto-discover --alert-threshold 5

# Audit existing content
/content-audit example.com --scope full --cannibalization

# Find content refresh opportunities
/workflows:content-refresh example.com --ranking-drop 5

# Analyze technical issues
/technical-seo example.com --check-schema
```

### Pattern 3: Competitor Analysis

```bash
# Run comprehensive gap analysis
/competitor-gap example.com competitor1.com competitor2.com --focus all

# Identify backlink opportunities
/link-prospecting example.com --similar-pages --da-min 40

# Map competitor topic coverage
/keyword-research competitor1.com --depth 2 --export competitor-keywords.csv
```

### Pattern 4: Content Production Pipeline

```bash
# Set up automated pipeline
/workflows:ai-content-pipeline --keywords high-priority.csv --output-dir ./drafts/

# Individual brief generation
/content-brief "target keyword" --format how-to --competitors 10

# Generate full calendar
/content-calendar --domain example.com --months 3 --analyze-gaps
```

## Troubleshooting

### Issue: "API rate limit exceeded"

**Solution:**
```bash
# Check API usage in config
cat .seo-config.json | grep -A 5 "api_keys"

# Reduce crawl depth
/technical-seo example.com --crawl-depth 1

# Use cached results
/content-audit example.com --use-cache
```

### Issue: "No keyword data returned"

**Cause:** Invalid market/language combination or API key.

**Solution:**
```bash
# Verify API credentials
echo $SERP_API_KEY  # should output key

# Test with default market
/keyword-research "test keyword" --market us --lang en

# Check available markets
/keyword-research --list-markets
```

### Issue: "Crawl timeout on large sites"

**Solution:**
```bash
# Limit scope
/content-audit example.com --scope /blog/

# Reduce depth
/technical-seo example.com --crawl-depth 1

# Use sitemap-only mode
/content-audit example.com --sitemap-only
```

### Issue: "Schema validation errors"

**Solution:**
```bash
# Run isolated schema check
/technical-seo example.com --check-schema --output schema-errors.json

# Validate specific URL
/technical-seo example.com/page --schema-only

# Get detailed error report
/technical-seo example.com --check-schema --verbose
```

### Issue: "Competitor analysis incomplete"

**Solution:**
```bash
# Auto-discover competitors
/competitor-gap example.com --competitors auto --limit 3

# Use manual list
/competitor-gap example.com comp1.com comp2.com --focus backlinks

# Split analysis by focus area
/competitor-gap example.com comp1.com --focus topics
/competitor-gap example.com comp1.com --focus backlinks
```

## Integration Examples

### Export to Google Sheets

```bash
# Export keyword research
/keyword-research "target" --export keywords.csv

# Convert and upload (requires gsheet-cli)
csv-to-sheets keywords.csv "SEO Research/Keywords" --credentials ${GOOGLE_CREDENTIALS}
```

### Combine with Analytics

```bash
# Get Search Console data
gsc-data example.com --days 90 --export gsc.csv

# Cross-reference with audit
/content-audit example.com --gsc-data gsc.csv --identify-opportunities
```

### CI/CD Integration

```bash
# Add to GitHub Actions workflow
- name: Pre-deploy SEO check
  run: |
    /workflows:launch-seo ${{ env.STAGING_URL }} --pre-launch --fail-on-critical
```

## Best Practices

1. **Always validate config before large audits**
   ```bash
   cat .seo-config.json | jq .
   ```

2. **Use scoped audits for faster iteration**
   ```bash
   /content-audit example.com --scope /blog/2024/
   ```

3. **Export results for historical tracking**
   ```bash
   /serp-monitor example.com --export rankings-$(date +%Y%m%d).csv
   ```

4. **Combine workflows for complete campaigns**
   ```bash
   /workflows:full-seo-sprint example.com --scope full --export report.md
   ```

5. **Set up automated monitoring**
   ```bash
   # Add to cron
   0 9 * * * /serp-monitor example.com --alert-threshold 3 --email alerts@example.com
   ```
