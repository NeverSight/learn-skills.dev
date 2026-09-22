---
name: ticket-driven-development
description: Execute an approved directory of dependency-linked Markdown tickets as a tested integration branch — bounded fresh workers, senior-guide/junior-implementer pairing for risky tickets, risk-based review, deterministic Git integration, resumable run state. Executes approved tickets; never authors them.
metadata:
  invocation: explicit-only
  omp-frontmatter: disable-model-invocation
---

# Ticket-Driven Development

Act as the **controller**. Convert an approved directory of Markdown tickets into a tested integration branch without expanding worker context unnecessarily. Keep scheduling, integration, state, and final acceptance in the controller; give each guide, implementation, or review worker one bounded assignment.

## Non-negotiable invariants

1. Work from one isolated integration branch; the user's primary branch and dirty checkout stay untouched.
2. Treat tickets as a dependency graph, not a list. Dispatch only tickets whose blockers have passed the required checkpoint.
3. Parallelize only confidently independent tickets. Concurrent writers get separate checkouts.
4. Give each worker one ticket and file pointers, not the parent conversation or every ticket.
5. Only the controller dispatches guide, implementation, review, or conflict-resolution workers — workers never recurse.
6. Require durable report files and compact returns: full diffs and detailed reports stay in files, reaching the controller as pointers.
7. Use deterministic Git commands for clean integration; a conflict agent is used only after Git demonstrates a conflict.
8. Cap ticket repair at two rounds, then stop, split, escalate, or ask for a decision.
9. Persist `state.json` and an append-only `ledger.md` as the run database — conversation memory is not durable.
10. Mark a ticket complete only after its change is reachable from the integration branch and its applicable checkpoint passes. Terminal statuses are canonical — a ticket with a commit ends `integrated`; artifact-only output ends `verified` with its report as evidence. Checkpoint outcomes and review verdicts are recorded in the ledger, never by restamping a status (`references/recovery.md` holds the full contract).
11. A source status claiming completion is a claim, not evidence: corroborate it against the repository before trusting it. Corroborated work is never redispatched.
12. Mutate the repository only when open work exists. When corroboration leaves no incomplete ticket, end the run with zero repository changes.
13. Pair medium- and high-risk implementation tickets: a senior guide plans from repository evidence, a junior implementer executes the plan. Review tier follows risk: high-risk tickets get one plan-aware review verifying both the plan's soundness and the diff's adherence; medium-risk tickets get a quick review on the fast tier with the guidance as an input pointer, escalating to the plan-aware review when the diff is beyond its depth (gate in `references/verification-policy.md`). Guidance is a durable, base-pinned artifact, never conversation memory.

## Read references only when needed

| Situation | Read |
|---|---|
| Parse or repair tickets, prepare worker briefs | `references/ticket-format.md` |
| Several ready tickets, wave planning, integration conflicts | `references/scheduling.md` |
| Classify risk, pairing gate, review depth, service preflight, repair | `references/verification-policy.md` |
| Start, resume, reconcile, or clean a run | `references/recovery.md` |
| Map orchestration onto the active environment | `references/adapters.md` |
Bulk-reading references at preflight defeats this table: open one only when its situation row fires.

## Workflow

### 2. Preflight: repository safety, tooling, and run directory

Require an approved specification or substantial request, a local directory containing one Markdown file per ticket, and a Git repository. Ask only when a missing decision changes behavior, ticket boundaries, acceptance criteria, dependencies, or an irreversible design choice.

This skill executes tickets; ticket shaping happens before it. If tickets are absent or materially incomplete, stop and request ticket shaping. Minor metadata omissions may be inferred conservatively.

### 2. Inspect repository safety

Read applicable repository instruction files. Record the repository root, current branch, current `HEAD`, worktree list, and dirty status. Pre-existing user changes are left exactly as found.

Verify the environment can actually run the configured checkpoints before the first dispatch: discover the repository's own service and code-location tooling, measure what each checkpoint costs, and — when the invocation names a prior run's `repo-profile.json` that `scripts/repo_profile.py reuse` reports reusable — adopt its recorded commands and budgets and re-verify availability only. The full discovery, availability, worktree re-check, and background cost-probe procedure is in `references/verification-policy.md` ("Service availability preflight").

