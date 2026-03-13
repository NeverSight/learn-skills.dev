---
name: cpt-codes
description: CPT procedure code search, lookup, cost/RVU data, and ICD-10 linking. Activates when tasks involve procedure codes, surgical codes, RVU values, Medicare fee schedules, or medical billing.
license: MIT
author: SequoiaPort
version: 0.1.0
---

# CPT Codes

Search, lookup, and get cost data for CPT procedure codes via the `@sequoiaport/codes` package.

## When to Apply

- User asks for a CPT code or procedure code
- User needs RVU values or cost data for a procedure
- User wants to find ICD-10 linking terms for a CPT code
- User mentions medical billing, fee schedules, or procedure coding

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

### `client.cpt.searchCode({ query, limit? })`
Hybrid search for CPT codes by procedure description.

```typescript
const results = await client.cpt.searchCode({
  query: "knee replacement surgery",
  limit: 10,
});
// results.results → [{ code, short_description, long_description, category, specialty, similarity, ... }]
```

### `client.cpt.identifyCode({ code })`
Look up a specific CPT code.

```typescript
const result = await client.cpt.identifyCode({ code: "27447" });
// result.result → { code: "27447", short_description: "Total knee arthroplasty", ... }
```

### `client.cpt.getCost({ code })`
Get RVU and cost data for a CPT code.

```typescript
const cost = await client.cpt.getCost({ code: "99213" });
// cost.cost → { code, rvu_work, rvu_pe, rvu_mp, rvu_total, conversion_factor, fee_schedule }
```

### `client.cpt.linkIcd10({ code })`
Get ICD-10 linking/search terms for a CPT code.

```typescript
const linking = await client.cpt.linkIcd10({ code: "45378" });
// linking → { code, code_type, short_description, indications, search_terms }
```

## REST API (curl)

```bash
# Search CPT codes
curl -X GET "https://api.sequoiacodes.com/v1/cpt/searchCode?query=knee%20arthroscopy&limit=10" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"

# Lookup specific code
curl -X GET "https://api.sequoiacodes.com/v1/cpt/identifyCode?code=99213" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"

# Get RVU/cost data
curl -X GET "https://api.sequoiacodes.com/v1/cpt/getCost?code=99213" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"

# Get ICD-10 linking terms
curl -X GET "https://api.sequoiacodes.com/v1/cpt/linkIcd10?code=29881" \
  -H "Authorization: Bearer $SEQUOIA_CODES_API_KEY"
```

## Response Fields

Each CPT code result includes:
- `code` - The CPT code (e.g., "99213")
- `code_type` - "CPT" or "HCPCS"
- `short_description` / `long_description` - Descriptions
- `indications` - Clinical indications
- `category` / `specialty` - Classification
- `similarity` - Search relevance score (0-1)
- `rvu_work` / `rvu_pe` / `rvu_mp` - RVU components (when available)
