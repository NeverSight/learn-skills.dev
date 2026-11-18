---
name: postgres-writing-guidelines
description: "Use when writing or reviewing PostgreSQL/PL-pgSQL, designing table schemas, writing functions and procedures, building migrations, defining domains, or architecting a Postgres application database. Also use when writing RAISE EXCEPTION patterns, BEFORE/AFTER triggers for cross-table constraints, base/subtype hierarchies, composite key designs, row-level security policies, or idempotent DDL scripts. If you are touching Postgres for an application database, use this skill. PostgreSQL-specific — examples will not run on other engines."
---

# Postgres Writing Guidelines


## When to Use

- Starting a new PostgreSQL application database from scratch
- Adding tables, views, functions, procedures, or triggers to an existing schema following this methodology
- Reviewing PL/pgSQL for type safety, RLS coverage, and structural enforcement
- Writing migrations that must be idempotent and safe to rerun
- Designing table hierarchies (base/subtype, parent-child composite keys)
- Implementing background job queues backed by Postgres tables (`FOR UPDATE SKIP LOCKED`)

**When NOT to use:** one-off ad-hoc queries, read-only reporting databases, or any non-Postgres engine. Examples and syntax throughout are PostgreSQL/PL-pgSQL.

## snake_case Everywhere

Postgres folds unquoted identifiers to lowercase. Using `PascalCase` forces double-quoting (`"PascalCase"`) on every reference, forever. **Use `snake_case` for everything**: tables, columns, views, functions, procedures, types, constraints, parameters.

| Object | Pattern | Examples |
|--------|---------|----------|
| Tables | `entity_name` | `account`, `customer`, `order_line` |
| Views | `vw_<role>_<intent>` | `vw_manager_team_report`, `vw_admin_all_customers` |
| Materialized views | `mv_<role>_<intent>` | `mv_customer_lifetime_value` |
| Procedures | `pr_<verb>_<noun>` | `pr_add_order_line`, `pr_modify_customer`, `pr_remove_order` |
| Functions | `fn_<descriptive>` | `fn_next_order_no`, `fn_find_customer` |
| Trigger functions | `tg_<subject>_<action>` | `tg_savings_account_check_type` |
| Constraints | `subject_relationship_object` | `customer_rents_vehicle`, `savings_account_is_account` |
| Domains | `noun` (lowercase) | `email`, `account_no`, `api_key` |

Avoid SQL keywords as verbs — use `add`/`modify`/`remove`/`find` instead of `create`/`update`/`delete`/`select`. Avoid abbreviations unless universally understood (`no` for Number, `id` for external identifiers).

For full naming guide, read [Naming Conventions](references/naming-conventions.md).

## Custom Type System (CREATE DOMAIN)

Never use bare built-in types (`VARCHAR`, `INT`, `TIMESTAMPTZ`, `BOOLEAN`) for columns. Define a catalog of named **DOMAINs** that form a consistent, semantic layer. Postgres DOMAINs support inline CHECK constraints.

    CREATE DOMAIN email AS VARCHAR(100) NOT NULL
        CHECK (VALUE LIKE '%_@_%.__%');

    CREATE DOMAIN api_key AS VARCHAR(128) NOT NULL;
    CREATE DOMAIN account_no AS BIGINT NOT NULL;
    CREATE DOMAIN ts_now AS TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp();
    CREATE DOMAIN bool_false AS BOOLEAN NOT NULL DEFAULT FALSE;

Every column uses a named DOMAIN. `email` instead of `VARCHAR(100)`. `ts_now` instead of `TIMESTAMPTZ`. `bool_false` instead of `BOOLEAN`.

**Consistency.** Change the domain definition once; every column using it updates.

**Semantic inference.** `api_key` tells you what the data *is*; `VARCHAR(128)` tells you nothing. Find every API key column by querying `information_schema.columns` for `domain_name = 'api_key'`.

**NOT NULL by default.** Define DOMAINs as `NOT NULL`. Nullable only with explicit business reason — optional is a deliberate design choice, not the default.

