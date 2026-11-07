---
name: aibijia-price-comparison
description: AI token price comparison platform that scrapes and aggregates prices across multiple platforms to help users find cheap, reliable AI account tokens
triggers:
  - compare AI token prices
  - find cheap ChatGPT plus
  - scrape AI account prices
  - build price comparison for AI tokens
  - submit token vendor to aibijia
  - aggregate AI CDK prices
  - find reliable AI token resellers
  - price scraping multiple platforms
---

# Aibijia Price Comparison Platform

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Aibijia is a multi-platform price scraping and comparison website for AI tokens (ChatGPT Plus CDKs, API keys, etc.). It aggregates prices from various resellers/agents across platforms, helping users find the cheapest reliable source and avoid scams.

**Live site:** https://aibijia.org  
**Telegram:** https://t.me/ai_bi_jia_notice

---

## What This Project Does

- **Scrapes** token/CDK prices from multiple card-selling platforms (卡网)
- **Compares** prices across vendors for the same type of AI account (e.g., ChatGPT Plus, GPT Pro)
- **Aggregates** vendor reliability info via community submissions
- **Exposes** price differences between resellers sourcing from the same upstream

## Project Structure

Since the repo is primarily a community/data project with a web frontend, the core components are:

```
AIbijia/
├── assets/           # Static assets (banner, images)
├── data/             # Price data / scraped results (JSON/CSV)
├── scrapers/         # Platform price scrapers
├── frontend/         # Website UI (aibijia.org)
└── SKILL.md
```

---

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/ka-pi-ba-la/AIbijia.git
cd AIbijia
```

### Install Dependencies

If Python-based scrapers:

```bash
pip install -r requirements.txt
```

If Node.js-based:

```bash
npm install
# or
pnpm install
```

---

## Core Concepts

### Token Types Tracked

| Token Type | Example Price Range | Notes |
|---|---|---|
| ChatGPT Plus CDK | ¥30–¥60 | Same upstream, different markup |
| GPT Pro (shared) | ~¥20/person | Split among multiple users |
| API Keys (各模型) | Varies | Per-token pricing |
| Claude / Gemini | Varies | Scraped from resellers |

### Price Scraping Pattern

```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class TokenPriceScraper:
    """
    Base scraper for AI token price platforms.
    Each platform subclasses this with custom parsing.
    """
    
    def __init__(self, platform_name: str, base_url: str):
        self.platform_name = platform_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; Aibijia/1.0)"
        })
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    
    def parse_prices(self, soup: BeautifulSoup) -> list[dict]:
        """Override in subclass to extract price data."""
        raise NotImplementedError
    
    def scrape(self) -> list[dict]:
        soup = self.fetch_page(self.base_url)
        prices = self.parse_prices(soup)
        
        # Annotate with metadata
        for item in prices:
            item["platform"] = self.platform_name
            item["scraped_at"] = datetime.utcnow().isoformat()
        
        return prices


class KawangScraper(TokenPriceScraper):
    """Example scraper for a 卡网 (card platform)."""
    
    def parse_prices(self, soup: BeautifulSoup) -> list[dict]:
        results = []
        
        # Adapt selectors to target platform's HTML structure
        for card in soup.select(".product-card"):
            name = card.select_one(".product-name")
            price = card.select_one(".product-price")
            stock = card.select_one(".product-stock")
            
            if name and price:
                results.append({
                    "name": name.get_text(strip=True),
                    "price_cny": float(
                        price.get_text(strip=True)
                             .replace("¥", "")
                             .replace(",", "")
                    ),
                    "in_stock": stock and "有货" in stock.get_text(),
                })
        
        return results
```

### Aggregating Prices Across Platforms

```python
import asyncio
import aiohttp
from dataclasses import dataclass

@dataclass
class PriceListing:
    token_type: str
    platform: str
    price_cny: float
    in_stock: bool
    url: str
    scraped_at: str

