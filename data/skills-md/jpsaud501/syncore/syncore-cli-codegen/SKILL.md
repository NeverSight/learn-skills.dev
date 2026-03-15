---
name: syncore-cli-codegen
description: Syncore CLI workflows for project scaffolding, generated APIs, schema checks, sample-data import, seeding, SQL migrations, and the local devtools hub. Use when editing CLI source, codegen output, app bootstrapping, or the documented Syncore developer loop.
---

# Syncore CLI And Codegen

Use this skill when working on `@syncore/cli`, generated files, or the
developer loop inside a Syncore app.

## Documentation Sources

Read these first:

- `packages/core/src/cli.ts`
- `packages/cli/src/index.ts`
- `packages/cli/AGENTS.md`
- `README.md`
- `docs/development.md`
- `docs/architecture.md`

## Instructions

### CLI Commands

The current CLI surface includes:

- `npx syncorejs init`
- `npx syncorejs codegen`
- `npx syncorejs doctor`
- `npx syncorejs import --table <table> <file>`
- `npx syncorejs seed --table <table>`
- `npx syncorejs seed --table <table> --file <file>`
- `npx syncorejs migrate:status`
- `npx syncorejs migrate:generate [name]`
- `npx syncorejs migrate:apply`
- `npx syncorejs dev`

### init

`syncorejs init` scaffolds the standard project layout and supports templates
such as `minimal`, `node`, `react-web`, `expo`, `electron`, and `next`.

Core scaffold output is:

- `syncore.config.ts`
- `syncore/schema.ts`
- `syncore/functions/tasks.ts`
- `syncore/migrations/`
- `syncore/_generated/`

Template-specific files are added on top of that. Current scaffolding does not
create a special `syncore/crons.ts` file.

### codegen

`syncorejs codegen` scans `syncore/functions/**/*.ts`, finds exported `query`,
`mutation`, and `action` definitions, and generates:

- `syncore/_generated/api.ts`
- `syncore/_generated/functions.ts`
- `syncore/_generated/server.ts`

The generated API must preserve end-to-end types by referencing function
definitions through `createFunctionReferenceFor<typeof ...>(...)`.

Generated server helpers currently re-export `action`, `mutation`, `query`,
`createFunctionReference`, `createFunctionReferenceFor`, and `v`.

### dev

`syncorejs dev` is the main local development loop. It can scaffold a missing
Syncore project, then bootstraps codegen and migration work, starts the
devtools hub and dashboard shell when available, and watches relevant project
inputs.

### import And seed

Use `import` to load JSONL data into an explicit table and file path.

Use `seed` to load conventional sample data from `syncore/seed.jsonl` or
`syncore/seed/<table>.jsonl`, or from an explicit `--file` path.

### Migrations

The CLI compares the current schema against a stored snapshot and renders SQL
for safe changes.

Typical flow:

```bash
npx syncorejs migrate:status
npx syncorejs migrate:generate add_notes_table
npx syncorejs migrate:apply
```

`migrate:generate` accepts an optional name and falls back to `auto`.

### Monorepo Constraint

Inside the Syncore repo, examples intentionally run codegen from CLI source or
from already-built workspace packages. Avoid changes that require unrelated
shared `dist` output to exist while parallel tasks are running.

## Examples

### Typical App Loop

```bash
npx syncorejs dev
npx syncorejs doctor
npx syncorejs import --table tasks sampleData.jsonl
npx syncorejs seed --table tasks
```

### Generated API Pattern

Codegen should emit references shaped like this:

```ts
import { createFunctionReferenceFor } from "syncorejs";
import type { FunctionReferenceFor } from "syncorejs";
import {
  create as tasks__create,
  list as tasks__list
} from "../functions/tasks";

export const api = {
  tasks: {
    list: createFunctionReferenceFor<typeof tasks__list>("query", "tasks/list"),
    create: createFunctionReferenceFor<typeof tasks__create>(
      "mutation",
      "tasks/create"
    )
  }
} as const;
```

## Best Practices

- Treat codegen regressions as high-priority DX issues
- Keep generated files as outputs, never hand-maintained sources
- Preserve `createFunctionReferenceFor<typeof ...>` in generated API files
- Prefer `import type` where generated code only needs type positions
- Verify codegen changes with CLI tests and example integrations
- Keep the dev loop independent from workspace `dist` artifacts when examples are involved
- Document `syncorejs dev` as the happy path unless the task is specifically about one-off commands

## Common Pitfalls

1. Breaking type flow by emitting looser generated reference types
2. Requiring built CLI output during parallel example validation
3. Fixing generated files manually instead of fixing the template source
4. Treating migration SQL as unreviewed boilerplate
5. Documenting scaffolded files that the current templates no longer create

## References

- `packages/core/src/cli.ts`
- `packages/cli/src/index.ts`
- `packages/cli/AGENTS.md`
- `README.md`
- `docs/development.md`
