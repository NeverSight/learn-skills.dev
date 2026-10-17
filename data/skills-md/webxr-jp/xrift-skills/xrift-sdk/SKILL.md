---
name: xrift-sdk
description: Guide for using the @xrift/sdk package to programmatically upload worlds and items to the XRift platform. Covers XriftClient initialization, WorldsApi, ItemsApi, file upload flows, error handling, and Node.js vs browser usage.
---

# XRift SDK Guide

A guide for using `@xrift/sdk` to programmatically interact with the XRift platform API.

## References

- [API Reference](references/api-reference.md) - Full specification of XriftClient, WorldsApi, ItemsApi, error classes, and utility functions
- [Code Templates](references/code-templates.md) - Ready-to-use code examples for Node.js and browser environments
- [Type Definitions](references/type-definitions.md) - Complete TypeScript type definitions for all SDK interfaces

## Critical Rules

1. **API token is always required** — `XriftClient` must be initialized with a valid `token`. Never hardcode tokens; use environment variables or secure configuration.
2. **File data must be `FileData` type** — The SDK accepts `ArrayBuffer | Uint8Array`, not file paths or strings. The caller is responsible for reading files into binary data before passing to the SDK.
3. **`remotePath` must be a relative path** — Never use absolute paths or paths starting with `/`. Use paths like `scene.glb` or `assets/texture.png`.
4. **Always handle errors** — Wrap API calls in try/catch and handle `XriftAuthError`, `XriftApiError`, and `XriftNetworkError` separately.

## Project Overview

### What is @xrift/sdk?

`@xrift/sdk` is a universal TypeScript SDK for the XRift platform. It provides programmatic access to world and item APIs with integrated file upload capabilities.

### Key Characteristics

- **Universal**: Works in both Node.js (>=18) and browser environments
- **Zero dependencies**: Built on native `fetch` API
- **TypeScript first**: Full type definitions included
- **Dual build**: ESM + CJS support
- **Integrated upload**: Hash calculation → signed URL retrieval → upload → completion in one call

### Tech Stack

- TypeScript (strict mode)
- fetch API (no axios)
- SHA-256 hashing (node:crypto / Web Crypto API)
- ESM + CJS dual build

## Installation

```bash
npm install @xrift/sdk
```

## Quick Start

```typescript
import { XriftClient, getMimeType } from '@xrift/sdk';

const client = new XriftClient({
  token: process.env.XRIFT_TOKEN!,
});

// Upload a world
const result = await client.worlds.upload(
  [
    {
      remotePath: 'scene.glb',
      data: fileData, // Uint8Array or ArrayBuffer
      size: fileData.byteLength,
      contentType: getMimeType('scene.glb'),
    },
  ],
  {
    name: 'My World',
  },
);

console.log(`Uploaded: ${result.worldId} v${result.versionNumber}`);
```

## Upload Flow

The `upload()` method (on both `WorldsApi` and `ItemsApi`) executes these steps internally:

1. **Determine ID** — Use provided `worldId`/`itemId` or create a new resource via `create()`
2. **Calculate content hash** — SHA-256 hash of all file data + config values (first 12 hex chars)
3. **Calculate total file size** — Sum of all `file.size` values
4. **Get signed upload URLs** — POST to `/upload-urls` endpoint with metadata and file list
5. **Upload files** — PUT each file to its signed URL with correct Content-Type header
6. **Complete upload** — POST to `/complete` endpoint with the version ID

All these steps are handled internally by `upload()` and cannot be called individually.

## Error Handling

```typescript
import { XriftAuthError, XriftApiError, XriftNetworkError } from '@xrift/sdk';

try {
  await client.worlds.upload(files, options);
} catch (error) {
  if (error instanceof XriftAuthError) {
    // 401 - Invalid or expired token
  } else if (error instanceof XriftApiError) {
    // Other API errors (400, 403, 404, 500, etc.)
    console.error(`Status: ${error.statusCode}, Body:`, error.responseBody);
  } else if (error instanceof XriftNetworkError) {
    // Network connectivity issues
    console.error('Cause:', error.cause);
  }
}
```

### Error Hierarchy

```
XriftSdkError (base)
├── XriftApiError (HTTP errors with statusCode and responseBody)
│   └── XriftAuthError (HTTP 401)
└── XriftNetworkError (connectivity errors with cause)
```

## Node.js vs Browser

| Aspect | Node.js | Browser |
|--------|---------|---------|
| File reading | `fs.readFile()` → `Uint8Array` | `File.arrayBuffer()` → `Uint8Array` |
| Hash algorithm | `node:crypto` (createHash) | `crypto.subtle.digest` (Web Crypto API) |
| Token storage | Environment variables | Secure storage (not localStorage) |
| Minimum version | Node.js 18+ | Modern browsers with fetch + Web Crypto |

## Related Resources

- [npm: @xrift/sdk](https://www.npmjs.com/package/@xrift/sdk)
- [GitHub: WebXR-JP/xrift-sdk](https://github.com/WebXR-JP/xrift-sdk)
- [XRift Documentation](https://xrift-docs.vercel.app/sdk/overview)
