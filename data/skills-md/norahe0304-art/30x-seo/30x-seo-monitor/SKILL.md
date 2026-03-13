---
name: 30x-seo-monitor
description: >
  Monitor your own website's SEO performance using Google Search Console data.
  Track keyword rankings, clicks, impressions, CTR, and position changes over time.
  Identify top performing pages, declining keywords, and new ranking opportunities.
  Use when user says "monitor my site", "my rankings", "GSC data", "Search Console",
  "my keywords", "position changes", "CTR", "impressions", or "clicks".
allowed-tools:
  - Bash
  - Read
---

# SEO Monitor (Google Search Console)

Monitor your own website's SEO performance using Google Search Console API.

[PROTOCOL]: Update this header on changes, then check CLAUDE.md

## Prerequisites

Requires `gws` CLI with Google Search Console access, or GSC MCP server.

### Option 1: gws CLI

```bash
gws auth status
gws auth login  # if needed
```

### Option 2: GSC MCP Server

Configure in `~/.config/claude/mcp.json`:

```json
{
  "mcpServers": {
    "google-search-console": {
      "command": "npx",
      "args": ["-y", "mcp-server-gsc"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    }
  }
}
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/30x-seo monitor overview` | Dashboard: top queries, pages, CTR, position |
| `/30x-seo monitor keywords` | All ranking keywords with metrics |
| `/30x-seo monitor pages` | Top performing pages |
| `/30x-seo monitor changes` | Position changes (gains/losses) |
| `/30x-seo monitor opportunities` | High impression, low CTR keywords |

---

## Metrics Explained

| Metric | What it means |
|--------|---------------|
| **Clicks** | Users clicked your result |
| **Impressions** | Your result appeared in search |
| **CTR** | Click-through rate (clicks / impressions) |
| **Position** | Average ranking position (1 = top) |

---

## Analysis Workflows

### 1. Weekly Performance Check

```
/30x-seo monitor overview
```

Output:
- Total clicks, impressions, CTR, avg position (7 days)
- Top 10 queries by clicks
- Top 10 pages by clicks
- Week-over-week comparison

### 2. Keyword Ranking Report

```
/30x-seo monitor keywords
```

Output:
- All ranking keywords
- Position, clicks, impressions, CTR per keyword
- Sort by: position, clicks, impressions, or CTR

### 3. Position Change Detection

```
/30x-seo monitor changes
```

Output:
- Keywords that gained positions (rising)
- Keywords that lost positions (declining)
- New keywords (just started ranking)
- Lost keywords (dropped out of top 100)

### 4. Quick Win Opportunities

```
/30x-seo monitor opportunities
```

Find keywords with:
- High impressions (>1000/month)
- Low CTR (<3%)
- Position 4-20 (page 1-2)

These are "quick wins" - improve title/description to boost CTR.

---

## Date Ranges

Default: last 7 days

Specify custom range:
```
/30x-seo monitor overview --days 30
/30x-seo monitor keywords --days 90
```

---

## Output Format

Reports include:
1. **Summary table** — Key metrics at a glance
2. **Detailed data** — Full keyword/page lists
3. **Action items** — Specific recommendations

---

## Integration with Other Skills

| Scenario | Next Step |
|----------|-----------|
| Found declining keyword | → `30x-seo-content-decay` to analyze page |
| Low CTR on page 1 | → `30x-seo-page` to optimize title/meta |
| Keyword cannibalization suspected | → `30x-seo-cannibalization` to check |
| New keyword opportunity | → `30x-seo-content-brief` to plan content |

---

## Limitations

- **Only your verified sites** — GSC only shows data for sites you own
- **Data delay** — GSC data is 2-3 days behind
- **90 day max** — Historical data limited to ~16 months, but API typically 90 days
- **Sampled data** — High-traffic sites may show sampled data
