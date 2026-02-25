---
name: raison-sdk
description: "Raison JavaScript/TypeScript prompt management SDK. Use when working with the `raison` npm package to render templates or query prompt data."
---

# Raison SDK

Raison is a prompt management platform. Prompts live in the dashboard at raison.ist with full version history and are delivered to applications via real-time WebSocket sync — no redeployments needed when prompts change.

**Key concepts:** Organization → Project → Agent → Prompt. Each project has Development/Staging/Production environments, each with its own `rsn_` API key.

## Installation

```bash
npm install raison
```

## Connect and Use

```typescript
import { Raison } from "raison";

const raison = new Raison({ apiKey: process.env.RAISON_API_KEY }); // rsn_...

// Render a prompt with variables (Handlebars template)
const message = await raison.render("PROMPT_ID", { userName: "Alice" });

// Query all prompts in this environment
const all = await raison.find();

// Find by agent + name (most efficient — uses composite index)
const systemPrompt = await raison.findOne({ agentId: "AGENT_ID", name: "system-prompt" });

// Shutdown
raison.disconnect();
```

All methods (`render`, `find`, `findOne`) await the initial WebSocket sync automatically — no race conditions, no manual readiness checks.

## Core Methods

| Method | Returns | Notes |
|---|---|---|
| `render(id, vars?)` | `Promise<string>` | Returns `""` if not found; raw content if no vars |
| `find(params?)` | `Promise<Prompt[]>` | Returns `[]` if no match |
| `findOne(params)` | `Promise<Prompt \| null>` | Returns `null` if no match |
| `disconnect()` | `void` | Call on process shutdown |
| `Raison.registerHelper(name, fn)` | `void` | Global Handlebars helper; register at startup |

## Finding IDs

- **Prompt ID** — Dashboard: open project → click agent → click prompt → copy ID at top
- **Agent ID** — Dashboard: open project → click agent → copy ID at top
- IDs are stable across environments (same ID works in Dev/Staging/Prod)

## Error Handling Pattern

```typescript
const prompt = await raison.render("PROMPT_ID", variables);
if (!prompt) {
  return FALLBACK_SYSTEM_PROMPT; // render() returns "" for missing prompts
}
```

## References

- **[sdk-reference.md](references/sdk-reference.md)** — Full API reference: constructor options, method signatures, types, and error behavior table. Read when you need precise signatures, TypeScript types, or to check all error cases.

- **[templating.md](references/templating.md)** — Handlebars guide: variables, nested objects, `{{#if}}`, `{{#each}}`, custom helpers with code examples. Read when writing or debugging prompt templates.

- **[examples.md](references/examples.md)** — Integration patterns: Anthropic/Claude, OpenAI, Express.js, Next.js serverless singleton, multiple environments, graceful shutdown. Read when integrating Raison into a specific framework or setting up a production pattern.
