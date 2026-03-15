---
name: get-weather-forecast
description: "Retrieve current weather conditions and multi-day forecasts for any location using the wttr.in API. Use this skill when the user asks for weather information, weather forecast, current conditions, temperature, or weather updates for a specific city or location. Provides detailed weather data including temperature, wind, precipitation, and visibility."
tags: [weather, api, information-retrieval, forecast, climate, auto-generated]
version: 0.1.0
---

# Skill: get-weather-forecast

## When to Use
Use this skill when the user asks to:
- Get the weather for a location
- Check the weather forecast
- Look up current conditions
- Get temperature and wind information
- Retrieve a multi-day weather forecast
- Check if it will rain or snow
- Get weather updates for a city

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `location` | Yes | The city or location name to retrieve weather for | Sydney |

## Procedure
1. Extract the location name from the user's request (e.g., Sydney, London, New York)
2. Execute the curl command: curl wttr.in/{{LOCATION}}
3. Parse the response to extract key weather data: current conditions, temperature, wind speed, visibility, and multi-day forecast
4. Format the weather information in a readable way for the user, highlighting current conditions and upcoming forecast
5. Report the complete weather summary including today's forecast and next 2-3 days

## Bundled Scripts

| Script | Type | Description |
|--------|------|-------------|
| `scripts/run.sh` | SH | Execute API call |

### Script Usage

```bash
bash scripts/run.sh
```

Credentials in scripts use environment variables. Set them via `get_keys` before running.

## Example

Example requests that trigger this skill:

```
curl wttr.in/Sydney
```
