---
name: nba-game-intel
description: Retrieve NBA game information from ESPN public APIs, including daily scoreboards, game summaries, boxscores, play-by-play, team lists, team schedules, and standings context. Use when requests ask for NBA scores, live game status, specific game-id details, or team-centric recent/upcoming game context.
---

# NBA Game Intel

Use this skill to map natural-language NBA game requests to ESPN endpoints and return consistent, source-backed summaries.

## Endpoint Reference

Read endpoint details in [references/espn-nba-endpoints.md](references/espn-nba-endpoints.md).

## Workflow

1. Classify request type:
   - `scoreboard`: "today's NBA games", "scores on 2026-02-20"
   - `summary`: "game summary for event 401585123"
   - `boxscore`: "full boxscore for game 401585123"
   - `playbyplay`: "play-by-play for game 401585123"
   - `team-schedule`: "Lakers upcoming schedule"
   - `teams` / `standings`: supporting team or context lookups
2. Select the matching endpoint from `references/espn-nba-endpoints.md`.
3. Fill required params exactly:
   - `sport=basketball`
   - `league=nba`
   - `event_id` or `team_id` when required
4. Request JSON data and extract the core game context for the user.
5. Return a normalized result with endpoint provenance.

## Output Contract

Return concise structured output with these fields when available:

- `request_type`
- `source_endpoint`
- `event_id`
- `status` (scheduled/live/final + short detail)
- `teams` (home/away names + scores)
- `date_time`
- `top_notes` (leaders/highlights or notable context)

Always include the endpoint URL template you used and the concrete URL after parameter substitution.

## Failure Handling

- Missing or invalid `event_id`: tell the user the ID is required and suggest finding it via `scoreboard`.
- Empty scoreboard/date: report no games found for that date and suggest checking adjacent dates.
- Unavailable live details: fall back in this order:
  1. `summary`
  2. `boxscore`
  3. `scoreboard` context

## Response Quality Rules

- Keep answers compact and factual.
- Prefer explicit dates in `YYYY-MM-DD` format.
- Do not invent scores, status, or IDs.
- If data is partial, state what is missing and what endpoint was attempted.

## Validation Scenarios

- "Get today's NBA games and scores." -> `scoreboard`
- "Give me summary for game id 401585123." -> `summary`
- "Show full boxscore for game id 401585123." -> `boxscore`
- "Show play-by-play for game id 401585123." -> `playbyplay`
- "What is the Lakers upcoming schedule?" -> `team-schedule`
- Invalid game id -> clear error + recommend scoreboard lookup for valid IDs
