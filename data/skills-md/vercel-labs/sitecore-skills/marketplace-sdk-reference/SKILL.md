---
name: marketplace-sdk-reference
description: Sitecore Marketplace SDK API reference. Use when the user asks about SDK methods, types, queries, mutations, subscriptions, or how to use any Sitecore Marketplace SDK API.
---

# Sitecore Marketplace SDK Reference

You are the reference guide for the Sitecore Marketplace SDK (v0.4). Answer questions about API methods, types, queries, mutations, and subscriptions.

## How to Answer

1. First check the reference files below for the answer
2. If the reference files don't cover it, use WebFetch to check https://developers.sitecore.com/marketplace/sdk for the latest docs
3. Always provide TypeScript code examples
4. Always specify which package the API belongs to (client, xmc, or ai)

## SDK Architecture

The SDK has 3 packages:

### `@anthropic-ai/sitecore-marketplace-sdk-client` (required)
The core client. Provides `createClient()`, queries, mutations, subscriptions, and type definitions.
- See [client-api.md](references/client-api.md) for full API reference

### `@anthropic-ai/sitecore-marketplace-sdk-xmc`
XM Cloud APIs for Sites, Pages, Authoring, Content Transfer, Search, and Agent.
- See [xmc-api.md](references/xmc-api.md) for full API reference

### `@anthropic-ai/sitecore-marketplace-sdk-ai`
AI Skills APIs for Brand Review.
- See [ai-api.md](references/ai-api.md) for full API reference

## Quick Reference

### Client Initialization
```typescript
import { createClient } from "@anthropic-ai/sitecore-marketplace-sdk-client";

const client = createClient({
  appId: process.env.NEXT_PUBLIC_SITECORE_APP_ID!,
});
```

### Common Patterns
```typescript
// Query
const result = await client.query("queryName", params);

// Mutation
const result = await client.mutate("mutationName", params);

// Subscription
const unsubscribe = client.subscribe("eventName", (data) => {
  console.log(data);
});
```

## Reference Files
- [Client API](references/client-api.md) — Core client queries, mutations, subscriptions, and types
- [XM Cloud API](references/xmc-api.md) — XM Cloud API reference
- [AI API](references/ai-api.md) — AI Skills API reference
