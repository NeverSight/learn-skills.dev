---
name: tempest
description: >-
  Query hyper-local weather from a WeatherFlow Tempest station over its REST
  API and the hub's local UDP broadcast: current conditions, forecast,
  historical observations, and real-time decoded datagrams (obs_st,
  rapid_wind, evt_precip, evt_strike, hub_status). Use when the user asks
  about weather, temperature, rain, wind, humidity, or forecast data from
  their own Tempest/WeatherFlow station, or wants to parse the hub's UDP port
  50222 broadcast. Do not use this skill for generic or city forecasts
  without a Tempest station (public weather services serve those), for
  Shakespeare's play The Tempest or other literature questions, or for
  weather hardware from other vendors - the REST endpoints require a
  personal-use token and the UDP broadcast only exists on a Tempest hub's
  LAN.
license: MIT
compatibility: >-
  Requires TEMPEST_TOKEN env var for REST (create it in the Tempest web app
  under Settings -> Data Authorizations), Python 3.8+, and `requests`. UDP
  listening needs a Tempest hub on the LAN and no token. `--help` and
  `--dry-run` work without credentials.
metadata:
  tags: weather, tempest, weatherflow, forecast, station, udp, hyper-local
  sources: https://apidocs.tempestwx.com/reference/quick-start, https://weatherflow.github.io/Tempest/api/udp/v171/
---

# tempest — Hyper-local weather from your Tempest station

Drive a WeatherFlow Tempest station from the terminal. Two transports, both
first-class: the documented REST API (`swd.weatherflow.com/swd/rest`,
personal-use token) for conditions, forecast, and history — officially the
primary data source — and the hub's unauthenticated UDP broadcast on port
50222 for real-time, lowest-latency readings on your LAN. The bundled CLI
decodes the positional observation arrays and every UDP message family, keeps
`--json` output metric-native, and converts units only for human display.

## Setup

1. Create a personal access token: sign in to the Tempest web app
   (tempestwx.com), then **Settings → Data Authorizations → Create Token**.
   (This is the documented non-graphical auth method; OAuth exists for web
   apps but is not what a CLI uses.)
2. Export it:

```bash
export TEMPEST_TOKEN="<YOUR_TOKEN>"
```

The token travels to the API as a **query parameter** (`?token=...`) per the
official docs — the CLI handles this. If the env var is not set, the CLI
falls back to reading `TEMPEST_TOKEN=` from `~/.tempest.env` (handy for agent
subprocesses that skip shell profiles). `--help` and `--dry-run` never need a
token. UDP listening never needs one either — the hub broadcast is
unauthenticated and LAN-only.

## Essential Commands

### stations — discover your stations and devices

```bash
tempest stations                       # names, station ids, device types, serials
tempest stations --json | jq '.stations[] | {station_id, name,
  devices: [.devices[] | {device_id, device_type, serial_number}]}'
```

Every station response nests a `devices` array: `device_type` is `ST` (the
Tempest all-in-one), `AR`/`AIR`, `SK`/`SKY`, or `HB` (the hub — it has **no**
observations; always filter it out before querying observations). Run this
first when you don't know your ids.

### current — latest conditions

```bash
tempest current                                       # human-readable, converted
tempest current --json                                # metric-native, jq-ready
tempest current --station-id 12799 --device-id 60526  # pin exact hardware
```

With one station it auto-selects and picks the best sensor (`ST`, then
`SKY`/`SK`, then `AIR`/`AR`, skipping `HB`). Output `.observation` carries the
decoded positional array as named fields with `_unit` companions.

### forecast — current conditions + daily + hourly

```bash
tempest forecast                       # current + 5-day daily + next 12 hours
tempest forecast --days 7 --json
tempest forecast --station-id 12799 --days 3
```

The `better_forecast` response nests daily/hourly under a `forecast` wrapper
key, and it is unit-selectable (`units_temp=c|f` and friends, default metric)
— the CLI reads the response's `units` before converting anything.

### obs — historical observations

```bash
tempest obs --device-id 60526 --days 1       # last UTC day (day_offset)
tempest obs --device-id 60526 --days 7
tempest obs --device-id 60526 --json
```

`--days N` maps to the API's `day_offset` (whole UTC days). The underlying
endpoint also accepts `time_start`/`time_end` epoch ranges (one-minute
resolution guaranteed up to 5 days) — use raw calls for those; see
references/rest-api-and-auth.md.

