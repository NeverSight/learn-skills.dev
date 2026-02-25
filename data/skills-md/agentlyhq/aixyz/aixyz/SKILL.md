---
name: aixyz
description: >-
  Build, run, and deploy an AI agent using the aixyz framework.
  Use this skill when creating a new agent, adding tools, wiring up A2A/MCP protocols,
  configuring x402 micropayments, or deploying to Vercel.
license: MIT
metadata:
  version: 1.0.0
  framework: aixyz
  runtime: bun
---

# Build an Agent with aixyz

## When to Use

Use this skill when:

- Scaffolding a new AI agent project from scratch
- Adding a new tool to an existing agent
- Configuring x402 micropayments for an agent or tool
- Wiring up A2A and MCP protocol endpoints
- Deploying an agent to Vercel

## Instructions

### 1. Scaffold a new project

```bash
bunx create-aixyz-app my-agent
cd my-agent
```

This creates the standard project layout:

```
my-agent/
  aixyz.config.ts     # Agent metadata and skills
  app/
    agent.ts          # Agent definition
    tools/            # One file per tool
    icon.png          # Agent icon (optional)
  package.json
  vercel.json
```

### 2. Configure the agent (`aixyz.config.ts`)

Every agent needs a config file at the project root. Declare identity, payment address, and skills:

```ts
import type { AixyzConfig } from "aixyz/config";

const config: AixyzConfig = {
  name: "My Agent",
  description: "A short description of what this agent does.",
  version: "0.1.0",
  x402: {
    payTo: process.env.X402_PAY_TO!,
    network: process.env.NODE_ENV === "production" ? "eip155:8453" : "eip155:84532",
  },
  skills: [
    {
      id: "my-skill",
      name: "My Skill",
      description: "What this skill does for callers.",
      tags: ["example"],
      examples: ["Do something with my skill"],
    },
  ],
};

export default config;
```

### 3. Payment: `accepts` export (`aixyz/accepts`)

Every agent and tool controls whether it requires payment by exporting `accepts` from `aixyz/accepts`.
Without this export, the endpoint is not registered for payment gating.

```ts
import type { Accepts } from "aixyz/accepts";

// Require x402 micropayment
export const accepts: Accepts = {
  scheme: "exact",
  price: "$0.001", // USD-denominated
  network: "eip155:8453", // optional — defaults to config.x402.network
  payTo: "0x...", // optional — defaults to config.x402.payTo
};

// Or make the endpoint free
export const accepts: Accepts = {
  scheme: "free",
};
```

Export `accepts` from `app/agent.ts` to gate the A2A endpoint, or from a tool file to gate that tool via MCP.

### 4. Write a tool (`app/tools/<name>.ts`)

Each file in `app/tools/` exports a Vercel AI SDK `tool` as its default export:

```ts
import { tool } from "ai";
import { z } from "zod";
import type { Accepts } from "aixyz/accepts";

export const accepts: Accepts = { scheme: "exact", price: "$0.001" };

export default tool({
  description: "A short description of what this tool does.",
  inputSchema: z.object({
    query: z.string().describe("Input to the tool"),
  }),
  execute: async ({ query }) => {
    // your logic here
    return { result: query };
  },
});
```

Files prefixed with `_` (e.g. `_helpers.ts`) are ignored by the auto-generated server.

### 5. Define the agent (`app/agent.ts`)

```ts
import { openai } from "@ai-sdk/openai";
import { stepCountIs, ToolLoopAgent } from "ai";
import type { Accepts } from "aixyz/accepts";
import myTool from "./tools/my-tool";

export const accepts: Accepts = { scheme: "exact", price: "$0.005" };

export default new ToolLoopAgent({
  model: openai("gpt-4o-mini"),
  instructions: "You are a helpful assistant.",
  tools: { myTool },
  stopWhen: stepCountIs(10),
});
```

### 6. Environment variables (`.env` files)

Environment variables are loaded in the same priority order as Next.js:

1. `.env.<NODE_ENV>.local` (highest priority; not loaded when `NODE_ENV=test`)
2. `.env.local`
3. `.env.<NODE_ENV>` (e.g. `.env.production`, `.env.development`)
4. `.env`

Common variables:

| Variable               | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `X402_PAY_TO`          | Default EVM address to receive payments                                 |
| `X402_NETWORK`         | Default payment network (e.g. `eip155:8453`)                            |
| `X402_FACILITATOR_URL` | Custom facilitator URL (default: `https://x402.agently.to/facilitator`) |
| `OPENAI_API_KEY`       | OpenAI API key                                                          |

### 7. Agent icon (`app/icon.png`)

Place an icon file at `app/icon.png` (also accepts `.svg`, `.jpeg`, `.jpg`). During `aixyz build` it is:

- Copied to the output as `icon.png`
- Converted to a `favicon.ico` (32×32) and placed in `public/`

No configuration needed — the build step auto-detects and processes the icon.

### 8. Custom facilitator (`app/accepts.ts`)

By default, aixyz uses `https://x402.agently.to/facilitator` to verify payments. To use a different
facilitator, create `app/accepts.ts` and export a `facilitator`:

```ts
import { HTTPFacilitatorClient } from "aixyz/accepts";

export const facilitator = new HTTPFacilitatorClient({
  url: process.env.X402_FACILITATOR_URL ?? "https://www.x402.org/facilitator",
});
```

### 9. Run the dev server

```bash
bun run dev      # aixyz dev — starts at http://localhost:3000 with hot reload
bun run dev -- -p 4000  # custom port
```

Endpoints served automatically:

| Endpoint                       | Protocol | Description                   |
| ------------------------------ | -------- | ----------------------------- |
| `/.well-known/agent-card.json` | A2A      | Agent discovery               |
| `/agent`                       | A2A      | JSON-RPC, x402 payment gate   |
| `/mcp`                         | MCP      | Tool sharing with MCP clients |

### 10. (Optional) Custom server (`app/server.ts`)

For full control, create `app/server.ts`. It takes precedence over auto-generation.
The `accepts` field in `mcp.register` is optional — omit it to expose the tool without payment gating:

```ts
import { AixyzServer } from "aixyz/server";
import { useA2A } from "aixyz/server/adapters/a2a";
import { AixyzMCP } from "aixyz/server/adapters/mcp";
import * as agent from "./agent";
import myTool from "./tools/my-tool";

const server = new AixyzServer();
await server.initialize();
server.unstable_withIndexPage();

useA2A(server, agent);

const mcp = new AixyzMCP(server);
await mcp.register("myTool", {
  default: myTool,
  // accepts is optional — omit to expose without payment
  accepts: { scheme: "exact", price: "$0.001" },
});
await mcp.connect();

export default server;
```

### 11. Build and deploy to Vercel

```bash
bun run build    # aixyz build — outputs Vercel Build Output API v3 to .vercel/output/
vercel deploy
```

## Examples

Working examples in the repo: `examples/agent-boilerplate`, `examples/agent-price-oracle`, `examples/agent-byo-facilitator`.

## Common Edge Cases

- **Missing `x402.network`** — always provide `x402.network`; it has no fallback.
- **Missing `x402.payTo`** — set `X402_PAY_TO` in `.env.local` or provide it directly in config.
- **Tool file ignored** — files prefixed with `_` are excluded; rename to remove the prefix.
- **Agent card missing skills** — `skills` defaults to `[]`; add at least one entry to be discoverable.
- **Free endpoint** — export `accepts: { scheme: "free" }` to expose an endpoint without payment.
- **Port conflict in dev** — use `aixyz dev -p <port>` to change the default port (3000).
