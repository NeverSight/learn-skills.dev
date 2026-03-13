---
name: nextjs-app-router
description: "Next.js App Router implementation workflow for route structure, server/client boundaries, and caching/revalidation behavior. Use when App Router architecture or data/rendering behavior must be implemented or changed; do not use for repository-wide architecture governance or release management policy."
---

# Nextjs App Router

## Overview
Use this skill to design App Router implementations that are predictable in rendering, caching, and navigation behavior.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Server/client and cache rules:
  - `references/server-client-and-cache-rules.md`

## Templates And Assets
- App Router architecture template:
  - `assets/app-router-architecture-template.md`
- App Router verification checklist:
  - `assets/app-router-checklist.md`

## Inputs To Gather
- Route hierarchy, layout composition, and navigation requirements.
- Server/client interaction boundaries.
- Freshness, SEO, and caching constraints.
- Error/loading behavior requirements.
- Route param/search param/request payload contracts and ownership boundaries.

## Deliverables
- Route/layout map with rendering strategy.
- Data-fetch and cache/revalidation policy.
- Error/loading/not-found boundary plan.
- Verification evidence for transition and consistency behavior.

## Workflow
1. Define route/layout architecture in `assets/app-router-architecture-template.md`.
2. Apply server/client boundary rules from `references/server-client-and-cache-rules.md`.
3. Parse and normalize route/search/action inputs at boundaries into explicit typed shapes.
4. Configure fetch/cache/revalidation policy per route criticality.
5. Implement explicit loading/error/not-found boundaries.
6. Validate with `assets/app-router-checklist.md`.

## Quality Standard
- Route tree and ownership are explicit.
- Server/client boundaries are minimal and intentional.
- Cache policy matches data freshness requirements.
- Navigation preserves data consistency across transitions.
- Server actions and route handlers avoid repeated cast-heavy shape fixes by using boundary-normalized contracts.

## Failure Conditions
- Stop when boundaries between server and client are ambiguous.
- Stop when caching strategy risks stale or inconsistent user state.
- Escalate when critical route behavior cannot be made deterministic.