async def aggregate_all_platforms(platforms: list[TokenPriceScraper]) -> list[PriceListing]:
    """
    Run all scrapers concurrently and merge results.
    """
    results = []
    
    async def run_scraper(scraper):
        loop = asyncio.get_event_loop()
        # Run sync scraper in thread pool
        data = await loop.run_in_executor(None, scraper.scrape)
        return data
    
    tasks = [run_scraper(p) for p in platforms]
    all_data = await asyncio.gather(*tasks, return_exceptions=True)
    
    for platform_data in all_data:
        if isinstance(platform_data, Exception):
            print(f"Scraper error: {platform_data}")
            continue
        results.extend(platform_data)
    
    return results


def find_cheapest(listings: list[PriceListing], token_type: str) -> list[PriceListing]:
    """Filter and sort by price for a specific token type."""
    filtered = [
        l for l in listings
        if token_type.lower() in l.token_type.lower()
        and l.in_stock
    ]
    return sorted(filtered, key=lambda x: x.price_cny)


# Usage
async def main():
    platforms = [
        KawangScraper("platform_a", "https://example-card-site-a.com/chatgpt"),
        KawangScraper("platform_b", "https://example-card-site-b.com/chatgpt"),
    ]
    
    all_listings = await aggregate_all_platforms(platforms)
    cheapest = find_cheapest(all_listings, "ChatGPT Plus")
    
    print("Cheapest ChatGPT Plus CDKs:")
    for listing in cheapest[:5]:
        print(f"  ¥{listing.price_cny} — {listing.platform}")

asyncio.run(main())
```

---

## Vendor Submission API

The site exposes a submission endpoint for community-sourced vendors:

```python
import requests
import os

AIBIJIA_API = "https://aibijia.org/api"  # hypothetical endpoint

