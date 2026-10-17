---
name: error-states-and-empty-ui
description: >-
  Use when building lists, tables, dashboards, feeds, or any data-driven UI that
  needs loading, empty, error, or retry states. Not for static marketing pages
  or pure styling tweaks.
---

# Error states and empty UI

Every data surface needs four states: **loading**, **empty**, **error**, **success**.

## Loading

- Use skeletons or spinners matching layout (table rows → row skeletons).
- Disable destructive buttons while loading.
- Avoid layout shift (reserve min-height where needed).

## Empty (required quality)

Never ship bare `"No data"` alone. Include:

- **What** this list is.
- **Why** it might be empty (first visit vs filters).
- **Primary action** (e.g. "Create your first project").

```tsx
<EmptyState
  title="No projects yet"
  description="Create a project to start tracking work."
  action={<Button onClick={onCreate}>New project</Button>}
/>
```

Differentiate **filtered empty** vs **truly empty** when filters exist.

## Error

- Human-readable message (not raw `error.message` from API unless debug mode).
- **Retry** button calling `refresh()` / `refetch()`.
- Log technical detail to console only in dev.

## Success edge cases

- Partial load failures: show what loaded + inline error for the failed section.
- Optimistic UI: rollback on mutation failure + toast (see `optimistic-updates`).
- Forbidden (403): explain *why* instead of pretending the resource doesn't exist, where appropriate.

## Checklist per list/table

- [ ] Loading UI
- [ ] Empty UI with CTA
- [ ] Error UI with retry
- [ ] No infinite spinner on failed fetch

## Avoid

- Blank `<div />` when `data.length === 0`.
- Swallowing errors silently.
- Loading forever when `error` is set.
