---
name: adk-workflow-design
description: >-
  Select, implement or review Google ADK workflow control flow, event
  consumption, session-state handoffs, callbacks and checkpoints. Use when
  choosing between ordinary code, sequential, parallel, bounded-loop, graph or
  dynamic orchestration, or repairing those runtime contracts in an existing
  agent: output_key handoffs where a later agent's {key} placeholder stays
  literal or raises KeyError, reusing saved stages after an input changed, a
  checkpoint too large for its store, a run waiting days for approval across
  restarts (ADK resume or a durable engine), draft consistency checks in code
  and warning-only corrections. Do not activate for unrelated UI edits,
  general LLM explanations, standalone cloud deployment, implementing RAG,
  memory or SQL services, instruction wording or sub-agent descriptions
  (adk-agent-instructions), remote A2A agents or MCP servers
  (adk-agent-interoperability), or an injection threat model
  (adk-agent-security).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "00"
  last-tested: "2026-09-16"
  verified-against: "google-adk 2.8.0 companion run 2026-09-16; 2.12.0 CHANGELOG read 2026-10-22"
  version: "2026.10.28"
---

# ADK workflow design

Produce the smallest justified orchestration change, or an actionable design/review
when implementation is not requested. Establish what constitutes a usable result,
how work stops, and which evidence supports the outcome. The skill is self-contained;
the book and companion repository are optional provenance, not prerequisites.

## Inspect before selecting a pattern

1. Read project instructions, status/diff, manifests and lockfiles, entry points,
   existing tests and startup/cleanup commands. Preserve the package manager,
   conventions and unrelated changes. Inspect configuration names without printing
   credential values or importing application modules just to inspect them.
2. Record the target Python, ADK and GenAI versions, model/backend, current result
   contract, state ownership, side effects and relevant test commands. Use the
   existing project interpreter. The read-only helper can provide an initial map:

   ```bash
   python "$SKILL_DIR/scripts/inspect_project.py" --project .
   ```

   Resolve `SKILL_DIR` to this skill's installed directory. Read
   [compatibility.md](references/compatibility.md) before using an SDK recipe or
   interpreting the helper. A different/missing version blocks claims of tested
   compatibility; independent planning continues. Resolve the target API
   contract or report the exact blocker, keeping dependency pins as they are.
3. Define acceptance in observable terms: ordered handoff, two preserved branch
   outputs, bounded refinement with an explicit result, typed node output, or a
   callback action. For example, "the reviewer node receives the writer's
   actual draft text, and a reviewer exception leaves the draft saved and the
   run marked failed" is acceptance; an import or an HTTP 200 is a precondition.
   List missing prerequisites together. Ask for the decisions only the user
   can settle and continue independent offline work meanwhile.

Inspection is complete when the chosen mode, version baseline, output contract
and validation path are known, or their specific blockers are recorded.

## Choose a mode

| Need | Mode and next reference |
| --- | --- |
| Known rules; no model judgement needed | Prefer ordinary Python. Use [orchestration.md](references/orchestration.md) only if ADK coordination adds value. |
| Fixed order, independent concurrent work, bounded refinement, typed graph, or runtime-sized work | Selection/implementation/review: read [orchestration.md](references/orchestration.md). Preserve an existing supported pattern unless changing it solves the requested problem. |
| Missing final result, lost state, streaming, restart or paused-run semantics; a worker restart that re-ran a tool; a pause of days; choosing resume or a durable-execution engine | Runtime contract: read [runtime.md](references/runtime.md), "Resume and durable execution are different promises". |
| Saved-stage continuation, changed dependencies during recovery, or a checkpoint or saved artifact too large for its store | Checkpoint qualification and the storage-limit check: read [checkpoint-reuse.md](references/checkpoint-reuse.md) before reusing artifacts, writing a checkpoint or dispatching a continuation. |
| Logging hooks, deterministic short-circuits, tool visibility or call-time policy | Callback boundary: read [callbacks.md](references/callbacks.md). |
| Local startup, actual HTTP/UI checks, buffering, timing or retained sessions | Reader/runtime operation: read [local-runbook.md](references/local-runbook.md). |

