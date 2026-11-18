---
name: weather
description: Gets weather and air quality for any place without an API key from Open-Meteo - current conditions, an hourly and daily forecast up to 16 days (temperature, feels-like, rain and its chance, wind and gusts, UV, sunrise and sunset), past weather for any day since 1940, and air quality now and ahead (European and US AQI, PM2.5, PM10, ozone, NO2, pollen) - for a city, address, landmark or coordinates, with the resolved place shown. Use when the user asks about the weather, temperature, rain, snow or wind, a forecast for a place or date, what the weather was on a past date or in a past month, whether to take an umbrella or how to dress, or whether the air is clean or safe to run or go outside, AQI, PM2.5, smog or pollen today ("какая погода в", "будет ли дождь", "какой сейчас воздух"). Not for severe-weather warnings, climate facts or classifications (wiki-lookup), climate projections, marine or aviation forecasts.
license: MIT
compatibility: Python 3.12+ (standard library only; uv optional); macOS, Linux, Windows. Needs network access to api.open-meteo.com, archive-api.open-meteo.com, air-quality-api.open-meteo.com and geocoding-api.open-meteo.com, plus nominatim.openstreetmap.org for addresses and landmarks. The free tier is for non-commercial use only (600 calls/min, 5,000/hour, 10,000/day, 300,000/month); OPEN_METEO_API_KEY switches to the commercial API.
metadata:
  author: zedxter
  version: "1.0.0"
  source: https://github.com/zedxter/utility-belt
---

# Weather

