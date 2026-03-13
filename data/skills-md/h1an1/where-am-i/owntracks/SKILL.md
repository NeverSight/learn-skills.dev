---
name: owntracks
description: Receive and query GPS location from OwnTracks iOS/Android app via a lightweight HTTP server. Supports named places (home, office, gym), semantic location queries, and location history. Use when the user asks about location tracking, "where am I", GPS awareness, geofencing, or setting up OwnTracks. Triggers on "owntracks", "location", "GPS", "where am I", "位置".
---

# OwnTracks Location Receiver

Give your AI agent GPS awareness. Zero dependencies, one Node.js file.

## Architecture

```
OwnTracks app → (HTTPS via Cloudflare Tunnel) → server.mjs → data/
                                                         ├── current-location.json
                                                         └── location-log.jsonl
```

## Setup

### 1. Start the receiver

```bash
AUTH_USER=yi AUTH_SECRET=$(openssl rand -base64 24) node scripts/server.mjs
# Default port 8073. Override with PORT=9090
```

Without `AUTH_SECRET`, the server runs open (fine for localhost, not for public URLs).

### 2. Expose via tunnel (if behind NAT)

Pick one:

| | **ngrok** | **Cloudflare Tunnel** |
|---|---|---|
| Setup | One command | Needs domain + DNS config |
| URL | Random subdomain (changes on restart) | Fixed custom domain |
| Best for | Quick testing, no domain | Production, permanent setup |
| China | Works but unstable | Use `--protocol http2` (QUIC blocked) |

**Option A: ngrok (quick start)**

```bash
ngrok http 8073
# Copy the https://xxx.ngrok-free.app URL to OwnTracks
```

**Option B: Cloudflare Tunnel (permanent)**

```bash
# One-time setup
brew install cloudflared
cloudflared tunnel login
cloudflared tunnel create owntracks
cloudflared tunnel route dns owntracks gps.yourdomain.com

# Create ~/.cloudflared/config.yml:
# tunnel: <tunnel-id>
# credentials-file: ~/.cloudflared/<tunnel-id>.json
# ingress:
#   - hostname: gps.yourdomain.com
#     service: http://localhost:8073
#   - service: http_status:404

# Run (use --protocol http2 in China where QUIC is blocked)
cloudflared tunnel run owntracks
```

Tip: set up as a launchd service for auto-start on boot.

### 3. Configure OwnTracks app

- **Mode:** HTTP
- **URL:** Your tunnel URL (ngrok URL or `https://gps.yourdomain.com/`)
- **Authentication:** Username + password (matching AUTH_USER / AUTH_SECRET)
- **Monitoring:** Significant (battery-friendly) or Move (precise tracking)

⚠️ OwnTracks may add trailing spaces when pasting passwords. The server trims automatically.

## Named Places

Copy and edit the example:
```bash
cp scripts/places.example.json places.json
# Edit places.json with your locations
```

Format:
```json
{
  "places": [
    { "name": "home", "label": "Home", "lat": 37.775, "lon": -122.419, "radius": 200 },
    { "name": "office", "label": "Office", "lat": 37.790, "lon": -122.389, "radius": 300 }
  ]
}
```

With places configured, queries return semantic locations ("At 家") instead of raw coordinates.

## Querying Location

```bash
# Current location + nearest place
node scripts/query.mjs

# JSON output (for programmatic use)
node scripts/query.mjs --json

# Last N locations
node scripts/query.mjs --history 5

# Locations from a specific date
node scripts/query.mjs --at 2026-03-10

# List configured places
node scripts/query.mjs --places
```

### Direct file access
```bash
cat data/current-location.json          # latest location
tail -5 data/location-log.jsonl         # recent history
```

### Location fields
`lat`, `lon`, `alt`, `acc` (meters), `vel` (km/h), `batt` (%), `conn` (w=wifi, m=mobile), `tid`, `tst` (epoch), `timestamp` (ISO), `receivedAt` (ISO).

## Use Cases for Agents

- **Context awareness:** "You're still at the office at 11pm — time to head home?"
- **Proactive help:** Detect arrival at airport → check flight status
- **Smart home:** Detect "at home" → trigger automations
- **Daily journaling:** Log places visited with timestamps
- **Safety:** Alert if no location update for extended period

