---
name: marketplace-add-xmc
description: Adds XM Cloud API integration to a Sitecore Marketplace app. Use when the user wants to access Sites, Pages, Authoring, Content Transfer, Search, or Agent APIs from XM Cloud.
argument-hint: "[api-name]"
---

# Add XM Cloud API Integration

You are helping the user add XM Cloud API integration to their Sitecore Marketplace app.

## Prerequisites

The XMC package must be installed. If not:
```bash
npx shadcn@latest add https://marketplace-sdk.sitecorecloud.io/r/xmc.json
```

## Step 1: Determine Which API

Ask the user (or infer from $ARGUMENTS) which XMC API they need:

| API | Namespace | Use For |
|-----|-----------|---------|
| **Sites** | `xmc.sites.*` | List/get sites, current site context |
| **Pages** | `xmc.pages.*` | List/get pages, current page context |
| **Authoring** | `xmc.authoring.*` | GraphQL queries/mutations against authoring API |
| **Content Transfer** | `xmc.contentTransfer.*` | Import/export content |
| **Search** | `xmc.search.*` | Search content items |
| **Agent** | `xmc.agent.*` | Invoke XM Cloud agents |

## Step 2: Choose Client-Side or Server-Side

- **Client-side**: Use `client.query()` / `client.mutate()` — simpler, works in any architecture
- **Server-side**: Use `experimental_createXMCClient()` — requires Auth0 (full-stack architecture)

## Step 3: Implement

See [xmc-patterns.md](references/xmc-patterns.md) for complete code patterns for each API.

## Step 4: Suggest Related Skills

- Use `/marketplace-build-component` to build UI for the data
- Use `/marketplace-sdk-reference` for detailed type information

## Reference Files
- [XMC Patterns](references/xmc-patterns.md) — Code patterns for each XMC API
