---
name: design-website
description: Generate a premium mockup website for a prospect using the buildinamsterdam.com template style. Use when user asks to design a website, create a mockup, or build a prospect website.
---

# Design Website

## Goal
Generate a polished, single-page HTML website mockup for a prospect's business. The website matches the **buildinamsterdam.com** aesthetic: bold typography, off-white backgrounds, editorial grid layouts, terracotta accents. Used to pitch web design services.

## Inputs
- **Google Sheet URL** with prospect data
- **Row number** (1-indexed, excluding header) to select which prospect
- Optional: **worksheet name** (defaults to first sheet)

### Expected Sheet Columns
The script maps these columns (case-insensitive, flexible matching):
| Column | Maps To |
|---|---|
| company_name / company | Business name (hero, nav, footer) |
| description / about | About section + hero subtitle |
| keywords / services | Services grid (comma-separated) |
| phone / phone_number | Contact section |
| email / contact_email | Contact section |
| address / full_address | Contact section |
| city, state, country | Location info |
| industry / category | Unsplash image search queries |
| first_name, last_name | Owner attribution |
| title / role | Owner role |

## Scripts
- `scripts/read_prospect.py` — Read a single prospect row from Google Sheets → JSON
- `scripts/generate_website.py` — Generate HTML website from prospect JSON

## Process

### Step 1: Read prospect data
```bash
python3 .claude/skills/design-website/scripts/read_prospect.py \
  --url "SHEET_URL" \
  --row ROW_NUMBER \
  --worksheet "WORKSHEET_NAME"  # optional
```
Outputs JSON to stdout.

### Step 2: Generate website
```bash
python3 .claude/skills/design-website/scripts/read_prospect.py \
  --url "SHEET_URL" --row 1 | \
python3 .claude/skills/design-website/scripts/generate_website.py
```
Or with a JSON file:
```bash
python3 .claude/skills/design-website/scripts/generate_website.py < prospect.json
```

### Step 3: Preview
Open the generated file in browser:
```bash
open .tmp/website_*.html
```

## Outputs
- `.tmp/website_{company_slug}.html` — Self-contained HTML file, viewable in any browser
- All CSS is inline, images are external URLs (Unsplash)

## Environment
- `UNSPLASH_ACCESS_KEY` in `.env` — Required for stock photos. Get free key at https://unsplash.com/developers
- If no key is set, falls back to curated placeholder images from picsum.photos
- Google OAuth credentials (token.json / credentials.json) for Sheets access

## Design System
- **Font**: Inter (Google Fonts CDN)
- **Colors**: Off-white `#F2EFE6`, Black `#000`, White `#FFF`, Terracotta `#C38133`
- **Typography**: Bold uppercase display (72-100px), section heads (36-48px), body (16-18px)
- **Layout**: Full-viewport hero, 2-col about, 3-col services grid, 2x2 gallery
- **Buttons**: Bordered, uppercase, letter-spaced

## Edge Cases
- Missing columns: Script uses sensible defaults (e.g., "Welcome" if no description)
- No Unsplash key: Falls back to picsum.photos placeholder images
- Long company names: CSS handles wrapping with responsive font sizing
- Special characters: HTML-escaped in output

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sheet_url` | string | Yes | Google Sheet URL with prospect data |
| `row` | integer | Yes | Row number (1-indexed, excluding header) |
| `worksheet` | string | No | Worksheet name (default: first sheet) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `html_file` | file_path | Self-contained HTML file at .tmp/website_{slug}.html |

### Credentials
| Name | Source |
|------|--------|
| `UNSPLASH_ACCESS_KEY` | .env (optional, falls back to picsum) |

### Composable With
Skills that chain well with this one: `scrape-leads`, `gmaps-leads`

### Cost
Free (Unsplash free tier)
