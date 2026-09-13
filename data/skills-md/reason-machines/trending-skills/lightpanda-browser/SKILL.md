---
name: lightpanda-browser
description: Expert skill for Lightpanda — the headless browser built in Zig for AI agents and automation. 9x less memory, 11x faster than Chrome. Installation, CLI, CDP server, Playwright/Puppeteer integration, and web scraping.
triggers:
  - lightpanda
  - headless browser for AI
  - lightweight headless browser
  - CDP automation
  - web scraping automation
  - zig browser
  - lightpanda browser
  - fast headless browser
---

# Lightpanda — Headless Browser for AI & Automation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

Lightpanda is a headless browser built from scratch in Zig, designed for AI agents, web scraping, and automation. It uses 9x less memory and runs 11x faster than Chrome headless.

**Key facts:**
- Not based on Chromium, Blink, or WebKit — clean-slate Zig implementation
- JavaScript execution via V8 engine
- CDP (Chrome DevTools Protocol) compatible — works with Playwright, Puppeteer, chromedp
- Respects `robots.txt` via `--obey_robots` flag
- Beta status, actively developed
- License: AGPL-3.0

## Installation

### macOS (Apple Silicon)

```bash
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos
chmod a+x ./lightpanda
```

### Linux (x86_64)

```bash
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux
chmod a+x ./lightpanda
```

### Docker

```bash
# Supports amd64 and arm64
docker run -d --name lightpanda -p 9222:9222 lightpanda/browser:nightly
```

## CLI Usage

### Fetch a URL (dump rendered HTML)

```bash
./lightpanda fetch --obey_robots --log_format pretty --log_level info https://example.com
```

### Start CDP Server

```bash
./lightpanda serve --obey_robots --log_format pretty --log_level info --host 127.0.0.1 --port 9222
```

This launches a WebSocket-based CDP server for programmatic control.

### CLI Flags

| Flag | Description |
|------|-------------|
| `--obey_robots` | Respect robots.txt rules |
| `--log_format pretty` | Human-readable log output |
| `--log_level info` | Log verbosity: `debug`, `info`, `warn`, `error` |
| `--host 127.0.0.1` | Bind address for CDP server |
| `--port 9222` | Port for CDP server |
| `--insecure_disable_tls_host_verification` | Disable TLS verification (testing only) |

## Playwright Integration

Start the CDP server, then connect Playwright to it:

```javascript
import { chromium } from 'playwright-core';

const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = await browser.contexts()[0] || await browser.newContext();
const page = await context.newPage();

await page.goto('https://example.com', { waitUntil: 'networkidle' });
const title = await page.title();
const content = await page.content();

console.log(`Title: ${title}`);
console.log(`HTML length: ${content.length}`);

await browser.close();
```

## Puppeteer Integration

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://127.0.0.1:9222',
});

const context = await browser.createBrowserContext();
const page = await context.newPage();

await page.goto('https://example.com', { waitUntil: 'networkidle0' });

const title = await page.title();
const text = await page.evaluate(() => document.body.innerText);

console.log(`Title: ${title}`);
console.log(`Body text: ${text.substring(0, 200)}`);

await page.close();
await browser.close();
```

## Go (chromedp) Integration

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/chromedp/chromedp"
)

func main() {
    allocCtx, cancel := chromedp.NewRemoteAllocator(context.Background(), "ws://127.0.0.1:9222")
    defer cancel()

    ctx, cancel := chromedp.NewContext(allocCtx)
    defer cancel()

    var title string
    err := chromedp.Run(ctx,
        chromedp.Navigate("https://example.com"),
        chromedp.Title(&title),
    )
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Title:", title)
}
```

## Python Integration

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com", wait_until="networkidle")
        title = await page.title()
        content = await page.content()

        print(f"Title: {title}")
        print(f"HTML length: {len(content)}")

        await browser.close()

asyncio.run(main())
```

## Web Scraping Patterns

### Batch Page Fetching

```javascript
import { chromium } from 'playwright-core';

const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = await browser.newContext();

const urls = [
  'https://example.com/page1',
  'https://example.com/page2',
  'https://example.com/page3',
];

for (const url of urls) {
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });

  const data = await page.evaluate(() => ({
    title: document.title,
    text: document.body.innerText,
    links: [...document.querySelectorAll('a[href]')].map(a => a.href),
  }));

  console.log(JSON.stringify(data, null, 2));
  await page.close();
}

await browser.close();
```

### Extract Structured Data

```javascript
const data = await page.evaluate(() => {
  const items = document.querySelectorAll('.product-card');
  return [...items].map(item => ({
    name: item.querySelector('h2')?.textContent?.trim(),
    price: item.querySelector('.price')?.textContent?.trim(),
    link: item.querySelector('a')?.href,
  }));
});
```

## Docker Compose (with your app)

```yaml
services:
  lightpanda:
    image: lightpanda/browser:nightly
    ports:
      - "9222:9222"
    restart: unless-stopped

  scraper:
    build: .
    depends_on:
      - lightpanda
    environment:
      - BROWSER_WS_ENDPOINT=ws://lightpanda:9222
```

## Supported Web APIs

Lightpanda supports (partial, expanding):
- DOM tree manipulation and querying
- JavaScript execution (V8)
- XMLHttpRequest (XHR)
- Fetch API
- Cookie management
- Network interception
- Proxy support

## Configuration

| Environment Variable | Description |
|---------------------|-------------|
| `LIGHTPANDA_DISABLE_TELEMETRY` | Set to `true` to opt out of usage metrics |

## Performance Comparison

| Metric | Lightpanda | Chrome Headless |
|--------|-----------|-----------------|
| Memory | ~9x less | Baseline |
| Speed | ~11x faster | Baseline |
| Binary size | Small (Zig) | Large (Chromium) |
| Rendering | No visual rendering | Full rendering engine |

## When to Use Lightpanda

**Use Lightpanda when:**
- Running AI agents that need to browse the web
- Batch scraping at scale (memory/CPU savings matter)
- Automating form submissions and data extraction
- Running in containers where resources are limited
- You need CDP compatibility but not full visual rendering

**Use Chrome/Playwright instead when:**
- You need pixel-perfect screenshots or PDF generation
- You need full Web API coverage (Lightpanda is still partial)
- Visual regression testing
- Testing browser-specific rendering behavior

## Building from Source

Requires: Zig 0.15.2, Rust, CMake, system dependencies.

```bash
# Ubuntu/Debian dependencies
sudo apt install xz-utils ca-certificates pkg-config libglib2.0-dev clang make curl

# Build
git clone https://github.com/lightpanda-io/browser.git
cd browser
zig build

# Optional: pre-build V8 snapshot for faster startup
zig build snapshot_creator -- src/snapshot.bin
zig build -Dsnapshot_path=../../snapshot.bin
```

## Troubleshooting

**Connection refused on port 9222:**
- Ensure `./lightpanda serve` is running
- Check `--host 0.0.0.0` if connecting from Docker/remote

**Playwright script breaks after update:**
- Lightpanda is beta — Playwright's capability detection may behave differently across versions
- Pin your Lightpanda version or use nightly consistently

**Missing Web API support:**
- Check the [zig-js-runtime](https://github.com/lightpanda-io/zig-js-runtime) repo for current API coverage
- File issues at [lightpanda-io/browser](https://github.com/lightpanda-io/browser/issues)

## Links

- GitHub: https://github.com/lightpanda-io/browser
- Runtime APIs: https://github.com/lightpanda-io/zig-js-runtime
