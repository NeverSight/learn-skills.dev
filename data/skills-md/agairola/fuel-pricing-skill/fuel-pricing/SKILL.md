---
name: fuel-pricing
description: >-
  Find the cheapest fuel prices near the user's current location in Australia.
  Use this skill whenever the user asks about fuel prices, petrol prices, gas
  station prices, servo prices, cheapest fuel, diesel prices, E10 prices, or
  wants to compare fuel costs nearby. Also trigger when the user mentions filling
  up, refueling, or asks "where should I get fuel/petrol/diesel". Works across
  all Australian states with zero configuration — no API keys needed. Works in
  any environment — Telegram, WhatsApp, Signal, Discord, terminal, or any chat
  platform.
---

# Fuel Pricing Skill

Find the cheapest fuel at nearby stations across Australia. Zero config — no API keys, no setup.

## When to Use

Trigger this skill when the user:

- Asks about fuel, petrol, diesel, or gas prices
- Wants to compare prices at nearby stations
- Mentions filling up, refueling, or finding a servo
- Asks "where should I get fuel/petrol/diesel?"
- Mentions a specific fuel type (E10, U91, U95, U98, diesel, LPG)

## Prerequisites

- **uv** — `brew install uv` (macOS) or `pip install uv` (all platforms)
- **API keys** — not needed. Optional: FuelCheck keys in `~/.config/fuel-pricing/credentials.json` for official NSW govt data.
- **Dependencies** — declared inline (PEP 723), installed automatically by `uv run`.

## Setup Status

!`command -v uv > /dev/null 2>&1 && echo "uv: installed" || echo "uv: NOT INSTALLED"`
!`test -f ~/.config/fuel-pricing/credentials.json && python3 -c "import json; d=json.load(open('$HOME/.config/fuel-pricing/credentials.json')); print('FuelCheck API: configured' if d.get('fuelcheck_key') else 'FuelCheck API: not configured')" 2>/dev/null || echo "FuelCheck API: not configured (using community data — may be stale)"`

## Location Flow (IMPORTANT — follow this exactly)

Before fetching prices, you MUST resolve the user's location. Follow these steps in order — do NOT skip ahead to IP fallback.

**Step 1: Check what the user already provided.**
- User shared a location pin (Telegram, WhatsApp, Signal, Discord)? Extract lat/lng → use `--lat` / `--lng`. Done.
- User mentioned a suburb, city, or address? → use `--location`. Done.
- User mentioned a postcode? → use `--postcode`. Done.

**Step 2: User said "near me" or "nearby" but gave no location.**
Ask them to share location. Tailor the ask to their platform:
- Telegram: "Tap the paperclip icon → Location → Send My Current Location"
- WhatsApp: "Tap the + button → Location → Send Your Current Location"
- Signal: "Tap the + button → Location"
- Discord/terminal: "What suburb or postcode are you near?"

Wait for their response. Do not proceed without it.

**Step 3: User can't or won't share location.**
Ask: "No worries — what suburb or postcode are you near?" Wait for response.

**Step 4: User refuses to give any location info.**
Only now fall back to auto-detect (no location args). This uses IP geolocation which is city-level only and often wrong. If the result comes back with `confidence: "low"`, tell the user: "I got an approximate location of [city] from your IP but it may not be accurate. Can you tell me your suburb or postcode for better results?"

**Never silently use IP geolocation when you can ask the user instead.**

### Command Template

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py" [LOCATION_FLAGS] [OPTIONS]
```

### Options

| Flag | Values | Default | Purpose |
|------|--------|---------|---------|
| `--fuel-type` | `E10` `U91` `U95` `U98` `DSL` `PDSL` `LPG` | `U91` | Fuel type to search |
| `--radius` | km (integer) | `5` | Search radius |
| `--no-cache` | *(flag)* | off | Force fresh data |

Only parse **stdout** (JSON). Stderr contains diagnostics only.

### Common Commands

```bash
# User shared location via chat platform
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py" --lat -34.07 --lng 150.74

# User mentioned a place or postcode
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py" --location "Newtown, NSW"
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py" --postcode 2042

# Auto-detect location (terminal — opens browser on first run)
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py"

