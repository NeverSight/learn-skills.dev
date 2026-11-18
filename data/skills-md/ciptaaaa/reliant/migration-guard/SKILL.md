---
name: migration-guard
description: Evidence-based risk analysis for database migrations. Use when a change adds, alters, or drops a table, column, index, or constraint in PostgreSQL or MySQL; when writing or reviewing ALTER TABLE, CREATE INDEX, or data backfill scripts; or when asked whether a migration is safe to deploy, needs a rollback plan, or will cause locking or downtime.
license: MIT
compatibility: Designed for coding agents that can read repository files. Requires no database connection. PostgreSQL and MySQL only.
metadata:
  author: reliant
  version: "0.1.0"
  phase: "1"
---

# Migration Guard

Analyze a database migration **before** it is considered done. The output is a risk report backed
by evidence, plus a safer migration path. You do not execute migrations.

## What makes this different from a normal review

A migration that is syntactically valid can still destroy data, block a table for minutes, or break
the running application version. Your job is to find out whether this specific migration, against
this specific schema and this specific application code, is safe — and to prove it.

**The rule you must never break:** every risk level you assign must cite evidence you actually
found. If you lack evidence, downgrade your confidence and say what you could not verify — do not
guess and do not stay silent about the gap.

## Hard constraints

- Do not run the migration, and do not connect to a database. Read files only.
- Do not request production credentials, and do not suggest that the user paste production data.
- Never produce an `APPROVED` verdict when any evidence needed for the riskiest finding is missing.
  Use `CONDITIONAL` with an explicit verification step instead.
- A finding may never be more severe than the evidence supports. Unverified data property → `HIGH`
  with the check query, not `BLOCKER`. See [risk classification](references/risk-classification.md) §2.
- Any data change needs whatever permission the host agent requires. On top of that, an
  **approval to accept risk** is required only when the old value cannot be restored. Reversibility,
  not the operation type, decides — see "Approvals" below.
- Do not invent table sizes, row counts, lock durations, or database behavior. If the user did not
  provide them, list them under **Unknowns** and state how a missing value changes the risk.

## Workflow

Work through these steps in order. Do not skip steps, and do not write the report until you finish
step 5.

- [ ] **Step 1 — Identify engine and version.** Find the engine (PostgreSQL or MySQL) and the version
      from config, Dockerfiles, CI, `package.json`, `requirements.txt`, `Gemfile`, or the user's
      message. Version changes the answer for many operations. If unknown, say so and record it in
      **Unknowns** — it may cap the verdict at `CONDITIONAL`. If the engine is MariaDB or anything
      other than PostgreSQL/MySQL, say the analysis does not apply and stop at `CONDITIONAL`.
- [ ] **Step 2 — Reconstruct the schema.** Read migrations, `schema.sql`, or an ORM model to learn
      the current definitions of every table the migration touches: columns, types, nullability,
      defaults, indexes, constraints, foreign keys, and approximate size if available.
- [ ] **Step 3 — Read the migration.** Parse every statement. For each one, record exactly what it
      does to the schema, and classify it as additive, modifying, or destructive.
- [ ] **Step 4 — Trace application usage.** Search the codebase for every affected identifier (table,
      column, index, constraint). Include raw SQL, ORM models, query builders, views, migrations
      still pending, seeders, analytics jobs, reporting code, and ETL scripts. Cite `path:line` for
      each hit, and note absence explicitly (`no references outside schema.sql`).
- [ ] **Step 5 — Assess operational impact and rollback.** Decide whether the change rewrites the
      table, takes a blocking lock, needs a backfill, or is irreversible. Compare against the
      deployment model: does an older application version still run while the new schema is live?
      Then classify each finding and compute the verdict.

Steps 1-3 usually need `references/risk-classification.md` only. Load engine specifics only when the
migration needs them:

- PostgreSQL (locks, `CONCURRENTLY`, `NOT VALID`, rewrites, `USING`):
  read `references/postgres.md`.
- MySQL/InnoDB (`ALGORITHM=INSTANT|INPLACE|COPY`, `LOCK=`, metadata locks, implicit commit):
  read `references/mysql.md`.
- Need a safer version of a risky operation: read `references/safe-migration-patterns.md`.
- Need a recovery or downgrade plan, or the user asked about rollback: read
  `references/rollback-strategy.md`.

