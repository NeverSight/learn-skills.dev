---
name: webmcp-browser-tools
description: >-
  WebMCP — browser-side API that lets web applications expose their own functionality as MCP tools TO AI agents. Use
  when designing or integrating with web apps that surface UI actions (forms, buttons, data queries) as callable agent
  tools. NOT for web scraping or fetching external pages.
version: 1.2.0
model: sonnet
invoked_by: agent
user_invocable: false
tools:
  - Read
  - WebFetch
  - WebSearch
agents:
  - frontend-pro
  - developer
  - researcher
category: Web Development
tags:
  - webmcp
  - browser
  - mcp
  - w3c
  - ai-agents
  - web-development
  - chrome
verified: true
lastVerifiedAt: '2026-03-01T06:07:51.950Z'
---

# WebMCP Browser Tools

WebMCP is a browser API specification — published as a W3C Community Group Draft by contributors from Google and Microsoft (February 2026) — that enables **web applications to expose their own UI functionality as MCP tools to AI agents**.

**Direction of data flow: Web App → exposes tools → AI Agent calls them.**

This is the reverse of web scraping. The web app author decides what functions agents can call. The agent doesn't read the page — it calls structured tools the page registered.

## Critical Distinction

| Scenario                                                                                  | Correct Tool                             |
| ----------------------------------------------------------------------------------------- | ---------------------------------------- |
| Agent fetches content from an external website (BLS, Ongig, news sites)                   | `WebFetch` or `mcp__Exa__web_search_exa` |
| Web app exposes its own actions (add to cart, filter results, submit form) to an AI agent | **WebMCP**                               |
| Agent automates a browser (click, fill, navigate)                                         | `mcp__chrome-devtools__*` or Playwright  |

WebMCP is **not** a web scraper, crawler, or search engine. It is a tool registration protocol for web apps that want to be first-class AI-callable services.

## Status (as of 2026-02-22)

- **Spec**: W3C Community Group Draft — <https://github.com/webmachinelearning/webmcp>
- **Browser support**: Early preview in **Chrome 146 Canary** (shipped February 2026) behind the `Experimental Web Platform Features` flag. Stable rollout expected mid–late 2026.
- **Installable packages**: YES — the `@mcp-b/` ecosystem provides working npm packages today (polyfill + React integration)

### Available npm packages

| Package                    | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| `@mcp-b/react-webmcp`      | React hooks to expose components as MCP tools (v1.1.1) |
| `@mcp-b/webmcp-polyfill`   | Strict WebMCP core polyfill for any framework          |
| `@mcp-b/webmcp-types`      | TypeScript type definitions                            |
| `@mcp-b/transports`        | Browser transport layer (WebSocket/postMessage)        |
| `@mcp-b/webmcp-ts-sdk`     | Adapts the official MCP TypeScript SDK for browsers    |
| `@mcp-b/create-webmcp-app` | Scaffolding tool for new WebMCP apps                   |

Install:

```bash
npm install @mcp-b/react-webmcp
# or for raw usage:
npm install @mcp-b/transports @modelcontextprotocol/sdk zod
```

## How WebMCP Works

A web app registers tools with the browser. An AI agent (that has been granted access) can call those tools. The handler runs as client-side JavaScript with full access to the page's state.

```javascript
// Web app registers tools for AI agents to call
if ('modelContext' in window.navigator) {
  window.navigator.modelContext.provideContext({
    tools: [
      {
        name: 'filterProducts',
        description: 'Filter the product list by a natural language query',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Natural language filter' },
          },
          required: ['query'],
        },
        execute({ query }, agent) {
          // Runs in-browser, has access to current UI state
          const results = productService.filter(query);
          return { content: [{ type: 'text', text: JSON.stringify(results) }] };
        },
      },
    ],
  });
}
```

### React integration (via `@mcp-b/react-webmcp`)

