---
name: ca-project
description: >
  Build the Code Atlas technical foundation from verified Fact Inventory: System,
  Project, Module, production entries, dependencies, integrations, and physical
  references. Use when mapping repository/workspace structure without inventing
  business domains from technical layout.
---

# ca-project

## Mission

Own the technical map:

```text
System / Workspace
  ↓
Project / Repository
  ↓
Module
  ↓
Component / Entry / Integration / Data reference
```

The output is a technical foundation for higher-level business modeling.

## Ownership

You own:

- System
- Project
- Module
- Technical topology
- Production Entry inventory
- Technical dependency references
- Physical reference inventories

You do not own:

- Business Domain
- Capability
- Business Object
- Lifecycle
- Scenario
- Process
- Execution Chain semantic definition

You may discover evidence relevant to them, but only propose it to the owner.


## Canonicalization boundary

Use the shared protocol only for technical identity normalization needed by owned entities:

```text
../code-atlas/references/semantic-canonicalization-protocol.md
```

For System / Project / Module:

- deduplicate technical aliases only with evidence;
- preserve repository/module identity;
- do not convert technical structure into business semantics;
- do not infer Domain identity from structural similarity.

Business-semantic canonicalization remains with the appropriate business Owner Skill.

## Inputs

Consume `ca-code-intel` Fact Inventory, especially:

```text
STRUCTURE
CODE
ENTRY
INTEGRATION
DATA
CONFIG
CONTAINS
DECLARES
DEPENDS_ON
CALLS
IMPLEMENTS
PUBLISHES
CONSUMES
```

Use current repository metadata and source when needed to resolve structure.

## Core rule

> Project structure is not business structure.

Never infer a Business Domain merely from:

- repository name
- module name
- package name
- Maven artifact name
- service name

Those can be signals, never sufficient proof.

## Analysis Workspace Root

Consume the `Analysis Workspace Root` resolved by `code-atlas`.

The root is the publication scope for the complete Atlas, not a signal that every sibling directory must be analyzed.

Keep these concepts separate:

```text
Analysis Workspace Root
= where the one Canonical Atlas is published

Selected Project Set
= which repositories/projects are actually analyzed
```

For a single project:

```text
emp-account/
├── src/
└── docs/code-atlas/
```

For multiple selected projects:

```text
settleWork/
├── emp-account/
├── site-account/
└── docs/code-atlas/
```

Do not create one `docs/code-atlas/` per Project for a single multi-project analysis.

Project-specific technical documents are represented inside the shared Atlas:

```text
<analysis-workspace-root>/docs/code-atlas/projects/
├── emp-account.md
└── site-account.md
```

## Multi-project model

Treat selected repositories as one technical workspace when relevant.

Maintain technical continuity:

```text
System
├── Project A
│   ├── Module A1
│   └── Module A2
├── Project B
└── Project C
```

Do not cut a synchronous relationship just because it crosses projects.

Do not infer that every repository under the workspace root belongs to the analysis; only selected/in-scope Projects do.

## Module classification

When code facts support it, classify module responsibilities such as:

```text
api
domain
service
application
infrastructure
entry
shared
client
```

Classification describes technical role only.

Do not promote `shared/common/util` into business domains.

## Production Entry inventory

Record production triggers such as:

- HTTP endpoint
- RPC provider
- MQ consumer
- Job / scheduled task
- Event listener
- Callback endpoint

Tests are excluded from the production entry map.

## Integration inventory

Record:

- RPC clients/providers
- MQ producers/consumers/topics
- HTTP clients
- external SDK/client
- datasource boundaries

Do not describe external-system internals that are not visible.

## Physical references

Own `docs/code-atlas/references/`:

```text
entries.md
tables.md
rpc.md
mq.md
jobs.md
```

These files are technical inventories, not business interpretation.

### references/tables.md

Describe physical structure and technical usage:

- datasource/schema
- table
- columns when relevant
- mapper/repository
- READS/WRITES
- source locations

Do not define the table's Business Object meaning here.

Business semantics for important tables belong to `ca-business`.

## System / Project Markdown

Generate stable technical Markdown under the shared Analysis Workspace Root:

```text
<analysis-workspace-root>/docs/code-atlas/system/
<analysis-workspace-root>/docs/code-atlas/projects/
<analysis-workspace-root>/docs/code-atlas/references/
```

Use complete, readable file names without ambiguous abbreviations.

## IDs

Examples:

```text
SYSTEM-finance-platform
PROJECT-finance-account
PROJECT-payment-service
```

Project/System IDs may contain technical project names because those entities represent technical structure.

Business entity IDs must not inherit project naming merely because this layer discovered them.

## Evidence rules

Every structural or dependency claim must point to direct evidence such as:

- build files
- module declarations
- application bootstrap
- source package
- interface implementation
- configuration
- client/provider definition

## Challenge protocol

If technical discovery suggests a business change, emit an evidence-backed proposal:

```text
Evidence Challenge
target_owner: ca-business | ca-scenario | ca-chain
observed_fact:
evidence:
reason:
```

Do not modify the target knowledge directly.

## Completion gate

Before reporting project modeling complete, verify:

- all visible projects accounted for
- modules mapped
- production entries inventoried
- major integrations inventoried
- datasource/table references inventoried
- unresolved project/provider boundaries declared
- tests excluded from production topology
- no business domain was invented from technical naming

Return technical knowledge plus any Evidence Challenges.
