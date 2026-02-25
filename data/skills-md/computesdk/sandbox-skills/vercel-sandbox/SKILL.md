---
name: vercel-sandbox
description: Guide for creating and managing Vercel sandboxes using ComputeSDK. Use when building applications that need Vercel's globally distributed serverless sandbox environments for code execution with Node.js or Python runtimes.
---

# Vercel Sandboxes with ComputeSDK

Run code in Vercel's globally distributed serverless environments through ComputeSDK's unified API. Vercel provides fast edge execution with Node.js and Python runtimes — ideal for serverless functions and globally distributed code execution.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
VERCEL_TOKEN=your_vercel_token
VERCEL_TEAM_ID=your_vercel_team_id
VERCEL_PROJECT_ID=your_vercel_project_id
```

Get your ComputeSDK key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects Vercel from environment variables

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello from Vercel!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'vercel',
  vercel: {
    token: process.env.VERCEL_TOKEN,
    teamId: process.env.VERCEL_TEAM_ID,
    projectId: process.env.VERCEL_PROJECT_ID,
  }
});

const sandbox = await compute.sandbox.create();
```

## Vercel Configuration Options

```typescript
interface VercelConfig {
  token?: string;               // Uses VERCEL_TOKEN env var if not set
  teamId?: string;              // Uses VERCEL_TEAM_ID env var if not set
  projectId?: string;           // Uses VERCEL_PROJECT_ID env var if not set
  runtime?: 'node' | 'python';  // Auto-detects from code patterns
  timeout?: number;              // Execution timeout in ms
}
```

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/