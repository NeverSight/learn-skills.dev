---
name: nextjs-nestjs-integration
description: Use for real projects that combine a Next.js frontend/BFF with a NestJS API. Covers ownership boundaries, OpenAPI client generation, session and auth propagation, CORS/proxy contracts, Server Component data fetching, shared environment contracts, and split deployment/runtime alignment.
metadata:
  author: xiro
  version: "0.1.0"
  organization: local
  date: May 2026
  framework: Next.js + NestJS
  frameworkVersion: "Next.js v16.2.6 / NestJS v11.1.16"
  supportedVersions:
    - "Next.js 15.x.x"
    - "Next.js 16.x.x"
    - "NestJS 10.x.x"
    - "NestJS 11.x.x"
  priority: high
  abstract: Integration skill for monorepos and distributed systems where Next.js owns UI/BFF concerns and NestJS owns durable API/domain contracts.
---

# Next.js NestJS Integration

Use this skill when a project has both a Next.js app and a NestJS API. The main job is to keep ownership boundaries clear so the web app does not accidentally duplicate backend policy, bypass API contracts, or self-fetch at build time.

## When to Apply

Use this skill when:
- Generating or consuming typed clients from a NestJS OpenAPI document
- Deciding whether logic belongs in Next.js Route Handlers/Server Actions or NestJS controllers/services
- Propagating auth/session context from Next.js to NestJS
- Configuring CORS, cookies, Proxy, rewrites, or internal API origins
- Fetching NestJS data from Server Components without calling the Next.js app's own Route Handlers
- Aligning Docker, environment variables, health checks, and deployment topology across apps

## Load On Demand

Start with this file. Load detailed files only when the task needs them:

```
references/_sections.md
references/integration-openapi-client-boundary.md
references/integration-session-propagation.md
references/integration-cors-proxy-contract.md
references/integration-server-component-fetching.md
references/integration-shared-env-contract.md
references/integration-deployment-split.md
dataset/integration/openapi-client-boundary/correct.ts
sources/inventory.json
```

Each rule file includes:
- Why the pattern matters
- Incorrect and correct examples
- Dataset path with larger TypeScript examples
- Official source references

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Integration Boundaries | CRITICAL | `integration-` |
| 2 | API Contracts | CRITICAL | `api-` |
| 3 | Deployment & Operations | HIGH | `deploy-` |

## Source Policy

Use this skill together with `nextjs-secure-bff`, `nextjs-production-platform`, and `nestjs-production-api-contracts` when the work spans both apps. Official Next.js and NestJS docs outrank framework-agnostic monorepo examples.
