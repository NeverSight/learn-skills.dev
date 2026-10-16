---
name: add-a-store
description: Add persistence through a service named for an application job, with validation, vendor Layers, migrations, bounded reads, and shared backend tests.
plain: "Name the facts and their writer, then put validated, bounded reads and writes behind one job-shaped port."
diagram: |-
  facts + one writer
    │
  port: small named ops
    │ decode input first
    │ bound every read
    ▼
  vendor Layer
    D1 or Postgres
    │
  same tests, each backend
---

# Add a store

A service is a named interface for one job. Its port declares the operations that callers need. An adapter implements those operations for a storage provider.

Effect describes work with typed failures and required dependencies. Schema defines accepted values and their runtime checks.

A Layer builds services and supplies their construction dependencies. Alchemy declares and deploys cloud resources through Effect programs.

A capability is one named action with shared value definitions and a server-side implementation.

Read `AGENTS.md` first. Follow its source-first rules before changing Effect or Alchemy code. Start from `packages/database` and check which storage requirements it meets.

## 1. Name the facts and their owner

- Name the stored data, its system of record, and the writer.
- Mark copies calculated from source data. Describe how to rebuild them, how current they are, and their consistency guarantees.
- Read `packages/database/src/model.ts` and `packages/database/src/run-log.ts`.
- Reuse `RunLog` when its person-scoped completed-run facts and operation guarantees fit the job.
- Name genuinely different facts before adding another store. Anonymous execution starts do not fit today's `RunLog` schema.
- Keep observational reporting failures from changing whether unrelated capabilities run or what they return, as request capture does in `packages/events`.
- If completeness requires gating execution, make that availability tradeoff an explicit product decision.
- Check composition before assuming recording exists. The deployed site does not currently provide or call `RunLog`.
- For a repeated aggregate, compare a bounded query with a keyed read model. Do not scan all history per page request.
- Write the authoritative fact once. Independent writes to source and aggregate cannot guarantee consistency.

Read `skills/rat-stack-mode/principles/name-the-system-of-record.md` and `skills/rat-stack-mode/principles/no-dual-writes.md`.

## 2. Define operations for the application job

- Copy the service shape in `packages/database/src/run-log.ts`.
- Give the port small named operations. Keep SQL, Drizzle, and vendor resources out of its callers.
- Put schemas and expected failures beside the port, as in `packages/database/src/model.ts`.
- Distinguish `InvalidDatabaseInput` from `DatabaseError`. Preserve operation and source cause.
- Define retries and operation identity explicitly. `RunLog.record` generates a fresh UUIDv7 for each call; it is not replay-idempotent.

The existing port has no atomic multi-write operation. Do not imply that two port calls share a transaction. If a source write and cursor must commit together, design that operation before building the adapter.

## 3. Validate input and decode stored rows

- Decode input before issuing storage statements, as `RunLog.record` and `RunLog.listRecent` do.
- Reject invalid input with `InvalidDatabaseInput` before storage work starts.
- Decode unknown returned rows with `PersistedRunLogRowSchema` in `packages/database/src/store.ts`.
- Decode the domain entry too. Reject mismatched outcome and failure fields instead of silently repairing them.
- Keep adapter failures typed as `DatabaseError`.

Read `skills/rat-stack-mode/principles/validate-before-durable-write.md`.

## 4. Implement each vendor and bound reads

- Read `packages/database/src/vendor.ts` and `packages/database/src/run-log-vendor.ts`.
- Keep each vendor's Drizzle operations in the cartridge, a package for one job with its implementation and required infrastructure. Choose one Layer with the exhaustive `DatabaseVendorResource` union.
- Name each read's key, index, ordering, row budget, and pagination rule.
- `ListRecentRunsInputSchema` bounds results to 1–100; adapters apply the person filter and `limit`.
- Inspect query plans. A bounded result can still scan many rows.
- Measure before choosing new operational limits. Label unmeasured values as guesses.

Read `skills/rat-stack-mode/principles/bound-every-read.md` and `skills/rat-stack-mode/principles/measure-real-limits.md`.

## 5. Carry schemas, migrations, and resources together

- Follow `packages/database/src/schema/d1.ts` and `packages/database/src/schema/postgres.ts`.
- Keep each dialect's migrations under `packages/database/migrations/`.
- Read `packages/database/src/migrations.ts` for paths that work outside the package directory.
- Follow `packages/database/src/d1.ts` or `packages/database/src/hyperdrive-postgres.ts` for resource-owning Layers.
- Keep connection strings redacted. Do not expose credentials through the port or failure messages.
- Follow `packages/database/src/postgres-migrations.ts` for deploy-time registration.
- Review infrastructure plans under AGENTS.md's approval rules. A schema change is not permission to delete a resource.

## 6. Prove the behavior on every storage implementation

Use `packages/database/test/run-log.test.ts` and `packages/database/test/local-layers.ts` as the executable references.

- Run the same behavior checks against D1 with local SQLite and Hyperdrive Postgres with PGlite.
- Check outcome variants, person isolation, ordering, limits, invalid inputs, and typed storage failures.
- Check replay and interrupted execution when the new operation promises idempotency or atomicity.
- Check migration paths with `packages/database/test/migration-paths.test.ts`.
- Prefer generated properties and command histories for new domain behavior. Plant a violation and observe failure before trusting them.

The current tests compare both storage implementations with examples. Deployed-provider behavior and vendor switching remain unproven. Name those gaps when reporting. Add real-infrastructure proof when the runtime differs from these substitutes.

## 7. Compose, validate, and report

Provide the chosen Layer at the app's composition root. Expose new actions through [add-a-capability](/skills/add-a-capability). For stateful workflows, also follow [add-a-lifecycle-machine](/skills/add-a-lifecycle-machine). Run `pnpm turbo run check test build` and fix failures without weakening the fence. The fence is the compiler checks, lint rules, and hooks that reject prohibited code and shortcuts.

Report:

- The port, operations, system of record, and derived copies.
- Vendor choice, schema changes, migrations, and resource-plan actions.
- Read bounds, query-plan evidence, and measured limits or explicit guesses.
- Validation, backend test results, replay proof, and atomicity gaps.
- Composition wiring and what remains unproven on deployed infrastructure.
