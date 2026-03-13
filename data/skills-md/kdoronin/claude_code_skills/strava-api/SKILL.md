---
name: strava-api
description: Universal Strava API integration for fitness data management. Use when working with Strava activities, athlete profiles, segments, routes, clubs, or any fitness tracking data. Triggers on requests to get/create/update activities, analyze training stats, export routes, explore segments, or interact with Strava data programmatically.
---

# Strava API

Direct integration with Strava API v3 for fitness data management.

## Security Model

**IMPORTANT**: All secrets are stored in system keychain (macOS Keychain / Linux Secret Service).

- AI agents **CANNOT** read secrets from keychain
- Only the Python scripts can access credentials at runtime
- Non-secret metadata (athlete name, token expiry) stored in `~/.strava/metadata.json`

This design ensures your API credentials are never exposed to AI agents.

---

## First-Time Setup Workflow

When user requests Strava data for the first time:

### Step 1: Check if configured

```bash
python3 scripts/strava_api.py athlete
```

If error "Strava not configured" → proceed to Step 2.
If success → skip to "Using the API" section.

### Step 2: Create Strava Application

Guide user to create API application:

1. Open https://www.strava.com/settings/api
2. Fill application form:
   - **Application Name**: Any name (e.g., "My Fitness App")
   - **Category**: Choose any
   - **Website**: `http://localhost`
   - **Authorization Callback Domain**: `localhost`
3. Note **Client ID** and **Client Secret** (will be entered in setup)

### Step 3: Run Interactive Setup

```bash
python3 scripts/setup_oauth.py
```

Script will:
1. Ask for Client ID and Client Secret (secret input hidden)
2. Open browser for Strava authorization
3. Guide user to copy redirect URL
4. Exchange code for tokens automatically
5. Store secrets in system keychain (secure)
6. Store metadata in `~/.strava/metadata.json`
7. Verify connection

### Step 4: Verify Setup

```bash
python3 scripts/strava_api.py athlete
```

Should display athlete profile JSON.

---

## Using the API

### CLI Commands

```bash
# Get athlete profile
python3 scripts/strava_api.py athlete

# Get athlete stats
python3 scripts/strava_api.py stats

# List recent activities
python3 scripts/strava_api.py activities --limit 20

# Get specific activity
python3 scripts/strava_api.py activity 12345678

# Explore segments in area
python3 scripts/strava_api.py segments "37.7,-122.5,37.8,-122.4" --type running

# Raw API request
python3 scripts/strava_api.py raw GET /athlete/zones
python3 scripts/strava_api.py raw POST /activities --data '{"name":"Test","sport_type":"Run","start_date_local":"2024-01-15T10:00:00Z","elapsed_time":1800}'
```

### Python Import

```python
from scripts.strava_api import StravaClient

client = StravaClient()  # Auto-loads from keychain, refreshes token if needed

# Get athlete
athlete = client.get_athlete()

# List activities
activities = client.list_activities(per_page=50)

# Create activity
new_activity = client.create_activity(
    name="Morning Run",
    sport_type="Run",
    start_date_local="2024-01-15T07:30:00Z",
    elapsed_time=1800,
    distance=5000
)
```

### Token Management

Tokens refresh automatically. Check status:

```bash
# Check token status
python3 scripts/refresh_token.py --status

# Force refresh
python3 scripts/refresh_token.py --force
```

---

## Decision Tree

```
User Request
├── First time / "setup strava" → Run setup_oauth.py
├── "Get my profile/stats" → strava_api.py athlete/stats
├── "List my activities" → strava_api.py activities
├── "Get activity details" → strava_api.py activity {id}
├── "Create/log activity" → client.create_activity()
├── "Update activity" → client.update_activity()
├── "Get training data/streams" → client.get_activity_streams()
├── "Find segments nearby" → strava_api.py segments {bounds}
├── "Export route" → raw GET /routes/{id}/export_gpx
└── "Token expired" → Auto-handled by client
```

---

## Quick Reference

| Item | Value |
|------|-------|
| Secrets storage | System Keychain (secure) |
| Metadata location | `~/.strava/metadata.json` |
| Base URL | `https://www.strava.com/api/v3` |
| Rate limits | 100 req/15min, 1000 req/day |
| Token lifetime | 6 hours (auto-refresh) |

**References**:
- Full API docs: [references/api_reference.md](references/api_reference.md)
- Manual setup: [references/setup_guide.md](references/setup_guide.md)

## Sport Types

- **Running**: `Run`, `TrailRun`, `VirtualRun`
- **Cycling**: `Ride`, `MountainBikeRide`, `GravelRide`, `EBikeRide`
- **Other**: `Swim`, `Walk`, `Hike`, `Workout`, `WeightTraining`, `Yoga`

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Token expired | Auto-handled by client |
| 403 | Insufficient scope | Re-run setup_oauth.py |
| 404 | Resource not found | Check ID |
| 429 | Rate limit | Wait 15 min |
