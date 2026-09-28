---
name: database-engineering
description: >-
  Design, implement, or review application database behavior: data models, schemas, identifiers,
  constraints, transactions, queries, and indexes. Use when correctness depends on relational or
  persistent-data invariants and access patterns. Respect the database already selected by the
  project; provider-specific specialists may refine implementation but must not replace the
  architecture by default. Route cross-version/coexistence transitions to migration-engineering.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Database Engineering

Model persistent truth from invariants and access patterns, not from ORM convenience.

## Workflow

1. Inspect the existing database engine, schema/migrations, repository/data-access conventions, and actual workload.
2. State the invariants and authority of the data before choosing tables/collections, keys, or abstractions.
3. Model identity, ownership, cardinality, lifecycle, nullability, uniqueness, and referential constraints explicitly.
4. Define transaction boundaries from atomic business invariants.
5. Derive indexes and query shapes from real access patterns and ordering/filter requirements.
6. Consider concurrency and isolation only to the depth required by the invariant; do not add locks or serialization without a concrete race.
7. Use engine-specific features only after the project engine is known. A specialist provider can help with syntax/tuning, not silently choose the engine.
8. If existing data, old code, or multiple deployed versions must coexist during change, report a migration-engineering concern.

## Stop

Stop when persistent invariants, transaction boundaries, and important query/access behavior are explicit and have sufficient evidence. Do not turn ordinary application modeling into enterprise data architecture.
## Reference Guide

Load only the references needed for the current task:

- [data model](references/data-model.md)
- [query index](references/query-index.md)
- [transactions](references/transactions.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [authority](references/_shared/state/authority.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
