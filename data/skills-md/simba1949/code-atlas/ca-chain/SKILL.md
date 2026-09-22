---
name: ca-chain
description: >
  Trace evidence-backed technical Execution Chains that implement Code Atlas Processes
  and activities across projects, synchronous RPC, MQ, callbacks, jobs, data handoffs,
  retries, compensation, databases, and external boundaries. Use for deep technical
  verification, not for redefining business knowledge.
---

# ca-chain

## Mission

Answer:

> How is this Process or business activity actually implemented in code?

Execution Chain is the technical implementation layer.

It primarily binds to Process, and may map precisely to Sub-process / Step.

## Ownership

You own:

- Execution Chain
- Common Chain
- chain nodes
- chain relations
- technical boundaries
- termination
- unresolved technical continuation

You do not own:

- Domain
- Capability
- Business Object
- Lifecycle
- Scenario
- Process semantics

If tracing contradicts them, submit an Evidence Challenge.




## Shared semantic rules

Use:

```text
../code-atlas/references/semantic-canonicalization-protocol.md
../code-atlas/references/semantic-identity-rules.md
```

For Chains, canonicalization only prevents duplicate technical-chain identities.

Do not use Chain similarity to merge or redefine Scenario, Process, Business Object or Lifecycle semantics.

If tracing contradicts owned business knowledge, return the evidence to its Owner for re-evaluation.


## Entry model

A Chain begins at a clear technical trigger, for example:

- HTTP endpoint
- RPC provider
- MQ consumer
- Job
- event listener
- callback
- manual trigger

Then follow real code relationships while remaining in one continuous execution context.

## Continue the same Chain across

Do not split merely because execution crosses:

- method
- class
- module
- project
- JVM
- synchronous RPC
- transaction
- database

Continue while the same Process and execution context remain continuous.


For multi-project analysis, Project changes are rendered as boundary markers inside the same Chain when execution remains synchronous/continuous.

Example:

```text
site-account
  → synchronous RPC
emp-account
  → database write
```

may remain one Execution Chain.

Do not create separate per-Project Chain documents solely because the implementation crosses repository boundaries.

All Chain documents for the analysis are published under the one shared:

```text
<analysis-workspace-root>/docs/code-atlas/chains/
```

## Split Chain at independent execution context

Create a new Chain for:

- MQ consumer continuation
- external callback
- scheduled Job
- independent retry worker
- compensation worker
- manual retrigger
- DB-driven later worker/job continuation

Common roles:

```text
ENTRY
ASYNC_CONTINUATION
CALLBACK
SCHEDULED
RETRY
COMPENSATION
MANUAL
```

## Process boundary

If code flow reaches a genuinely different Process, terminate current Chain with:

```text
PROCESS_BOUNDARY
```

Do not absorb the next Process into one giant chain merely because the code calls it synchronously.

Process boundary is decided by `ca-scenario`; if trace evidence suggests it is wrong, challenge it.

## Data handoff

A database write may be:

1. an ordinary effect inside the current Chain; or
2. a `DATA_HANDOFF` if a later job/worker independently queries it to continue work.

In case 2, end the current Chain and create another Chain for the later execution context.

## External systems

At an external boundary record only visible facts:

- client/interface
- protocol
- endpoint/config if visible
- request/response types if visible
- code-visible result handling

Do not invent third-party internals.

Use:

```text
EXTERNAL_BOUNDARY
```

when the system boundary is clear.

## Framework internals

Do not trace generic framework internals such as:

- DispatcherServlet
- Dubbo framework transport internals
- RocketMQ client internals
- MyBatis/JDBC internals

Cross-cutting code belongs in a Chain only when business-significant, e.g.:

- idempotency
- authorization affecting business path
- distributed lock
- transaction semantics
- risk control
- signature/security verification

Ordinary logging/metrics/tracing/helpers are normally omitted.

## Chain termination

Every Chain must terminate explicitly:

```text
RETURN
ASYNC_BOUNDARY
EXTERNAL_BOUNDARY
PROCESS_BOUNDARY
DATA_HANDOFF
SOURCE_UNAVAILABLE
```

No open-ended `...`.

## Resolution

Use:

```text
CLOSED
PARTIAL
UNRESOLVED
```

A missing provider/consumer/continuation must be visible as unresolved.

## Multi-chain Process

A Process may have:

```text
Execution Chain Set
```

rather than one giant arrow.

Example:

```text
ENTRY
→ ASYNC_CONTINUATION
→ CALLBACK
→ SCHEDULED timeout handler
→ COMPENSATION
```

These are separate chains connected by explicit technical relations.

## Chain relation semantics

Use relations such as:

```text
ASYNC_CONTINUE
CALLBACK
SCHEDULED_CONTINUE
RETRY
COMPENSATE
DATA_HANDOFF
TRIGGER
```

Only when code evidence proves the connection.

## Common Chain

A Common Chain is genuine shared implementation.

Do not extract Common Chain merely because two code paths are conceptually similar.

Store under:

```text
chains/common-chains/
```

Use complete ID:

```text
COMMON-CHAIN-account-validation
```

Ordinary Chains reference Common Chains; Common Chains do not manually maintain reverse used-by lists.

## Implementation mapping

Canonical direction:

```text
Execution Chain → Process
Execution Chain → Activity
Execution Chain → Common Chain
```

Prefer precise activity mapping when evidence supports it.

Do not require Process Markdown to duplicate Chain lists.

## Data / state trace

Record:

- reads
- writes
- SQL/table
- state field writes
- MQ produce/consume
- RPC call/provider
- Job scheduling/entry
- external call
- configuration affecting technical path

When a state write provides new lifecycle evidence, challenge `ca-business`; do not define the lifecycle yourself.

## Test rule

Test code may validate interpretation but never forms a production Chain by default.

## Chain Markdown

Front matter should identify:

- stable ID
- `type: EXECUTION_CHAIN`
- source/business name
- owner
- analysis result
- `chain_kind: PROCESS | COMMON`
- role for process-specific Chains
- implements Process/activity references when applicable

Body should contain:

- technical responsibility
- Trigger
- Execution Flow
- Nodes
- Data Access
- State Transition implementation
- RPC / MQ / Job / External
- Common Chain references
- Termination
- Unresolved
- Evidence

Do not redefine Process business rules/lifecycle.

## Evidence Challenge

If tracing reveals contradictory knowledge, return:

```text
Evidence Challenge
target_owner:
target_entity:
observed_fact:
proposed_change:
evidence:
```

Examples:

- previously unknown state write → `ca-business`
- Process actually continues into a second stable business goal → `ca-scenario`
- provider project relationship differs → `ca-project`

## Completion gate

A verified Chain has:

- clear trigger
- continuous evidence-backed path
- visible side effects
- explicit boundaries
- explicit termination
- no invented continuation
- correct Process/activity mapping
- source evidence for critical edges