**Organize by category** (identity, web/auth, civic, financial, generic primitives) and maintain a YAML manifest as the source of truth. Domain names are unique per system — a property management app has `party_no`, `entrata_id`, `lease_no`; a financial app has `account_no`, `transaction_no`, `routing_number`.

## Enums vs Reference Tables

Postgres has two ways to constrain a column to a fixed vocabulary: `CREATE TYPE ... AS ENUM` and a reference (lookup) table with a FK. **Default to reference tables** — they support extra columns (display name, sort order, deprecated flag), serve as FK targets, and accept runtime additions. Reach for `ENUM` only when the vocabulary is closed, stable, and value-only (audit actions, simple labels).

For decision rules, the migration path between them, and the hybrid pattern — read [Enums vs Reference Tables](references/enums-vs-references.md).

## Time & Timezones

**Always use `timestamptz`, never `timestamp` (without timezone).** Store UTC at rest; convert at the read boundary using `AT TIME ZONE 'America/New_York'`. Use `clock_timestamp()` for true wall-clock samples, `transaction_timestamp()` (or `now()`) for "as of the transaction start." Use `date` (not `timestamptz` at midnight) when time-of-day doesn't matter. For non-overlapping periods, use `tstzrange` + `EXCLUDE` constraints.

For bucketing, gap-filling with `generate_series`, range operators, and common gotchas — read [Time & Timezones](references/time-and-timezones.md).

## UUID Strategies

Pick UUIDs only when you need distributed ID generation, public-facing identifiers, or merge-friendly cross-system IDs. Default to `bigint` (or hierarchical composite keys) for internal data — they're smaller, faster, and index better. Common production pattern: **`bigint` PK for internal joins + a `uuid` `public_id` column for the API boundary.** If you do use a UUID PK on a high-write table, prefer **UUID v7** (time-ordered) over v4 to keep B-tree index performance acceptable.

For storage costs, index fragmentation, v4 vs v7 tradeoffs — read [UUID Strategies](references/uuids.md).

## Generated Columns

For derived data that's queried often, use `GENERATED ALWAYS AS (...) STORED` instead of a trigger:

    full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED

Postgres keeps it in sync automatically, you can index it like any column, and the expression is type-checked at definition time. The expression must be deterministic (no `clock_timestamp()`, no cross-row data); use a trigger for anything else.

For patterns and limitations — read [Generated Columns](references/generated-columns.md).

## Schema Separation

Split your DB into logical schemas — `app` (live tables), `audit` (history), `ref` (lookup), `archive` (cold storage), `util` (helpers). Schemas are namespaces inside one DB; cross-schema FKs and joins work transparently. **Granting a role access requires both `USAGE` on the schema and `SELECT`/`EXECUTE` on the objects** — forgetting the `USAGE` is a common permission bug.

For layout, `search_path` management, and migration tool configuration — read [Schema Separation](references/schema-separation.md).

## Two Access Rules in Postgres

Postgres's native row-level security puts the security boundary at the table layer. Views and procedures don't need to act as access gates to keep data safe — they earn their keep for other reasons.

**The new posture:**

- **Direct table access is fine** when RLS + CHECK constraints + triggers cover the rules.
- **Use views** when they add value: flattening multi-table joins, role-specific column projections, hiding schema evolution.
- **Use procedures** when you need: multi-statement atomicity, multi-table coordination, business rule enforcement spanning entities.

Views and procedures become tools for **API ergonomics and business logic**, not security boundaries. Don't add a procedure where a constrained-and-policied table will do.

## Row-Level Security (Native, Replaces View-Based Filtering)

Each table holding user-scoped data enables RLS and defines policies. The filter happens transparently regardless of how the data is queried — `SELECT *` returns only rows the current role is allowed to see.

    ALTER TABLE customer ENABLE ROW LEVEL SECURITY;

    CREATE POLICY customer_owner_can_read ON customer
        FOR SELECT
        USING (owner_id = fn_current_app_user_id());

    CREATE POLICY customer_owner_can_modify ON customer
        FOR UPDATE
        USING (owner_id = fn_current_app_user_id())
        WITH CHECK (owner_id = fn_current_app_user_id());

    CREATE POLICY admin_full_access ON customer
        FOR ALL TO admin_role
        USING (TRUE) WITH CHECK (TRUE);

