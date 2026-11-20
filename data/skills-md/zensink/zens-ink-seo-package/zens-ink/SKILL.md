---
name: zens-ink
description: >-
  Free SEO toolkit for indie builders. 22 zero-dependency Python tools covering
  the full SEO workflow: keyword discovery (Google Autocomplete), keyword clustering
  (semantic grouping), keyword difficulty (SERP structure analysis, no Ahrefs needed),
  KGR opportunity scoring, search volume (Bing + Brave), real Ahrefs Domain Rating
  (free public API), search intent classification (keyword + SERP-based), content
  opportunity matrix, Query Fan-out content planning (GEO/AI search), Reddit
  blue-ocean keyword mining, competitor content gap analysis (sitemap comparison),
  technical site audit (broken links, orphan pages, missing canonicals/H1/meta),
  on-page quality scoring (7 dimensions, 0-100 per page), robots.txt AI-crawler
  policy audit (AI-readiness score), llms.txt generation, pre-publish content QC,
  keyword rank tracking (SQLite history), and real ranking data (Google Search
  Console). Ships an MCP stdio server so any agent can drive every tool.
  Pure Python stdlib — no pip install required beyond this package. Optional API
  keys unlock volume data but all core tools work without any keys.
version: "1.4.12"
authors:
  - name: Jask
    url: https://zens.ink
license: MIT
compatibility: >-
  Python 3.10+ (stdlib only, zero pip dependencies). Optional API keys:
  BING_API_KEY (keyword volume), BRAVE_API_KEY (alternative volume),
  SERPER_API_KEY (SERP data for KD scoring), Google ADC credentials (search performance).
  Tools without keys auto-skip gracefully.
runtime:
  language: python
  entry_point: zens-ink
allowed-tools: shell file_read file_write
triggers:
  - seo keyword research
  - find long tail keywords
  - keyword difficulty check
  - can i rank for this keyword
  - keyword clustering
  - search intent analysis
  - content opportunity matrix
  - competitor content gap
  - seo site audit
  - check broken links
  - find orphan pages
  - on-page seo audit
  - google search console data
  - search ranking performance
  - website seo check
  - technical seo audit
  - kgr keyword golden ratio
---

# ZensInk — Free SEO Toolkit for Indie Builders

## Setup (one-time)

```bash
pip install zens-ink
```

After install, `zens-ink` command is available globally. Verify:
```bash
zens-ink --help
```

All 13 tools can also be run as Python modules:
```bash
python3 -m zens_ink.keyword_research "tarot meaning"
```

## The 16 Tools (site_audit now includes agent-readiness checks)

### Keyword Discovery

#### 1. keyword_research — Discover Keywords (FREE, no API key)

Mines Google Autocomplete for long-tail keyword variations.

```bash
zens-ink keyword_research "tarot meaning"
zens-ink keyword_research "tarot meaning" --expand    # a-z deep discovery
zens-ink keyword_research "塔罗牌" --lang zh            # Chinese keywords
zens-ink keyword_research "tarot meaning" --json        # JSON output
```

#### 2. keyword_cluster — Semantic Grouping (FREE, no API key)

Groups raw keyword lists into topic clusters based on word overlap similarity.

```bash
echo "tarot reading\ntarot cards\nfree tarot" | zens-ink keyword_cluster --stdin
zens-ink keyword_cluster -f keywords.txt --threshold 0.2
zens-ink keyword_cluster -f keywords.txt --csv output.csv
```

### Difficulty & Opportunity

#### 3. kd — Keyword Difficulty (needs SERPER_API_KEY, free 2500/mo)

SERP structure analysis — no expensive Ahrefs DR data needed. Outputs GO / CAUTION / WAIT / AVOID.

```bash
zens-ink kd "tarot reading"
zens-ink kd "bazi calculator" --lang zh
```

#### 4. kgr_auto — KGR Opportunity Scoring (FREE scoring, optional Bing key for volume)

Automated keyword opportunity scoring using the Keyword Golden Ratio methodology.

```bash
zens-ink kgr_auto "tarot" "tarot reading" "free tarot"
zens-ink kgr_auto -f keywords.txt
```

