---
name: e2b-sandbox
description: Guide for creating and managing E2B sandboxes using ComputeSDK. Use when building applications that need E2B Firecracker microVM sandboxes for secure code execution, AI code runners, or isolated development environments on E2B.
---

# E2B Sandboxes with ComputeSDK

Run code in E2B's Firecracker microVMs through ComputeSDK's unified API. E2B provides sub-second cold starts and secure isolation — ideal for AI code execution, data science, and educational platforms.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
E2B_API_KEY=your_e2b_api_key
```

Get your ComputeSDK key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects E2B from environment variables

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello from E2B!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'e2b',
  e2b: {
    apiKey: process.env.E2B_API_KEY,
  }
});

const sandbox = await compute.sandbox.create();
```

## E2B Configuration Options

```typescript
interface E2BConfig {
  apiKey?: string;              // Uses E2B_API_KEY env var if not set
  runtime?: 'node' | 'python'; // Auto-detects from code patterns
  timeout?: number;             // Execution timeout in ms
}
```

## Runtime Detection

E2B auto-detects Python from `print` statements, `import`, `def`, and Python-specific syntax like `f"strings"`. All other code defaults to Node.js.

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/