`fn_current_app_user_id()` is a `SECURITY DEFINER` function that returns the application user's ID, typically derived from a session variable set at connection time (`SET LOCAL app.user_id = ...`).

For full RLS patterns — policies, USING vs WITH CHECK, FORCE RLS, multi-tenant designs, bypass roles, debugging — read [Row-Level Security](references/row-level-security.md).

## Transaction Model — No Hierarchy, No Nesting

Postgres enforces transaction boundaries naturally:

- **PROCEDUREs** can `COMMIT`/`ROLLBACK`, but only when `CALL` runs in its own transaction. Inside the caller's `BEGIN` block, the `COMMIT` fails with `2D000` (`invalid_transaction_termination`).
- **FUNCTIONs** always run inside a transaction (the caller's, or implicit). They cannot `COMMIT`/`ROLLBACK`.
- **A PL/pgSQL block with an `EXCEPTION` clause is a subtransaction.** It cannot `COMMIT` or `ROLLBACK`, and PL/pgSQL has no `SAVEPOINT` command. A nested `BEGIN ... EXCEPTION ... END` block is how PL/pgSQL rolls back part of the work.

**Default: the caller owns the transaction.** A procedure does its work and lets errors propagate, so the caller's transaction (or the implicit one around a bare `CALL`) rolls back. Only a procedure that deliberately owns batch boundaries calls `COMMIT`, and only outside any block with an `EXCEPTION` clause.

**The one rule: no explicit nested transactions.** Never wrap one `BEGIN` inside another. For selective rollback, use a nested `BEGIN ... EXCEPTION ... END` block in PL/pgSQL, or `SAVEPOINT` in client-side SQL.

A batch procedure that commits must be called outside an explicit transaction; PostgreSQL enforces this with `2D000` at the first `COMMIT`.

For full procedure/function templates, transaction patterns, and selective rollback — read [Procedure Structure](references/procedure-structure.md).

## Concurrency & Locking

Postgres has four row-lock strengths: `FOR KEY SHARE`, `FOR SHARE`, `FOR NO KEY UPDATE`, and `FOR UPDATE` (strongest). **Most app updates only need `FOR NO KEY UPDATE`** — `FOR UPDATE` is overkill unless you're changing keys. Use `SKIP LOCKED` for queue claim, `NOWAIT` to fail fast instead of blocking. For high-throughput state changes where conflicts are rare, prefer **optimistic concurrency** (version columns) over pessimistic locking. Use `pg_advisory_xact_lock(...)` to serialize operations that don't map to a single row (e.g., max-plus-one ID generation per parent).

For lock modes, deadlock prevention (consistent ordering of lock acquisition), and isolation levels — read [Concurrency & Locking](references/concurrency-locking.md).

## Error Handling (EXCEPTION Blocks, SQLSTATE Codes)

PL/pgSQL has no `GOTO`. Errors flow through `EXCEPTION WHEN ... THEN` blocks, which automatically roll back the surrounding subtransaction. For client-parseable errors, use a SQLSTATE catalog:

    RAISE EXCEPTION 'email already taken: %', new_email
        USING ERRCODE = 'Z0003';

SQLSTATE codes are 5 alphanumeric chars. Application codes use class `Z0` (`Z0001`–`Z0999`), not `P0`: PostgreSQL owns `P0001`–`P0004` (`raise_exception`, `no_data_found`, `too_many_rows`, `assert_failure`), so a `P0` application code collides with native PL/pgSQL errors. Maintain a constants document mapping codes to semantic names so client apps can match on the code:

| Code | Meaning |
|------|---------|
| `Z0001` | INVALID_INPUT |
| `Z0002` | NOT_FOUND |
| `Z0003` | DUPLICATE_KEY |
| `Z0004` | FORBIDDEN |
| `Z0005` | STATE_CONFLICT |
| `Z0010` | TYPE_DISCRIMINATOR_MISMATCH |
| `Z0011` | TRANSACTION_REQUIRED |

Reserve `EXCEPTION WHEN OTHERS` for truly unexpected failures — don't use it as control flow. Catch specific conditions (`unique_violation`, `foreign_key_violation`, named SQLSTATEs) when you need to translate them.

For the full code catalog and EXCEPTION block patterns — read [Error Handling](references/error-handling.md).

## Cross-Table Constraints (Triggers Calling Functions)

Postgres `CHECK` constraints can't reliably reach across tables — functions in `CHECK` must be `IMMUTABLE`, but cross-table reads are not. Use `BEFORE INSERT/UPDATE` triggers that delegate to validation functions. **Triggers stay thin; functions hold all logic.**

    -- The function holds the validation logic
    CREATE OR REPLACE FUNCTION tg_savings_account_check_type()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM account
            WHERE account_no = NEW.account_no AND type = 'savings'
        ) THEN
            RAISE EXCEPTION 'savings_account requires account.type = ''savings'''
                USING ERRCODE = 'Z0010';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- The trigger is a one-liner that calls the function
    CREATE TRIGGER savings_account_must_be_savings_type
        BEFORE INSERT OR UPDATE ON savings_account
        FOR EACH ROW EXECUTE FUNCTION tg_savings_account_check_type();

