---
name: sydney-commute
description: >-
  Plan trips, check real-time departures, and find stops on Sydney's public
  transport network (trains, buses, ferries, light rail, metro). Use this
  skill when the user asks about trains, buses, ferries, light rail, metro,
  Opal fares, commuting, "how do I get to", next departure, timetable,
  platform, or any Sydney public transport question. Works without API keys
  (provides Google Maps/TfNSW links) but best with a free TfNSW API key
  for real-time data.
---

# Sydney Commute Skill

Plan trips, check real-time departures, and find stops across Sydney's public transport network. Works without API keys — best with a free TfNSW key for real-time data.

## Install

```bash
npx skills add agairola/life-skills --skill sydney-commute
```

## When to Use

Trigger this skill when the user:

- Asks about trains, buses, ferries, light rail, or metro in Sydney
- Wants to plan a trip or commute ("how do I get to...?")
- Asks about next departures, timetables, or platforms
- Mentions a Sydney station or stop name
- Asks about Opal fares or travel times
- Wants to find nearby stops or stations

## Prerequisites

- **uv** — `brew install uv` (macOS) or `pip install uv` (all platforms)
- **API keys** — not needed for basic links. Optional: TfNSW API key in `~/.config/sydney-commute/credentials.json` for real-time data.
- **Dependencies** — declared inline (PEP 723), installed automatically by `uv run`.

## Setup Status

!`command -v uv > /dev/null 2>&1 && echo "uv: installed" || echo "uv: NOT INSTALLED"`
!`test -f ~/.config/sydney-commute/credentials.json && python3 -c "import json; d=json.load(open('$HOME/.config/sydney-commute/credentials.json')); print('TfNSW API: configured' if d.get('tfnsw_api_key') else 'TfNSW API: not configured')" 2>/dev/null || echo "TfNSW API: not configured (zero-config mode — Google Maps/TfNSW links only)"`

## Location Flow (IMPORTANT — follow this exactly)

Before fetching transport info, you MUST resolve the user's origin and destination. Follow these steps in order.

**Step 1: Extract from/to from the user message.**
- User said "from Central to Bondi Junction"? → use `--from "Central Station" --to "Bondi Junction"`. Done.
- User shared a location pin (Telegram, WhatsApp, Signal, Discord)? Extract lat/lng → use `--lat` / `--lng` with `--from`. Done.
- User mentioned a station, suburb, or address? → use `--from` and/or `--to`. Done.
- **Never ask users for stop IDs** — always ask for place names. The script fuzzy-matches names to stops automatically. If the match is ambiguous (e.g. multiple stops with similar names), confirm with the user before proceeding.

**Step 2: If "from here" or origin is unclear.**
Ask them for their station or suburb. Tailor the ask to their platform:
- Telegram: "Tap the paperclip icon → Location → Send My Current Location"
- WhatsApp: "Tap the + button → Location → Send Your Current Location"
- Signal: "Tap the + button → Location"
- Discord/terminal: "What station or suburb are you near?"

Wait for their response. Do not proceed without it.

**Step 3: For departures mode, only origin is needed.**
If the user asks "next train from Central", you only need `--from "Central Station" --mode departures`.

**Step 4: User can't or won't share location.**
Ask: "No worries — what station or suburb are you near?" Wait for response.

**Never silently use IP geolocation when you can ask the user instead.**

### Command Template

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" [OPTIONS]
```

### Options

| Flag | Values | Default | Purpose |
|------|--------|---------|---------|
| `--from` | station, stop, or place name | *(none)* | Origin location |
| `--to` | station, stop, or place name | *(none)* | Destination location |
| `--mode` | `trip` `departures` `stops` | `trip` | Query mode |
| `--depart` | `HH:MM` or `now` | `now` | Departure time |
| `--arrive-by` | `HH:MM` | *(none)* | Arrive by time |
| `--transport` | `train` `bus` `ferry` `lightrail` `metro` | *(all)* | Filter transport type |
| `--lat` / `--lng` | coordinates | *(auto)* | Explicit coordinates |
| `--no-cache` | *(flag)* | off | Force fresh data |

Only parse **stdout** (JSON). Stderr contains diagnostics only.

### Common Commands

```bash
# Plan a trip
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --from "Central Station" --to "Bondi Junction"

