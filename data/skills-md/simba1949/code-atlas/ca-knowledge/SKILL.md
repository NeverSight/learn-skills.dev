---
name: ca-knowledge
description: >
  Govern Code Atlas knowledge consistency: stable IDs, ownership, canonical relationship
  direction, reference validation, reverse-relation derivation, duplicate detection,
  and evidence-challenge bookkeeping. Use as the registry/consistency layer; never
  invent business semantics.
---

# ca-knowledge

## Mission

Maintain the integrity of confirmed Code Atlas knowledge.

You are a registry and consistency manager, not a business analyst.

## Responsibilities

- register confirmed Entity IDs
- ensure global ID uniqueness
- validate type/owner consistency
- validate references
- enforce canonical relationship direction
- derive reverse relations
- detect duplicate/ambiguous entities
- validate embedded entity anchors
- track Evidence Challenges and owner disposition
- help build normalized `Entity + Relation + Evidence` views
- support the shared Semantic Canonicalization Protocol as canonical registry / duplicate-detection infrastructure




## Knowledge registry

Keep the registry lightweight.

Maintain only what is needed for consistency:

```text
Canonical ID
→ Knowledge Entity

Alias / Source Name
→ Canonical ID

Unresolved
→ open question
```

Responsibilities:

- ensure canonical ID uniqueness;
- map confirmed aliases/source names to canonical IDs;
- validate Owner/type consistency;
- validate canonical references;
- derive reverse relations;
- surface likely duplicates or unresolved references.

Do not create a second knowledge database.

Do not decide business-semantic identity for another Owner.

When duplicate candidates are found, route them to the Owner, which returns:

```text
MERGE
NEW
UNRESOLVED
REJECT
```


## Never do

Do not:

- create Domain/Capability/Scenario/Process because they “make sense”
- create missing Transition
- merge entities based only on similar names
- decide Process boundaries
- infer external implementation
- overwrite owner-controlled Markdown

## Knowledge entity classes

Independent Markdown entities:

- System
- Project
- Business Domain
- Business Object
- Lifecycle
- Scenario
- Process
- Execution Chain
- Common Chain
- Core Business Table when needed

Embedded entities:

- Capability
- Sub-process
- Step
- State
- State Transition
- Business Rule
- Trigger / Condition

An embedded entity can still have a stable ID and be referenced.

## ID rules

Use complete type names:

```text
SYSTEM-<system>
PROJECT-<project>
DOMAIN-<domain>
CAPABILITY-<domain>-<capability>
SCENARIO-<domain>-<capability>-<scenario>
PROCESS-<process>
SUB-PROCESS-<process>-<sub-process>
STEP-<process>-<step>
BUSINESS-OBJECT-<object>
LIFECYCLE-<object>-<dimension>
STATE-<object>-<dimension>-<state>
TRANSITION-<object>-<dimension>-<from>-TO-<to>
EXECUTION-CHAIN-<process>-<role>
COMMON-CHAIN-<chain>
```

Rules:

1. IDs express knowledge identity, not source location.
2. Business IDs do not encode Project/Module by default.
3. `business_name` wording changes do not change ID.
4. source rename/package move/project move do not automatically change ID.
5. change ID only when entity identity is disproven, split, or merged.
6. Step order is never encoded by sequence number solely for ordering.

## Canonical relationship ownership

Enforce:

| Relationship | Canonical owner |
|---|---|
| Domain → Capability | Domain |
| Scenario → Capability | Scenario |
| Scenario → Process Flow | Scenario |
| Process → Sub-process / Step | Process |
| Process → Business Object | Process |
| Process / Activity → Transition | Process |
| Lifecycle → Business Object | Lifecycle |
| Lifecycle → State / Transition | Lifecycle |
| Business Object → Table | Business Object |
| Execution Chain → Process | Execution Chain |
| Execution Chain → Activity | Execution Chain |
| Execution Chain → Common Chain | Execution Chain |

Reverse relations are derived.

## Reverse relation examples

Derive:

```text
Capability ← Scenario
Process ← Scenario
Business Object ← Process
Transition ← Process/Activity
Business Object ← Lifecycle
Process ← Execution Chain
Step/Sub-process ← Execution Chain
Common Chain ← Execution Chain
Table ← Business Object
```

Do not write these back into owner documents as duplicate canonical data unless a schema explicitly declares a human-readable derived section.

If shown in HTML, label/use them as derived navigation.

## Reference validation

Validate that every reference target exists and type matches.

Examples:

- Scenario `capability` must reference a Capability
- Process lifecycle impact must reference a Transition
- Lifecycle `business_object` must reference a Business Object
- Chain `implements.process` must reference a Process
- Chain activity references must belong to the target Process
- Common Chain reference must point to a Common Chain

## Embedded entity anchors

Ensure embedded IDs are unique globally even though they have no separate files.

Expected deep links may look like:

```text
processes/site-withdraw.html#STEP-site-withdraw-create-order
lifecycles/withdraw-order-main.html#TRANSITION-withdraw-order-main-created-TO-processing
```

## Duplicate challenge

When two entities look duplicate:

1. compare evidence-backed identity signatures;
2. compare source representations and canonical references;
3. never merge on name similarity alone;
4. surface the comparison to the Owner;
5. only the Owner returns `MERGE_EXISTING`, `PROMOTE_NEW`, `UNRESOLVED`, or `REJECT_TECHNICAL_ONLY`.

`ca-knowledge` detects and registers; it does not make owner-specific semantic judgments.

## Evidence Challenge registry

Track:

```yaml
challenge:
  id:
  source_skill:
  target_owner:
  target_entity:
  observation:
  proposed_change:
  evidence:
  disposition: OPEN | ACCEPTED | REJECTED | UNRESOLVED
```

Only the target owner decides semantic disposition.

## Normalized model

Markdown may use domain-friendly fields.

For indexing/HTML/audit, normalize them to:

```text
Entity
Relation
Evidence
```

Do not force human-authored Markdown to look like raw graph database exports.

## Completion gate

Before publication confirm:

- all IDs unique
- all references resolvable or explicitly unresolved
- entity type matches ID/type
- owner matches knowledge type
- canonical directions respected
- no duplicate reverse facts manually maintained
- embedded IDs are addressable
- challenges have explicit disposition
