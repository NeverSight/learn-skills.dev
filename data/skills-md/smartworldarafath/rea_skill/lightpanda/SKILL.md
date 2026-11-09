---
name: lightpanda
description: Headless browser built from scratch for AI agents and automation workflows. 16x lighter and 9x faster than Chromium — 123MB peak memory vs 2GB, 5s vs 46s for 100 pages. Written in Zig, not a Chromium fork or WebKit patch. Use when integrating headless browser automation into AI agent pipelines, web scraping at scale, or any automation needing a lightweight, fast alternative to Puppeteer/Playwright with Chromium. Supports CDP (Chrome DevTools Protocol) for drop-in compatibility.
---

# Lightpanda Browser

The headless browser built from scratch for AI agents and automation.

> Not a Chromium fork. Not a WebKit patch. A new browser, written in Zig.
> **16x lighter and 9x faster than Chromium.**

## Benchmarks

933 real web pages over the network on an AWS EC2 m5.large instance:

| Metric | Lightpanda | Headless Chrome | Difference |
| :---- | :---- | :---- | :---- |
| Memory (peak, 100 pages) | 123MB | 2GB | ~16x less |
| Execution time (100 pages) | 5s | 46s | ~9x faster |

## Install

**Homebrew (macOS):**
```bash
brew install lightpanda-io/browser/lightpanda
```

**Arch Linux:**
```bash
yay -S lightpanda-nightly-bin
```

**Download:** [nightly builds](https://github.com/lightpanda-io/browser/releases/tag/nightly) for Linux and macOS (x86_64 and aarch64)

## Usage for AI Agents

Lightpanda supports CDP (Chrome DevTools Protocol), making it a drop-in replacement for Chromium in Puppeteer/Playwright workflows:

```javascript
// Use with Playwright (drop-in Chromium replacement)
const browser = await playwright.chromium.connectOverCDP('http://localhost:9222');
```

**Start Lightpanda:**
```bash
lightpanda serve --host 127.0.0.1 --port 9222
```

## Why Use for AI Agents

- **Memory efficiency:** Run hundreds of concurrent browser instances in a cloud environment
- **Speed:** 9x faster page loading means faster agent feedback loops
- **Cost:** 16x less memory means lower cloud infrastructure costs
- **CDN compatibility:** Full JavaScript execution, not just static HTML parsing
- **CDP compatibility:** Drop-in replacement in existing automation stacks

## Reference

- **Website:** [lightpanda.io](https://lightpanda.io)
- **Source:** [github.com/lightpanda-io/browser](https://github.com/lightpanda-io/browser)
- **License:** AGPL-3.0
- **Language:** Zig
