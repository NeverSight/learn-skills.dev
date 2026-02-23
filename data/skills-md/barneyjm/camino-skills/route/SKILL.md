---
name: route
description: "Get detailed routing between two points with distance, duration, and optional turn-by-turn directions. Use when you need navigation instructions or travel time estimates between locations."
metadata: {"clawdbot":{"emoji":"🧭","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (query, places, relationship, context, route, journey, real-estate, hotel-finder, ev-charger, school-finder, parking-finder, fitness-finder, safety-checker, travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill route
```

**Via clawhub:**
```bash
npx clawhub@latest install route
# or: pnpm dlx clawhub@latest install route
# or: bunx clawhub@latest install route
```

# Route - Point-to-Point Navigation

Get detailed routing between two points with distance, duration, and optional turn-by-turn directions.

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
# Get driving directions
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851
}'

# Walking directions
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "foot"
}'

# With route geometry for mapping
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "bike",
  "include_geometry": true
}'
```

### Via curl

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/route?start_lat=40.7128&start_lon=-74.0060&end_lat=40.7589&end_lon=-73.9851&mode=car"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| start_lat | float | Yes | - | Starting latitude |
| start_lon | float | Yes | - | Starting longitude |
| end_lat | float | Yes | - | Ending latitude |
| end_lon | float | Yes | - | Ending longitude |
| mode | string | No | "car" | Transport mode: "car", "bike", or "foot" |
| include_geometry | bool | No | false | Include detailed route geometry for mapping |
| include_imagery | bool | No | false | Include street-level imagery at waypoints |

## Response Format

```json
{
  "distance_km": 6.8,
  "duration_minutes": 18,
  "mode": "car",
  "summary": "Head north on Broadway, then east on 42nd Street",
  "steps": [
    {
      "instruction": "Head north on Broadway",
      "distance_m": 2400,
      "duration_s": 420
    },
    {
      "instruction": "Turn right onto 42nd Street",
      "distance_m": 1800,
      "duration_s": 300
    }
  ]
}
```

## Examples

### Walking directions
```bash
./scripts/route.sh '{
  "start_lat": 51.5074,
  "start_lon": -0.1278,
  "end_lat": 51.5014,
  "end_lon": -0.1419,
  "mode": "foot"
}'
```

### Cycling with geometry
```bash
./scripts/route.sh '{
  "start_lat": 37.7749,
  "start_lon": -122.4194,
  "end_lat": 37.8199,
  "end_lon": -122.4783,
  "mode": "bike",
  "include_geometry": true
}'
```

### Driving directions with imagery
```bash
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "car",
  "include_imagery": true
}'
```

## Use Cases

- **Navigation**: Get turn-by-turn directions for any transport mode
- **Travel time estimation**: Know how long it takes to get between two points
- **Map visualization**: Include geometry data for drawing routes on maps
- **Commute planning**: Compare driving, cycling, and walking times
