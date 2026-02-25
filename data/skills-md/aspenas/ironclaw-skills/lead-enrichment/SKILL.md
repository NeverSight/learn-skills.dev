---
name: lead-enrichment
description: Enrich contact and lead records with LinkedIn profiles, email addresses, company data, and education info. Use when asked to "enrich contacts", "fill in missing data", "find emails for leads", "complete lead profiles", "look up company info", or any bulk data completion task for CRM records.
metadata: { "openclaw": { "emoji": "✨" } }
---

# Lead Enrichment — Multi-Source Data Completion

Enrich CRM contact records by filling missing fields from multiple sources. Works with DuckDB workspace entries or standalone JSON data.

## Sources (Priority Order)

1. **LinkedIn** (via linkedin-scraper skill) — name, title, company, education, connections
2. **Web Search** (via web_search tool) — email patterns, company info, social profiles
3. **Company Website** (via web_fetch) — team pages, about pages, contact info
4. **Email Pattern Discovery** — derive email from name + company domain

## Enrichment Pipeline

### Step 1: Assess What's Missing
```sql
-- Query the target object to find gaps
SELECT "Name", "Email", "LinkedIn URL", "Company", "Title", "Location"
FROM v_leads
WHERE "Email" IS NULL OR "LinkedIn URL" IS NULL OR "Title" IS NULL;
```

### Step 2: Prioritize by Value
- **High priority**: Missing email (needed for outreach)
- **Medium priority**: Missing title/company (needed for personalization)
- **Low priority**: Missing education, connections count, about text

### Step 3: Enrich Per Record

For each record with gaps:

#### If LinkedIn URL is known but other fields missing:
1. Use linkedin-scraper to visit profile
2. Extract: title, company, location, education, about
3. Update DuckDB record

#### If LinkedIn URL is missing:
1. Search LinkedIn: `{name} {company}` or `{name} {title}`
2. Verify match (name + company alignment)
3. Store LinkedIn URL, then scrape full profile

#### If Email is missing:
1. Find company domain (web search or LinkedIn company page)
2. Try common patterns:
   - `first@domain.com`
   - `first.last@domain.com`
   - `flast@domain.com`
   - `firstl@domain.com`
3. Optionally verify with web search: `"email" "{name}" site:{domain}`
4. Check company team/about page for email format clues

#### If Company info is missing:
1. Web search: `"{name}" "{title}"` or check LinkedIn
2. Fetch company website for: industry, size, description, funding

### Step 4: Update Records
```sql
-- Update via DuckDB pivot view
UPDATE v_leads SET
  "Email" = ?,
  "LinkedIn URL" = ?,
  "Title" = ?,
  "Company" = ?,
  "Location" = ?
WHERE id = ?;
```

## Bulk Enrichment Mode

For enriching many records at once:

1. **Query all incomplete records** from DuckDB
2. **Group by company** (scrape company once, apply to all employees)
3. **Process in batches** of 10-20 records
4. **Report progress** after each batch:
   ```
   Enrichment Progress: 45/120 leads (38%)
   ├── Emails found: 32/45 (71%)
   ├── LinkedIn matched: 41/45 (91%)
   ├── Titles updated: 38/45 (84%)
   └── ETA: ~15 min remaining
   ```
5. **Save checkpoint** after each batch (in case of interruption)

## Enrichment Quality Rules

- **Confidence scoring**: Mark each enriched field with confidence (high/medium/low)
  - High: Direct match from LinkedIn profile or company website
  - Medium: Inferred from patterns (email format) or partial match
  - Low: Best guess from web search results
- **Never overwrite existing data** unless explicitly asked
- **Flag conflicts**: If enriched data contradicts existing data, flag for review
- **Dedup check**: Before inserting LinkedIn URL, check it's not already assigned to another contact

## Email Pattern Discovery

Common corporate email formats by frequency:
1. `first.last@domain.com` (most common, ~45%)
2. `first@domain.com` (~20%)
3. `flast@domain.com` (~15%)
4. `firstl@domain.com` (~10%)
5. `first_last@domain.com` (~5%)
6. `last.first@domain.com` (~3%)
7. `first.l@domain.com` (~2%)

Strategy:
1. If you know one person's email at the company, derive the pattern
2. Search web for `"@{domain}" email format`
3. Check company team page source code for mailto: links
4. Use the most common pattern as fallback

## Output

After enrichment, provide a summary:

```
Enrichment Complete: 120 leads processed
├── Emails: 94 found (78%), 26 still missing
├── LinkedIn: 108 matched (90%), 12 not found
├── Titles: 115 updated (96%)
├── Companies: 118 confirmed (98%)
├── Locations: 89 found (74%)
└── Avg confidence: High (82%), Medium (14%), Low (4%)

Top gaps remaining:
- 26 leads missing email (mostly small/stealth companies)
- 12 leads missing LinkedIn (common names, ambiguous matches)
```

## DuckDB Field Mapping

Standard field names for Ironclaw CRM objects:

| Enrichment Data | DuckDB Field | Type |
|----------------|--------------|------|
| Full name | Name | text |
| Email address | Email | email |
| LinkedIn URL | LinkedIn URL | url |
| Job title | Title | text |
| Company name | Company | text / relation |
| Location | Location | text |
| Education | Education | text |
| Phone | Phone | phone |
| Company size | Company Size | text |
| Industry | Industry | text |
| Enrichment date | Enriched At | date |
| Confidence | Enrichment Confidence | enum (high/medium/low) |
