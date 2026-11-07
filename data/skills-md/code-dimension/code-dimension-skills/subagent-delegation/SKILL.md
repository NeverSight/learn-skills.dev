---
name: subagent-delegation
description: Delegate context-heavy or independently valuable work through compact context packets, reusable workers, and a shared validation ledger. Use only when the user explicitly requests subagents or delegation, or when an explicitly invoked orchestration skill requires it; authorization is not a quota.
metadata:
  author: code-dimension
  version: 1.0
---

# Pragmatic Subagent Delegation

Preserve the coordinator's context without increasing total work unnecessarily.
Delegation is useful only when its benefit exceeds context-transfer,
coordination, and review costs.

## Delegation Is Not A Quota

An explicit request to use subagents authorizes delegation but does not require
delegating every phase. Keep a phase with the coordinator unless at least one
of these advantages is concrete:

- an independent review or perspective is required;
- the phase spans enough files, consumers, or subsystems to materially burden
  the coordinator context;
- an independent context line can run in parallel without overlapping files or
  decisions;
- the worker will be reused for several phases sharing the same domain, files,
  decisions, and validation strategy.

Do not delegate status checks, small preflights, checkbox updates, formatting,
single-purpose command execution, integration, archive, final reconciliation,
or work whose handoff costs as much as doing it locally.

Before spawning, record a compact decision: phase, explicit delegation
advantage, context line, worker, and validation owner. Use a full matrix only
when multiple context lines or dependencies make the decision genuinely hard
to follow.

## Context Lines And Phase Grouping

One context line represents a domain or boundary whose artifacts, decisions,
and validation knowledge remain useful. Reuse its worker while that context is
valid.

Consecutive OpenSpec sections or plan phases may be assigned together when
they share files, decisions, and validation and no intermediate decision can
invalidate the next phase. Section numbers are reporting boundaries, not
automatic subagent turns. Stop between phases only for a blocker, required
independent review, unresolved decision, or real dependency.

Create a new worker when the domain, primary file set, ownership boundary, or
validation strategy changes materially. Never use a new worker merely to run
another command over the same context.

## Context Transfer

Use `fork_turns: "none"` by default. Workers share the filesystem and can read
the authoritative files directly; they should not inherit unrelated tool
outputs or prior discussion.

Use `fork_turns: "all"` only when the conversation is short and contains
essential, unrecorded decisions that cannot be summarized safely. State the
reason before spawning. Do not use it after large tool outputs or long task
history. A short bounded fork is acceptable only when its turns were
deliberately prepared as the context packet.

Before the first spawn, read
[the coordination protocol](references/coordination-protocol.md). Send paths
and decisions, not copied file contents. Include authorization and stop
conditions that exist only in conversation.

## Validation Ownership

Every check has one owner. Pass a compact validation ledger between agents and
reuse valid evidence while its inputs remain unchanged. Do not rerun a green
check merely because ownership changed.

- implementer: focused tests, lint, and invariants for its edits;
- reviewer: fresh analysis plus only the representative check needed to test
  an unsupported claim or risk;
- coordinator: missing integration checks and the final full-workspace gate;
- archive/reconciliation: specification, formatting, and diff hygiene only,
  unless code changed after the final code gate.

Documentation-only edits do not invalidate runtime tests. Invalidate a ledger
entry only when a changed input can affect that check.

## Execution

1. Coordinator resolves ambiguity, authorization, and architectural decisions.
2. Assign one context line with an exact objective, allowed files/tasks,
   required context paths, recorded decisions, stop conditions, and validation
   ownership.
3. Prohibit nested delegation unless independently justified and explicitly
   authorized.
4. Treat the worker's edit scope as exclusive until its final checkpoint.
5. Reuse the same worker through compatible phases without resending known
   context.
6. At completion, inspect the focused changed paths and one risk-relevant
   invariant. Do not repeat the worker's valid checks.
7. Coordinator owns integration, archive, registry reconciliation, and final
   reporting.

Parallelize only context lines with no overlapping files, contracts,
decisions, or pending dependencies.

## OpenSpec

The coordinator performs the initial apply workflow and reads every required
`contextFile`. Delegate implementation only after the change and edit boundary
are known. A worker may cover multiple numbered sections under one context
line when the grouping rule above holds, while reporting each section's task
state separately.

Do not delegate canonical synchronization, archive, parent reconciliation, or
the final integrated verification. A checked task is not validation evidence;
the validation ledger is.
