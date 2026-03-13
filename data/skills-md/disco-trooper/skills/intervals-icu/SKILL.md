---
name: intervals-icu
description: Intervals.icu API for wellness, activities, power curves, and fitness metrics.
license: MIT
metadata:
  author: disco-trooper
  version: "1.0.0"
---

# Intervals.icu API Skill

## Skill Relationship

```
┌─────────────────┐     fetch data      ┌───────────────────┐
│  intervals-icu  │ ──────────────────► │ cycling-training  │
│   (DATA API)    │                     │    (ANALYSIS)     │
│                 │ ◄────────────────── │                   │
│ • wellness      │   interpret results │ • zone calc       │
│ • activities    │                     │ • periodization   │
│ • power curves  │                     │ • workout design  │
│ • fitness       │                     │ • load management │
└─────────────────┘                     └───────────────────┘
```

**Usage pattern:**
1. Use `intervals-icu` to fetch data from API
2. Use `cycling-training` to analyze and interpret
3. Use `intervals-icu` to update wellness/events

API wrapper for intervals.icu cycling training platform. Designed to work alongside the `cycling-training` skill.

## Quick Start

```bash
# Set credentials (one-time)
export INTERVALS_API_KEY="your_api_key"
export INTERVALS_ATHLETE_ID="iXXXXX"

# Use the API helper
~/.claude/skills/intervals-icu/scripts/api.sh wellness today
~/.claude/skills/intervals-icu/scripts/api.sh activities 2024-01-01 2024-01-31
```

## Authentication

Get your API key from https://intervals.icu/settings → Developer Settings → API Key.

Find athlete ID in the URL when logged in: `intervals.icu/athlete/iXXXXX/...`

## Rate Limiting

Intervals.icu API has rate limits. The script handles this with:
- Automatic retry with exponential backoff (default: 3 attempts)
- Configurable via `INTERVALS_MAX_RETRIES` environment variable

```bash
# Increase retries for bulk operations
export INTERVALS_MAX_RETRIES=5
```

If you hit rate limits frequently:
- Add delays between bulk requests: `sleep 1`
- Use date ranges instead of individual requests
- Cache responses locally for analysis

## Prerequisites

- **curl** - Pre-installed on most systems
- **jq** - `brew install jq` (macOS) / `apt install jq` (Linux)
- **bats-core** - Optional, for tests: `brew install bats-core`

## API Helper Script

Use `scripts/api.sh` to handle authentication and common operations:

| Command | Description |
|---------|-------------|
| `api.sh wellness [date]` | Get wellness for date (default: today) |
| `api.sh wellness-range <start> <end>` | Get wellness for date range |
| `api.sh wellness-update <date> <json>` | Update wellness fields |
| `api.sh activities <start> <end> [format] [--all]` | List activities (--all for pagination) |
| `api.sh activity <id>` | Get single activity details |
| `api.sh activity-streams <id> [types]` | Get activity data streams |
| `api.sh activity-upload <file>` | Upload activity (.fit, .gpx, .tcx) |
| `api.sh athlete` | Get athlete profile |
| `api.sh fitness` | Get current CTL/ATL/TSB |
| `api.sh zones` | Get power/HR zone settings |
| `api.sh events <start> <end>` | Get planned events/workouts |
| `api.sh event-create <date> <json>` | Create planned workout/event |
| `api.sh power-curves <start> <end> [format]` | Power curves (json/summary/seconds) |

### Examples

```bash
# Get today's wellness
~/.claude/skills/intervals-icu/scripts/api.sh wellness

# Get wellness for specific date
~/.claude/skills/intervals-icu/scripts/api.sh wellness 2024-01-15

# Update wellness (weight and sleep)
~/.claude/skills/intervals-icu/scripts/api.sh wellness-update 2024-01-15 '{"weight": 72.5, "sleepSecs": 28800}'

# Get last month's activities
~/.claude/skills/intervals-icu/scripts/api.sh activities 2024-01-01 2024-01-31

# Export activities as CSV
~/.claude/skills/intervals-icu/scripts/api.sh activities 2024-01-01 2024-01-31 csv > activities.csv
```

## Direct curl Examples

For custom operations not covered by the helper:

