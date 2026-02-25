---
name: google-maps-api
description: Complete Google Maps Platform API client - 20+ APIs including geocoding, routes, places, weather, air quality, pollen, solar, elevation, timezone, address validation, roads, street view, and more
category: google
user_invocable: true
---

# Google Maps Platform - Universal API Skill

## Critical Behavior Rules

**These rules override all other instructions in this skill:**

1. **Communicate blockers immediately.** When ANY API call fails (403, REQUEST_DENIED, "not enabled", etc.), STOP and tell the user what happened in plain language. Do NOT silently work around it with web search or other fallbacks. Offer to fix it via Playwright (see "Guided API Enablement" section below).

2. **Ask before generating HTML.** NEVER start writing an HTML page without asking the user first. They may just want a text answer, JSON output, or a quick summary. Ask: "Want me to make an interactive HTML page for this, or is a text summary enough?"

3. **Ask before choosing output format.** When the user's request could be answered as text, JSON, or a visual page, ask which they prefer. Don't assume.

## Overview

Full-featured CLI client for **every** Google Maps Platform REST API. Unlike the browser-based google-maps skill, this skill calls Google's APIs directly for fast, structured JSON responses. Covers 20+ APIs across maps, routes, places, environment, and geospatial services.

## Setup

### 1. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the APIs you need (see API list below)
4. Go to **APIs & Services > Credentials** and create an API key
5. (Recommended) Restrict the key to only the APIs you need

### 2. Save the API Key

Add to your `.env` file in any of these locations (searched in order):

```bash
# Option 1: Project directory .env
echo 'GOOGLE_MAPS_API_KEY=your_key_here' >> .env

# Option 2: Home directory .env
echo 'GOOGLE_MAPS_API_KEY=your_key_here' >> ~/.env

# Option 3: Environment variable
export GOOGLE_MAPS_API_KEY=your_key_here
```

### 3. Enable Required APIs

In Google Cloud Console > APIs & Services > Library, enable the APIs you need:

| API Name | Console Name |
|----------|-------------|
| Geocoding | Geocoding API |
| Routes | Routes API |
| Places | Places API (New) |
| Elevation | Elevation API |
| Time Zone | Time Zone API |
| Air Quality | Air Quality API |
| Pollen | Pollen API |
| Solar | Solar API |
| Weather | Weather API |
| Address Validation | Address Validation API |
| Roads | Roads API |
| Street View | Street View Static API |
| Static Maps | Maps Static API |
| Geolocation | Geolocation API |
| Aerial View | Aerial View API |
| Route Optimization | Route Optimization API |
| Places Aggregate | Places Insights API |

## Script Location

```
~/.claude/skills/google-maps-api/scripts/gmaps.py
```

No external dependencies required - uses only Python standard library (`urllib`, `json`, `ssl`).

## Complete API Reference

### 1. Geocoding

**Forward geocode** - address to coordinates:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py geocode "1600 Amphitheatre Parkway, Mountain View, CA"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py geocode "Tokyo Tower" --language ja --region jp
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py geocode "Paris" --components "country:FR"
```

**Reverse geocode** - coordinates to address:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py reverse-geocode 37.4224 -122.0856
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py reverse-geocode 48.8584 2.2945 --language fr
```

### 2. Routes & Directions

**Get directions** between two locations:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py directions "New York, NY" "Boston, MA"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py directions "LAX" "SFO" --mode transit
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py directions "Seattle" "Portland" --alternatives --avoid-tolls
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py directions "A" "D" --waypoints "B" "C"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py directions "Home" "Work" --mode bicycling --units imperial
```

**Distance matrix** - multiple origins/destinations:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py distance-matrix \
  --origins "New York" "Boston" \
  --destinations "Philadelphia" "Washington DC"
```

### 3. Places