This enforces at the schema level that a `savings_account` row can only reference an `account` with `type = 'savings'`. The database rejects invalid data.

**Use triggers + functions for:**

- Type discriminator enforcement across base/subtype tables
- Cross-table existence validation
- Business rules spanning multiple tables
- State machine transition validation
- Audit row generation

For full pattern — read [Cross-Table Constraints](references/cross-table-constraints.md).

## Base/Subtype Inheritance (PK Inheritance)

When entities share common attributes but have specialized ones, use **primary key inheritance** instead of polymorphic columns. A base table holds shared attributes and a type discriminator. Each subtype table inherits the base PK as both its PK and FK, plus a trigger enforcing the discriminator.

    CREATE TABLE savings_account (
        account_no account_no PRIMARY KEY,
        interest_rate growth_rate NOT NULL,
        min_balance money_amount NOT NULL,

        CONSTRAINT savings_account_is_account
            FOREIGN KEY (account_no) REFERENCES account(account_no)
    );

    -- Trigger enforces type discriminator (see Cross-Table Constraints)

**Avoid Postgres's `INHERITS` keyword** — it has FK and uniqueness gotchas. Stick with the explicit FK + trigger pattern.

For full pattern — base table setup, type discriminator triggers, referencing base vs subtype, inserting subtypes — read [Base/Subtype Inheritance](references/basetype-subtype.md).

## Hierarchical Composite Keys

Tables in a parent-child hierarchy use composite primary keys that grow wider as the hierarchy deepens. Each child inherits the full PK of its parent and adds its own discriminator:

    customer        (customer_no)
    order           (customer_no, order_no)
    order_line      (customer_no, order_no, line_no)
    order_shipment  (customer_no, order_no, line_no, shipment_no)

Use **per-parent SEQUENCEs** or keep max-plus-one functions if you prefer no sequences. Both work in Postgres.

For full pattern — sequence-per-parent, max-plus-one alternative, temporal children, sibling tables, insert procedures — read [Hierarchical Composite Keys](references/hierarchical-keys.md).

## Constraint Names as Predicates

Constraints read as natural-language statements about the relationship between entities, snake-cased:

    CONSTRAINT customer_rents_vehicle
        FOREIGN KEY (customer_no) REFERENCES customer(customer_no)

    CONSTRAINT savings_account_is_account
        FOREIGN KEY (account_no) REFERENCES account(account_no)

    CONSTRAINT customer_must_have_valid_email
        CHECK (email LIKE '%_@_%.__%')

    CONSTRAINT customer_email_is_unique
        UNIQUE (email)

`fk_rental_customer` describes the *mechanism*. `customer_rents_vehicle` describes the *meaning*. Constraint violations in error logs immediately tell you which business rule was broken.

## Role-Scoped Views

Views still earn their keep for flattening joins and projecting role-specific column sets. The `vw_role_intent` naming convention:

    vw_manager_team_report
    vw_admin_all_customers
    vw_customer_my_orders
    vw_worker_pending_jobs

The difference: **no in-view `current_user` filter** — RLS handles row filtering at the table layer. Views become pure projections.

