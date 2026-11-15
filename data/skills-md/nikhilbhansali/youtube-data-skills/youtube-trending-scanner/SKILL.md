---
name: youtube-trending-scanner
description: "Scan what's trending right now in any YouTube niche using YouTube Data API v3. Find velocity outliers, rising channels, breakout videos, and emerging topics. Use when users want to (1) See what's trending in their niche right now, (2) Find breakout videos getting disproportionate views, (3) Discover rising channels with unusual traction, (4) Catch trends before they peak, (5) Find outdated content to remake, (6) Identify first-mover opportunities. Requires user's YouTube Data API v3 key."
---

# YouTube Trending Scanner

Scan what's trending right now in any YouTube niche -- find breakout videos, rising channels, and emerging topics.

## Usage

```
/youtube-trending-scanner "meditation"
/youtube-trending-scanner "AI tools" --days 14
/youtube-trending-scanner "home cooking" --days 30
```

## Instructions

### Step 1: Parse Arguments

- **Niche/keyword** (required): the niche to scan
- **--days N** (optional): time window to scan (default: 14, max: 30)

### Step 2: Get the API Key

Check Claude memory for a YouTube Data API v3 key. If not found, ask:
> "I need a YouTube Data API v3 key. You can get one from the Google Cloud Console. Please paste your key."

### Step 3: Run the Bundled Script

Run `scripts/scan_trending.py` — resolve the path relative to this skill's own directory:

```bash
YT_API_KEY=API_KEY python3 <skill-dir>/scripts/scan_trending.py "NICHE" [--days N]
```

Dependency: `pip3 install google-api-python-client`.

The script searches the window three ways (relevance, viewCount, date), pulls a
90-day baseline for comparison, then computes velocity outliers, rising channels,
trending words/bigrams, format distribution, and publishing-rate change.

### Step 4: Read the Data

```
reports/data/trending-scan-<niche-slug>-<YYYY-MM-DD>.json
```

### Step 5: Write the Report

Write to the path the script printed:

```
reports/trending-scan-<niche-slug>-<YYYY-MM-DD>.md
```

```markdown
# Trending Scanner: [Niche]
*Scanned [date] | Last [N] days | [N] videos analyzed*

## Hot Right Now
Overall trend assessment: Is this niche heating up, stable, or cooling down?
Compare recent publishing rate vs baseline.

## Breakout Videos (Velocity Outliers)
| # | Title | Views | Velocity (views/day) | Channel | Channel Size | Age |
|---|-------|-------|---------------------|---------|--------------|-----|
These videos are getting disproportionate views. What do they have in common?

## Trending Topics
Words and phrases appearing frequently in recent high-performing content.
Topic clusters and emerging themes.

## Rising Channels
Small channels getting unusual traction right now.
| Channel | Subs | Recent Videos | Recent Views | Avg View/Sub Ratio |
|---------|------|---------------|--------------|-------------------|

## Format Trends
What formats are being used? Which are performing best?
Shorts vs long-form breakdown.

## Content Velocity
- Current niche publishing rate vs baseline
- Is competition increasing or decreasing?
- Saturation signals

## Timely Content Recommendations
3-5 specific video ideas based on current trends:
- What to make THIS WEEK
- Why (data backing)
- Format and angle recommendation

## Trend Assessment
- Growing / Stable / Declining
- First-mover opportunities
- Risks and considerations

## Quota Usage
| Operation | Calls | Units |
|-----------|-------|-------|
Use the `quota_used.breakdown` block from the JSON.
```

### Step 6: Report Completion

Tell the user the report path, the trend assessment, the top breakout video,
the number of rising channels found, and the quota consumed.

## Quota Estimate

Trend detection depends on time-windowed keyword search, so `search.list` stays.

| Operation | Calls | Units |
|-----------|-------|-------|
| `search.list` (relevance, viewCount, date, 90-day baseline) | 4 | 400 |
| `videos.list` (batches of 50) | ~4 | ~4 |
| `channels.list` (batches of 50) | ~3 | ~3 |
| **Total** | | **~407** |

Daily default allowance is 10,000 units, resetting at midnight Pacific Time.