**Text search** - find places by query:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-search "best pizza in Chicago"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-search "pharmacy" --location "40.714,-74.006" --radius 1000
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-search "5-star hotels" --min-rating 4.5 --open-now
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-search "EV charging" --type "electric_vehicle_charging_station"
```

**Nearby search** - find places near coordinates:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-nearby 40.7128 -74.0060 --type restaurant --radius 800
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-nearby 34.0522 -118.2437 --type cafe --max-results 5
```

**Place details** - full info for a place:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py place-details ChIJN1t_tDeuEmsRUsoyG83frY4
```

**Autocomplete** - type-ahead suggestions:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py autocomplete "star" --location "37.7749,-122.4194"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py autocomplete "central p" --types "park"
```

**Place photo** - get photo URL:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py place-photo "places/PLACE_ID/photos/PHOTO_REF" --max-width 800
```

### 4. Air Quality

**Current conditions**:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py air-quality 40.7128 -74.0060
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py air-quality 40.7128 -74.0060 --health --pollutants
```

**Historical data** (up to 30 days):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py air-quality-history 40.7128 -74.0060 --hours 48
```

**Forecast** (up to 96 hours):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py air-quality-forecast 40.7128 -74.0060
```

### 5. Pollen

**Pollen forecast** (up to 5 days, grass/weed/tree):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py pollen 40.7128 -74.0060
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py pollen 34.0522 -118.2437 --days 5
```
Returns: Universal Pollen Index (UPI) for 3 plant types and 15 species.

### 6. Solar

**Building solar potential**:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py solar 37.4219 -122.0841
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py solar 37.4219 -122.0841 --quality HIGH
```
Returns: roof area, sunlight hours, optimal panel layout, energy/cost estimates.

**Solar data layers** (DSM, flux, shade rasters):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py solar-layers 37.4219 -122.0841 --radius 100
```

### 7. Weather

**Current conditions**:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py weather 40.7128 -74.0060
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py weather 40.7128 -74.0060 --mode current
```

**Hourly forecast** (up to 240 hours):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py weather 40.7128 -74.0060 --mode hourly --hours 48
```

**Daily forecast** (up to 10 days):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py weather 40.7128 -74.0060 --mode daily --days 7
```

**Recent history** (up to 24 hours):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py weather 40.7128 -74.0060 --mode history --hours 12
```

### 8. Elevation

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py elevation 39.7392 -104.9903
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py elevation --locations "39.7392,-104.9903|36.4555,-116.8666"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py elevation --path "36.578,-118.292|36.606,-118.099" --samples 20
```

### 9. Time Zone

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py timezone 40.7128 -74.0060
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py timezone 35.6762 139.6503 --language ja
```

### 10. Address Validation

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py validate-address "1600 Amphitheatre Pkwy, Mountain View, CA 94043"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py validate-address "123 Main St" --region US --enable-usps
```
Returns: deliverability verdict, corrected address, component-level confirmation, USPS CASS data.

### 11. Roads

**Snap to roads** - align GPS traces:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py snap-roads "60.170,-24.942|60.171,-24.941|60.172,-24.940"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py snap-roads "60.170,-24.942|60.172,-24.940" --interpolate
```

**Nearest roads**:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py nearest-roads "60.170,-24.942|60.171,-24.941"
```

### 12. Street View

**CLI data use** (server-side image download, costs $7/1,000):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py streetview --lat 46.414 --lng 10.013 --heading 90
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py streetview --location "Eiffel Tower, Paris" --size 800x600
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py streetview --pano CAoSLEFGMVFpcE... --output paris_sv.jpg
```

**For HTML pages** — ALWAYS use a direct Google Maps link instead (zero cost, zero key exposure):
```
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}&heading={heading}&pitch=0&fov=90
```
See "Street View in HTML" section below for details.

**WARNING:** Do NOT use the old shorthand format `@{lat},{lng},3a,75y,{heading}h,90t` — it is unreliable and often opens a zoomed-out world map instead of Street View. Always use the `map_action=pano` format above.

### 13. Static Maps

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py static-map --lat 40.714 --lng -74.006 --zoom 13
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py static-map --center "Tokyo" --maptype satellite --zoom 12
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py static-map --center "NYC" --markers "color:red|40.714,-74.006" --size 800x600
```

