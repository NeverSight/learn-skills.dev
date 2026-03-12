---
name: soccer-match-tracker
description: >-
  Dedicated soccer/football match tracker covering Premier League, La Liga, Champions
  League, and MLS with live scores, league standings, fixtures, match events, and team
  squad info across multiple leagues simultaneously.
  Triggers: soccer scores, football scores, live soccer, match tracker, soccer results,
  Premier League, Champions League, soccer stats, La Liga, MLS, football table, fixtures,
  match day.
author: buildkit-ai
repository: https://github.com/buildkit-ai/soccer-match-tracker
license: MIT
---

# Soccer Match Tracker

A dedicated football companion that tracks live scores, standings, fixtures,
and match events across the world's top leagues: Premier League, La Liga,
Champions League, and MLS.

## What It Does

- Displays live scores across multiple leagues simultaneously
- Shows match events as they happen: goals, cards, substitutions
- Provides current league standings / tables
- Lists upcoming fixtures for the next 7 days
- Supports team squad lookup
- Groups output by league for clean multi-league tracking

## Leagues Covered

| League               | Code | Country/Region  | Season Status (Feb 2026)      |
|----------------------|------|-----------------|-------------------------------|
| Premier League       | PL   | England         | Matchday ~26, title race hot  |
| La Liga              | PD   | Spain           | Mid-season                    |
| Champions League     | CL   | Europe (UEFA)   | Knockout rounds underway      |
| MLS                  | MLS  | United States   | Pre-season / early season     |

## Data Sources

| Data Type           | Source            | Update Frequency     |
|---------------------|-------------------|----------------------|
| Live scores         | Real-time feed    | Polling (10-30s)     |
| Match events        | Real-time feed    | As they happen       |
| League standings    | football-data.org | Per matchday         |
| Upcoming fixtures   | football-data.org | Daily                |
| Team squads         | football-data.org | Updated per window   |

## How It Works

1. Connects to a live data feed for real-time match scores and events
2. Fetches league data (standings, fixtures, squads) from football-data.org
3. Merges live and reference data into unified match views
4. Groups matches by league for clean multi-league output
5. Provides both structured JSON and formatted display output

## Requirements

- Python 3.9+
- `requests` library
- A data API key for live match events (see README)
- football-data.org API key (free tier: 10 requests/minute)

## Related Skills
- For injury updates across soccer leagues, also install `injury-report-monitor`
- For pre-match head-to-head analysis, try `matchup-analyzer`
- For betting odds on soccer matches, install `betting-odds-tracker`
