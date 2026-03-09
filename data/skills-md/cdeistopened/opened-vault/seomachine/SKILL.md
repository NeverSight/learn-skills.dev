---
name: seomachine
description: SEO data platform - keyword research, rankings, traffic, competitor analysis, content briefs, and performance reports. Adapts to any SEO research or analysis task.
---

# SEOMachine

Unified SEO data platform. Use for any SEO-related task - keyword research, performance tracking, competitor analysis, content planning, or reporting.

## Credentials

All credentials in vault `.env` file. Scripts read from environment variables:

```
DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
GA4_PROPERTY_ID (451203520)
GOOGLE_SERVICE_ACCOUNT_PATH
GSC_SITE_URL (https://opened.co/)
KEYWORDS_EVERYWHERE_API_KEY
```

**DO NOT hardcode credentials in scripts.**

---

## Tool Map

### Scripts (Ready-to-Run)

| Script | Purpose | Command |
|--------|---------|---------|
| `weekly_seo_report.py` | Full performance report | `python3 scripts/weekly_seo_report.py --domain opened.co` |
| `content_brief_generator.py` | Competitor-informed brief | `python3 scripts/content_brief_generator.py "keyword"` |
| `competitor_gap_finder.py` | Keywords we're missing | `python3 scripts/competitor_gap_finder.py --competitor domain.com` |

### Modules (Import for Custom Queries)

| Module | Class | Key Methods |
|--------|-------|-------------|
| `dataforseo.py` | `DataForSEO` | `get_keyword_ideas()`, `get_serp_data()`, `get_questions()`, `analyze_competitor()` |
| `google_analytics.py` | `GoogleAnalytics` | `get_top_pages()`, `get_declining_pages()`, `get_page_trends()`, `get_traffic_sources()` |
| `google_search_console.py` | `GoogleSearchConsole` | `get_keyword_positions()`, `get_quick_wins()`, `get_low_ctr_pages()`, `get_page_performance()` |
| `data_aggregator.py` | `DataAggregator` | `identify_content_opportunities()`, `generate_performance_report()`, `get_priority_queue()` |
| `keyword_analyzer.py` | `KeywordAnalyzer` | Keyword clustering, difficulty analysis |
| `search_intent_analyzer.py` | `SearchIntentAnalyzer` | Classify search intent |
| `seo_quality_rater.py` | `SEOQualityRater` | Score content for SEO |
| `content_length_comparator.py` | `ContentLengthComparator` | Compare to competitors |
| `hubspot.py` | `HubSpot` | Email/contact data |
| `meta.py` | `Meta` | Facebook/Instagram metrics |
| `youtube.py` | `YouTube` | YouTube analytics |
| `webflow.py` | `Webflow` | CMS publishing |
| `keywords_everywhere.py` | `KeywordsEverywhere` | Related keywords, PASF, volume, backlinks, domain keywords |

### References

| File | Content |
|------|---------|
| `references/seo-guidelines.md` | SEO best practices |
| `references/target-keywords.md` | Priority keyword list |
| `references/internal-links-map.md` | Internal linking structure |

---

## Common Tasks

### "What keywords should we target?"

```bash
# Generate content brief with keyword cluster
python3 .claude/skills/seomachine/scripts/content_brief_generator.py "homeschool curriculum"

# Find gaps vs competitors
python3 .claude/skills/seomachine/scripts/competitor_gap_finder.py --batch --min-volume 200
```

### "How is our content performing?"

```bash
# Full weekly report
python3 .claude/skills/seomachine/scripts/weekly_seo_report.py --domain opened.co --output markdown
```

### "What's ranking/trending?"

```python
# Custom query using modules
import sys
sys.path.insert(0, ".claude/skills/seomachine/modules")
from google_search_console import GoogleSearchConsole

gsc = GoogleSearchConsole()
quick_wins = gsc.get_quick_wins(days=28)  # Keywords at position 11-20
trending = gsc.get_trending_queries()      # Rising searches
```

### "What content needs refresh?"

```python
from google_analytics import GoogleAnalytics

ga = GoogleAnalytics()
declining = ga.get_declining_pages(comparison_days=30, threshold_percent=-20)
```

### "Combined analysis"

```python
from data_aggregator import DataAggregator

agg = DataAggregator()
opportunities = agg.identify_content_opportunities()
# Returns: quick_wins, declining_content, low_ctr, trending_topics
```

---

## Script Details

### weekly_seo_report.py

Generates comprehensive weekly SEO report.

```bash
# Console output
python3 scripts/weekly_seo_report.py --domain opened.co

# Markdown output
python3 scripts/weekly_seo_report.py --domain opened.co --output markdown

# Save to file
python3 scripts/weekly_seo_report.py --domain opened.co --output markdown --save report.md

# Skip history tracking (dry run)
python3 scripts/weekly_seo_report.py --domain opened.co --no-history
```

**Output includes:**
- Priority keyword tracking (from PRIORITY_KEYWORDS dict)
- Quick wins (position 11-20)
- Declining content alerts
- Keyword opportunities
- Week-over-week changes

### content_brief_generator.py

Generates competitor-informed content brief.

```bash
python3 scripts/content_brief_generator.py "keyword phrase"
python3 scripts/content_brief_generator.py "waldorf vs montessori" --scrape-top-n 10
```

