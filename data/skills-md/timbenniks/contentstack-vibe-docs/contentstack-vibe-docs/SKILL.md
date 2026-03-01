---
name: contentstack-vibe-docs
description: >-
  Comprehensive Contentstack CMS documentation for building web applications.
  Covers REST API, GraphQL API, Content Management API, Image Delivery API,
  TypeScript SDKs, Live Preview, OAuth authentication, and framework patterns
  for Next.js, Nuxt, and Gatsby. Use when implementing any Contentstack feature,
  fetching or managing content, setting up Live Preview, configuring regions,
  building CLI plugins, or creating Developer Hub apps.
license: MIT
metadata:
  author: timbenniks
  version: "2.0"
---

# Contentstack Documentation for AI Agents

Comprehensive, AI-optimized documentation for the Contentstack CMS. This skill contains ~10,000 lines across 20 reference files.

**STOP. Do not read all reference files.** Use the routing table below to read ONLY the 1-3 files relevant to your current task.

## Routing Table

Match your task to the right file(s). Read the minimum set needed.

| Task | Read this file | Lines |
|------|---------------|-------|
| Quick code pattern lookup | [QUICK_REFERENCE.md](references/QUICK_REFERENCE.md) | 477 |
| Understand Contentstack basics | [base-concepts.md](references/concepts/base-concepts.md) | 166 |
| Configure regions/endpoints | [regions.md](references/concepts/regions.md) | 350 |
| Fetch content (REST) | [rest-api.md](references/api/rest-api.md) | 487 |
| Fetch content (GraphQL) | [graphql-api.md](references/api/graphql-api.md) | 620 |
| Create/update/delete/publish content | [content-management-api.md](references/api/content-management-api.md) | 1138 |
| Transform/optimize images | [image-delivery-api.md](references/api/image-delivery-api.md) | 565 |
| Use TypeScript Delivery SDK | [delivery-sdk.md](references/sdk/delivery-sdk.md) | 431 |
| Implement Live Preview | [concepts.md](references/live-preview/concepts.md) | 131 |
| Live Preview (client-side, ssr:false) | [csr-mode.md](references/live-preview/csr-mode.md) | 268 |
| Live Preview (server-side, ssr:true) | [ssr-mode.md](references/live-preview/ssr-mode.md) | 315 |
| Build with Next.js | [nextjs.md](references/frameworks/nextjs.md) | 424 |
| Build with Nuxt | [nuxt.md](references/frameworks/nuxt.md) | 404 |
| Build with Gatsby | [gatsby.md](references/frameworks/gatsby.md) | 433 |
| Implement OAuth login | [oauth.md](references/authentication/oauth.md) | 906 |
| Create CLI plugins | [cli-plugins.md](references/extensions/cli-plugins.md) | 1672 |
| Build Developer Hub apps | [devhub-apps.md](references/extensions/devhub-apps.md) | 869 |
| See real-world code patterns | [practical-examples.md](references/examples/practical-examples.md) | 409 |
| Check package versions | [VERSIONS.md](references/VERSIONS.md) | 103 |

## Common Task Combinations

When a task requires multiple docs, read only these combinations:

| Scenario | Files to read (in order) |
|----------|------------------------|
| **New Next.js project** | base-concepts.md, delivery-sdk.md, nextjs.md |
| **New Nuxt project** | base-concepts.md, delivery-sdk.md, nuxt.md |
| **Add Live Preview to Next.js** | live-preview/concepts.md, live-preview/ssr-mode.md, nextjs.md |
| **Add Live Preview to Nuxt** | live-preview/concepts.md, live-preview/csr-mode.md, nuxt.md |
| **Build a content pipeline (CRUD)** | content-management-api.md |
| **Responsive image optimization** | image-delivery-api.md |
| **Full-stack with auth** | delivery-sdk.md, nextjs.md, oauth.md |
| **Content migration script** | content-management-api.md, regions.md |
| **Quick code snippet** | QUICK_REFERENCE.md (this alone is usually enough) |

## Decision Helpers

### Which API to use?

- Reading published content for a website/app -> REST API or GraphQL API or Delivery SDK
- Creating, updating, deleting, or publishing content -> Content Management API
- Transforming images (resize, crop, format) -> Image Delivery API

### Which SDK?

- `@contentstack/delivery-sdk` — reading content (frontend/backend)
- `@contentstack/management` — writing content (backend only, never in frontend)

### Which Live Preview mode?

**Important**: The `ssr` setting controls how preview updates work inside the CMS iframe, NOT your website's rendering strategy.

- **`ssr: false`**: Uses postMessage. CMS sends data changes to iframe, client JS re-fetches and updates UI instantly (no page refresh)
- **`ssr: true`**: CMS refreshes the iframe with query params (`?live_preview=hash&entry_uid=...`). Server reads params and fetches preview data

## Security: Credentials Handling

**NEVER ask the developer to share API keys, tokens, or secrets in the conversation.** Always use environment variable references (`process.env.CONTENTSTACK_API_KEY`, etc.) in code. Never output, log, or hardcode actual credential values. If the developer pastes a real token, warn them and suggest they rotate it.

## Questions to Ask Developers First

### Basic Setup