### Search Volume

#### 5. keyword_volume — Search Volume (needs BING_API_KEY, free)

Real monthly search volume from Bing Webmaster API.

```bash
zens-ink keyword_volume "tarot meaning" --lang en
```

#### 6. brave_volume — Alternative Volume (needs BRAVE_API_KEY, free 2000/mo)

Supplements Bing volume data. Especially useful when Bing returns 0 for Chinese keywords.

```bash
zens-ink brave_volume "tarot reading" --count 5
```

### Intent & Content Strategy

#### 7. search_intent — Intent Classification (FREE, no API key)

Classifies each keyword as informational / commercial / transactional / navigational, with question/buyer/problem flags.

```bash
zens-ink search_intent "buy tarot cards" "what is tarot" "best tarot deck"
zens-ink search_intent -f keywords.txt --json
```

#### 8. content_matrix — Opportunity Matrix (FREE, no API key)

Combines clustering + intent + KGR into a prioritized content matrix: what to write, in what order, and why.

```bash
zens-ink content_matrix -f keywords.txt
zens-ink content_matrix -f keywords.txt --json
```

### Competitive Analysis

#### 9. competitor_gap — Competitor Content Analysis (FREE, no API key)

Compares sitemaps to find topics competitors cover that you don't.

```bash
zens-ink competitor_gap \
  --url https://yoursite.com \
  --compare https://competitor1.com https://competitor2.com
```

### Technical SEO Audit

#### 10. site_audit — Technical Site Audit (FREE, no API key)

Scans built HTML for 30+ issues: orphan pages, broken internal links, canonical/meta/H1 problems, GEO checks (llms.txt, FAQ schema, BLUF), plus agent-readiness checks — llms.txt must carry a when-to-use section and a how-to-call line so AI agents know which jobs your product fits.

```bash
zens-ink site_audit --dist dist --sitemap dist/sitemap.xml
zens-ink site_audit --dist dist --sitemap dist/sitemap.xml --format json
```

#### 11. onpage_audit — On-Page Quality Scoring (FREE, no API key)

7-dimension quality scoring per page: title, meta, headings, images, links, URL, content. 0-100 score with grade and fix suggestions.

```bash
zens-ink onpage_audit --dist dist --sitemap dist/sitemap.xml
zens-ink onpage_audit --dist dist --keywords keywords.txt
```

### Google Search Console

#### 12. setup_gsc — Connect Google Search Console (FREE, one-time)

One-time OAuth setup for Google Search Console.

```bash
zens-ink setup_gsc
```

#### 13. search_performance — Real Ranking Data (FREE, needs setup_gsc)

Pulls actual Google Search Console data: impressions, clicks, CTR, average position.

```bash
zens-ink search_performance
zens-ink search_performance --start 2025-01-01 --end 2025-06-30
zens-ink search_performance --query tarot
```

### Off-Page Authority

#### 14. domain_rating — Real Ahrefs DR (FREE public API, needs AHREFS_API_KEY)

Ahrefs exposes a free Domain Rating endpoint. Check your own site vs the
domains currently ranking on your target SERPs — closes the off-page authority
gap that kd.py's curated proxies could only approximate.

```bash
zens-ink domain_rating example.com
zens-ink domain_rating a.com b.com c.com --json
zens-ink domain_rating --file serp-domains.txt --csv dr.csv
cat serp-domains.txt | zens-ink domain_rating   # stdin pipe
```

Results are cached locally (`dr-cache.json`) so batch reruns never re-query.
Attribution "Domain Rating by Ahrefs" is required by the DR License and kept
in all outputs. Free key: app.ahrefs.com → Account settings → API keys.

#### 15. content_qc — Pre-Publish Content Gate (FREE, no API key)

Grades a DRAFT before it ships — the publishing-side companion to
site_audit/geo scoring. Catches BLUF absence, vague-claim density,
missing FAQ, thin sourcing, and title/description length issues at the
desk, not after Google re-crawls. Works on Markdown (with frontmatter)
and HTML; directory mode averages a whole drafts folder. Exit code 1
below the gate score, so it drops straight into CI or a pre-commit hook.

