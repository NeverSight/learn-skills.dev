---
name: playwright-web-scraper
description: |
  Extract structured data from multiple web pages using Playwright with built-in ethical
  crawling practices including rate limiting, robots.txt compliance, and error monitoring.
  Use when asked to "scrape data from", "extract information from pages", "collect data
  from site", "crawl multiple pages", or when gathering structured data from websites.
  Supports pagination, multi-page extraction, data aggregation, and export to CSV/JSON/Markdown.
  Works with browser_navigate, browser_evaluate, browser_wait_for, and browser_snapshot tools.

---

# Playwright Web Scraper

Extract structured data from multiple web pages with respectful, ethical crawling practices.

## When to Use This Skill

Use when extracting structured data from websites with "scrape data from", "extract information from pages", "collect data from site", or "crawl multiple pages".

Do NOT use for testing workflows (use `playwright-e2e-testing`), monitoring errors (use `playwright-console-monitor`), or analyzing network (use `playwright-network-analyzer`). Always respect robots.txt and rate limits.

## Quick Start

Scrape product listings from an e-commerce site:

```javascript
// 1. Validate URLs
python scripts/validate_urls.py urls.txt

// 2. Scrape pages with rate limiting
const results = [];
for (const url of urls) {
  await browser_navigate({ url });
  await browser_wait_for({ time: Math.random() * 2 + 1 }); // 1-3s delay

  const data = await browser_evaluate({
    function: `
      Array.from(document.querySelectorAll('.product')).map(el => ({
        title: el.querySelector('.title')?.textContent?.trim(),
        price: el.querySelector('.price')?.textContent?.trim(),
        url: el.querySelector('a')?.getAttribute('href')
      }))
    `
  });

  results.push(...data);
}

// 3. Process results
python scripts/process_results.py scraped.json -o products.csv
```

## Table of Contents

1. Core Workflow
2. Rate Limiting Strategy
3. URL Validation
4. Data Extraction
5. Error Handling
6. Processing Results
7. Supporting Files
8. Expected Outcomes

## Core Workflow

### Step 1: Prepare URL List

Create a text file with URLs to scrape (one per line):

```
https://example.com/products?page=1
https://example.com/products?page=2
https://example.com/products?page=3
```

Validate URLs and check robots.txt compliance:

```bash
python scripts/validate_urls.py urls.txt --user-agent "MyBot/1.0"
```

### Step 2: Initialize Scraping Session

Navigate to the site and take a snapshot to understand structure:

```javascript
await browser_navigate({ url: firstUrl });
await browser_snapshot();
```

Identify CSS selectors for data extraction using the snapshot.

### Step 3: Implement Rate-Limited Crawling

Use random delays between requests (1-3 seconds minimum):

```javascript
const results = [];

for (const url of urlList) {
  // Navigate to page
  await browser_navigate({ url });

  // Wait for content to load
  await browser_wait_for({ text: 'Expected content marker' });

  // Add respectful delay (1-3 seconds)
  const delay = Math.random() * 2 + 1;
  await browser_wait_for({ time: delay });

  // Extract data
  const pageData = await browser_evaluate({
    function: `/* extraction code */`
  });

  results.push(...pageData);

  // Check console for errors/warnings
  const console = await browser_console_messages();
  // Monitor for rate limit warnings
}
```

### Step 4: Extract Structured Data

Use `browser_evaluate` to extract data with JavaScript:

```javascript
const data = await browser_evaluate({
  function: `
    try {
      return Array.from(document.querySelectorAll('.item')).map(el => ({
        title: el.querySelector('.title')?.textContent?.trim(),
        price: el.querySelector('.price')?.textContent?.trim(),
        rating: el.querySelector('.rating')?.textContent?.trim(),
        url: el.querySelector('a')?.getAttribute('href')
      })).filter(item => item.title && item.price); // Filter incomplete records
    } catch (e) {
      console.error('Extraction failed:', e);
      return [];
    }
  `
});
```

See `references/extraction-patterns.md` for comprehensive extraction patterns.

### Step 5: Handle Errors and Rate Limits

Monitor for rate limiting indicators:

```javascript
// Check HTTP responses via browser_network_requests
const requests = await browser_network_requests();
const rateLimited = requests.some(r => r.status === 429 || r.status === 503);

if (rateLimited) {
  // Back off exponentially
  await browser_wait_for({ time: 10 }); // Wait 10 seconds
  // Retry or skip
}

// Check console for blocking messages
const console = await browser_console_messages({ pattern: 'rate limit|blocked|captcha' });
if (console.length > 0) {
  // Handle blocking
}
```

### Step 6: Aggregate and Store Results

Save results to JSON file:

```javascript
// In your scraping script
fs.writeFileSync('scraped.json', JSON.stringify({ results }, null, 2));
```

Process and convert to desired format:

```bash
# View statistics
python scripts/process_results.py scraped.json --stats

# Convert to CSV
python scripts/process_results.py scraped.json -o output.csv

# Convert to Markdown table
python scripts/process_results.py scraped.json -o output.md
```

## Rate Limiting Strategy

### Minimum Delays

Always add delays between requests:

- **Standard sites**: 1-3 seconds (random)
- **High-traffic sites**: 3-5 seconds
- **Small sites**: 5-10 seconds
- **After errors**: Exponential backoff (5s, 10s, 20s, 40s)

### Implementation

```javascript
// Random delay between 1-3 seconds
const randomDelay = () => Math.random() * 2 + 1;
await browser_wait_for({ time: randomDelay() });

// Exponential backoff after rate limit
let backoffSeconds = 5;
for (let retry = 0; retry < 3; retry++) {
  try {
    await browser_navigate({ url });
    break; // Success
  } catch (e) {
    await browser_wait_for({ time: backoffSeconds });
    backoffSeconds *= 2; // Double delay each retry
  }
}
```

### Adaptive Rate Limiting

Adjust delays based on response:

| Response Code | Action |
|---------------|--------|
| 200 OK | Continue with normal delay (1-3s) |
| 429 Too Many Requests | Increase delay to 10s, retry |
| 503 Service Unavailable | Wait 60s, then retry |
| 403 Forbidden | Stop scraping this domain |

See `references/ethical-scraping.md` for detailed rate limiting strategies.

## URL Validation

Use `validate_urls.py` before scraping to ensure compliance:

```bash
# Basic validation
python scripts/validate_urls.py urls.txt

# Check robots.txt with specific user agent
python scripts/validate_urls.py urls.txt --user-agent "MyBot/1.0"

# Strict mode (exit on any invalid/disallowed URL)
python scripts/validate_urls.py urls.txt --strict
```

**Output includes**:

- URL format validation
- Domain grouping
- robots.txt compliance check
- Summary statistics

## Data Extraction

### Basic Pattern

```javascript
// Single page extraction
const data = await browser_evaluate({
  function: `
    Array.from(document.querySelectorAll('.item')).map(el => ({
      field1: el.querySelector('.selector1')?.textContent?.trim(),
      field2: el.querySelector('.selector2')?.getAttribute('href')
    }))
  `
});
```

### Pagination Pattern

```javascript
let hasMore = true;
let page = 1;

while (hasMore) {
  await browser_navigate({ url: `${baseUrl}?page=${page}` });
  await browser_wait_for({ time: randomDelay() });

  const pageData = await browser_evaluate({ function: extractionCode });
  results.push(...pageData);

  // Check for next page
  hasMore = await browser_evaluate({
    function: `document.querySelector('.next:not(.disabled)') !== null`
  });

  page++;
}
```

See `references/extraction-patterns.md` for:

- Advanced selectors
- Data cleaning patterns
- Table extraction
- JSON-LD extraction
- Shadow DOM access

## Error Handling

### Network Errors

```javascript
try {
  await browser_navigate({ url });
} catch (e) {
  console.error(`Failed to load ${url}:`, e);
  failedUrls.push(url);
  continue; // Skip to next URL
}
```

### Content Validation

```javascript
const data = await browser_evaluate({ function: extractionCode });

if (!data || data.length === 0) {
  console.warn(`No data extracted from ${url}`);
  // Log for manual review
}

// Validate data structure
const validData = data.filter(item =>
  item.title && item.price // Ensure required fields exist
);
```

### Monitoring Indicators

Check for blocking/errors:

```javascript
// Monitor console
const console = await browser_console_messages({
  pattern: 'error|rate|limit|captcha',
  onlyErrors: true
});

if (console.length > 0) {
  console.log('Warnings detected:', console);
}

// Monitor network
const requests = await browser_network_requests();
const errors = requests.filter(r => r.status >= 400);
```

## Processing Results

### View Statistics

```bash
python scripts/process_results.py scraped.json --stats
```

Output:
```
📊 Statistics:
  Total records: 150
  Fields (5): title, price, rating, url, image
  Sample record: {...}
```

### Convert Formats

```bash
# To CSV
python scripts/process_results.py scraped.json -o products.csv

# To JSON (compact)
python scripts/process_results.py scraped.json -o products.json --compact

# To Markdown table
python scripts/process_results.py scraped.json -o products.md
```

### Combine Statistics with Conversion

```bash
python scripts/process_results.py scraped.json -o products.csv --stats
```

## Supporting Files

### Scripts

- **`scripts/validate_urls.py`** - Validate URL lists, check robots.txt compliance, group by domain
- **`scripts/process_results.py`** - Convert scraped JSON to CSV/JSON/Markdown, view statistics

### References

- **`references/ethical-scraping.md`** - Comprehensive guide to rate limiting, robots.txt, error handling, and monitoring
- **`references/extraction-patterns.md`** - JavaScript patterns for data extraction, selectors, pagination, tables

## Expected Outcomes

### Successful Scraping

```
✅ Validated 50 URLs
✅ Scraped 50 pages in 5 minutes (6 req/min)
✅ Extracted 1,250 products
✅ Zero rate limit errors
✅ Exported to products.csv (1,250 rows)
```

### With Error Handling

```
⚠️  Validated 50 URLs (2 disallowed by robots.txt)
✅ Scraped 48 pages
⚠️  3 pages returned no data (logged for review)
✅ Extracted 1,100 products
⚠️  1 rate limit warning (backed off successfully)
✅ Exported to products.csv (1,100 rows)
```

### Rate Limit Detection

```
❌ Rate limited after 20 pages (429 responses)
✅ Backed off exponentially (5s → 10s → 20s)
✅ Resumed scraping successfully
✅ Extracted 450 products from 25 pages
```

## Expected Benefits

| Metric | Before | After |
|--------|--------|-------|
| Setup time | 30-45 min | 5-10 min |
| Rate limit errors | Common | Rare |
| robots.txt violations | Possible | Prevented |
| Data format conversion | Manual | Automated |
| Error detection | Manual review | Automated monitoring |

## Success Metrics

- **Success rate** > 95% (pages successfully scraped)
- **Rate limit errors** < 5% of requests
- **Valid data rate** > 90% (complete records)
- **Scraping speed** 6-12 requests/minute (polite crawling)

## Requirements

### Tools

- Playwright MCP browser tools
- Python 3.8+ (for scripts)
- Standard library only (no external dependencies for scripts)

### Knowledge

- Basic CSS selectors
- JavaScript for data extraction
- Understanding of HTTP status codes
- Awareness of web scraping ethics

## Red Flags to Avoid

- ❌ Scraping without checking robots.txt
- ❌ No delays between requests (hammering servers)
- ❌ Ignoring 429/503 response codes
- ❌ Scraping personal/private information
- ❌ Not monitoring console for blocking messages
- ❌ Scraping sites that explicitly prohibit it (check ToS)
- ❌ Using scraped data in violation of copyright
- ❌ Not handling pagination correctly (missing data)
- ❌ Hardcoding selectors without fallbacks
- ❌ Not validating extracted data structure

## Notes

- **Default to polite crawling**: 1-3 second delays minimum, adjust based on site response
- **Always check robots.txt first**: Use `validate_urls.py` before scraping
- **Monitor console and network**: Watch for rate limit warnings and adjust delays
- **Start small**: Test with 5-10 URLs before scaling to hundreds
- **Save progress**: Write results incrementally in case of interruption
- **Respect ToS**: Some sites prohibit scraping in their terms of service
- **Use descriptive user agents**: Identify your bot clearly
- **Handle errors gracefully**: Log failures for manual review, don't crash
