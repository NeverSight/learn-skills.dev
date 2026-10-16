---
name: pythia-table
description: Use when creating or changing a table, column, constraint, index, sequence or comment - "add a column", "create a table for X", "them cot", "tao bang", "sua kieu du lieu", "comment cho cot", a migration script, or a column type change. Designs the DDL to the house standard and Oracle practice, documents every table and column with COMMENT ON, and lands it through pythia deploy with the honest rollback.
---

# Tables, Columns, Comments

**Announce at start:** "Using pythia-table — reading the table and its neighbours before designing DDL."

**Phase:** Learn → Ask → Do — the table as it is, the decisions that are the developer's, then one ordered script

A table outlives every program that reads it. Its columns are a contract
with every report, interface and procedure in the schema, and structural DDL
has almost no undo: `DROP COLUMN` is permanent, a renamed column breaks every
caller at once. Five minutes of design is the cheapest step there is.

## The Iron Law

```
NO TABLE OR COLUMN WITHOUT ITS COMMENT, ITS CONSTRAINTS AND ITS IMPACT KNOWN
```

## The Workflow

1. **Learn the table and its neighbours.**
   - `pythia cols T` · `pythia comments T` · `pythia stats T` — what exists,
     what is documented, which foreign keys lack an index.
   - `pythia impact T` before any ALTER — every program that recompiles.
   - `pythia similar T_<NAME>` and `pythia ddl TABLE <NEIGHBOUR>` — how this
     house already builds tables: PK style, audit columns, tablespace,
     naming. Read `.pythia/conventions.md` and `pythia conventions`.
2. **Ask what is the developer's** (through `pythia-spec`): what is kept or
   deleted, nullability of existing rows and the backfill value, retention,
   who writes the table (an API package, a trigger, an interface), identity
   column vs sequence when the house has no rule. Never invent a business
   default for a NOT NULL column.
3. **Write one ordered script** — `reference/ddl-standards.md` has the
   template and the datatype rules:
   - name every constraint (`PK_`, `FK_`, `UK_`, `CK_` unless the house says
     otherwise); a primary key on every table; an index on every FK column;
   - text as `VARCHAR2(n CHAR)` — a Vietnamese character can take 3 bytes;
     money as `NUMBER(p,s)`, never FLOAT; `DATE` or `TIMESTAMP` by need;
   - `COMMENT ON TABLE` and `COMMENT ON COLUMN` for **every** new table and
     column: meaning, unit, allowed values, source. Vietnamese is fine here
     — `COMMENT ... IS` takes a literal only (no `unistr`), and pythia sends
     UTF-8 exactly; `pythia doctor --db` warns if the character set cannot
     hold it.
4. **Lint it**: `pythia lint script.sql comments.sql` (one run, so the
   comments file counts) — missing comments, unnamed
   constraints, unindexed FKs, `ADD ... NOT NULL` without a default,
   byte-semantics text, missing house columns. Errors are fixed, not argued.
5. **Land it** with `pythia-deploy` (`pythia deploy script.sql`): every
   statement previewed, one approval, run in order, stopped at the first
   failure. A single statement can go through `pythia apply` as usual.
   `structural` is `deny` by default — relay the refusal; the developer
   decides (`pythia policy set structural confirm`, or an autopilot lease
   naming `structural`).
6. **Verify** (`pythia-verify`): `pythia cols T`, `pythia comments T` (0
   missing), `pythia invalid` against the baseline.

## Changing a live table — expand, then contract

| Change | Safe shape |
|---|---|
| New mandatory column | `ADD (c ... DEFAULT <agreed> NOT NULL)` — one step, metadata-only on 12c+. No agreed default → add nullable, backfill (`data_dml`), then `MODIFY c NOT NULL`. |
| Rename | Never in place on a shared schema: add the new column, copy, move the callers, drop the old one later — a separate, destructive approval. |
| Type change | Widening (`VARCHAR2(50)` → `(100)`) is in place; anything narrowing or converting: new column, copy, swap. |
| New FK on existing data | `ENABLE NOVALIDATE` first, clean the rows, then `VALIDATE` — and the index before the constraint. |
| Drop | Destructive: its own preview, its own approval, never inside an autopilot lease unless the card said so. Check the Recycle Bin is on and never add `PURGE` without being asked. |

Big tables (millions of rows): `ALTER TABLE ... ADD` with a default is
metadata-only, but `MODIFY`, index builds and backfills are not — ask about
a window, and `ONLINE` index builds need Enterprise Edition. Partitioning
and compression are separately licensed options: name that before
proposing them.

## Is rollback real?

| Statement | Undo |
|---|---|
| `COMMENT ON` | **Yes** — the previous comment is snapshotted; `pythia journal restore <entry>`. |
| `CREATE TABLE / INDEX / SEQUENCE` | A `DROP` — structural, written by hand, approved like any write. |
| `ALTER TABLE ADD` | `ALTER TABLE ... DROP COLUMN` — the data written since is lost. |
| `DROP`, `TRUNCATE`, `SET UNUSED` | **No.** Flashback is a DBA's job, if retention allows it. |

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "Comments later, once it works" | Later never comes; the dictionary is the only documentation that survives. Same script. |
| "The FK index is an optimisation" | Without it, deleting a parent locks the whole child table. It is correctness under load. |
| "VARCHAR2(100) is plenty" | 100 bytes is ~33 Vietnamese characters in AL32UTF8. Say `CHAR`. |
| "I'll default the NOT NULL column to 0" | That is a business decision made silently. Ask. |
| "Rename is one statement" | And one broken caller per reference. Expand, then contract. |
| "The table is new, impact is zero" | Say so with `pythia impact` as evidence — then it is a fact, not a guess. |

## When NOT to use this skill

- Changing code that reads the table → `pythia-write` / `pythia-package`.
- A slow query on an existing table → `pythia-tune` (an index is still
  designed here once tuning asks for it).
- Data fixes (`UPDATE`/`DELETE`) → `pythia-apply`; they are `data_dml`.
