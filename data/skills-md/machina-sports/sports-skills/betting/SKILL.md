---
name: betting
description: |
  Betting analysis — odds conversion, de-vigging, edge detection, Kelly criterion, arbitrage detection, parlay analysis, and line movement. Pure computation, no API calls. Works with odds from any source: ESPN (American odds), Polymarket (decimal probabilities), Kalshi (integer probabilities).

  Use when: user asks about bet sizing, expected value, edge analysis, Kelly criterion, arbitrage, parlays, line movement, odds conversion, or comparing odds across sources. Also use when you have odds from ESPN and a prediction market price and want to evaluate whether a bet has positive expected value.
  Don't use when: user asks for live odds or market data — use polymarket, kalshi, or the sport-specific skill to fetch odds first, then use this skill to analyze them.
license: MIT
metadata:
  author: machina-sports
  version: "0.2.0"
---

# Betting Analysis

## Quick Start

```bash
sports-skills betting convert_odds --odds=-150 --from_format=american
sports-skills betting devig --odds=-150,+130 --format=american
sports-skills betting find_edge --fair_prob=0.58 --market_prob=0.52
sports-skills betting evaluate_bet --book_odds=-150,+130 --market_prob=0.52
sports-skills betting find_arbitrage --market_probs=0.48,0.49
sports-skills betting parlay_analysis --legs=0.58,0.62,0.55 --parlay_odds=600
sports-skills betting line_movement --open_odds=-140 --close_odds=-160
```

Python SDK:
```python
from sports_skills import betting

betting.convert_odds(odds=-150, from_format="american")
betting.devig(odds="-150,+130", format="american")
betting.find_edge(fair_prob=0.58, market_prob=0.52)
betting.find_arbitrage(market_probs="0.48,0.49")
betting.parlay_analysis(legs="0.58,0.62,0.55", parlay_odds=600)
betting.line_movement(open_odds=-140, close_odds=-160)
```

## Odds Formats

| Format | Example | Description |
|---|---|---|
| American | `-150`, `+130` | US sportsbook standard. Negative = favorite, positive = underdog |
| Decimal | `1.67`, `2.30` | European standard. Payout per $1 (includes stake) |
| Probability | `0.60`, `0.43` | Direct implied probability (0-1). Polymarket uses this format |

**Conversion rules:**
- American negative: prob = -odds / (-odds + 100). Example: -150 → 150/250 = 0.600
- American positive: prob = 100 / (odds + 100). Example: +130 → 100/230 = 0.435
- Decimal: prob = 1 / odds. Example: 1.67 → 0.599
- Kalshi prices (0-100 integer): divide by 100 to get probability format

## Commands

| Command | Required | Optional | Description |
|---|---|---|---|
| `convert_odds` | odds, from_format | | Convert between American, decimal, probability |
| `devig` | odds | format | Remove vig from sportsbook odds → fair probabilities |
| `find_edge` | fair_prob, market_prob | | Compute edge, EV, and Kelly from two probabilities |
| `kelly_criterion` | fair_prob, market_prob | | Kelly fraction for optimal bet sizing |
| `evaluate_bet` | book_odds, market_prob | book_format, outcome | Full pipeline: devig → edge → Kelly |
| `find_arbitrage` | market_probs | labels | Detect arbitrage across outcomes from multiple sources |
| `parlay_analysis` | legs, parlay_odds | odds_format, correlation | Multi-leg parlay EV and Kelly analysis |
| `line_movement` | | open_odds, close_odds, open_line, close_line, market_type | Analyze open-to-close line movement |

## Workflows

### Workflow: Compare ESPN vs Polymarket/Kalshi

This is the primary workflow. The agent already has odds from ESPN and a prediction market — no user estimation needed.

1. Get ESPN moneyline odds for a game (e.g., from `nba get_scoreboard`):
   - Home: `-150`, Away: `+130`
2. Get Polymarket/Kalshi price for the same outcome (e.g., home team at `0.52`).
3. De-vig the ESPN odds to get fair probabilities:
   `devig --odds=-150,+130 --format=american`
   → Fair: Home 57.9%, Away 42.1% (removed ~3.5% vig)
4. Compare fair prob to market price:
   `find_edge --fair_prob=0.579 --market_prob=0.52`
   → Edge: 5.9%, EV: 11.3%, Kelly: 0.123
5. Or do it all in one step:
   `evaluate_bet --book_odds=-150,+130 --market_prob=0.52`

### Workflow: Arbitrage Detection

Spot guaranteed-profit opportunities when prices across sources don't sum to 100%.

1. Get the best available price per outcome from different sources:
   - Source A (Polymarket): Home team at 0.48
   - Source B (Kalshi): Away team at 0.49
2. `find_arbitrage --market_probs=0.48,0.49 --labels=home,away`
   → Total implied: 0.97 (< 1.0 = arbitrage!)
   → Guaranteed ROI: 3.09%
   → Allocation: 49.5% on home, 50.5% on away
3. For 3-way soccer markets: `find_arbitrage --market_probs=0.40,0.25,0.30 --labels=home,draw,away`

