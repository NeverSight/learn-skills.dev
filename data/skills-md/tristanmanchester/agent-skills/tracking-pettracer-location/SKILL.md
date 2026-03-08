---
name: tracking-pettracer-location
description: >-
  Tracks PetTracer (pettracer.com) GPS collars via the PetTracer portal API: fetches a pet’s latest location,
  location history, and optionally streams updates via the PetTracer WebSocket (SockJS/STOMP).
  Use when the user asks “where is my pet/cat”, “track my PetTracer”, wants GPS coordinates/history,
  or needs help with PetTracer authentication tokens or live tracking.
---

# Tracking PetTracer pet location

## Why this exists

PetTracer exposes an (unofficial) web portal API used by their apps/website. This skill gives a reliable, low-drama workflow for:
- **Current location** (latest known point)
- **Recent route/history** (time-windowed points)
- **Near-real-time updates** (WebSocket push, optional)

It is designed to minimise API load (be respectful) and to produce **consistent, copy/paste-friendly outputs**.

## Quick start

### Snapshot location (recommended default)
1. Set credentials (prefer env vars, not CLI args):

```bash
export PETTRACER_USERNAME="you@example.com"
export PETTRACER_PASSWORD="••••••••"
```

2. List devices:

```bash
python scripts/pettracer_cli.py list --format json --pretty
```

3. Locate a pet:

- By name:
```bash
python scripts/pettracer_cli.py locate --pet "Fluffy" --format json --pretty
```

- By id:
```bash
python scripts/pettracer_cli.py locate --device-id 12345 --format json --pretty
```

- If the account has **exactly one collar**, you can omit `--pet/--device-id`:
```bash
python scripts/pettracer_cli.py locate --format json --pretty
```

### Get location history (last 6 hours)
```bash
python scripts/pettracer_cli.py history --pet "Fluffy" --hours 6 --format json --pretty
```

## Core workflow the agent should follow

### 1) Decide: snapshot vs history vs live updates
- **Snapshot**: user asks “where is X right now?” → use `locate`.
- **History**: user asks “where has X been today/last hour?” → use `history`.
- **Live**: user wants continuous updates → use WebSocket (see [references/websocket.md](references/websocket.md)).

Default to **snapshot** unless the user explicitly wants a route or live tracking.

### 2) Authenticate safely
Preferred order:
1. Use `PETTRACER_TOKEN` if already available.
2. Else login with `PETTRACER_USERNAME` + `PETTRACER_PASSWORD` (or `PETTRACER_EMAIL`).

**Never** ask the user to paste tokens into chat. Ask them to set env vars or store secrets in their vault.

Optional overrides (useful for debugging / future-proofing):
- `PETTRACER_API_BASE` (REST base; default `https://portal.pettracer.com/api`)
- `PETTRACER_WS_BASE` (WebSocket base; default `wss://pt.pettracer.com/sc`)

### 3) Identify the right device
- Fetch devices via `GET /api/map/getccs` (wrapped by `pettracer_cli.py list`).
- Match by `details.name` case-insensitively.
- If multiple matches: show a disambiguation list (id + name) and ask the user which one.
- If no match: show available device names.
- If the account has exactly one collar, you can default to it.

### 4) Fetch location data
- **Current location** comes from `device.lastPos` (collars) or top-level `posLat/posLong` (HomeStations):
  - `posLat`, `posLong`
  - `timeMeasure` (timestamp)
  - `acc` (accuracy, metres) or `horiPrec` (fallback)
- **History** uses `POST /api/map/getccpositions` with:
  - `devId`, `filterTime` (ms), `toTime` (ms)

See [references/endpoints.md](references/endpoints.md) and [references/data-model.md](references/data-model.md).

### 5) Present results consistently
When reporting location, include:
- Pet name + device id
- Coordinates (lat, lon)
- Last update time
- Accuracy (if present)
- How old the fix is (seconds/minutes since last fix), if possible
- Optional: a map link (Google Maps + OpenStreetMap)

**Preferred JSON shape (for tool-to-tool handoff):**
```json
{
  "pet": { "id": 12345, "name": "Fluffy" },
  "last_fix": {
    "lat": 48.137154,
    "lon": 11.576124,
    "time": "2026-02-25T12:34:56+00:00",
    "accuracy_m": 12
  },
  "last_fix_age_s": 90,
  "battery_mv": 4012,
  "battery_percent_est": 78,
  "home": false,
  "links": {
    "google_maps": "https://www.google.com/maps?q=48.137154,11.576124",
    "openstreetmap": "https://www.openstreetmap.org/?mlat=48.137154&mlon=11.576124#map=18/48.137154/11.576124"
  }
}
```

Notes:
- `battery_percent_est` is an **estimate** derived from voltage (PetTracer reports millivolts, not %).
- If there’s no GPS fix, report `error=no_recent_fix` and include `last_contact`.

## Live tracking (optional, avoid aggressive polling)

If you need frequent updates:
- Prefer WebSocket push (avoid aggressive polling).
- Only fall back to polling if WebSocket is not possible; keep polling ≥ 60s by default.

Install dependency:
```bash
pip install aiohttp
```

Then run:
```bash
python scripts/pettracer_watch.py --pet "Fluffy"
```

See:
- [references/websocket.md](references/websocket.md)
- `scripts/pettracer_watch.py` for a working SockJS/STOMP implementation.

## Troubleshooting playbook

### No location / `lastPos` is missing
Common reasons:
- Collar hasn’t reported a GPS fix recently (indoors, low signal).
- Battery low / collar off.
- Subscription expired.

Action:
- Report “no recent fix” and show `lastContact` if available.
- Suggest switching to a higher-frequency mode (Fast/Live) in the PetTracer app/portal **only if the user asks** (see [references/modes.md](references/modes.md)).

### Auth failures (401 / invalid_auth)
- Re-login to obtain a fresh `access_token`.
- Confirm the login payload uses keys `login` + `password` (not `username`).

### Rate limiting / service respect
- Avoid tight loops against `/map/getccs`.
- Prefer WebSocket for near-real-time tracking.

## THE EXACT PROMPT — Location response format

Use this when the user wants a human-readable answer:

```
Give the pet’s latest known PetTracer location.

Include:
- Pet name + device id
- Time of last fix (and last contact if different)
- Coordinates + map link(s)
- Accuracy (metres) if present
- One-line assessment: “recent fix” vs “stale fix” (use last_fix_age_s if available; interpret in the context of the current tracking mode)
```
