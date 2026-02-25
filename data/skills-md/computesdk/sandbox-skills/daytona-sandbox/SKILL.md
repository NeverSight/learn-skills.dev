---
name: daytona-sandbox
description: Guide for creating and managing Daytona sandboxes using ComputeSDK. Use when building applications that need Daytona development workspace environments for code execution, full-featured dev environments, or isolated coding workspaces.
---

# Daytona Sandboxes with ComputeSDK

Run code in Daytona's development workspace environments through ComputeSDK's unified API. Daytona provides full-featured development workspaces — ideal for complex application development, multi-service environments, and persistent coding workspaces.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
DAYTONA_API_KEY=your_daytona_api_key
```

Get your ComputeSDK key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects Daytona from environment variables

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello from Daytona!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'daytona',
  daytona: {
    apiKey: process.env.DAYTONA_API_KEY,
  }
});

const sandbox = await compute.sandbox.create();
```

## Daytona Configuration Options

```typescript
interface DaytonaConfig {
  apiKey?: string;              // Uses DAYTONA_API_KEY env var if not set
  runtime?: 'node' | 'python'; // Auto-detects from code patterns
  timeout?: number;             // Execution timeout in ms
}
```

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/