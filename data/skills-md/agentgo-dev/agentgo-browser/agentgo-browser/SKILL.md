---
name: agentgo-browser
description: Automates browser interactions using AgentGo's distributed cloud browser cluster via playwright@1.51.0. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information — running on AgentGo's remote cloud browsers instead of a local browser.
---

# Browser Automation with AgentGo Cloud Browsers

AgentGo provides a distributed cloud browser cluster. Connect via WebSocket using `chromium.connect()` from `playwright@1.51.0`.

> **Note:** Must use `playwright@1.51.0` exactly — newer versions have protocol incompatibilities with AgentGo's server.

## Get an API key

Register at **https://app.agentgo.live/** — free credits included, no credit card required.

```bash
export AGENTGO_API_KEY=your_api_key_here
```

## Install

```bash
npm install playwright@1.51.0
# or
pnpm add playwright@1.51.0
```

## Quick start

```typescript
import { chromium } from "playwright"; // must be playwright@1.51.0

const options = { _apikey: process.env.AGENTGO_API_KEY };
const serverUrl = `wss://app.browsers.live?launch-options=${encodeURIComponent(JSON.stringify(options))}`;

const browser = await chromium.connect(serverUrl);
const page = await browser.newPage();

await page.goto("https://example.com");
const title = await page.title();
console.log(title);

await browser.close();
```

## Connection helper

```typescript
import { chromium } from "playwright";

export async function connectAgentGo() {
  if (!process.env.AGENTGO_API_KEY)
    throw new Error("AGENTGO_API_KEY is not set");
  const opts = encodeURIComponent(JSON.stringify({ _apikey: process.env.AGENTGO_API_KEY }));
  return chromium.connect(`wss://app.browsers.live?launch-options=${opts}`);
}
```

## Basic interactions

```typescript
const browser = await connectAgentGo();
const page = await browser.newPage();

await page.goto("https://example.com");
await page.click("button#submit");
await page.fill("input[name=email]", "user@example.com");
await page.press("input[name=email]", "Enter");
await page.screenshot({ path: "screenshot.png" });

await browser.close();
```

## Extract data

```typescript
const browser = await connectAgentGo();
const page = await browser.newPage();
await page.goto("https://news.ycombinator.com");

const items = await page.$$eval(".titleline a", els =>
  els.map(a => ({ title: a.textContent, href: (a as HTMLAnchorElement).href }))
);

await browser.close();
return items;
```

## Multiple pages (parallel)

```typescript
const browser = await connectAgentGo();
const [page1, page2] = await Promise.all([browser.newPage(), browser.newPage()]);

await Promise.all([
  page1.goto("https://site-a.com"),
  page2.goto("https://site-b.com"),
]);

await browser.close();
```

## Always close in finally

```typescript
const browser = await connectAgentGo();
try {
  const page = await browser.newPage();
  await doWork(page);
} finally {
  await browser.close();
}
```

## Specific Tasks

- **Connection & auth** [references/connection.md](references/connection.md)
- **Session management** [references/session-management.md](references/session-management.md)
- **Running Playwright code** [references/running-code.md](references/running-code.md)
