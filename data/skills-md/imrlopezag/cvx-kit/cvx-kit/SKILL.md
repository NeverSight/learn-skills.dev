---
name: cvx-kit
description: Build, migrate, and review Convex applications using cvx-kit table boundaries, authenticated functions, Effect commands and queries, relationships, triggers, and components. Use when the project depends on cvx-kit or the user requests its APIs.
---

# cvx-kit

Use the application's installed cvx-kit version and existing wiring. Inspect
`package.json`, the lockfile, and `convex/functions.ts` before selecting APIs.
These references come from the GitHub revision used to install this skill;
they may describe APIs newer than the application's package. Check exported
types when versions differ, and do not invent adapters or patch dependencies
to make a missing API appear. Upgrading requires the user's requested scope.

## Choose the relevant reference

Read only the guides needed for the task, resolving paths relative to this skill:

| Task                                                  | References                                                                                               |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Application structure and ownership                   | [architecture](references/architecture.md), [conventions](references/conventions.md)                     |
| Tables, masks, DTOs, variants, tool validators        | [zod-table](references/zod-table.md)                                                                     |
| Relationships, filtering, cursors, bounded pagination | [querying](references/querying.md)                                                                       |
| Variant joins, branch predicates, mixed pages         | [variant-querying](references/variant-querying.md)                                                       |
| Native-ID union links, inverse pages, link migration  | [native-id-relations](references/native-id-relations.md)                                                 |
| Authentication, roles, shared Effect context          | [auth](references/auth.md)                                                                               |
| Tenant isolation and row security                     | [tenancy](references/tenancy.md)                                                                         |
| Commands, queries, registry wiring, audit             | [commands](references/commands.md), [effect](references/effect.md)                                       |
| Contracts and domain API integration                  | [domain-contracts](references/domain-contracts.md), [domain-operations](references/domain-operations.md) |
| Request-local registry context                        | [command-context](references/command-context.md)                                                         |
| Timestamps and database lifecycle rules               | [triggers](references/triggers.md)                                                                       |
| Approval workflows and callbacks                      | [approvals](references/approvals.md)                                                                     |
| CRUD and agent tools                                  | [crud](references/crud.md), [agent-tools](references/agent-tools.md)                                     |
| Webhook verification and deduplication                | [webhooks](references/webhooks.md)                                                                       |
| Consumer lint rules                                   | [oxlint](references/oxlint.md)                                                                           |
| Migration and upgrades                                | [migration](references/migration.md), [upgrading](references/upgrading.md)                               |
| Maintaining an application                            | [maintainability](references/maintainability.md)                                                         |
| Existing deprecated Promise commands                  | [commands-legacy](references/commands-legacy.md)                                                         |

[llms](references/llms.md) is an optional condensed overview, not a prerequisite
for every task. Examples use illustrative entities; adapt them to the app.

## Preserve the boundaries

- Derive storage, input, and public DTOs from the entity's table declaration.
  Return projected DTOs, with matching return validators, rather than raw rows.
- Reuse the configured authenticated builders and injected policies. Authority
  and audit actors come from trusted context, not client inputs. Normalize
  external IDs against the expected table before fetching them.
- Use `cvx-kit/effect` for new command/query registries. Keep audit and writes in
  the mutation transaction; allow failures to escape for rollback. Return lazy
  Effects through the shared API builders rather than starting nested runners.
- Declare relations once and configure one global query engine. Apply read
  authorization and eligibility before bounded pagination. Unknown managed
  contexts fail closed; do not add an allow-all fallback.
- For variant patches, require the tag, fetch the expected table, verify the
  stored tag, merge and validate the complete storage row, then write in the
  same mutation. Declare branch-specific relation references and filter nodes
  explicitly; keep the public discriminated union intact.
- Keep native IDs in storage validators; JSON-safe tool inputs are a separate
  boundary. Let registered triggers maintain timestamps. Consume components
  through their public clients and generated references.

Run the application's relevant type checks, lint, and runtime tests. Test DTO
redaction, denied access, wrong-table IDs, invalid patches, and rollback when
those behaviors change. Distinguish in-memory tests from native deployment
and provider checks in the result.

## Source

[GitHub repository](https://github.com/ImRLopezAG/cvx-kit) ·
[Canonical documentation](https://github.com/ImRLopezAG/cvx-kit/tree/main/skills/cvx-kit/references)

Maintainers edit `skills/cvx-kit/references/*.md` directly. CI verifies portable
relative links with `bun run skills:check`.
