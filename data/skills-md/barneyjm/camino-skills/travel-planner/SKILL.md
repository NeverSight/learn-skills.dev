---
name: travel-planner
description: "Plan complete day trips, walking tours, and multi-stop itineraries with time budgets using Camino AI's journey planning and route optimization."
metadata: {"clawdbot":{"emoji":"✈️","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (query, places, relationship, context, route, journey, real-estate, hotel-finder, ev-charger, school-finder, parking-finder, fitness-finder, safety-checker, travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill travel-planner
```

**Via clawhub:**
```bash
npx clawhub@latest install travel-planner
# or: pnpm dlx clawhub@latest install travel-planner
# or: bunx clawhub@latest install travel-planner
```

# Travel Planner

Plan complete day trips, walking tours, and multi-stop itineraries with time budgets. Wraps the Camino AI journey endpoint with opinionated defaults for travel planning.

## Setup

**Instant Trial (no signup required):** Get a temporary API key with 25 calls:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

Returns: `{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

For 1,000 free calls/month, sign up at [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate).

**Add your key to Claude Code:**

Add to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

Restart Claude Code.

## Usage

### Via Shell Script

```bash
# Plan a walking tour in Paris
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
    {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre Museum"}
  ],
  "constraints": {"transport": "foot", "time_budget": "4 hours"}
}'

# Plan a driving day trip
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 34.0195, "lon": -118.4912, "purpose": "Santa Monica Pier"},
    {"lat": 34.0259, "lon": -118.7798, "purpose": "Malibu Beach"},
    {"lat": 34.0922, "lon": -118.3287, "purpose": "Hollywood Sign viewpoint"}
  ],
  "constraints": {"transport": "car", "time_budget": "6 hours"}
}'

# Simple two-stop trip
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 40.7484, "lon": -73.9857, "purpose": "Empire State Building"},
    {"lat": 40.7614, "lon": -73.9776, "purpose": "MoMA"}
  ]
}'
```

### Via curl

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "waypoints": [
      {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
      {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre"}
    ],
    "constraints": {"transport": "foot", "time_budget": "4 hours"}
  }' \
  "https://api.getcamino.ai/journey"
```

## Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| waypoints | array | Yes | - | List of stops with lat, lon, and purpose (min 2) |
| constraints | object | No | - | Trip constraints |
| constraints.transport | string | No | "walking" | Transport mode: "walking", "car", or "bike" |
| constraints.time_budget | string | No | - | Time limit (e.g., "4 hours", "90 minutes") |
| constraints.preferences | array | No | [] | Route preferences |

### Waypoint Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lat | float | Yes | Latitude of the stop |
| lon | float | Yes | Longitude of the stop |
| purpose | string | No | Description of the stop (e.g., "Eiffel Tower", "lunch break") |

## Response Format

```json
{
  "feasible": true,
  "total_distance_km": 6.8,
  "total_time_minutes": 85,
  "total_time_formatted": "1 hour 25 minutes",
  "transport_mode": "foot",
  "route_segments": [
    {
      "from": "Eiffel Tower",
      "to": "Louvre Museum",
      "distance_km": 3.4,
      "duration_minutes": 42
    },
    {
      "from": "Louvre Museum",
      "to": "Notre-Dame",
      "distance_km": 3.4,
      "duration_minutes": 43
    }
  ],
  "analysis": {
    "summary": "This walking tour is feasible within your 4-hour time budget...",
    "optimization_opportunities": ["Consider starting at the Louvre to reduce backtracking"]
  }
}
```

## Examples

### Paris walking tour
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
    {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre Museum"},
    {"lat": 48.8530, "lon": 2.3499, "purpose": "Notre-Dame Cathedral"},
    {"lat": 48.8867, "lon": 2.3431, "purpose": "Sacre-Coeur"}
  ],
  "constraints": {
    "transport": "foot",
    "time_budget": "6 hours"
  }
}'
```

### NYC cycling tour
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Start at Battery Park"},
    {"lat": 40.6892, "lon": -74.0445, "purpose": "Statue of Liberty viewpoint"},
    {"lat": 40.7061, "lon": -73.9969, "purpose": "Brooklyn Bridge"},
    {"lat": 40.7580, "lon": -73.9855, "purpose": "Times Square"}
  ],
  "constraints": {
    "transport": "bike",
    "time_budget": "3 hours"
  }
}'
```

### Business meeting circuit
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 37.7749, "lon": -122.4194, "purpose": "Office downtown"},
    {"lat": 37.7849, "lon": -122.4094, "purpose": "Client meeting"},
    {"lat": 37.7900, "lon": -122.4000, "purpose": "Lunch"},
    {"lat": 37.7749, "lon": -122.4194, "purpose": "Return to office"}
  ],
  "constraints": {
    "transport": "car",
    "time_budget": "2 hours"
  }
}'
```

## Best Practices

- Always include a `purpose` for each waypoint to get better route analysis
- Set a `time_budget` to get feasibility checks and optimization suggestions
- Use "foot" transport for city walking tours, "bike" for cycling tours, "car" for road trips
- Order waypoints in your preferred visiting sequence; the API will check feasibility
- Combine with the `query` skill to discover points of interest to add as waypoints
- Combine with the `hotel-finder` skill to find accommodation near your first or last waypoint
- Combine with the `context` skill to learn more about each waypoint's neighborhood
- For longer trips, break the itinerary into manageable day segments
