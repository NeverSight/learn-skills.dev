---
name: scrapling-mcp
description: Advanced web scraping with Scrapling — MCP-native guidance for extraction, crawling, and anti-bot handling. Use via mcporter (MCP) to call the `scrapling` MCP server for execution; this skill provides strategy, recipes, and best practices.
---

# Scrapling MCP — Web Scraping Guidance

Source repo: https://github.com/DevBD1/openclaw-skill-scrapling-mcp

> **Guidance Layer + MCP Integration**  
> Use this skill for **strategy and patterns**. For execution, call Scrapling's MCP server via `mcporter`.

## Quick Start (MCP)

### 1. Install Scrapling with MCP support
```bash
pip install scrapling[mcp]
# Or for full features:
pip install scrapling[mcp,playwright]
python -m playwright install chromium
```

### 2. Add to OpenClaw MCP config
```json
{
  "mcpServers": {
    "scrapling": {
      "command": "python",
      "args": ["-m", "scrapling.mcp"]
    }
  }
}
```

### 3. Call via mcporter
```
mcporter call scrapling fetch_page --url "https://example.com"
```

## Execution vs Guidance

| Task | Tool | Example |
|------|------|---------|
| Fetch a page | **mcporter** | `mcporter call scrapling fetch_page --url URL` |
| Extract with CSS | **mcporter** | `mcporter call scrapling css_select --selector ".title::text"` |
| Which fetcher to use? | **This skill** | See "Fetcher Selection Guide" below |
| Anti-bot strategy? | **This skill** | See "Anti-Bot Escalation Ladder" |
| Complex crawl patterns? | **This skill** | See "Spider Recipes" |

## Fetcher Selection Guide

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Fetcher       │────▶│ DynamicFetcher   │────▶│ StealthyFetcher  │
│   (HTTP)        │     │ (Browser/JS)     │     │ (Anti-bot)       │
└─────────────────┘     └──────────────────┘     └──────────────────┘
     Fastest              JS-rendered               Cloudflare, 
     Static pages         SPAs, React/Vue          Turnstile, etc.
```

### Decision Tree
1. **Static HTML?** → `Fetcher` (10-100x faster)
2. **Need JS execution?** → `DynamicFetcher`
3. **Getting blocked?** → `StealthyFetcher`
4. **Complex session?** → Use Session variants

### MCP Fetch Modes
- `fetch_page` — HTTP fetcher
- `fetch_dynamic` — Browser-based with Playwright
- `fetch_stealthy` — Anti-bot bypass mode

## Anti-Bot Escalation Ladder

### Level 1: Polite HTTP
```python
# MCP call: fetch_page with options
{
  "url": "https://example.com",
  "headers": {"User-Agent": "..."},
  "delay": 2.0
}
```

### Level 2: Session Persistence
```python
# Use sessions for cookie/state across requests
FetcherSession(impersonate="chrome")  # TLS fingerprint spoofing
```

### Level 3: Stealth Mode
```python
# MCP: fetch_stealthy
StealthyFetcher.fetch(
    url,
    headless=True,
    solve_cloudflare=True,  # Auto-solve Turnstile
    network_idle=True
)
```

### Level 4: Proxy Rotation
See `references/proxy-rotation.md`

## Adaptive Scraping (Anti-Fragile)

Scrapling can **survive website redesigns** using adaptive selectors:

```python
# First run — save fingerprints
products = page.css('.product', auto_save=True)

# Later runs — auto-relocate if DOM changed
products = page.css('.product', adaptive=True)
```

**MCP usage:**
```
mcporter call scrapling css_select \\
  --selector ".product" \\
  --adaptive true \\
  --auto-save true
```

## Spider Framework (Large Crawls)

When to use Spiders vs direct fetching:
- ✅ **Spider**: 10+ pages, concurrency needed, resume capability, proxy rotation
- ✅ **Direct**: 1-5 pages, quick extraction, simple flow

### Basic Spider Pattern
```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://example.com/products"]
    concurrent_requests = 10
    download_delay = 1.0
    
    async def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                "name": product.css('h2::text').get(),
                "price": product.css('.price::text').get(),
                "url": response.url
            }
        
        # Follow pagination
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

# Run with resume capability
result = ProductSpider(crawldir="./crawl_data").start()
result.items.to_jsonl("products.jsonl")
```

### Advanced: Multi-Session Spider
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "/protected/" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast")
```

