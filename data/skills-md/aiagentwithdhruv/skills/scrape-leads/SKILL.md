---
name: scrape-leads
description: Scrape and verify business leads using Apify, classify with LLM, enrich emails, and save to Google Sheets. Use when user asks to find leads, scrape businesses, generate prospect lists, or build lead databases for any industry or location.
---

# Lead Scraping & Verification

## Goal
Scrape leads using Apify (`code_crafter/leads-finder`), verify their relevance (industry match > 80%), and save them to a Google Sheet. For large scrapes (1000+ leads), use parallel scraping for 3-5x faster performance.

## Inputs
- **Industry**: The target industry (e.g., "Plumbers", "Software Agencies")
- **Location**: The target location (e.g., "Texas", "United States", "California"). Scripts auto-format to Apify's required format (US states get ", us" suffix automatically).
- **Total Count**: The total number of leads desired

## Scripts
All scripts are in `./scripts/`:
- `scrape_apify.py` - Single scrape, for <1000 leads
- `scrape_apify_parallel.py` - Parallel scraping, for 1000+ leads
- `classify_leads_llm.py` - LLM-based lead classification
- `enrich_emails.py` - Email enrichment via AnyMailFinder
- `update_sheet.py` - Batch sheet updates
- `read_sheet.py` - Read data from Google Sheets

## Process

### Small Scrapes (<1000 leads)

1. **Test Scrape**
   ```bash
   python3 ./scripts/scrape_apify.py --query "INDUSTRY" --location "LOCATION" --max_items 25 --no-email-filter --output .tmp/test_leads.json
   ```

2. **Verification**
   - Read `.tmp/test_leads.json`
   - Check if at least 20/25 (80%) leads match the Industry
   - **Pass**: Proceed to step 3
   - **Fail**: Stop and ask user to refine keywords

3. **Full Scrape**
   ```bash
   python3 ./scripts/scrape_apify.py --query "INDUSTRY" --location "LOCATION" --max_items TOTAL_COUNT --no-email-filter --output .tmp/leads.json
   ```

4. **[Optional] LLM Classification** (for complex niches)
   ```bash
   python3 ./scripts/classify_leads_llm.py .tmp/leads.json --classification_type product_saas --output .tmp/classified_leads.json
   ```

5. **Upload to Google Sheet**
   ```bash
   python3 ./scripts/update_sheet.py .tmp/leads.json --title "Leads - INDUSTRY"
   ```

6. **Enrich Missing Emails**
   ```bash
   python3 ./scripts/enrich_emails.py SHEET_URL
   ```

### Large Scrapes (1000+ leads)

1. **Test Scrape** (same as above with 25 items)

2. **Parallel Full Scrape**
   ```bash
   python3 ./scripts/scrape_apify_parallel.py \
     --query "INDUSTRY" \
     --total_count 4000 \
     --location "United States" \
     --strategy regions \
     --no-email-filter
   ```

   Geographic partitioning is automatic:
   - **United States**: 4-way (Northeast, Southeast, Midwest, West)
   - **EU/Europe**: 4-way (Western, Southern, Northern, Eastern)
   - **UK**: 4-way (SE England, N England, Scotland/Wales, SW England)
   - **Canada**: 4-way (Ontario, Quebec, West, Atlantic)
   - **Australia**: 4-way (NSW, VIC/TAS, QLD, WA/SA)

3. Continue with steps 4-6 from small scrapes

## Outputs
**The ONLY deliverable is the Google Sheet URL.** Local JSON files in `.tmp/` are temporary intermediates.

## Edge Cases
- **No leads found**: Ask user to broaden search
- **API Error**: Check credentials in `.env`
- **Low quality classifications**: If >80% "unclear", improve scrape keywords

## Environment
Requires in `.env`:
```
APIFY_API_TOKEN=your_token
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
ANTHROPIC_API_KEY=your_key
ANYMAILFINDER_API_KEY=your_key
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `industry` | string | Yes | Target industry (e.g., 'Plumbers', 'Software Agencies') |
| `location` | string | Yes | Target location (e.g., 'Texas', 'United States') |
| `total_count` | integer | Yes | Total number of leads desired |
| `classification_type` | string | No | LLM classification type (e.g., 'product_saas') |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Google Sheet URL with scraped leads |
| `lead_count` | integer | Number of leads found |

### Credentials
| Name | Source |
|------|--------|
| `APIFY_API_TOKEN` | .env |
| `GOOGLE_APPLICATION_CREDENTIALS` | .env |
| `ANTHROPIC_API_KEY` | .env |
| `ANYMAILFINDER_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `classify-leads`, `casualize-names`, `instantly-campaigns`, `onboarding-kickoff`

### Cost
$0.01-0.02 per lead + $0.30/1K for classification