The guide role has one hard preflight dependency: the `i-have-adhd` skill file that shapes every guidance document. Resolve and read it per `references/adapters.md`; an unresolved dependency stops the run before any dispatch.
The `codegraph-cli` skill is the mirror image: a soft preflight dependency. When preflight finds a CodeGraph index, resolve the skill if it is installed and pass its path as the brief's code-locator detail pointer; when it is absent, the distilled CLI discipline that the locator block carries (`references/ticket-format.md`) still delivers the behavior. No run ever stops over it — indexing is the repository owner's decision, and grep/find remain the fallback.

Choose an ignored run directory such as `.scratch/<feature>/runs/<run-id>/` and verify with `git check-ignore` that it is actually ignored — repositories sometimes track `.scratch/`, in which case pick another ignored path or keep run state outside the repository. The integration worktree path must be outside the repository or ignored before creation.

### 3. Normalize and validate tickets

Run:

```bash
python3 <skill-dir>/scripts/index_tickets.py <ticket-dir> \
  --output <run-dir>/ticket-index.json
```

Stop on duplicate IDs, missing fields, unresolved blockers, dependency cycles, or a zero-ticket index — an empty or mistyped ticket directory is an input error to surface, not a run to start. Begin setup only when `valid` is true for the ticket directory the invocation named; when it is false, report the validation errors and stop — never self-select another ticket directory. Read `references/ticket-format.md` when repairing tickets or preparing worker context.

### 4. Corroborate completion claims and compute open work

The index reports every ticket whose source status claims completion as a warning (the exact completed-status set is in `references/ticket-format.md`). Treat each claim as unverified until corroborated against the repository:

- **Corroborated** — commits, merged branches, tags, or changelog entries reachable from the recorded base that plausibly implement the ticket's outcome. Record the evidence (commit SHA or file) with the ticket. A corroborated ticket is complete: it satisfies its dependents and is never redispatched.
- **Uncorroborated** — the repository shows no trace of the claimed work. This is the user's decision, not the controller's: record a ruling request asking whether to reopen the ticket, and schedule nothing that depends on it until the user rules.

Run `scripts/corroborate.py --repo <repo> --index <run-dir>/ticket-index.json [--since <base-sha>]` as the scripted first pass; the controller adjudicates only `needs_review` and uncorroborated tickets — corroborated-by-script tickets take the **Corroborated** path with the commit SHA as recorded evidence.

If corroboration leaves no incomplete ticket, stop and report the directory as a historical record: no integration branch, worktree, `state.json`, or ledger, and the repository exactly as found. Continue to setup only when open work remains or the user reopens a claim.

### 5. Create the integration branch and worktree

With open work confirmed, create a branch such as `agent/<feature>/integration` at the recorded base SHA. Prefer a real integration worktree that isolates the run from the user checkout:

```bash
python3 <skill-dir>/scripts/make_worktree.py \
  --repo <repo> \
  --path <integration-worktree> \
  --branch agent/<feature>/integration \
  --start <base-sha> \
  --metadata <run-dir>/workspaces/integration.json
```

If the active environment cannot move the controller into that worktree, keep the controller read-only in its original checkout and use absolute paths for all operations in the integration worktree. Use environment-native isolated children only when they are based on this integration worktree; otherwise use explicit child worktrees.

A second checkout is a different environment, not just a different path: rerun the service availability command from inside the worktree and record the outcome. When a duplicate service would collide with a healthy one, point the worktree at the shared service; when the checkpoints themselves write to it, descend the service-isolation ladder ("Service availability preflight" in `references/verification-policy.md`). Record either decision.

Any baseline verification — a green base-suite run, a service check, a build probe — happens inside this worktree once it exists: even a read-only test run in the user checkout writes build artifacts into the user's tree.

### 6. Initialize durable state

Run `scripts/run_state.py init` as shown in `references/recovery.md`. Record inferred risk, pairing decisions, conflict domains, test commands, review policy, environment adapter, corroboration outcomes, and any ruling before dispatch.

