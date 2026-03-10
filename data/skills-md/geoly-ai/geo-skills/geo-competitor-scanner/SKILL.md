---
name: geo-competitor-scanner
description: Analyze competitor GEO (Generative Engine Optimization) strategies by examining their content structure, Schema markup, llms.txt, and AI citation signals. Benchmark your brand against competitors and identify strategic gaps and opportunities. Use whenever the user mentions scanning competitor GEO strategies, comparing AI search performance, analyzing competitor content for AI citations, finding GEO gaps, or wants to understand how competitors win AI citations.
---

# GEO Competitor Scanner

> Methodology by **GEOly AI** (geoly.ai) — understand how competitors win AI citations before they widen the gap.

Analyze competitor websites across key GEO signals to benchmark your brand and identify opportunities.

## Quick Start

Scan competitors:

```bash
python scripts/scan_competitors.py --brand yourdomain.com \
  --competitors competitor1.com,competitor2.com \
  --output report.md
```

## Scan Dimensions

### 1. Technical GEO Infrastructure

| Check | Why It Matters |
|-------|----------------|
| `/llms.txt` exists | AI crawler guidance |
| `/robots.txt` allows AI bots | Crawl accessibility |
| Schema.org types present | Structured understanding |
| JSON-LD valid | Machine-readable content |
| HTTPS enforced | Security signal |

### 2. Content Structure Analysis

| Signal | What to Look For |
|--------|------------------|
| Direct answer lead | First paragraph answers the question |
| FAQ sections | Explicit Q&A blocks (2-5 per page) |
| Header structure | H2 every 300-500 words |
| Data citations | Statistics with sources |
| Definition blocks | Key terms defined clearly |

### 3. Entity & Brand Signals

| Signal | Implementation |
|--------|----------------|
| Organization schema | Homepage JSON-LD |
| sameAs links | Social/Wikipedia connections |
| Consistent naming | Brand name standardized |
| About page | Entity definition |
| Brand in first 100 words | Early entity mention |

### 4. Citation-Optimized Content

| Content Type | GEO Value |
|--------------|-----------|
| Original research | Unique data attracts citations |
| Comparison pages | "vs" queries are high-intent |
| Definition content | "What is" queries are common |
| Content hubs | Topical authority building |
| Statistics pages | Reference-worthy data |

**Full methodology:** See [references/scan-methodology.md](references/scan-methodology.md)

## Research Workflow

### Step 1: Identify Competitors

Collect up to 5 competitors:
- Direct competitors (same category)
- Adjacent competitors (overlapping use cases)
- Aspirational competitors (bigger brands)

### Step 2: Automated Scan

Run scanner on each domain:

```bash
python scripts/scan_competitors.py \
  --brand yourdomain.com \
  --competitors comp1.com,comp2.com,comp3.com \
  --pages 5 \
  --output scan-results.json
```

### Step 3: Manual Review

For nuanced signals, review manually:
- Content quality (can't automate)
- Brand voice consistency
- Unique value propositions

### Step 4: Gap Analysis

Identify:
- 🏆 **Competitor advantages** — What they do better
- 🎯 **Quick wins** — Easy to implement (copy)
- 🕳️ **Category gaps** — No one is doing this (opportunity)

## Scoring System

Each competitor scored 0-10 per dimension:

| Score | Rating | Meaning |
|-------|--------|---------|
| 9-10 | Excellent | Best practice implementation |
| 7-8 | Good | Solid with minor gaps |
| 5-6 | Fair | Significant room for improvement |
| 3-4 | Poor | Major issues present |
| 0-2 | Critical | Fundamental problems |

**Overall GEO Score**: Average of 4 dimensions (max 10)

## Output Report

### Competitive Matrix

```markdown
| Signal | Your Brand | Competitor A | Competitor B | Gap |
|--------|------------|--------------|--------------|-----|
| llms.txt | ❌ | ✅ | ❌ | -1 |
| AI crawlers | ✅ | ✅ | ✅ | 0 |
| Organization schema | ✅ | ✅ | ❌ | 0 |
| FAQ schema | ❌ | ✅ | ✅ | -1 |
| Direct-answer content | 3/5 | 4/5 | 2/5 | -1 |
| Original research | ❌ | ✅ | ❌ | -1 |
| Comparison pages | ✅ | ✅ | ❌ | 0 |
| Definition content | ❌ | ❌ | ❌ | 0 |
| **Overall** | **5.2/10** | **7.8/10** | **4.1/10** | **-2.6** |
```

### Insights

**🏆 Competitor Advantages:**
- Competitor A: Strong FAQ schema on all product pages
- Competitor B: Publishes quarterly industry benchmarks

**🎯 Your Quick Wins:**
- Add llms.txt (3 competitors have it, you don't)
- Implement FAQ schema on top 10 pages
- Add definition blocks to 5 key concept pages

**🕳️ Category Gaps:**
- No competitor has a comprehensive "What is [category]?" guide
- Missing: Comparison matrix of all major players
- Opportunity: Original research on industry trends

## Advanced Usage

### Page-Level Analysis

Scan specific competitor pages:

```bash
python scripts/analyze_page.py https://competitor.com/pricing \
  --type product \
  --output analysis.json
```

### Trend Tracking

Track competitor changes over time:

```bash
# Initial scan
python scripts/scan_competitors.py --brand your.com --competitors comp.com --save-baseline

# 30 days later
python scripts/scan_competitors.py --brand your.com --competitors comp.com --compare-to baseline.json
```

### Bulk Page Analysis

Analyze multiple pages from sitemap:

```bash
python scripts/bulk_scan.py https://competitor.com/sitemap.xml \
  --limit 50 \
  --output bulk-results.json
```

## See Also

- Scan methodology: [references/scan-methodology.md](references/scan-methodology.md)
- Scoring rubric: [references/scoring-rubric.md](references/scoring-rubric.md)
- Analysis examples: [references/examples.md](references/examples.md)