## Gotchas

These are the mistakes that make a migration review wrong:

- **A valid migration is not a safe migration.** `ALTER TABLE users DROP COLUMN phone;` parses fine
  and still breaks every code path that selects `phone`. Never treat "the SQL is valid" as a verdict.
- **"No references found" is weak evidence.** The column may be used in a reporting repo, a BI
  dashboard, a mobile app, or a migration not yet applied. Say where you looked, and treat
  unsearched surfaces as unknowns.
- **The old application version is still running during a rolling deploy.** Renames, drops, and
  `NOT NULL` additions break version N while version N+1 is still rolling out.
- **MySQL DDL implicitly commits.** A "transaction-wrapped" DDL is not atomic. A failed multi-statement
  migration may leave half the changes applied.
- **PostgreSQL `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block**, and a failed
  concurrent build leaves an `INVALID` index behind.
- **Adding `NOT NULL` without a default requires a full table scan and fails on existing `NULL`s**
  unless you use the add-constraint-as-`NOT VALID` then `VALIDATE` pattern.
- **`MEDIUM` is not a pass.** A backfill on a large unspecified table is operational risk, not a
  formality.

## Risk levels

Use exactly these five levels. Full criteria live in `references/risk-classification.md`.

| Level | Meaning |
|---|---|
| `BLOCKER` | Unsafe based on evidence (proven data loss or application breakage in scope) |
| `HIGH` | Large risk to data or operations (likely data loss, rewrite, blocking lock, deploy breakage) |
| `MEDIUM` | Risk that requires mitigation (backfill, coordinated release, extra verification) |
| `LOW` | Relatively small risk (additive, non-destructive, cheap on the stated schema) |
| `INFO` | Additional information; no risky finding in the inspected scope |

## Verdict

| Verdict | When |
|---|---|
| `BLOCKED` | At least one unresolved `BLOCKER` finding |
| `CONDITIONAL` | No `BLOCKER`, but at least one `HIGH` or `MEDIUM` finding, or a material unknown |
| `APPROVED` | No finding above `LOW`, all required evidence present, scope stated |

`APPROVED` means only that no blocker was found in the inspected scope with the evidence available.
Say this in the report every time. It is not a guarantee for production.

Report the verdict as the single worst case:

1. Any `BLOCKER` → `BLOCKED`.
2. Else any `HIGH`/`MEDIUM`, or any unknown that could hide a `BLOCKER` (e.g. row count unknown for
   a `NOT NULL` backfill, old application version status unknown for a rename) → `CONDITIONAL`.
3. Else `APPROVED`.

## Approvals

Separate two questions that are easy to merge:

- **Approval to execute** — the host agent's own permission model decides this. The skill cannot grant
  it and does not replace it. Every write, and every step that would touch a database, needs it.
- **Approval to accept risk** — a human decision that data loss or irreversible change is acceptable.
  Required only when the previous value **cannot be restored**.

Reversibility decides the class, not the operation name. An `UPDATE` can be either class; a `DROP
COLUMN` never makes it reversible.

| Class | Test | Required |
|---|---|---|
| Reversible, additive | Old value was `NULL` or default; data is derived and recomputable; column/table added and nothing wrote to it | `none` — state that it is reversible and why |
| Reversible but costly | Restorable with effort/schedule: large backfill, coordinated release, long lock | `schedule` — window, throttle, abort conditions |
| Irreversible | Old value overwritten or deleted; structure removed with data; narrowing type change | `accept-risk` — plus recovery plan and restore point |

If an irreversible step has no recovery plan, the finding is at least `BLOCKER`. A reversible step
without a recovery plan is not.

## Report format

This format is **mandatory and machine-parsed**. Emit exactly these six headings, in this order, and
nothing else. Do not add a Summary, Overview, Conclusion, or Notes section; put that content in the
relevant finding. A tool matches your output against this contract, so a different structure is an
unparseable report even when the analysis is correct.

Rules that are easy to get wrong:

1. The verdict word is exactly one of `BLOCKED`, `CONDITIONAL`, `APPROVED`. Write `BLOCKED`, not
   `BLOCK`, `BLOCKING`, or `DO NOT MERGE`.
2. Every finding heading begins with `### F<number> — <SEVERITY> — <category>`, using the literal
   severity token and one category from the list below. Severity belongs in the heading, not in a
   separate `**Risk:**` line.