### 14. Geolocation

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py geolocation
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py geolocation --wifi "00:11:22:33:44:55,-65" "66:77:88:99:AA:BB,-72"
```

### 15. Aerial View (US only)

```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py aerial-view check --address "1600 Amphitheatre Pkwy, Mountain View"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py aerial-view render --address "1600 Amphitheatre Pkwy, Mountain View"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py aerial-view get --video-id VIDEO_ID
```

### 16. Route Optimization

Solve vehicle routing problems (VRP):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py route-optimize problem.json --project my-gcp-project
```

Input JSON format: `{"model": {"shipments": [...], "vehicles": [...]}}` per Google Route Optimization API spec.

### 17. Places Aggregate (Insights)

Count or list places matching filters in an area:
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-aggregate --location "40.714,-74.006" --radius 5000 --type restaurant
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py places-aggregate --location "34.052,-118.244" --type cafe --min-rating 4.0 --insight INSIGHT_PLACES
```

### 18. Maps Embed URL (Free)

Generate embeddable map URLs (free, unlimited):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode place --query "Eiffel Tower"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode directions --origin "NYC" --destination "Boston"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode streetview --lat 46.414 --lng 10.013
```

## Usage Patterns for Claude

When the user asks location/geography/environment questions, use the appropriate command:

| User Intent | Command |
|-------------|---------|
| "Where is...?" | `geocode` |
| "What address is at...?" | `reverse-geocode` |
| "How do I get from A to B?" | `directions` |
| "How far is A from B?" | `distance-matrix` |
| "Find restaurants near..." | `places-search` or `places-nearby` |
| "What are the hours for...?" | `place-details` |
| "What's the air quality in...?" | `air-quality` |
| "Is the pollen bad today?" | `pollen` |
| "What's the weather in...?" | `weather` |
| "Is this address valid?" | `validate-address` |
| "What's the elevation of...?" | `elevation` |
| "What timezone is...?" | `timezone` |
| "Show me a map of..." | `static-map` |
| "Can I put solar panels on my roof?" | `solar` |
| "Optimize delivery routes" | `route-optimize` |
| "How many coffee shops in area?" | `places-aggregate` |

## Interactive HTML Output

**IMPORTANT: Always ASK before generating HTML.** Never start writing an HTML file without the user's explicit approval. After delivering results as text, ask:

> "Want me to put this into an interactive HTML page you can open in the browser? Default theme is **Warm Stone Sunrise** (light, warm-toned, premium)."

If the user says yes (or explicitly asks for HTML/a page/a map), then generate it. If they don't respond or say no, just give them the text/JSON results.

**By default, generate zero-key HTML pages** using Google Maps embed iframes (`output=embed`) — no API key needed, no key exposure risk. Only use the Maps JavaScript API (`<script src="https://maps.googleapis.com/maps/api/js?key=...">`) when the user explicitly requests advanced interactive features (custom markers, polylines, clustering, etc.) that embeds can't support.

### Zero-Key Embed Iframes (Default)

Use these iframe formats for maps — they require **no API key** and are free:

**Location/place map:**
```html
<iframe src="https://maps.google.com/maps?q=Oahu+Hawaii&z=10&output=embed"
  width="100%" height="400" style="border:0" allowfullscreen></iframe>
```

**Directions map:**
```html
<iframe src="https://maps.google.com/maps?saddr=Los+Angeles+CA&daddr=San+Jose+CA&output=embed"
  width="100%" height="400" style="border:0" allowfullscreen></iframe>
```

**Parameters:**
- `q` — place name or address (URL-encoded, use `+` for spaces)
- `saddr` / `daddr` — origin/destination for directions
- `z` — zoom level (1-20, default ~12)
- `output=embed` — required, makes it embeddable
- `ll` — optional center coordinates `lat,lng`

**WARNING:** Do NOT use `loading="lazy"` on Google Maps embed iframes. Lazy loading prevents off-screen iframes from loading, causing maps below the fold to appear permanently blank. Always omit the `loading` attribute or use `loading="eager"`.

