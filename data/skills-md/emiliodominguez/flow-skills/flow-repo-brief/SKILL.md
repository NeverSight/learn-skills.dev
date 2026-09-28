---
name: flow-repo-brief
description: "Maintained, source-cited brief for a subsystem that agents reuse across sessions. Use when agents keep rediscovering conventions and commands, or agent notes on a subsystem need refreshing against source. Feeds `flow-plan` and `flow-specialize`."
metadata:
  stage: understand
---

# Repository brief

Capture the facts that change implementation decisions, with sources another agent can reopen.
A brief is maintained evidence, never an authority above user or repository instructions.

## Phase 1: Bound the question

- Identify the task or subsystem and the next consumer. Read agent instruction files (for example AGENTS.md), manifests,
  lockfiles, lint/format config, CI and representative nearby code. Trace one real flow before
  describing architecture. Use `flow-onboard` first if a broad tour is needed; do not scan the
  whole repository for a narrow change.
- Write to the user's knowledge location, else `.plans/context/<topic>.md`. Preserve tracked or
  ignored status and say when an ignored file is local-only. Do not change global instructions,
  ignore rules or installed skills as a side effect.

## Phase 2: Separate fact from inference

Cite a path plus symbol or line range at the recorded revision for every load-bearing claim;
add command output for operational claims. Capture:

- Repository identity, branch, commit, date, scope, relevant dirty/untracked files.
- Constraint provenance: explicit instruction, executable config, repeated precedent, or
  inference. One example is not a universal rule.
- Entry points, ownership boundaries, key types/contracts, one real data flow.
- Exact build/test/lint commands and cwd, each marked `run`, `observed in config`, or
  `unavailable`, with actual outcomes.
- Reusable patterns, exceptions, failure modes and areas the task must not change.
- Assumptions and hypotheses, each with the evidence that would confirm or falsify it.

Record variable names and required access, never secrets or private payloads. For uncertain
external API facts, prefer primary docs or pinned source and record the version and date.

## Phase 3: Write for selective reading

Keep it small enough to use directly. Use a claims table:

| Claim | Kind | Source at revision | Confidence / unresolved evidence |
| --- | --- | --- | --- |
| Function declarations and four-column tabs | config or instruction | actual file and key | confirmed or unknown |

Add scope, architecture, commands, conventions, hypotheses and refresh-trigger sections only
when task-relevant. Split large subsystem detail into linked sibling files with an index of what
to read per task. No copied source, transcripts, file listings or framework tutorials.

## Phase 4: Refresh and verify

Reopen the sources behind claims the next task relies on. Compare current instructions, config,
source and dependency versions with recorded inputs: changed cited inputs invalidate claims, an
unrelated commit does not. Mark unsupported claims stale and update only affected sections. A
date alone never proves old evidence valid. For consequential decisions, have an independent
pragmatic verifier check claims and hypotheses via `flow-verify`; missing verification stays visible.

## Anti-patterns

- "Uses DDD" or "all IDs are opaque" without types and boundary evidence.
- Copying another repository's preferences over this one's conventions.
- Calling a command verified when it was only found in package.json.
- Treating a stale brief as permission to ignore live source or user scope.

## Done when

- The next worker can find relevant code, conventions, commands and open questions.
- Load-bearing claims have citations and a current or explicitly stale status.
- The artifact path and refresh conditions are recorded.

Hand off to `flow-plan` for decomposition or `flow-specialize` for a repository-specific worker.
