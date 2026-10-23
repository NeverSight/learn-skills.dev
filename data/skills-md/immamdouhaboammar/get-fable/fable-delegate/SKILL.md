---
name: fable-delegate
description: "Delegate independent subtasks to parallel workers or subagents with strict disjoint ownership, bounded scope, and explicit acceptance contracts. Use when coordinating multiple independent tasks, parallelizing multi-file work without merge conflicts, or managing subagent task assignments — even if the user does not explicitly say \"fable-delegate\" (e.g. \"split this work among workers\", \"delegate these subtasks\", \"run parallel agents\", \"assign independent pieces\"). Do NOT use for tightly coupled sequential tasks or when shared mutable state causes edit collisions."
version: 1.3.0
pack: build
inputs:
  - bounded_cards
requires:
  - disjoint_ownership
produces:
  - delegation_contracts
  - worker_results
gates:
  - ownership_explicit
  - acceptance_explicit
fallback: fable-plan
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-plan
  continuations:
    - fable-execute
    - fable-verify
  lateral_peers:
    - fable-tdd
  recovery: fable-recover
---

# Fable Delegate

Use parallel workers when independence is real, not merely because there are multiple tasks.

## Mission
Delegation should reduce latency without multiplying ambiguity. The parent remains responsible for decomposition, contract stability, integration, and final proof.

A worker is not a place to dump context. It receives one bounded responsibility with enough evidence to act independently and a return contract that makes integration reviewable.

## Activate When
- two or more cards can proceed without waiting for each other's decisions;
- specialist perspectives can investigate independent hypotheses in parallel;
- separate components have stable interfaces and independent acceptance checks;
- independent review/research can be parallelized without shared mutation.

## Do Not Activate When
- workers would change the same unstable contract or invariant;
- one card's design result changes another card's requirements;
- a tiny task costs more to explain/integrate than to execute;
- the parent has not established enough context to write precise worker contracts;
- all workers depend on one unresolved architectural decision.

## Independence Classification
For each candidate pair, classify coupling:

| Coupling | Parallel? | Why |
| --- | --- | --- |
| Different files + different contracts | usually yes | low semantic overlap |
| Different files + shared unstable contract | no | semantic conflict despite path separation |
| Same integration file + separate components | maybe, but serialize integration | component work may parallelize; integration does not |
| Shared read-only evidence | yes | no ownership conflict |
| Same database schema/invariant | usually no | one worker can invalidate another's assumptions |
| Independent research hypotheses | yes | merge conclusions, not source edits |
| Parent decision required by both | no | resolve decision first |

## Delegation Protocol

### Stage 1 — Prove independence
Check:
- write ownership;
- shared contracts/invariants;
- dependency order;
- generated artifacts;
- migration/state coupling;
- integration hotspot;
- whether one worker failure changes another worker's assumptions.

If independence cannot be explained in one short paragraph, do not parallelize yet.

### Stage 2 — Write a worker contract
Each contract includes:
- objective;
- context/evidence already established;
- owned paths or semantic area;
- forbidden scope;
- dependencies assumed stable;
- acceptance evidence to produce;
- expected return packet;
- stop/escalation conditions.

Do not ask a worker to "handle X" with an entire repository and no boundary.

### Stage 3 — Decide mutation ownership
Prefer one writer per semantic area. Multiple read-only investigators may inspect overlapping files; multiple writers should not independently redefine the same contract.

For a shared integration file, assign integration to the parent or one named worker after component work converges.

### Stage 4 — Dispatch and supervise by exception
Do not micromanage every command. Intervene when:
- worker discovers a load-bearing unknown;
- owned scope must expand;
- acceptance cannot be satisfied;
- contract assumption is false;
- worker stalls/repeats failure.

### Stage 5 — Inspect returns, not summaries alone
Require concrete artifacts: diff/paths, commands/results, evidence, unresolved risk. A prose "done" is not integration evidence.

