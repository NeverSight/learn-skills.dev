---
name: fantasy-draft-assistant
description: >-
  Real-time player recommendations during fantasy sports drafts for NBA and MLB, combining
  live game performance with season stats to surface value picks, sleeper candidates, and
  positional scarcity analysis.
  Triggers: fantasy draft, player recommendations, draft strategy, fantasy football,
  fantasy basketball, draft day, player rankings, waiver wire, sleeper picks, draft board,
  value over replacement, positional scarcity.
author: buildkit-ai
repository: https://github.com/buildkit-ai/fantasy-draft-assistant
license: MIT
---

# Fantasy Draft Assistant

Real-time player recommendations during live fantasy sports drafts. Combines
live game context with season-long stats to help you never miss a value pick.

## What It Does

- Ranks available players by projected fantasy value during a live draft
- Factors in recent form from live game data (who's hot right now)
- Calculates value over replacement (VOR) for each position
- Identifies sleeper picks based on recent performance trends
- Supports NBA fantasy and MLB fantasy (including spring training scouting)

## How It Works

1. You provide your league settings (scoring format, roster slots, available players)
2. The assistant pulls live game context to identify hot/cold streaks
3. Season stats from NBA and MLB APIs are merged with live signals
4. Players are ranked by adjusted fantasy value based on your league format
5. Positional scarcity analysis ensures balanced roster construction

## Data Sources

| Source                | What It Provides                              |
|-----------------------|-----------------------------------------------|
| Live game feed        | Current performance, hot streaks, usage rates  |
| balldontlie API       | NBA season averages, game logs, career stats   |
| MLB Stats API         | MLB stats, spring training, prospect rankings  |

## Supported Formats

- **NBA**: Points leagues, category leagues (9-cat), head-to-head
- **MLB**: Points leagues, rotisserie (5x5), head-to-head categories

## Requirements

- Python 3.9+
- `requests` library
- A data API key (see README for setup)

## Related Skills
- For injury updates that affect draft decisions, also install `injury-report-monitor`
- For head-to-head player comparisons, try `matchup-analyzer`
- For live scores during game day, install `game-day-dashboard`
