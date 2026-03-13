---
name: hcpcs-codes
description: HCPCS Level II code search, lookup, and cost data. Activates when tasks involve durable medical equipment codes, supply codes, or Level II procedure codes.
license: MIT
author: SequoiaPort
version: 0.1.0
---

# HCPCS Codes

Search, lookup, and get cost data for HCPCS Level II codes via the `@sequoiaport/codes` package.

## When to Apply

- User asks for an HCPCS code
- User needs codes for durable medical equipment (DME), supplies, or services
- User mentions Level II codes, J-codes, E-codes, or supply codes
- User needs cost data for HCPCS items

## Getting an API Key

First check if `SEQUOIA_CODES_API_KEY` is already set in the environment. If it is, skip key generation entirely and proceed to usage. Only if no key exists, see [AGENT_PROMPT.md](../../AGENT_PROMPT.md) for how your agent can obtain one via the agent auth flow.

## MCP Server

Once you have an API key, you can set up the MCP server for direct tool access from Claude Code, Cursor, or VS Code. See [MCP_SETUP.md](../../MCP_SETUP.md).

## How It Works

```typescript
import { SequoiaCodesClient } from "@sequoiaport/codes";

const client = new SequoiaCodesClient({
  apiKey: process.env.SEQUOIA_CODES_API_KEY!,
});
```

## Available Operations

### `client.hcpcs.searchCode({ query, limit? })`
Hybrid search for HCPCS codes.

```typescript
const results = await client.hcpcs.searchCode({
  query: "wheelchair motorized",
  limit: 10,
});
// results.results → [{ code, code_type: "HCPCS", short_description, similarity, ... }]
```

### `client.hcpcs.identifyCode({ code })`
Look up a specific HCPCS code.

```typescript
const result = await client.hcpcs.identifyCode({ code: "E1161" });
// result.result → { code: "E1161", short_description: "Manual wheelchair accessory...", ... }
```

### `client.hcpcs.getCost({ code })`
Get RVU and cost data for an HCPCS code.

```typescript
const cost = await client.hcpcs.getCost({ code: "E1161" });
// cost.cost → { code, rvu_work, rvu_pe, rvu_mp, rvu_total, conversion_factor, fee_schedule }
```

## REST API (curl)

```bash
# Search HCPCS codes
curl -X GET "https://api.sequoiacodes.com/v1/hcpcs/searchCode?query=wheelchair&limit=10" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"

# Lookup specific code
curl -X GET "https://api.sequoiacodes.com/v1/hcpcs/identifyCode?code=E1161" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"

# Get cost data
curl -X GET "https://api.sequoiacodes.com/v1/hcpcs/getCost?code=A0425" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"
```

## HCPCS Code Prefixes

- **A** - Transport, medical/surgical supplies
- **B** - Enteral and parenteral therapy
- **C** - Hospital outpatient payment
- **E** - Durable medical equipment
- **G** - Temporary procedures/services
- **J** - Drugs administered other than oral
- **K** - Temporary DME codes
- **L** - Orthotics and prosthetics
- **V** - Vision and hearing services