For view templates and projection patterns — read [View Patterns](references/view-patterns.md).

## Relational Queues (FOR UPDATE SKIP LOCKED)

Postgres queue tables use `SELECT ... FOR UPDATE SKIP LOCKED` for atomic concurrent claim. Optionally augment with `LISTEN`/`NOTIFY` for low-latency wake-up.

    -- Worker claims and starts the next item atomically
    WITH claimed AS (
        SELECT job_id FROM job_queue
        WHERE status = 'pending' AND scheduled_for <= clock_timestamp()
        ORDER BY scheduled_for
        LIMIT 1
        FOR UPDATE SKIP LOCKED
    )
    UPDATE job_queue
    SET status = 'in_progress',
        started_at = clock_timestamp(),
        attempt_num = attempt_num + 1
    FROM claimed
    WHERE job_queue.job_id = claimed.job_id
    RETURNING job_queue.*;

For full queue patterns — table shapes, state machines, claim/report procedures, LISTEN/NOTIFY integration, max-attempts, queues as base/subtypes — read [Relational Queues](references/relational-queues.md).

## Soft Deletes

A `deleted_at timestamptz` column preserves the row in a "deleted" state so FK references still resolve and history queries still work. RLS policies filter `WHERE deleted_at IS NULL` for normal callers; admin/`BYPASSRLS` roles see all rows. **Make all uniqueness constraints partial** (`WHERE deleted_at IS NULL`) so the column can be reused after deletion. Use procedures (`pr_remove_*`, `pr_restore_*`) for the transitions so the timestamp and actor are captured consistently.

For FK cascade behavior, GDPR-driven hard delete, and integration with audit — read [Soft Deletes](references/soft-deletes.md).

## Auditing & History Tables

Every audited table gets a parallel `<table>_audit` capturing INSERT/UPDATE/DELETE with `before_data`, `after_data`, and `change_diff` (only the changed keys) — all `jsonb`. An `AFTER` trigger calls `tg_<table>_audit()` to write the audit row, using `to_jsonb(OLD)` / `to_jsonb(NEW)` for snapshots. A GIN index on `change_diff` makes "every change that touched the email field" cheap.

For the diff helper, retention/archival, performance mitigations, and system-versioned alternatives — read [Auditing & History Tables](references/auditing.md).

## Indexing Strategy

Five access methods: **B-tree** (default), **GIN** (arrays, jsonb, full-text), **GiST** (ranges, geo), **BRIN** (huge append-only), Hash (rarely useful). For composite indexes, equality columns first, ranges last. **Partial indexes** (`CREATE INDEX ... WHERE ...`) are nearly mandatory for soft-deletable tables and queue tables — they cut index size by orders of magnitude. **Covering indexes** (`INCLUDE (col1, col2)`) enable index-only scans for hot lookups. Default to "no index" — add when measurement justifies it.

For each access method, partial/expression/covering patterns, and maintenance — read [Indexing Strategy](references/indexing.md).

## Idempotent Migrations (Mostly Native)

Postgres has native `IF NOT EXISTS` for most DDL, dramatically reducing the meta-function library:

    CREATE TABLE IF NOT EXISTS customer (...);
    ALTER TABLE customer ADD COLUMN IF NOT EXISTS is_verified bool_false;
    CREATE INDEX IF NOT EXISTS customer_email_idx ON customer(email);
    DROP TABLE IF EXISTS old_customer;
    CREATE OR REPLACE FUNCTION ...;
    CREATE OR REPLACE PROCEDURE ...;

A small meta-function library is still useful for things Postgres doesn't natively guard:

- `fn_constraint_exists(table_name, constraint_name)` — for adding/dropping named constraints
- `fn_column_data_type(table_name, column_name)` — for type-change migrations
- `fn_policy_exists(table_name, policy_name)` — for RLS policy migrations
- `fn_trigger_exists(table_name, trigger_name)` — for trigger migrations

For migration templates and the slim meta-function library — read [Migration Patterns](references/migration-patterns.md).

## Reference Tables

