---
name: opencli-web-automation
description: Turn any website into a CLI using browser session reuse and AI-powered command discovery
triggers:
  - "use opencli to scrape a website"
  - "make a CLI command for a website"
  - "automate browser with opencli"
  - "add a new opencli adapter"
  - "extract data from website using CLI"
  - "opencli explore and synthesize commands"
  - "create yaml adapter for opencli"
  - "opencli browser automation"
---

# OpenCLI Web Automation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenCLI turns any website into a command-line interface by reusing Chrome's logged-in browser session. It supports 19 sites and 80+ commands out of the box, and lets you add new adapters via TypeScript or YAML dropped into the `clis/` folder.

---

## Installation

```bash
# Install globally via npm
npm install -g @jackwener/opencli

# One-time setup: discovers Playwright MCP token and distributes to all tools
opencli setup

# Verify everything is working
opencli doctor --live
```

### Prerequisites

- Node.js >= 18.0.0
- Chrome browser **running and logged into the target site**
- [Playwright MCP Bridge](https://chromewebstore.google.com/detail/playwright-mcp-bridge/mmlmfjhmonkocbjadbfplnigmagldckm) extension installed in Chrome

### Install from Source (Development)

```bash
git clone git@github.com:jackwener/opencli.git
cd opencli
npm install
npm run build
npm link
```

---

## Environment Configuration

```bash
# Required: set in ~/.zshrc or ~/.bashrc after running opencli setup
export PLAYWRIGHT_MCP_EXTENSION_TOKEN="<your-token-from-setup>"
```

MCP client config (Claude/Cursor/Codex `~/.config/*/config.json`):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--extension"],
      "env": {
        "PLAYWRIGHT_MCP_EXTENSION_TOKEN": "$PLAYWRIGHT_MCP_EXTENSION_TOKEN"
      }
    }
  }
}
```

---

## Key CLI Commands

### Discovery & Registry

```bash
opencli list                        # Show all registered commands
opencli list -f yaml                # Output registry as YAML
opencli list -f json                # Output registry as JSON
```

### Running Built-in Commands

```bash
# Public API commands (no browser login needed)
opencli hackernews top --limit 10
opencli github search "playwright automation"
opencli bbc news

# Browser commands (must be logged into site in Chrome)
opencli bilibili hot --limit 5
opencli twitter trending
opencli zhihu hot -f json
opencli reddit frontpage --limit 20
opencli xiaohongshu search "TypeScript"
opencli youtube search "browser automation"
opencli linkedin search "senior engineer"
```

### Output Formats

All commands support `--format` / `-f`:

```bash
opencli bilibili hot -f table     # Rich terminal table (default)
opencli bilibili hot -f json      # JSON (pipe to jq)
opencli bilibili hot -f yaml      # YAML
opencli bilibili hot -f md        # Markdown
opencli bilibili hot -f csv       # CSV export
opencli bilibili hot -v           # Verbose: show pipeline debug steps
```

### AI Agent Workflow (Creating New Commands)

```bash
# 1. Deep explore a site — discovers APIs, auth, capabilities
opencli explore https://example.com --site mysite

# 2. Synthesize YAML adapters from explore artifacts
opencli synthesize mysite

# 3. One-shot: explore → synthesize → register in one command
opencli generate https://example.com --goal "hot posts"

# 4. Strategy cascade — auto-probes PUBLIC → COOKIE → HEADER auth
opencli cascade https://api.example.com/data
```

Explore artifacts are saved to `.opencli/explore/<site>/`:
- `manifest.json` — site metadata
- `endpoints.json` — discovered API endpoints
- `capabilities.json` — inferred command capabilities
- `auth.json` — authentication strategy

---

## Adding a New Adapter

### Option 1: YAML Declarative Adapter

Drop a `.yaml` file into `clis/` — auto-registered on next run:

```yaml
# clis/producthunt.yaml
site: producthunt
commands:
  - name: trending
    description: Get trending products on Product Hunt
    args:
      - name: limit
        type: number
        default: 10
    pipeline:
      - type: navigate
        url: https://www.producthunt.com
      - type: waitFor
        selector: "[data-test='post-item']"
      - type: extract
        selector: "[data-test='post-item']"
        fields:
          name:
            selector: "h3"
            type: text
          tagline:
            selector: "p"
            type: text
          votes:
            selector: "[data-test='vote-button']"
            type: text
          url:
            selector: "a"
            attr: href
      - type: limit
        count: "{{limit}}"
```

### Option 2: TypeScript Adapter

```typescript
// clis/producthunt.ts
import type { CLIAdapter } from "../src/types";