On an existing run, follow the resume protocol in `references/recovery.md` and reconcile Git before doing new work.

### 7. Compute and classify the ready frontier

A ticket is ready only when every blocker is integrated and its required checkpoint passed. Infer missing conflict domains from a narrow repository inspection, using the repository's code-location tool when preflight found one. Read `references/scheduling.md` and choose:

- **Sequential:** one fresh worker in the integration worktree when only one ticket is ready, domains overlap, or risk is high.
- **Parallel:** fresh workers in isolated child workspaces when at least two dependency-independent tickets have confidently disjoint conflict domains, within the concurrency policy of `references/scheduling.md` (default four; a user-declared cap is authoritative). Writer concurrency and checkpoint concurrency are different budgets: code may be written in parallel while suite executions take seats, per the contention rule in `references/verification-policy.md`. Child workspaces provision in the background through the guide wave (`references/scheduling.md`), so a junior launches when both its `PLAN_READY` and its provisioned workspace exist and a guide never waits on an install.

Classify pairing per the gate in `references/verification-policy.md`: medium- and high-risk implementation tickets get a senior guide before their junior implementer; low-risk tickets and artifact-only tickets dispatch directly. A user-declared pairing override at invocation is authoritative. Record the decision per ticket in the ledger.

Record the chosen wave base. Start every parallel child from that exact integration commit.

Render the dependency graph for the record and the user's orientation:

```bash
python3 <skill-dir>/scripts/render_graph.py <run-dir>/ticket-index.json \
  --output <run-dir>/ticket-graph.md
```

Include the rendered diagram in your report of the ready frontier. This is a plan snapshot, presentation only — it never feeds scheduling (the live frontier is durable state), and a defect the user spots in it (wrong blocker, missing dependency, misjudged risk) is surfaced and resolved through ticket shaping or a user ruling, never by the controller rewriting tickets. Do not re-render per frontier change; render again only for the final report if the delivered shape is worth contrasting with the plan.

### 8. Dispatch bounded guides and implementers

