---
name: hyperbrowser-mcp
description: Hyperbrowser Model Context Protocol (MCP) server for cloud headless browser automation, dynamic SPA crawling, session recording, and stealth web scraping (hyperbrowserai/mcp). Use when the agent needs to render complex JavaScript single-page apps, crawl websites, or execute browser agents.
---

# Hyperbrowser MCP (Cloud Headless Browser Automation & Crawling)

Based on [hyperbrowserai/mcp](https://github.com/hyperbrowserai/mcp): an MCP server providing cloud headless browser automation, dynamic JavaScript rendering, full-site crawling, and structured web data extraction for AI agents.

---

## 🎯 When to Use
- **Complex Single-Page Applications (SPAs):** Scraping websites that rely on heavy client-side JavaScript, React/Vue hydration, or WebGL where static HTML extractors return blank templates.
- **Deep Site Crawling:** Recursively following links across web applications, documentation trees, or API portals.
- **Stealth Browsing & Session Recordings:** Recording video replays and interaction traces of web navigation for verification and audit trails.
- **Browser Agent Delegation:** Powering browser agents (such as Claude Computer Use, OpenAI CUA, or Browser Use).

---

## 🚀 Setup & Registration

### MCP Configuration
Register Hyperbrowser MCP in your agent's configuration (`.mcp.json` or IDE settings):

```json
{
  "mcpServers": {
    "hyperbrowser": {
      "command": "npx",
      "args": ["-y", "hyperbrowser-mcp"],
      "env": {
        "HYPERBROWSER_API_KEY": "YOUR_HYPERBROWSER_API_KEY"
      }
    }
  }
}
```

---

## 🛠️ Key Capabilities & Tools
- `crawl_page`: Crawls dynamic web applications and returns fully rendered DOM contents and structured link trees.
- `extract_data`: Uses vision and LLM parsing to turn visual elements on web pages into clean JSON data models.
- `record_session`: Records full interactive browser sessions into shareable artifacts for test reports and audits.

---

## ⚡ Integration with REA & Security Audits
- **Auditing Client-Side Rendered Applications:** Render Next.js, Nuxt, or Vite web apps in Hyperbrowser to intercept WebSocket connections, runtime-injected scripts, and dynamic API calls that do not appear in raw HTML.
- **Visual Regression Verification:** Capture live renders of web applications after applying security headers or CSP rules to confirm user interface integrity.