3. Quote the file path with a line number in **Evidence**. A finding without a path citation is an
   Unknown, not a finding.

Categories (use one per finding): `destructive-column-drop`, `destructive-table-drop`, `type-change`,
`not-null-add`, `unique-constraint`, `foreign-key`, `index-build`, `lock-and-rewrite`, `backfill`,
`rename`, `charset-collation`, `implicit-commit`, `application-compatibility`, `data-integrity`,
`operational`, `no-risk-observed`.

````markdown
# Migration Guard Report

## Scope
- **Migration**: path or filename
- **Engine**: PostgreSQL 16 / MySQL 8.0 / unknown
- **Inspected**: files and directories you actually read
- **Not inspected**: directories, external services, analytics, mobile clients, etc.
- **Unknowns**: unknown version, row counts, deployment model, missing schema files

## Verdict
**BLOCKED** — one-sentence justification that names the decisive finding.

> APPROVED (when used): no blocker found for the inspected scope and evidence. This is not a
> guarantee of production safety.

## Findings

### F1 — BLOCKER — destructive-column-drop
- **Statement**: `ALTER TABLE users DROP COLUMN phone` in `migration.sql:2`
- **Why it is risky**: concrete consequence (data lost, query fails, table locked for N minutes)
- **Evidence**:
  - `app/controllers/users_controller.rb:31` — `slice(:phone)` returns it in the API response
- **Mitigation**: the safe alternative or precondition
- **Verification**: how a human confirms the mitigation worked
- **Approval**: `none` | `schedule` | `accept-risk`
- **Reversible**: yes | no

### F2 — INFO — no-risk-observed
- **Statement**: what you examined
- **Evidence**: `path:LINE`
- **Why it is safe**: the mechanism or schema fact

## Safer migration path
Numbered, ordered steps for the recommended alternative (for example expand-and-contract), with the
engine-specific syntax the user needs.

## Rollback and recovery
- **Schema rollback**: what reverses the structure, and whether it is cleanly reversible
- **Data recovery**: what happens to rows changed or deleted by this migration
- **Application rollback**: whether the previous app version works with the new schema
  (call out separately when "rollback" would not restore data)

## Pre-deploy checklist
- [ ] Human approval recorded for each `accept-risk` step
- [ ] Backup or snapshot confirmed (type and scope)
- [ ] Old application version status confirmed
- [ ] Verification queries listed below are runnable
- [ ] (any further case-specific item)
````

## Calibration examples

**Destructive and used → BLOCKER.**

```sql
ALTER TABLE users DROP COLUMN phone;
```

Evidence: `app/api/users.py:41` selects `phone`; `app/models/user.rb:12` declares the attribute;
scope note says the column is also exported to a partner integration.

**Edge case that is easy to get wrong: `NOT NULL` on an empty-in-practice column.**

```sql
ALTER TABLE orders ADD CONSTRAINT orders_status_not_null CHECK (status IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_not_null;
```

If `application-usage.md` and the user confirm there are zero NULL rows and the table is small, this
is `LOW`. If NULL rows exist, `VALIDATE` fails and the migration is `HIGH` with a backfill-then-validate
mitigation. Do not apply the PostgreSQL pattern blindly in MySQL — the mechanisms differ.

**Category flags for classification.** Tag every finding with a `category` so results are comparable
across runs. Use one of: `destructive-column-drop`, `destructive-table-drop`, `type-change`,
`not-null-add`, `unique-constraint`, `foreign-key`, `index-build`, `lock-and-rewrite`,
`backfill`, `rename`, `charset-collation`, `implicit-commit`, `application-compatibility`,
`data-integrity`, `operational`, `no-risk-observed`.

## Anti-patterns to reject

- A report with zero findings that never states what was inspected.
- A severity without a citation.
- "Looks safe" or "should be fine" without a rollback and verification plan.
- Treating a pending backfill "to be done later" as a mitigation. Either it is scheduled and
  specified, or the finding stands.
- Recommending `IF EXISTS` or `IF NOT EXISTS` as a safety measure. It hides a mismatch between the
  expected schema and the real one.
