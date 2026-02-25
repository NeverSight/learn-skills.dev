---
name: context7-mcp
description: "Query up-to-date library and framework documentation via the Context7 MCP server."
metadata:
  version: 1.0.0
  mcp-server: context7
---

# Context7 Library Documentation

You are an expert at using the Context7 MCP server to retrieve current, accurate library documentation. Context7 provides up-to-date docs for thousands of libraries and frameworks, eliminating outdated training data issues.

## Critical: These Are Direct Tool Calls

MCP tools are **direct tool calls** — exactly like `Read`, `Grep`, or `Bash`. They are NOT CLI commands.

**CORRECT** — call the tool directly:
```
Tool: mcp__context7__resolve-library-id
Parameters: { "libraryName": "next.js" }
```

**WRONG** — do NOT shell out:
```
Bash: claude mcp call context7 resolve-library-id ...  # This does not work
```

All Context7 MCP tools use the `mcp__context7__` prefix.

## Critical: Always Resolve Library ID First

You **must** call `resolve-library-id` before `query-docs` unless you already have a confirmed `/org/project` ID from a previous call in this session.

## Critical: Output Size Awareness

| Tool | Output Size | Notes |
|------|------------|-------|
| `resolve-library-id` | Small | Returns list of matching library IDs |
| `query-docs` | Medium-Large | Documentation content — scales with topic breadth. Use specific queries to limit size. |

## Workflow: Find & Query Documentation

**Trigger:** User asks about library APIs, framework patterns, configuration options, or "how to do X with Y library"

### Steps

1. **Resolve the library ID:**
   ```
   resolve-library-id({ libraryName: "next.js" })
   → returns matching libraries with /org/project IDs
   ```

2. **Query documentation with a specific question:**
   ```
   query-docs({ libraryId: "/vercel/next.js", query: "how to use middleware for authentication" })
   → returns relevant documentation sections
   ```

3. **Refine if needed** (max 3 calls per tool per question):
   ```
   query-docs({ libraryId: "/vercel/next.js", query: "middleware matcher config" })
   → more specific follow-up
   ```

### Key Patterns

- **Be specific in queries:** "How to set up authentication with JWT in Express.js" beats "auth"
- **Max 3 calls per tool per question** — if 3 queries don't answer it, use a different approach
- **One library per query** — don't try to query multiple libraries in a single `query-docs` call
- **Use the full `/org/project` format** for `libraryId` (e.g., `/vercel/next.js`, `/supabase/supabase`)

### Decision Tree

| User Needs | Action |
|------------|--------|
| Docs for a known library | `resolve-library-id` → `query-docs` |
| Not sure which library to use | `resolve-library-id` with general term, review matches |
| Already have library ID from this session | Skip resolve, go straight to `query-docs` |
| Library not found in Context7 | Fall back to `tavily-mcp` search or `WebFetch` for official docs site |

## Common Library IDs

These are frequently used in this project — skip `resolve-library-id` for these:

| Library | ID |
|---------|-----|
| Next.js | `/vercel/next.js` |
| React | `/facebook/react` |
| Supabase JS | `/supabase/supabase-js` |
| TanStack Query | `/tanstack/query` |
| Zod | `/colinhacks/zod` |
| React Hook Form | `/react-hook-form/react-hook-form` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |
| date-fns | `/date-fns/date-fns` |
| Radix UI | `/radix-ui/primitives` |
| Playwright | `/microsoft/playwright` |
| Vitest | `/vitest-dev/vitest` |

**Note:** If a common ID stops working, re-resolve it — library IDs can change when repos are reorganized.

## Troubleshooting

### "Library not found"

1. Try alternate names: "react-query" vs "tanstack query" vs "@tanstack/react-query"
2. Try the npm package name: "next" vs "next.js"
3. Try the GitHub org/repo format directly: "vercel/next.js"
4. Fall back to `tavily-mcp` search for the official docs URL, then use `WebFetch`

### Query Returns Irrelevant Results

1. Make your query more specific — include the exact API name or concept
2. Try rephrasing: "server actions" vs "use server directive" vs "form actions"
3. Add version context: "Next.js 15 app router middleware" vs just "middleware"

### Query Returns Too Much Content

1. Narrow the query to a specific function or concept
2. Ask about one feature at a time rather than broad overviews
3. If output is still large, extract the relevant section and summarize for the user
