---
name: ca-scenario
description: >
  Identify evidence-backed Scenarios under confirmed Capabilities, split and promote
  Processes by business boundaries, and model Process-internal Sub-process/Step flows.
  Use when distinguishing real business paths from technical entries, workflow stages,
  error branches, or implementation details.
---

# ca-scenario

## Mission

Own:

```text
Capability
  ↓
Scenario
  ↓
Process
  ↓
Sub-process / Step
```

Scenario orchestrates Processes.

Process models a business-flow unit.

Sub-process/Step express business actions, never raw technical calls.




## Shared semantic rules

Use:

```text
../code-atlas/references/semantic-canonicalization-protocol.md
../code-atlas/references/semantic-identity-rules.md
```

Scenario:

```text
Selector
→ Candidate Path
→ compare canonical Business Process Flow
→ MERGE / NEW / UNRESOLVED / REJECT
```

Process:

```text
independent business goal
+ business boundary
+ business result
```

determines whether a behavior deserves Process identity.

The detailed Scenario Canonicalization rules below remain the local specialization for preventing scenario explosion.


## Inputs

Consume:

- confirmed Capability / Business Object / Lifecycle from `ca-business`
- Fact Inventory from `ca-code-intel`
- technical context from `ca-project`
- trace evidence / challenges from `ca-chain`

## Scenario definition

> 同一 Capability 下，经过候选路径归一化后，具有稳定且实质不同 Business Process Flow 的真实业务路径。

Core principle:

> Selector discovers candidate paths; Canonical Business Process Flow defines Scenario identity.

A Scenario is not “a branch exists” and is not “a unique condition combination exists”.

Different conditions, parameter values, entry types, roles, channels, or technical chains do not automatically imply different Scenarios.

A Scenario is a stable, repeatable, business-meaningful path under the same Capability whose canonical Process orchestration remains materially distinct after technical/parameter noise is removed.

## Scenario Promotion Gate

A Candidate Scenario must pass all gates.

### 1. Capability Gate

It still serves the same core Capability.

If the business goal is actually different, revisit Capability boundaries.

### 2. Selection Gate

There is a real code-backed path selector, for example:

- channel
- role
- object/account type
- settlement/payment type
- route/config
- strategy/business mode

A different Controller/RPC/MQ/Job entry alone is not a selector.

### 3. Divergence Gate

Selection leads to material business-path divergence, such as:

- different Process orchestration
- different participants/responsibilities
- materially different business rules
- different Business Object interaction
- different Lifecycle impact
- different settlement/handling route
- different external business system

### 4. Stability Gate

The path is stable/repeatable, not merely one runtime failure or retry.

### 5. Evidence Gate

Path selection and Process Flow edges are code-proven.

### 6. Canonicalization Gate

Before promoting a new Scenario, prove that the candidate cannot be merged with an existing Scenario after normalizing non-identity dimensions.

Normalize away differences that do not materially change the canonical Business Process Flow, including when applicable:

- HTTP / RPC / MQ / Job entry type
- Project / Module / package
- Controller / Facade / Service implementation
- actor labels
- channel labels
- amount bands
- parameter values
- policy/rule result values
- sync vs async implementation detail
- retry / callback / compensation mechanics
- success / failure / timeout outcomes

Then compare:

- canonical Process sequence / orchestration
- business responsibility handoffs
- Business Object interactions
- Lifecycle impact
- stable business result / closure
- materially different business route

If two candidates remain business-equivalent after normalization:

```text
MERGE
```

Do not create separate Scenarios.

If they remain materially different:

```text
CONTINUE Scenario Promotion
```

The burden of proof is on Scenario split, not on Scenario merge.

## Scenario Candidate Signature

Use an internal analysis-only structure to compare candidate paths.

It is not a published Knowledge Entity.

Suggested fields:

```yaml
capability:
selectors:
applicable_conditions:
canonical_process_flow:
business_objects:
lifecycle_impact:
business_result:
business_responsibility_handoffs:
business_route:
evidence:
```

Do not include transient technical noise in Scenario identity unless it causes a real business-path difference.

## Scenario Canonicalization

For each Capability:

```text
Discover selectors
    ↓
Trace candidate paths
    ↓
Build Candidate Signatures
    ↓
Normalize technical/parameter differences
    ↓
Canonicalize Business Process Flow
    ↓
Merge equivalent candidates
    ↓
Evaluate remaining divergence
    ↓
Scenario Promotion Gate
    ↓
Publish Scenario
```

Target behavior:

```text
many code branches
→ fewer candidate paths
→ fewer canonical business paths
→ stable Scenario set
```

Never use:

```text
one if/branch
→ one Scenario
```

as a modeling rule.

## De-dimension Test

Before splitting two Scenarios, remove the dimension labels that differ, such as:

- channel
- actor/role
- object subtype
- settlement method label
- amount band
- policy result
- entry mechanism

Then ask:

> Do the two candidates still have materially different canonical Business Process Flows?

