---
name: code-atlas
description: >
  Orchestrate a full Code Atlas analysis of one or more codebases. Use when the user
  wants a project/business atlas covering technical structure, Business Domains,
  Capabilities, Scenarios, Processes, Business Objects, Lifecycles, Execution Chains,
  Canonical Markdown, and an HTML viewer, all grounded in current code evidence.
---

# Code Atlas

## Mission

Turn the current visible codebase into a navigable, evidence-backed knowledge atlas.

Do not treat this as a one-pass call-graph task.

Use this lifecycle:

> Discover → Model → Trace → Challenge → Converge → Audit → Publish

Inside every semantic modeling stage, apply the shared protocol:

> Fact → Candidate → Canonicalize → Verify → Publish

Chinese shorthand:

> 发现 → 建模 → 追链 → 反证 → 收敛 → 审计 → 发布

## Non-negotiable rules

1. Use only current visible code facts.
2. Never complete missing business semantics from industry intuition.
3. Technical project/module boundaries must not split a continuous business path.
4. Markdown is Canonical Knowledge; HTML is derived presentation.
5. Every run is full analysis and full generation.
6. Candidate knowledge stays outside final `docs/code-atlas/`.
7. No Evidence → No Semantic Change.
8. One knowledge object has exactly one owner.
9. Store relationships in one canonical direction; derive reverse relations.
10. Tests are auxiliary evidence only and never production entries/chains by default.
11. Canonical Atlas output belongs to the Analysis Workspace Root, not to an individual Project.
12. Every semantic entity must pass the shared Semantic Canonicalization Protocol before publication.



## Shared semantic rules

Use:

```text
references/semantic-canonicalization-protocol.md
references/semantic-identity-rules.md
```

Keep the mechanism simple:

```text
Fact
→ Candidate
→ Canonicalize
→ Verify
→ Publish
```

Canonicalization has only four outcomes:

```text
MERGE
NEW
UNRESOLVED
REJECT
```

Owner Skills decide semantics for the knowledge they own.

`ca-knowledge` only keeps IDs, aliases, references and consistency; it is not a central business analyst.


## Skill topology

Use:

- `ca-code-intel` — discover code-intelligence providers and build Fact Inventory.
- `ca-project` — own System / Project / Module / technical-reference knowledge.
- `ca-business` — own Domain / Capability / Business Object / Lifecycle.
- `ca-scenario` — own Scenario / Process / Sub-process / Step.
- `ca-chain` — own Execution Chain / Common Chain.
- `ca-knowledge` — validate IDs, references, ownership and reverse relations.
- `ca-audit` — gate publication quality.
- `ca-visual` — generate HTML only from canonical Markdown.

Do not collapse these ownership boundaries.

## Full execution

### 1. Resolve analysis scope and Analysis Workspace Root

First identify the exact repositories/projects that belong to this analysis.

Do not automatically include every sibling repository merely because it exists under the same parent directory.

Then resolve one `Analysis Workspace Root`.

Resolution order:

1. an explicit workspace root selected by the user;
2. the current workspace root when it contains the selected projects;
3. the nearest common parent of the selected project roots when that parent clearly represents the requested analysis scope.

If the root remains ambiguous, do not generate separate per-project Atlases as a fallback. Resolve the workspace root before publication.

Single-project example:

```text
emp-account/
├── src/
└── docs/
    └── code-atlas/
```

Multi-project example:

```text
settleWork/
├── emp-account/
├── site-account/
└── docs/
    └── code-atlas/
```

Treat selected projects as one analysis workspace when the business crosses them.

The selected Project set and the Analysis Workspace Root are different concepts:

- selected Project set controls what code is analyzed;
- Analysis Workspace Root controls where the one Canonical Atlas is published.

Capture final snapshot metadata when available:

- Git branch
- Git commit
- worktree state

Human-facing code status must use:

- `代码状态：与当前 Git 提交一致`
- `代码状态：包含本地未提交修改`

### 2. Full Fact Discovery

Invoke `ca-code-intel`.

Require breadth-first coverage of:

- Structure
- HTTP/RPC/MQ/Job/Event/Callback entries
- Outbound RPC/HTTP/MQ/external clients
- DataSource/Table/Mapper/Repository/SQL/DDL
- State fields/enums/readers/writers
- Business configuration/routes/channels/types
- Async/retry/compensation surfaces

Do not deep-trace one entry before major surfaces are inventoried.

### 3. Technical model

Invoke `ca-project`.

Build technical topology and references without inventing business domains from module/package names.

