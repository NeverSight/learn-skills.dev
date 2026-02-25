---
name: nextjs
description: Next.js 16.1+ App Router patterns including Server Components, Client Components, Server Actions, Route Handlers, Turbopack, MCP integration, and modern React patterns. Use when building pages, layouts, data fetching, or API routes. Triggers on Next.js, App Router, RSC, or Server Actions questions.
metadata:
  author: FractionEstate
  version: '16.1.1'
---

# Next.js App Router

Expert knowledge for building modern web applications with Next.js App Router.

## Next.js 16.1.1 highlights

- **Turbopack improvements**: faster `next dev` restarts (project-dependent)
- **Bundle Analyzer** (experimental): `next experimental-analyze`
- **Easier Debugging**: `next dev --inspect`
- **Upgrade Command**: `next upgrade`
- **MCP Server**: Built-in `/_next/mcp` endpoint for coding agents

## MCP Server (Coding Agents)

Next.js 16+ includes MCP support for AI coding agents via `next-devtools-mcp`:

### Setup

```json
// .mcp.json at project root
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

### Available Tools

| Tool                      | Purpose                                            |
| ------------------------- | -------------------------------------------------- |
| `get_errors`              | Build errors, runtime errors, and type errors      |
| `get_logs`                | Dev log file path (browser console, server output) |
| `get_page_metadata`       | Routes, components, rendering info                 |
| `get_project_metadata`    | Project structure, config, dev server URL          |
| `get_server_action_by_id` | Lookup Server Actions by ID                        |

### Capabilities

- **Error Detection**: Real-time build/runtime/type errors
- **Live State Queries**: Access application state and runtime info
- **Page Metadata**: Query routes, components, rendering details
- **Server Actions**: Inspect Server Actions and component hierarchies
- **Knowledge Base**: Query Next.js documentation
- **Migration Tools**: Automated upgrade helpers with codemods
- **Playwright Integration**: Browser testing via [Playwright MCP](https://github.com/microsoft/playwright-mcp)

## Core Concepts

### Server Components (Default)

All components in the `app/` directory are Server Components by default:

```tsx
// app/posts/page.tsx - Server Component
export default async function PostsPage() {
  const posts = await db.post.findMany();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Client Components

Use `'use client'` directive for interactivity:

```tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>;
}
```

### Server Actions

Use `'use server'` for mutations:

```tsx
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  await db.post.create({ data: { title: formData.get('title') } });
  revalidatePath('/posts');
}
```

## File Conventions

| File            | Purpose               |
| --------------- | --------------------- |
| `page.tsx`      | Unique UI for route   |
| `layout.tsx`    | Shared UI wrapper     |
| `loading.tsx`   | Loading UI (Suspense) |
| `error.tsx`     | Error boundary        |
| `not-found.tsx` | 404 UI                |
| `route.ts`      | API endpoint          |

## References

- [references/routing.md](references/routing.md) - Routing patterns
- [references/data-fetching.md](references/data-fetching.md) - Data fetching strategies
- [references/server-actions.md](references/server-actions.md) - Server Actions guide

## Assets

- [assets/page.tsx](assets/page.tsx) - Basic page template
- [assets/layout.tsx](assets/layout.tsx) - Layout template
- [assets/route-handler.ts](assets/route-handler.ts) - API route template
- [assets/server-action.ts](assets/server-action.ts) - Server Action template
- [assets/middleware.ts](assets/middleware.ts) - Middleware template
