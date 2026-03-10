---
name: google-trends
description: |
  Use this skill when the user wants to fetch, search, or analyze Google Trends data for any country or category.
  Triggers when users say "what's trending in [country]", "popular [topic] in [country]", "Google Trends for [country]",
  or invoke /google-trends. Fetches real-time trending data using trendspyg for 125+ countries and 20 categories.
---

# Google Trends Skill

Fetch real-time trending searches from Google Trends for any country and category.

## When to Use This Skill

Trigger when the user:
- Asks "what's trending in [country]?"
- Asks "popular [games/AI/tech/sports/etc.] in [country]"
- Says "Google Trends for [country]"
- Wants to compare trends between countries
- Invokes `/google-trends`

## Parameters

| Flag | Default | Options |
|------|---------|---------|
| `--geo` | US | Any 2-letter country code: `US`, `BR`, `ID`, `GB`, `JP`, `IN`, `DE`, `FR`, `AU`, `MX`, ... |
| `--category` | all | `all`, `games`, `technology`, `sports`, `entertainment`, `business`, `health`, `science`, `food`, `travel`, `beauty`, `politics`, `shopping` |
| `--hours` | 24 | `4`, `24`, `48`, `168` (7 days) |
| `--top` | 20 | Any integer |
| `--method` | auto | `rss` (fast, no category filter), `csv` (Selenium, supports categories) |

**Auto method logic:** Uses `rss` when `--category all`, uses `csv` when a specific category is given.

## Country Code Reference

| Country | Code | Country | Code |
|---------|------|---------|------|
| Brazil | `BR` | Indonesia | `ID` |
| USA | `US` | India | `IN` |
| UK | `GB` | Japan | `JP` |
| Germany | `DE` | France | `FR` |
| Australia | `AU` | Mexico | `MX` |
| Canada | `CA` | South Korea | `KR` |
| Argentina | `AR` | Nigeria | `NG` |
| Philippines | `PH` | Thailand | `TH` |

## Script Execution

**CRITICAL**: Always use the `run.py` wrapper. It handles venv setup automatically.

### Basic Usage (general trends, fast)
```bash
python scripts/run.py --geo BR
```

### Category-specific trends (uses Selenium)
```bash
python scripts/run.py --geo BR --category games
python scripts/run.py --geo ID --category technology
python scripts/run.py --geo US --category sports --hours 48
```

### Multiple countries (run in parallel)
```bash
python scripts/run.py --geo BR --category games &
python scripts/run.py --geo ID --category games &
wait
```

### Top N results with longer period
```bash
python scripts/run.py --geo JP --category entertainment --hours 168 --top 30
```

## Workflow

1. **Parse user intent** → extract country, category, time period
2. **Map to parameters:**
   - "Brazil" → `--geo BR`
   - "Indonesia" → `--geo ID`
   - "games" → `--category games`
   - "AI/tech/technology" → `--category technology`
   - "past week" / "7 days" → `--hours 168`
3. **Inform user:** "Fetching [category] trends for [country] (past [N] hours)..."
4. **Run script** and parse JSON output
5. **Present results** as a formatted table with rank, trend name, and search volume

## Output Format

Script outputs JSON:
```json
{
  "geo": "BR",
  "category": "games",
  "hours": 24,
  "method": "csv",
  "count": 20,
  "trends": [
    {"rank": 1, "trend": "grêmio x internacional", "volume": "500K+", "started": "..."},
    {"rank": 2, "trend": "arsenal x chelsea", "volume": "500K+", "started": "..."}
  ]
}
```

## Presenting Results

Format output as a clean markdown table:

```
## 🔥 Trending in Brazil — Games (past 24h)

| # | Trend | Volume |
|---|-------|--------|
| 1 | grêmio x internacional | 500K+ |
| 2 | arsenal x chelsea | 500K+ |
...
```

Add brief context/insights after the table when relevant (e.g., "Football dominates Brazil's trending games — the Grenal derby between Grêmio and Internacional was the biggest search spike.").

## Error Handling

| Error | Action |
|-------|--------|
| `BrowserError` / timeout | Retry with `--method rss` (drops category filter) |
| `InvalidParameterError` | Check geo code or category name |
| venv setup failure | Check Python 3.8+ is available |
| No trends returned | Try broader category or different time window |

## Troubleshooting

- **CSS method slow**: normal — Selenium launches Chrome headlessly
- **Category filter not working with RSS**: RSS doesn't support categories, use `--method csv`
- **Empty results**: try `--hours 168` for a wider time window
- **Country not found**: run `python scripts/run.py --list-countries` to see all supported codes