```bash
zens-ink content_qc draft.md
zens-ink content_qc drafts/ --min-score 75
zens-ink content_qc draft.md --format json
```

Checks: BLUF up front (w=15), fact density per 1k words (15),
vague-word ceiling (10), outbound sources (10), H2 structure (10),
FAQ block (10), internal links (5), question-format headings (5),
lists/tables (5), title and description length (5+5), alt coverage (3),
date signal (2).

#### 16. llms_gen — Generate llms.txt + llms-full.txt (FREE, no API key)

Builds the two-tier AI discovery catalog from your static build or a
remote sitemap: curated `llms.txt` (core pages) plus comprehensive
`llms-full.txt` (every page with title/description, grouped by section).
Skips admin/api/noindex routes automatically. Works with Astro/Next/Hugo
dist directories or any sitemap.xml URL.

```bash
zens-ink llms_gen --dist dist --site https://example.com
zens-ink llms_gen --sitemap https://example.com/sitemap.xml --site https://example.com
zens-ink llms_gen --dist dist --site https://example.com --name "MyBrand" --tagline "What you build"
```


#### 17. ai_crawler_audit — robots.txt AI-Crawler Policy + llms.txt Audit (FREE, no API key)

Answers "who can actually read my content" at the crawler layer: 17 AI
crawlers (training vs AI search, per vendor), Content Signals, sitemap
declaration, and the llms.txt / llms-full.txt discovery layer, plus an
AI-readiness score and plain-language notes. Distinguishes site-wide
blocks from subpath-only blocks (Disallow /admin is not Disallow /).
Pairs with llms_gen: audit what you have, generate what's missing.

```bash
zens-ink ai_crawler_audit https://example.com
zens-ink ai_crawler_audit https://example.com --markdown report.md --json report.json
```


## Typical Workflow

```
keyword_research  →  what should I target?
        ↓
keyword_cluster   →  group into topics
        ↓
search_intent     →  why do people search this?
        ↓
kd / kgr_auto     →  can I win? Is it worth it?
        ↓
keyword_volume    →  how many people search?
        ↓
domain_rating     →  how strong are the ranking domains?
content_matrix    →  what to write first?
        ↓
competitor_gap    →  what am I missing?
        ↓
site_audit        →  is my site technically healthy?
        ↓
onpage_audit      →  is each page optimized?
        ↓
search_performance →  how am I doing?
```

## API Key Setup (Optional)

Create a `.env` file in your project root:

```env
BING_API_KEY=xxx      # Free from bing.com/webmasters
BRAVE_API_KEY=xxx     # Free 2000/mo from brave.com/search/api
SERPER_API_KEY=xxx    # Free 2500/mo from serper.dev
AHREFS_API_KEY=xxx    # Free DR API from app.ahrefs.com
```

Google Search Console: run `zens-ink setup_gsc` and follow the OAuth flow.

## Going Further

**ZensInk Pro** adds automated workflow engines that go beyond individual tools:
Winability Score (personalized KD based on YOUR domain's GSC data), Content Radar
(weekly editorial calendar with angle suggestions), Competitor Radar (pricing/features/
Reddit sentiment), GEO Visibility (does AI mention your brand?), GEO Score (will AI cite
your page? 5-layer 16-dimension scoring), and full 12-step automated audit with HTML
report.

Learn more: https://zens.ink

## Tech Notes

- **Zero dependencies**: Pure Python stdlib. Only `zens-ink` package itself needs installing.
- **Cross-platform**: macOS, Linux, Windows.
- **Privacy-first**: All processing local. No telemetry, no tracking.
- **MCP server**: `python3 -m zens_ink.mcp` (or `zens-ink mcp`) exposes all tools as native model tools via the MCP stdio protocol — works with DSH (@deepseek-ai/dsh-mcp-client), Claude Desktop, Codex. Zero extra dependencies.
- **Tests**: `python3 -m unittest discover tests` — smoke-checks every tool imports, exposes `main()`, and stays stdlib-only.
