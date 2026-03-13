---
name: wind-calendar
description: Display current wind forecasts and calendar feeds for Israeli windsurfing/kitesurfing spots. **Fetch and parse ICS data immediately** when users ask to see forecasts, then offer calendar subscription. Use when users want to see upcoming wind conditions, check "when is good wind", or add forecasts to their calendar. Triggers on "show wind", "wind forecast", "what's the forecast", "when is good wind", "windsurfing", "kitesurfing", or Israeli beach spot names (Beit Yanai, Herzliya, Tel Aviv, Bat Galim).
---

# Wind Calendar

Generate calendar feeds for windsurfing and kitesurfing sessions based on wind forecasts.

## What This Skill Does

This skill provides access to an API that generates calendar feeds (ICS format) for windsurfing and kitesurfing sessions. The API:

- Fetches wind forecasts from Open-Meteo (primary) or Windguru (fallback) for Israeli Mediterranean coast locations
- Uses public weather model data (GFS, ICON, GDPS, IFS-HRES) from NOAA, DWD, CMC, and ECMWF
- Filters sessions based on customizable wind speed, wave height, and duration thresholds
- Groups consecutive hours of good conditions into sessions
- Returns standard ICS calendar format compatible with all calendar applications
- Auto-updates every 6 hours with fresh forecast data

The calendar feeds can be subscribed to in Apple Calendar, Google Calendar, Outlook, or any other calendar app that supports ICS subscriptions.

## When to Use This Skill

Use this skill when:

- User asks to **see/show/display** wind forecasts ("show me wind", "what's the forecast", "tell me the forecast")
- User asks about upcoming good wind conditions ("when is good wind", "any good wind days")
- User wants to add wind forecasts to their calendar or subscribe
- User mentions windsurfing, kitesurfing, or wind sports activities
- User asks about wind conditions at specific Israeli beach locations

## Default Behavior: Fetch First, Then Offer Subscription

**When users ask to see/show the forecast:**

1. **Immediately fetch** the ICS data from the API endpoint
2. **Parse and display** upcoming wind sessions in readable format:
   - Date and time range (convert UTC to local or show as-is)
   - Wind speed range, direction, wave height (from SUMMARY field)
   - Hourly breakdown (from DESCRIPTION field)
3. **Then recommend** subscribing for automatic updates with platform-specific instructions

**When users explicitly ask to subscribe or add to calendar:**

Skip the fetch and go straight to subscription instructions.

**ICS Format Overview:**

- Each wind session is a VEVENT block
- SUMMARY: "Wind 13-14kn N | 0.7m waves"
- DTSTART/DTEND: UTC timestamps
- DESCRIPTION: Hourly conditions (newline-separated)

## Available Locations

The API currently supports these Israeli Mediterranean coast locations:

- `beit-yanai` - Mediterranean coast, north of Netanya
- `herzliya` - Popular Tel Aviv area spot
- `tel-aviv` - Central location, urban beach
- `bat-galim` - Haifa area spot

## API Endpoint

```
https://wind-calendar.vercel.app/api/calendar
```

## Query Parameters

### Required

- `location` - One of: `beit-yanai`, `herzliya`, `tel-aviv`, `bat-galim`

### Optional

- `windMin` - Minimum wind speed in knots (default: 14)
- `windMax` - Maximum wind speed in knots (default: 35)
- `minSessionHours` - Minimum session duration in hours (default: 2)
- `model` - Forecast model ID (default: `3` for Windguru GFS, or `om_gfs` for Open-Meteo)
  - **Open-Meteo (Recommended)**:
    - `om_gfs` - GFS 13km (NOAA Global Forecast System)
    - `om_icon` - ICON 13km (DWD German weather model)
    - `om_gdps` - GDPS 15km (Canadian Meteorological Centre)
    - `om_ifs` - IFS-HRES 9km (ECMWF high-resolution)
  - **Windguru (Legacy, for backward compatibility)**:
    - `3` - GFS 13km
    - `45` - ICON 13km
    - `59` - GDPS 15km
    - `117` - IFS-HRES 9km
