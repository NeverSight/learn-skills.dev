---
name: adding-entity-types
description: "Creates new Saleor entity types with complete implementation. Use when implementing new entities, adding modules, writing GraphQL operations, bulk mutations, deployment stages, Zod schemas for entities, or creating features that interact with Saleor API."
allowed-tools: "Read, Grep, Glob, Write, Edit"
metadata:
  author: Ollie Shop
  version: 1.0.0
compatibility: "Claude Code with Node.js >=20, pnpm, TypeScript 5.5+"
---

# Adding Entity Types

## Overview

Implement new Saleor entity types following a 7-step pipeline: schema, GraphQL operations, repository, bulk mutations, service, tests, and deployment stage. Each step builds on the previous, producing a complete entity module.

## When to Use

- Implementing a new Saleor entity (e.g., categories, products, menus)
- Adding a new module to `src/modules/`
- Creating features that need full CRUD with the Saleor API
- **Not for**: Modifying existing entities (see `understanding-saleor-domain`)

## Quick Reference

| Step | Output | Key File |
|------|--------|----------|
| 1. Schema | Zod validation | `src/modules/config/schema/<entity>.schema.ts` |
| 2. GraphQL | gql.tada operations | `src/modules/<entity>/operations.ts` |
| 3. Repository | Data access | `src/modules/<entity>/repository.ts` |
| 4. Bulk Mutations | Chunked processing | Integrated in repository |
| 5. Service | Business logic | `src/modules/<entity>/service.ts` |
| 6. Tests | Vitest + MSW | `src/modules/<entity>/*.test.ts` |
| 7. Pipeline | Deployment stage | `src/modules/deployment/stages/` |

## E2E Workflow

```
+-----------------+
| 1. Zod Schema   |  Define validation + infer types
+--------+--------+
         v
+-----------------+
| 2. GraphQL Ops  |  gql.tada queries/mutations
+--------+--------+
         v
+-----------------+
| 3. Repository   |  Data access + error wrapping
+--------+--------+
         v
+-----------------+
| 4. Bulk Mutations|  Chunking + error policies
+--------+--------+
         v
+-----------------+
| 5. Service      |  Business logic + orchestration
+--------+--------+
         v
+-----------------+
| 6. Tests        |  Unit + integration + builders
+--------+--------+
         v
+-----------------+
| 7. Pipeline     |  Add deployment stage
+-----------------+
```

## Step-by-Step Implementation

### Step 1: Define Zod Schema

Create in `src/modules/config/schema/<entity>.schema.ts`. Key patterns:
- Infer types with `z.infer<typeof schema>` (never manual type definitions)
- Use branded types for slugs/names (e.g., `transform((v) => v as EntitySlug)`)
- Use discriminated unions for variant types

See [references/zod-schemas.md](references/zod-schemas.md) for detailed patterns.

### Step 2: Create GraphQL Operations

Define in `src/modules/<entity>/operations.ts`. Key patterns:
- Import `graphql` from `@/lib/graphql/graphql` (gql.tada auto-types)
- Use `ResultOf<typeof Query>` for type inference
- Always include `errors { field, message, code }` in mutations
- Follow naming: `get<Entity>Query`, `create<Entity>Mutation`, `bulk<Action><Entity>Mutation`

See [references/graphql-operations.md](references/graphql-operations.md) for detailed patterns.

### Step 3: Implement Repository

Create `src/modules/<entity>/repository.ts`. Key patterns:
- Define interface (e.g., `EntityOperations`) for testability
- Wrap errors with `GraphQLError.fromCombinedError()`
- Always check both `result.error` and `result.data?.mutation?.errors`

See [references/repository-service.md](references/repository-service.md) for detailed patterns.

### Step 4: Add Bulk Mutations