## Nearby Search (AMap/高德)

Requires `AMAP_API_KEY` env var. Get a free key at https://lbs.amap.com

### Coordinate System (China users)

AMap requires GCJ-02 coordinates. iOS CoreLocation returns **WGS-84** (the GPS standard), and the `nearby.mjs` script includes a built-in WGS-84 → GCJ-02 converter (default: `COORD_SYSTEM=wgs84`). If your device already provides GCJ-02, set `COORD_SYSTEM=gcj02` to skip conversion:

```bash
# iOS / standard GPS devices (default, auto-converts WGS→GCJ)
node scripts/nearby.mjs "咖啡"

# If your device already reports GCJ-02
COORD_SYSTEM=gcj02 node scripts/nearby.mjs "咖啡"
```

```bash
# Auto-uses current GPS location
node scripts/nearby.mjs "咖啡"

# Custom radius and explicit coordinates
node scripts/nearby.mjs "餐厅" --radius 1000 --lat 37.775 --lng -122.419

# JSON output for programmatic use
node scripts/nearby.mjs "药店" --json

# Limit results
node scripts/nearby.mjs "便利店" --limit 5
```

Combines with GPS: if OwnTracks is running, nearby search auto-detects your location. No need to pass coordinates.

**Use cases:** restaurants, cafes, pharmacies, hospitals, transit, gyms — anything in AMap's POI database (excellent coverage in China).

## Files

- `scripts/server.mjs` — HTTP receiver (zero deps)
- `scripts/query.mjs` — CLI query tool (zero deps)
- `scripts/nearby.mjs` — AMap nearby POI search (zero deps, needs AMAP_API_KEY)
- `scripts/gps-inject.sh` — Injects GPS status into HEARTBEAT.md (for agent context)
- `scripts/places.example.json` — Example places config
- `places.json` — Your places config (create from example, gitignored)
- `data/` — Location data (created automatically, gitignored)

## Heartbeat Integration (Agent GPS Awareness)

The key challenge: an agent's heartbeat reads HEARTBEAT.md, but may skip instructions inside it. The solution is **code-level injection** — a shell script writes GPS status directly into HEARTBEAT.md so the data is already in the agent's system prompt.

### How it works

```
launchd (every 2 min) → gps-inject.sh → reads GPS data → writes to HEARTBEAT.md header
                                                          ↓
                                         Agent heartbeat reads HEARTBEAT.md
                                         GPS data is already in system prompt
                                         Agent can't "forget" to check GPS
```

### Setup

1. Copy and edit `scripts/gps-inject.sh`:
   - Set `GPS_FILE` to your `data/current-location.json` path
   - Set `HEARTBEAT` to your agent's `HEARTBEAT.md` path
   - Create a `known-places.json` with your named locations (see format below)

2. Create a launchd plist (macOS) or cron entry:

```xml
<!-- ~/Library/LaunchAgents/com.agent.gps-inject.plist -->
<plist version="1.0">
<dict>
    <key>Label</key><string>com.agent.gps-inject</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/scripts/gps-inject.sh</string>
    </array>
    <key>StartInterval</key><integer>120</integer>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
```

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.agent.gps-inject.plist
```

3. Your HEARTBEAT.md will automatically show:
```
<!-- GPS_START -->
> 📍 User at Home | Updated 09:53 (1 min ago) | 🔋85% WiFi | Accuracy 7m
<!-- GPS_END -->
```

### Known places format

```json
[
  {"name": "Home", "lat": 40.033, "lon": 116.417, "radius": 0.003},
  {"name": "Office", "lat": 40.052, "lon": 116.294, "radius": 0.003}
]
```

Use coordinates from your actual GPS data (same coordinate system). For unknown locations, the script falls back to OSM Nominatim reverse geocoding (WGS-84, free, no API key).

### Why this pattern matters

Text-level instructions ("check GPS every heartbeat") are unreliable — agents read them but may not execute. Code-level injection bypasses the agent's decision-making entirely: the data is in the prompt whether the agent "remembers" to check or not. This is a general pattern: **if an agent must see something, inject it into context; don't ask the agent to go look.**