# Trip at a specific time
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --from "Town Hall" --to "Manly" --depart 14:30

# Arrive by a certain time
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --from "Newtown" --to "Circular Quay" --arrive-by 09:00

# Filter by transport type
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --from "Central" --to "Parramatta" --transport train

# Check departures from a stop
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --mode departures --from "Central Station"

# Departures for trains only
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --mode departures --from "Central Station" --transport train

# Search for stops
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --mode stops --from "Central"

# Zero-config (no API key) — returns Google Maps / TfNSW links
uv run "${CLAUDE_SKILL_DIR}/scripts/commute.py" --from "Central Station" --to "Bondi Junction"
```

## Presenting Results

DO NOT use markdown tables. They don't render on mobile chat platforms (Telegram, WhatsApp, Signal). Use plain text with line breaks instead.

### Trip Mode

Keep it simple — users just need to know what to catch, where from, and when.

**Simplification rules:**
- **Consolidate similar routes** — if multiple results are the same route at different times, show it once with a list of departure times. Don't repeat identical legs.
- **Lead with a practical summary** — one plain-English sentence describing the route, like a local would explain it
- Show platform numbers only for large train stations (Central, Town Hall, Wynyard) — users need these to find the right platform
- Always include short line codes (T4, T1, Bus 333) so users can find the right platform/stop
- Drop wharf numbers, sides (Side A/B), stand letters, and terminus descriptions ("City to Parramatta or Leppington")
- Only list distinct route options separately (e.g. train-only vs train+ferry)

**When all results are the same route (common case):**

For platforms with hyperlinks (Telegram, Discord, terminal):
```
Train → Ferry (~35 min)

Take any city train from Central (T1/T4, Platform 17 or 21) to Circular Quay (2 stops), then the Manly ferry (~20 min). Runs every ~20 min.

Next departures: 2:05 pm, 2:26 pm, 2:47 pm

[View on Google Maps](google_maps_url) · [TfNSW Trip Planner](transport_nsw_url)
```

For platforms without hyperlinks (WhatsApp, Signal, SMS):
```
Train → Ferry (~35 min)

Take any city train from Central (T1/T4, Platform 17 or 21) to Circular Quay (2 stops), then the Manly ferry (~20 min). Runs every ~20 min.

Next departures: 2:05 pm, 2:26 pm, 2:47 pm

Google Maps: [url]
TfNSW: [url]
```

**When results have genuinely different routes:**

```
Two ways to get from Central to Parramatta:

1. Direct train (~30 min)
   T1 from Central (Platform 16) to Parramatta · 12 stops
   Next: 2:10 pm, 2:25 pm, 2:40 pm

2. Metro (~25 min)
   Train from Central to Sydenham, then Metro from Sydenham to Parramatta
   Next: 2:15 pm, 2:35 pm

[View on Google Maps](google_maps_url) · [TfNSW Trip Planner](transport_nsw_url)
```

### Departures Mode

Show a compact departure list with delays highlighted.

```
Departures from Central Station:

14:30  T1 North Shore Line → Hornsby · Platform 16 · on time
14:32  T4 Eastern Suburbs → Bondi Junction · Platform 18 · 2 min late
14:35  T2 Inner West Line → Leppington · Platform 20 · on time
14:38  Bus 301 → Eastgardens · Stand B · no realtime
```

Highlight delays: if `delay_min > 0`, show "X min late" in bold or with emphasis. If delay is null and realtime is false, show "no realtime".

### Stops Mode

Show a list with transport types.

```
Stops matching "Central":

1. Central Station — train, bus, lightrail
2. Central Chalmers St — bus
3. Central Pitt St — bus
```

### Zero-Config Mode

When no API key is configured, show the fallback URLs as clickable links.

```
I don't have a TfNSW API key configured, so I can't get real-time data. Here are links to plan your trip:

