---
name: generate-report
description: Generate weekly weather reports for Canada using Open-Meteo API (free, no API key required) and PDF generation. Use when user asks to create a weather report, generate Canada weather summary, or build weekly weather PDF.
---

# Canada Weekly Weather Report Generator

## Goal
Generate a professional PDF weather report for Canada using real-time data from Open-Meteo API (free, no API key required). The report uses the "Orange and Black Modern Annual Report" template style.

## Inputs
- **Week Start Date** (optional): Start date for the report period (defaults to current week)
- **Cities** (optional): List of Canadian cities to include (defaults to major cities)

## Default Canadian Cities
The report covers these major cities by default:
- **West Coast**: Vancouver, Victoria
- **Prairies**: Calgary, Edmonton, Winnipeg
- **Central**: Toronto, Ottawa, Montreal
- **Atlantic**: Halifax, St. John's
- **North**: Whitehorse, Yellowknife

## Scripts
All scripts are in `./scripts/`:
- `fetch_weather.py` - Fetches weather data from Open-Meteo API (no API key needed)
- `generate_report_pdf.py` - Generates the styled PDF report

## Process

### 1. Fetch Weather Data
```bash
python3 ./scripts/fetch_weather.py --output .tmp/canada_weather.json
```

Optional parameters:
- `--cities "Vancouver,Toronto,Montreal"` - Custom city list
- `--days 7` - Number of forecast days (default: 7, max: 16)

### 2. Generate PDF Report
```bash
python3 ./scripts/generate_report_pdf.py \
  --input .tmp/canada_weather.json \
  --output .tmp/canada_weekly_weather_report.pdf \
  --template ".tmp/Orange and Black Modern Annual Report.pdf"
```

### 3. Review and Deliver
- Open `.tmp/canada_weekly_weather_report.pdf` to verify
- Upload to Google Drive or send via email if requested

## Report Structure (Matching Template)
1. **Cover Page**: "Canada Weekly Weather Report" with date range
2. **Table of Contents**: Regional sections listed
3. **National Overview**: Summary of weather patterns across Canada
4. **Regional Highlights**: Key metrics (avg temp, precipitation, extremes)
5. **West Coast Weather**: Vancouver, Victoria details
6. **Prairies Weather**: Calgary, Edmonton, Winnipeg details
7. **Central Canada Weather**: Toronto, Ottawa, Montreal details
8. **Atlantic Weather**: Halifax, St. John's details
9. **Northern Territories**: Whitehorse, Yellowknife details
10. **7-Day Outlook**: Forecast summary with trends
11. **Weather Alerts**: Any active warnings/advisories
12. **Data Sources**: Open-Meteo attribution

## Output
**Primary deliverable**: PDF report at `.tmp/canada_weekly_weather_report.pdf`

The report includes:
- Current conditions for each city
- 7-day forecast with highs/lows
- Precipitation amounts
- Regional comparisons

## Error Handling
- **City not found**: Skip city, log warning, continue
- **Network error**: Retry up to 3 times with backoff
- **Missing data**: Use "N/A" placeholders

## Environment
**No API key required!** Open-Meteo is free and open-source.

Data source: https://open-meteo.com/

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `week_start_date` | string | No | Start date for report period (defaults to current week) |
| `cities` | string | No | Comma-separated list of Canadian cities |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `pdf_path` | file_path | PDF report at .tmp/canada_weekly_weather_report.pdf |

### Cost
Free (Open-Meteo API)
