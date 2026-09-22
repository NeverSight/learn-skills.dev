---
name: ca-code-intel
description: >
  Discover available code-intelligence capabilities, select the best providers, fall
  back from index-based navigation to source exploration when needed, and produce the
  unified Code Atlas Fact Inventory (Fact + Relation + Evidence). Use as the factual
  code-discovery layer; do not perform business modeling.
---

# ca-code-intel

## Mission

Discover code facts reliably.

> Discover capabilities, not brands.

> Index is an accelerator, not a dependency.

> Fact discovery must not become business interpretation.


## Boundary with Semantic Canonicalization

Semantic Canonicalization is downstream of the Fact Layer.

References:

```text
../code-atlas/references/semantic-canonicalization-protocol.md
../code-atlas/references/semantic-identity-rules.md
```

Your responsibility is to preserve evidence fidelity:

```text
source/config/SQL/runtime-visible structure
→ Fact + Relation + Evidence
```

Do not turn similar technical facts into one business identity.

Do not decide that:

```text
two tables = one Business Object
two entry paths = one Scenario
two conditions = one Business Rule
```

Those decisions belong to the relevant semantic Owner Skill under the shared protocol.

Technical duplicate suppression is allowed only when it preserves the same observable source fact identity.

## Never do

Do not create:

- Business Domain
- Capability
- Scenario
- Process
- Sub-process
- Step
- Business Object
- Lifecycle
- business-level State Transition

Do not invent missing consumers/providers/callbacks.

## Provider discovery

Inventory available providers and capabilities such as:

```text
PROJECT_DISCOVERY
FILE_DISCOVERY
TEXT_SEARCH
SYMBOL_SEARCH
DEFINITION
REFERENCES
IMPLEMENTATIONS
CALLERS
CALLEES
TYPE_HIERARCHY
CALL_HIERARCHY
SOURCE_READ
CONFIG_READ
SQL_SEARCH
INDEX_QUERY
STRUCTURAL_SEARCH
```

Provider choice is based on:

```text
task requirement
+ capability
+ coverage
+ precision
+ cost
```

Multiple providers may be combined.

If providers disagree, verify against current source/config/SQL and prefer direct current evidence.

## Analysis modes

### Index Mode

Use definition/reference/implementation/caller/callee facilities to locate relationships quickly.

Verify critical results in current source.

### Source Exploration Mode

If no usable index exists or a needed artifact is not indexed, continue automatically using:

```text
workspace discovery
→ targeted search
→ source read
→ interface/implementation resolution
→ caller/callee reconstruction
→ Fact/Relation/Evidence
```

Do not stop because no index exists.

When useful, the orchestrator may mention CodeGraph as an optional accelerator:
`https://github.com/colbymchenry/codegraph`.

### Hybrid fallback

Index mode may locally fall back for XML/YAML/SQL/DDL or unindexed source.

Represent as:

```yaml
primary_mode: INDEX
fallback_used: true
```

## Discovery strategy

> Discovery seeks Coverage; Trace seeks Depth.

Breadth-first inventory:

1. Project / Module / bootstrap
2. Production entries
3. Outbound integrations
4. Data
5. State
6. Configuration
7. Async/event surfaces
8. External clients

Exclude typical build/IDE noise unless business-significant.

## Tests

Treat test code as auxiliary evidence only.

Recognize common test scopes such as:

- `src/test`
- `*Test`
- `*Tests`
- `*IT`
- fixtures/mocks/helpers

Use:

```text
production_scope: PRODUCTION | TEST | GENERATED
```

Tests must never become production entry or production chain facts by default.

## Fact Inventory

Use one common schema.

### Fact

Required logical fields:

```yaml
id:
category:
kind:
source_name:
scope:
location:
attributes:
evidence:
production_scope:
resolution:
```

Categories:

```text
STRUCTURE
CODE
ENTRY
INTEGRATION
DATA
STATE
CONFIG
```

Kinds include, as needed:

```text
PROJECT
MODULE
CLASS
METHOD
INTERFACE
HTTP_ENDPOINT
RPC_PROVIDER
RPC_CLIENT
MQ_PRODUCER
MQ_CONSUMER
MQ_TOPIC
JOB
EVENT_LISTENER
CALLBACK_ENDPOINT
HTTP_CLIENT
EXTERNAL_CLIENT
DATASOURCE
TABLE
COLUMN
MAPPER
REPOSITORY
SQL
STATE_FIELD
STATE_ENUM
STATE_VALUE
CONFIG_KEY
BUSINESS_SWITCH
ROUTE_CONFIG
CHANNEL_CONFIG
STRATEGY_CONFIG
```

Do not create business-specific technical kinds such as `SETTLEMENT_MQ_CONSUMER`.

### Relation

Use:

```yaml
id:
type:
from:
to:
attributes:
evidence:
```

Core relation types:

```text
CONTAINS
DECLARES
CALLS
IMPLEMENTS
TRIGGERS
PUBLISHES
CONSUMES
READS
WRITES
USES
DEPENDS_ON
MAPS_TO
```

Do not create target-specific variants such as `READS_TABLE`; the target Fact already identifies its type.

Conditions must retain exact code expressions where possible:

```yaml
condition:
  source_expression: "withdrawType == BANK"
```

Do not convert this at the Fact layer into an inferred business sentence.

### Evidence

Use durable anchors:

```yaml
id:
type: SOURCE | CONFIG | DATABASE | TEST | GENERATED
scope:
location:
range:
discovered_by:
```

Prefer:

- project
- module
- file
- symbol
- table
- field
- config key

Line ranges are secondary because they drift.

Index is normally `discovered_by`, not final semantic evidence.

## State rules

An enum proves candidate state values, not transitions.

A status write is represented as a Relation, for example:

```text
METHOD --WRITES--> STATE_FIELD
```

with a value attribute.

Do not infer `CREATED → PROCESSING` merely from seeing both values.

## MQ rules

Model:

```text
Producer Method --PUBLISHES--> MQ Topic <--CONSUMES-- Consumer Method
```

If no consumer is found, keep the continuation unresolved.

## RPC rules

Follow synchronous RPC to provider implementation when visible.

If provider code is unavailable:

- mark a verified external boundary when proven external;
- otherwise mark unresolved.

Do not invent provider behavior.

## Database rules

Discover method/repository/SQL/table relationships and actual READS/WRITES.

Pay special attention to:

- state fields
- amount/balance fields
- business records
- history/flow/log tables

Do not declare Business Objects from tables; that belongs to `ca-business`.

## External boundary

Record only code-visible interface/protocol/config/request/response facts.

Do not infer external internals.

## Resolution

Use:

```text
RESOLVED
PARTIAL
UNRESOLVED
```

`UNRESOLVED` means a continuation/target is known to exist but cannot be resolved in the visible source.

## Discovery completion gate

Do not equate completion with “read every file”.

Require coverage of major business-bearing surfaces:

```text
Project / Module
HTTP
RPC Provider / Client
MQ Producer / Consumer
Job
Callback / Listener
Tables
State
Config
External Client
```

Return a coverage matrix and unresolved count.

## Return contract

Return internal data equivalent to:

```yaml
result:
  status: FACT_DISCOVERY_COMPLETE | FACT_DISCOVERY_PARTIAL
  mode:
    primary: INDEX | SOURCE_EXPLORATION
    fallback_used: true | false
  coverage:
    structure: COMPLETE | PARTIAL
    entry: COMPLETE | PARTIAL
    integration: COMPLETE | PARTIAL
    data: COMPLETE | PARTIAL
    state: COMPLETE | PARTIAL
    config: COMPLETE | PARTIAL
  unresolved_count:
  fact_inventory:
    facts: []
    relations: []
    evidence: []
    unresolved: []
```

This output is Analysis Workspace data, not Canonical Markdown.
