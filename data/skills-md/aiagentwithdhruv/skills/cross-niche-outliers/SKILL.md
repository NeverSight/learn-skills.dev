---
name: cross-niche-outliers
description: Find viral YouTube videos from adjacent business niches to extract content patterns and hooks. Use when user asks to find content inspiration, YouTube outliers, viral video patterns, or cross-niche content ideas.
---

# Cross-Niche Outlier Detection

## Goal
Identify high-performing videos from adjacent business niches to extract transferable content patterns, hooks, and structures. These outliers provide inspiration for content ideation without being directly competitive.

## Two Approaches

### 1. TubeLab API (RECOMMENDED)
```bash
# Default: 1 query = 5 credits, ~100 outliers from last 30 days
python3 ./scripts/scrape_cross_niche_tubelab.py

# Custom search term
python3 ./scripts/scrape_cross_niche_tubelab.py --terms "business strategy"

# Skip transcripts (faster, cheaper)
python3 ./scripts/scrape_cross_niche_tubelab.py --skip_transcripts
```

**Pros:** Pre-calculated scores, no rate limiting, fast
**Cons:** 5 credits per query

### 2. yt-dlp Scraping (LEGACY)
```bash
python3 ./scripts/scrape_cross_niche_outliers.py
```
**Use only if TubeLab credits are exhausted.** Often fails due to rate limiting.

## Scripts
- `./scripts/scrape_cross_niche_tubelab.py` - TubeLab API (recommended)
- `./scripts/scrape_cross_niche_outliers.py` - yt-dlp direct scraping
- `./scripts/generate_title_variants.py` - Generate title variants for outliers

## Process

### 1. Video Discovery
- Search keywords (50 videos per keyword)
- Monitor business channels (15 videos per channel)
- Deduplicate and filter noise

### 2. Outlier Scoring
- Base score: video views / channel average views
- Recency boost: <1 day = 2x, <3 days = 1.5x, <7 days = 1.2x
- Threshold: 1.1x or higher (10% above average)

### 3. Cross-Niche Scoring
Modifiers applied to base score:
- -20% per technical term (API, Python, code, SDK)
- +30% for money hooks ($, revenue, income, profit)
- +20% for time hooks (faster, productivity)
- +20% for curiosity gaps (?, "this changed everything")
- +10% for listicles (numbers in title)

### 4. Transcript & Summary
- Fetches transcript (youtube-transcript-api, Apify fallback)
- Claude summarizes: hook, structure, how to adapt
- Raw transcript saved for deeper analysis

### 5. Title Variant Generation
For each outlier, generates 3 title variants adapted to your niche.

### 6. Output to Google Sheet (19 columns)
Cross-Niche Score, Outlier Score, Days Old, Category, Title, Video Link, Views, Duration, Channel, Thumbnail, Summary, Title Variants 1-3, Raw Transcript, Publish Date, Source

## TubeLab Options
| Flag | Description | Default |
|------|-------------|---------|
| `--queries N` | Number of searches (5 credits each) | 1 |
| `--terms "a" "b"` | Custom search terms | entrepreneur |
| `--min_views N` | Minimum views | 10,000 |
| `--max_days N` | Max video age | 30 |
| `--skip_transcripts` | Skip transcripts | False |

## Keyword Tiers

**Tier 1: Adjacent Business/Tech**
- "AI for business", "ChatGPT business use cases", "no-code automation"

**Tier 2: Broad Business**
- "scale your business", "solopreneur success", "founder productivity"

**Tier 3: Money/Revenue Hooks**
- "increase revenue", "passive income systems", "10x your income"

## Monitored Channels
Alex Hormozi, My First Million, Starter Story, Colin and Samir, Ali Abdaal, Think Media, Iman Gadzhi, Pat Flynn, GaryVee, MrBeast, Justin Welsh, Charlie Morgan

## Output
- Google Sheet: "Cross-Niche Outliers v2 - [timestamp]"
- ~100 outliers with 19 columns
- Sorted by publish date (most recent first)
- 3 title variants + raw transcript per outlier

## Environment
```
TUBELAB_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
APIFY_API_TOKEN=your_token (optional fallback)
```

## Workflow
1. Run weekly for ~100 outliers
2. Review by Cross-Niche Score
3. Pick outlier with good thumbnail/title
4. Use title variants as starting points
5. Recreate thumbnail with your face (see recreate-thumbnails skill)

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `terms` | array | No | Custom search terms (default: 'entrepreneur') |
| `queries` | integer | No | Number of TubeLab searches (5 credits each, default: 1) |
| `min_views` | integer | No | Minimum views (default: 10,000) |
| `max_days` | integer | No | Max video age in days (default: 30) |
| `skip_transcripts` | boolean | No | Skip transcript fetching (faster) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Google Sheet with ~100 outliers (19 columns) |

### Credentials
| Name | Source |
|------|--------|
| `TUBELAB_API_KEY` | .env |
| `ANTHROPIC_API_KEY` | .env |
| `APIFY_API_TOKEN` | .env (optional fallback) |

### Composable With
Skills that chain well with this one: `title-variants`, `recreate-thumbnails`

### Cost
5 TubeLab credits per query + Claude API