Weather from [Open-Meteo](https://open-meteo.com), which serves national
weather models and the ERA5 reanalysis through one key-less API. The script
resolves the place, asks the right endpoint in the place's local time zone,
and prints a compact table or JSON.

- **Forecast:** now, then up to 16 days, and hour by hour on request.
- **History:** any day since 1 January 1940, with a summary: mean highs and
  lows, total precipitation, wet days, hottest and coldest day. Long ranges
  also get monthly rows.
- **Air quality:** European and US AQI with their levels, PM2.5, PM10, ozone,
  NO2, SO2 and UV, plus pollen in Europe. The daily worst AQI is shown for
  the coming days.

Every answer starts with the place it resolved to: name, region, country,
coordinates, elevation and time zone. When a name is ambiguous, check that
line before you answer.

## When to use

- "What's the weather in X", "do I need a jacket", "weekend forecast" → the
  default command.
- "Will it rain this afternoon / tomorrow" → `--hours 24` / `--hours 48`.
- "What was the weather on 12 June 2019", "how hot was last July" →
  `history`. For "is this November unusually warm", compare with a
  30-year baseline (`history PLACE --from 1991-11-01 --to 2020-11-30`; its
  monthly rows give the normal range).
- "Is the air bad today", "can I run outside", "smog", "pollen" → `air`.

Not for:
- severe-weather warnings or alerts (those come from national weather
  services);
- climate facts and classifications (Köppen, climate zones) → `wiki-lookup`;
- climate projections;
- marine, surf or aviation (METAR/TAF) forecasts.

## Quick start

The script is `scripts/weather.py` relative to this skill. It uses only the
standard library.

```bash
uv run scripts/weather.py Berlin                                   # now + 7 days
uv run scripts/weather.py "Paris, Texas" --days 3 --hourly --hours 12
uv run scripts/weather.py 40.71,-74.01 --units imperial
uv run scripts/weather.py "Eiffel Tower" --days 1                  # landmarks go through OpenStreetMap
uv run scripts/weather.py history Moscow --from 2024-07-01 --to 2024-07-31
uv run scripts/weather.py air Delhi
```

Output of the first command (shortened):

```
# Berlin, State of Berlin, Germany · 52.53°N 13.42°E · 46 m · Europe/Berlin (GMT+1)
now (20:00): 8.6°C, feels 6.8°C · Light drizzle · wind 8 km/h WNW (gusts 18) · humidity 95% · 1032 hPa

date       weather     min/max °C  feels  precip mm (chance)  wind/gusts km/h  UV   sun
Fri 10-30  Light rain  7 / 9       5 / 8  0.0 (0%)            10/22 WNW        2.1  06:58–16:40
Sat 10-31  Light rain  6 / 11      4 / 9  0.0 (3%)            11/27 NNW        2.1  07:00–16:38

model: best_match (Open-Meteo's regional blend of national models) · Weather data by Open-Meteo.com (CC BY 4.0) · free tier for non-commercial use
```

## Places

- **Name:** `"Berlin"`. The most prominent match is taken. When another
  place of that name is comparable in size, a `note:` lists the others.
- **Name with region or country:** `"Paris, Texas"`, `"Springfield,
  Illinois"`, `"Valencia, Venezuela"`. Only matches whose region or country
  fits are kept. `--country US` does the same with a code.
- **Addresses, landmarks, districts** that the place index lacks fall back to
  OpenStreetMap Nominatim, and the output credits it.
- **Region and country codes:** US state codes (`Salem, IN` is Indiana),
  Canadian province codes (`Victoria, BC`), and country codes (`Paris, FR`,
  `London, UK`).
- **Coordinates:** `52.52,13.41` or `-33.87,151.21`, latitude first, in
  decimal degrees. Decimal commas also work: `52,52 13,41`.
- `--lang de` gives place names in another language. Weather descriptions
  stay in English.

The output shows the model's grid point. It can be a few kilometres from the
place, and its elevation can differ in the mountains.

## Options

| Command / flag | Default | Meaning |
|---|---|---|
| `PLACE` (or `forecast PLACE`) | — | Current conditions and a daily forecast. Use `forecast` explicitly if the place is called "history" or "air". |
| `--days N` | 7 | Forecast days, 1–16. For `air`: 1–7, default 3. |
| `--hourly`, `--hours N` | off, 24 | Add an hourly table for the next N hours (1–384), starting at the current hour, with temperature, feels-like, precipitation, its chance and wind. `--hours` alone implies `--hourly`. For `history`, `--hourly` covers ranges up to 7 days. |
| `--model NAME` | `best_match` | `best_match` lets Open-Meteo pick the best model for the place. Others: `ecmwf_ifs025`, `icon_seamless` (DWD), `gfs_seamless` (NOAA), `meteofrance_seamless`, `ukmo_seamless`, `jma_seamless`, `gem_seamless`. Some models do not provide every field, so columns such as rain chance or UV can show `–`. |
| `history PLACE --from D [--to D]` | `--to` = `--from` | Daily rows for up to 62 days, monthly rows beyond. Ranges run from 1940-01-01 to today. |
| `air PLACE` | — | Air quality now and the daily maximum AQI ahead. |
| `--units` | `metric` | `imperial` gives °F, mph and inches (two decimals). Not for `air`, whose units are the same everywhere. |
| `--country CC`, `--lang` | —, `en` | Restrict the place search; name language. |
| `-f` | `table` | `markdown` (tables for a chat or document) or `json`. |
| `-o FILE`, `--timeout S`, `-q` | —, 30, off | Write to FILE; network timeout; hide `note:` lines. |

## JSON output

Shapes, values shortened:

```jsonc
// forecast
{"kind": "forecast",
 "place": {"name": "Berlin", "admin1": "State of Berlin", "country": "Germany", "country_code": "DE",
           "latitude": 52.52, "longitude": 13.41, "grid_latitude": 52.53, "grid_longitude": 13.42,
           "elevation": 46.0, "timezone": "Europe/Berlin", "timezone_abbreviation": "GMT+1",
           "source": "Open-Meteo geocoding (GeoNames)", "alternatives": ["Berlin, New Hampshire, United States"]},
 "units": {"temperature_2m": "°C", "wind_speed_10m": "km/h", "precipitation": "mm", ...},
 "model": "best_match",
 "current": {"time": "2026-10-30T20:00", "temperature_2m": 8.6, "apparent_temperature": 6.8, "weather_code": 51,
             "weather": "Light drizzle", "wind_speed_10m": 8.0, "wind_from": "WNW", "wind_gusts_10m": 18.0,
             "relative_humidity_2m": 95, "precipitation": 0.1, "cloud_cover": 100, "pressure_msl": 1032.0, "is_day": 0, ...},
 "daily": [{"date": "2026-10-30", "weather": "Light rain", "temperature_2m_min": 7.0, "temperature_2m_max": 9.0,
            "precipitation_sum": 0.0, "precipitation_probability_max": 0, "wind_speed_10m_max": 10.0, "wind_from": "WNW",
            "apparent_temperature_min": 4.0, "apparent_temperature_max": 7.0, "wind_gusts_10m_max": 30.0,
            "uv_index_max": 2.1, "sunrise": "2026-10-30T06:58", "sunset": "2026-10-30T16:40",
            "daylight_duration": 35000.0, ...}],
 "hourly": [{"time": "2026-10-30T21:00", "temperature_2m": 8.4, "precipitation_probability": 10, "weather": "...", ...}],
 "attribution": "Weather data by Open-Meteo.com (CC BY 4.0)"}
// history
{"kind": "history", "place", "units", "from": "2024-07-01", "to": "2024-07-31",
 "summary": {"days": 31, "days_with_data": 31, "mean_temperature", "mean_max", "mean_min",
             "hottest": {"date", "temperature_2m_max"}, "coldest": {"date", "temperature_2m_min"},
             "precipitation_total", "wet_days"},
 "daily": [{"date", "weather", "temperature_2m_min", "temperature_2m_max", "temperature_2m_mean",
            "precipitation_sum", "snowfall_sum", "wind_speed_10m_max", "sunshine_hours"}],
 "hourly": [{"time", "temperature_2m", "apparent_temperature", "precipitation", "weather", ...}],   // with --hourly
 "monthly": [{"month": "2024-07", "mean_max", "mean_min", "precipitation_total", "wet_days"}],   // ranges over 62 days
 "note": "the last days are preliminary ...",                                                  // ranges ending in the last 5 days
 "dataset", "attribution"}
// air
{"kind": "air", "place", "units",
 "current": {"time", "european_aqi": 56, "european_aqi_level": "moderate", "us_aqi": 62, "us_aqi_level": "moderate",
             "pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide", "uv_index"},
 "pollen": {"birch": 3.0, "grass": 12.0} | null,
 "daily": [{"date", "european_aqi_max", "european_aqi_level", "us_aqi_max", "us_aqi_level", "pm2_5_max"}],
 "model", "attribution"}
```

All times are the place's local time. Units follow `--units` and are listed
in `units`. A wet day has at least 1 mm (0.04 inch). In the table, the sun
column says "polar night" or "polar day" when the sun does not rise or set.

## Workflow for the agent

1. **Use the place the user means.** If the `note:` lists alternatives, or
   the header names a different country than the conversation suggests, run
   again with `"Name, Region"` or `--country`. Mention the resolved place in
   your answer ("Paris, Texas").
2. **Answer the question, not the table.**
   - "Umbrella?": the precipitation chance and amount for the hours that
     matter. Use `--hours 48` when the question is about tomorrow.
   - "What to wear?": the feels-like temperatures (the daily "feels" column),
     the gusts and the rain.
   - Give numbers with units, in the user's convention: `--units imperial`
     for US users.
3. **Forecasts are model output.** Beyond about 7 days they are rough
   trends. Say so when giving days 8–16. `best_match` blends national models
   by region; for a second opinion, use `--model ecmwf_ifs025` or
   `--model gfs_seamless`.
4. **History is reanalysis, not a station record.** ERA5 is a 25 km grid
   (ERA5-Land 0.1°, about 11 km). It smooths extremes and local effects such as cities,
   coasts and valleys. For official records, point to the national weather
   service. The last 5 days are preliminary.
5. **Air quality is a CAMS model forecast**, not a sensor reading. Pollen is
   only available in Europe, in season.
6. **Credit Open-Meteo** ("weather data by Open-Meteo.com") when you publish
   the numbers. The free tier is for non-commercial use; a commercial product
   needs an Open-Meteo API key (`OPEN_METEO_API_KEY`).
7. **On exit 4, stop.** The free-tier limits are in the compatibility line
   above. Don't loop over many places or dates: one `history` call covers a
   whole range.

## Exit codes

One `error:` line on stderr with a hint after `—`.

| Exit | Meaning | What to do |
|------|---------|------------|
| 0 | Done. | — |
| 1 | The place was not found. | Check the spelling, add the region or country, or give lat,lon. |
| 2 | Bad input: an empty place, numbers that are not a lat,lon pair, coordinates out of range, `--days`/`--hours` out of range, a bad date or a date outside 1940..today, `--hourly` history over 7 days, a bad `--lang`/`--country`/`--model`, or a parameter Open-Meteo rejects (its reason is shown). | Fix the argument. |
| 4 | Rate-limited by Open-Meteo (HTTP 429), or Nominatim refused an address lookup. | Wait; do not loop. For addresses, give lat,lon. |
| 6 | Network error, or Open-Meteo down (5xx). | Retry later. |
| 7 | An unexpected answer, a rejected `OPEN_METEO_API_KEY`, or a bug. | Read the message. |
| 130 | Interrupted. | — |

## Limitations

- **No warnings or alerts.** Severe-weather warnings come from national
  services (DWD, Météo-France, NWS…), not from these models.
- **The model grid is coarse.** Point forecasts in mountains, on coasts and
  in cities can be off by several degrees.
- **History before 1950 is less certain.** ERA5 assimilates fewer
  observations for that period.
- **Pollen covers Europe only.** Air-quality resolution is about 45 km
  globally and 11 km in Europe.
- **Weather descriptions are English.** They come from the WMO weather code;
  `--lang` changes only place names.
- **Licences.** Open-Meteo data is CC BY 4.0; OpenStreetMap place results
  are ODbL. The output credits both.

## Chaining

- `weather history` + `pdf-typeset` → a one-page climate summary for a trip
  or report.
- `wiki-lookup entity CITY --props P625` gives coordinates for a place whose
  name is ambiguous.
