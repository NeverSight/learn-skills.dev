---
name: indexer-core
description: VeChain indexer-core library — IndexerFactory, IndexerRunner, LogsIndexer vs BlockIndexer mode selection, ABI and business events, rollback semantics, and integration guidance.
allowed-tools: []
license: MIT
metadata:
  author: VeChain
  version: "0.1.0"
---

# Indexer Core Skill

## CRITICAL RULES

1. **Read reference files first.** When the user's request matches a topic in the table below, read those files before writing code, proposing architecture, or answering behavioral questions.
2. **Treat mode selection as a correctness decision.** `LogsIndexer` and `BlockIndexer` are not interchangeable. Do not present them as equivalent options with different performance profiles.
3. **Default to `IndexerFactory`.** For normal library usage, indexers should be configured and built with `IndexerFactory`, not by manually wiring implementation classes.
4. **Treat startup rollback as intentional.** It is part of the data-integrity model and reorg recovery workflow, not a bug.
5. **Prefer bundled references over ad hoc code spelunking.** If you are working inside the `indexer-core` repository, align with the local repo docs and `AGENTS.md`. Use source code mainly to confirm implementation details or debug discrepancies.

## Scope

Use this skill for `indexer-core` tasks such as:

- integrating the library into another service
- choosing between `LogsIndexer` and `BlockIndexer`
- configuring `IndexerFactory`, `IndexerProcessor`, and `IndexerRunner`
- designing ABI-event, VET-transfer, or business-event indexing setups
- debugging dependency ordering, fast sync, rollback, and reorg behavior
- changing the library itself while preserving documented behavior
- answering migration questions for 7.x to 8.x consumers

## Operating Procedure

### 1. Classify the task

Decide whether the user needs:

- **consumer guidance** for integrating or configuring the library
- **library maintenance** for changing `indexer-core` itself

For consumer guidance, optimize for correct mode selection and integration advice before discussing internals.

For library maintenance, preserve the documented contract unless the task explicitly changes that contract.

### 2. Read the matching references

Use the table below and load only the files needed for the current request.

### 3. Clarify the high-risk choices before implementing

Ask before building when any of these are unclear:

- whether the user needs full block access or only decoded events
- whether one indexer must finish a block before another processes it
- whether downstream consumers want raw ABI events or higher-level business events
- whether the task is a behavior change, a docs change, or a debugging task

### 4. Implement with indexer-core correctness

- build normal indexers through `IndexerFactory`
- assume repo docs are the authoritative description of public behavior
- keep rollback and reorg semantics intact unless the task explicitly changes them
- do not infer public contracts from a single implementation detail or type signature

### 5. Verify and deliver

A task is not complete until all applicable gates pass:

1. **Targeted verification** for the touched behavior
2. **Broader tests** with `./gradlew test` when the change is cross-cutting
3. **Formatting** with `./gradlew spotlessCheck` or `./gradlew spotlessApply` when Kotlin code changed
4. **Docs consistency** when public behavior or examples changed

## Reference Files

Read the matching files before doing anything else.

| Topic | File | Read when user mentions... |
|-------|------|---------------------------|
| Runtime model, lifecycle, rollback, dependencies | [references/runtime-model.md](references/runtime-model.md) | `IndexerProcessor`, `IndexerRunner`, lifecycle, status, rollback, reorg, dependency ordering |
| `LogsIndexer` vs `BlockIndexer` and factory choices | [references/mode-selection.md](references/mode-selection.md) | `LogsIndexer`, `BlockIndexer`, `includeFullBlock`, `dependsOn`, fast sync, full block access |
| ABI events, business events, VET transfers, filtering | [references/event-pipeline.md](references/event-pipeline.md) | ABI, business events, `VET_TRANSFER`, event criteria, transfer criteria, classpath JSON |
| Repo maintenance and migration | [references/maintenance-and-migration.md](references/maintenance-and-migration.md) | tests, formatting, docs authority, 7.x vs 8.x migration, `IndexingResult` renames |
