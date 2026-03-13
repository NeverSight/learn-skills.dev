---
name: just-scrape
description: "CLI tool for AI-powered web scraping, data extraction, search, and crawling via ScrapeGraph AI. Use when the user needs to scrape websites, extract structured data from URLs, convert pages to markdown, crawl multi-page sites, search the web for information, automate browser interactions (login, click, fill forms), get raw HTML, discover sitemaps, or generate JSON schemas. Triggers on tasks involving: (1) extracting data from websites, (2) web scraping or crawling, (3) converting webpages to markdown, (4) AI-powered web search with extraction, (5) browser automation, (6) generating output schemas for scraping. The CLI is just-scrape (npm package just-scrape)."
---

# Web Scraping with just-scrape

AI-powered web scraping CLI by [ScrapeGraph AI](https://scrapegraphai.com). Get an API key at [dashboard.scrapegraphai.com](https://dashboard.scrapegraphai.com).

## Setup

Always install or run the `@latest` version to ensure you have the most recent features and fixes.

```bash
npm install -g just-scrape@latest           # npm
pnpm add -g just-scrape@latest              # pnpm
yarn global add just-scrape@latest          # yarn
bun add -g just-scrape@latest               # bun
npx just-scrape@latest --help               # run without installing
bunx just-scrape@latest --help              # run without installing (bun)
```

```bash
export SGAI_API_KEY="sgai-..."
```

API key resolution order: `SGAI_API_KEY` env var → `.env` file → `~/.scrapegraphai/config.json` → interactive prompt (saves to config).

## Command Selection

| Need | Command |
|---|---|
| Extract structured data from a known URL | `smart-scraper` |
| Search the web and extract from results | `search-scraper` |
| Convert a page to clean markdown | `markdownify` |
| Crawl multiple pages from a site | `crawl` |
| Get raw HTML | `scrape` |
| Automate browser actions (login, click, fill) | `agentic-scraper` |
| Generate a JSON schema from description | `generate-schema` |
| Get all URLs from a sitemap | `sitemap` |
| Check credit balance | `credits` |
| Browse past requests | `history` |
| Validate API key | `validate` |

## Common Flags

All commands support `--json` for machine-readable output (suppresses banner, spinners, prompts).

Scraping commands share these optional flags:
- `--stealth` — bypass anti-bot detection (+4 credits)
- `--headers <json>` — custom HTTP headers as JSON string
- `--schema <json>` — enforce output JSON schema

## Commands

### Smart Scraper

Extract structured data from any URL using AI.

```bash
just-scrape smart-scraper <url> -p <prompt>
just-scrape smart-scraper <url> -p <prompt> --schema <json>
just-scrape smart-scraper <url> -p <prompt> --scrolls <n>     # infinite scroll (0-100)
just-scrape smart-scraper <url> -p <prompt> --pages <n>       # multi-page (1-100)
just-scrape smart-scraper <url> -p <prompt> --stealth         # anti-bot (+4 credits)
just-scrape smart-scraper <url> -p <prompt> --cookies <json> --headers <json>
just-scrape smart-scraper <url> -p <prompt> --plain-text
```

```bash
# E-commerce extraction
just-scrape smart-scraper https://store.example.com/shoes -p "Extract all product names, prices, and ratings"

# Strict schema + scrolling
just-scrape smart-scraper https://news.example.com -p "Get headlines and dates" \
  --schema '{"type":"object","properties":{"articles":{"type":"array","items":{"type":"object","properties":{"title":{"type":"string"},"date":{"type":"string"}}}}}}' \
  --scrolls 5

# JS-heavy SPA behind anti-bot
just-scrape smart-scraper https://app.example.com/dashboard -p "Extract user stats" \
  --stealth
```

### Search Scraper

Search the web and extract structured data from results.

```bash
just-scrape search-scraper <prompt>
just-scrape search-scraper <prompt> --num-results <n>     # sources to scrape (3-20, default 3)
just-scrape search-scraper <prompt> --no-extraction       # markdown only (2 credits vs 10)
just-scrape search-scraper <prompt> --schema <json>
just-scrape search-scraper <prompt> --stealth --headers <json>
```

```bash
# Research across sources
just-scrape search-scraper "Best Python web frameworks in 2025" --num-results 10

# Cheap markdown-only
just-scrape search-scraper "React vs Vue comparison" --no-extraction --num-results 5

# Structured output
just-scrape search-scraper "Top 5 cloud providers pricing" \
  --schema '{"type":"object","properties":{"providers":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"free_tier":{"type":"string"}}}}}}'
```

### Markdownify

Convert any webpage to clean markdown.

```bash
just-scrape markdownify <url>
just-scrape markdownify <url> --stealth         # +4 credits
just-scrape markdownify <url> --headers <json>
```

```bash
just-scrape markdownify https://blog.example.com/my-article
just-scrape markdownify https://protected.example.com --stealth
just-scrape markdownify https://docs.example.com/api --json | jq -r '.result' > api-docs.md
```

### Crawl

Crawl multiple pages and extract data from each.

```bash
just-scrape crawl <url> -p <prompt>
just-scrape crawl <url> -p <prompt> --max-pages <n>      # default 10
just-scrape crawl <url> -p <prompt> --depth <n>           # default 1
just-scrape crawl <url> --no-extraction --max-pages <n>   # markdown only (2 credits/page)
just-scrape crawl <url> -p <prompt> --schema <json>
just-scrape crawl <url> -p <prompt> --rules <json>        # include_paths, same_domain
just-scrape crawl <url> -p <prompt> --no-sitemap
just-scrape crawl <url> -p <prompt> --stealth
```

```bash
# Crawl docs site
just-scrape crawl https://docs.example.com -p "Extract all code snippets" --max-pages 20 --depth 3

# Filter to blog pages only
just-scrape crawl https://example.com -p "Extract article titles" \
  --rules '{"include_paths":["/blog/*"],"same_domain":true}' --max-pages 50

# Raw markdown, no AI extraction (cheaper)
just-scrape crawl https://example.com --no-extraction --max-pages 10
```

### Scrape

Get raw HTML content from a URL.

```bash
just-scrape scrape <url>
just-scrape scrape <url> --stealth          # +4 credits
just-scrape scrape <url> --branding         # extract logos/colors/fonts (+2 credits)
just-scrape scrape <url> --country-code <iso>
```

```bash
just-scrape scrape https://example.com
just-scrape scrape https://store.example.com --stealth --country-code DE
just-scrape scrape https://example.com --branding
```

### Agentic Scraper

Browser automation with AI — login, click, navigate, fill forms. Steps are comma-separated strings.

```bash
just-scrape agentic-scraper <url> -s <steps>
just-scrape agentic-scraper <url> -s <steps> --ai-extraction -p <prompt>
just-scrape agentic-scraper <url> -s <steps> --schema <json>
just-scrape agentic-scraper <url> -s <steps> --use-session   # persist browser session
```

```bash
# Login + extract dashboard
just-scrape agentic-scraper https://app.example.com/login \
  -s "Fill email with user@test.com,Fill password with secret,Click Sign In" \
  --ai-extraction -p "Extract all dashboard metrics"

# Multi-step form
just-scrape agentic-scraper https://example.com/wizard \
  -s "Click Next,Select Premium plan,Fill name with John,Click Submit"

# Persistent session across runs
just-scrape agentic-scraper https://app.example.com \
  -s "Click Settings" --use-session
```

### Generate Schema

Generate a JSON schema from a natural language description.

```bash
just-scrape generate-schema <prompt>
just-scrape generate-schema <prompt> --existing-schema <json>
```

```bash
just-scrape generate-schema "E-commerce product with name, price, ratings, and reviews array"

# Refine an existing schema
just-scrape generate-schema "Add an availability field" \
  --existing-schema '{"type":"object","properties":{"name":{"type":"string"},"price":{"type":"number"}}}'
```

### Sitemap

Get all URLs from a website's sitemap.

```bash
just-scrape sitemap <url>
just-scrape sitemap https://example.com --json | jq -r '.urls[]'
```

### History

Browse request history. Interactive by default (arrow keys to navigate, select to view details).

```bash
just-scrape history <service>                     # interactive browser
just-scrape history <service> <request-id>        # specific request
just-scrape history <service> --page <n>
just-scrape history <service> --page-size <n>     # max 100
just-scrape history <service> --json
```

Services: `markdownify`, `smartscraper`, `searchscraper`, `scrape`, `crawl`, `agentic-scraper`, `sitemap`

```bash
just-scrape history smartscraper
just-scrape history crawl --json --page-size 100 | jq '.requests[] | {id: .request_id, status}'
```

### Credits & Validate

```bash
just-scrape credits
just-scrape credits --json | jq '.remaining_credits'
just-scrape validate
```

## Common Patterns

### Generate schema then scrape with it

```bash
just-scrape generate-schema "Product with name, price, and reviews" --json | jq '.schema' > schema.json
just-scrape smart-scraper https://store.example.com -p "Extract products" --schema "$(cat schema.json)"
```

### Pipe JSON for scripting

```bash
just-scrape sitemap https://example.com --json | jq -r '.urls[]' | while read url; do
  just-scrape smart-scraper "$url" -p "Extract title" --json >> results.jsonl
done
```

### Protected sites

```bash
# JS-heavy SPA behind Cloudflare
just-scrape smart-scraper https://protected.example.com -p "Extract data" --stealth

# With custom cookies/headers
just-scrape smart-scraper https://example.com -p "Extract data" \
  --cookies '{"session":"abc123"}' --headers '{"Authorization":"Bearer token"}'
```

## Credit Costs

| Feature | Extra Credits |
|---|---|
| `--stealth` | +4 per request |
| `--branding` (scrape only) | +2 |
| `search-scraper` extraction | 10 per request |
| `search-scraper --no-extraction` | 2 per request |
| `crawl --no-extraction` | 2 per page |

## Environment Variables

```bash
SGAI_API_KEY=sgai-...              # API key
JUST_SCRAPE_TIMEOUT_S=300          # Request timeout in seconds (default 120)
JUST_SCRAPE_DEBUG=1                # Debug logging to stderr
```
