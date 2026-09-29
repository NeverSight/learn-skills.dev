---
name: designing-data-intensive-systems
description: "Use when workload or failure requirements drive storage, time-series, retention, partitioning, replication, stream-processing, consistency, recovery, or Postgres/Timescale decisions."
---

# Designing data-intensive systems

## Overview

Apply these domain constraints within the primary engineering or review skill. Start with the workload and operational guarantees; load references for the current decision.

## When to Use

- Choose among database, log, cache, queue, search, and analytical roles.
- Decide tradeoffs in consistency, partitioning, replication, or recovery.
- Compare batch, stream, and CDC designs.
- Plan Postgres or Timescale changes based on the actual workload.

## When Not to Use

- Keep `engineering` as the primary skill for ordinary implementation and refactoring.
- Use `engineering/references/boundary-design.md` for architecture questions confined to a module.
- Establish the workload shape before considering Postgres or Timescale details.

## Minimal Workflow

1. Describe the workload with concrete read, write, volume, latency, retention, ordering, and failure requirements where they apply.
2. Name each system role: source of truth, derived view, cache, queue or log, index, analytical store, and recovery path.
3. For an unresolved design decision, compare two or three viable options, including the simplest one, against the workload and correctness requirements. Keep a settled design unless new evidence invalidates it.
4. Identify the benchmark, failure test, migration proof, or operational observation that would decide the remaining uncertainty.
5. During implementation, apply these workload constraints within the primary `engineering` loop and stop when its verified completion criterion is met. Reuse proof that still covers the current code and relevant state.

## Reference Routing

- Read [FOUNDATIONS.md](FOUNDATIONS.md) to frame reliability, maintainability, and evolvability.
- Choose [PARTITIONING.md](PARTITIONING.md), [REPLICATION.md](REPLICATION.md), [TRANSACTIONS.md](TRANSACTIONS.md), [STREAM.md](STREAM.md), [BATCH.md](BATCH.md), or [DISTRIBUTED.md](DISTRIBUTED.md) according to the current design pressure.
- Read [POSTGRES_TIMESCALE.md](POSTGRES_TIMESCALE.md) once the question moves from architecture to Postgres or Timescale details.
- Read [TIMESCALE-API.md](TIMESCALE-API.md) when choosing Timescale API names or planning an upgrade; check the installed extension version first.
- Read [TIMESCALE-VALIDATION.md](TIMESCALE-VALIDATION.md) when validating a Timescale migration, storage policy, or query plan.
- Read [GLOSSARY.md](GLOSSARY.md) when an unfamiliar data-system term blocks the current decision.

## Failure modes

- Recommending a data store from habit rather than workload evidence.
- Treating caches, indexes, and sources of truth as interchangeable.
- Advising a Timescale migration before showing that the workload fits.
