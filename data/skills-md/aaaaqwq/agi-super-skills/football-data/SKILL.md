---
name: football-data
description: |
  Football (soccer) data across 13 leagues — standings, schedules, match stats, xG, transfers, player profiles. Zero config, no API keys. Covers Premier League, La Liga, Bundesliga, Serie A, Ligue 1, MLS, Champions League, World Cup, Championship, Eredivisie, Primeira Liga, Serie A Brazil, European Championship.

  Use when: user asks about football/soccer standings, fixtures, match stats, xG, lineups, player values, transfers, injury news, league tables, daily fixtures, or player profiles.
  Don't use when: user asks about American football/NFL (use nfl-data), college football (use cfb-data), NBA (use nba-data), WNBA (use wnba-data), college basketball (use cbb-data), NHL (use nhl-data), MLB (use mlb-data), tennis (use tennis-data), golf (use golf-data), Formula 1 (use fastf1), or betting odds (use polymarket or kalshi). Don't use for live/real-time scores — data updates post-match. Don't use get_season_leaders or get_missing_players for non-Premier League leagues (they return empty). Don't use get_event_xg for leagues outside the top 5 (EPL, La Liga, Bundesliga, Serie A, Ligue 1).
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Football Data

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails (package not found or Python version error), install from GitHub:
```bash
pip install git+https://github.com/machina-sports/sports-skills.git
```
The package requires Python 3.10+. If your default Python is older, use a specific version:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills football get_daily_schedule
sports-skills football get_season_standings --season_id=premier-league-2025
```

Python SDK (alternative):
```python
from sports_skills import football

