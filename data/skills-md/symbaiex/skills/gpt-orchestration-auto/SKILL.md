---
name: gpt-orchestration-auto
description: "Complete sustained engineering objectives through research, building, verification, and recovery. Use for explicitly requested /goal-style engineering work."
license: MIT
metadata:
  author: SYMBaiEX
  version: "2.3.0"
---

# GPT Orchestration Auto

Use installed GPT Engineer as the shared contract. This wrapper adds durable progress, not another
model policy. Preserve the selected parent. GPT-6 Astra is parent/orchestrator-only and never a
child; GPT-6.1 Sol and GPT-6 Luna are the only GPT Engineer child routes. Same-model is the default
under 6.1 Sol/Luna parents; an Astra, retired GPT-6 Sol, or existing GPT-5.6 parent needs an explicit
mixed-model GPT-6.1 Sol or GPT-6 Luna child. Native Claude execution remains provider-specific. No fleet is mandatory.

Record objective, scope, acceptance, authority, requirements, evidence, current stage and blockers.
Use native goal tools only when explicitly requested and available, following their exact lifecycle
and budget semantics. Otherwise use a compact private checkpoint; never claim automatic persistence
or scheduled continuation without runtime support. Skills installation is not dependency resolution.

Carry forward authorization and steering within the active task. Routine decisions remain autonomous.
Persistence does not authorize unlimited retries, spending, global setup, production writes, or
new scope. Use milestones and progress checkpoints; estimates and checkpoint intervals are not
automatic deadlines. Continue productive work for as long as needed within authorization and runtime
constraints, including multi-hour work and compaction. Honor explicit user/operator time and resource
limits; on exhaustion, retain evidence and report remaining work without claiming completion or
silently raising the limit. Reassess stalled attempts from evidence rather than elapsed time alone.

Research only uncertainty that affects a decision. Implement confirmed findings, integrate returned
artifacts, and verify accepted behavior. Later cycles are delta-only: reconcile Git drift and live
handles, reuse valid evidence, and rerun affected checks. Do not redispatch an unknown prior attempt
until its possible side effects are reconciled.

Use dependency-aware delegation only when independent work benefits the outcome. Inspect live
capacity, reserve bounded lanes and isolated disjoint write scopes, and keep one integrator. Workers
are not alone and must preserve concurrent changes. Consume completions continuously; keep required
integration barriers without waiting on unrelated lanes.

At interruption or completion, collect terminal handoffs and checkpoint open requirements. Teardown
only recorded task-owned agents, processes, listeners and candidates after preserving evidence.
Preserve shared MCP services, other tasks and unclassified processes. Do not use a generic Stop or
SubagentStop hook to force continuation.

Finish when acceptance and release evidence support the requested outcome. Reconcile every required
finding/check and finalize the journal truthfully on every exit. Report actual completion, external
verification/trust boundaries, and the next required action without inventing success.
