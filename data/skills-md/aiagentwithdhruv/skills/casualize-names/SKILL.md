---
name: casualize-names
description: Convert formal names to casual versions for cold email personalization - first names, company names, and city names. Use when user asks to casualize names, make names friendly, or prepare lead data for emails.
---

# Casualize Names Workflow

## Goal
Convert formal names (first names, company names, cities) to casual, friendly versions suitable for cold email copy.

## Scripts
- `./scripts/casualize_batch.py` - Main script (all 3 fields at once)
- `./scripts/casualize_company_names_batch.py` - Company names only
- `./scripts/casualize_first_names_batch.py` - First names only
- `./scripts/casualize_city_names_batch.py` - City names only

## Quick Start

```bash
# Process all three fields at once (recommended, 3x faster)
python3 -u ./scripts/casualize_batch.py "GOOGLE_SHEET_URL"

# Re-process existing (overwrite)
python3 -u ./scripts/casualize_batch.py "GOOGLE_SHEET_URL" --overwrite
```

## How It Works
1. Processes records in batches of 50
2. Uses 5 parallel workers
3. Claude converts all three fields in one API call
4. Batch updates Google Sheet with results
5. Only processes rows with emails

**Performance**: ~35 records/sec (3,000 records ≈ 90 seconds)

## Casualization Rules

### First Names
- Use common nicknames: "William" → "Will", "Jennifer" → "Jen"
- Keep original if no common nickname exists
- Keep it professional

### Company Names
- Remove "The" at beginning
- Remove legal suffixes (LLC, Inc, Corp, Ltd)
- Remove generic words (Realty, Group, Solutions, Services)
- Keep core brand name
- Use "you guys" for overly generic names

**Examples:**
- "Keller Williams Realty Inc" → "Keller Williams"
- "The Teal Umbrella Family Dental Healthcare" → "Teal Umbrella"

### City Names
- Use local nicknames: "San Francisco" → "SF", "Philadelphia" → "Philly"
- Keep original if no common nickname

## Output
Creates three new columns:
- `casual_first_name`
- `casual_company_name`
- `casual_city_name`

## Environment
```
ANTHROPIC_API_KEY=your_key
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sheet_url` | string | Yes | Google Sheet URL with lead data |
| `overwrite` | boolean | No | Re-process existing casualized names |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Same sheet with casual_first_name, casual_company_name, casual_city_name columns added |

### Credentials
| Name | Source |
|------|--------|
| `ANTHROPIC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `scrape-leads`, `gmaps-leads`, `instantly-campaigns`

### Cost
~35 records/sec, minimal API cost
