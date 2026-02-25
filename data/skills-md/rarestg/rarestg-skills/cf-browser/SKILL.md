---
name: cf-browser
description: >-
  Browse and scrape websites using Cloudflare's Browser Rendering REST API.
  Use when the agent needs to fetch rendered web content, extract structured
  data from pages, take screenshots, or scrape specific elements via CSS
  selectors. Triggers on tasks like "scrape this site", "get listings from
  this page", "extract data from this URL", "take a screenshot of this page",
  "browse this website", or any task requiring headless browser access to
  read, crawl, or extract information from live web pages. Also use when
  WebFetch is insufficient (JS-heavy sites, SPAs, pages requiring cookies,
  or when structured extraction is needed).
---

# Cloudflare Browser Rendering

Browse and scrape the web via Cloudflare's Browser Rendering REST API. Every call is a single POST request — no browser setup, no Puppeteer scripts.

## Prerequisites

Requires two env vars (confirm they're set before making calls):
- `CF_ACCOUNT_ID` — Cloudflare account ID
- `CF_API_TOKEN` — API token with **Browser Rendering - Edit** permission

## Helper script

Use [cfbr.sh](scripts/cfbr.sh) for all API calls. It handles auth headers and the base URL:

```bash
# JSON endpoints
cfbr.sh <endpoint> '<json_body>'

# Screenshot (binary) — optional third arg for output filename
cfbr.sh screenshot '<json_body>' output.png
```

## Choosing an endpoint

| Goal | Endpoint | When to use |
|---|---|---|
| Read page content for analysis | `markdown` | Default choice — clean, token-efficient |
| Extract specific elements | `scrape` | Know the CSS selectors for what you need |
| Extract structured data with AI | `json` | Need typed objects, don't know exact selectors |
| Get full rendered DOM | `content` | Need raw HTML for parsing or debugging |
| Discover pages / crawl | `links` | Building a sitemap or finding subpages |
| Visual inspection | `screenshot` | Need to see the page layout or debug visually |
| DOM + visual in one shot | `snapshot` | Need both HTML and a screenshot |

For full endpoint details and parameters, see [api.md](references/api.md).

## Scraping workflow

Follow this sequence when scraping a site for structured data (e.g. rental listings, product catalogs, job boards):

### 1. Reconnaissance — understand the page

Start with `markdown` to see what content is on the page and how it's structured:

```bash
cfbr.sh markdown '{"url":"https://target-site.com/listings", "gotoOptions":{"waitUntil":"networkidle0"}}'
```

If the page is an SPA or loads content dynamically, `networkidle0` ensures JS finishes executing. If you know a specific element that signals content is ready, use `waitForSelector` instead — it's faster:

```json
{"url":"...", "waitForSelector": ".listing-card"}
```

### 2. Discover structure — find the selectors

From the markdown/HTML, identify repeating patterns (listing cards, table rows, etc.) and their CSS selectors. If unclear from markdown alone, use `screenshot` to visually inspect:

```bash
cfbr.sh screenshot '{"url":"https://target-site.com/listings", "screenshotOptions":{"fullPage":true}, "gotoOptions":{"waitUntil":"networkidle0"}}' listings.png
```

### 3. Extract — pull structured data

**Option A: CSS selectors (when you know the DOM structure)**

```bash
cfbr.sh scrape '{
  "url": "https://target-site.com/listings",
  "gotoOptions": {"waitUntil": "networkidle0"},
  "elements": [
    {"selector": ".listing-card .title"},
    {"selector": ".listing-card .price"},
    {"selector": ".listing-card .address"},
    {"selector": ".listing-card a"}
  ]
}'
```

The `scrape` endpoint returns `text`, `html`, `attributes` (including `href`), and position/dimensions for each match. Correlate results across selectors by index (first title matches first price, etc.).

**Option B: AI extraction (when structure is complex or unknown)**

```bash
cfbr.sh json '{
  "url": "https://target-site.com/listings",
  "gotoOptions": {"waitUntil": "networkidle0"},
  "prompt": "Extract all rental listings with title, price, address, bedrooms, and link",
  "response_format": {
    "type": "json_schema",
    "schema": {
      "type": "object",
      "properties": {
        "listings": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": {"type": "string"},
              "price": {"type": "string"},
              "address": {"type": "string"},
              "bedrooms": {"type": "string"},
              "url": {"type": "string"}
            },
            "required": ["title", "price"]
          }
        }
      }
    }
  }
}'
```

Prefer `scrape` when selectors are clear — it's deterministic and free. Use `json` when the page structure is messy or you need semantic interpretation (incurs Workers AI charges).

### 4. Paginate — get all results

Use `links` to find pagination URLs:

```bash
cfbr.sh links '{"url":"https://target-site.com/listings"}'
```

Look for `?page=2`, `next`, or load-more patterns. Repeat extraction for each page.

Infinite-scroll pages are a limitation — the API is stateless (one request = one browser session), so there's no way to scroll, wait for new content to load, and then extract in a single call. For these pages, look for an underlying API or URL parameters (e.g. `?page=2`, `?offset=20`) that serve paginated data directly.

### 5. Handle obstacles

**SPA / empty results** — Add `"gotoOptions": {"waitUntil": "networkidle0"}` or `"waitForSelector": "<selector>"`.

**Slow pages** — Increase timeout: `"gotoOptions": {"timeout": 60000}`.

**Heavy pages** — Strip unnecessary resources:

```json
{"rejectResourceTypes": ["image", "stylesheet", "font", "media"]}
```

**Auth-gated pages** — Pass session cookies:

```json
{"cookies": [{"name": "session", "value": "abc123", "domain": "target-site.com", "path": "/"}]}
```

**Bot detection** — Cloudflare Browser Rendering is always identified as a bot. The `userAgent` field changes what the site sees but will not bypass bot protection. If a site blocks the request, there is no workaround via this API.

## Tips

- `markdown` is the best default for content extraction — it's clean, compact, and LLM-ready.
- Always use `networkidle0` or `waitForSelector` on any modern site. Without it you'll get incomplete content.
- `rejectResourceTypes` dramatically speeds up text-only operations. Always strip images/fonts/stylesheets when you only need text.
- `scrape` results are ordered by DOM position — correlate across selectors by array index.
- For large scraping jobs, process pages sequentially to stay within rate limits.
