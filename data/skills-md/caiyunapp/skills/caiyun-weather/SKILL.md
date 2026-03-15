---
name: caiyun-weather
description: Query Caiyun comprehensive weather data by latitude and longitude. Returns realtime weather, minutely precipitation guidance, hourly forecast, daily forecast, life index cues, and sky condition interpretation. Use when the user asks to check weather, next 2 hours rain, hourly or daily forecast, life index, precipitation intensity, weather codes, or Caiyun weather API data.
license: MIT
compatibility: Requires python3 and internet access.
argument-hint: For example, check the weather for 116.3176,39.9760, or show the next 24 hours in Shanghai
allowed-tools: ["Bash(python3:*)", "Read"]
---

# Caiyun Weather

## Prerequisites

- Get API access and your API key from https://docs.caiyunapp.com/weather-api/.
- The skill reads credentials from `CAIYUN_WEATHER_API_TOKEN` environment variable first, then `~/.config/caiyunapp/config.json` (JSON object with key `caiyun_weather_api_token`).
- Requires coordinates. Ask for latitude and longitude if they are missing.

## Quick Start

```bash
python3 skills/caiyun-weather/scripts/query_weather.py --lon 116.3176 --lat 39.9760 --hourlysteps 24 --dailysteps 5
```

## Workflow

1. Confirm coordinates are available.
2. Confirm credentials are available through `CAIYUN_WEATHER_API_TOKEN` or the local config file.
3. Run the helper script:

```bash
python3 skills/caiyun-weather/scripts/query_weather.py --lon <lon> --lat <lat> --hourlysteps 24 --dailysteps 5
```

4. Summarize results in this order when relevant:
   - current conditions from `result.realtime`
   - near-term change from `result.forecast_keypoint`
   - 24-hour trend from `result.hourly.description`
   - daily highs, lows, or sky conditions from `result.daily`
5. Return raw JSON only when the user asks for it.

## Defaults

- Returned values are interpreted using the code's fixed unit settings.
- Use `hourlysteps=24` unless the user requests a different horizon.
- Use `dailysteps=5` unless the user requests a different day count.

## Failure Handling

- If credentials are missing, explain how to set `CAIYUN_WEATHER_API_TOKEN` or create `~/.config/caiyunapp/config.json` with `{"caiyun_weather_api_token": "<your_token>"}`.
- If coordinates are missing, ask for latitude and longitude.
- If the API response status is not `ok`, report the HTTP status and API status payload.

## Additional Resources

- [reference.md](reference.md)
- [examples.md](examples.md)
