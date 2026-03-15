---
name: context7
description: Fetch up-to-date documentation and code examples for any library or framework. Use when needing API references, code examples, library documentation, or framework guides. Supports React, Next.js, MongoDB, Supabase, and thousands of other libraries.
---

# Context7

Base directory for this skill: C:\Users\lyf1143312445\.agents\skills\context7

Retrieve up-to-date documentation and code examples for any library via the Context7 MCP service.

## Quick Start

Run the CLI script with bun from this skill directory:

```bash
bun ./scripts/context7.ts <command> [options]
```

## Available Commands

### resolve-library-id

Resolve a package/product name to a Context7-compatible library ID.

```bash
bun ./scripts/context7.ts resolve-library-id --library-name "react"
bun ./scripts/context7.ts resolve-library-id --library-name "next.js"
```

**Required before `get-library-docs`** unless user provides library ID in format `/org/project`.

### get-library-docs

Fetch documentation for a library.

```bash
# Basic usage
bun ./scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/vercel/next.js"

# With topic focus
bun ./scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/vercel/next.js" --topic "routing"

# Different modes: code (API refs) or info (conceptual guides)
bun ./scripts/context7.ts get-library-docs \
  --context7-compatible-library-i-d "/mongodb/docs" --mode "info"
```

**Parameters:**
- `--context7-compatible-library-i-d`: Library ID (e.g., `/mongodb/docs`, `/vercel/next.js`)
- `--mode`: `code` (default) for API/examples, `info` for conceptual guides
- `--topic`: Focus on specific topic (e.g., `hooks`, `routing`, `authentication`)
- `--page`: Pagination (1-10), use higher pages if context insufficient

## Global Options

- `-t, --timeout <ms>`: Call timeout (default: 30000)
- `-o, --output <format>`: Output format: `text` | `markdown` | `json` | `raw`

## Common Library IDs

| Library | ID |
|---------|-----|
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| MongoDB | `/mongodb/docs` |
| Supabase | `/supabase/supabase` |
| Prisma | `/prisma/prisma` |

## Requirements

- [Bun](https://bun.sh) runtime
- `mcporter` package (embedded in script)