| Result Type | Default HTML Element |
|-------------|------------------------|
| Street View | **Direct Google Maps link** (`map_action=pano`) — opens full interactive Street View in new tab. See "Street View in HTML" section. |
| Directions | Embed iframe with `saddr`/`daddr` + `output=embed` |
| Places search | Embed iframe with `q=place+name` + `output=embed` + info cards |
| Nearby search | Embed iframe centered on location + place cards |
| Static map | Embed iframe with `q` and `z` (zoomable, draggable) |
| Weather/Air Quality | Embed iframe for location + condition cards, icons, charts |
| Elevation | Elevation profile chart + embed iframe with path markers |
| Solar | Embed iframe for building location + solar potential stats |
| Trip plans | Combined multi-section page: embed iframe maps, place cards, weather widget |

When generating HTML pages:
1. Use a single self-contained `.html` file (inline CSS/JS, no external dependencies)
2. **Default to zero-key embed iframes** (`output=embed`) for all maps — NO API key in HTML
3. **NEVER use `google.maps.StreetViewPanorama` or the Street View JS API in HTML pages.** Always use direct Google Maps links with `map_action=pano` for Street View. This is a hard rule.
4. **NEVER include a Google Maps JS API `<script>` tag unless the user explicitly requests advanced interactive features.** The `output=embed` iframe approach handles most use cases without any API key.
5. Save to the current working directory with a descriptive name (e.g., `marea-streetview.html`, `nyc-trip-plan.html`)
6. Open automatically in the browser via `open <file>` (macOS) after creation

### Street View in HTML — Zero Key Exposure

**HARD RULE: Never embed Street View using the JavaScript API or Embed API in HTML pages.** Both approaches expose the API key in client-side code. Instead, ALWAYS use a direct Google Maps link that opens the full interactive Street View experience in the user's browser — zero cost, zero API key exposure.

**Direct link format (Google Maps URLs API — reliable):**
```
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}&heading={heading}&pitch={pitch}&fov=90
```

**Parameters:**
- `viewpoint={lat},{lng}` — coordinates of the Street View location
- `heading` — compass heading in degrees (0=North, 90=East, 180=South, 270=West)
- `pitch` — pitch angle (-90=down, 0=level, 90=up)
- `fov` — field of view in degrees (10-100, default 90)
- `map_action=pano` — **required** — explicitly triggers Street View panorama mode

**WARNING:** Do NOT use the old shorthand format `@{lat},{lng},3a,75y,{heading}h,{pitch}t` — it is unreliable and often fails to open Street View, instead showing a zoomed-out world map. Always use the `map_action=pano` format.

**Examples:**
```
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=40.76545,-73.98115&heading=90&pitch=0&fov=90
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=48.8584,2.2945&heading=180&pitch=0&fov=90
https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=46.414,10.013&heading=270&pitch=-5&fov=90
```

**How to implement in HTML pages:**

For a standalone Street View button:
```html
<a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=40.76545,-73.98115&heading=90&pitch=0&fov=90"
   target="_blank" rel="noopener noreferrer"
   style="display:inline-block; padding:12px 24px; background:#4f46e5; color:white;
          border-radius:8px; text-decoration:none; font-weight:600;">
  Open Street View →
</a>
```

For a JavaScript function (e.g., in trip plan pages with many locations):
```javascript
function openStreetView(lat, lng, name) {
  window.open(
    `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}&heading=0&pitch=0&fov=90`,
    '_blank'
  );
}
```

For a card/preview with context:
```html
<div class="streetview-card">
  <div class="sv-preview">
    <!-- Optional: use a static map or place photo as preview thumbnail -->
    <div class="sv-overlay">
      <span class="sv-icon">🔭</span>
      <span>Interactive Street View</span>
    </div>
  </div>
  <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}&heading=0&pitch=0&fov=90"
     target="_blank" rel="noopener noreferrer" class="sv-button">
    Open in Google Maps →
  </a>
  <p class="sv-note">Opens full 360° interactive Street View — pan, zoom, and walk around</p>
</div>
```

