---
name: upwork-apply
description: Scrape Upwork jobs and generate personalized proposals with cover letters. Use when user asks to find Upwork jobs, create Upwork proposals, or apply to Upwork listings.
---

# Upwork Job Scraping & Proposal Generation

## Goal
Scrape Upwork job listings and generate personalized proposals with compelling cover letters.

## Scripts
- `./scripts/upwork_apify_scraper.py` - Scrape Upwork jobs via Apify
- `./scripts/upwork_proposal_generator.py` - Generate proposals with Claude
- `./scripts/update_sheet.py` - Save to Google Sheets

## Process

### 1. Scrape Jobs
```bash
python3 ./scripts/upwork_apify_scraper.py \
  --query "AI automation" \
  --limit 50 \
  --output .tmp/upwork_jobs.json
```

### 2. Generate Proposals
```bash
python3 ./scripts/upwork_proposal_generator.py \
  --jobs .tmp/upwork_jobs.json \
  --output .tmp/proposals.json
```

Uses Claude Opus 4.5 for high-quality, personalized cover letters.

### 3. Save to Sheet
```bash
python3 ./scripts/update_sheet.py .tmp/proposals.json --title "Upwork Proposals"
```

## Output
Google Sheet with:
- Job details (title, description, budget, client info)
- Generated proposal/cover letter
- Application link

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
| `query` | string | Yes | Search query (e.g., 'AI automation') |
| `limit` | integer | No | Max job listings (default: 50) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `sheet_url` | string | Google Sheet with job details + generated proposals |

### Credentials
| Name | Source |
|------|--------|
| `APIFY_API_TOKEN` | .env |
| `ANTHROPIC_API_KEY` | .env |

### Cost
Apify credits + Claude API
