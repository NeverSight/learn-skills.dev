---
name: parking-finder
description: "Locate parking garages, lots, and street parking near your destination using Camino AI's location intelligence with AI-powered ranking."
metadata: {"clawdbot":{"emoji":"🅿️","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (query, places, relationship, context, route, journey, real-estate, hotel-finder, ev-charger, school-finder, parking-finder, fitness-finder, safety-checker, travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill parking-finder
```

**Via clawhub:**
```bash
npx clawhub@latest install parking-finder
# or: pnpm dlx clawhub@latest install parking-finder
# or: bunx clawhub@latest install parking-finder
```

# Parking Finder

Locate parking garages, lots, and street parking near your destination. Uses OpenStreetMap data with AI-powered ranking to find the most relevant parking options.

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
# Find parking near a venue
./scripts/parking-finder.sh '{"query": "parking near Madison Square Garden", "limit": 10}'

# Find parking with coordinates
./scripts/parking-finder.sh '{"lat": 40.7505, "lon": -73.9934, "radius": 500}'

# Find parking garages specifically
./scripts/parking-finder.sh '{"query": "parking garages", "lat": 37.7749, "lon": -122.4194}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=parking+garages+lots&lat=40.7505&lon=-73.9934&radius=1000&rank=true"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | No | "parking garages lots" | Search query (override for specific parking types) |
| lat | float | No | - | Latitude for search center. AI generates if omitted for known locations. |
| lon | float | No | - | Longitude for search center. AI generates if omitted for known locations. |
| radius | int | No | 1000 | Search radius in meters |
| limit | int | No | 15 | Maximum results (1-100) |

## Response Format

```json
{
  "query": "parking garages lots",
  "results": [
    {
      "name": "Icon Parking - West 33rd Street",
      "lat": 40.7502,
      "lon": -73.9930,
      "type": "parking",
      "distance_m": 120,
      "relevance_score": 0.93,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 11,
    "limit": 15,
    "offset": 0,
    "has_more": false
  }
}
```

## Examples

### Parking near a stadium
```bash
./scripts/parking-finder.sh '{"query": "parking near Dodger Stadium", "radius": 2000}'
```

### Parking near an airport
```bash
./scripts/parking-finder.sh '{"query": "long term parking near SFO airport", "radius": 3000}'
```

### Parking in a downtown area
```bash
./scripts/parking-finder.sh '{"lat": 41.8781, "lon": -87.6298, "radius": 800, "limit": 10}'
```

## Best Practices

- Use a smaller radius (500-1000m) in dense urban areas where parking is nearby but hard to find
- Use a larger radius (2000-3000m) near stadiums, airports, or suburban destinations
- Include the venue name in your query for contextual results (e.g., "parking near Madison Square Garden")
- Combine with the `route` skill to get walking directions from parking to your destination
- Combine with the `relationship` skill to compare distances between multiple parking options
- Specify "parking garages" or "street parking" in the query for more targeted results