**In consolidated trip plan pages**, replace the former `StreetViewPanorama` section with a styled button/link card. The user clicks to open full Street View in a new tab — they get the complete interactive experience directly from Google Maps.

**Why this approach:**
- Zero API key exposure — no key in HTML source at all
- Zero cost — no API calls, no billing
- Better experience — full Google Maps Street View with navigation, not a limited embed
- Works for all deployment modes (personal, BYOK, platform key)

### Consolidated One-Stop Pages

For multi-part requests (trip plans, location research, comparisons), **always offer to generate a single consolidated HTML page** that combines ALL collected data into one interactive dashboard. The user should be able to see everything in one stop rather than scrolling through terminal output.

A consolidated page should include every piece of data gathered during the conversation, for example a trip plan page might combine:
- Interactive route map with driving directions polyline
- Weather widget for the destination
- Hotel/place cards with photos, ratings, hours
- Restaurant recommendation with Street View link (opens full 360° view in Google Maps)
- Timeline/itinerary section
- Rental car & airport info

Design principles for consolidated pages:
- Use a clean, modern dashboard layout with distinct sections
- Each section should be visually rich: maps, cards, icons, badges — not just text
- Include smooth scroll navigation (sticky frosted-glass nav with active link highlighting)
- Scroll-reveal animations (IntersectionObserver fade-up on each section)
- Fully responsive: desktop (>1024px), tablet (641-1024px), mobile (<=640px), small phone (<=380px)
- Cards, buttons, travel chips, and stat grids stack to single column on mobile
- Maps reduce height on mobile (280px), buttons go full-width

### Default Theme: Warm Stone Sunrise

All HTML pages use this theme by default unless the user requests otherwise.

**Color palette:**
- Background: `#fafaf9` (warm off-white)
- Surface: `#ffffff` cards, `#f5f5f4` alt surfaces
- Borders: `#e7e5e4` (warm stone), `#f0eeec` (light dividers)
- Text: `#1c1917` primary, `#57534e` secondary, `#a8a29e` tertiary
- Accent: `#4f46e5` (indigo) with `#eef2ff` light and `#c7d2fe` mid
- Semantic: green `#059669`, amber `#d97706`, red `#dc2626`, blue `#2563eb`

**Typography:**
- Headings: `Playfair Display` (serif, 700-900 weight) — editorial luxury feel
- Body: `Inter` (sans-serif) with full font-smoothing
- Section pattern: uppercase label (11px, accent) → serif title (26px) → description (14px, tertiary)

**Hero:** `linear-gradient(160deg, #eef2ff, #faf5ff, #fff7ed)` — indigo to lavender to peach

**Maps:** Default Google Maps style via embed iframes. When using Maps JS API (opt-in), apply light custom style — muted stone tones, soft blue water `#c9d7e4`, green parks `#d4e9d4`, white roads

**Shadows:** Subtle `0 1px 2px rgba(0,0,0,0.04)` base, `0 4px 6px` on hover

**Nav:** Sticky frosted glass (`rgba(255,255,255,0.85)` + `backdrop-filter: blur(20px)`), active link underline animation

**Interactions:** Card lift on hover (`translateY(-2px)`), timeline dot fill + glow ring, step indent on hover, button lift with shadow increase

## API Key Security & Production Architecture

### The Problem

Any API key embedded in client-side HTML/JavaScript is visible to users via browser DevTools. This is fine for personal use but **critical for production apps** where you're serving multiple users.

### Deployment Modes

This skill supports three deployment modes with different security profiles:

#### Mode 1: Personal / CLI Use (Single User)

The user's own API key in `.env`, used locally by `gmaps.py`. Key never leaves the machine.

```
User's Machine
├─ .env (GOOGLE_MAPS_API_KEY=...)
├─ gmaps.py → calls Google APIs directly
└─ HTML pages → zero-key embed iframes (preferred) or key embedded (acceptable)
```