def submit_vendor(vendor_info: dict) -> dict:
    """
    Submit a new vendor/price source for review.
    
    vendor_info keys:
      - name: str          Vendor/platform name
      - url: str           Purchase URL
      - token_type: str    e.g. "ChatGPT Plus CDK"
      - price_cny: float   Current price in RMB
      - notes: str         Optional reliability notes
    """
    resp = requests.post(
        f"{AIBIJIA_API}/submit",
        json=vendor_info,
        headers={
            "Content-Type": "application/json",
            # Use env var if auth is required:
            "Authorization": f"Bearer {os.environ.get('AIBIJIA_API_KEY', '')}",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


# Example usage
result = submit_vendor({
    "name": "某卡网",
    "url": "https://example-card-site.com/gpt-plus",
    "token_type": "ChatGPT Plus CDK",
    "price_cny": 32.0,
    "notes": "24h售后，支持补货",
})
print(result)
```

---

## Data Storage Pattern

```python
import json
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("./data")

def save_price_snapshot(listings: list[dict], token_type: str):
    """Save a timestamped price snapshot to data/."""
    DATA_DIR.mkdir(exist_ok=True)
    
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = DATA_DIR / f"{token_type.replace(' ', '_')}_{date_str}.json"
    
    snapshot = {
        "token_type": token_type,
        "captured_at": datetime.utcnow().isoformat(),
        "count": len(listings),
        "listings": listings,
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(listings)} listings to {filename}")


def load_latest_snapshot(token_type: str) -> dict | None:
    """Load the most recent snapshot for a token type."""
    pattern = f"{token_type.replace(' ', '_')}_*.json"
    files = sorted(DATA_DIR.glob(pattern), reverse=True)
    
    if not files:
        return None
    
    with open(files[0], encoding="utf-8") as f:
        return json.load(f)
```

---

## Community Reporting (Avoid Scams)

Post scam reports as GitHub Issues or submit to the repo:

```markdown
## 避雷报告模板

**平台名称：** xxx卡网
**购买时间：** 2026-04-28
**商品：** ChatGPT Plus CDK
**价格：** ¥35
**问题：** CDK已失效，无法联系售后
**证据：** [截图]
**建议：** 避免购买
```

---

## Configuration

```python
# config.py — Aibijia scraper configuration

import os

CONFIG = {
    # Scraping behavior
    "request_timeout": int(os.environ.get("SCRAPE_TIMEOUT", "10")),
    "rate_limit_seconds": float(os.environ.get("SCRAPE_RATE_LIMIT", "2.0")),
    "max_retries": int(os.environ.get("SCRAPE_MAX_RETRIES", "3")),
    
    # Proxy (optional, for bot detection avoidance)
    "proxy": os.environ.get("HTTP_PROXY", None),
    
    # Data output
    "data_dir": os.environ.get("DATA_DIR", "./data"),
    
    # Notifications (Telegram)
    "telegram_bot_token": os.environ.get("TELEGRAM_BOT_TOKEN"),
    "telegram_channel_id": os.environ.get("TELEGRAM_CHANNEL_ID"),
    
    # Price alert threshold (alert if price drops below X CNY)
    "alert_price_threshold": float(os.environ.get("ALERT_PRICE_CNY", "30.0")),
}
```

### Environment Variables

```bash
# .env (never commit this file)
SCRAPE_TIMEOUT=15
SCRAPE_RATE_LIMIT=3.0
HTTP_PROXY=http://proxy.example.com:8080
DATA_DIR=./data
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@ai_bi_jia_notice
ALERT_PRICE_CNY=28.0
```

---

## Telegram Price Alert Bot

```python
import os
import asyncio
from telegram import Bot

async def send_price_alert(listings: list[dict], threshold: float):
    """
    Send Telegram alert when ChatGPT Plus CDK drops below threshold price.
    """
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    channel = os.environ["TELEGRAM_CHANNEL_ID"]
    
    cheap = [l for l in listings if l["price_cny"] <= threshold and l["in_stock"]]
    
    if not cheap:
        return
    
    lines = [f"🔥 低价预警！ChatGPT Plus CDK ≤ ¥{threshold}\n"]
    for l in cheap[:5]:
        lines.append(f"• ¥{l['price_cny']} — {l['platform']}")
    
    await bot.send_message(
        chat_id=channel,
        text="\n".join(lines),
        disable_web_page_preview=True,
    )

asyncio.run(send_price_alert(all_listings, threshold=30.0))
```

---

## Common Patterns

### Daily Cron Job (GitHub Actions)

```yaml
# .github/workflows/scrape.yml
name: Daily Price Scrape

on:
  schedule:
    - cron: "0 2 * * *"   # 2 AM UTC daily
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python scrapers/run_all.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHANNEL_ID: ${{ secrets.TELEGRAM_CHANNEL_ID }}
      - uses: actions/upload-artifact@v4
        with:
          name: price-data
          path: data/
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Scraper returns empty results | Target site changed HTML structure | Update CSS selectors in `parse_prices()` |
| 403 / blocked requests | Bot detection on target platform | Add proxy via `HTTP_PROXY` env var or rotate User-Agent |
| Prices stale | Cron not running | Check GitHub Actions logs; run `python scrapers/run_all.py` manually |
| Telegram alerts not sending | Wrong token/channel | Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHANNEL_ID` env vars |
| CDK already used / invalid | Upstream fraud | Report in repo issues with evidence; avoid that vendor |

### Anti-Bot Countermeasures

```python
import time
import random

def polite_get(session, url: str, min_delay=1.5, max_delay=4.0) -> str:
    """Add random delay between requests to avoid rate limiting."""
    time.sleep(random.uniform(min_delay, max_delay))
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text
```

---

## Contributing Price Sources

1. Fork the repo
2. Add your vendor/source to `data/sources.json`
3. Open a PR with evidence of reliability (screenshots, purchase history)
4. Community reviews and merges

```json
// data/sources.json entry format
{
  "id": "vendor_slug",
  "name": "平台名称",
  "url": "https://example-card-site.com",
  "token_types": ["ChatGPT Plus CDK", "Claude API"],
  "verified": false,
  "submitted_by": "github_username",
  "notes": "24h售后，微信群支持"
}
```
