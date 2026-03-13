---
name: gmaps-leads
description: Scrape Google Maps for B2B leads with deep website enrichment and contact extraction. Use when user asks to find local businesses, scrape Google Maps, generate contractor lists, or build local service business databases.
---

# Google Maps Lead Generation

## Goal
Generate high-quality B2B leads from Google Maps with deep contact enrichment by scraping websites and using Claude to extract structured contact data.

## Inputs
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--search` | Yes | Search query (e.g., "plumbers in Austin TX") |
| `--limit` | No | Max results (default: 10) |
| `--sheet-url` | No | Existing sheet to append to |
| `--workers` | No | Parallel workers (default: 3) |

## Scripts
- `./scripts/gmaps_lead_pipeline.py` - Main orchestration
- `./scripts/gmaps_parallel_pipeline.py` - Parallel version
- `./scripts/scrape_google_maps.py` - Google Maps scraper
- `./scripts/extract_website_contacts.py` - Website contact extractor
- `./scripts/update_sheet.py` - Google Sheets sync

## Process

### Basic Usage
```bash
# Create new sheet with 10 leads
python3 ./scripts/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 10

# Append to existing sheet (recommended for building database)
python3 ./scripts/gmaps_lead_pipeline.py --search "dentists in Miami FL" --limit 25 \
  --sheet-url "https://docs.google.com/spreadsheets/d/..."

# Higher volume
python3 ./scripts/gmaps_lead_pipeline.py --search "roofing contractors in Austin TX" \
  --limit 50 --workers 5
```

## Pipeline Steps

1. **Google Maps Scrape** - Apify `compass/crawler-google-places` returns listings
2. **Website Scraping** - Fetches main page + up to 5 contact pages
3. **Web Search Enrichment** - DuckDuckGo search for owner contact info
4. **Claude Extraction** - Claude 3.5 Haiku extracts structured contacts
5. **Google Sheet Sync** - Appends new leads, deduplicates by lead_id

## Output Schema (36 fields)

**Business Basics:** business_name, category, address, city, state, zip_code, phone, website, rating, review_count

**Extracted Contacts:** emails, additional_phones, business_hours

**Social Media:** facebook, twitter, linkedin, instagram, youtube, tiktok

**Owner Info:** owner_name, owner_title, owner_email, owner_phone, owner_linkedin

**Team Contacts:** JSON array of team members

**Metadata:** lead_id, scraped_at, search_query, pages_scraped, enrichment_status

## Cost
| Component | Per Lead |
|-----------|----------|
| Apify Google Maps | ~$0.01-0.02 |
| Claude Haiku | ~$0.002 |
| DuckDuckGo/HTTP | Free |
| **Total** | **~$0.012-0.022** |

For 100 leads: ~$1.50-2.50 total

## Troubleshooting

- **"No businesses found"**: Include location in query
- **403 Forbidden**: ~10-15% of sites block scrapers (handled gracefully)
- **Auth issues**: Delete `token.json` and re-authenticate
- **Duplicates**: Uses lead_id (MD5 of name|address) for deduplication

## Environment
```
APIFY_API_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `search` | string | Yes | Search query (e.g., 'plumbers in Austin TX') |
| `limit` | integer | No | Max results (default: 10) |
| `sheet_url` | string | No | Existing sheet to append to |
| `workers` | integer | No | Parallel workers (default: 3) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Google Sheet URL with 36-field lead data |
| `lead_count` | integer | Number of leads scraped |

### Credentials
| Name | Source |
|------|--------|
| `APIFY_API_TOKEN` | .env |
| `ANTHROPIC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `classify-leads`, `casualize-names`, `instantly-campaigns`, `onboarding-kickoff`

### Cost
$0.012-0.022 per lead