### Stage 6 — Integrate centrally
The parent checks:
- combined diff;
- contract compatibility;
- cross-worker behavior;
- generated artifacts;
- integration tests;
- whether worker-local evidence is still fresh after merge/integration mutations.

## Decision Rules
- Different files are neither necessary nor sufficient for independence.
- Stable contract + isolated implementation can parallelize; unstable contract + separate files should not.
- If workers produce competing approaches, keep them read-only until the parent chooses; do not merge both experiments blindly.
- If a worker needs to cross ownership boundaries, pause that worker and renegotiate the contract instead of silently expanding scope.
- A failed/hung worker does not automatically justify rerunning the same prompt; classify failure and route the card to `fable-recover` or execute locally.
- Parent integration verification is mandatory whenever delegated work affects one user-visible behavior.

## Invariants
- Every mutable surface has clear ownership.
- Workers receive only the context needed to make their bounded decisions.
- Worker completion never equals global completion.
- Shared contract changes have one integration owner.
- Combined workspace is verified after all integration mutations.

## Failure Taxonomy
### Ownership collision
Two workers need the same mutable contract/file. Stop parallel mutation and replan ownership.

### Semantic collision
Files differ but both change one invariant/schema. Treat as coupled work.

### Context starvation
Worker repeatedly asks questions the parent should have resolved. Improve contract or route back to discovery/plan.

### Scope escape
Worker finds necessary work outside ownership. Pause, evaluate, then expand/replan explicitly.

### Worker-local green / integration red
Local checks pass but combined behavior fails. Parent owns diagnosis; do not bounce workers blindly.

### Worker stall
No meaningful progress or repeated failure. Terminate/recover rather than consuming unbounded budget.

## Anti-Patterns
- "two tasks = two agents";
- path-disjointness as the only parallelism test;
- giving every worker the entire broad task;
- allowing each worker to update shared manifests/routes independently;
- accepting prose summaries without diffs/evidence;
- merging worker outputs before inspecting assumptions;
- assuming subagents transfer responsibility away from the parent;
- delegating a decision the parent has not made simply to avoid making it.

## Mandatory TOON Delegation Protocol

All subagent delegation contracts and worker return packets MUST use **TOON (Token-Oriented Object Notation)**. This guarantees:
1. **Token efficiency**: 35-70% fewer tokens compared to verbose markdown/JSON.
2. **Deterministic parsing**: Explicit length tags `[N]` allow the parent agent to instantly detect truncated or dropped tasks.
3. **Structured schema**: Field headers `{fields}` enforce contract compliance.

### Boss → Worker Delegation Contract (TOON)
```toon
contract:
  workerId: worker-1
  targetCard: CARD-101
  objective: "Implement JWT authentication guard"
ownedPaths[2]: src/auth/guard.ts,test/auth/guard.test.ts
forbiddenPaths[2]: src/config/keys.ts,.env
acceptanceChecks[2]: "bun test test/auth/guard.test.ts","bun run typecheck"
rules[2]: "Do not touch files outside ownedPaths","Use TOON format for the return packet"
```

### Worker → Boss Return Packet (TOON)
```toon
result:
  workerId: worker-1
  targetCard: CARD-101
  status: complete
  allChecksPassed: true
mutations[2]{path,action}:
  src/auth/guard.ts,modified
  test/auth/guard.test.ts,created
verifications[2]{command,result,durationMs}:
  "bun test test/auth/guard.test.ts",pass,120
  "bun run typecheck",pass,340
notes[1]: Successfully implemented guard with full test coverage
```

## Completion Criteria
Delegation is complete when:
- every worker contract had explicit ownership and acceptance;
- returned artifacts/evidence were inspected;
- ownership/contract conflicts are resolved;
- combined diff passes integration verification on the current workspace;
- residual failures are routed explicitly rather than hidden in worker summaries.

## Progressive Resources
- Deep guide: `references/parallelism-and-integration.md`
- Existing contract guide: `references/subagent-contracts.md`
- Template: `templates/delegation-contract.template.md`
- Example: `examples/parallel-workers-walkthrough.md`