- **What Contentstack region?** (US, EU, AU, Azure, GCP) — Required for endpoints
- **Do you have credentials set up?** (API Key, Delivery Token, Preview Token as environment variables — do NOT ask for the actual values)
- **What environment?** (production, staging, preview)

### Framework & Architecture

- **What framework?** (Next.js, Nuxt, Gatsby, React, Vue)
- **Does your site fetch data client-side or server-side?** — Determines Live Preview SDK mode
- **What's the hosting?** (Vercel, Netlify, self-hosted)

### Content Requirements

- **What content types?** — Query patterns
- **Need references included?** — `.includeReference()` usage
- **Using modular blocks?** — Rendering patterns
- **Multiple locales?** — Locale handling
- **Need image transforms?** — Image Delivery API

### Authentication

- **Need user login?** — OAuth implementation with Contentstack
- **What framework?** — OAuth guide available for Next.js with Auth.js
- **Session storage?** — Cookie-based (JWT) or database-persisted

## Implementation Workflow

1. **Gather requirements** — Ask questions above
2. **Read relevant docs** — Use routing table, start with concepts if new
3. **Check examples** — Find matching patterns in QUICK_REFERENCE.md
4. **Implement step-by-step** — Follow patterns exactly
5. **Add error handling** — Always try-catch
6. **Use environment variables** — Never hardcode credentials
7. **Test thoroughly** — Verify with real stack

## Red Flags

**Never do these:**

- Ask the developer for actual API keys, tokens, or secrets — always reference `process.env.*` variables
- Output, log, or echo credential values in code, scripts, or responses
- Hardcode API keys or tokens — use environment variables
- Commit `.env` files or credentials to version control
- Use Management Tokens in frontend code — server-side only
- Read all reference files — pick only what you need
- Skip error handling
- Mix Delivery SDK patterns with Management SDK patterns
- Mix REST and GraphQL patterns incorrectly
- Forget to include references when needed

## Quick Start: Stack Initialization

The most common pattern — initialize the Contentstack SDK:

```typescript
// lib/contentstack.ts
import contentstack from "@contentstack/delivery-sdk";
import { getContentstackEndpoints } from "@timbenniks/contentstack-endpoints";

const endpoints = getContentstackEndpoints(
  process.env.CONTENTSTACK_REGION || "us",
  true // omitHttps = true (needed for SDK host parameter)
);

export const stack = contentstack.stack({
  apiKey: process.env.CONTENTSTACK_API_KEY!,
  deliveryToken: process.env.CONTENTSTACK_DELIVERY_TOKEN!,
  environment: process.env.CONTENTSTACK_ENVIRONMENT!,
  region: process.env.CONTENTSTACK_REGION || "us",
  live_preview: {
    enable: true,
    preview_token: process.env.CONTENTSTACK_PREVIEW_TOKEN,
    host: endpoints.contentPreview,
  },
});
```

### Basic Content Fetching

```typescript
// Fetch a single entry
const entry = await stack.contentType("blog_post").entry("entry_uid").fetch();

// Fetch all entries of a type
const entries = await stack
  .contentType("blog_post")
  .entry()
  .query()
  .find();

// Fetch with references included
const entry = await stack
  .contentType("blog_post")
  .entry("entry_uid")
  .includeReference(["author", "category"])
  .fetch();
```

### Environment Variables Template

```bash
CONTENTSTACK_API_KEY=your_api_key
CONTENTSTACK_DELIVERY_TOKEN=your_delivery_token
CONTENTSTACK_PREVIEW_TOKEN=your_preview_token
CONTENTSTACK_ENVIRONMENT=production
CONTENTSTACK_REGION=us
```

## Region Quick Reference

| Region Code | Provider | Content Delivery Host |
|-------------|----------|----------------------|
| `us` | AWS | `cdn.contentstack.io` |
| `eu` | AWS | `eu-cdn.contentstack.com` |
| `au` | AWS | `au-cdn.contentstack.com` |
| `azure-na` | Azure | `azure-na-cdn.contentstack.com` |
| `azure-eu` | Azure | `azure-eu-cdn.contentstack.com` |
| `gcp-na` | GCP | `gcp-na-cdn.contentstack.com` |
| `gcp-eu` | GCP | `gcp-eu-cdn.contentstack.com` |

Use the `@timbenniks/contentstack-endpoints` package instead of hardcoding these — see [regions.md](references/concepts/regions.md) for full details.

## Reference Directory

The `references/` directory contains detailed documentation organized by topic:

| Directory | Contents |
|-----------|----------|
| `references/api/` | REST, GraphQL, Content Management, and Image Delivery API docs |
| `references/sdk/` | TypeScript Delivery SDK guide |
| `references/concepts/` | CMS fundamentals and region configuration |
| `references/frameworks/` | Next.js, Nuxt, and Gatsby integration patterns |
| `references/live-preview/` | Live Preview concepts, CSR mode, and SSR mode |
| `references/authentication/` | OAuth with Auth.js for Next.js |
| `references/extensions/` | CLI plugin development and Developer Hub apps |
| `references/examples/` | Real-world code patterns |
| `references/QUICK_REFERENCE.md` | Condensed code patterns for quick lookup |
| `references/VERSIONS.md` | Package version compatibility |