Google Maps: [Central Station to Bondi Junction](google_maps_url)
TfNSW Trip Planner: [Plan this trip](transport_nsw_url)

For real-time departures and delays, you can set up a free TfNSW API key in about 2 minutes. Want me to walk you through it?
```

### Formatting Rules

- Trip mode: consolidate same-route results into one block with departure times, lead with a plain-English summary, include line codes (T1/T4) and platform at large stations, only list distinct routes separately
- Departures mode: compact time-based list, highlight delays
- Stops mode: numbered list with transport types
- Zero-config: show URLs as clickable links with upgrade nudge
- Google Maps and TfNSW links for each journey
- Real-time indicators: show "on time", "X min late", or "no realtime"

## Handling Edge Cases

- **No API key**: Return zero-config fallback with Google Maps / TfNSW URLs. Always works.
- **Invalid API key** (`401`): Show error with registration URL. "Your TfNSW API key appears to be invalid. You can get a new one at opendata.transport.nsw.gov.au"
- **Ambiguous stop** (multiple matches in departures mode): The script uses the first match and logs alternatives to stderr. If the JSON shows an unexpected stop name, tell the user and suggest alternatives.
- **No results**: "No trips/departures found. Try a different time or check the stop name."
- **Low confidence location** (`confidence: "low"`): Tell the user their location was detected via IP and may not be accurate. Ask for their suburb or station.
- **API errors**: Show the error message from the JSON response. Suggest trying again or checking the stop name.

## Upgrade Nudge

In zero-config mode (no API key), always append an upgrade suggestion. This is shown automatically since the API key is required for any real data.

**When to show:** Every time the JSON response has `"api_key_configured": false`.

**What to say (adapt to tone, don't copy verbatim):**

For platforms with hyperlinks:
```
Tip: For real-time departures, delays, and trip planning, you can register for a free TfNSW API key (~2 minutes):

1. Sign up at [opendata.transport.nsw.gov.au](https://opendata.transport.nsw.gov.au) — name + email
2. Create an application (any name, e.g. "Commute Helper")
3. Subscribe to "Trip Planner APIs" (free: 60,000 calls/day)
4. Copy your API key and share it with me — I'll save it securely.
```

For platforms without hyperlinks:
```
Tip: For real-time data, register for a free TfNSW API key (~2 minutes):

1. Sign up at opendata.transport.nsw.gov.au
2. Create an application (any name works)
3. Subscribe to "Trip Planner APIs" (free tier)
4. Copy your API key and share it with me.
```

**When the user provides a key**, save it securely:

```bash
mkdir -p ~/.config/sydney-commute
cat > ~/.config/sydney-commute/credentials.json << 'CREDS'
{
  "tfnsw_api_key": "<key>"
}
CREDS
chmod 600 ~/.config/sydney-commute/credentials.json
```

Then confirm: "Key saved securely. Future commute queries will use real-time TfNSW data."

**Do NOT show the nudge if:**
- TfNSW API is already configured (check setup status above)
- You've already shown the nudge in this conversation

## Reference

### Transport Types

| Product Class | Type |
|--------------|------|
| 1 | Train |
| 4 | Light Rail |
| 5 | Bus |
| 7 | Coach |
| 9 | Ferry |
| 11 | School Bus |
| 99, 100 | Walk |

### Stop ID Format (internal — script handles automatically)

TfNSW stop IDs are numeric strings used internally by the API. Users always provide place names — the script resolves names to IDs automatically via the stop_finder API. Never ask users for stop IDs.

### Script Location Fallback (internal — for reference only)

When the script runs, it resolves location internally in this order:

1. **Explicit args** — `--lat`/`--lng` (Nominatim reverse geocoding)
2. **From arg** — `--from` value forward-geocoded if it looks like a place name
3. **Browser consent** — localhost page requesting `navigator.geolocation` (WiFi, ~15-50ft accuracy, cached 24hrs)
4. **IP geolocation** — ip-api.com (city-level only, often inaccurate for non-city users)

The agent should almost never reach step 4. The Location Flow above ensures the user provides location info before the script runs.