When creating a reference (lookup) table, immediately seed it in the same DDL script using `ON CONFLICT DO NOTHING` for idempotency:

    CREATE TABLE account_type (
        type type_name PRIMARY KEY
    );

    INSERT INTO account_type(type) VALUES
        ('savings'),
        ('checking'),
        ('money_market'),
        ('certificate_of_deposit')
    ON CONFLICT DO NOTHING;

This ensures FK constraints referencing the table are immediately enforceable. A subtype table with `FOREIGN KEY (type) REFERENCES account_type(type)` won't accept any inserts until the reference data exists.

## Application Settings

A centralized `app_settings` table for runtime configuration — max retry attempts, feature flags, service endpoints, batch sizes:

    CREATE TABLE app_settings (
        param param_name PRIMARY KEY,
        val_bool BOOLEAN NOT NULL DEFAULT FALSE,
        val_int BIGINT NOT NULL DEFAULT 0,
        val_float DOUBLE PRECISION NOT NULL DEFAULT 0,
        val_str TEXT NOT NULL DEFAULT ''
    );

Each row is a named parameter using dot-separated namespaces (`notification.max_attempts`, `smtp.host`, `feature.email_enabled`). Functions read from the typed column wrapped in `COALESCE` with sane defaults so the system works even if a setting hasn't been configured.

Optionally augment with Postgres GUC custom params (`SET app.max_attempts = 3`) for session-scoped overrides.

For full pattern — read [Application Settings](references/application-settings.md).

## Useful Extensions

Enable extensions on demand with `CREATE EXTENSION IF NOT EXISTS <name>`:

- **pgcrypto** — `gen_random_uuid()`, password hashing (`crypt(...)` + `gen_salt('bf')`), symmetric encryption
- **citext** — case-insensitive text type (great for email)
- **pg_trgm** — fuzzy substring search with GIN indexes
- **pg_stat_statements** — per-query performance tracking
- **pg_cron** — in-DB scheduled jobs
- **pgvector** — vector embeddings for semantic search

For each extension's purpose and basic usage — read [Useful Extensions](references/extensions.md).

## Connection Pooling Caveats

Most production apps run **transaction-mode** pooling (pgbouncer, PgCat, RDS Proxy). In this mode the physical connection rotates between transactions, so:

- Session `SET` is lost — use `SET LOCAL` inside the transaction (including for RLS identity)
- `LISTEN`/`NOTIFY` doesn't work — needs session pooling
- Session-scoped advisory locks lost — use `pg_advisory_xact_lock`
- Prepared statements may be disabled by the pooler

For mode selection, RLS identity setup, and connection-count math — read [Connection Pooling Caveats](references/connection-pooling.md).

## Testing Patterns

Test against real Postgres — never mock the DB. Use **transactional isolation**: `BEGIN` before each test, `ROLLBACK` after, runs thousands per second. For RLS tests, `SET LOCAL ROLE` to a non-privileged role and assert what they see. For trigger tests, do the DML and assert the side effects. Match exceptions on **SQLSTATE**, not message text. Use **pgTAP** for schema and SQL-only unit tests; use your app's test framework for everything that crosses the boundary.

For fixture strategies, RLS test setup, procedure testing constraints, and CI configuration — read [Testing Patterns](references/testing.md).

## Normal Form Violations

Engine-agnostic theory; same patterns apply. The most damaging violation in practice is the **Relational Breach**: a child table with a `BIGSERIAL`/`IDENTITY` surrogate PK instead of a composite key including the parent's PK. Every table that does this severs itself from its ancestry — joins that should be direct require traversing every intermediate table.

For each violation: what it looks like in Postgres, why it's wrong, and the fix pattern — read [Normal Form Violations](references/normal-form-violations.md). For the theoretical foundation, see `relational-db-design`.

## Query Patterns

SARGable WHERE clauses matter. Window functions use standard SQL syntax. Postgres-specific patterns:

- `LATERAL` joins for per-row subqueries
- `DISTINCT ON` replaces `ROW_NUMBER() = 1` for "first row per group"
- Array operators (`ANY`, `ALL`, `@>`, `&&`) for set operations
- JSONB operators (`->`, `->>`, `@>`) for semi-structured data
- `INSERT ... ON CONFLICT` for upserts
- Parameter sniffing is rarely a concern; trust the planner