### Spider Features
- **Pause/Resume**: `crawldir` parameter saves checkpoints
- **Streaming**: `async for item in spider.stream()` for real-time processing
- **Auto-retry**: Configurable retry on blocked requests
- **Export**: Built-in `to_json()`, `to_jsonl()`

## CLI & Interactive Shell

### Terminal Extraction (No Code)
```bash
# Extract to markdown
scrapling extract get 'https://example.com' content.md

# Extract specific element
scrapling extract get 'https://example.com' content.txt \\
  --css-selector '.article' \\
  --impersonate 'chrome'

# Stealth mode
scrapling extract stealthy-fetch 'https://protected.com' content.md \\
  --no-headless \\
  --solve-cloudflare
```

### Interactive Shell
```bash
scrapling shell

# Inside shell:
>>> page = Fetcher.get('https://example.com')
>>> page.css('h1::text').get()
>>> page.find_all('div', class_='item')
```

## Parser API (Beyond CSS/XPath)

### BeautifulSoup-Style Methods
```python
# Find by attributes
page.find_all('div', {'class': 'product', 'data-id': True})
page.find_all('div', class_='product', id=re.compile(r'item-\\d+'))

# Text search
page.find_by_text('Add to Cart', tag='button')
page.find_by_regex(r'\\$\\d+\\.\\d{2}')

# Navigation
first = page.css('.product')[0]
parent = first.parent
siblings = first.next_siblings
children = first.children

# Similarity
similar = first.find_similar()  # Find visually/structurally similar elements
below = first.below_elements()  # Elements below in DOM
```

### Auto-Generated Selectors
```python
# Get robust selector for any element
element = page.css('.product')[0]
selector = element.auto_css_selector()  # Returns stable CSS path
xpath = element.auto_xpath()
```

## Proxy Rotation

```python
from scrapling.spiders import ProxyRotator

# Cyclic rotation
rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://user:pass@proxy3:8080"
], strategy="cyclic")

# Use with any session
with FetcherSession(proxy=rotator.next()) as session:
    page = session.get('https://example.com')
```

## Common Recipes

### Pagination Patterns
```python
# Page numbers
for page_num in range(1, 11):
    url = f"https://example.com/products?page={page_num}"
    ...

# Next button
while next_page := response.css('.next a::attr(href)').get():
    yield response.follow(next_page)

# Infinite scroll (DynamicFetcher)
with DynamicSession() as session:
    page = session.fetch(url)
    page.scroll_to_bottom()
    items = page.css('.item').getall()
```

### Login Sessions
```python
with StealthySession(headless=False) as session:
    # Login
    login_page = session.fetch('https://example.com/login')
    login_page.fill('input[name="username"]', 'user')
    login_page.fill('input[name="password"]', 'pass')
    login_page.click('button[type="submit"]')
    
    # Now session has cookies
    protected_page = session.fetch('https://example.com/dashboard')
```

### Next.js Data Extraction
```python
# Extract JSON from __NEXT_DATA__
import json
import re

next_data = json.loads(
    re.search(
        r'__NEXT_DATA__" type="application/json">(.*?)</script>',
        page.html_content,
        re.S
    ).group(1)
)
props = next_data['props']['pageProps']
```

## Output Formats

```python
# JSON (pretty)
result.items.to_json('output.json')

# JSONL (streaming, one per line)
result.items.to_jsonl('output.jsonl')

# Python objects
for item in result.items:
    print(item['title'])
```

## Performance Tips

1. **Use HTTP fetcher when possible** — 10-100x faster than browser
2. **Impersonate browsers** — `impersonate='chrome'` for TLS fingerprinting
3. **HTTP/3 support** — `FetcherSession(http3=True)`
4. **Limit resources** — `disable_resources=True` in Dynamic/Stealthy
5. **Connection pooling** — Reuse sessions across requests

## Guardrails (Always)

- Only scrape content you're authorized to access
- Respect robots.txt and ToS
- Add delays (`download_delay`) for large crawls
- Don't bypass paywalls or authentication without permission
- Never scrape personal/sensitive data

## References

- `references/mcp-setup.md` — Detailed MCP configuration
- `references/anti-bot.md` — Anti-bot handling strategies
- `references/proxy-rotation.md` — Proxy setup and rotation
- `references/spider-recipes.md` — Advanced crawling patterns
- `references/api-reference.md` — Quick API reference
- `references/links.md` — Official docs links

## Scripts

- `scripts/scrapling_scrape.py` — Quick one-off extraction
- `scripts/scrapling_smoke_test.py` — Test connectivity and anti-bot indicators
