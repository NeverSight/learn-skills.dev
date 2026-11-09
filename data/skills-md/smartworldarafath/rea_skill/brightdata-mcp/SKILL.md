---
name: brightdata-mcp
description: Bright Data Model Context Protocol (MCP) server for industrial web scraping, CAPTCHA bypass, residential proxy routing, and search engine data extraction (brightdata/brightdata-mcp). Use when the agent needs to bypass anti-bot walls, scrape protected websites, or collect public web intelligence.
---

# Bright Data MCP (Anti-Bot Web Scraping & Data Extraction)

Based on [brightdata/brightdata-mcp](https://github.com/brightdata/brightdata-mcp): an all-in-one Model Context Protocol (MCP) server providing AI agents with resilient, real-time public web access powered by Bright Data's Web Unlocker and proxy infrastructure.

---

## 🎯 When to Use
- **Anti-Bot & CAPTCHA Bypassing:** When target sites block curl, standard fetch, or headless browsers with Cloudflare, DataDome, or Akamai anti-bot challenges.
- **SERP & Search Engine Scraping:** Extracting Google, Bing, or DuckDuckGo search engine result pages (SERPs) with structured JSON output.
- **Large-Scale Public Web Extraction:** Scraping product catalogs, reviews, public directory profiles, or news articles without rate-limiting IP bans.

---

## 🚀 Setup & Registration

### MCP Configuration
Register Bright Data MCP in your agent's configuration (`.mcp.json` or IDE settings):

```json
{
  "mcpServers": {
    "brightdata": {
      "command": "npx",
      "args": ["-y", "@brightdata/mcp"],
      "env": {
        "BRIGHTDATA_API_KEY": "YOUR_BRIGHTDATA_API_KEY"
      }
    }
  }
}
```

*Note: Bright Data offers a free tier of 5,000 requests/month without credit card.*

---

## 🛠️ Key Capabilities & Tools
- `scrape_url`: Fetches clean HTML or Markdown content from any URL, automatically executing JavaScript and solving CAPTCHAs.
- `search_engine`: Runs structured queries across Google and returns ranked organic, sponsored, and snippet items.
- `extract_structured_data`: Converts target pages directly into validated JSON schemas.

---

## ⚡ Integration with REA & Security Audits
- **Auditing Blocked Endpoints:** When an external target API or website endpoint returns `403 Forbidden` due to IP reputation, route through Bright Data MCP to analyze real response headers and payloads.
- **Competitor & Pre-Release Research:** Gather public security advisories and competitor feature implementations without triggering rate limits.