Modes can combine within one task. Read only relevant references. Cloud hosting,
retrieval, long-term memory and tenant authentication may be architectural
recommendations; implementing them is a separate scope decision.

When the project has `agents-cli-manifest.yaml`, consult the installed
`google-agents-cli-adk-code` skill (`references/adk-python-workflows.md` for
the graph API, `references/adk-python.md` for `SequentialAgent`,
`ParallelAgent` and `LoopAgent`, or the `ambient-expense-agent` and
`deep-search` recipes in `google/adk-recipes`); if it is not installed,
adk-engineer explains how to get it. Keep this skill's acceptance contracts;
the scaffold's conventions (agent code in `app/`, `App(name=)` equal to that
directory name for `agents-cli eval`) are project facts to preserve, not
design decisions.

## Implement or advise

1. Present a short plan before broad edits. For a planning/review request, give
   the selected pattern, alternatives that materially affect the decision, output
   contract, failure boundaries and acceptance plan; stop short of generating an
   unsolicited application.
2. For authorised implementation, reproduce the reported failure through the
   public runner, CLI, HTTP or UI path before a narrow correction. Reuse existing
   orchestration and change only the boundary causing the defect. Keep a regression
   case. Greenfield work starts from the actual user task.
3. Account for each output, model/tool attempt and state writer. Authorisation
   lives in code, a request budget in a reservation before dispatch, and
   exactly-once execution in an idempotency key; a prompt, a loop limit and a
   checkpoint each do a different job. Label simulated inputs/results explicitly.
4. Keep proposed production controls distinct from implemented controls. Add
   deadlines, idempotency, persistence or observability when the task requires
   them, and validate each claim. Derive limits and identities from the new
   project's own measurements; a historical campaign's numbers are provenance.

## Authority and external work

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Present the execution window with the request and retry limits. Read
[external-validation.md](references/external-validation.md) only when
real-service acceptance or cloud prerequisites are in scope.

## Validate and finish

Follow [validation.md](references/validation.md) for mode-specific assertions,
offline boundary doubles, browser timings and a concise result format. Run the
project's relevant tests and static/build checks, including a real application
path where applicable. Prove concurrent branches overlap, state survives only as
claimed, and a failed branch yields a failed result. Repeat setup/adaptation to
check that it preserves existing work rather than duplicating it.

For structured review/correction, read [review-contracts.md](references/review-contracts.md)
before tuning model reliability: pass honest references for decisive and
nondecisive issues, required controls and unresolved/contradictory evidence through
the actual schema, checker and Runner/served boundary. Solvability is shown by
an honest reference that keeps every obligation and passes.

When a drafting stage produces officer-facing decisions, read
[content-safeguards.md](references/content-safeguards.md): check internal
consistency in code on every fresh draft (a condition cannot require what a
reason waives; a refusal carries no conditions), rank warnings by whether
they could change the decision, treat source documents as data, and ask the
reviewer for the strongest objection. When a model check's verdict stops the
run or sends a case to a person, re-check its costly verdict in code (its
"Re-check the verdict whose error costs most" section).

For strict paid-request limits, SDK retries or campaign restart, read
[model-call-controls.md](references/model-call-controls.md) before choosing the
enforcement point: a transport cap is enforced where the HTTP attempt is made,
with a callback counter as the observer.

Report changed files, exact commands and versions, actual outcomes, warnings,
manual prerequisites and outstanding work, giving an outcome for offline
execution, live behaviour, browser functionality, latency and cleanup as
applicable. Historical companion results are provenance for the rule, not the
pass for the target project.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

This is an independent community project, not affiliated with or endorsed by Google.
