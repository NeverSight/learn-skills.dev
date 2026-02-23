---
name: safety-checker
description: "Find 24-hour businesses, well-lit public areas, transit stations, police stations, and hospitals near any location for late night safety awareness."
metadata: {"clawdbot":{"emoji":"🔦","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## Installation

**Companion Skills**: This is part of the Camino AI location intelligence suite. Install all available skills (query, places, relationship, context, route, journey, real-estate, hotel-finder, ev-charger, school-finder, parking-finder, fitness-finder, safety-checker, travel-planner) for comprehensive coverage.

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill safety-checker
```

**Via clawhub:**
```bash
npx clawhub@latest install safety-checker
# or: pnpm dlx clawhub@latest install safety-checker
# or: bunx clawhub@latest install safety-checker
```

# Late Night Safety

Find 24-hour businesses, well-lit public areas, transit stations, police stations, and hospitals near any location. Provides safety-focused context awareness for late night situations.

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
# Check safety resources near a location
./scripts/safety-checker.sh '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500}'

# Check with larger radius
./scripts/safety-checker.sh '{"location": {"lat": 37.7749, "lon": -122.4194}, "radius": 800}'
```

### Via curl

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500, "context": "late night safety: 24-hour businesses, transit, police, hospitals"}' \
  "https://api.getcamino.ai/context"
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| location | object | Yes | - | Coordinate with lat/lon |
| radius | int | No | 500 | Search radius in meters |

## Response Format

```json
{
  "area_description": "Busy commercial area in Midtown Manhattan with 24-hour businesses...",
  "relevant_places": {
    "hospitals": [...],
    "police": [...],
    "transit": [...],
    "24_hour_businesses": [...],
    "pharmacies": [...]
  },
  "location": {"lat": 40.7506, "lon": -73.9935},
  "search_radius": 500,
  "total_places_found": 34,
  "context_insights": "This area has good late-night safety resources including..."
}
```

## Examples

### Check safety near a hotel at night
```bash
./scripts/safety-checker.sh '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500}'
```

### Check safety in an unfamiliar neighborhood
```bash
./scripts/safety-checker.sh '{"location": {"lat": 34.0407, "lon": -118.2468}, "radius": 600}'
```

### Check safety near a transit stop
```bash
./scripts/safety-checker.sh '{"location": {"lat": 41.8827, "lon": -87.6233}, "radius": 400}'
```

## Use Cases

- **Late night arrivals**: Check what safety resources are near your hotel or Airbnb
- **Walking at night**: Identify well-lit areas, open businesses, and emergency services along your path
- **Travel safety**: Assess unfamiliar neighborhoods before visiting at night
- **Emergency awareness**: Know where the nearest hospital and police station are located
- **Transit safety**: Check what resources are near transit stops you'll be using late at night
