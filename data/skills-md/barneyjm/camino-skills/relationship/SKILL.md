---
name: relationship
description: "Calculate spatial relationships between two points including distance, direction, travel time, and human-readable descriptions. Use when you need to understand how locations relate to each other."
metadata: {"clawdbot":{"emoji":"📐","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (query, places, relationship, context, route, journey, real-estate, hotel-finder, ev-charger, school-finder, parking-finder, fitness-finder, safety-checker, travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill relationship
```

**Via clawhub:**
```bash
npx clawhub@latest install relationship
# or: pnpm dlx clawhub@latest install relationship
# or: bunx clawhub@latest install relationship
```

# Relationship - Spatial Calculations

Calculate distance, direction, travel time, and human-readable descriptions between two points.

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
# Calculate relationship between two points
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851}
}'

# Include specific calculations
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction", "travel_time", "description"]
}'
```

### Via curl

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"start": {"lat": 40.7128, "lon": -74.0060}, "end": {"lat": 40.7589, "lon": -73.9851}}' \
  "https://api.getcamino.ai/relationship"
```

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| start | object | Yes | Starting point with lat/lon |
| end | object | Yes | Ending point with lat/lon |
| include | array | No | What to include: distance, direction, travel_time, description |

## Response Format

```json
{
  "distance": {
    "meters": 5420,
    "kilometers": 5.42,
    "miles": 3.37
  },
  "direction": {
    "bearing": 42,
    "cardinal": "NE",
    "description": "northeast"
  },
  "travel_time": {
    "walking_minutes": 68,
    "driving_minutes": 15,
    "cycling_minutes": 22
  },
  "description": "5.4 km northeast, about 15 minutes by car"
}
```

## Examples

### Simple distance check
```bash
./scripts/relationship.sh '{
  "start": {"lat": 51.5074, "lon": -0.1278},
  "end": {"lat": 48.8566, "lon": 2.3522}
}'
```

### Get only distance and direction
```bash
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction"]
}'
```

## Use Cases

- **Proximity checks**: Determine if two locations are within a certain distance
- **Direction guidance**: Provide cardinal direction context (north, southeast, etc.)
- **Travel planning**: Estimate travel times for different transport modes
- **Location context**: Generate human-readable descriptions of spatial relationships
