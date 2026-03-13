---
name: lead-scorer
description: |
  Score leads 0-100 by analyzing a domain's website, DNS, sitemap, and social presence.
  Uses customizable JSON scoring profiles so users can define what signals matter for
  their brand. Use when qualifying leads, prioritizing outreach lists, or evaluating
  potential partners. Supports single domains, multiple domains, and CSV batch mode.
---

# Lead Scorer

Analyze a domain and return a 0-100 lead score with detailed breakdown. The key feature is **customizable scoring profiles** — JSON configs that define which signals matter and their weights.

## How It Works

1. **DNS Analysis** — MX records (Google Workspace/M365 = real business), SPF/DMARC
2. **Sitemap Parsing** — URL count, last modified dates, content volume
3. **Website Scraping** — Blog detection, tech stack, meta tags, social links, contact info
4. **Signal Scoring** — Each signal scored against the profile weights
5. **Grade Assignment** — A (80-100), B (60-79), C (40-59), D (20-39), F (0-19)

## Dependencies

```bash
pip3 install dnspython
```

## Usage

### Single domain (default profile)
```bash
python3 scripts/score_lead.py example.com
```

### With custom profile
```bash
python3 scripts/score_lead.py example.com --profile clearscope.json
```

### Multiple domains
```bash
python3 scripts/score_lead.py domain1.com domain2.com domain3.com
```

### Batch from CSV
```bash
python3 scripts/score_lead.py --csv leads.csv --domain-column "Website"
```

### Options
- `--profile FILE` — Scoring profile JSON (default: `default.json`, resolved from `scripts/profiles/`)
- `--csv FILE` — CSV file with domains
- `--domain-column NAME` — Column name for domains in CSV (default: `domain`)
- `--scrape-delay SECONDS` — Delay between HTTP requests (default: 0.5)
- `--output FILE` — Write results to file instead of stdout

## Output

JSON to stdout with overall score, per-signal breakdown, raw data, and summary:

```json
{
  "domain": "example.com",
  "score": 72,
  "grade": "B",
  "profile": "default",
  "signals": {
    "has_blog": {"score": 20, "max": 20, "evidence": "Blog found at /blog; 234 URLs in sitemap"},
    "business_legitimacy": {"score": 15, "max": 20, "evidence": "MX: Google Workspace; SPF configured"}
  },
  "raw_data": {
    "sitemap_urls": 234,
    "mx_provider": "Google Workspace",
    "tech_stack": ["WordPress", "Cloudflare"]
  },
  "summary": "Strong in: has blog, business legitimacy. Good lead, worth pursuing."
}
```

## Scoring Profiles

Profiles are the key differentiator. They let you define **what matters for YOUR use case**.

### Profile format

```json
{
  "name": "my-profile",
  "description": "What this profile scores for",
  "signals": {
    "signal_name": {
      "weight": 25,
      "description": "What this signal measures",
      "keywords": ["optional", "keyword", "list"]
    }
  }
}
```

### Built-in signals

| Signal | What it checks |
|--------|---------------|
| `has_blog` | Blog/content section existence + sitemap volume |
| `business_legitimacy` | MX provider, SPF/DMARC, about page, meta tags |
| `content_velocity` | Sitemap dates — recency and frequency of updates |
| `tech_stack` | CMS, analytics, chat tools detected in page source |
| `audience_size` | Social media links (Twitter, LinkedIn, YouTube, Facebook) |
| `contact_findability` | Contact page, emails on site, LinkedIn link |
| `seo_tools` | Keyword matching in homepage text (requires `keywords` array) |

### Custom keyword signals

Any signal with a `keywords` array will match those terms against the homepage text. This is how you detect competitors, tools, or industry terms:

```json
{
  "name": "crm-seller",
  "signals": {
    "uses_crm": {
      "weight": 30,
      "description": "Already uses a CRM",
      "keywords": ["salesforce", "hubspot", "pipedrive", "zoho crm", "close.io"]
    },
    "has_sales_team": {
      "weight": 25,
      "description": "Mentions sales roles or team",
      "keywords": ["sales team", "account executive", "sdr", "business development"]
    }
  }
}
```

### Shipped profiles

- `default.json` — Generic scoring for any SaaS/content company
- `clearscope.json` — Example profile for SEO tool partnership leads

Create your own in `scripts/profiles/` or pass any path with `--profile`.

## Rate Limiting

The script is polite by default:

- **`--scrape-delay 0.5`** — 500ms between HTTP requests (default)
- Each domain makes ~5-8 requests (homepage, blog, about, contact, sitemap, DNS)
- For batch mode, there's an additional delay between domains
- Increase delay for large batches: `--scrape-delay 2`
- All requests use a generic User-Agent string

### Recommended delays

| Batch size | Delay | Est. time |
|-----------|-------|-----------|
| 1-10 | 0.5s (default) | ~30s-2min |
| 10-50 | 1.0s | ~5-15min |
| 50+ | 2.0s | ~30min+ |

## Error Handling

If a signal can't be gathered (site down, DNS timeout, etc.), it scores 0 with an explanation in the evidence field. The script never crashes on a single domain failure — it logs the issue to stderr and continues.

## Tips

- **Start with default profile**, review results, then customize
- **Weights should sum to 100** for intuitive scoring (not required — auto-normalizes)
- **Keywords are powerful** — add competitor names, industry terms, technology mentions
- **Pipe to jq** for quick filtering: `python3 scripts/score_lead.py domain.com | jq '.score'`
- **Batch + sort**: Score a CSV, then sort by score to prioritize outreach