Paired tickets dispatch a read-only senior guide first. Render `templates/guide-prompt.md` with the `i-have-adhd` skill path resolved at preflight: the guide reads the ticket and the code at the expected base, writes a bounded, repo-grounded plan to `<run-dir>/guidance/<ticket-id>.md`, and returns `PLAN_READY`, `NEEDS_CONTEXT`, `NEEDS_SPLIT`, or `BLOCKED`. Guides are read-only — batch sibling guides concurrently. Guides may also dispatch speculatively: while a wave's implementers are in flight, batch the guides of their known dependents concurrently, pinned to the current integration head as the expected base, and record the dispatch in the ledger as speculative with that expected base. Pre-pin only when the in-flight blocker's conflict domain is disjoint from the dependent's conflict domain — then drift cannot touch the guidance's named files. At junior launch, run `scripts/guidance_drift.py` against the actual base: immaterial drift re-pins with `--patch-base` (the re-pinned Base line is the junior's start SHA, satisfying the success contract); material drift regenerates the guidance once. The guidance is a reading-grounded plan, not a proof: a guide may execute at most one load-bearing snippet — the step whose failure would void the whole plan — in a scratch directory, never the full plan. A guide stop is handled exactly like an implementer stop, at guide prices: the gate exists to catch malformed tickets before a junior burns a workspace on them. On `PLAN_READY`, dispatch the junior implementer with the guidance pointer; when the junior's actual start SHA differs from the guidance base, run `scripts/guidance_drift.py` and regenerate only on material drift — `--patch-base` re-pins a plan that stayed valid.

Render `templates/implementer-prompt.md` for each ticket with `scripts/render_brief.py` (template plus a context file): the renderer errors on missing placeholders and warns on unused context keys, so both halves of the brief boundary — every assignment field present, nothing extra riding along — are enforced by the tool, not discipline. The judgment calls of what a brief carries (specification excerpts over whole files, dependency interface notes over transcripts, the ~20k-token initial-context target with 40k as the warning line, and citation resolution) live in the worker-brief boundary rules of `references/ticket-format.md`.

Use the adapter in `references/adapters.md`, including its role-to-model-tier mapping, and structured return fields when supported. A worker may finish as `COMPLETE`, `BLOCKED`, `NEEDS_CONTEXT`, `NEEDS_SPLIT`, or `FAILED`.

A stalled worker announces itself through silence, not failure. Its heartbeat is the observable evidence of progress: file changes in its workspace, a growing or freshly touched report file. The **stall window** — twice the longest checkpoint budget the assignment declares, fifteen minutes minimum — is the silence budget after which the worker counts as wedged: ping it once, and if another stall window passes with no change, cancel it, preserve the partial workspace, and either redispatch once from a fresh worker or complete the step yourself in the controller. A worker still running past its guidance's declared time-box plus half is equally stalled even with a heartbeat — slow grinding is a stall you are watching happen. Derive the window from declared budgets, never from median completed durations: when every worker is slow, a median window stretches to match and never fires. Cancellation also stops the processes the worker spawned — a test runner that outlives its worker keeps consuming the resources the next worker needs. Record the intervention, its window, and its reason in the ledger; a silently absorbed stall is a lost audit event. A window the user declared at invocation overrides these defaults.

Requirements discovered while workers are running reach them through one bounded channel: collection. Verify the returned report, and when evidence is missing, run that one scoped check yourself in the worker's workspace or dispatch a single follow-up naming the exact check and its timeout budget. A broadcast of new requirements into running workers multiplies across every seat — four juniors told to run the full suite before finishing become four suites contending for the same infrastructure, each stalling the others.

### 9. Verify and integrate each result

For a complete result, batch collection: verification, packaging, and state transition as one shell invocation per result rather than separate steps — controller round-trips between collection actions measured roughly a fifth of a four-ticket run's wall time:

1. Confirm the report exists and the claimed commit/patch belongs to the assigned base and workspace.
2. Confirm focused tests, a relevant component check, and self-review are recorded.
3. Package the complete change:

```bash
python3 <skill-dir>/scripts/package_diff.py \
  --repo <workspace> \
  --base <ticket-base-sha> \
  --head <ticket-head-sha> \
  --ticket <ticket-id> \
  --output <run-dir>/diffs/<ticket-id>.md
```

4. Route by review tier per `references/verification-policy.md`: high-risk tickets render `templates/reviewer-prompt.md` (plan-aware reviewer receives the guidance and labels each blocking finding `IMPLEMENTATION` or `PLAN`, routing repair to the junior or back to the senior guide); medium-risk tickets and unguided low-risk tickets that cannot skip review render `templates/quick-reviewer-prompt.md` on the fast tier — for a paired medium-risk ticket the guidance document rides along as an input pointer for context, never as a plan judgment. An `ESCALATE` verdict re-renders the full reviewer prompt once with the guidance pointer empty.
5. If approved, integrate with deterministic Git. Confirm the ticket head is an ancestor of the integration head, then check elision before scheduling any smoke command: when the worker-verified and integration tree hashes are equal (routine after a clean cherry-pick onto an unmoved base), record both hashes with `scripts/run_state.py checkpoint --ticket <id> --kind elision --outcome pass --evidence "<worker-hash> <integration-hash>"` and stop there. When the trees differ, run the smoke scoped to the ticket — its focused suite plus the components its diff touches, selected with the repository's affected-test selector recorded at preflight (per the "Affected-check selection" section of `references/verification-policy.md`) — and record the outcome with `scripts/run_state.py checkpoint --ticket <id> --kind smoke --outcome pass|fail --evidence "<command + result>"`.
6. Persist every transition with `scripts/run_state.py transition --quiet`, recording measurements from the worker result at collection time — duration and context size are only reliably observable now, and backfilled numbers are guesses. Pass `--integration-head <new-tip>` on every transition that records an integration, so the state's recorded integration head tracks the branch it certifies — `state.json` is the resume authority, and a head left at the base SHA is a lie a later resume pays for.

A result with no repository change ends `verified`: confirm its artifacts landed at their assigned run-directory paths, with the report as evidence. A result with a commit ends `integrated`, per invariant 10.

For review failure, route repair by finding label — `IMPLEMENTATION` findings to a repair worker with the unchanged guidance, `PLAN` findings back to the senior guide for one revision — under the repair caps, senior-touch limit, and resume-or-fresh rules of `references/verification-policy.md` ("Review and repair").

For a real merge conflict, preserve both sides and render `templates/conflict-resolver-prompt.md`. A general merger agent never reinterprets a clean integration.

### 10. Advance by waves

Advance per ticket, not per wave: as soon as one ticket's integration checkpoint passes, recompute the frontier from durable state and dispatch newly ready work — a dependent waits on its blocker's checkpoint, never on a sibling still under review. Only high-risk runs keep a wave-wide barrier (smoke before any further dispatch). Reviews of independent tickets are read-only: batch them concurrently instead of serially. Newly unblocked work starts from the updated integration head. Repeat dispatch, verification, and integration until no incomplete ticket remains or the run becomes blocked.

When no ticket is ready but incomplete tickets remain, diagnose an invalid state, unresolved failure, or unrecorded ruling.

### 11. Run the final gate

Package the full original-base-to-integration-head diff. Run the configured full suite and the requirements-aware final branch review (`templates/final-review-prompt.md`) concurrently — both are read-only against the same final head. Give the review the controller's recorded evidence as input pointers — per-ticket suite outcomes, reviewer oracle results, and packaged diffs — and it runs a command only for a criterion no recorded evidence covers. After a fix wave the suite reruns only when the fix changed code.

If changes are requested, dispatch the fix wave per `references/scheduling.md` ("Dispatch a fix wave") — consolidated in the integration worktree by default, parallel child worktrees only for disjoint fix requests — then one scoped re-review. True up durable state first: run `scripts/reconcile_run.py --state <run-dir>/state.json --apply` so the recorded `integration.head_sha` equals the delivered head — fix-wave commits land after the last ticket transition and would otherwise leave state stale. Mark the run complete only when all intended tickets are integrated, required checks pass, and the final verdict is `PASS`.

### 12. Measure, report, and clean up safely

Measure critical-path wall time per accepted change rather than worker count. Record duration and worker context size at collection time — `run_state.py` derives ticket duration from its recorded timestamps, and the dispatch result (on OMP and ZCode, the task completion notification) is the only place token totals exist before they are gone. Summarize ticket duration, worker context size, agent seats, senior and junior model tiers used, review tiers with escalations, guidance generations, repair rounds, merge conflicts, worktree overhead, and human interventions. Treat routine worker context above 64k tokens, mandatory merger agents on clean integrations, frequent parallel conflicts, workers running the repository's full suite, checkpoint processes that outlive their worker, and suites queued on shared infrastructure as policy failures to investigate rather than normal costs.

Report the integration branch and head, completed tickets, exact tests, review outcomes, rulings, corroboration outcomes, deferred observations, unresolved risks, measurements, and workspace disposition. Distinguish passed, failed, and skipped checks.

Offer cleanup. Remove only integrated child worktrees that hold nothing beyond regenerable build artifacts (`__pycache__`, caches, `node_modules`, `dist`, build output) — `git worktree remove --force` is safe only after confirming that residue is all there is; a workspace with real uncommitted changes is never force-removed. Never delete the run ledger or branches without explicit user instruction. Keep the run directory in the main checkout's ignored path (or outside the repository) — never inside a worktree that teardown removes — so the ledger, reports, reviews, and guidance survive cleanup as the run's audit record.

## Success contract

A successful run produces:

| Artifact | Requirement |
|---|---|
| Integration branch | Contains every accepted ticket commit and no unreviewed conflict resolution. |
| `state.json` and `ledger.md` | Reconcile with Git and support restart without redispatching integrated work. |
| Guidance documents | Bounded and repo-grounded for every paired ticket, pinned to the junior's start SHA, with plan adherence recorded in each implementer report. |
| Ticket reports and reviews | Provide acceptance evidence through file pointers. |
| Final diff package | Covers the complete base-to-head change. |
| Ticket graph (`ticket-graph.md`) | Plan-snapshot Mermaid DAG rendered from the ticket index at frontier time; presentation only, never a scheduling input. |
| Verification record | Lists exact commands and truthful outcomes. |
