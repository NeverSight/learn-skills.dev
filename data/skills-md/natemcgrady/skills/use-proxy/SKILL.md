---
name: use-proxy
description: Remind the assistant to use Next.js 16 Proxy (`proxy.ts`) instead of Middleware (`middleware.ts`) when working on Next.js apps, including migration guidance and reference links.
---

# Use Proxy, not Middleware

- Default to creating or updating `proxy.ts` (or `src/proxy.ts`) with a `proxy` export.
- If a request mentions `middleware.ts` or `middleware` in Next.js 16, call out that Proxy replaces Middleware and suggest renaming.
- When migrating, recommend running the codemod: `npx @next/codemod@canary middleware-to-proxy .`

References:
- https://nextjs.org/docs/messages/middleware-to-proxy
- https://nextjs.org/docs/app/getting-started/proxy