standings = football.get_season_standings(season_id="premier-league-2025")
schedule = football.get_daily_schedule()
```

## Choosing the Season

Derive the current year from the system prompt's date (e.g., `currentDate: 2026-02-16` → current year is 2026).

- **If the user specifies a season**, use it as-is.
- **If the user says "current", "latest", or doesn't specify**: Call `get_current_season(competition_id="...")` to get the active season_id. Do NOT guess or hardcode the year.
- **Season format**: Always `{league-slug}-{year}` (e.g., `"premier-league-2025"` for the 2025-26 season). The year is the start year of the season, not the end year.
- **MLS exception**: MLS runs spring-fall within a single calendar year. Use `get_current_season(competition_id="mls")` — don't assume MLS follows European calendar.
- **Never hardcode a season_id.** Always derive it via `get_current_season()` or from the system date.

## Data Coverage by League

Not all data is available for every league. Use the right command for the right league.

| Command | All 13 leagues | Top 5 only | PL only |
|---------|:-:|:-:|:-:|
| get_season_standings | x | | |
| get_daily_schedule | x | | |
| get_season_schedule | x | | |
| get_season_teams | x | | |
| search_team | x | | |
| get_team_schedule | x | | |
| get_team_profile | x | | |
| get_event_summary | x | | |
| get_event_lineups | x | | |
| get_event_statistics | x | | |
| get_event_timeline | x | | |
| get_current_season | x | | |
| get_competitions | x | | |
| get_event_xg | | x | |
| get_event_players_statistics (with xG) | | x | |
| get_season_leaders | | | x |
| get_missing_players | | | x |

**Top 5 leagues** (Understat): EPL, La Liga, Bundesliga, Serie A, Ligue 1.
**PL only** (FPL): Premier League — injury news, player stats, ownership, ICT index.
**All leagues**: via ESPN — scores, standings, schedules, match summaries, lineups, team stats.
**Transfermarkt**: Works for any player with a `tm_player_id` — market values and transfer history.

**Note**: MLS uses a different season structure (spring-fall calendar). Use `get_current_season(competition_id="mls")` to detect the right season_id.

## ID Conventions

- **season_id**: `{league-slug}-{year}` e.g. `"premier-league-2025"`, `"la-liga-2025"`
- **competition_id**: league slug e.g. `"premier-league"`, `"serie-a"`, `"champions-league"`
- **team_id**: ESPN team ID (numeric string) e.g. `"359"` (Arsenal), `"86"` (Real Madrid)
- **event_id**: ESPN event ID (numeric string) e.g. `"740847"`
- **fpl_id**: FPL element ID or code (PL players only)
- **tm_player_id**: Transfermarkt player ID e.g. `"433177"` (Saka), `"342229"` (Mbappe)

## Commands

### get_current_season
Detect current season for a competition. Works for all leagues.
- `competition_id` (str, required): Competition slug

Returns `data.competition` and `data.season`:
```json
{"competition": {"id": "premier-league", "name": "Premier League"}, "season": {"id": "premier-league-2025", "name": "2025-26 English Premier League", "year": "2025"}}
```

### get_competitions
List available competitions with current season info. No params. Works for all leagues.

Returns `data.competitions[]` with `id`, `name`, `code`, `current_season`.

### get_competition_seasons
Get available seasons for a competition. Works for all leagues.
- `competition_id` (str, required): Competition slug

### get_season_schedule
Get full season match schedule. Works for all leagues.
- `season_id` (str, required): Season slug (e.g., "premier-league-2025")

Returns `data.schedules[]` — same shape as events below.

### get_season_standings
Get league table for a season. Works for all leagues.
- `season_id` (str, required): Season slug

Returns `data.standings[].entries[]`:
```json
{
  "position": 1,
  "team": {"id": "359", "name": "Arsenal", "short_name": "Arsenal", "abbreviation": "ARS", "crest": "https://..."},
  "played": 26, "won": 17, "drawn": 6, "lost": 3,
  "goals_for": 50, "goals_against": 18, "goal_difference": 32, "points": 57
}
```

### get_season_leaders
Get top scorers/leaders for a season. **Premier League only** (via FPL).
- `season_id` (str, required): Season slug (must be `premier-league-*`)

Returns `data.leaders[]` — note: player name is nested under `.player.name`:
```json
{
  "player": {"id": "223094", "name": "Erling Haaland", "first_name": "Erling", "last_name": "Haaland", "position": "Forward"},
  "team": {"id": "43", "name": "Man City"},
  "goals": 22, "assists": 6, "penalties": 0, "played_matches": 25
}
```
Returns empty for non-PL leagues.

### get_season_teams
Get teams in a season. Works for all leagues.
- `season_id` (str, required): Season slug

### search_team
Search for a team by name across all leagues (or a specific one). Uses fuzzy matching.
- `query` (str, required): Team name to search (e.g., "Corinthians", "Barcelona", "Man Utd")
- `competition_id` (str, optional): Limit search to one league (e.g., "serie-a-brazil", "premier-league")

Returns `data.results[]` with `team`, `competition`, and `season` for each match:
```json
{"team": {"id": "874", "name": "Corinthians"}, "competition": {"id": "serie-a-brazil", "name": "Serie A Brazil"}, "season": {"id": "serie-a-brazil-2025", "year": "2025"}}
```

### get_team_profile
Get basic team info (name, crest, venue). **Does not return squad/roster** — use `get_season_leaders` to find PL player IDs, then `get_player_profile` for individual player data.
- `team_id` (str, required): ESPN team ID
- `league_slug` (str, optional): League hint (faster resolution)

Returns `data.team` and `data.venue`. `data.players[]` is empty — see "Deep dive on a PL team" example below for the recommended workflow.

### get_daily_schedule
Get all matches for a specific date across all leagues.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.

Returns `data.date` and `data.events[]`:
```json
{
  "id": "748381", "status": "not_started", "start_time": "2026-02-16T20:00Z",
  "competition": {"id": "la-liga", "name": "La Liga"},
  "season": {"id": "la-liga-2025", "year": "2025"},
  "venue": {"name": "Estadi Montilivi", "city": "Girona"},
  "competitors": [
    {"team": {"id": "9812", "name": "Girona", "abbreviation": "GIR"}, "qualifier": "home", "score": 0},
    {"team": {"id": "83", "name": "Barcelona", "abbreviation": "BAR"}, "qualifier": "away", "score": 0}
  ],
  "scores": {"home": 0, "away": 0}
}
```
Status values: `"not_started"`, `"live"`, `"halftime"`, `"closed"`, `"postponed"`.

### get_event_summary
Get match summary with scores. Works for all leagues.
- `event_id` (str, required): Match/event ID

Returns `data.event` (same shape as daily schedule events).

### get_event_lineups
Get match lineups. Works for all leagues (when available from ESPN).
- `event_id` (str, required): Match/event ID

Returns `data.lineups[]`:
```json
{
  "team": {"id": "364", "name": "Liverpool", "abbreviation": "LIV"},
  "qualifier": "home",
  "formation": "4-3-3",
  "starting": [{"id": "275599", "name": "Caoimhín Kelleher", "position": "Goalkeeper", "shirt_number": 1}],
  "bench": [{"id": "...", "name": "...", "position": "...", "shirt_number": 62}]
}
```

### get_event_statistics
Get match team statistics. Works for all leagues.
- `event_id` (str, required): Match/event ID

Returns `data.teams[]`:
```json
{
  "team": {"id": "244", "name": "Brentford"},
  "qualifier": "home",
  "statistics": {"ball_possession": "40.8", "shots_total": "10", "shots_on_target": "3", "fouls": "12", "corners": "4"}
}
```

### get_event_timeline
Get match timeline/key events (goals, cards, substitutions). Works for all leagues.
- `event_id` (str, required): Match/event ID

Returns `data.timeline[]` with goal, card, and substitution events.

### get_team_schedule
Get schedule for a specific team — includes both past results and upcoming fixtures. Works for all leagues.
- `team_id` (str, required): ESPN team ID
- `league_slug` (str, optional): League hint (faster resolution)
- `season_year` (str, optional): Season year filter
- `competition_id` (str, optional): Filter results to a single competition (e.g., "serie-a-brazil", "premier-league")

### get_head_to_head
**UNAVAILABLE** — requires licensed data. Do not call this command; it will return empty results. Instead, use `get_team_schedule` for both teams and filter overlapping matches manually.
- `team_id` (str, required): First team ID
- `team_id_2` (str, required): Second team ID

### get_event_xg
Get expected goals (xG) data from Understat. **Top 5 leagues only**: EPL, La Liga, Bundesliga, Serie A, Ligue 1. Returns empty for other leagues.
- `event_id` (str, required): Match/event ID

Returns `data.teams[]` and `data.shots[]`:
```json
{"team": {"id": "244", "name": "Brentford"}, "qualifier": "home", "xg": 1.812}
```
`data.shots[]` contains individual shot data with xG per shot. Note: very recent matches (last 24-48h) may not be indexed on Understat yet.

### get_event_players_statistics
Get player-level match statistics with xG enrichment. Works for all leagues (basic stats from ESPN). xG/xA enrichment only for top 5 leagues (Understat).
- `event_id` (str, required): Match/event ID

Returns `data.teams[].players[]`:
```json
{
  "id": "...", "name": "Bukayo Saka", "position": "Midfielder", "shirt_number": 7, "starter": true,
  "statistics": {"appearances": "1", "shotsTotal": "3", "shotsOnTarget": "1", "foulsCommitted": "1", "xg": "0.45", "xa": "0.12"}
}
```
`xg` and `xa` fields only present for top 5 leagues.

### get_missing_players
Get injured/missing/doubtful players. **Premier League only** (via FPL). Returns empty for other leagues.
- `season_id` (str, required): Season slug (must be `premier-league-*`)

Returns `data.teams[].players[]`:
```json
{
  "id": "463748", "name": "Mikel Merino Zazón", "web_name": "Merino",
  "position": "Midfielder", "status": "injured",
  "news": "Foot injury - Unknown return date",
  "chance_of_playing_this_round": 0, "chance_of_playing_next_round": 0
}
```
Status values: `"injured"`, `"unavailable"`, `"doubtful"`, `"suspended"`.

### get_season_transfers
Get transfer history for specific players via Transfermarkt. Works for any league.
- `season_id` (str, required): Season slug (used to filter transfers by year)
- `tm_player_ids` (list, required): Transfermarkt player IDs

Returns `data.transfers[]`:
```json
{
  "player_tm_id": "433177", "date": "2019-07-01", "season": "19/20",
  "from_team": {"name": "Arsenal U23", "image": "https://..."},
  "to_team": {"name": "Arsenal", "image": "https://..."},
  "fee": "-", "market_value": "-"
}
```

### get_player_season_stats
Get player season stats via ESPN overview endpoint. Works for any league with ESPN athlete IDs.
- `player_id` (str, required): ESPN athlete ID
- `league_slug` (str, optional): League slug hint (e.g., "eng.1", "esp.1"). Defaults to auto-detect.

Returns season stats (goals, assists, appearances, etc.) and game log when available.

### get_player_profile
Get player profile. Works for any player if you have their Transfermarkt or FPL ID. At least one ID required.
- `fpl_id` (str, optional): FPL player ID (PL players only)
- `tm_player_id` (str, optional): Transfermarkt player ID (any league)

With `tm_player_id`, returns `data.player` with:
```json
{
  "market_value": {"value": 130000000, "currency": "EUR", "formatted": "€130.00m", "date": "09/12/2025", "age": "24", "club": "Arsenal FC"},
  "market_value_history": [{"value": 7000000, "formatted": "€7.00m", "date": "23/09/2019", "club": "Arsenal FC"}],
  "transfer_history": [
    {"player_tm_id": "433177", "date": "2019-07-01", "season": "19/20", "from_team": {"name": "Arsenal U23"}, "to_team": {"name": "Arsenal"}, "fee": "-"}
  ]
}
```

With `fpl_id`, also includes `data.player.fpl_data` with FPL stats (points, form, ICT index, ownership, etc.).

## Supported Leagues

Premier League, La Liga, Bundesliga, Serie A, Ligue 1, MLS, Championship, Eredivisie, Primeira Liga, Serie A Brazil, Champions League, European Championship, World Cup.

## Data Sources

| Source | What it provides | League coverage |
|--------|-----------------|-----------------|
| ESPN | Scores, standings, schedules, lineups, match stats, timelines | All 13 leagues |
| openfootball | Schedules, standings, team lists (fallback when ESPN is down) | 10 leagues (all except CL, Euros, World Cup) |
| Understat | xG per match, xG per shot, player xG/xA | Top 5 (EPL, La Liga, Bundesliga, Serie A, Ligue 1) |
| FPL | Top scorers, injuries, player stats, ownership | Premier League only |
| Transfermarkt | Market values, transfer history | Any player (requires tm_player_id) |

For licensed data with full coverage across all sports (Sportradar, Opta, Genius Sports), see [Machina Sports](https://machina.gg).

## Examples

User: "Show me the Premier League table"
1. Call `get_current_season(competition_id="premier-league")` to get the current season_id
2. Call `get_season_standings(season_id=<season_id from step 1>)`
3. Present standings table with position, team, played, won, drawn, lost, GD, points

User: "How did Arsenal vs Liverpool go?"
1. Call `get_daily_schedule()` or `get_team_schedule(team_id="359")` to find the event_id
2. Call `get_event_summary(event_id="...")` for the score
3. Call `get_event_statistics(event_id="...")` for possession, shots, etc.
4. Call `get_event_xg(event_id="...")` for xG comparison (EPL — top 5 only)
5. Present match report with scores, key stats, and xG

User: "Deep dive on Chelsea's recent form"
1. Call `search_team(query="Chelsea")` → team_id=363, competition=premier-league
2. Call `get_team_schedule(team_id="363", competition_id="premier-league")` → find recent closed events
3. For each recent match, call in parallel:
   - `get_event_xg(event_id="...")` for xG comparison and shot map
   - `get_event_statistics(event_id="...")` for possession, shots, passes
   - `get_event_players_statistics(event_id="...")` for individual player xG/xA
4. Call `get_missing_players(season_id=<season_id>)` → filter Chelsea's injured/doubtful players
5. Call `get_season_leaders(season_id=<season_id>)` → filter Chelsea players, get their FPL IDs
6. Call `get_player_profile(fpl_id="...", tm_player_id="...")` for key players — combine FPL stats (form, ownership, ICT) with Transfermarkt data (market value, transfer history)
7. Present: xG trend across matches, key player stats, injury report, market values

User: "What's Saka's market value?"
1. Call `get_player_profile(tm_player_id="433177")` for Transfermarkt data
2. Optionally add `fpl_id` for FPL stats if Premier League player
3. Present market value, value history, and transfer history

User: "Tell me about Corinthians"
1. Call `search_team(query="Corinthians")` → team_id=874, competition=serie-a-brazil
2. Call `get_team_schedule(team_id="874", competition_id="serie-a-brazil")` for fixtures
3. Pick a recent match and call `get_event_timeline(event_id="...")` for goals, cards, subs
4. Note: xG, FPL stats, and season leaders are NOT available for Brazilian Serie A

## Error Handling

When a command fails (wrong event_id, missing data, network error, etc.), **do not surface the raw error to the user**. Instead:

1. **Catch it silently** — treat the failure as an exploratory miss, not a fatal error.
2. **Try alternatives** — e.g., if an event_id returns no data, call `get_daily_schedule()` or `get_team_schedule()` to discover the correct ID. If ESPN is down, openfootball data may still be available via `get_season_standings` or `get_season_schedule`.
3. **Only report failure after exhausting alternatives** — and when you do, give a clean human-readable message (e.g., "I couldn't find that match — can you confirm the teams or date?"), not a traceback or raw CLI output.

This is especially important when the agent is responding through messaging platforms (Telegram, Slack, etc.) where raw exec failures look broken.

## Common Mistakes

**These are the ONLY valid commands.** Do not invent or guess command names:
- `get_current_season`
- `get_competitions`
- `get_competition_seasons`
- `get_season_schedule`
- `get_season_standings`
- `get_season_leaders`
- `get_season_teams`
- `search_team`
- `get_team_profile`
- `get_daily_schedule`
- `get_event_summary`
- `get_event_lineups`
- `get_event_statistics`
- `get_event_timeline`
- `get_team_schedule`
- `get_head_to_head`
- `get_event_xg`
- `get_event_players_statistics`
- `get_missing_players`
- `get_season_transfers`
- `get_player_profile`
- `get_player_season_stats`

**Commands that DO NOT exist** (commonly hallucinated):
- ~~`get_standings`~~ — the correct command is `get_season_standings` (requires `season_id`).
- ~~`get_live_scores`~~ — not available. Use `get_daily_schedule()` for today's matches; status field shows "live" for in-progress games.
- ~~`get_team_squad`~~ / ~~`get_team_roster`~~ — `get_team_profile` does NOT return players. Use `get_season_leaders` for PL player IDs, then `get_player_profile` for individual data.
- ~~`get_transfers`~~ — the correct command is `get_season_transfers` (requires `season_id` + `tm_player_ids`).
- ~~`get_match_results`~~ / ~~`get_match`~~ — use `get_event_summary` with an `event_id`.
- ~~`get_player_stats`~~ — use `get_event_players_statistics` for match-level stats, or `get_player_profile` for career data.

**Other common mistakes:**
- Using `get_season_leaders` or `get_missing_players` on non-PL leagues — they return empty. Check the Data Coverage table.
- Using `get_event_xg` on leagues outside the top 5 — returns empty. Only works for EPL, La Liga, Bundesliga, Serie A, Ligue 1.
- Guessing `team_id` or `event_id` instead of discovering them via `search_team`, `get_daily_schedule`, or `get_season_schedule`.

If you're unsure whether a command exists, check this list. Do not try commands that aren't listed above.

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills`. If the package is not found on PyPI, install from GitHub: `pip install git+https://github.com/machina-sports/sports-skills.git`. Requires Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **Empty results for PL-only commands on other leagues**: `get_season_leaders` and `get_missing_players` only return data for Premier League. They silently return empty for other leagues — check the Data Coverage table.
- **`get_team_profile` returns empty players**: This is expected — squad rosters are not available. To get player data for a PL team, use `get_season_leaders` to find players and their FPL IDs, then `get_player_profile(fpl_id="...")` for detailed stats. For Transfermarkt data, you need the player's `tm_player_id`.
- **Finding FPL IDs and Transfermarkt IDs**: Use `get_season_leaders(season_id="premier-league-2025")` to discover FPL IDs for PL players. Transfermarkt IDs must be looked up on [transfermarkt.com](https://www.transfermarkt.com) — the ID is the number at the end of the player's URL. Well-known examples: Cole Palmer = `568177`, Bukayo Saka = `433177`, Mbappe = `342229`.
- **No xG for recent matches**: Understat data may lag 24-48 hours after a match ends. If `get_event_xg` returns empty for a recent top-5 match, try again later.
- **Wrong season_id format**: Must be `{league-slug}-{year}` e.g. `"premier-league-2025"`. Not `"2025-2026"`, not `"EPL-2025"`. Use `get_current_season()` to discover the correct format.
- **Team/event IDs unknown**: Use `search_team(query="team name")` to find team IDs by name, or `get_season_teams` to list all teams in a season. Use `get_daily_schedule` or `get_season_schedule` to find event IDs. IDs are ESPN numeric strings.
