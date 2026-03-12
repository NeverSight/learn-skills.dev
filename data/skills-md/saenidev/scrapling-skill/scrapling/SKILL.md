---
name: scrapling
description: Scrapling web scraping reference for this project. Provides fetcher selection (Fetcher/DynamicFetcher/StealthyFetcher), selector patterns, session management, anti-bot bypass, adaptive/self-healing selectors, Spider framework for crawling, proxy rotation, CLI commands, and MCP server for AI integration. Use when implementing web scraping, handling protected sites, or building data extraction pipelines.
---

# Scrapling

Adaptive, high-performance Python web scraping library. 774x faster than BeautifulSoup. Auto-relocates elements when websites change structure.

**Key capabilities:** HTTP/browser fetching, Cloudflare bypass, adaptive selectors, Spider crawling framework, proxy rotation, CLI tools, MCP server for AI agents.

> **v0.4 breaking changes:** `css_first()`/`xpath_first()` are removed — use `.css('.sel').first` or `.css('.sel').get()` instead. `css('::text')` and `css('::attr()')` now return `Selector` objects (not `TextHandler`). `Response.body` is always `bytes`.

## Quick Start

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
titles = page.css('.title::text')
links = page.css('a.link::attr(href)').getall()

# Response metadata
print(page.status, page.headers, page.cookies)
```

### Global Configuration

```python
Fetcher.configure(adaptive=True, encoding="utf-8", keep_comments=False)
```

## Fetcher Selection

| Need | Use | Why |
|------|-----|-----|
| Static HTML | `Fetcher` | Fastest, TLS spoofing |
| JavaScript content | `DynamicFetcher` | Playwright browser |
| Cloudflare/anti-bot | `StealthyFetcher` | Camoufox + stealth |
| Multi-page crawl | `Spider` | Async crawling framework |

See [references/fetchers.md](references/fetchers.md) for complete fetcher options.

## Common Patterns

### Basic Scraping

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.example.com')

for quote in page.css('.quote'):
    text = quote.css('.text').first.text
    author = quote.css('.author').first.text
    print(f'{text} - {author}')
```

### JavaScript-Rendered Content

```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch(
    'https://spa-app.com',
    headless=True,
    network_idle=True,
    wait_selector='.content-loaded'
)
```

### Cloudflare Bypass

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    humanize=True,
    headless=True
)
```

### Session with Cookies

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    session.get('https://site.com/login')
    dashboard = session.get('https://site.com/dashboard')
```

### Multi-Page Crawling (Spider)

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com/"]

    async def parse(self, response: Response):
        for item in response.css('.product'):
            yield {"title": item.css('h2::text').get()}

MySpider().start()
```

See [references/spiders.md](references/spiders.md) for the full Spider framework.

### Proxy Rotation

```python
from scrapling.engines.toolbelt import ProxyRotator

rotator = ProxyRotator(["http://proxy1:8080", "http://proxy2:8080"])
page = Fetcher.get('https://example.com', proxy_rotator=rotator)
```

### Adaptive Selectors (Self-Healing)

```python
from scrapling import Selector

# Save element properties on first visit (storage defaults to SQLite)
selector = Selector(html, url='https://example.com', adaptive=True)
products = selector.css('.product-card', auto_save=True)

# On subsequent runs, relocate even if structure changed
products = selector.css('.product-card', adaptive=True)
```

## Element Selection

```python
# CSS (recommended)
page.css('.class')              # Multiple → Selectors list
page.css('.class').first        # Single (safe, returns None if missing)
page.css('.class').get()        # First as TextHandler (alias: extract_first)
page.css('.title::text')        # Text extraction → Selector objects
page.css('a::attr(href)')       # Attribute → Selector objects

# XPath
page.xpath('//div[@id="main"]')
page.xpath('//h1').first

# BeautifulSoup-style
page.find('div', class_='content')
page.find_all('a', attrs={'data-type': 'link'})

# Text search (no tag= param — filter by tag separately if needed)
page.find_by_text('Add to Cart')
page.css('button').filter(lambda el: el.text == 'Add to Cart').first
```

> **Note:** `.first` and `.last` are safe accessors — they return `None` instead of raising `IndexError`.

See [references/selectors.md](references/selectors.md) for navigation and advanced selection.

## Element Navigation

```python
el = page.css('.target').first
el.parent                # Parent element
el.children              # Child elements
el.next                  # Next sibling
el.previous              # Previous sibling
el.siblings              # All siblings
el.text                  # Inner text
el.text.clean()          # Whitespace-normalized text
el.attrib['href']        # Attribute access
```

## Parse Existing HTML

```python
from scrapling.parser import Selector

html = '<div class="item">Content</div>'
page = Selector(html)
content = page.css('.item').first.text
```

## CLI Usage

```bash
# Interactive shell
scrapling shell

# Extract from URL (output format by extension: .html, .md, .txt)
scrapling extract get 'https://example.com' output.md --css-selector '.content'

# Dynamic content with browser
scrapling extract fetch 'https://spa.com' out.html --network-idle

# Cloudflare bypass
scrapling extract stealthy-fetch 'https://site.com' out.html --solve-cloudflare
```

See [references/cli.md](references/cli.md) for all commands and options.

## Error Handling

```python
from scrapling.fetchers import Fetcher

try:
    page = Fetcher.get('https://example.com', timeout=10)  # seconds
    element = page.css('.target').first
    if element:
        print(element.text)
    else:
        print('Element not found')
except Exception as e:
    print(f'Request failed: {e}')
```

## MCP Server (AI Integration)

Enables AI agents (Claude Desktop/Code) to scrape via natural language:

```bash
pip install "scrapling[ai]"
scrapling install
```

Tools: `get`, `bulk_get`, `fetch`, `bulk_fetch`, `stealthy_fetch`, `bulk_stealthy_fetch`

See [references/mcp.md](references/mcp.md) for configuration.

## Resources

- [references/fetchers.md](references/fetchers.md) - Complete fetcher options and configurations
- [references/selectors.md](references/selectors.md) - Selector methods and element navigation
- [references/spiders.md](references/spiders.md) - Spider crawling framework
- [references/cli.md](references/cli.md) - CLI commands reference
- [references/adaptive.md](references/adaptive.md) - Self-healing selector system
- [references/mcp.md](references/mcp.md) - MCP server for AI integration
- [scripts/scrape_list.py](scripts/scrape_list.py) - CLI tool for extracting list items to JSON/CSV
