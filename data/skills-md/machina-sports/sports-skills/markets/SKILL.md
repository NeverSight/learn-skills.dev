---
name: markets
description: |
  Markets orchestration — connects ESPN live schedules with Kalshi & Polymarket prediction markets.
  Unified dashboards, odds comparison, entity search, and bet evaluation across platforms.

  Use when: user wants to see prediction market odds alongside ESPN game schedules, compare odds across platforms, search for a team/player on Kalshi or Polymarket, check for arbitrage between ESPN odds and prediction markets, or evaluate a specific game's market value.
  Don't use when: user wants raw prediction market data without ESPN context — use polymarket or kalshi directly. For pure odds math (conversion, de-vigging, Kelly) — use betting. For live scores without market data — use the sport-specific skill.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Markets Orchestration

Bridges ESPN live schedules (NBA, NFL, MLB, NHL, WNBA, CFB, CBB) with Kalshi and Polymarket prediction markets.

## Quick Start

```bash
# Today's games with matching prediction markets
sports-skills markets get_todays_markets --sport=nba

# Search for a team across both exchanges
sports-skills markets search_entity --query="Lakers"

# Compare ESPN odds vs prediction market prices for a game
sports-skills markets compare_odds --sport=nba --event_id=401234567

# Sports-filtered market listing (no political/weather noise)
sports-skills markets get_sport_markets --sport=nfl

# Unified ESPN schedule
sports-skills markets get_sport_schedule --sport=nba

# Normalize a price from any source
sports-skills markets normalize_price --price=0.65 --source=polymarket

# Full evaluation: ESPN odds + market price → devig → edge → Kelly
sports-skills markets evaluate_market --sport=nba --event_id=401234567
```

Python SDK:
```python
from sports_skills import markets

markets.get_todays_markets(sport="nba")
markets.search_entity(query="Lakers")
markets.compare_odds(sport="nba", event_id="401234567")
markets.get_sport_markets(sport="nfl")
markets.get_sport_schedule(sport="nba", date="2025-02-26")
markets.normalize_price(price=0.65, source="polymarket")
markets.evaluate_market(sport="nba", event_id="401234567")
```

## Commands

| Command | Required | Optional | Description |
|---|---|---|---|
| `get_todays_markets` | | sport, date | Fetch ESPN schedule → search both exchanges → unified dashboard |
| `search_entity` | query | sport | Search Kalshi + Polymarket for a team/player/event name |
| `compare_odds` | sport, event_id | | ESPN odds + prediction market prices → normalized side-by-side + arb check |
| `get_sport_markets` | sport | status, limit | Sports-filtered market listing on both platforms |
| `get_sport_schedule` | | sport, date | Unified ESPN schedule across one or all sports |
| `normalize_price` | price, source | | Convert any source format to common {implied_prob, american, decimal} |
| `evaluate_market` | sport, event_id | token_id, kalshi_ticker, outcome | ESPN odds + market price → devig → edge → Kelly |

## Supported Sports

| Sport | Key | Kalshi Series |
|---|---|---|
| NFL | `nfl` | KXNFL |
| NBA | `nba` | KXNBA |
| MLB | `mlb` | KXMLB |
| NHL | `nhl` | KXNHL |
| WNBA | `wnba` | KXWNBA |
| College Football | `cfb` | KXCFB |
| College Basketball | `cbb` | KXCBB |

## Workflows

### Today's NBA Dashboard

Show all NBA games today with matching prediction market odds.

```bash
sports-skills markets get_todays_markets --sport=nba
```

Returns each game with:
- ESPN game info (teams, time, status)
- ESPN DraftKings odds (American format)
- Matching Kalshi markets (scoped to KXNBA series)
- Matching Polymarket markets (text search, sports-filtered)

### Find Arb on a Specific Game

1. Get the ESPN event ID from the schedule:
   `sports-skills markets get_sport_schedule --sport=nba`
2. Compare odds across all sources:
   `sports-skills markets compare_odds --sport=nba --event_id=401234567`
3. If arbitrage is detected, the response includes allocation percentages and guaranteed ROI.

### Compare ESPN vs Polymarket

1. `sports-skills markets compare_odds --sport=nba --event_id=401234567`
2. Response includes ESPN odds normalized to probability + Polymarket prices side-by-side
3. Arbitrage check runs automatically using `betting.find_arbitrage`

### Full Bet Evaluation

1. `sports-skills markets evaluate_market --sport=nba --event_id=401234567`
2. Fetches ESPN odds, searches for matching prediction market price
3. Pipes through `betting.evaluate_bet`: devig → edge → Kelly
4. Returns fair probability, edge percentage, EV, Kelly fraction, and recommendation

### Search for a Team

Find all prediction markets related to a team:

```bash
sports-skills markets search_entity --query="Chiefs" --sport=nfl
```

Returns Kalshi events (scoped to KXNFL) and Polymarket markets matching "Chiefs".

## Price Normalization

Different sources use different formats:

| Source | Format | Example | Meaning |
|---|---|---|---|
| ESPN | American odds | `-150` | Favorite, implied 60% |
| Polymarket | Probability (0-1) | `0.65` | 65% implied probability |
| Kalshi | Integer (0-100) | `65` | 65% implied probability |

`normalize_price` converts any format to a common structure:
```json
{
  "implied_probability": 0.65,
  "american": -185.7,
  "decimal": 1.5385,
  "source": "polymarket"
}
```

## Examples

User: "What NBA games are on today and what are the prediction market odds?"
→ `markets.get_todays_markets(sport="nba")`

User: "Find me Lakers markets on Kalshi and Polymarket"
→ `markets.search_entity(query="Lakers", sport="nba")`

User: "Compare the odds for this Celtics game across ESPN and Polymarket"
→ `markets.compare_odds(sport="nba", event_id="<id>")`

User: "Is there edge on the Chiefs game?"
→ `markets.evaluate_market(sport="nfl", event_id="<id>")`

User: "Show me all NFL prediction markets"
→ `markets.get_sport_markets(sport="nfl")`

User: "Convert a Polymarket price of 65 cents to American odds"
→ `markets.normalize_price(price=0.65, source="polymarket")`

## Partial Results

If one source is unavailable (e.g., Kalshi is down), the module returns what it has with warnings:

```json
{
  "status": true,
  "data": {
    "games": [...],
    "warnings": ["Kalshi search failed: connection timeout"]
  }
}
```

This ensures you always get usable data even when a source is temporarily unavailable.