### Workflow: Parlay Evaluation

Evaluate multi-leg parlays to see if the offered odds are +EV.

1. De-vig each leg to get fair probabilities:
   - Leg 1: `devig --odds=-150,+130` → fair prob 0.58
   - Leg 2: `devig --odds=-130,+110` → fair prob 0.55
   - Leg 3: `devig --odds=-110,-110` → fair prob 0.50
2. `parlay_analysis --legs=0.58,0.55,0.50 --parlay_odds=600`
   → Combined fair: 15.95%, offered +600 implies 14.29%
   → Edge: 1.66%, +EV
3. If legs are correlated (e.g. same-game parlay): add `--correlation=0.1` — this increases combined probability since correlated events are more likely to co-occur

### Workflow: Line Movement from ESPN

Quantify how a line has moved and what it implies about sharp money.

1. Get ESPN odds for a game — both open and close lines are available:
   - Open moneyline: -140, Close moneyline: -160
   - Open spread: -6.5, Close spread: -7.5
2. `line_movement --open_odds=-140 --close_odds=-160`
   → Probability shift: +3.21% toward favorite
   → Classification: sharp_action
3. With spread too: `line_movement --open_odds=-140 --close_odds=-160 --open_line=-6.5 --close_line=-7.5`
   → If ML and spread move same direction: sharp action confirmed
   → If they move opposite: reverse line movement (public vs sharp split)

### Workflow: De-Vig Sportsbook Odds

Strip the vig/juice from DraftKings odds to see the "true" implied probabilities.

1. `devig --odds=-110,-110 --format=american`
   → Each side is 50.0% fair (standard -110/-110 spread/total)
2. `devig --odds=-200,+170 --format=american`
   → Favorite: 65.2%, Underdog: 34.8%
3. `devig --odds=-150,+300,+400 --format=american` (3-way soccer)
   → Home: 47.3%, Draw: 19.8%, Away: 15.7%

### Workflow: Odds Conversion

Convert odds from one format to another.

1. `convert_odds --odds=-150 --from_format=american`
   → Probability: 60.0%, Decimal: 1.6667
2. `convert_odds --odds=2.50 --from_format=decimal`
   → Probability: 40.0%, American: +150

## Examples

User: "Is there edge on the Lakers game? ESPN has them at -150 and Polymarket has them at 52 cents"
1. `devig --odds=-150,+130 --format=american` → Fair home prob ~58%
2. `find_edge --fair_prob=0.58 --market_prob=0.52` → Edge ~6%, positive EV
3. `kelly_criterion --fair_prob=0.58 --market_prob=0.52` → Kelly fraction
4. Present: edge, EV per dollar, recommended bet size as % of bankroll

User: "Can I arb this? Polymarket has home at 48 cents and Kalshi has away at 49 cents"
1. `find_arbitrage --market_probs=0.48,0.49 --labels=home,away`
2. If arbitrage_found: present allocation percentages and guaranteed ROI
3. If not: present the overround and explain there's no guaranteed profit

User: "Is this 3-leg parlay at +600 worth it?"
1. De-vig each leg to get fair probs (e.g. 0.58, 0.62, 0.55)
2. `parlay_analysis --legs=0.58,0.62,0.55 --parlay_odds=600`
3. Present: combined fair prob, edge, EV, +EV or -EV, Kelly fraction

User: "The line moved from -140 to -160, what does that mean?"
1. `line_movement --open_odds=-140 --close_odds=-160`
2. Present: probability shift, direction, magnitude, classification (sharp action, steam move, etc.)

User: "What are the true odds for this spread? Both sides are -110"
1. `devig --odds=-110,-110 --format=american`
2. Present: each side is 50% fair probability, vig is ~4.5%

User: "Convert -200 to implied probability"
1. `convert_odds --odds=-200 --from_format=american`
2. Present: 66.7% implied probability, 1.50 decimal odds

## Key Concepts

- **Vig/Juice**: The sportsbook's margin. A -110/-110 line implies 52.4% + 52.4% = 104.8% total, meaning 4.8% overround. De-vigging removes this to get fair probabilities.
- **Edge**: The difference between your estimated true probability and the market price. Positive edge = profitable in expectation.
- **Kelly Criterion**: Optimal bet sizing that maximizes long-term growth. f* = (fair_prob - market_prob) / (1 - market_prob). For conservative sizing, multiply the Kelly fraction by 0.5 (half-Kelly) or 0.25 (quarter-Kelly).
- **Expected Value (EV)**: Average return per dollar bet. EV = fair_prob / market_prob - 1.
- **Arbitrage**: When prices across sources don't sum to 100%, you can bet all outcomes and guarantee profit regardless of the result.
- **Parlay**: A multi-leg bet where all legs must win. Combined probability = product of individual leg probabilities. Higher risk, higher reward. Check if the offered odds exceed the fair combined odds.
- **Line Movement**: How odds change between open and close. Large moves toward one side suggest sharp/professional money. Reverse line movement (moneyline and spread moving opposite directions) suggests a public vs sharp split.
