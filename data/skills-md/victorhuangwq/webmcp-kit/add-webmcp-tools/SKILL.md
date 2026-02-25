---
name: add-webmcp-tools
description: Add, edit, debug, and test WebMCP tools built with webmcp-kit. Use when users ask to create or modify defineTool-based tools, fix missing tools, resolve schema/execution errors, or validate tools in dev panel/native mode.
---

# Add WebMCP Tools with webmcp-kit

## When to Use This Skill

Use this skill when the request is about WebMCP tools in a website codebase:
- Add a new tool using `defineTool(...)`
- Edit existing tool behavior, schema, or annotations
- Debug tools that do not appear or fail at runtime
- Test tools with webmcp-kit dev panel or direct execution

Do not use this skill for unrelated frontend/backend feature work that does not involve WebMCP tool definitions.

## Preflight

Run these checks before changing code:

1. Confirm dependencies and framework
- Check `package.json` for `webmcp-kit` and `zod`
- If missing, install with `npm install webmcp-kit zod`

2. Find likely tool files
- Search for existing tools and registration:
  - `rg -n "defineTool\(|\.register\(" src`
  - `rg -n "enableDevMode\(" src`
- Prioritize common locations:
  - `src/mcp-tools.ts`
  - `src/lib/mcp-tools.ts`
  - `src/mcp/*.ts`

3. Locate app entrypoint
- Identify where browser app bootstraps and where tool `.register()` calls belong
- Ensure `enableDevMode()` is enabled for local debugging when requested

## Playbooks

### 1) Add New Tool

Entry condition: No existing tool satisfies the requested capability.

Steps:
1. Create or update the tool module.
2. Define tool with specific camelCase name and clear description.
3. Add strict `inputSchema` with `.describe()` for every field and `.default()` for optional defaults.
4. Implement `execute` and return either string or response helper (`textContent`, `jsonContent`, `errorContent`).
5. Register the tool in the app flow with `.register()`.
6. Verify with dev panel and direct execution.

Reference template:

```typescript
import { defineTool, jsonContent } from 'webmcp-kit';
import { z } from 'zod';

export const searchProducts = defineTool({
  name: 'searchProducts',
  description: 'Search products by query',
  inputSchema: z.object({
    query: z.string().describe('Search text entered by user'),
    limit: z.number().min(1).max(50).default(10).describe('Maximum results'),
  }),
  execute: async ({ query, limit }) => {
    const results = await db.products.search(query, limit);
    return jsonContent(results);
  },
});

searchProducts.register();
```

Completion checks:
- Tool appears in dev panel list
- Valid inputs execute successfully
- Invalid inputs return schema validation errors

### 2) Edit Existing Tool

Entry condition: Tool exists and user requests schema/behavior changes.

Steps:
1. Update only the target tool definition (`description`, `inputSchema`, `execute`, `annotations`).
2. Keep input changes backward-compatible unless user explicitly requests breaking changes.
3. Re-run dev panel execution with old and new input shapes when relevant.
4. Confirm `.register()` path still executes at app startup.

Common edits:
- Schema constraints (`.min()`, `.max()`, `.regex()`, `z.enum(...)`)
- Output formatting (`jsonContent` vs string)
- Optional params (`.optional()` / `.default()`)
- Confirmation hints for sensitive actions

Completion checks:
- Existing intended flow still works
- Updated behavior matches user request

### 3) Debug Missing or Broken Tool

Entry condition: Tool does not show up or throws errors.

Steps:
1. If tool is missing in panel:
- Verify `.register()` executes
- Verify `enableDevMode()` runs in browser entry
- Check browser console for `[webmcp-kit]` diagnostics

2. If validation fails:
- Match failing field to `inputSchema`
- Add/adjust bounds, optionals, defaults, descriptions

3. If execution fails:
- Isolate failing logic in `execute`
- Add guarded error handling and clearer error messages

4. Confirm environment mode:
- Native mode: real `navigator.modelContext` available
- Mock mode: fallback message is expected and dev panel still works

Expected fallback log (normal in unsupported browsers):

```
[webmcp-kit] Using mock modelContext for tool "toolName". Native WebMCP not available.
```

Completion checks:
- Root cause identified and fixed
- Tool now appears/executes in expected mode

### 4) Test Tool (Dev Panel + Direct Execution)

Entry condition: New or changed tool needs verification.

Steps:
1. Dev panel test:
- Enable `enableDevMode()`
- Open panel, select tool, run with valid and invalid payloads

2. Direct execution test:

```typescript
const result = await searchProducts.execute({ query: 'pizza', limit: 5 });
```

3. Schema inspection when needed:

```typescript
console.log(searchProducts.inputSchema); // JSON Schema
console.log(searchProducts.schema);      // original Zod schema
```

Completion checks:
- Dev panel path works
- Direct invocation works
- Validation errors are understandable

## Destructive or Sensitive Actions

For delete/checkout/payment/account changes:
1. Add `annotations: { destructiveHint: true }` (or `confirmationHint: true`)
2. Request user confirmation in `execute` before mutation
3. Return cancellation result when confirmation is denied

Pattern:

```typescript
const deleteItem = defineTool({
  // ...
  annotations: { destructiveHint: true },
  execute: async (input, agent) => {
    const { confirmed } = await agent.requestUserInteraction({
      prompt: 'Are you sure?',
      type: 'confirmation',
    });
    if (!confirmed) return 'Cancelled';
    // perform mutation
  },
});
```

## Validation Checklist

- Tool name is specific, camelCase, and action-oriented
- `description` explains when an agent should call the tool
- Every schema field has `.describe(...)`
- Optional inputs use `.optional()` or `.default(...)`
- Tool is registered with `.register()` in startup path
- `enableDevMode()` is enabled when local testing is requested
- Native vs mock behavior is explicitly validated
- Sensitive actions require confirmation flow

## Expected Output

When using this skill, report results in this structure:

1. Summary
- What was added/edited/debugged

2. Files changed
- Exact paths touched
- What changed in each file

3. Verification
- Commands/tests/manual checks run
- Native or mock mode used

4. Remaining risks
- Open issues, follow-up tests, or assumptions
