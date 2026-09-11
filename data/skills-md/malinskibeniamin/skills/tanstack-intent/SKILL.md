---
name: tanstack-intent
description: Use TanStack Intent when a TanStack package is mentioned, referenced, or worked on. Load version-matched guidance before answering or changing Router, Query, Table, or other TanStack code.
---

Ask Intent for installed-package docs before answering, planning, reviewing, or editing any TanStack work.

## Load

1. Identify relevant `@tanstack/*` packages from request, imports, nearest `package.json`; never assume version.
2. At package root run:

```bash
bunx @tanstack/intent@latest list --json
```

3. Match `skills[].packageName`, `description`, and `use`; load each exact id:

```bash
bunx @tanstack/intent@latest load "$use_id"
```

4. Load its `requires`; compositions load every owner, such as Router+Query or Table+Query.

Use repo command runner when not Bun. Never guess ids or choose a similarly named framework.

## Authority

Installed Intent owns API syntax, status, migration, and framework behavior. Local `/tanstack-router`/`/tanstack-table` adds repo policy/checks afterward. Conflicts are harness defects: follow installed guidance and repair the harness.

If package/skill is absent, state no version-matched guidance and use `/read-the-damn-docs` against official TanStack sources; never silently rely on memory.

Setup: [SETUP.md](SETUP.md). Completion names loaded `package@version` and `use` ids.