- `waveEnabled` - Enable wave filtering (default: false). When true, only sessions with waves matching thresholds are included
- `waveSource` - Wave source type: `"total"` or `"swell"` (default: `"total"`)
- `waveHeightMin` - Minimum wave height in meters (default: 0.5)
- `waveHeightMax` - Maximum wave height in meters (default: 5.0)
- `wavePeriodMin` - Minimum wave period in seconds (default: 8)

### Parameter Constraints

- `windMin` must be >= 0
- `windMax` must be <= 200
- `windMin` must be < `windMax`
- `minSessionHours` must be between 0 and 24

## Example URL Construction

### Basic Usage

```
https://wind-calendar.vercel.app/api/calendar?location=herzliya
```

This uses default thresholds: 14-35kn wind, 2+ hour sessions. Wave filtering is disabled by default.

### Customized for Stronger Winds

```
https://wind-calendar.vercel.app/api/calendar?location=beit-yanai&windMin=18&windMax=30&minSessionHours=3
```

This filters for stronger, longer sessions.

### Using Alternative Forecast Model

```
https://wind-calendar.vercel.app/api/calendar?location=herzliya&model=om_ifs
```

This uses the ECMWF IFS-HRES 9km model (often considered most accurate). If Open-Meteo fails, the API automatically falls back to the equivalent Windguru model.

### Beginner-Friendly Settings

```
https://wind-calendar.vercel.app/api/calendar?location=tel-aviv&windMin=10&windMax=20&minSessionHours=1
```

This shows lighter wind sessions suitable for beginners.

## Response Format

The API returns:

- **Content-Type**: `text/calendar; charset=utf-8`
- **Format**: Standard ICS (RFC 5545)
- **Cache-Control**: 6-hour caching with stale-while-revalidate

Each calendar event represents a wind session with:

- **Summary**: "Wind 14-22kn NW | 0.8m waves"
- **Start/End Time**: In local timezone (Asia/Jerusalem)
- **Description**: Hourly breakdown of conditions (wind speed, gusts, direction)

Example event:

```
SUMMARY: Wind 14-22kn NW | 0.8m waves
DTSTART: 20260305T100000Z
DTEND: 20260305T160000Z
DESCRIPTION: 12:00  14kn  gusts 16kn  NW
             14:00  18kn  gusts 22kn  NW
             16:00  16kn  gusts 19kn  NW
```

## How to Subscribe to the Calendar

Guide users through platform-specific subscription methods:

### Apple Calendar (macOS/iOS)

1. Copy the API URL (starting with `https://`)
2. Replace `https://` with `webcal://`
3. Open the `webcal://` URL in Safari
4. Calendar app will open and prompt to subscribe

**Example:**

```
webcal://wind-calendar.vercel.app/api/calendar?location=herzliya
```

**Sync Frequency**: Apple Calendar typically syncs subscribed calendars every ~15 minutes.

### Google Calendar

1. Open Google Calendar in a web browser
2. Click the "+" next to "Other calendars"
3. Select "From URL"
4. Paste the `https://` URL (NOT `webcal://`)
5. Click "Add calendar"

**Important**: Google Calendar syncs subscribed calendars slowly (every 12-24 hours). This cannot be changed by the user.

### Outlook

1. In Outlook, go to File → Account Settings → Internet Calendars
2. Click "New"
3. Paste the `https://` URL
4. Click OK

**Sync Frequency**: Outlook typically syncs subscribed calendars every ~12 hours.

### Direct Download

Users can also download a one-time snapshot:

1. Open the URL in any web browser
2. The browser will download a `.ics` file
3. Double-click to import into any calendar app

Note: Downloaded files don't auto-update. Subscriptions are recommended for ongoing forecasts.

## What Sessions Look Like

Wind sessions are filtered and grouped based on the specified parameters. Each session includes:

- **Title**: Summarizes wind range, dominant direction, and average wave height
- **Time Range**: Start and end times in Asia/Jerusalem timezone
- **Detailed Conditions**: Hourly breakdown in the event description
- **Daylight Only**: Sessions are filtered to daylight hours based on sunrise/sunset times

Sessions are created by:

1. Filtering forecast hours by wind speed, wave height thresholds
2. Grouping consecutive hours (within 3-hour gaps)
3. Keeping only groups that meet the minimum duration requirement

## Update Frequency

- **Forecast Data**: Updated every 6 hours from Open-Meteo (primary provider) with Windguru fallback
- **API Cache**: Responses cached for 6 hours with stale-while-revalidate and stale-if-error fallbacks
- **Calendar Sync**: Depends on the calendar application (see platform sections above)

When the forecast updates, subscribed calendars will automatically receive the new data on their next sync cycle.

## Data Attribution

**Open-Meteo** provides publicly available weather data under CC-BY 4.0 license from:

- NOAA (GFS - Global Forecast System)
- DWD (ICON - Germany's weather model)
- CMC (GDPS - Canadian Global Model)
- ECMWF (IFS-HRES - European high-resolution model)

**Windguru** is used as a fallback provider for legacy model IDs (3, 45, 59, 117).

## Important Limitations

- **Forecast Accuracy**: Forecasts use public weather model data (GFS, ICON, GDPS, IFS-HRES) and are subject to typical weather prediction limitations. Different models can show different predictions - no model is always correct.
- **Data Source**: Primary provider is Open-Meteo (CC-BY 4.0). If Open-Meteo fails, the API automatically falls back to Windguru for the equivalent model.
- **Geographic Coverage**: Currently limited to Israeli Mediterranean coast locations
- **Daylight Hours Only**: Sessions are filtered to occur during daylight (based on sunrise/sunset)
- **Timezone**: All times are in Asia/Jerusalem timezone
- **Sync Delays**: Calendar app sync frequencies vary (Google Calendar is the slowest)
- **Wave Data**: Wave filtering requires both wind and wave data availability. Not all locations/models provide wave forecasts

## Example Agent Workflows

### Workflow 1: Display Current Forecast

**User**: "Show me wind forecast in Beit Yanai" / "When is good wind at Herzliya this week?"

**Agent Actions**:

1. Construct URL: `https://wind-calendar.vercel.app/api/calendar?location=beit-yanai`
2. **Fetch the ICS data** using curl/HTTP/WebFetch
3. **Parse and display** upcoming sessions in readable format:

```
Upcoming wind sessions for Beit Yanai:

1. March 12, 2026 — 08:00–20:00 (Asia/Jerusalem)
   Wind: 14–25kn NE | Waves: 1.4m
   • 08:00 — 24.9kn (gusts 26.6kn) E
   • 11:00 — 16.7kn (gusts 16.5kn) NE
   • 14:00 — 14kn (gusts 13.6kn) NE
   • 17:00 — 15kn (gusts 16.4kn) N

2. March 15, 2026 — 14:00–20:00 (Asia/Jerusalem)
   Wind: 15–16kn NW | Waves: 0.8m
   • 14:00 — 14.6kn (gusts 10.9kn) NW
   • 17:00 — 15.6kn (gusts 16kn) N
```

4. **Recommend subscription**: "Want me to add this to your calendar so it updates automatically?"

### Workflow 2: Calendar Subscription

**User**: "Add windsurfing forecasts for Herzliya to my calendar"

**Agent Actions**:

1. Construct URL: `https://wind-calendar.vercel.app/api/calendar?location=herzliya`
2. Detect user's platform (if possible) or provide all options
3. For Apple users, provide webcal URL: `webcal://wind-calendar.vercel.app/api/calendar?location=herzliya`
4. For Google/Outlook users, provide https:// URL with platform-specific instructions (see sections below)
5. Explain: "This calendar will update automatically every 6 hours with fresh forecasts (14-35kn winds, 2+ hour sessions)"

### Workflow 3: Kitesurfing-Specific Requirements

**User**: "I want kite forecasts for Tel Aviv but only strong wind days, at least 3 hours long, with decent waves"

**Agent Actions**:

1. Construct URL for longer, stronger sessions with wave filtering: `https://wind-calendar.vercel.app/api/calendar?location=tel-aviv&windMin=20&windMax=35&minSessionHours=3&waveEnabled=true&waveHeightMin=1.0`
2. Provide subscription instructions
3. Explain: "This filters for sustained strong wind sessions (20-35 knots, 3+ hours) with waves 1m+, ideal for kitesurfing"

### Workflow 4: Beginner Windsurfer

**User**: "I'm learning to windsurf in Herzliya, what days will have light winds and small waves?"

**Agent Actions**:

1. Construct URL for lighter winds and small waves: `https://wind-calendar.vercel.app/api/calendar?location=herzliya&windMin=8&windMax=15&minSessionHours=1&waveEnabled=true&waveHeightMin=0.3&waveHeightMax=0.8`
2. Provide subscription instructions
3. Explain: "This shows gentler wind sessions (8-15 knots) with small waves (0.3-0.8m), perfect for learning"

### Workflow 5: Comparing Multiple Spots

**User**: "Which spot has better wind this weekend - Herzliya or Beit Yanai?"

**Agent Actions**:

1. Generate URLs for both locations
2. Suggest subscribing to both calendars with different names/colors
3. Or: Offer to fetch both ICS files and compare upcoming sessions
4. Explain: "You can subscribe to both and see them side-by-side in your calendar"

### Workflow 6: Comparing Different Models

**User**: "Show me what ECMWF says about the wind this week versus GFS"

**Agent Actions**:

1. Fetch ICS for same location with model=om_ifs (ECMWF): `https://wind-calendar.vercel.app/api/calendar?location=herzliya&model=om_ifs`
2. Fetch ICS for same location with model=om_gfs (GFS): `https://wind-calendar.vercel.app/api/calendar?location=herzliya&model=om_gfs`
3. Parse and compare the sessions from both models
4. Display differences: "ECMWF predicts wind on March 12-13, while GFS shows March 13-14"
5. Explain: "Different models can show different forecasts. ECMWF (IFS-HRES) is often considered most accurate for short-term forecasts."

### Workflow 7: Wave-Specific Filtering

**User**: "Show me days with good swell (not just wind-driven waves) at Herzliya"

**Agent Actions**:

1. Construct URL with swell filtering: `https://wind-calendar.vercel.app/api/calendar?location=herzliya&windMin=12&waveEnabled=true&waveSource=swell&waveHeightMin=0.8`
2. Parse and display sessions with swell conditions
3. Explain: "This shows wind sessions with swell waves (0.8m+). Swell is more consistent ocean waves, unlike choppy wind-driven waves"

## Troubleshooting

### No Sessions Appearing

If a subscribed calendar shows no events:

- Wind conditions may not meet the threshold criteria
- Try lowering `windMin` or `minSessionHours` parameters
- Check that the location name is spelled correctly (exact match required)

### Calendar Not Updating

If forecasts seem stale:

- Check the calendar app's sync settings
- Google Calendar has the longest delay (12-24 hours)
- Try manually refreshing the calendar in the app
- For Apple Calendar, force refresh by removing and re-adding the subscription

### Invalid Location Error

Location names must exactly match (case-sensitive):

- `beit-yanai` (not "beit yanai" or "Beit-Yanai")
- `herzliya` (not "Herzliya")
- `tel-aviv` (not "tel aviv" or "Tel-Aviv")
- `bat-galim` (not "bat galim")

### Parameter Errors

If the API returns an error about invalid parameters:

- Ensure `windMin` < `windMax`
- Check that `windMin` >= 0 and `windMax` <= 200
- Verify `minSessionHours` is between 0 and 24
- All numeric parameters must be valid numbers