# Specific fuel type + wider radius
uv run "${CLAUDE_SKILL_DIR}/scripts/fuel_prices.py" --location "Parramatta" --fuel-type E10 --radius 10
```

## Presenting Results

DO NOT use markdown tables. They don't render on mobile chat platforms (Telegram, WhatsApp, Signal). Use plain text with line breaks instead.

### Map Links

Each station in the JSON includes two URL fields:
- `google_maps_url` — searches by business name + address
- `apple_maps_url` — pins exact lat/lng with business name label

Use hyperlinks (not raw URLs) where the platform supports them:
- **Telegram, Discord, terminal**: Use markdown links — `[Station Name](url)`
- **WhatsApp, Signal, SMS**: These don't support hyperlinks. Put the link on a separate line.

Provide **both** Google Maps and Apple Maps links so the user can choose.

### Two Response Modes

**Default (no fuel type specified):** Show a compact summary — cheapest station per fuel type. Covers everyone in one small message.

**Specific (user asked for a fuel type):** Show top 3–5 stations for that fuel type with map links.

### Default: Multi-Fuel Summary

Scan all stations and find the cheapest price for each fuel type available in the area. Show one line per fuel type. Only include the map link for the overall cheapest.

For platforms with hyperlinks (Telegram, Discord, terminal):
```
Cheapest fuel near [location]:

E10 — $2.17/L · [Ampol Smeaton Grange](google_maps_url) · 4.4 km
U91 — $2.17/L · [Ampol Smeaton Grange](google_maps_url) · 4.4 km
U95 — $2.31/L · [7-Eleven Gregory Hills](google_maps_url) · 3.7 km
U98 — $2.39/L · [7-Eleven Gregory Hills](google_maps_url) · 3.7 km
DSL — $2.19/L · [Ampol Smeaton Grange](google_maps_url) · 4.4 km
LPG — $1.10/L · [Ampol Foodary Narellan](google_maps_url) · 5.0 km

Ask me for more options on any fuel type.
```

For platforms without hyperlinks (WhatsApp, Signal, SMS):
```
Cheapest fuel near [location]:

E10 — $2.17/L · Ampol Smeaton Grange · 4.4 km
U91 — $2.17/L · Ampol Smeaton Grange · 4.4 km
U95 — $2.31/L · 7-Eleven Gregory Hills · 3.7 km
U98 — $2.39/L · 7-Eleven Gregory Hills · 3.7 km
DSL — $2.19/L · Ampol Smeaton Grange · 4.4 km
LPG — $1.10/L · Ampol Foodary Narellan · 5.0 km

Reply with a fuel type for more stations + directions.
```

### Specific: Single Fuel Type Detail

When the user asks for a specific type (e.g. "diesel near me", "cheapest E10"), show top stations for that type with map links.

For platforms with hyperlinks:
```
Cheapest DSL near Oran Park:

1. [Ampol Smeaton Grange](google_maps_url) — $2.19/L · 4.4 km · 6 hr ago
   [Apple Maps](apple_maps_url)
2. [Ampol Foodary Narellan](google_maps_url) — $2.16/L · 5.0 km · 6 days ago
3. [EG Ampol Oran Park](google_maps_url) — $2.34/L · 0.6 km · 6 days ago

[N] stations within [radius]km · [source]
```

For platforms without hyperlinks:
```
Cheapest DSL near Oran Park:

1. Ampol Smeaton Grange — $2.19/L · 4.4 km · 6 hr ago
   Google Maps: [google_maps_url]
   Apple Maps: [apple_maps_url]
2. Ampol Foodary Narellan — $2.16/L · 5.0 km · 6 days ago
   Google Maps: [google_maps_url]
3. EG Ampol Oran Park — $2.34/L · 0.6 km · 6 days ago
   Google Maps: [google_maps_url]

