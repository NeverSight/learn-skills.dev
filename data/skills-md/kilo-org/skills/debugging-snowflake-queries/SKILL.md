---
name: debugging-snowflake-queries
description: This skill should be used when a user needs help debugging a Snowflake SQL query, understanding a Snowflake query failure, isolating incorrect results, fixing joins or filters, diagnosing performance problems, or turning a vague warehouse error into a concrete root cause and corrected query. It is a standalone Snowflake query debugging skill for ad hoc SQL work across databases, schemas, and environments.
license: MIT
metadata:
  category: development
---

# Debugging Snowflake Queries

Debug Snowflake SQL systematically: reproduce the failure, classify the problem, isolate the smallest failing unit, verify grain and joins, and only then rewrite the query.

## When to Use

- Diagnose Snowflake errors such as `SQL compilation error`, `invalid identifier`, `object does not exist`, `ambiguous column`, cast failures, permission failures, or timeouts
- Debug queries that run but return the wrong count, duplicate rows, empty results, stale-looking data, or impossible percentages
- Investigate performance problems such as long scans, warehouse issues, or unexpectedly expensive joins
- Review an ad hoc SQL query and explain how to make it correct and reproducible

## Do Not Use For

- Template or application-layer SQL generation failures where no Snowflake SQL is actually being debugged
- General business investigations where the main task is answering the question rather than debugging the query itself

## Workflow

1. Reproduce the exact failing query or reconstruct the smallest equivalent query.
2. Classify the issue before changing SQL:
   - compile/name-resolution
   - permissions/environment
   - type/cast/null semantics
   - join/grain/result correctness
   - performance/scan/warehouse
   - stale or incomplete upstream data
3. Reduce the query to the smallest failing component:
   - one CTE at a time
   - one join at a time
   - one computed expression at a time
   - one filter at a time
4. Verify object existence, schema, and exact column names before assuming anything.
5. State the grain of each input and intermediate result explicitly.
6. Validate counts and null rates around every join boundary.
7. When a query is logically wrong but syntactically valid, prove the failure mode with a targeted counterexample or diagnostic query.
8. Only after isolating the root cause, rewrite the full query.

## Core Rules

- Prefer minimal diagnostic queries over speculative rewrites.
- Keep each debugging step falsifiable: each query should answer one question.
- Never assume two tables can be joined just because they share similarly named IDs.
- Treat row explosion as a grain mismatch until proven otherwise.
- Treat zero rows as a filter, time-window, or join-key problem before blaming missing data.
- Treat surprising percentages as denominator scope problems before blaming arithmetic.
- Use fully qualified names when working outside dbt macros or when environment ambiguity is possible.
- Check for soft-delete columns and freshness/ingestion timestamps when backend mirrors are involved.
- For large fact tables, tighten the date filter first and inspect scan behavior before running broad diagnostics.

## References

Load these references as needed:

- `references/debugging-playbook.md`
  Use for the end-to-end workflow, diagnostic query templates, and how to narrow a failure.
- `references/error-taxonomy.md`
  Use to map common Snowflake error messages to likely causes and next checks.
- `references/result-correctness-checklist.md`
  Use when the query runs but results look wrong: duplicates, drops, denominator mistakes, stale data.
- `references/query-patterns-and-failure-modes.md`
  Use for concrete warehouse-agnostic examples of common failure modes and how to correct them.

## Expected Output

When returning a debugging answer:

1. State the likely root cause in one sentence.
2. Show the minimal diagnostic evidence.
3. Provide the corrected query or exact fix.
4. Note any remaining assumptions, especially around grain, environment, or upstream freshness.
