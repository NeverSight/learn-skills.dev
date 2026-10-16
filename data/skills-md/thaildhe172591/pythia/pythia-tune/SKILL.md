---
name: pythia-tune
description: Use when a query, report or PL/SQL unit is slow, before adding an index or a hint, or when someone says "cham", "toi uu truy van", "optimize this query", "why is this report slow", "full table scan". Measures with the optimizer's own plan and statistics, changes one thing at a time, and proves the gain with the same measurement - license-safe, no AWR/ASH or Tuning Pack.
---

# Tuning a Query or a Unit

**Announce at start:** "Using pythia-tune — measuring before changing anything."

**Phase:** Learn → Ask → Do — the plan and the statistics first, one proposed change, the same measurement after

Performance folklore is the most confident kind of wrong. "Add an index",
"use a hint", "rewrite it as a join" — each is right for some plans and
harmful for others, and only the plan says which. Tuning without a before
and after is guessing with extra steps.

## The Iron Law

```
NO TUNING CHANGE WITHOUT A MEASUREMENT BEFORE AND THE SAME ONE AFTER
```

## The Workflow

1. **Get the real statement.** The exact SQL the application runs — from
   `pythia src` / `pythia grep`, with its bind variables as binds (`:id`),
   not pasted literals: a literal can get a different plan than the bind.
2. **Measure.**
   - `pythia explain "<the select>"` — the optimizer's plan; read rows
     (cardinality), cost, the access path per table, and the `-- note:`
     lines pythia adds (full scans, Cartesian joins, implicit conversions,
     dynamic sampling).
   - `pythia stats <TABLE>` for each table in the plan — row counts, when
     statistics were gathered, STALE, the indexes and their columns,
     unindexed foreign keys.
   - For DML, explain the `SELECT` that finds its rows.
3. **Diagnose with the checklist** (`reference/tuning-checklist.md`), in
   order — cheapest and most common causes first: statistics, a predicate
   that cannot use an index, the wrong or missing index, join shape, then
   PL/SQL row-by-row work. Name the cause in one sentence with the plan line
   that proves it.
4. **Propose ONE change** with its expected effect on the plan, and its
   cost: an index slows every write on that table and is a `structural`
   change (designed with `pythia-table`); a rewrite changes code
   (`pythia-write`, impact first). Gathering statistics on a shared schema
   is the DBA's or owner's call — say so, do not run it.
5. **Apply it** through the normal doors — `pythia apply` / `pythia deploy`
   — never a hint or an index created by hand.
6. **Measure again** with the exact step-2 commands, and report before vs
   after: plan shape, cost, cardinality. If it did not improve, say so and
   revert — a change that did not help still costs.

## What this kit can and cannot measure

- `explain` is EXPLAIN PLAN + `DBMS_XPLAN.DISPLAY`: the **estimated** plan,
  license-safe. The plan actually used at runtime can differ (bind peeking,
  adaptive plans) — `DBMS_XPLAN.DISPLAY_CURSOR` needs `V$` access, and AWR,
  ASH and the SQL Tuning Advisor need the Diagnostics/Tuning Pack licences.
  Never use or recommend them without the developer confirming the licence.
- Real timings: `pythia sql "<select>"` runs a query; wrap it in your shell's
  `time` for a rough number, on a dev schema, and say it is rough.

## The usual causes, by frequency

| Symptom in the plan | Usual cause | Usual fix |
|---|---|---|
| Rows estimate far from reality, "dynamic statistics used" | missing or stale statistics | ask the owner to gather stats (`DBMS_STATS`) |
| `TABLE ACCESS FULL` on a large table with a selective predicate | function or implicit conversion on the indexed column, leading `%` in LIKE, no index | rewrite the predicate to be sargable; then consider an index |
| `INTERNAL_FUNCTION`, `TO_NUMBER("COL")` in the predicates | comparing a VARCHAR2 column to a number, DATE to a string | compare like types; `TO_DATE` with a format on the literal side |
| `MERGE JOIN CARTESIAN` | a missing join predicate | add it |
| `FILTER` with `NOT IN` | nullable column under NOT IN | `NOT EXISTS` |
| A fast query called thousands of times | row-by-row PL/SQL, a function per row in SQL | one set-based statement; `BULK COLLECT LIMIT` + `FORALL`; scalar subquery caching; `RESULT_CACHE` for stable lookups |
| Many child cursors, parse time high | literals instead of binds in dynamic SQL | bind variables (`USING`) |

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "Just add a hint" | A hint freezes today's plan against tomorrow's data. Fix the cause; hints are a last resort the developer approves. |
| "An index will fix it" | Only if the predicate can use it — and it taxes every write. Prove it with the plan. |
| "It's slow, so it's the database" | The plan says whether it is the SQL, the data, or the 10,000 calls around it. |
| "I'll gather stats myself" | On a shared schema that changes every plan for everyone. The owner's call. |
| "It feels faster" | Same measurement, before and after, or it did not happen. |
| "Let me check AWR" | Licensed. Ask first. |

## When NOT to use this skill

- The code is wrong, not slow → `pythia-review`.
- Designing the index the diagnosis asked for → `pythia-table`.
- Writing the rewritten PL/SQL → `pythia-write` (after `pythia-impact`).