[N] stations within [radius]km · [source]
```

### Formatting Rules

- Default mode: one line per fuel type, cheapest station only, skip types with no data
- Specific mode: top 3–5 stations, sorted by price ascending
- Use `staleness.age_display` from JSON for freshness (specific mode only — keep default mode compact)
- Stale prices: append a note at the bottom — "Some prices may be a few days old"
- WA tomorrow prices: add "Tomorrow: $X.XX" after the current price
- Both Google Maps and Apple Maps for the top station; Google Maps only for the rest
- Invite follow-up: "Ask me for more options on any fuel type" or "Reply with a fuel type for more"

## Handling Edge Cases

- **Low confidence** (`confidence: "low"`): Do not silently show results. Tell the user: "I got an approximate location of [city] but it may not be exact. What suburb or postcode are you near?" Rerun with their answer.
- **Stale prices** (`stale_count > 0`): Show results but add a note — "Heads up: some of these prices are a few days old and may have changed." If this is the first query and FuelCheck is not configured, append the upgrade nudge (see below).
- **No results** (empty stations): "No stations found within [radius]km. Want me to try a wider search or a different suburb?"
- **API errors**: Multiple sources auto-fallback per state. If all fail: "Couldn't get prices right now. Can you try with a specific suburb name?"

Price sanity ($0.50–$5.00/L) is enforced automatically — out-of-range prices are filtered by the script.

## First Run: Upgrade Nudge

After showing results for the **first time**, check if FuelCheck is configured. If not, append an upgrade suggestion to your response. This is a one-time nudge — don't repeat it on subsequent queries in the same conversation.

**When to show:** The JSON response has `"source": "FuelSnoop"` or `"source": "PetrolSpy"` for NSW/ACT/TAS locations AND `stale_count > 0`.

**What to say (adapt to tone, don't copy verbatim):**

For platforms with hyperlinks:
```
Tip: Some of these prices are a few days old. For real-time government data, you can set up a free NSW FuelCheck API key (takes ~3 minutes):

1. Go to api.nsw.gov.au and click "Sign up" — just name + email
2. Once logged in, go to "My Apps" and create a new app (any name, e.g. "Fuel Prices")
3. Go to the API Catalogue, find "Fuel API", and click "Subscribe" — select your app and the free plan (2,500 calls/month)
4. Go back to "My Apps" → click your app → you'll see your API Key and API Secret
5. Share those with me and I'll save them so future lookups use live government data.
```

For platforms without hyperlinks:
```
Tip: Some prices may be outdated. You can get real-time data by setting up a free API key:

1. Go to api.nsw.gov.au and sign up (name + email)
2. Log in, go to "My Apps", create a new app (any name works)
3. In the API Catalogue, find "Fuel API" and subscribe (free plan)
4. Back in "My Apps", click your app to see your API Key and Secret
5. Share them with me — I'll save them for you.
```

**When the user provides keys**, save them securely:

```bash
mkdir -p ~/.config/fuel-pricing
cat > ~/.config/fuel-pricing/credentials.json << 'CREDS'
{
  "fuelcheck_key": "<key>",
  "fuelcheck_secret": "<secret>"
}
CREDS
chmod 600 ~/.config/fuel-pricing/credentials.json
```

Then confirm: "Keys saved securely. Future fuel price lookups will use real-time government data for NSW, ACT, and Tasmania."

**Do NOT show the nudge if:**
- FuelCheck is already configured (check setup status above)
- The user is in WA (FuelWatch is already govt data and free)
- The user is in VIC/SA/NT/QLD (FuelCheck doesn't cover these states)
- You've already shown the nudge in this conversation

## Reference

### Fuel Types

| Code | Name |
|------|------|
| E10 | Ethanol 10% |
| U91 | Unleaded 91 |
| U95 | Premium 95 |
| U98 | Premium 98 |
| DSL | Diesel |
| LPG | LPG |

### Data Sources

| State | Primary | Fallback |
|-------|---------|----------|
| WA | FuelWatch (govt, includes tomorrow's prices) | PetrolSpy |
| NSW, QLD | FuelSnoop | PetrolSpy |
| VIC, SA, TAS, NT, ACT | PetrolSpy | — |

All data sources are read-only public APIs. FuelWatch is official Australian government open data.
FuelSnoop and PetrolSpy are community data aggregators. No user data is sent to any service
beyond coordinates for the search area.

### Script Location Fallback (internal — for reference only)

When the script runs, it resolves location internally in this order:

1. **Explicit args** — `--lat`/`--lng`, `--location`, or `--postcode` (Nominatim geocoding)
2. **Browser consent** — localhost page requesting `navigator.geolocation` (WiFi, ~15-50ft accuracy, cached 24hrs)
3. **IP geolocation** — ip-api.com (city-level only, often inaccurate for non-city users)

The agent should almost never reach step 3. The Location Flow above ensures the user provides location info before the script runs.
