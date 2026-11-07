---
name: get-fable
description: "Orchestrate software engineering workflows across the canonical get-fable coding lifecycle with deterministic routing and evidence precedence. Use when starting a complex coding task, navigating lifecycle phases, resuming work with durable .fable state, or routing between research, planning, testing, verification, and recovery — even if the user does not explicitly say \"get-fable\" (e.g. \"follow fable lifecycle\", \"orchestrate this project\", \"what is the next engineering step\", \"route my task\"). Do NOT use when an individual specialist skill already has clear isolated ownership of a bounded subtask."
version: 1.3.0
pack: core
inputs:
  - task_description
  - current_state
requires:
  - repo_access
produces:
  - routing_decision
gates:
  - state_schema_valid
fallback: null
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors: []
  continuations:
    - fable-discover
    - fable-research
    - fable-plan
  lateral_peers:
    - fable-spark
  recovery: fable-recover
---

# get-fable

Choose the next engineering mode from the actual state of the work, not from the loudest keyword in the user's last message.

## Mission
`get-fable` is the **Master Orchestration Agent (Boss Agent)** and lifecycle control plane governing the Get-Fable ecosystem. It exercises central authority over task intake, decomposition, specialist ownership assignment, execution tracking, verification, recovery, and completion decisions across all 42 canonical skills.

Good routing is stateful. "Ship it" does not mean release if verification is stale. "Fix it" does not mean execute if the same hypothesis already failed twice. "Use this API" does not mean code from memory if the contract is current and unknown.

## Master Orchestration Control Plane (M5 Target)

As the Master Orchestrator, `get-fable` enforces six core supervisory invariants:

1. **Central Lifecycle Ownership:** One authoritative primary owner for each load-bearing decision. The master orchestrator decomposes tasks into bounded cards, assigns ownership, schedules execution, and makes authoritative phase transitions.
2. **Capability Bounding & Isolation:** Child agents run with least-privilege capability boundaries. Any requested tool or engine outside the assigned capability envelope is strictly rejected.
3. **Deterministic Delegation (The 3 Laws):** Parallel execution is permitted only when write scopes, semantic contracts, and verification commands are strictly independent. Conflicting mutations automatically serialize into sequential dependency waves.
4. **Worker Supervision & Crash Containment:** Child worker execution over gRPC/RPC is fully supervised. Worker crashes or unhandled rejections are isolated and trapped into structured failure receipts without bringing down the master orchestrator.
5. **Late-Event Fencing & Contradiction Detection:** Events emitted by cancelled workers after cancellation timestamps are fenced and dropped. Contradictory claims from concurrent workers over the same target or artifact fail closed.
6. **Evidence-First Completion:** Self-attestation is rejected. No task or phase transition is marked complete without fresh, machine-checked passing evidence matching the current mutation generation.

## Activate When
- a substantial engineering request enters the workspace;
- the next Skill is ambiguous;
- work resumes from `.fable` state or a handoff;
- a phase transition is requested;
- new evidence invalidates the current route;
- a failure/review/security/release gate may override ordinary execution.

## Do Not Activate When
- a specialist is already executing a bounded, still-valid contract and no routing condition changed;
- the user asks only for a raw command output that a current Skill already owns;
- repeated re-routing would add ceremony without changing the next safe action.

## Routing Classification
Classify the dominant reason the next action exists.

| Situation | Preferred owner |
| --- | --- |
| repository/runtime facts unknown | `fable-discover` |
| current external fact/API uncertain | `fable-research` |
| architecture/decomposition/contract choice | `fable-plan` |
| testable behavior change | `fable-tdd` |
| genuinely independent bounded cards | `fable-delegate` |
| bounded accepted implementation | `fable-execute` |
| fresh falsification required | `fable-verify` |
| independent diff correctness review | `fable-review` |
| trust boundary/vulnerability/security work | `fable-security` |
| repeated/contradictory failure | `fable-recover` |
| candidate is ready for distribution decision | `fable-release` |
| another session/agent must resume | `fable-handoff` |
| agent-control change needs benchmark proof | `fable-eval` |
| next atomic move is unclear inside active work | `fable-spark` |

## Orchestration Protocol

### Stage 1 — Read intent and durable state
Consider together:
- user's current request;
- active card/phase;
- failure streak;
- mutation vs verified generation;
- open review/security findings;
- unresolved load-bearing unknowns;
- release/handoff state.

The last sentence in chat does not erase the lifecycle state.