If `NO`, merge them and record those values as:

- Path Selection
- Applicable Conditions
- Business Rules
- Branches

If `YES`, continue through the Scenario Promotion Gate.

## Scenario anti-patterns

Do not create Scenarios merely from:

- HTTP vs RPC
- MQ vs sync
- Job vs callback
- Project / Module differences
- ordinary role differences
- ordinary channel differences
- amount bands
- fee/rate/deposit calculation differences
- create/submit/processing
- success/failure/timeout
- retry/compensation/callback
- one validation condition
- one extra method call
- one extra database query
- different Execution Chains with the same canonical business path

A technical entry difference can still converge into the same Scenario.

One entry can split into multiple Scenarios when business selectors cause materially different canonical Process orchestration.

Rule difference alone does not create a Scenario.

A rule/condition becomes Scenario-relevant only when it causes stable, material business-path divergence.

Different Execution Chains do not directly trigger Scenario split.

## Scenario Process Flow

Scenario owns ordered/conditional Process relationships.

Do not merely list Process IDs.

For every edge:

```text
PROCESS-A → PROCESS-B
```

store evidence proving the relation.

Process existence does not prove Process ordering.

## Process definition

> Scenario 中具有相对独立业务目标、明确业务边界和业务结果的业务流程单元。

Do not split by:

- Controller
- Service
- Method
- Project
- Module
- transaction
- thread
- RPC
- MQ
- Job

### Decisive Process boundaries

A boundary is strongly supported by:

- Business Goal changes
- independent Business Result
- independent business closure
- cross-Scenario reuse
- independent business value

### Strong supporting signals

- Business Object enters a stable new Lifecycle stage
- genuine business responsibility handoff

### Technical signals

MQ/Job/Callback often split Execution Chains, not Processes.

Only split Process when the business goal/boundary also changes.

## Process Promotion Gate

Confirmed Process should have:

- Business Goal
- Start Boundary
- End Boundary
- Business Result
- Business Flow
- involved Business Objects
- Lifecycle Impact
- evidence
- at least one real Execution Chain
- a clear distinction from neighboring Processes

## Sub-process

> Process 内由多个 Step 组成、具有局部业务目标，但业务价值仍依附于父 Process 的可展开流程。

Use Sub-process only when multiple related Steps need grouping around a local goal.

Default structure:

```text
Process
├── Step
├── Sub-process
│   ├── Step
│   └── Step
└── Step
```

Do not recursively nest Sub-process.

If deeper nesting appears, challenge granularity:

- collapse into Steps;
- split into sibling Sub-processes;
- or promote a reusable/independent unit to Process.

## Step

> 不可再拆出有意义业务流程的关键业务动作。

Good:

- 校验提现资格
- 创建提现单
- 冻结提现金额
- 提交付款
- 确认付款结果

Not Step:

- Call Dubbo
- Send MQ
- Mapper.update
- Query Redis
- Execute SQL

Those belong to Execution Chain.

## Lifecycle Impact

Process does not own Lifecycle.

Reference canonical Transition IDs:

```text
Process / Sub-process / Step → State Transition
```

If a Step can be identified as the precise driver, bind the impact to that Step.

Never duplicate lifecycle definitions inside Process Markdown.

## Business Object references

Process may store direct participating Business Objects because they are important reading context.

Do not manually store reverse `Business Object → Processes`; derive it.

## IDs

Use:

```text
SCENARIO-<domain>-<capability>-<scenario>
PROCESS-<process>
SUB-PROCESS-<process>-<sub-process>
STEP-<process>-<step>
```

Do not include sequence numbers in Step identity merely to encode order.

Order belongs to flow relations.

## Markdown

### Scenario owns

- capability reference
- description
- path selector
- applicable conditions
- normalized Scenario identity / canonical business path
- participants
- Business Objects
- Scenario Process Flow
- Process relation evidence
- business branches

Do not expand Java call chains.

### Process owns

- Business Goal
- Start / End Boundary
- Input / Output
- participants
- Business Objects
- Process Flow
- Sub-process / Step
- Business Rules / Branches
- Lifecycle Impact
- business Data Impact
- business error/compensation meaning

Do not maintain Execution Chain lists; Chain → Process is canonical.

## Challenge loop

Trace evidence may force:

- candidate Scenario merge
- candidate Scenario split
- Process split/merge
- activity reclassification
- lifecycle challenge to `ca-business`

Any semantic change requires new evidence.

## Completion gate

Scenario/Process modeling is stable only when:

- every Scenario passes all gates, including Canonicalization Gate
- candidate paths have been compared/merged before Scenario publication
- no Scenario identity is merely a Cartesian product of dimensions
- each Scenario has evidence-backed Process Flow
- Process boundaries are business-based
- no technical entry/stage/failure is mislabeled as Scenario
- no Service/Method is mechanically promoted to Process
- Sub-process depth remains flat
- Step language is business-semantic
- lifecycle impacts reference canonical transitions