## UDP broadcasts from your hub (port 50222, listen-only)

```bash
tempest udp listen                          # live stream until Ctrl-C
tempest udp listen --timeout 30             # auto-stop after 30s
tempest udp listen --timeout 60 --json      # one JSON object per datagram
tempest udp listen --show-all               # include hub_status/device_status
```

Requires being on the same LAN as the hub (routed connectivity is not enough
— broadcasts don't cross routers). No token involved. The listener decodes
every message family, dispatching on `type` before touching array positions:

| Family | Payload shape | Decoded fields |
|---|---|---|
| `obs_st` / `obs_air` / `obs_sky` | list of report rows under `obs` | named observation fields |
| `rapid_wind` | ONE 3-element array under `ob` | wind_speed_mps, wind_direction |
| `evt_precip` | ONE array under `evt` | timestamp (rain started) |
| `evt_strike` | ONE array under `evt` | distance_km, energy |
| `hub_status`, `device_status` | named fields, no array | uptime, rssi, seq, voltage, sensor_status |

## Multi-step pipeline recipes

### Discover, then observe

```bash
# Stage 1 -> stage 2: stations --json emits integer ids that current consumes
tempest stations --json | jq -r '.stations[].devices[]
  | select(.device_type == "ST") | .device_id' | head -1
tempest current --device-id <DEVICE_ID> --json
```

### Rain watch: yesterday's total, then live rain events

```bash
tempest obs --device-id 60526 --days 1 --json \
  | jq '{samples: (.observations | length),
         day_rain_mm: .observations[-1].local_day_rain_accumulation}'
tempest udp listen --timeout 600 --json | jq 'select(.type == "evt_precip")'
```

`obs --json` ends with decoded observations carrying
`local_day_rain_accumulation` (mm, number); `evt_precip` datagrams decode to
`{type, serial_number, timestamp}` — both stages emit typed fields the next
stage can consume.

### Unit-aware forecast slice

```bash
tempest forecast --days 7 --json \
  | jq '{units_temp: .forecast.units.units_temp,
         highs_f: [.forecast.forecast.daily[] | .air_temp_high * 9 / 5 + 32],
         rain_hours: [.forecast.forecast.hourly[]
                      | select(.precip_probability > 30) | .local_hour]}'
```

The jq math here is safe **only because** it checks `units_temp` first — see
gotcha 2.

## JSON output and jq processing

`--json` output is **metric-native** — the raw wire units (m/s wind, mm rain,
°C temperature, MB pressure) with `_unit` companion fields naming each.
Convert at the consumption edge:

```bash
tempest current --json | jq '{temp_c: .observation.air_temperature,
  temp_f: (.observation.air_temperature * 9 / 5 + 32),
  wind_mph: (.observation.wind_avg * 2.237),
  rain_in: (.observation.rain_accumulation / 25.4)}'
```

Global flags work in any position: `tempest --json current --device-id 60526`
and `tempest current --device-id 60526 --json` are identical. `--quiet`
silences the progress logs (data on stdout, logs on stderr).
`--dry-run` prints a plan object and exits 0 without touching the network.

## Known Gotchas

1. **Observations are positional arrays, not objects.** Raw `obs` rows have
   no field names; meaning comes from the index (obs_st: 0 epoch, 2 wind avg
   m/s, 4 wind direction, 6 pressure MB, 7 temperature °C, 12 rain mm, 16
   battery V, 17 report interval). Reading index 6 as temperature gives you a
   plausible-looking wrong number — decode with the CLI or the layout tables
   in references/observation-layouts-and-units.md.
2. **`/better_forecast` is unit-selectable, not Celsius-locked.** It defaults
   to metric but honors `units_temp=f`, `units_wind=mph`, `units_pressure=inhg`,
   `units_precip=in`. It reports what it used in `response.units`. Converting
   an already-Fahrenheit response doubles it (25.4 °C → 77.7 °F → 172 "°F").
   Always read `units` before converting; the CLI does this for you.
3. **UDP message families differ structurally — dispatch on `type` first.**
   obs families nest rows under `obs`; `rapid_wind` carries one array under
   `ob`; `evt_precip`/`evt_strike` carry one array under `evt`;
   `hub_status`/`device_status` carry named fields with no payload array.
   Iterating `rapid_wind`'s `ob` element-wise is the classic TypeError; the
   bundled `decode_message()` shows the correct dispatch.
4. **UDP obs_st rows stop at index 17; REST rows run to 21.** The four
   Nearcast/analysis fields (18–21) exist only in REST responses. Decoders
   must tolerate both lengths — the CLI emits `None` for missing tails.
5. **Pressure is MB (millibars), numerically hPa — not kPa.** It is also
   *station* pressure (raw sensor). The Tempest app's "relative pressure"
   adds an elevation adjustment; don't compare raw station pressure against
   the app and conclude the sensor drifted.
6. **Forecast timestamps are epoch integers, never ISO strings.**
   `day_start_local`, `sunrise`, `sunset`, hourly `time` are epoch seconds;
   hourly objects carry `local_hour` (0–23) and `local_day` (day of month).
   There is **no** `local_time` or `time_string` field — code expecting one
   silently falls back to its default branch.
7. **The forecast nests under a `forecast` wrapper key.** `data["daily"]` is
   always empty; read `data["forecast"]["daily"]` and
   `data["forecast"]["hourly"]` (the CLI's `--json` preserves the full
   response, wrapper and all).
8. **Hubs (`HB`) have no observations.** They only relay. Auto-selection
   skips them; if you call the API directly, filter `device_type == "HB"`
   out before hitting `/observations/device/{id}` (documented 404 otherwise).
9. **UDP is LAN-only and unauthenticated.** Broadcasts don't cross routers
   and can't be token-gated — anyone on the network can read your station.
   WeatherFlow officially positions REST/WebSocket as primary and UDP as the
   off-grid/backup interface.
10. **`obs_sky` UDP day-rain is always null.** Local-day rain accumulation
    (index 11) is `null` in UDP SKY broadcasts; REST supplies the real value.
    Don't build day-rain totals from UDP SKY rows.

## When to use

- The user owns or manages a WeatherFlow Tempest / Air / Sky station and asks
  about its readings, forecast, or history.
- Parsing or integrating with the hub's local UDP broadcast (port 50222).
- Rain/wind/lightning monitoring scripts, dashboards, or home-automation
  hooks fed from the station.

## When not to use

- **Generic city forecasts or users without a station** — every endpoint
  requires the user's own Tempest station and a personal-use token; use a
  public weather service instead.
- **Shakespeare's play *The Tempest*, or any literary/meteorological-theory
  question** — this is a station-data CLI, not an encyclopedia.
- **Other vendors' hardware** (Netatmo, Ecowitt, Davis, Ambient) — different
  APIs entirely; no endpoint here will accept their devices.
- **Commercial/network-wide data products** — those need WeatherFlow's
  TempestONE agreements, not a personal token (see the remote developer
  policy).

## Reference Files

| File | Read when |
|---|---|
| [references/rest-api-and-auth.md](references/rest-api-and-auth.md) | Working with REST endpoints directly: token auth, StationSet shapes, observation parameters, forecast units, error signatures |
| [references/udp-broadcast-protocol.md](references/udp-broadcast-protocol.md) | Parsing raw UDP datagrams: port 50222 transport, every message family's layout, the type-dispatch rule |
| [references/observation-layouts-and-units.md](references/observation-layouts-and-units.md) | Decoding positional observation arrays by index (obs_st/obs_air/obs_sky, UDP vs REST lengths) and unit conversion tables |
| [references/cli-worked-recipes.md](references/cli-worked-recipes.md) | Copy-paste multi-step CLI recipes with jq stages, dry-run plans, and expected error paths |

## Available Scripts

- [scripts/tempest](scripts/tempest) — the CLI: `stations`, `current`, `obs`,
  `forecast`, `udp listen`; global `--json`, `--dry-run`, `--quiet`,
  `--verbose` accepted in any position; offline dry-run plans for every
  command.
- [scripts/test_tempest.py](scripts/test_tempest.py) — offline suite: canned
  UDP datagram bytes fed to the decoder (no sockets), mocked REST transport,
  both pytest and unittest runners.

## Prerequisites

- Python 3.8+ with `requests` (the only dependency).
- `TEMPEST_TOKEN` for REST commands (free, personal use; created in the
  Tempest web app). UDP listening needs no token, only line-of-sight to the
  hub's LAN.
