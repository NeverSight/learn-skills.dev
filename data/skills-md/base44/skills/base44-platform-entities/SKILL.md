---
name: base44-platform-entities
description: "Base44 entities: the JSON-schema data models under base44/entities/, the entity SDK, and row-level security (RLS) rules. Use when adding or changing stored data, queries, or per-user access rules in a Base44 app."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 entities

Entities are JSON-schema objects stored as `base44/entities/<Name>.jsonc`; writing the file is what defines the data model. The platform applies each entity's `rls` rules on every app-user request.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

## For every app

- [Row-level security (RLS)](references/rls.md)

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Entities and the entity SDK (web apps)](references/web.md) |
| Web app, TanStack Start | [Entities and the entity SDK (web apps)](references/web.md) |
| Native mobile app (Expo, React Native) | [Entities and the entity SDK (mobile apps)](references/mobile.md) |
