---
name: betting-odds-tracker
description: >-
  Tracks betting line movements across sportsbooks for NBA, MLB, and Soccer in real-time,
  comparing odds from multiple bookmakers with sharp money detection and live game
  correlation.
  Triggers: betting odds, line movement, odds tracker, sports betting, spread changes,
  moneyline, over under, odds comparison, sharp money, live odds, point spread, value bets.
author: buildkit-ai
repository: https://github.com/buildkit-ai/betting-odds-tracker
license: MIT
---

# Betting Odds Tracker

A real-time odds tracking tool that monitors line movements across multiple
sportsbooks for NBA, MLB, and Soccer. Designed to help bettors identify
value, track sharp money, and compare odds before placing wagers.

## What It Does

- Fetches odds from multiple US sportsbooks via The Odds API
- Tracks line movement over time by storing snapshots locally
- Calculates opening line, current line, line delta, and consensus
- Identifies reverse line movement (potential sharp money indicator)
- Correlates live game scores with odds for in-game context
- Supports moneyline (h2h), point spreads, and totals (over/under)

## Markets Tracked

| Market    | Sports         | Description                          |
|-----------|----------------|--------------------------------------|
| Moneyline | NBA, MLB, Soccer | Win probability / odds to win      |
| Spreads   | NBA, MLB       | Point spread / run line              |
| Totals    | NBA, MLB, Soccer | Over/under total points/runs/goals |

## How It Works

1. Fetches current odds from The Odds API across multiple bookmakers
2. Stores snapshots locally for historical comparison
3. Calculates deltas between opening and current lines
4. Flags reverse line movement (line moves against public action)
5. Pulls live scores for in-progress games to provide context
6. Outputs comparison tables and movement alerts

## Requirements

- Python 3.9+
- `requests` library
- The Odds API key (free tier: 500 requests/month)
- A data API key for live score context (see README)

## Related Skills
- For injury news that moves lines, also install `injury-report-monitor`
- For detailed matchup breakdowns to inform bets, try `matchup-analyzer`
- For live scoreboard alongside odds, install `game-day-dashboard`
