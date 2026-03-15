---
name: matchup-analyzer
description: >-
  Head-to-head team and player comparison with statistical breakdowns, trend analysis,
  and structured matchup reports for NBA, MLB, and Soccer covering strengths, weaknesses,
  and historical context.
  Triggers: matchup analysis, head-to-head, team comparison, player comparison, sports
  analytics, stat comparison, pregame analysis, game preview, matchup trends, who will win,
  team strengths.
author: buildkit-ai
repository: https://github.com/buildkit-ai/matchup-analyzer
license: MIT
---

# Matchup Analyzer

Data-driven matchup breakdowns for NBA, MLB, and Soccer. Compares teams
and players head-to-head with stats, trends, and key factors.

## What It Does

- Produces structured matchup reports for any two teams or players
- Pulls stats from multiple sources for comprehensive analysis
- Identifies strengths, weaknesses, and key matchup factors
- Shows historical head-to-head records where available
- Highlights trending players and situational advantages
- Outputs clean markdown matchup cards

## How It Works

1. You provide two teams (or players) and the sport
2. The analyzer pulls today's schedule and live context for game-day matchups
3. Team and player stats are fetched from sport-specific APIs
4. Stats are compared across key categories with advantage indicators
5. A structured matchup card is generated with insights and edge factors

## Data Sources

| Source              | Sport  | What It Provides                          |
|---------------------|--------|-------------------------------------------|
| Live game feed      | All    | Today's schedule, live game context       |
| balldontlie API     | NBA    | Team stats, player stats, game logs       |
| MLB Stats API       | MLB    | Pitcher/batter matchups, team stats       |
| football-data.org   | Soccer | League standings, head-to-head records    |

## Supported Analysis Types

| Type             | Description                                    |
|------------------|------------------------------------------------|
| Team vs Team     | Full team stat comparison with key players     |
| Player vs Player | Direct stat comparison between two players     |
| Game Preview      | Pre-game breakdown for today's scheduled games |
| Trend Report      | Recent form analysis for a team or player      |

## Requirements

- Python 3.9+
- `requests` library
- A data API key (see README for setup)
- football-data.org API key for soccer data (free tier available)

## Related Skills
- For injury context in matchup analysis, also install `injury-report-monitor`
- For betting odds alongside matchup previews, try `betting-odds-tracker`
- For live game tracking after kickoff, install `game-day-dashboard`
