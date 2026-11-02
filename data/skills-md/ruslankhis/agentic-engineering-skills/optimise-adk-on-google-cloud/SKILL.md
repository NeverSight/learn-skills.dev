---
name: optimise-adk-on-google-cloud
description: >-
  Diagnose, implement or review Python Google ADK optimisations on Cloud Run,
  Agent Runtime and GKE involving model/tool work, in-session history and
  context growth (trimming, summarising), streaming completion, session
  handling, startup, concurrency or workload scaling. Use for measured changes
  or actionable optimisation plans. Do not activate for hosting selection or
  first deployment alone (deploy-adk-on-google-cloud), general Kubernetes
  administration, cross-session memory or RAG architecture
  (adk-memory-architecture), model choice or thinking settings
  (adk-model-and-output-contracts), production alerting and SLOs
  (adk-agent-observability), non-ADK performance work, or unrelated prompt and
  UI edits (adk-agent-instructions owns prompt wording).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "4"
  source-part: "1,2,3"
  last-tested: "2026-09-16"
  verified-against: "google-adk 2.8.0 companion runs and package tests 2026-09-16; 2.12.0 source read 2026-10-25"
  version: "2026.10.28"
---

# Optimise ADK on Google Cloud

Reduce avoidable work while preserving correct, authorised and complete results.
This one skill covers all three parts of Chapter 4: application optimisation,
Cloud Run, Agent Runtime and GKE. The book and companion repository are optional
provenance, never runtime dependencies.

## Inspect and define acceptance

1. Read project instructions, status, dependency declarations and locks, agent
   exports, serving and tool code, deployment definitions and relevant tests.
   Establish whether the user wants advice, an audit, an implementation or a live
   comparison. Preserve the domain, package manager, versions and customisations.
2. Use the existing project interpreter. The read-only
   [project inspector](scripts/inspect_project.py) (its baseline gate records
   ADK 2.8.0; `baseline_gate_passed: false` on a newer pin means "not the
   recorded baseline", so read the dated 2.12 notes in the references rather
   than treating it as a project failure) accepts `--project`, `--mode`
   (`auto`, `application`, `cloud-run`, `agent-runtime`, `gke`) and `--require-baseline`. It reads bounded
   dependency manifests and reports configuration presence; it does not import
   application code, read `.env` contents or execute cloud commands. Manually
   inspect its uncovered files and lock resolution. Read
   [compatibility.md](references/compatibility.md) before using an ADK recipe.
   Compare installed distribution metadata with declared Python and ADK pins.
   A mismatch requires contract verification or a specific blocked path, never
   an automatic upgrade or downgrade.
3. Trace the actual request: server and session service, ADK `App` or bare agent,
   model requests, tools, child handoffs, result storage and client consumption.
   Record model/backend and configuration keys without exposing secret values.
   Nested environment files can override root configuration. Inspect the image's
   actual source package and entrypoint, not just a similarly named example.
4. Separate external request time, platform startup/queueing and application
   spans. Identify one candidate boundary and its evidence. If measurements are
   absent, deliver an instrumentation/comparison plan; do not invent a bottleneck.
   Define correct output, permitted effects, completion, work limits and relevant
   quality checks before selecting an optimisation.

Inspection ends with the current architecture, version status, selected mode,
acceptance criteria and missing prerequisites. Missing cloud credentials still
permit local inspection, implementation and offline validation.

## Select the smallest useful mode

| Observed work or requested decision | Read when entering this mode | Evidence needed |
| --- | --- | --- |
| Remote adapter overhead, repeated schema, oversized results, unnecessary child history/output or serial independent I/O | [Application path](references/application.md) | Same authorised result, bounded handoff, complete answer and relevant request-boundary observations |
| Large repeated instructions or uncertain prefix-cache benefit | [Skills and cache](references/skills-and-cache.md) | Actual instruction loading or outgoing request/usage metadata, with correctness and separate cache lifecycle |
| Long sessions, token growth per turn, cache misses, oversized tool results or sub-agent context isolation | [Context window](references/context-window.md) | Captured request composition, cached-token counts, bounded tool results and preserved correctness |
| Cloud Run startup, concurrency, CPU allocation, session locality or revision comparison | [Cloud Run](references/cloud-run.md) | Effective revision configuration, external/platform/application measurements and state/security checks |
| Agent Runtime session reuse, App/compaction propagation, model or hosting work | [Agent Runtime](references/agent-runtime.md) | Actual execution location, retained session events, selected model input and observed capacity |
| Agent Runtime streaming, buffered persistence, optional memory writes or deferred jobs | [State and streams](references/runtime-state-and-streams.md) | Complete outputs, bounded admission, immutable batches and correctly correlated recovery |
| GKE startup, resources, rollout capacity, scaling or identity delays | [GKE workload](references/gke.md) | Actual manifest generator/build inputs, admitted Pods, scheduling events and pressure measurements |
| GKE session continuity, HTTP/draining, tracing privacy or streaming | [GKE serving path](references/gke-serving.md) | Wired session backend, trusted caller, complete responses and final exported telemetry |
| Optimisation review or greenfield design without measurements | Read only the relevant references above | Prioritised hypotheses, concrete implementation seams and a validation plan; no claimed speedup |

Combine modes only when the request needs them. A general deployment, SQL
security overhaul or UI rewrite is not an implied optimisation task.

## Implement or recommend

1. Present a short plan before broad changes: affected files, one principal
   mechanism, preserved behaviour and validation. For advice/review, provide the
   decision and actionable changes without generating an unsolicited application.
2. Adapt the current implementation. Keep trusted policy at tool/backend
   boundaries; model instructions, Skills and structured output cannot grant
   access. Wire new components into the actual Runner/server and build inputs.
   An unused formatter or unshipped file is not an implemented optimisation.
3. Preserve explicit failure and uncertainty. Provider failure must not become
   fabricated fallback data. A token cap, timeout, nonempty answer or HTTP 200
   does not establish completion. Limit logical calls, provider attempts,
   nested work and elapsed time independently where the task needs bounds.
4. Read [lifecycle.md](references/lifecycle.md) before preparing a cloud mutation,
   paid comparison, export, cache experiment or cleanup. Finish reviewable
   configuration and exact commands before seeking approval.
   For Agent Runtime packaging or operation recovery, also read
   [runtime-lifecycle.md](references/runtime-lifecycle.md).
   For GKE deployment, capacity retries or teardown, read
   [gke-lifecycle.md](references/gke-lifecycle.md). A saved reference manifest is
   not necessarily the applied configuration; inspect the actual delivery path.

## Authority and safety

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

Billing linkage and quota increases require their own approval. Verify owned
cleanup of caches separately from sessions.

## Validate and finish

Read [validation.md](references/validation.md) for mode-specific tests, the
offline [saved-event checker](scripts/check_run.py) and the offline
[context budget helper](scripts/context_budget.py), which estimates request
composition, tool-result sizes and compaction coverage from a saved session
export. Run relevant local tests
and static/build checks first, after inspecting their side effects. Check the
actual boundary: tool results and correlation, outgoing child input, complete
outputs, result durability or revision configuration. Mocked execution proves
only the exercised local contract. Historical companion PASS results do not
verify this target.

For an approved live experiment, retain failed observations, compare equivalent
workloads and report sample counts, cold/warm/cache state and errors. Verify
owned cleanup, including caches separately from sessions. Repeat the local
adaptation to check for duplicate wiring or needless changes.

Report files changed, commands actually executed, exact versions, actual results,
manual steps and remaining uncertainty. State what the change improves and
what the evidence cannot establish.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
