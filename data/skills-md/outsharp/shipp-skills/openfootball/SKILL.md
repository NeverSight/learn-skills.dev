---
name: openfootball
description: >
  openfootball (football.json) is a free, open, public domain collection of
  football (soccer) match data in JSON format. It covers major leagues worldwide
  including the English Premier League, Bundesliga, La Liga, Serie A, Ligue 1,
  World Cup, Euro, and Champions League. Use this skill to fetch historical and
  current season fixtures, results, and scores. No API key or authentication is
  required.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Any HTTP client (curl, wget, fetch, requests, etc.)
    - A JSON parser
  notes:
    - All data is fully public — no authentication, API key, or account is needed.
    - Responses are JSON.
    - Data is served via raw GitHub URLs and GitHub Pages — standard GitHub rate limits apply.
    - Data is community-maintained and may lag behind live results by hours or days.
    - This is historical/completed match data, not live or real-time.

allowed-tools:
  - Bash(curl:*)
  - Bash(wget:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(node*:*)
  - Bash(npx*:*)
  - Bash(jq:*)

---

# openfootball / football.json API

[openfootball](https://github.com/openfootball) is a free, open, public domain collection of football (soccer) data. The [football.json](https://github.com/openfootball/football.json) repository provides pre-built JSON files for major leagues and tournaments worldwide. **No API key or authentication is required.**

---

## Data Sources

There are two ways to access the data:

### 1. Raw GitHub URLs (Primary)

```
https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{league}.json
```

### 2. GitHub Pages Mirror

```
https://openfootball.github.io/{country}/{season}/{league-name}.json
```

> **Recommendation:** Use the raw GitHub URLs for the `football.json` repo — they use a simple, consistent naming convention and are the most reliable.

---

## URL Structure

```
https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{code}.json
```

| Component | Description | Examples |
|-----------|-------------|---------|
| `{season}` | Season directory — cross-year or calendar year | `2024-25`, `2023-24`, `2025`, `2019` |
| `{code}` | League code in `{country}.{division}` format | `en.1`, `de.1`, `es.1`, `it.1`, `fr.1` |

---

## Available Leagues

### England

| Code | League | Tier |
|------|--------|------|
| `en.1` | English Premier League | 1st division |
| `en.2` | English Championship | 2nd division |
| `en.3` | English League One | 3rd division |
| `en.4` | English League Two | 4th division |

### Germany

| Code | League | Tier |
|------|--------|------|
| `de.1` | Deutsche Bundesliga | 1st division |
| `de.2` | 2. Bundesliga | 2nd division |
| `de.3` | 3. Liga | 3rd division |

### Spain

| Code | League | Tier |
|------|--------|------|
| `es.1` | Primera División (La Liga) | 1st division |
| `es.2` | Segunda División | 2nd division |

### Italy

| Code | League | Tier |
|------|--------|------|
| `it.1` | Serie A | 1st division |
| `it.2` | Serie B | 2nd division |

### France

| Code | League | Tier |
|------|--------|------|
| `fr.1` | Ligue 1 | 1st division |
| `fr.2` | Ligue 2 | 2nd division |

> **Note:** Not all leagues are available for all seasons. The `football.json` repo is continuously updated — check the [repository](https://github.com/openfootball/football.json) for the full list of available files.

---

## Available Seasons

Season directories in the `football.json` repo go back to `2010-11`. European leagues use cross-year format (`2024-25`), while some calendar-year leagues use single-year format (`2025`).

| Format | Usage | Examples |
|--------|-------|---------|
| `YYYY-YY` | European club seasons (Aug–May) | `2024-25`, `2023-24`, `2015-16` |
| `YYYY` | Calendar-year competitions | `2025`, `2020`, `2019` |

Known season directories: `2010-11`, `2011-12`, `2012-13`, `2013-14`, `2014-15`, `2015-16`, `2016-17`, `2017-18`, `2018-19`, `2019-20`, `2020-21`, `2021-22`, `2022-23`, `2023-24`, `2024-25`, `2025-26`, `2019`, `2020`, `2025`.

---

## JSON Response Format

All files follow the same JSON schema:

```json
{
  "name": "English Premier League 2024/25",
  "matches": [
    {
      "round": "Matchday 1",
      "date": "2024-08-16",
      "time": "20:00",
      "team1": "Manchester United FC",
      "team2": "Fulham FC",
      "score": {
        "ht": [0, 0],
        "ft": [1, 0]
      }
    }
  ]
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable league name and season |
| `matches` | array | Array of match objects |

### Match Object Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `round` | string | Yes | Round/matchday name (e.g., `"Matchday 1"`, `"Round of 16"`) |
| `date` | string | Yes | Match date in `YYYY-MM-DD` format |
| `time` | string | No | Kick-off time in `HH:MM` format (24-hour, local time) |
| `team1` | string | Yes | Home team name |
| `team2` | string | Yes | Away team name |
| `score` | object | No | Score object (absent for unplayed future matches) |
| `status` | string | No | Special status (e.g., `"awarded"` for administratively decided results) |

### Score Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `ft` | `[int, int]` | Full-time score `[home, away]` |
| `ht` | `[int, int]` | Half-time score `[home, away]` (may be absent for some matches) |

> **Note:** Some matches only have `ft` (full-time) without `ht` (half-time). Always check for the presence of `ht` before accessing it.

---

## Common Patterns

### Fetch a League Season (curl)

```bash
curl -s "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json" | jq .
```

### Fetch and Parse Match Data (Python)

```python
import requests

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
data = requests.get(url).json()

print(f"League: {data['name']}")
print(f"Total matches: {len(data['matches'])}")

for match in data["matches"][:10]:
    ft = match.get("score", {}).get("ft")
    if ft:
        print(f"  {match['date']}  {match['team1']} {ft[0]}-{ft[1]} {match['team2']}")
    else:
        print(f"  {match['date']}  {match['team1']} vs {match['team2']} (no score)")
```

### Build a League Table from Results (Python)

```python
import requests
from collections import defaultdict

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
data = requests.get(url).json()

table = defaultdict(lambda: {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                              "gf": 0, "ga": 0, "points": 0})

for match in data["matches"]:
    score = match.get("score", {}).get("ft")
    if not score:
        continue

    t1, t2 = match["team1"], match["team2"]
    g1, g2 = score

    for team, gf, ga in [(t1, g1, g2), (t2, g2, g1)]:
        table[team]["played"] += 1
        table[team]["gf"] += gf
        table[team]["ga"] += ga
        if gf > ga:
            table[team]["won"] += 1
            table[team]["points"] += 3
        elif gf == ga:
            table[team]["drawn"] += 1
            table[team]["points"] += 1
        else:
            table[team]["lost"] += 1

# Sort by points, then goal difference
sorted_table = sorted(table.items(),
                       key=lambda x: (x[1]["points"], x[1]["gf"] - x[1]["ga"]),
                       reverse=True)

print(f"{'Team':<35} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>4} {'GA':>4} {'GD':>4} {'Pts':>4}")
print("-" * 70)
for i, (team, stats) in enumerate(sorted_table, 1):
    gd = stats["gf"] - stats["ga"]
    print(f"{i:>2}. {team:<32} {stats['played']:>3} {stats['won']:>3} "
          f"{stats['drawn']:>3} {stats['lost']:>3} {stats['gf']:>4} "
          f"{stats['ga']:>4} {gd:>+4} {stats['points']:>4}")
```

### Filter Matches by Team (Python)

```python
import requests

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
data = requests.get(url).json()

team = "Arsenal FC"
matches = [m for m in data["matches"]
           if team in (m["team1"], m["team2"]) and m.get("score", {}).get("ft")]

for m in matches:
    ft = m["score"]["ft"]
    opponent = m["team2"] if m["team1"] == team else m["team1"]
    venue = "H" if m["team1"] == team else "A"
    my_goals = ft[0] if m["team1"] == team else ft[1]
    opp_goals = ft[1] if m["team1"] == team else ft[0]
    result = "W" if my_goals > opp_goals else ("D" if my_goals == opp_goals else "L")
    print(f"  {m['date']} ({venue}) {result} {my_goals}-{opp_goals} vs {opponent}")
```

### Fetch Multiple Leagues (Python)

```python
import requests

leagues = {
    "Premier League": "en.1",
    "Bundesliga": "de.1",
    "La Liga": "es.1",
    "Serie A": "it.1",
    "Ligue 1": "fr.1",
}

season = "2024-25"
base = "https://raw.githubusercontent.com/openfootball/football.json/master"

for name, code in leagues.items():
    url = f"{base}/{season}/{code}.json"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        total = len(data["matches"])
        played = sum(1 for m in data["matches"] if m.get("score", {}).get("ft"))
        print(f"{name}: {played}/{total} matches played")
    else:
        print(f"{name}: not available for {season}")
```

### Fetch and Parse (Node.js)

```javascript
const url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json";

const res = await fetch(url);
const data = await res.json();

console.log(`League: ${data.name}`);
console.log(`Matches: ${data.matches.length}`);

data.matches.slice(0, 10).forEach((m) => {
  const ft = m.score?.ft;
  if (ft) {
    console.log(`  ${m.date}  ${m.team1} ${ft[0]}-${ft[1]} ${m.team2}`);
  }
});
```

### Fetch and Parse (bash + jq)

```bash
# Get all results for a specific team
curl -s "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json" \
  | jq -r '.matches[]
    | select(.team1 == "Liverpool FC" or .team2 == "Liverpool FC")
    | select(.score.ft)
    | "\(.date) \(.team1) \(.score.ft[0])-\(.score.ft[1]) \(.team2)"'
```

### Compare Head-to-Head Results (Python)

```python
import requests

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
data = requests.get(url).json()

team_a = "Arsenal FC"
team_b = "Liverpool FC"

h2h = [m for m in data["matches"]
       if {m["team1"], m["team2"]} == {team_a, team_b}
       and m.get("score", {}).get("ft")]

for m in h2h:
    ft = m["score"]["ft"]
    ht = m["score"].get("ht", ["?", "?"])
    print(f"{m['date']}: {m['team1']} {ft[0]}-{ft[1]} {m['team2']} (HT: {ht[0]}-{ht[1]})")
```

### Aggregate Stats Across Seasons (Python)

```python
import requests

base = "https://raw.githubusercontent.com/openfootball/football.json/master"
seasons = ["2022-23", "2023-24", "2024-25"]
team = "Manchester City FC"
all_results = {"W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0}

for season in seasons:
    resp = requests.get(f"{base}/{season}/en.1.json")
    if resp.status_code != 200:
        continue
    data = resp.json()
    for m in data["matches"]:
        ft = m.get("score", {}).get("ft")
        if not ft:
            continue
        if m["team1"] == team:
            gf, ga = ft
        elif m["team2"] == team:
            ga, gf = ft
        else:
            continue
        all_results["GF"] += gf
        all_results["GA"] += ga
        if gf > ga:
            all_results["W"] += 1
        elif gf == ga:
            all_results["D"] += 1
        else:
            all_results["L"] += 1

print(f"{team} across {', '.join(seasons)}:")
print(f"  W{all_results['W']} D{all_results['D']} L{all_results['L']}")
print(f"  Goals: {all_results['GF']} scored, {all_results['GA']} conceded")
```

### Find High-Scoring Matches (bash + jq)

```bash
# Find all matches with 5+ total goals in the Premier League 2024/25
curl -s "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json" \
  | jq -r '.matches[]
    | select(.score.ft)
    | select((.score.ft[0] + .score.ft[1]) >= 5)
    | "\(.date) \(.team1) \(.score.ft[0])-\(.score.ft[1]) \(.team2) (Total: \(.score.ft[0] + .score.ft[1]))"'
```

### Get Results for a Specific Matchday (Python)

```python
import requests

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
data = requests.get(url).json()

matchday = "Matchday 38"
matches = [m for m in data["matches"] if m["round"] == matchday]

print(f"--- {matchday} ---")
for m in matches:
    ft = m.get("score", {}).get("ft")
    if ft:
        print(f"  {m['date']} {m.get('time', '')}  {m['team1']} {ft[0]}-{ft[1]} {m['team2']}")
    else:
        print(f"  {m['date']} {m.get('time', '')}  {m['team1']} vs {m['team2']}")
```

---

## Other Repositories (Source Data)

The `football.json` files are auto-generated from plain-text Football.TXT source files in country-specific repos:

| Repo | Content | GitHub URL |
|------|---------|------------|
| `england` | EPL, Championship, League One, League Two | [openfootball/england](https://github.com/openfootball/england) |
| `deutschland` | Bundesliga, 2. Bundesliga, 3. Liga, DFB Pokal | [openfootball/deutschland](https://github.com/openfootball/deutschland) |
| `espana` | La Liga, Segunda División | [openfootball/espana](https://github.com/openfootball/espana) |
| `italy` | Serie A, Serie B, Coppa Italia | [openfootball/italy](https://github.com/openfootball/italy) |
| `france` | Ligue 1, Ligue 2 | [openfootball/europe](https://github.com/openfootball/europe) (in `/europe`) |
| `worldcup` | FIFA World Cup (2022, 2018, 2014, etc.) | [openfootball/worldcup](https://github.com/openfootball/worldcup) |
| `euro` | Euro 2024, 2020, 2016, etc. | [openfootball/euro](https://github.com/openfootball/euro) |
| `champions-league` | UCL & Europa League | [openfootball/champions-league](https://github.com/openfootball/champions-league) |
| `clubs` | Club & stadium metadata | [openfootball/clubs](https://github.com/openfootball/clubs) |
| `world` | Leagues from N. America, Asia, Africa, Australia | [openfootball/world](https://github.com/openfootball/world) |

Country repos also have their own GitHub Pages JSON mirrors. For example:

```
https://openfootball.github.io/england/2024-25/1-premierleague.json
```

You can convert Football.TXT source files to JSON yourself using the `fbtxt2json` CLI tool:

```bash
# Convert a single league file
fbtxt2json england/2025-26/1-premierleague.txt -o en.1.json

# Convert an entire country repo at once
fbtxt2json . -o ./_site
```

---

## Rate Limits

GitHub does not publish specific rate limits for raw content, but general guidelines:

| Guideline | Recommendation |
|-----------|----------------|
| Polling interval | ≥ 60 seconds between requests for the same file |
| Concurrent requests | Keep reasonable (< 20 concurrent) |
| Caching | Cache responses locally — data changes infrequently |
| Unauthenticated GitHub API | 60 requests/hour per IP (only applies to API endpoints, not raw content) |

> **Tip:** Since match data doesn't change after a game is completed, you can aggressively cache historical seasons. Only poll the current season for updates.

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse the JSON |
| 404 | File not found | Check the season, league code, or URL spelling |
| 429 | Rate limited | Back off and retry after a delay |
| 5xx | Server error | Retry with exponential backoff |

---

## Tips

- **No auth needed** — all data is fully public. Start fetching immediately.
- **Check for `score` before accessing** — future/unplayed matches won't have a `score` field.
- **Check for `ht` separately** — some matches have `ft` but no `ht` data.
- **Team names include suffixes** — e.g., `"Arsenal FC"`, `"Manchester United FC"`, `"Borussia Dortmund"`. Use exact string matching.
- **Team names vary by league** — German teams use German names (`"FC Bayern München"`), English teams use English names (`"Arsenal FC"`).
- **The `status` field is rare** — it appears on administratively decided matches (e.g., `"awarded"`).
- **Cache aggressively** — completed seasons never change. Only the current season gets updates.
- **Build tables from the data** — the dataset provides raw match results; you compute standings, form, H2H, etc.
- **Cross-reference leagues** — fetch multiple league files to compare across countries.
- **Public domain (CC0)** — use the data however you want with no restrictions whatsoever.
- **Don't edit the JSON directly** — if contributing, edit the Football.TXT source files in the country repos; JSON is auto-generated.
- **Time field is local** — the `time` value represents the local kick-off time for the match venue.
- **Scores are `[home, away]`** — `score.ft[0]` is always the `team1` (home) goals, `score.ft[1]` is always the `team2` (away) goals.

---

## Changelog

- **0.1.0** — Initial release with league data access, JSON schema documentation, and common usage patterns.