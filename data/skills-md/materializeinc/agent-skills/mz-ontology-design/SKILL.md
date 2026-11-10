---
name: mz-ontology-design
description: >-
  Designing and reviewing the semantic layer of a Materialize SQL code
  base as a canonical ontology — a shared raw database, a shared core
  database, and one database per use case. Use this skill when a user
  asks how to structure or organize Materialize schemas and databases,
  wants to define canonical semantic objects (entities, events,
  measurements, relationship objects), needs identity resolution or
  temporal semantics for public objects, is deciding what belongs in a
  shared layer versus a consumer-specific one, is building or
  validating a relationship registry (core.public.relationships,
  reference edges, cardinality, optionality), or mentions ontology,
  semantic layer, semantic model, semantic objects, context graph,
  raw/core/use-case boundaries, grain, or enforceable layer
  dependencies. Also trigger when reviewing an existing Materialize
  code base for leaked private schemas, duplicated concepts, or
  undocumented public objects.
---

# Materialize ontology design

Build one canonical semantic graph between source-shaped data and consumer-specific
outputs. Shared meaning belongs in the ontology; presentation and workflow policy
belong at the edges.

## Architecture

Use a shared `raw` database, a shared `core` database, and one database per use case.
Preserve this dependency direction:

```text
raw.<source_system>  ->  core.<source_system>  ->  core.internal
                                                    |
                                                    v
                                               core.public
                                                    |
                                                    v
                                         <use_case>.<schema>
```

- `raw` contains source-shaped ingestion objects. Preserve source-table identity;
  recreating a source table can resnapshot the upstream system.
- `core.<source_system>` contains private, source-local typing, cleanup,
  deduplication, and naming.
- `core.internal` contains private cross-source integration and identity resolution.
- `core.public` is the documented ontology and the only core schema consumers may
  read.
- Each use case owns a database. Its schemas contain the projections, aggregates,
  scores, filters, and indexes for that application or workload. Use cases never
  share a database.

Only `core` reads `raw`. Every use-case database reads only `core.public`. Enforce
these boundaries with grants and dependency validation rather than naming conventions
alone.

## Semantic objects

A semantic object is a canonical relation whose rows have one documented grain, one
durable identity rule, explicit temporal semantics, and meaning independent of any
consumer. It represents one of:

- an entity: a durable thing with identity;
- an event: an occurrence with event identity and event time;
- a measurement: an observation at a subject, metric, and observation time; or
- a relationship object: an association with attributes, evidence, history, or
  many-to-many meaning.

An aggregate, score, display category, report row, source replica, or one-to-one
projection is not a semantic object merely because a consumer needs it.

Before adding a public object, require all of the following:

1. Its grain and identity can be stated unambiguously.
2. Its meaning does not depend on a particular dashboard, alert, model, or workflow.
3. It is useful to multiple consumers or foundational to another public object.
4. Its attributes belong at the same grain, have clear provenance, and are safe to
   expose through the public boundary.

If a use case needs missing data, first decide whether to add an attribute to an
existing object, add an event, measurement, or relationship object, or keep a
consumer-specific derivation at the edge. Never bypass the private boundary.

## Identity and time

Prefer immutable upstream identifiers when they are globally meaningful. Use explicit
composite keys when identity is scoped by a parent. Resolve cross-source identity once
in `core.internal` and retain source identifiers for lineage. Use a deterministic
synthetic identifier only when no durable key exists; document its inputs and stability
boundary.

Do not publish warehouse sentinel members or duplicate surrogate hashes beside the
keys they encode. Represent unresolved, unmatched, ambiguous, and resolved states
explicitly when those distinctions matter.

Every public object declares whether it represents current state, an immutable event,
a point-in-time measurement, or effective-dated history. Distinguish event time,
effective time, and ingestion time when more than one affects interpretation.

## Public and use-case objects

Define each `core.public` semantic object exactly once, name it with a domain noun,
and publish it as a materialized view on transformation compute. This lets serving
clusters consume maintained results without rebuilding the semantic graph.

Normalize shared meaning: one fact has one canonical owner. A denormalized copy is
acceptable only when its derivation is canonical and its relationship documentation
identifies it as denormalized.

Use-case databases may organize their surfaces into one or more schemas and reshape
the ontology into stars, wide tables, cohorts, rankings, scores, or alert states. They
may not redefine identity or maintain an independent version of a shared concept.
Transformation compute and serving compute remain separate; serving workloads may
share a cluster when their ownership, isolation, sizing, and availability requirements
are compatible.

## Relationships

Use two relationship forms:

- A reference edge is represented by columns on one public object that identify one
  row in another public object. Its cardinality from the referencing side is
  `many_to_one` or `one_to_one`.
- A relationship object is a public semantic object when the association has
  attributes, time, evidence, confidence, or many-to-many meaning. Its references to
  participating entities are ordinary reference edges.

Do not expose heuristic matches as foreign-key-like edges. Model the match as a
relationship object with its method, status, evidence, confidence, and effective time.

`core.public.relationships` is the machine-readable registry of all reference edges.
Read `references/relationships.sql` when creating or reviewing it. Composite references
list columns positionally and must be either wholly null or wholly non-null when
optional.

Validate the registry against the compiled schema: relationship names are unique;
objects and columns exist; column counts and types match; referenced columns form a
unique key; required references have no nulls or orphans; one-to-one references are
unique on the referencing side; enums are valid; and every public reference is
registered.

## Documentation and tests

Use `comment on` for the consumer contract. Each public object documents its grain,
identity, temporal behavior, meaning, and important exclusions. Comment keys,
timestamps, units, state fields, nullable relationships, sensitive fields, and
non-obvious derivations. Include semantic provenance when it affects interpretation;
exclude source mechanics, join implementation, and performance notes.

Keep implementation notes in SQL comments. Test public key uniqueness and non-nullness,
accepted states, relationship integrity, grain preservation, and non-obvious semantic
rules. CI should also reject reverse-layer dependencies, private-schema access by
use-case databases, undocumented public objects, and consumer indexes on
transformation compute.
