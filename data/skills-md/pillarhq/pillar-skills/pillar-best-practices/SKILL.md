---
name: pillar-best-practices
description: Best practices for integrating the Pillar SDK into React and Next.js applications. Use when adding an AI assistant panel, help center widget, or embedded product assistant.
---

# Pillar SDK Best Practices

Best practices for integrating the Pillar SDK into React and Next.js applications. Use when adding an AI assistant panel, help center widget, or embedded product assistant.

## When to Apply

Reference these guidelines when:

- Adding Pillar SDK to a React or Next.js project
- Setting up `PillarProvider` in your app
- Defining tools for the AI assistant to discover and call
- Creating tool handlers to execute user requests
- Designing multi-tool workflows for agentic operations

## Essential Rules

| Priority | Rule | Description |
|----------|------|-------------|
| CRITICAL | `setup-provider` | Always wrap your app with PillarProvider |
| CRITICAL | `setup-nextjs` | Next.js App Router requires a 'use client' wrapper |
| CRITICAL | `schema-compatibility` | inputSchema must follow cross-model formatting rules (arrays need items, no type unions) |
| HIGH | `tool-descriptions` | Write specific, AI-matchable descriptions and keep tools focused |
| HIGH | `tool-handlers` | Use centralized handlers with proper cleanup |
| HIGH | `guidance-field` | Use the guidance field for agent-facing disambiguation and prerequisites |
| HIGH | `workflow-patterns` | Design multi-tool workflows using the distributed guidance pattern |
| HIGH | `tool-overlap-audit` | Audit existing tools for overlap before creating new ones |
| HIGH | `codebase-verification` | Verify API shapes against the actual codebase -- never guess |

## Quick Reference

### 1. Provider Setup (CRITICAL)

Always wrap your app with `PillarProvider`:

```tsx
import { PillarProvider } from '@pillar-ai/react';

<PillarProvider productKey="your-product-key">
  {children}
</PillarProvider>
```

### 2. Next.js App Router (CRITICAL)

Create a client wrapper component:

```tsx
// providers/PillarSDKProvider.tsx
'use client';

import { PillarProvider } from '@pillar-ai/react';

export function PillarSDKProvider({ children }: { children: React.ReactNode }) {
  return (
    <PillarProvider productKey={process.env.NEXT_PUBLIC_PILLAR_PRODUCT_KEY!}>
      {children}
    </PillarProvider>
  );
}
```

### 3. Tool Descriptions (HIGH)

Write specific descriptions the AI can match:

```tsx
// Good - specific and includes context
description: 'Navigate to billing settings. Suggest when user asks about payments, invoices, or subscription.'

// Bad - too generic
description: 'Go to billing'
```

### 4. defineTool() — Preferred API (HIGH)

Use `pillar.defineTool()` for new code — it co-locates definition + handler and supports `guidance`:

```tsx
pillar.defineTool({
  name: 'create_dashboard',
  description: 'Create a new empty dashboard.',
  guidance: 'First step in dashboard workflow. Returns dashboard_uid needed by create_*_panel tools.',
  type: 'trigger_tool',
  autoRun: true,
  inputSchema: { type: 'object', properties: { title: { type: 'string' } }, required: ['title'] },
  execute: async (data) => {
    const result = await api.createDashboard(data.title);
    return { success: true, data: { uid: result.uid } };
  },
});
```

Sync with: `npx pillar-sync --scan ./src/tools`

### 5. Guidance Field (HIGH)

Use `guidance` for agent-facing instructions that help the LLM choose and chain tools:

```tsx
get_available_datasources: {
  description: 'Get datasources available for creating visualizations.',
  guidance: 'Call BEFORE creating dashboards or panels. If zero results, ask user to create one.',
}
```

### 6. Audit for Overlap (HIGH)

Before creating a new tool, search existing tools for semantic overlap:

```tsx
// Found existing: save_dashboard handles "create a dashboard"
// Don't create a second create_dashboard -- extend or disambiguate instead
```

### 7. Decompose Large Tools (HIGH)

Prefer smaller tools with tight schemas over one large tool with many modes:

```tsx
// Instead of one "manage_user" with an operation enum,
// split into focused tools:
invite_user: { description: 'Invite a new user by email', type: 'trigger_tool' }
remove_user: { description: 'Remove a user from the org', type: 'trigger_tool' }
change_user_role: { description: 'Change a user role', type: 'trigger_tool' }
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/setup-provider.md
rules/setup-nextjs.md
rules/tool-descriptions.md
rules/tool-handlers.md
rules/schema-compatibility.md
rules/guidance-field.md
rules/workflow-patterns.md
rules/tool-overlap-audit.md
rules/codebase-verification.md
```