const adapter: CLIAdapter = {
  site: "producthunt",
  commands: [
    {
      name: "trending",
      description: "Get trending products on Product Hunt",
      options: [
        {
          flags: "--limit <n>",
          description: "Number of results",
          defaultValue: "10",
        },
      ],
      async run(options, browser) {
        const page = await browser.currentPage();
        await page.goto("https://www.producthunt.com");
        await page.waitForSelector("[data-test='post-item']");

        const products = await page.evaluate(() => {
          return Array.from(
            document.querySelectorAll("[data-test='post-item']")
          ).map((el) => ({
            name: el.querySelector("h3")?.textContent?.trim() ?? "",
            tagline: el.querySelector("p")?.textContent?.trim() ?? "",
            votes:
              el
                .querySelector("[data-test='vote-button']")
                ?.textContent?.trim() ?? "",
            url:
              (el.querySelector("a") as HTMLAnchorElement)?.href ?? "",
          }));
        });

        return products.slice(0, Number(options.limit));
      },
    },
  ],
};

export default adapter;
```

---

## Common Patterns

### Pattern: Authenticated API Extraction (Cookie Injection)

```typescript
// When a site exposes a JSON API but requires login cookies
async run(options, browser) {
  const page = await browser.currentPage();

  // Navigate first to ensure cookies are active
  await page.goto("https://api.example.com");

  const data = await page.evaluate(async () => {
    const res = await fetch("/api/v1/feed?limit=20", {
      credentials: "include", // reuse browser cookies
    });
    return res.json();
  });

  return data.items;
}
```

### Pattern: Header Token Extraction

```typescript
// Extract auth tokens from browser storage for API calls
async run(options, browser) {
  const page = await browser.currentPage();
  await page.goto("https://example.com");

  const token = await page.evaluate(() => {
    return localStorage.getItem("auth_token") ||
           sessionStorage.getItem("token");
  });

  const data = await page.evaluate(async (tok) => {
    const res = await fetch("/api/data", {
      headers: { Authorization: `Bearer ${tok}` },
    });
    return res.json();
  }, token);

  return data;
}
```

### Pattern: DOM Scraping with Wait

```typescript
async run(options, browser) {
  const page = await browser.currentPage();
  await page.goto("https://news.ycombinator.com");

  // Wait for dynamic content to load
  await page.waitForSelector(".athing", { timeout: 10000 });

  return page.evaluate((limit) => {
    return Array.from(document.querySelectorAll(".athing"))
      .slice(0, limit)
      .map((row) => ({
        title: row.querySelector(".titleline a")?.textContent?.trim(),
        url: (row.querySelector(".titleline a") as HTMLAnchorElement)?.href,
        score:
          row.nextElementSibling
            ?.querySelector(".score")
            ?.textContent?.trim() ?? "0",
      }));
  }, Number(options.limit));
}
```

### Pattern: Pagination

```typescript
async run(options, browser) {
  const page = await browser.currentPage();
  const results = [];
  let pageNum = 1;

  while (results.length < Number(options.limit)) {
    await page.goto(`https://example.com/posts?page=${pageNum}`);
    await page.waitForSelector(".post-item");

    const items = await page.evaluate(() =>
      Array.from(document.querySelectorAll(".post-item")).map((el) => ({
        title: el.querySelector("h2")?.textContent?.trim(),
        url: (el.querySelector("a") as HTMLAnchorElement)?.href,
      }))
    );

    if (items.length === 0) break;
    results.push(...items);
    pageNum++;
  }

  return results.slice(0, Number(options.limit));
}
```

---

## Maintenance Commands

```bash
# Diagnose token and config across all tools
opencli doctor

# Test live browser connectivity
opencli doctor --live

# Fix mismatched configs interactively
opencli doctor --fix

# Fix all configs non-interactively
opencli doctor --fix -y
```

---

## Testing

```bash
npm run build

# Run all tests
npx vitest run

# Unit tests only
npx vitest run src/

# E2E tests only
npx vitest run tests/e2e/

# Headless browser mode for CI
OPENCLI_HEADLESS=1 npx vitest run tests/e2e/
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Failed to connect to Playwright MCP Bridge` | Ensure extension is enabled in Chrome; restart Chrome after install |
| Empty data / `Unauthorized` | Open Chrome, navigate to the site, log in or refresh the page |
| Node API errors | Upgrade to Node.js >= 18 |
| Token not found | Run `opencli setup` or `opencli doctor --fix` |
| Stale login session | Visit the target site in Chrome and interact with it to prove human presence |

### Debug Verbose Mode

```bash
# See full pipeline execution steps
opencli bilibili hot -v

# Check what explore discovered
cat .opencli/explore/mysite/endpoints.json
cat .opencli/explore/mysite/auth.json
```

---

## Project Structure (for Adapter Authors)

```
opencli/
├── clis/               # Drop .ts or .yaml adapters here (auto-registered)
│   ├── bilibili.ts
│   ├── twitter.ts
│   └── hackernews.yaml
├── src/
│   ├── types.ts        # CLIAdapter, Command interfaces
│   ├── browser.ts      # Playwright MCP bridge wrapper
│   ├── loader.ts       # Dynamic adapter loader
│   └── output.ts       # table/json/yaml/md/csv formatters
├── tests/
│   └── e2e/            # E2E tests per site
└── CLI-EXPLORER.md     # Full AI agent exploration workflow
```