### 4. Business model

Invoke `ca-business`.

Build candidates then confirm:

- Business Domain
- Capability
- Business Object
- Lifecycle

Only confirmed entities may later be published.

### 5. Scenario / Process model

Invoke `ca-scenario`.

Build and challenge:

- Scenario
- Scenario Process Flow
- Process
- Sub-process
- Step

Do not use HTTP/RPC/MQ/Job boundaries as business boundaries.

### 6. Technical trace

Invoke `ca-chain`.

For each Process, trace one or more real Execution Chains and verify:

- trigger
- path
- data effects
- state writes
- RPC/MQ/Job/external boundaries
- termination

If new evidence conflicts with the business model, create an Evidence Challenge instead of silently changing another skill's entity.

### 7. Reconcile

Route challenges back to the owner:

- structure → `ca-project`
- domain/capability/object/lifecycle → `ca-business`
- scenario/process/activity → `ca-scenario`
- chain → `ca-chain`

Re-run affected traces after semantic changes.

### 8. Converge

`Converge` is the global semantic convergence phase.

Its core work is:

```text
Semantic Canonicalization
+ Conflict Resolution
+ Knowledge Deduplication
+ Canonical Registration
```

Re-run the shared Semantic Canonicalization Protocol for cross-Skill duplicates/conflicts surfaced by tracing.

Convergence requires stability of:

- Domain / Capability
- Business Object
- Lifecycle / Transition
- Scenario set
- Process boundaries
- Scenario Process Flow
- Process ↔ Execution Chain mapping

Explicit unresolved external/source boundaries may remain.

### 9. Audit

Invoke `ca-audit`.

Publication is blocked by unsupported entity identity, unsupported Process Flow edges, invented State Transitions, ownership conflicts, broken references, or ambiguous unresolved technical continuations that were hidden rather than declared.

### 10. Publish

Generate exactly one Canonical Atlas for the current analysis scope under:

```text
<analysis-workspace-root>/docs/code-atlas/
```

Examples:

```text
# Single project
emp-account/docs/code-atlas/

# Multi-project workspace
settleWork/docs/code-atlas/
```

Do not generate:

```text
settleWork/emp-account/docs/code-atlas/
settleWork/site-account/docs/code-atlas/
```

for one cross-project analysis.

Project boundaries are represented inside the Atlas, primarily under:

```text
docs/code-atlas/projects/
```

They must not split the Atlas itself.

Then invoke `ca-visual` to generate the interactive HTML Atlas from this same Canonical Markdown root only.

HTML must follow:

```text
Business First
→ Scenario Flow
→ Business Object / Data
→ Code
```

with reverse navigation back to business.

The viewer must support:

- global search across business and technical names;
- progressive technical disclosure;
- local Focus/Spotlight rather than default global graphs;
- Process `Business / Data / Code` drill-down;
- Project swimlanes for cross-project Execution Chains;
- Evidence on demand.

The detailed contract is owned by `ca-visual`.

Never publish mixed candidate/confirmed output.

## Canonical cognitive model

```text
Business Domain
  ↓
Capability
  ↓
Scenario
  ↓
Process
  ↓
Sub-process / Step
  ↓
Execution Chain
```

Object axis:

```text
Business Object
  ↓
Lifecycle
  ↓
State
  ↓
State Transition
       ↑
Process / Sub-process / Step
```

## Output tree

All paths below are relative to the resolved Analysis Workspace Root:

```text
docs/code-atlas/
├── README.md
├── system/
├── projects/
├── business/
│   └── domains/
├── objects/
├── lifecycles/
├── scenarios/
├── processes/
├── chains/
│   ├── <process>/
│   └── common-chains/
├── tables/
├── html/
│   ├── index.html
│   ├── assets/
│   └── data/
└── references/
```

## IDs

Use complete type names, not abbreviations:

```text
SYSTEM-...
PROJECT-...
DOMAIN-...
CAPABILITY-...
SCENARIO-...
PROCESS-...
SUB-PROCESS-...
STEP-...
BUSINESS-OBJECT-...
LIFECYCLE-...
STATE-...
TRANSITION-...
EXECUTION-CHAIN-...
COMMON-CHAIN-...
```

Business IDs must not encode project/module boundaries by default.

## Final acceptance

A finished Atlas must support:

- business → process → code drill-down
- code → business reverse navigation
- state transition → activity/process navigation
- table → object/process/chain reverse navigation
- explicit unresolved boundaries
- durable evidence anchors for all critical claims