```bash
# Base URL
BASE="https://intervals.icu/api/v1"

# Auth header
AUTH="Authorization: Basic $(echo -n "API_KEY:$INTERVALS_API_KEY" | base64)"

# Get power curve
curl -s -H "$AUTH" "$BASE/athlete/$INTERVALS_ATHLETE_ID/power-curves?oldest=2024-01-01&newest=2024-12-31"

# Get streams for activity
curl -s -H "$AUTH" "$BASE/activity/iXXXX/streams?types=watts,heartrate,cadence"

# Upload activity
curl -s -H "$AUTH" -F "file=@ride.fit" "$BASE/athlete/$INTERVALS_ATHLETE_ID/activities"
```

## Key Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/athlete/{id}` | GET | Athlete profile |
| `/athlete/{id}/wellness/{date}` | GET/PUT | Wellness data |
| `/athlete/{id}/wellness` | GET | Wellness range (add `?oldest=&newest=`) |
| `/athlete/{id}/activities` | GET | Activities list |
| `/activity/{id}` | GET | Activity details |
| `/activity/{id}/streams` | GET | Activity data streams |
| `/athlete/{id}/events` | GET | Planned workouts/events |
| `/athlete/{id}/power-curves` | GET | Power duration curves |

## Wellness Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `weight` | float | 30-200 kg | Body weight |
| `restingHR` | int | 30-100 bpm | Resting heart rate |
| `hrv` | float | 10-150 ms | HRV RMSSD (typical: 20-80) |
| `hrvSDNN` | float | 10-200 ms | HRV SDNN |
| `sleepSecs` | int | 0-43200 | Sleep duration (0-12h in seconds) |
| `sleepScore` | float | 0-100 | Sleep quality percentage |
| `sleepQuality` | int | 1-5 | 1=poor, 5=excellent |
| `fatigue` | int | 1-5 | 1=fresh, 5=exhausted |
| `mood` | int | 1-5 | 1=bad, 5=great |
| `motivation` | int | 1-5 | Training motivation |
| `readiness` | int | 1-5 | Training readiness |
| `stress` | int | 1-5 | Stress level |
| `soreness` | int | 1-5 | Muscle soreness |
| `ctl` | float | 0-200 | Chronic Training Load (fitness) |
| `atl` | float | 0-300 | Acute Training Load (fatigue) |
| `rampRate` | float | -10 to +10 | CTL weekly change rate

## Integrate with cycling-training

Use both skills together:

1. **Fetch data** with intervals-icu skill:
   ```bash
   ~/.claude/skills/intervals-icu/scripts/api.sh wellness-range 2024-01-01 2024-01-31 > wellness.json
   ~/.claude/skills/intervals-icu/scripts/api.sh activities 2024-01-01 2024-01-31 > activities.json
   ```

2. **Analyze** with cycling-training skill:
   - Calculate training load distribution
   - Check polarization index
   - Evaluate recovery status based on HRV trends
   - Plan next mesocycle based on CTL/ATL/TSB

3. **Update wellness** after morning check-in:
   ```bash
   ~/.claude/skills/intervals-icu/scripts/api.sh wellness-update today '{"weight": 72.5, "sleepSecs": 28800, "readiness": 4}'
   ```

## End-to-End Workflow Example

Complete example: Morning HRV-based workout adjustment using both skills.

### Scenario
You wake up, check HRV, and want to adjust today's planned workout based on recovery status.

### Step 1: Fetch morning wellness data
```bash
# Get today's wellness (HRV from device sync)
WELLNESS=$(~/.claude/skills/intervals-icu/scripts/api.sh wellness today)
echo "$WELLNESS" | jq '{hrv, restingHR, sleepSecs, ctl, atl}'
```

Output:
```json
{
  "hrv": 42.5,
  "restingHR": 54,
  "sleepSecs": 25200,
  "ctl": 65.3,
  "atl": 72.1
}
```

### Step 2: Analyze with cycling-training skill

Based on the data:
- **HRV**: 42.5 ms (below your baseline of 50 ms = -15%)
- **TSB**: 65.3 - 72.1 = -6.8 (slightly fatigued)
- **Sleep**: 7 hours (adequate but not optimal)

**cycling-training recommendation**: Reduce intensity. Convert threshold workout to endurance/recovery.

### Step 3: Update today's planned event