**Risk**: Low — it's the user's own key on their own machine.
**Key restriction**: None needed (or restrict to the APIs you use).
**Best practice**: Even for personal use, prefer zero-key `output=embed` iframes for HTML pages. Only use Maps JS API when you need advanced features (custom markers, polylines, clustering).

#### Mode 2: Users Bring Their Own Key (Multi-User App)

Users configure their own Google API key. They control their own billing.

```
Your App
├─ User configures their own API key in app settings
├─ Key stored in user's profile (encrypted at rest)
├─ Used server-side for data queries
└─ Frontend key: user creates a separate domain-restricted key
```

**Risk**: Low-Medium — it's the user's key, their billing.
**Important**: When generating shareable/exportable HTML pages, NEVER embed the user's key. Use static exports instead (see Shareable Export Mode below).
**Onboarding**: Walk users through GCP Console setup and API enablement (see Setup section above).

#### Mode 3: Platform Key (Users Pay You) — CRITICAL

Users pay your platform. YOU provide the Google API key. Users must NEVER see it.

**Architecture: Two-Key + Backend Proxy**

```
┌─────────────────────────────────────────────────────┐
│  User's Browser                                      │
│                                                       │
│  HTML Page (served from app.yourdomain.com)           │
│  ├─ Interactive Maps  ← Frontend Key (domain-locked)  │
│  ├─ Street View       ← Frontend Key (domain-locked)  │
│  └─ All data (weather, places, directions, etc.)      │
│       ↑ pre-rendered from backend, NO key in browser  │
│                                                       │
└──────────────────┬────────────────────────────────────┘
                   │ /api/geocode, /api/directions, etc.
                   ▼
┌──────────────────────────────────────────────────────┐
│  YOUR Backend Server                                  │
│                                                       │
│  Backend Key (env var, never sent to browser)         │
│  ├─ Geocoding, Directions, Places, Weather, etc.      │
│  ├─ Street View Static → returns image bytes          │
│  └─ All data APIs proxied with your key server-side   │
│                                                       │
│  Key restricted by: Server IP address                 │
│  Even if leaked: won't work from other IPs            │
└──────────────────┬────────────────────────────────────┘
                   │
                   ▼
            Google Maps Platform
```

**Frontend Key** (client-side, in the HTML):
- Only enables: **Maps JavaScript API** (for interactive map rendering)
- Restricted by: **HTTP referrer** → `https://app.yourdomain.com/*`
- Even if someone copies it, it only works from your domain
- Cannot call data APIs (geocoding, places, etc.) — those are disabled on this key

**Backend Key** (server-side, hidden):
- Enables: ALL data APIs (geocoding, directions, places, weather, pollen, solar, etc.)
- Restricted by: **Server IP address**
- Never sent to the browser — lives in server environment variables only
- Even if leaked, only works from your server's IP

**How HTML pages work in this mode**:
```javascript
// UNSAFE — key exposed, data fetched client-side:
const service = new google.maps.DirectionsService();
service.route({ origin: 'JFK', destination: 'The Plaza' });

// SAFE — data pre-fetched by backend, only map rendering in browser:
const routeData = /* injected by server from backend API call */;
const path = google.maps.geometry.encoding.decodePath(routeData.polyline);
new google.maps.Polyline({ path: path, map: map });
```

### Setting Up Two Keys in GCP Console

#### Step 1: Create the Frontend Key
1. Go to **APIs & Services > Credentials** in GCP Console
2. Click **Create Credentials > API Key**
3. Click the key to edit it
4. Under **Application restrictions**: select **HTTP referrers**
5. Add your domain: `https://app.yourdomain.com/*`
6. Under **API restrictions**: select **Restrict key**
7. Enable ONLY: **Maps JavaScript API**
8. Save

