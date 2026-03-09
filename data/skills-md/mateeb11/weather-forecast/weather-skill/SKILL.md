---
name: weather-skill
description: >
  Fetches current weather conditions and forecasts for any location worldwide.
  Use this skill whenever the user asks about weather, temperature, rain, wind,
  forecast, climate conditions, or what to wear/pack for a trip. Triggers on
  queries like "what's the weather in X", "forecast for Y", "will it rain",
  "what should I pack for Z", "how hot/cold is it", "is it windy in X",
  or any travel-planning question where weather matters.
---

# Weather Skill

Provides current weather and forecasts for any location using two free APIs:
- **Nominatim** (OpenStreetMap) for geocoding locations → `scripts/geocode.py`
- **Open-Meteo** for weather data → `scripts/fetch_weather.py`

---

## Workflow

1. **Understand the user's request.** Extract the location, time range, and whether they're planning travel. See examples below.
2. **Geocode the location** by running `scripts/geocode.py "<location>"`. It returns JSON with `display_name`, `lat`, `lon`, and an `ambiguous` flag. If ambiguous, ask the user to clarify.
3. **Fetch weather** by running `scripts/fetch_weather.py` with the lat/lon and appropriate flags. See script usage below.
4. **Respond to the user** with a clear summary. See example outputs below.
5. **If travel intent is detected**, also read `references/clothing_guide.md` and include relevant clothing advice.

---

## Scripts

### Geocode: `scripts/geocode.py`

Converts a location string to coordinates.

```bash
python scripts/geocode.py "Tokyo"
python scripts/geocode.py "King Abdullah Financial District, Riyadh"
python scripts/geocode.py "Times Square, New York"
```

Returns JSON:
```json
{
  "display_name": "Tokyo, Japan",
  "lat": 35.6764,
  "lon": 139.6500,
  "importance": 0.82,
  "ambiguous": false
}
```

If `ambiguous` is `true`, an `alternatives` list is included — ask the user which they meant.

### Weather: `scripts/fetch_weather.py`

Fetches weather data for given coordinates.

```bash
# Current conditions only
python scripts/fetch_weather.py --lat 35.6764 --lon 139.65 --resolution current

# Hourly forecast (good for today, tomorrow, next 12 hours, specific day)
python scripts/fetch_weather.py --lat 35.6764 --lon 139.65 --resolution hourly

# Daily forecast (good for multi-day ranges, next week, etc.)
python scripts/fetch_weather.py --lat 35.6764 --lon 139.65 --resolution daily

# Custom timezone (default is "auto" which uses the location's timezone)
python scripts/fetch_weather.py --lat 35.6764 --lon 139.65 --resolution hourly --timezone Asia/Tokyo

# Include historical data when user asks about past weather
python scripts/fetch_weather.py --lat 35.6764 --lon 139.65 --resolution daily --past-days 7
```

Returns JSON with `meta`, `current`, `hourly`, and/or `daily` sections depending on resolution.

Example JSON response (`--resolution current`):
```json
{
  "meta": {
    "lat": 35.6764,
    "lon": 139.65,
    "timezone": "Asia/Tokyo",
    "resolution": "current",
    "forecast_days": 16,
    "past_days": 0
  },
  "current": {
    "time": "2026-02-25T14:00",
    "temperature_c": 12.3,
    "apparent_temperature_c": 10.8,
    "weather_code": 1,
    "weather_description": "Mainly clear",
    "wind_speed_kmh": 14.2,
    "humidity_pct": 48,
    "precipitation_mm": 0.0
  },
  "hourly": null,
  "daily": null
}
```

The script always requests `forecast_days=16` (max forecast horizon).
Use `--past-days` only for past weather requests (`0..92`).

---

## How to Interpret User Requests

The agent should interpret the user's natural language to determine three things:

### 1. Location
Extract the place name from the query. Examples:
- "Weather in **Jeddah** now" → `"Jeddah"`
- "Forecast for **London** this weekend" → `"London"`
- "I'm going to **Tokyo** next week" → `"Tokyo"`
- "How windy will it be in **AlUla** on Friday?" → `"AlUla"`

If no location is mentioned, ask the user.

### 2. Time Range, Resolution, and Past Weather

| User says | Resolution | `past_days` | Notes |
|---|---|---|---|
| "now" / "current" / no time specified | `current` (also include hourly for next 24h) | `0` | Forecast request always uses 16 days. |
| "today" / "tonight" / "tomorrow" / "tomorrow morning" | `hourly` | `0` | Use hourly data to answer specific time windows. |
| "this weekend" / "on Friday" / "hourly for next 12 hours" | `hourly` | `0` | Filter the returned series in the response. |
| "next 3 days" | `hourly` | `0` | Summarize from hourly data. |
| "next 7 days" / "next week" / "first week of March" | `daily` | `0` | Summarize relevant days from daily data. |
| "March" / "in April" / "05/01 to 06/30" | `daily` | `0` | If outside forecast horizon, clearly state limits. |
| "past weather" / "last 3 days" / "yesterday" | `daily` (or `hourly` for short windows) | set from request | If user says "past" without a number, default to `7`. |