**Output includes:**
- Primary keyword metrics (volume, CPC, competition)
- Secondary keyword cluster (top 20)
- Top 10 SERP results
- Competitor H2/H3 structure (scraped)
- FAQ questions to answer
- Recommended word count
- Differentiation opportunities

### competitor_gap_finder.py

Finds keywords competitors rank for that we don't.

```bash
# Single competitor
python3 scripts/competitor_gap_finder.py --competitor cathyduffy.com --min-volume 200

# Batch (default competitor set)
python3 scripts/competitor_gap_finder.py --batch --min-volume 100

# With keyword limit (cost control)
python3 scripts/competitor_gap_finder.py --competitor hslda.org --max-keywords 500
```

---

## Module API Reference

### DataForSEO

```python
from dataforseo import DataForSEO
dfs = DataForSEO()

# Keyword research
ideas = dfs.get_keyword_ideas("homeschool", limit=100)
questions = dfs.get_questions("homeschool curriculum", limit=50)

# SERP analysis
serp = dfs.get_serp_data("best homeschool curriculum")
# Returns: search_volume, cpc, competition, organic_results, features

# Check rankings
rankings = dfs.get_rankings(domain="opened.co", keywords=["homeschool", "virtual school"])

# Competitor analysis
comparison = dfs.analyze_competitor("cathyduffy.com", keywords=["curriculum reviews"])

# Domain metrics
metrics = dfs.get_domain_metrics("opened.co")
```

### GoogleAnalytics

```python
from google_analytics import GoogleAnalytics
ga = GoogleAnalytics()

# Top pages
top = ga.get_top_pages(days=30, limit=20, path_filter="/blog/")

# Traffic trends for specific page
trends = ga.get_page_trends("/blog/waldorf-vs-montessori", days=90)

# Declining content
declining = ga.get_declining_pages(comparison_days=30, threshold_percent=-20)

# Traffic sources
sources = ga.get_traffic_sources(days=30)
```

### GoogleSearchConsole

```python
from google_search_console import GoogleSearchConsole
gsc = GoogleSearchConsole()

# Current rankings
positions = gsc.get_keyword_positions(days=28)

# Quick wins (position 11-20, high impressions)
quick_wins = gsc.get_quick_wins(days=28)

# Low CTR opportunities
low_ctr = gsc.get_low_ctr_pages(days=28)

# Page performance
perf = gsc.get_page_performance("/blog/waldorf-vs-montessori", days=28)

# Trending queries
trending = gsc.get_trending_queries()
```

### DataAggregator

```python
from data_aggregator import DataAggregator
agg = DataAggregator()

# All opportunities in one call
opportunities = agg.identify_content_opportunities(days=30)
# Returns dict with: quick_wins, declining_content, low_ctr, trending_topics

# Full performance report
report = agg.generate_performance_report(days=30)

# Priority task queue
tasks = agg.get_priority_queue(limit=10)

# Comprehensive page analysis
page_data = agg.get_comprehensive_page_performance("/blog/article", days=30)
```

### Keywords Everywhere

```python
from keywords_everywhere import KeywordsEverywhere
ke = KeywordsEverywhere()

# Check credits
credits = ke.get_credits()

# Keyword data (volume, CPC, competition, trends) - up to 100 per call, auto-batches
data = ke.get_keyword_data(["homeschool curriculum", "virtual school", "montessori"])

# Related keywords (builds topical clusters)
related = ke.get_related_keywords("homeschool curriculum")

# People Also Search For (user intent paths, FAQ ideas)
pasf = ke.get_pasf_keywords("homeschool curriculum")

# Full keyword universe from seeds (related + PASF, deduplicated, sorted by volume)
universe = ke.keyword_universe(["homeschool", "virtual school", "open education"])

# Domain keywords (what a domain ranks for)
comp_kws = ke.get_domain_keywords("cathyduffy.com")

# URL-level keywords
url_kws = ke.get_url_keywords("https://opened.co/blog/best-homeschool-math-curriculum")

# Traffic estimates
traffic = ke.get_domain_traffic(["opened.co", "cathyduffy.com", "hslda.org"])

# Backlinks
backlinks = ke.get_domain_backlinks("cathyduffy.com")
unique_backlinks = ke.get_unique_domain_backlinks("cathyduffy.com")

# Competitor keyword overlap (finds gaps and shared keywords)
overlap = ke.competitor_keyword_overlap(
    "opened.co",
    ["cathyduffy.com", "thehomeschoolmom.com", "hslda.org"]
)
```

**Cost:** 1 credit per keyword. $10 = 100K credits. Auto-batches >100 keywords.

**Best combos with DataForSEO:**
- KE `keyword_universe()` for seed expansion → DFS `get_serp_data()` for difficulty + SERP features
- KE `get_pasf_keywords()` for FAQ content ideas → DFS `get_rankings()` to check current position
- KE `competitor_keyword_overlap()` for gap finding → DFS `analyze_competitor()` for ranking comparison

---

## Notes

- GSC data has ~3 day delay
- DataForSEO costs money per API call - be efficient, cache results
- GA4 property: 451203520 (opened.co)
- Service account: opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com