#### Step 2: Create the Backend Key
1. Click **Create Credentials > API Key** again
2. Click the key to edit it
3. Under **Application restrictions**: select **IP addresses**
4. Add your server IP(s)
5. Under **API restrictions**: select **Restrict key**
6. Enable: Geocoding, Routes, Places (New), Weather, Air Quality, Pollen, Solar, Elevation, Time Zone, Address Validation, Roads, Street View Static, Geolocation, Aerial View, Route Optimization
7. Save

#### Step 3: Configure Your App
```bash
# Backend server environment
GOOGLE_MAPS_BACKEND_KEY=AIzaSy...xxx   # Server-side only, IP-restricted
GOOGLE_MAPS_FRONTEND_KEY=AIzaSy...yyy  # Injected into HTML, domain-restricted
```

### Shareable Export Mode

When users want to download or share HTML pages (email, Slack, etc.), generate a **static export** with NO API keys:

| Element | In-App (interactive) | Shareable Export |
|---------|---------------------|------------------|
| Maps | Maps JavaScript API (frontend key) | Maps Embed API `<iframe>` (free, no key abuse risk) |
| Street View | **Direct Google Maps link** (no key needed) | **Direct Google Maps link** (no key needed) |
| Route lines | `DirectionsRenderer` (frontend key) | Static map image with path overlay (base64) |
| Data (weather, places) | Pre-rendered from backend | Same pre-rendered HTML — no API calls needed |
| API key exposure | Frontend key, domain-locked | **No key at all** |

To generate embed URLs (free, unlimited):
```bash
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode place --query "Marea Restaurant NYC"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode directions --origin "JFK" --destination "The Plaza Hotel NYC"
python3 ~/.claude/skills/google-maps-api/scripts/gmaps.py embed-url --mode streetview --lat 40.76545 --lng -73.98115
```

### Security Summary