Integrate chunked processing in repository. Key patterns:
- Use `processInChunks` from `@/lib/utils/chunked-processor`
- Threshold: `BulkOperationThresholds.DEFAULT` (10 items)
- Chunk size: `ChunkSizeConfig.DEFAULT_CHUNK_SIZE` (10 items/chunk)
- Error policy: `IGNORE_FAILED` (continue processing, report all failures)

See [references/bulk-mutations.md](references/bulk-mutations.md) for detailed patterns.

### Step 5: Create Service Layer

Create `src/modules/<entity>/service.ts`. Key patterns:
- Inject repository via constructor (interface, not concrete class)
- Validate inputs with Zod schema before passing to repository
- Orchestrate bulk operations and collect results

See [references/repository-service.md](references/repository-service.md) for detailed patterns.

### Step 6: Write Tests

Create in `src/modules/<entity>/`. Key patterns:
- Use test builders with fluent interface (`entityBuilder().withName("Test").build()`)
- Mock repositories with `vi.fn()` for unit tests
- Use MSW for integration tests with real GraphQL operations
- Validate builder output with Zod schema in `build()`

See [references/testing.md](references/testing.md) for detailed patterns.

### Step 7: Add to Deployment Pipeline

Create stage in `src/modules/deployment/stages/<entity>-stage.ts`:
- Set `order` after dependencies (entities this depends on)
- Skip if no config entries: `if (!config.entities?.length) return { skipped: true }`
- Delegate to service layer

## Validation Checkpoints

| Phase | Validate | Command |
|-------|----------|---------|
| Schema | Types compile | `npx tsc --noEmit` |
| GraphQL | Schema matches | `pnpm fetch-schema` |
| Repository | Unit tests | `pnpm test src/modules/<entity>/repository.test.ts` |
| Service | Integration | `pnpm test src/modules/<entity>/service.test.ts` |
| Pipeline | E2E flow | See `validating-pre-commit` skill |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not using branded types | Use `EntitySlug` or `EntityName` types for domain safety |
| Skipping bulk mutations | Use bulk for >1 item, always |
| Missing error wrapping | Wrap with `GraphQLError.fromCombinedError()` |
| Hardcoded pagination | Use `first: 100` with pagination support |
| Not checking `errors` array | Always check `result.data?.mutation?.errors` |

## Architecture Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Type source | Zod schemas | Single source of truth, runtime validation |
| GraphQL typing | gql.tada | Auto-inference from schema |
| Bulk threshold | 10 items | Balance granularity vs performance |
| Error policy | IGNORE_FAILED | Continue processing, report all failures |
| Chunking | 10 items/chunk | Rate limit compliance |

## Troubleshooting

### Schema Won't Compile

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Type 'string' is not assignable` | Missing branded type transform | Add `.transform((v) => v as EntitySlug)` |
| Circular type reference | Schema imports forming cycle | Extract shared primitives to `primitives.ts` |
| `z.infer` returns `any` | Schema not exported correctly | Check exports in `index.ts` |

### GraphQL Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot query field` | Schema drift | Run `pnpm fetch-schema` to update local schema |
| `Variable not provided` | Missing required variable | Check operation variables match gql.tada types |
| `Permission denied` | Token lacks scope | Verify token has required permissions in Saleor Dashboard |

### Deployment Stage Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Stage skipped unexpectedly | Config section empty or misspelled | Check top-level key name in `config.yml` |
| Dependency entity missing | Stage order incorrect | Verify `order` is after dependency stages |
| Bulk operation partial failure | Some items invalid | Check `IGNORE_FAILED` error policy output for details |

### Rollback

If a deployment stage fails mid-execution:
1. Run `pnpm dev introspect` to capture the current (partially modified) state
2. Compare with git history to identify what changed
3. Manually fix or re-deploy with corrected config

## Related Skills

- **Domain concepts**: See `understanding-saleor-domain`
- **Testing details**: See `analyzing-test-coverage`
- **Zod patterns**: See `designing-zod-schemas`
- **GraphQL details**: See `writing-graphql-operations`
- **Code quality**: See `reviewing-typescript-code`