```bash
# Find today's planned workout
TODAY=$(date +%Y-%m-%d)
EVENTS=$(~/.claude/skills/intervals-icu/scripts/api.sh events $TODAY $TODAY)
EVENT_ID=$(echo "$EVENTS" | jq -r '.[0].id')

# Update to easier workout
~/.claude/skills/intervals-icu/scripts/api.sh event-update "$EVENT_ID" '{
  "name": "Recovery Ride (HRV adjusted)",
  "description": "Original: Threshold intervals. Adjusted due to low HRV (-15% from baseline).",
  "icu_training_load": 40
}'
```

### Step 4: Log subjective wellness

```bash
~/.claude/skills/intervals-icu/scripts/api.sh wellness-update today '{
  "readiness": 3,
  "fatigue": 3,
  "mood": 4,
  "soreness": 2
}'
```

### Decision Matrix

| HRV vs Baseline | TSB | Recommendation |
|-----------------|-----|----------------|
| >+10% | >0 | Execute as planned or add intensity |
| ±10% | >0 | Execute as planned |
| ±10% | <0 | Execute but monitor |
| <-10% | Any | Reduce intensity or rest |
| <-20% | Any | Rest day |

## Testing

Run the test suite:

```bash
# Requires: bats-core
# Install: brew install bats-core (macOS) or apt install bats (Linux)

~/.claude/skills/intervals-icu/tests/run_tests.sh
```

Tests verify:
- Help and argument validation
- Environment variable checks
- Date parsing (cross-platform)
- JSON parsing with mock fixtures
- Power curve calculations

## Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| HTTP 401 | Invalid API key | Regenerate key in settings |
| HTTP 403 | No permission | Check athlete ID ownership |
| HTTP 404 | Resource not found | Verify date format (YYYY-MM-DD) |
| HTTP 429 | Rate limited | Wait 60s, reduce request frequency |
| "jq: command not found" | jq not installed | `brew install jq` (macOS) / `apt install jq` (Linux) |
| Empty response | No data for date range | Check date range contains activities |
| "Invalid JSON" | Malformed JSON payload | Validate JSON: `echo '{"key": "value"}' | jq .` |

### Debug Mode

Enable verbose output for debugging:

```bash
# Show curl commands
export INTERVALS_DEBUG=1
~/.claude/skills/intervals-icu/scripts/api.sh wellness today
```

### Common Issues

**Issue: Activities not syncing from Garmin/Wahoo**
- Check device sync in intervals.icu settings
- Verify connection status with fitness platform
- Manual upload: `api.sh activity-upload ride.fit`

**Issue: HRV not appearing in wellness**
- HRV requires compatible device (Garmin, Wahoo, Oura, etc.)
- Check device sync completed before fetching
- Some devices sync HRV with delay (up to 2 hours)

**Issue: Power curves show 0 for some durations**
- Need activity with sustained effort at that duration
- Indoor trainers may have gaps in data
- Check activity streams: `api.sh activity-streams <id> watts`

**Issue: CSV export has wrong encoding**
- Intervals.icu returns UTF-8
- If Excel shows garbled text: Import as UTF-8, not auto-detect

### Undocumented Endpoints

For endpoints not covered by api.sh, use Context7:

```javascript
// Find Intervals.icu docs
mcp__plugin_context7_context7__resolve-library-id({
  libraryName: "intervals.icu"
})

// Query specific endpoint
mcp__plugin_context7_context7__query-docs({
  libraryId: "/websites/intervals_icu_api_v1",
  query: "how to create workout library entry"
})
```

## Common Workflows

### Morning Wellness Check-in
```bash
# Get HRV device data (if synced)
~/.claude/skills/intervals-icu/scripts/api.sh wellness today

# Update subjective metrics
~/.claude/skills/intervals-icu/scripts/api.sh wellness-update today '{"readiness": 4, "mood": 4, "soreness": 2}'
```

### Weekly Training Review
```bash
# Get last 7 days
END=$(date +%Y-%m-%d)
START=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)

~/.claude/skills/intervals-icu/scripts/api.sh activities $START $END
~/.claude/skills/intervals-icu/scripts/api.sh wellness-range $START $END
~/.claude/skills/intervals-icu/scripts/api.sh fitness  # Current CTL/ATL/TSB
```

### Export for Analysis
```bash
# CSV export for spreadsheet analysis
~/.claude/skills/intervals-icu/scripts/api.sh activities 2024-01-01 2024-12-31 csv > yearly_activities.csv
~/.claude/skills/intervals-icu/scripts/api.sh wellness-range 2024-01-01 2024-12-31 csv > yearly_wellness.csv
```