The user may specify dates in various formats (MM/DD, DD/MM, "May 1st", "1 March", etc.) — interpret based on context and filter the returned timeline accordingly. Use the current year unless another year is stated or implied.

Use `daily` for ranges > 3 days, `hourly` for shorter windows, `current` for right-now queries (but still include hourly for context).

**Default** (no time specified): current conditions + next 24 hours hourly.

**Remember:** Forecast is fixed to 16 days. For past requests, use `past_days` (`0..92`).

### 3. Travel Intent

Detect if the user is planning to go somewhere. Look for keywords like:
**pack, wear, travel, visiting, going to, headed to, trip, vacation, holiday, outing, flight, should I bring**

If travel intent is detected → also include clothing guidance (see below).

---

## Example Outputs

### Example 1: Simple current weather

**User:** "What's the weather in Jeddah now?"

**Response:**

> **Weather in Jeddah, Saudi Arabia**
>
> Right now it's **Clear sky** with a temperature of **28°C** (feels like 30°C). Wind is light at **12 km/h** from the north, and humidity is at 45%. No precipitation expected.
>
> **Next few hours:**
> - 3 PM: 29°C, Clear sky, 0% rain
> - 4 PM: 28°C, Partly cloudy, 0% rain
> - 5 PM: 26°C, Clear sky, 0% rain
> *(and so on...)*

### Example 2: Weekend forecast

**User:** "Forecast for London this weekend"

**Response:**

> **Weekend Forecast for London, UK**
>
> **Saturday, Mar 1:** Highs of 11°C, lows of 5°C. Moderate rain expected (70% probability, ~4mm). Wind up to 25 km/h.
>
> **Sunday, Mar 2:** Highs of 13°C, lows of 6°C. Partly cloudy, 20% rain chance. Lighter wind at 15 km/h.
>
> Overall: A wet Saturday clearing into a drier Sunday. Bring an umbrella for Saturday.

### Example 3: Travel planning with clothing advice

**User:** "I'm going to Tokyo next week — what should I pack?"

**Response:**

> **Tokyo, Japan — Next Week Forecast (Mar 3–9)**
>
> | Day | High | Low | Conditions | Rain | Wind |
> |---|---|---|---|---|---|
> | Mon | 12°C | 4°C | Partly cloudy | 10% | 15 km/h |
> | Tue | 10°C | 3°C | Slight rain | 65% | 20 km/h |
> | ... | ... | ... | ... | ... | ... |
>
> **What to Wear:**
> Expect **cold** conditions (lows near 3°C) with **rain** mid-week. Pack:
> - Warm layers: fleece or wool sweater + insulated jacket
> - Waterproof jacket and umbrella for Tuesday/Wednesday
> - Closed-toe waterproof shoes
> - Scarf and light gloves for mornings/evenings
>
> *See: clothing_guide.md — sections: cold, rainy*

### Example 4: Specific condition query

**User:** "How windy will it be in AlUla on Friday?"

**Response:**

> **Wind Forecast for AlUla, Saudi Arabia — Friday, Feb 28**
>
> Wind speeds will peak at **35 km/h** in the early afternoon, settling to around 15 km/h by evening. Morning winds are lighter at ~10 km/h.
>
> ⚠️ Moderately windy conditions expected midday — secure loose items and consider a windbreaker if you'll be outdoors.

---

## Warnings

Include warnings when conditions are notable:
- **Extreme heat:** temp ≥ 40°C
- **Extreme cold:** temp ≤ -10°C
- **Strong wind:** ≥ 50 km/h
- **Heavy rain:** ≥ 20mm precipitation

---

## Clothing Guidance

When travel intent is detected, read `references/clothing_guide.md` and include relevant advice in the response.

---

## Error Handling

- **Location not found:** Ask the user to be more specific (add city, country).
- **Ambiguous location:** Present the alternatives and ask which one.
- **API failure / network blocked:** Scripts return a JSON error envelope instead of a traceback:
  ```json
  {
    "error": {
      "code": "NETWORK_UNAVAILABLE",
      "message": "Unable to reach remote weather service.",
      "details": "URLError: ...",
      "retryable": true,
      "hint": "Enable outbound network access or rerun with elevated permissions."
    }
  }
  ```
- **Error codes:**
  - `INVALID_INPUT`: bad user input (invalid `past_days`, missing location, no results).
  - `NETWORK_UNAVAILABLE`: DNS/connectivity/timeouts to upstream weather APIs.
  - `UPSTREAM_API_ERROR`: upstream HTTP/API response issues.
- **Exit codes:**
  - `0`: success.
  - `1`: usage or input validation failures.
  - `2`: network/upstream API failures.
- **Operational guidance:** If network is blocked in a sandbox, request elevated permissions or run scripts from an environment with outbound internet access.
- **Beyond forecast horizon:** Inform them of the 16-day limit, return what's available.
- **No time specified:** Default to current + next 24 hours.