For the full Postgres-specific catalog — read [Query Patterns](references/query-patterns.md).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using bare `VARCHAR`, `INT`, `TIMESTAMPTZ` for columns | Always use a named DOMAIN — `email`, `account_no`, `ts_now` |
| Using `PascalCase` for identifiers | Use `snake_case` — Postgres folds unquoted identifiers to lowercase |
| Naming constraints `fk_table_othertable` | Use predicates: `customer_rents_vehicle` |
| Using `BIGSERIAL`/`IDENTITY` for child table keys | Use composite PKs that include the parent's PK |
| Forgetting `ON CONFLICT DO NOTHING` on reference seeds | Makes reseeding fail on rerun |
| Using views as security boundaries | Use RLS + `CREATE POLICY` at the table layer |
| Putting cross-table reads inside `CHECK` constraints | `CHECK` can't safely reach across tables — use `BEFORE` triggers calling functions |
| Putting DML inside trigger bodies directly | Triggers stay thin; call a function that holds the logic |
| Wrapping deterministic operations in `EXCEPTION WHEN OTHERS` | Reserve EXCEPTION for actual failure handling, not control flow |
| Nesting explicit transactions | Never `BEGIN` inside `BEGIN`. Use a nested `BEGIN ... EXCEPTION ... END` block (PL/pgSQL) or `SAVEPOINT` (client SQL) for selective rollback |
| `COMMIT`/`ROLLBACK` inside a block with an `EXCEPTION` clause | Fails at runtime. Let errors propagate to the caller's transaction; commit only in batch procedures, outside exception blocks |
| Using `Create`, `Update`, `Delete` as procedure verbs | Use `add`, `modify`, `remove` — avoid keyword collisions |
| Nullable columns by default | Define DOMAINs as `NOT NULL`; nullable only with explicit business reason |
| Hardcoding configuration in functions | Read from `app_settings` with `COALESCE` defaults |
| Wrapping columns in functions in WHERE clauses | Keep predicates SARGable — apply functions to parameters, not columns |
| Using `NOT IN` with a subquery | Use `NOT EXISTS` — `NOT IN` returns nothing if subquery contains NULL |
| Using `MERGE` | Use `INSERT ... ON CONFLICT` for upserts |
| Using `timestamp` (without timezone) for app data | Use `timestamptz` — always UTC at rest, convert at the read boundary |
| Storing dates as `timestamptz` at midnight | Use `date` when time-of-day doesn't matter |
| `now()` for "right now" inside a long batch | Use `clock_timestamp()` for real-time samples; `now()` returns transaction start |
| Plain `UNIQUE` constraint on a soft-deletable column | Partial unique index `WHERE deleted_at IS NULL` so values can be reused after delete |
| `FOR UPDATE` on every row read before update | Use `FOR NO KEY UPDATE` unless you're modifying key columns |
| `pg_advisory_lock` (session-scoped) inside a transaction-pool app | Use `pg_advisory_xact_lock` — auto-released, pool-safe |
| Session `SET app.user_id = ...` under transaction pooling | Use `SET LOCAL app.user_id = ...` so it scopes to the transaction |
| Mocking the database in tests | Test against real Postgres with transactional isolation — `BEGIN` per test, `ROLLBACK` after |
| Granting `SELECT` on a table without `USAGE` on its schema | Grant both, plus `ALTER DEFAULT PRIVILEGES ... GRANT SELECT ON TABLES` for future tables |
| Using `text` columns to store UUIDs | Use the `uuid` type — 16 bytes vs 37+ bytes for text |
| UUID v4 PK on a high-write table | Use UUID v7 (time-ordered) or `bigint` + `public_id uuid` hybrid |
| Computing `lower(email)` ad-hoc in queries | Add a `STORED` generated column or use `citext` |
| ENUM picked for a vocabulary that needs metadata or runtime additions | Use a reference table — ENUMs are hard to extend and can't carry extra columns |
| All tables in `public` schema | Split into `app`/`audit`/`ref`/`util` schemas for permission and lifecycle separation |
| Adding indexes speculatively | Add when `pg_stat_user_indexes` or EXPLAIN shows the need; every index costs writes |
