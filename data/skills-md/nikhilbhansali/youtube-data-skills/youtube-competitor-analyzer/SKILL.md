---
name: youtube-competitor-analyzer
description: "Find and analyze YouTube competitor channels using YouTube Data API v3. Discover competitors through keyword search, category matching, content similarity, and related channel discovery. Compare metrics, content strategies, and market positioning. Use when users want to (1) Find competitors for their YouTube channel, (2) Analyze competitor performance metrics, (3) Compare their channel against competitors, (4) Identify content gaps and opportunities, (5) Benchmark against similar creators, (6) Generate competitive analysis reports. Requires user's YouTube Data API v3 key."
---

# YouTube Competitor Analyzer

Find and analyze competitor channels using YouTube Data API v3.

## Usage

```
/youtube-competitor-analyzer @MyChannel
/youtube-competitor-analyzer @MyChannel --keywords "meditation" "mindfulness"
/youtube-competitor-analyzer --competitors @rivalA @rivalB UCxxxxxxx
/youtube-competitor-analyzer @MyChannel --top 15 --max-queries 4
```

## Instructions

### Step 1: Parse Arguments

- **--channel** (optional): the user's channel for context and ranking
- **--competitors** (optional): specific channels to analyze directly (`@handles`, URLs, or IDs)
- **--keywords** (optional): discovery keywords; defaults to keywords derived from the user's channel
- **--max-queries N** (optional): max discovery searches, 100 units each (default: 3)
- **--top N** (optional): how many competitors to profile in depth (default: 12)

At least one of `--channel` or `--competitors` is required.

### Step 2: Get the API Key

Get a key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
with YouTube Data API v3 enabled. Check Claude memory first; if not found, ask the user to paste it.

### Step 3: Run the Bundled Script

Run `scripts/analyze_competitors.py` — resolve the path relative to this skill's own directory:

```bash
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/analyze_competitors.py --channel "@MyChannel"
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/analyze_competitors.py --competitors "@rivalA" "@rivalB"
```

Dependency: `pip3 install google-api-python-client`.

### Step 4: Read the Data

```
reports/data/competitor-analysis-<slug>-<YYYY-MM-DD>.json
```

### Step 5: Write the Report

Write to the path the script printed: `reports/competitor-analysis-<slug>-<YYYY-MM-DD>.md`

## Competitor Discovery Methods

1. **Keyword search** — `search.list(type=channel)` on terms drawn from the user's
   `brandingSettings.keywords`, channel description, and recent video titles.
2. **Content similarity** — frequent 5+ character words from the user's last 25 video
   titles feed the same discovery queries.
3. **Direct input** — `--competitors` accepts `@handles`, channel IDs, or URLs and
   resolves each for 1 unit. Directly supplied channels are weighted above search hits.
4. **Manual keywords** — `--keywords` overrides the derived terms entirely.

### Niche-Specific Search Terms

Useful starting points for `--keywords`:

```
Spiritual/wellness: meditation, mindfulness, yoga, spiritual, consciousness, wellness, self-help, awakening
Tech:               tech review, unboxing, tutorial, how to, comparison, tips, gadget
Gaming:             gameplay, let's play, walkthrough, gaming, stream, esports
```

## Competitor Ranking

```
sizeSimilarity  = 1 - |log10(compSubs + 1) - log10(targetSubs + 1)| / 10
relevanceScore  = discoveryHits(channel) / maxDiscoveryHits     # normalized 0-1
overallScore    = sizeSimilarity * 0.3 + relevanceScore * 0.7
```

Sorted by `overallScore`; the top N (default 12) get a full recent-content profile.
Without a `--channel` for comparison, `sizeSimilarity` is held neutral at 0.5.

## Comparative Analysis

Per competitor:

| Metric | Description |
|--------|-------------|
| Subscribers | Direct count |
| Total Views | Channel lifetime views |
| Video Count | Total videos published |
| Views/Video | Average performance |
| Views/Sub | Audience efficiency |
| Uploads/Month | videoCount / months since channel creation |
| Channel Age | Days since creation |

Plus a `recent_content` profile per competitor from their last 25 uploads: average
duration, Shorts percentage, average recent views, average days between uploads,
preferred publishing days, top title words, and top tags.

`positioning` compares the user's channel against the competitor averages on every
metric (as a percentage of average) and gives their rank by subscribers.

## Content Gap Analysis

Compare across the `recent_content` profiles:
- Content types and topics they cover that the user does not (top title words / tags)
- Duration preferences and Shorts adoption
- Upload schedules and cadence
- High-performing topics by average recent views

## Output Report Structure

```markdown
# Competitive Analysis Report: [Channel Name]
*Analyzed [date] | [N] competitors from [N] candidates*

## Executive Summary
- Competitors found, key positioning insights

## Competitor Table
| Channel | Subs | Videos | Total Views | Views/Video | Uploads/Mo | Score |
|---------|------|--------|-------------|-------------|------------|-------|

## Competitive Positioning
- User vs competitor averages (use `positioning.vs_average`)
- Rank by subscribers, market position assessment

## Content Strategy Comparison
- What competitors do differently (duration, Shorts %, cadence)
- Common patterns among top performers
- Topic and tag overlap vs whitespace

## Opportunities
- Content gaps to fill
- Underserved niches
- Schedule optimization

## Recommendations
- Strategic actions based on analysis, each tied to a data point

## Quota Usage
| Operation | Calls | Units |
|-----------|-------|-------|
Use the `quota_used.breakdown` block from the JSON.
```

### Step 6: Report Completion

Tell the user the report path, how many competitors were profiled, their market
position in one line, the top opportunity, and the quota consumed.

## Quota Estimate

Channel *discovery* is one of the few places `search.list` is genuinely required;
everything after discovery uses 1-unit endpoints.

| Operation | Calls | Units |
|-----------|-------|-------|
| `channels.list` (resolve user's channel) | 1 | 1 |
| `playlistItems.list` + `videos.list` (user's last 25 videos) | 2 | 2 |
| `search.list` (discovery, 100 each) | 3 | 300 |
| `channels.list` (candidate details, batches of 50) | ~1 | ~1 |
| `playlistItems.list` + `videos.list` (12 competitor profiles) | 24 | 24 |
| **Total (discovery mode)** | | **~328** |

**Direct mode** (`--competitors`, no discovery): ~1 unit to resolve each channel plus
2 units per profile — about **40 units for 12 competitors**.

Lower `--max-queries` to cut 100 units per query removed. Daily default allowance is
10,000 units, resetting at midnight Pacific Time.
