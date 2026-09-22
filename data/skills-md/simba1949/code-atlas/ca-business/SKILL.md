---
name: ca-business
description: >
  Model Code Atlas business knowledge from verified code evidence: Business Domains,
  Capabilities, Business Objects, Lifecycles, and core-table business semantics.
  Use strict promotion gates so tables, DTOs, enums, method names, or module names are
  not mistaken for business entities or state machines.
---

# ca-business

## Mission

Own the stable business semantics beneath Scenarios:

```text
Business Domain
  ↓
Capability

Business Object
  ↓
Lifecycle
  ↓
State
  ↓
State Transition
```

## Ownership

You own:

- Business Domain
- Capability
- Business Object
- Lifecycle
- State
- State Transition
- core-table business semantics

You do not own:

- Scenario
- Process
- Sub-process
- Step
- Execution Chain
- technical project structure




## Shared semantic rules

Use:

```text
../code-atlas/references/semantic-canonicalization-protocol.md
../code-atlas/references/semantic-identity-rules.md
```

For owned knowledge, decide only:

```text
MERGE
NEW
UNRESOLVED
REJECT
```

Key local rules:

- Domain identity comes from stable business responsibility, not Project/Module.
- Capability identity comes from stable business function and result.
- Business Object identity comes from real business identity, not Class/Table count.
- Lifecycle identity comes from Business Object + business state dimension.
- Business Rules stay embedded by default; do not create a standalone rule taxonomy.
- Business relationships use direct business wording; do not require a large fixed relation-kind taxonomy.

Preserve aliases and evidence when knowledge is merged.


## Evidence discipline

Use:

- Fact Inventory
- source behavior
- data reads/writes
- state reads/writes
- configuration
- validated Execution Chain evidence
- tests only as auxiliary evidence

Never promote a business entity from naming alone.

## Business Domain

A Domain is a stable business boundary supported by related capabilities, objects, rules and behavior.

Do not infer Domain solely from:

- module
- package
- service name
- database schema
- team ownership

Require a coherent business responsibility supported by code behavior.

## Capability

Definition:

> 一个 Business Domain 长期稳定提供的业务功能。

Examples:

- 入账
- 消费
- 提现
- 充值
- 退款

### Capability promotion gate

Require a behavior cluster such as:

```text
entry/operation
+
business behavior
+
Business Object or data effect
+
identifiable business result
```

A single method named `withdraw()` is insufficient.

Use the de-scenario test:

> Remove channel/role/object/settlement/path qualifiers. If the remainder is a stable standalone business function, it may be a Capability.

Capability is embedded in Domain Markdown and still receives a stable ID.

## Business Object

> Business Object != Data Table.

Promotion requires:

1. relatively stable business identity;
2. meaningful business data/state;
3. meaningful business behavior that reads or mutates it.

Strong clusters may include:

- primary table
- domain/DO entity
- repository
- state/amount/type fields
- create/submit/confirm/cancel behavior

Do not promote:

- DTO/VO/Request alone
- generic context/result/page types
- one ambiguous log/config/detail table
- Java class merely because its name sounds business-like

### Persistence mapping

A Business Object may map to multiple tables.

Use roles:

```text
PRIMARY
DETAIL
RELATION
STATE_HISTORY
BUSINESS_FLOW
AUDIT_LOG
SNAPSHOT
CONFIG
TECHNICAL
```

Store authoritative direction:

```text
Business Object → Table
```

Do not manually maintain reverse `Table → Business Object` lists.

## Lifecycle

Canonical Lifecycle belongs only to a Business Object.

Promotion requires:

1. confirmed Business Object;
2. confirmed state dimension;
3. confirmed state values;
4. real state transitions supported by execution/write evidence.

### Multiple dimensions

Separate fields such as:

```text
status
pay_status
audit_status
```

into separate Lifecycles unless code proves they form one dimension.

### State does not imply Transition

Enum values alone are candidate states.

A state field alone is a candidate dimension.

A transition requires real write/control-flow evidence.

Never draw arrows merely because two enum values exist.

### Partial lifecycle

A Lifecycle may be confirmed even when only some transitions are found.

Publish only verified transitions and explicitly state that no additional transitions were found in the current visible code range.

## Direct vs indirect writes

Distinguish:

- project directly writes table/state;
- project calls another service/RPC which performs the write.

Never claim the caller project writes a table merely because the business effect occurs downstream.

## Dual names

Use:

```text
source_name
business_name
```

`source_name` must come from source/table/field/config/interface facts.

`business_name` may summarize verified behavior.

If business semantics are insufficient, keep a neutral label or unresolved description.

## IDs

Use complete names:

```text
DOMAIN-courier-wallet
CAPABILITY-courier-wallet-withdraw
BUSINESS-OBJECT-withdraw-order
LIFECYCLE-withdraw-order-main
STATE-withdraw-order-main-created
TRANSITION-withdraw-order-main-created-TO-processing
```

Do not encode project/module into business IDs by default.

## Markdown ownership

### Domain

Store:

- positioning
- boundaries
- Capabilities
- core Business Objects
- evidence

Do not store Scenario lists manually; derive from Scenario → Capability.

### Business Object

Store:

- identity
- semantics
- important fields
- persistence mapping and Data Roles
- evidence

### Lifecycle

Store:

- `business_object` parent reference
- state dimension/storage
- states
- transitions
- transition evidence
- derived diagram

Do not manually store Process/Scenario reverse references.

## Challenge protocol

If `ca-chain` or `ca-scenario` discovers new state/object evidence:

1. inspect direct evidence;
2. ACCEPT, REJECT or mark UNRESOLVED;
3. update only owned knowledge;
4. do not change semantics without new evidence.

## Completion gate

Before confirming business modeling:

- Domains are behavior-backed
- Capabilities pass promotion gate
- Business Objects are not table/class aliases
- Lifecycle dimensions are explicit
- every State Transition is code-proven
- table roles are evidence-backed
- IDs are stable and business-oriented
- no Scenario/Process ownership has leaked into this skill
