---
name: onboarding-kickoff
description: Automated client onboarding after kickoff call - generates leads, creates email campaigns, sets up auto-reply. Use when user asks to onboard a new client, set up campaigns for client, or run post-kickoff automation.
---

# Post-Kickoff Client Onboarding

## Goal
Automated onboarding workflow that runs after kickoff call. Generates leads, creates campaigns, and sets up auto-reply system.

## Inputs (from kickoff call)

**Required:**
- `client_name`: Company name
- `client_email`: Primary contact email
- `service_type`: What service they provide
- `target_location`: Geographic area
- `offers`: Three offers (pipe-separated)
- `target_audience`: Who they're targeting
- `social_proof`: Credentials/results

**Optional:**
- `lead_limit`: Number of leads (default: 500)
- `value_proposition`: Additional context

## Scripts
- `./scripts/gmaps_lead_pipeline.py` - Lead generation
- `./scripts/casualize_company_names_batch.py` - Name casualization
- `./scripts/instantly_create_campaigns.py` - Campaign creation
- `./scripts/onboarding_post_kickoff.py` - Full orchestration
- `./scripts/update_sheet.py` - Sheet updates

## Process

### Step 1: Generate Lead Search Query
Format: `{service_type} in {target_location}`
Example: "plumbers in Austin TX"

### Step 2: Scrape and Enrich Leads
```bash
python3 ./scripts/gmaps_lead_pipeline.py \
  --search "{service_type} in {target_location}" \
  --limit {lead_limit} \
  --sheet-name "{client_name} - Leads" \
  --workers 5
```

### Step 3: Casualize Company Names
```bash
python3 ./scripts/casualize_company_names_batch.py \
  --sheet-url "{sheet_url}" \
  --column "business_name" \
  --output-column "casualCompanyName"
```

### Step 4: Create Instantly Campaigns
```bash
python3 ./scripts/instantly_create_campaigns.py \
  --client_name "{client_name}" \
  --client_description "..." \
  --offers "{offers}" \
  --target_audience "{target_audience}" \
  --social_proof "{social_proof}"
```

### Step 5: Upload Leads to Campaigns
Distribute leads evenly across 3 campaigns via Instantly API.

### Step 6: Add Knowledge Base Entry
Add entry to auto-reply knowledge base sheet for intelligent response handling.

### Step 7: Send Summary Email
Send completion email to client with:
- Campaign links and leads counts
- Lead spreadsheet URL
- Auto-reply configuration details
- Next steps

## Output
```json
{
  "status": "success",
  "client_name": "...",
  "sheet_url": "...",
  "lead_count": 50,
  "campaigns": [...],
  "leads_uploaded": true,
  "knowledge_base_updated": true,
  "summary_email_sent": true
}
```

## Timing
- Full workflow: ~10-15 minutes for 50 leads
- Lead scraping uses 5 workers by default

## Error Handling
- < 10 leads found: Warn but continue
- 0 leads found: Error (bad search query)
- Instantly API error: Capture, note for manual fix
- Sheet/email failures: Log but complete workflow

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_name` | string | Yes | Company name |
| `client_email` | string | Yes | Primary contact email |
| `service_type` | string | Yes | What service they provide |
| `target_location` | string | Yes | Geographic area |
| `offers` | string | Yes | Three offers (pipe-separated) |
| `target_audience` | string | Yes | Who they're targeting |
| `social_proof` | string | Yes | Credentials/results |
| `lead_limit` | integer | No | Number of leads (default: 500) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `status` | string | success/failure |
| `sheet_url` | string | Lead spreadsheet URL |
| `lead_count` | integer | Number of leads generated |
| `campaigns` | array | Campaign IDs created |
| `summary_email_sent` | boolean | Whether summary was emailed |

### Credentials
| Name | Source |
|------|--------|
| `APIFY_API_TOKEN` | .env |
| `ANTHROPIC_API_KEY` | .env |
| `INSTANTLY_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `gmaps-leads`, `casualize-names`, `instantly-campaigns`, `welcome-email`

### Cost
~$5-10 for 500 leads + campaigns