```jsx
import { useTool } from '@mcp-b/react-webmcp';

function ProductList({ products }) {
  useTool({
    name: 'filterProducts',
    description: 'Filter products visible on screen',
    inputSchema: {
      /* ... */
    },
    execute({ query }) {
      return products.filter(p => p.name.includes(query));
    },
  });
  return (
    <ul>
      {products.map(p => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

## Key Differences from Standard MCP

| Aspect         | Standard MCP Server         | WebMCP                                                  |
| -------------- | --------------------------- | ------------------------------------------------------- |
| Location       | Separate server process     | Browser client-side JS                                  |
| Context access | Isolated from UI            | Shares live UI state, DOM, user session                 |
| Status         | Production-ready            | Chrome Canary preview (stable ~mid-2026)                |
| Installation   | npm server package          | `@mcp-b/` npm packages (polyfill) or native browser API |
| Setup          | Separate process, stdio/SSE | In-page script, browser transport                       |
| Auth           | Server-level                | Browser security model + page context                   |

## When to Use This Skill

Use `Skill({ skill: 'webmcp-browser-tools' })` when:

- **Designing a web app** that should expose UI actions to AI agents (e.g., a dashboard that agents can query, a form workflow agents can submit)
- **Integrating an existing web app** with Claude via browser-side tools rather than building a backend MCP server
- **Planning agent-to-web-app collaboration** where the agent and user share the same browser interface (human-in-the-loop workflows)
- **Evaluating whether to use WebMCP vs. backend MCP** for a new product feature

Do NOT use this skill when:

- You need to **fetch or scrape content from external sites** → use `WebFetch` or `mcp__Exa__web_search_exa`
- You need **browser automation** (click, fill, navigate) → use `mcp__chrome-devtools__*`
- The web app does **not** support WebMCP → build a standard backend MCP server instead

## Real-World Use Cases

- **E-commerce agent**: Product page registers `searchInventory`, `addToCart`, `applyPromoCode` — agent calls them without scraping
- **Analytics dashboard**: Dashboard registers `runQuery(metric, timeRange)` — agent can answer data questions without screen-reading
- **Browser IDE**: Code editor registers `insertSnippet`, `runTests`, `openFile` — agent assists without Playwright automation
- **Figma/design tool**: Registers `createComponent`, `applyTheme` — agent can directly modify designs

## agent-studio Integration Path

### Today (Chrome Canary + @mcp-b polyfill)

1. Install `@mcp-b/webmcp-polyfill` or `@mcp-b/react-webmcp` in the target web app
2. Register tools using `window.navigator.modelContext.provideContext()`
3. Claude Code (with the `mcp__chrome-devtools__*` tools available) can discover and call registered tools on the page

### When Chrome Stable Ships (~mid-2026)

1. No polyfill needed — native browser API available
2. Update this skill's examples to reflect the stable API surface
3. Consider creating a dedicated `webmcp-integration` workflow for onboarding web apps as agent-callable services

## Monitoring

Watch: <https://github.com/webmachinelearning/webmcp> for:

- Chrome intent-to-ship / origin trial announcements
- Firefox and Safari implementation signals
- Breaking changes in the `window.navigator.modelContext` API surface
- `@mcp-b/` package releases for updated polyfill patterns

## Anti-Patterns

- Do NOT use WebMCP to scrape or read content from sites you don't control — that's `WebFetch` / Exa
- Do NOT confuse with Anthropic's MCP (Model Context Protocol) — same underlying protocol, different surface: WebMCP is the browser-side extension of MCP
- Do NOT build production systems that require Chrome stable WebMCP until the API ships; use the `@mcp-b/webmcp-polyfill` for progressive enhancement today
- Do NOT register tools that require server-side data access — those belong in a backend MCP server, not a browser tool

## Assigned Agents

| Agent          | Role                                                                      |
| -------------- | ------------------------------------------------------------------------- |
| `frontend-pro` | Primary — designing and implementing WebMCP tool registration in web apps |
| `developer`    | Supporting — integration architecture, polyfill setup, TypeScript types   |
| `researcher`   | Supporting — tracking spec evolution, browser support status              |

## Iron Laws

1. **ALWAYS** gate WebMCP usage behind `if ('modelContext' in window.navigator)` feature detection
2. **NEVER** use WebMCP for external page fetching or web scraping — use WebFetch or Exa instead
3. **ALWAYS** define JSON Schema for tool inputs before writing the handler (schema-first design)
4. **NEVER** register WebMCP tools that replicate backend requests — exploit current page state instead
5. **ALWAYS** use the polyfill (`@mcp-b/webmcp-polyfill`) for development until Chrome stable ships the native API

## Anti-Patterns

| Anti-Pattern                            | Why It Fails                              | Correct Approach                                    |
| --------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| No feature detection guard              | Crashes in non-WebMCP browsers            | Always check `'modelContext' in window.navigator`   |
| Using WebMCP for external URL fetching  | Wrong direction of data flow              | Use `WebFetch` or Exa for external content          |
| Skipping JSON Schema for tool inputs    | Ambiguous contracts, runtime errors       | Define schema for all tool inputs before handler    |
| Registering backend-equivalent tools    | Duplicates MCP server, ignores page state | Tools should expose UI-specific actions and state   |
| Relying on native API in production now | Chrome stable ships ~mid-2026             | Use `@mcp-b/webmcp-polyfill` until native is stable |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New WebMCP pattern or API update → `.claude/context/memory/learnings.md`
- Browser support change (Chrome flag, origin trial) → `.claude/context/memory/learnings.md`
- Architecture decision for agent-browser integration → `.claude/context/memory/decisions.md`
- Breaking change in `@mcp-b/` packages → `.claude/context/memory/issues.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
