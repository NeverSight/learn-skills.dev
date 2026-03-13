---
name: aviation-weather
description: Fetch aviation weather data (METAR, TAF, PIREPs, SIGMETs) from NOAA. Use when user asks about airport weather, flight conditions, aviation forecasts, pilot reports, or weather briefings for flying. Supports any ICAO airport code worldwide.
---

# Aviation Weather

CLI tool for aviation weather data from NOAA Aviation Weather Center. No API key required.

## Quick Start

```bash
# Current conditions
avwx metar KHSV

# Forecast
avwx taf KJFK

# Full briefing
avwx brief KHSV,KMDQ
```

## Commands

### METAR (Current Conditions)
```bash
avwx metar KHSV              # Single station
avwx metar KHSV,KBHM,KMSL    # Multiple stations
avwx metar KHSV --hours 3    # Last 3 hours
avwx metar KHSV --raw        # Raw METAR text
avwx metar KHSV --json       # JSON output
```

Output includes: flight category (VFR/MVFR/IFR/LIFR), wind, visibility, clouds, temperature, altimeter.

### TAF (Forecast)
```bash
avwx taf KJFK                # Terminal forecast
avwx taf KHSV,KBHM           # Multiple stations
avwx taf KJFK --raw          # Raw TAF text
```

Shows forecast periods with wind, visibility, and cloud conditions.

### PIREP (Pilot Reports)
```bash
avwx pirep                   # Recent PIREPs
avwx pirep --hours 4         # Last 4 hours
avwx pirep --limit 50        # More results
```

Includes turbulence, icing, and weather observations from pilots.

### SIGMET/AIRMET
```bash
avwx sigmet                  # All active
avwx sigmet --hazard TURB    # Turbulence only
avwx sigmet --hazard ICE     # Icing only
avwx sigmet --hazard CONVECTIVE  # Thunderstorms
```

### Full Briefing
```bash
avwx brief KHSV              # Complete weather briefing
avwx brief KHSV,KMDQ,KBHM    # Multi-airport briefing
```

Combines METAR, TAF, and active SIGMETs in one report.

## Flight Categories

| Category | Ceiling | Visibility | Color |
|----------|---------|------------|-------|
| **VFR** | >3000ft | >5 SM | Green |
| **MVFR** | 1000-3000ft | 3-5 SM | Blue |
| **IFR** | 500-1000ft | 1-3 SM | Red |
| **LIFR** | <500ft | <1 SM | Magenta |

## Common ICAO Codes

Use 4-letter ICAO codes (not FAA LIDs):
- US airports: Add K prefix (HSV → KHSV, LAX → KLAX)
- Alaska: PA prefix (PANC = Anchorage)
- Hawaii: PH prefix (PHNL = Honolulu)
- International: varies (EGLL = London Heathrow, LFPG = Paris CDG)

## Data Source

All data from NOAA Aviation Weather Center (aviationweather.gov). Updated every minute for METARs, every 6 hours for TAFs.

## Installation

No dependencies required (uses Python stdlib only).

```bash
chmod +x scripts/avwx.py
# Optional: symlink to PATH
ln -s $(pwd)/scripts/avwx.py /usr/local/bin/avwx
```