| Deployment | Data APIs | Map Rendering | Key Exposure | Shareable |
|-----------|-----------|---------------|-------------|-----------|
| **Personal CLI** | User's key locally | Zero-key embed iframes (default) | **None** | Yes (no key) |
| **Personal CLI (advanced)** | User's key locally | Maps JS API (opt-in for polylines, clustering, etc.) | User's own risk | No (key leaks) |
| **BYOK (user's key)** | User's key on server | User creates frontend key | User's own risk | Static export only |
| **Platform key (you pay)** | Backend key (IP-locked) | Frontend key (domain-locked) | **Safe** | Static export only |

### Rate Limiting & Abuse Prevention (Platform Mode)

When serving multiple users with your key, also implement:
- **Per-user rate limits**: Cap API calls per user per hour/day
- **Authentication**: Only authenticated, paying users can trigger API calls
- **Usage tracking**: Log which user triggered which API call for billing
- **Quota alerts**: Set up GCP billing alerts to catch unexpected spikes
- **Budget caps**: Set maximum daily spend in GCP Console

## Error Handling & Guided API Setup

**CRITICAL: When ANY command fails, you MUST tell the user immediately.** Do NOT silently fall back to web search or other workarounds. The user needs to know what's broken so they can decide how to fix it.

When a command fails, detect the error type and respond accordingly:

- **403 Forbidden / API not enabled**: **STOP. Tell the user. Offer Playwright walkthrough** (see below)
- **REQUEST_DENIED**: **STOP. Tell the user. Offer Playwright walkthrough** (see below)
- **400 Bad Request**: Invalid parameters — check the API docs
- **429 Rate Limited**: Too many requests — add a short delay
- **ZERO_RESULTS**: No results found — try broader search
- **INVALID_REQUEST**: Missing required parameters
- **Key not found**: Ensure `GOOGLE_MAPS_API_KEY` is set in `.env` or environment
- **RefererNotAllowedMapError**: Frontend key's HTTP referrer restriction doesn't match the current domain

### Guided API Enablement (Playwright Walkthrough)

**This is the PRIMARY response when an API is not enabled.** Do not skip this. Do not silently work around it.

When a user's API call fails with **403**, **REQUEST_DENIED**, or an "API not enabled" error:

1. **Tell the user what happened** in plain language:
   > "It looks like the [API Name] isn't enabled on your Google Cloud project yet. No worries — I can walk you through enabling it right now in your browser. Want me to go ahead?"

2. **If the user says yes**, use Playwright MCP to automate the enablement:

   ```
   Step 1: Navigate to the specific API's enablement page:
           https://console.cloud.google.com/apis/library/[API_ENDPOINT]

   Step 2: If a project selector appears, let the user pick their project
           (or auto-select if there's only one)

   Step 3: Click the "Enable" button

   Step 4: Wait for the confirmation (loading spinner → "API enabled" or
           the button changes to "Manage")

   Step 5: Confirm to the user: "Done! [API Name] is now enabled.
           Let me retry your request."

   Step 6: Retry the original command automatically
   ```

3. **API endpoint URLs** for Playwright navigation (use these exact paths):

   | API | GCP Library URL path |
   |-----|---------------------|
   | Geocoding | `geocoding-backend.googleapis.com` |
   | Routes | `routes-backend.googleapis.com` |
   | Places (New) | `places-backend.googleapis.com` |
   | Elevation | `elevation-backend.googleapis.com` |
   | Time Zone | `timezone-backend.googleapis.com` |
   | Air Quality | `airquality.googleapis.com` |
   | Pollen | `pollen.googleapis.com` |
   | Solar | `solar.googleapis.com` |
   | Weather | `weather.googleapis.com` |
   | Address Validation | `addressvalidation.googleapis.com` |
   | Roads | `roads.googleapis.com` |
   | Street View Static | `street-view-image-backend.googleapis.com` |
   | Maps Static | `static-maps-backend.googleapis.com` |
   | Maps JavaScript | `maps-backend.googleapis.com` |
   | Maps Embed | `maps-embed-backend.googleapis.com` |
   | Geolocation | `geolocation.googleapis.com` |
   | Aerial View | `aerialview.googleapis.com` |
   | Route Optimization | `routeoptimization.googleapis.com` |

   Full URL pattern: `https://console.cloud.google.com/apis/library/[path_from_table]`

4. **If the user says no** (prefers to do it manually), give them the direct URL:
   > "No problem! Here's the direct link — just click Enable:
   > https://console.cloud.google.com/apis/library/[API_ENDPOINT]"

5. **Batch enablement**: If the user is setting up for the first time and multiple APIs need enabling, offer to enable them all in one go:
   > "I can enable all the commonly used APIs for you in one pass — Geocoding, Routes, Places, Weather, Elevation, Time Zone, and Maps JavaScript. Want me to set them all up?"

   Then loop through each API page via Playwright, clicking Enable on each.

6. **Important notes for Playwright walkthrough**:
   - The user must already be logged into Google Cloud Console in their browser
   - If they're not logged in, tell them to sign in first at https://console.cloud.google.com
   - Some APIs (Weather, Solar) may require billing to be enabled on the project
   - After enabling, there can be a ~30 second propagation delay before the API works
   - If "Enable" button is not visible and "Manage" is shown instead, the API is already enabled

## Pricing Notes

Most APIs charge per request. Key free/paid tiers:
- **Maps Embed API**: Always free (use for shareable exports)
- **Maps JavaScript API**: $7 per 1,000 loads
- **Street View (JS)**: $7 per 1,000 panorama loads — **NEVER use in HTML pages; use direct Google Maps links instead (free, no key)**
- **$200/month free credit** on Google Maps Platform
- Routes API: $5-15 per 1,000 requests depending on features
- Places API: $17-40 per 1,000 requests
- Environment APIs (Air Quality, Pollen, Solar): varies
- Check [Google Maps pricing](https://developers.google.com/maps/billing-and-pricing/pricing) for current rates

## Notes

- All output is JSON (except image downloads which save to file)
- No external Python dependencies - uses only stdlib
- The script searches for `.env` in: CWD, home dir, skill dir
- For image APIs (streetview, static-map), files are saved locally
- Weather API may require separate billing enablement
- Aerial View is US addresses only
- Route Optimization requires a GCP project ID
- Roads speed limits require an Asset Tracking license
