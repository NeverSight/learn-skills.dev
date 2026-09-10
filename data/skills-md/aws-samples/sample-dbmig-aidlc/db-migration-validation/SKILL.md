---
name: db-migration-validation
description: Validation & Testing phase of an AI-DLC database migration. Use after Construction is approved, or when the user asks to validate, test, reconcile, or verify a database migration — to prove the converted target behaves the same as the source. Loads test data (one-time load via dbmig for dev/test, or consumes data already loaded via AWS DMS), reconciles row counts, and runs LLM-generated equivalence tests for functions/procedures/packages — same input → same return value (functions) and same net effect (procedures) — executed inside a rolled-back transaction. You (Kiro) generate the test specs from sampled real data. Failures are logged for follow-up (silent mode) or prompted (interactive mode). Writes artifacts to migrations/<project>/03-validation/.
---

# Validation & Testing — Equivalence

This is the **Validation** phase. Prove that *same input → same value* (functions/queries)
and *same input → same net effect* (procedures/DML) between source and target. The
methodology is in `engines/<pair>/checks/equivalence-spec.md` (substitute the active
engine pair, e.g. `oracle-to-postgresql` or `sqlserver-to-mysql`, derived from the
connection engines).

Conversion-style hand-off: `dbmig` does the deterministic work (sample data, run tests,
compare, report); **you (Kiro) generate the test cases** from real data.

## Run mode & follow-up (applies to this whole phase)
Per `migration-config.yaml run.mode` (or `--mode`):
- **silent** (default): any test/reconcile failure is recorded to
  `migrations/<project>/follow-up.yaml` (+ `follow-up.md`) and the run **continues** — never
  blocks. Summarize open follow-up items at the end for later human resolution.
- **interactive**: also prompt for input/correction; failures surface via a non-zero exit.

## Step 1 — Get data into the target
Per `migration-config.yaml testing.data_load`:
- **`framework`** (dev/test): `python -m dbmig migrate-data --schema <S> --workers 8 --project <P>`
  - **Method** (`testing.data_method`, or `--method`): `toolkit` (default) pulls rows through
    this host and `COPY`s into the target; **`fdw`** makes the target PostgreSQL read directly
    from the source via a foreign data wrapper (`oracle_fdw`/`tds_fdw`) so data moves
    source→target **server-side** — use it when the toolkit host is on-prem across a slow VPN
    while source and target are both in the cloud (PostgreSQL target only). FDW objects are
    dropped after the load by default (the user mapping stores the source credentials); pass
    `--fdw-keep` to retain them and `--fdw-cleanup` to remove them later:
    `python -m dbmig migrate-data --schema <S> --method fdw --shards 16 --workers 16 --project <P>`
- **`dms`** (prod/large): the user runs AWS DMS externally; confirm the target is populated.

## Step 2 — Apply deferred foreign keys + triggers
```bash
python -m dbmig apply-schema --schema <S> --project <P> --post-data
```
Construction deferred `FOREIGN KEY` constraints and triggers; apply them **now that the data
is loaded** (enforced FKs would otherwise dictate load order, and row triggers would rewrite
loaded data). Writes `02-construction/apply_report_postdata.yaml`; the same automated
error-retry loop applies. This is a **gated** target write — confirm before running.

## Step 3 — Reconcile data (row counts)
```bash
python -m dbmig compare --schema <S> --project <P>
```
Writes `03-validation/reconcile_report.yaml`. Mismatches are logged to the follow-up file
(silent) or surfaced (interactive).

## Step 4 — Generate equivalence tests from REAL data (you do this)
```bash
python -m dbmig gen-tests --schema <S> --project <P>
```
`gen-tests` extracts callables (functions, procedures, packages), **samples real rows** from
the source, and writes a prompt bundle per object to `03-validation/test_prompts/` plus
`test-manifest.yaml`. Then, for each `pending` unit, **you generate a test spec**:
- Read the prompt bundle (it includes the source code + the sampled real data + the required
  spec format).
- Write a `.test.yaml` to the unit's `spec_file` (`03-validation/tests/<S>/<obj>.test.yaml`)
  using **only real values from the sample** so tests hit rows that exist.
- For **functions**: cases with `source_sql`/`target_sql` whose return value is compared.
- For **procedures**: choose probe queries that capture the procedure's effect; the runner
  snapshots each probe **before and after** the call on both engines and compares the
  **delta** (net effect). This is where you decide *how to verify* the net result.
- Set the unit's `status` to `generated` in `test-manifest.yaml`.

## Step 5 — Run the tests (txn + rollback)
```bash
python -m dbmig run-tests --schema <S> --project <P>
```
Each case runs on **both engines inside a transaction that is rolled back** afterward — real
data, real writes, but non-destructive. Functions compare the return value; procedures
compare before/after deltas per probe (tolerance/normalization from
`testing.equivalence`). Results go to `03-validation/equivalence-report.yaml` (+ `.md`).
Failures are logged to the follow-up file (silent) or prompted (interactive).

> Caveat: if a procedure issues its own `COMMIT`, rollback cannot undo it — flag such
> procedures and test them only against a disposable target.

## Step 6 — Triage
- **silent**: present the open follow-up items (conversion failures from Construction +
  test/reconcile failures here) as the to-do list; the run did not block.
- For each failure, link to the converted object and the relevant playbook reference; the
  fix loops back to `db-migration-construction` (re-convert), then re-run the affected tests.

## Gate
Summarize pass/fail counts and open follow-up items. **Stop at the gate: "Approve the
equivalence test results?"** Proceeding with open follow-up items is allowed (silent mode)
but must be explicitly acknowledged. On approval, hand off to `db-migration-operations`.

## Safety
- Test data loads and procedure tests write to the target — gated actions. Prefer a
  dedicated test schema/database; never run net-effect procedure tests against a populated
  production target.
