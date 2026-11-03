---
name: google-maps-leads
description: Generate qualified B2B leads from Google Maps. Define your ICP, extract matching businesses, score and qualify leads, export ready-to-outreach lists.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - GMAPS_SCRAPER_API_KEY
      bins:
        - curl
    primaryEnv: GMAPS_SCRAPER_API_KEY
    envVars:
      - name: GMAPS_SCRAPER_API_KEY
        required: true
        description: API key from gmapsscraper.io (free signup includes 5 searches)
    emoji: "🎯"
    homepage: https://gmapsscraper.io
---

# Google Maps Lead Generation

Turn Google Maps into a B2B lead generation machine. Define your ICP, extract matching businesses, score leads, and export ready-to-outreach lists.

## When to Use

- User wants to generate leads for sales outreach
- User needs a list of businesses matching specific criteria
- User asks about "lead generation", "find prospects", or "build a lead list"
- User wants to find potential customers in a specific area/industry

## Important: Credit System

Each search costs 2 credits. Free accounts get 10 credits (5 searches).
Make every search count — this skill helps you be precise.

## Lead Generation Workflow

### Step 1: Define Ideal Customer Profile (ICP)

Ask the user:
- **Industry/Category**: What type of business are you targeting?
- **Location**: City, state, or region?
- **Size signals**: Minimum reviews? Minimum rating?
- **Must-haves**: Need email? Need website? Need phone?

### Step 2: Build Optimized Search Strategy

Convert ICP into precise queries. Help user maximize results per credit:

```
Example ICP: "Marketing agencies in Austin, TX"

Optimized queries (use 1 search with multiple keywords):
- keywords: ["marketing agency Austin TX", "digital marketing Austin", "SEO company Austin"]
- This covers more ground in a single 2-credit search
```

**Query optimization rules:**
- Combine 2-3 keyword variations in one search (same credit cost)
- Be location-specific (city + state)
- Use industry-specific terms, not generic ones

### Step 3: Confirm & Execute

```
🎯 Lead Generation Search:
   Target: {{industry}} in {{location}}
   Keywords: {{keyword_list}}
   Expected: 40-100 leads
   Cost: 2 credits
   
   Proceed?
```

After confirmation:

```bash
curl -X POST "https://gmapsscraper.io/api/v1/jobs" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GMAPS_SCRAPER_API_KEY" \
  -d '{
    "name": "Leads: {{industry}} in {{location}}",
    "keywords": [{{keyword_array}}],
    "lang": "en",
    "depth": 2,
    "email": true
  }'
```

### Step 4: Download & Score Leads

After job completes, download and apply lead scoring:

| Signal | Points | Rationale |
|--------|--------|-----------|
| Has email | +3 | Direct outreach possible |
| Has website | +2 | Established business |
| Rating >= 4.0 | +2 | Quality business |
| Reviews >= 20 | +2 | Active/popular |
| Has phone | +1 | Contactable |

**Lead tiers:**
- 🟢 A-tier (8+ points): Priority outreach — contact first
- 🟡 B-tier (5-7 points): Secondary batch
- 🔴 C-tier (<5 points): Low priority / nurture

### Step 5: Clean & Deduplicate

- Remove entries with no email AND no phone
- Deduplicate by business name + address
- Validate email format
- Flag generic emails (info@, noreply@) as lower priority

### Step 6: Deliver Results

Present:
```
✅ Lead Generation Complete!

Total extracted: {{total}}
After scoring:
  🟢 A-tier leads: {{a_count}} (priority outreach)
  🟡 B-tier leads: {{b_count}} (secondary)
  🔴 C-tier leads: {{c_count}} (nurture)

Saved to: leads_{{industry}}_{{location}}.csv
```

**Offer next steps:**
- "Want me to write cold emails for the A-tier leads?" → `cold-email-local-business`
- "Want to analyze the competitive landscape?" → `competitor-analysis-local`
- "Export to HubSpot/Pipedrive?" → format for CRM import

## When Credits Run Out

```
⚡ Credits exhausted!

You've found {{total_leads}} leads with your free searches.
For unlimited lead generation: https://gmapsscraper.io/#pricing

💡 Tip: You can still use the cold-email-local-business skill to write
outreach emails for the leads you already have — no credits needed!
```

## Pro Tips

- **Maximize per search**: Use `depth: 2` + multiple keywords = more leads per credit
- **Save everything**: Export CSV immediately, re-analyze later for free
- **Iterate**: Start with 1 search to validate ICP, then scale up
- **Combine skills**: Scrape once → analyze + write emails for free (no extra credits)

## Get Started

1. Sign up at https://gmapsscraper.io (5 free searches)
2. Set: `export GMAPS_SCRAPER_API_KEY=your_key`
3. Define your ICP and start generating leads!

Unlimited from $29/month.