### Stage 2 — Apply precedence gates
Before intent scoring, check hard overrides:
1. corrupted/invalid state → diagnose/repair state before trusting it;
2. repeated failure or contradictory evidence → recover;
3. explicit security-sensitive request → security specialist;
4. stale verification when completion/release is requested → verify;
5. blocking unknown that changes design → discover/research;
6. otherwise route by task ownership.

Precedence exists to stop a plausible but unsafe lower-level action.

### Stage 3 — Distinguish task type from requested outcome
Examples:
- "Publish this" is an outcome; current state may still require verify/review first.
- "Fix this" is an outcome; unknown root location may require discovery.
- "Make it faster" may be research/measurement/planning before execution.
- "Review and fix" is two stages; review should identify grounded findings before mutation unless user explicitly asks for direct repair and evidence is already clear.

### Stage 4 — Route to one primary owner
Choose the Skill that owns the **next load-bearing decision**, not every Skill that might eventually participate.

Return:
- selected Skill;
- reason/precedence;
- evidence/state used;
- gate that will permit the next transition.

### Stage 5 — Persist only meaningful transitions
Update lifecycle state when the route changes actual work phase or evidence freshness. Do not churn state for read-only explanatory turns.

### Stage 6 — Re-route on new evidence
A route is not permanent. Recompute when:
- an assumption is disproved;
- scope expands;
- a failure repeats;
- security risk appears;
- mutation makes proof stale;
- a worker discovers a dependency collision;
- release candidate changes.

## Decision Rules
- `failureStreak >= 2` with materially similar attempts outranks execution and routes to recovery.
- Explicit vulnerability/threat/authz/secret/trust-boundary work routes to security even if the diff also needs general review later.
- Current external API/version uncertainty routes to research; repository-local uncertainty routes to discovery.
- If implementation cannot proceed without choosing a new contract/architecture, plan before execute.
- A testable bug/behavior change should route through TDD unless a valid regression harness is impossible or already established.
- "Done", "merge", "ship", or "release" cannot bypass stale/missing verification.
- A passing receipt/research note is not completion-capable evidence.
- Delegation is selected for real independence, not simply because there are multiple subtasks.
- Handoff is selected when continuity itself is the deliverable; it does not substitute for verification.
- Prefer the narrowest specialist that owns the next decision; avoid keeping the orchestrator active once ownership is clear.

## Invariants
- One primary Skill owns the next load-bearing decision.
- State/evidence precedence can override textual intent when necessary for correctness.
- No completion/release route relies on evidence older than relevant mutation.
- Repeated failed hypotheses do not route back into blind execution.
- Research and discovery are distinct: external current fact vs repository/runtime fact.
- Routing explanations remain traceable to intent/state, not hidden scoring alone.

## Failure Taxonomy
### Keyword capture
Router sees "release", "security", or "test" and ignores the actual state/task. Re-evaluate precedence and ownership.

### State blindness
Router uses the last prompt but ignores failure streak, stale proof, or active card. Re-read durable state.

### Over-orchestration
Every small step returns through the router although specialist ownership remains valid. Keep the active specialist until a routing condition changes.

### Under-routing
Execution continues after a new architecture unknown, repeated failure, or security boundary appears. Stop and re-route.

### Multi-owner ambiguity
Several Skills seem plausible. Select the one that owns the earliest unresolved decision; encode later Skills as continuations/gates, not simultaneous primary owners.

### Stale-state corruption
State does not match repository reality. Diagnose/repair before using it as a routing oracle.

## Anti-Patterns
- routing by one keyword;
- treating user's desired final outcome as the immediate next action;
- re-routing every turn for ceremony;
- using Spark as a substitute for specialist selection;
- sending a repeated failure back to execute;
- sending unknown external API details to repository discovery;
- accepting stale verification because the user said "ship it";
- selecting multiple primary Skills with no order.

## Routing Packet

```text
Intent/outcome:
Current phase/card:
State overrides: failure / stale evidence / security / unknowns
Primary next decision:
Selected Skill:
Why this Skill now:
Gate to leave it:
Likely continuation(s):
```

## Completion Criteria
Orchestration for a turn is complete when:
- the next load-bearing decision has one clear owner;
- precedence gates were checked;
- route is consistent with current evidence/state;
- specialist receives enough context to begin without reinterpreting the whole conversation;
- no later lifecycle claim is implied before its evidence exists.

## Progressive Resources
- Deep guide: `references/stateful-routing-and-precedence.md`
- Existing matrix: `references/lifecycle-routing-matrix.md`
- Example: `examples/lifecycle-walkthrough.md`
