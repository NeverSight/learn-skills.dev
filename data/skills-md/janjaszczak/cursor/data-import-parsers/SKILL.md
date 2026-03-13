---
name: data-import-parsers
description: Implement or refactor data import/parsing so it streams files sequentially (memory-safe), validates/coerces types explicitly, skips irreparable records while logging them to an error CSV (full original columns + timestamp/file/line/error), emits rows_ok/rows_skipped/parse_errors metrics, and guarantees idempotent DB writes.
metadata:
  author: janjaszczak
  version: "1.0"
---

# Data Import & Validation (Streaming + Error CSV + Metrics + Idempotency)

## When to use this skill
Use when working on:
- ETL / import pipelines (CSV/XLSX/JSON) into a DB
- Parsers that currently load whole files into memory
- Data validation/coercion, error isolation, auditability, and reproducibility
- Any import job that must be safe to re-run (idempotent)

## Non-negotiables (contract)
1) **Process input files sequentially** (no “load everything then insert”) to control memory.
2) **Validate and coerce types explicitly** (define allowed coercions; reject ambiguous cases).
3) **Irreparable records must be skipped and logged** to an error CSV containing:
   - all original columns exactly as seen in input
   - extra columns: `timestamp`, `file`, `line`, `error`
4) **Emit metrics** at minimum: `rows_ok`, `rows_skipped`, `parse_errors`.
5) **DB writes must be idempotent**: re-running the import must not duplicate or corrupt data.

## Standard workflow
### 1) Plan-first (before coding)
- Identify input formats, volume, and “row identity” rules (keys/dedup strategy).
- Locate current import entrypoints + DB write layer.
- Define:
  - schema mapping (source -> target columns)
  - validation rules per field
  - coercion rules per field (what is allowed, what is not)
  - error taxonomy (what counts as “irreparable”)

### 2) Streaming architecture
- Read **one file at a time**, **row by row** (or chunked) and write in bounded batches.
- Never accumulate full datasets in memory.
- Ensure progress logging is monotonic (e.g., file + row counters).

### 3) Validation & coercion
- Treat raw row values as immutable “source of truth”.
- Perform coercions in a controlled layer:
  - return `(ok, parsed_record)` or `(error, reason)` per row
- Separate concerns:
  - parsing (raw -> typed)
  - business validation (typed -> acceptable)
  - persistence (acceptable -> DB)

### 4) Error CSV logging
- On any irreparable row:
  - write **original row values** (unmodified)
  - add: `timestamp`, `file`, `line`, `error`
- Avoid partial writes that drop context; every skipped row must be explainable from the CSV alone.

### 5) Metrics
Maintain counters:
- `rows_ok`: successfully persisted rows
- `rows_skipped`: irreparable rows skipped
- `parse_errors`: count of parse/validation errors (can equal rows_skipped or be a superset if you track recoverable warnings separately)

Emit metrics:
- end-of-file summary
- end-of-run summary (aggregate over files)
Optionally persist metrics to a JSON or a DB table for observability.

### 6) Idempotent persistence
Pick and implement **one** clear strategy:
- Upsert by natural key / business key
- Insert with unique constraint + conflict handling
- Staging table + merge
- Per-file “ingestion ledger” (hash/checkpoint) + skip already-ingested files

Idempotency must hold across:
- reruns after crashes
- partial completion
- duplicate input files

## Review checklist (definition of done)
- [ ] Demonstrably streaming: memory does not scale with total rows.
- [ ] Every skipped record is present in error CSV with full context.
- [ ] Metrics are emitted and consistent with observed behavior.
- [ ] Re-running import on same inputs does not create duplicates (verified).
- [ ] Failures are isolated: one bad row/file does not poison the full run.
