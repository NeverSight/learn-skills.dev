---
name: gantry
description: Harness-neutral agentic SDLC workflow. Resolves ready Issues deterministically, plans only to operator approval, implements with TDD, reviews against standards and Spec, and accepts delivery only after adversarial verification.
argument-hint: <spec-slug | spec#NN | wave:N | frontier | all | "Implement the <slug> Spec" | "free-text goal"> [--limit N] [--budget N]
---

# Gantry

Gantry is a harness-neutral skill pack, not an execution engine. Workflow scripts decide readiness,
acceptance, gates and roadmap state; agents plan, implement, review and refute; the operator makes
approval decisions in the host harness.

```
preflight → models → frontier.py → planned round loop
                         └→ spec.py --check → Requirement Critic → research → draft plan → critique
                            → STOP for operator approval
round: implement (TDD) → review (standards + Spec) → Critic → serial integration → roadmap.py done
```

## Resolve the portable runtime

Before a Run, resolve these values once and pass them as `args` to every reference workflow:

1. `skillDir` is this `gantry` directory as an absolute real path. A harness-specific symlink resolves
   through `realpath`; never assume a fixed installation directory.
2. `repoRoot` is the enclosing Git repository or worktree (`common.repo_root()`).
3. `policy` is `common.resolve_policy(repoRoot)`: Gantry's sparse defaults overlaid by
   `<repoRoot>/.gantry/config.json` when present. A missing repository policy is valid.
4. `paths` comes from `common.resolve_workflow_paths(repoRoot, scopeSlug)`. Prompts receive paths, not
   repository-specific literals.
5. `caveman` comes from resolving repository preference `policy["caveman"]` and host availability
   via `caveman.resolve_activation(policy, harness=hostHarness, root=repoRoot, warned=args.cavemanWarned)`.
   When active, the coordinating agent, planning roles (Requirement Critic, research, Planner, Plan Critic)
   and round roles (Implementer, Reviewer, Critic, optional Learner) across all initial calls, retries,
   review fixes and correction passes receive concise phrasing instructions for conversational messages
   and summaries along with supported external-skill access, while all Specs, draft Issues, code,
   documentation, lesson candidates, PR descriptions, Result Contracts, exact commands, exact errors,
   acceptance criteria and verification evidence retain full detail. If enabled in policy but unavailable
   in the host environment, emit at most one actionable warning per Run with installation guidance and
   continue with normal behavior without claiming live token savings; a disabled preference does not load
   the skill. The manual harness-neutral path carries the same instructions.
6. `roles` comes from resolving repository defaults under `policy["execution"]["roles"]` overlaid by
   optional Run and Issue overrides via `execution.resolve_roles()`. Preflight validates that every selected
   combination is supported, executable, meets minimum installed harness version requirements, and authenticated
   (via `execution.preflight_validate()`), refusing to start implementation when validation fails. Derived roles
   (`requirement-critic`, `plan-critic`, `learner` inheriting from `critic`, and `research` from `plan`) adopt
   parent defaults unless explicitly set. Bounded native harness invocations execute roles across Codex CLI,
   Claude Code, OpenCode, and Antigravity (`agy --print`) while the Host Harness retains coordination. External
   results pass `result.py` contract validation, missing or invalid results trigger Protocol Failure handling,
   unsupported installed versions are rejected, Critic verification fails visibly on permission or tool limitations,
   selection identity is honestly recorded in the Run log, and native or configured automatic model fallback
   is detected and rejected. Runtime execution failures preserve work and pause the affected Issue separately
   from Critic refutations and protocol failures; independent Issues integrate serially, while the next round
   waits for explicit recovery without automatic fallback or retry. Explicit Issue-role replacements are
   validated and recorded via `role.changed`, leave saved repository defaults and running agents unchanged, and
   preserve spent correction budgets. Run log selection (`role.selected`) and change (`role.changed`) events
   record requested and effective selection evidence without command outputs or credentials. Model strength
   guidance between roles is advisory and does not block valid cross-family selections.

Run the standard-library workflow scripts as `python3 <skillDir>/scripts/<script>.py`. `common.py` provides
the shared Markdown parser and policy resolution; its `--json` path prints the resolved portable runtime.
Every script provides `--help`, and data-producing paths support `--json`.

## Workflow rules

- Preflight refuses a dirty worktree, offers a dedicated Run worktree before creating anything, resolves
  the effective policy, checks `roadmap.py check`, and asks models for Plan, Implement, Review and Critic.
  Preflight also resolves `unitId` (`runlog.py unit-id --cwd <repoRoot> --json`) and a fresh `runId`, then
  queries `runlog.py inflight <unitId> --json`. Every match names an Issue still `ready-for-agent`, its
  phase and its preserved worktree; preflight offers the operator continuation there before doing anything
  else. `runlog.py inflight` reports only `run`, `issue`, `phase`, `worktree`, `repositoryRoot`,
  `policyHash`, `tier` and `staleAfterSeconds` — it does not report `correctionsSpent` or `branch`, so
  preflight derives them before building `args.priorRun` by invoking the shipped query
  `runlog.py corrections <unitId> <match.run> <match.issue> --json`, which reads the match's own Run log
  (`~/.gantry/state/<unitId>/runs/<match.run>.jsonl`, or `--state-root` when overridden) and returns
  `correctionsSpent` as the sum of two counts: (1) the `run.resumed.data.correctionsSpent` recorded in
  that same Run log, but only when that same `run.resumed` event's `data.issue` also equals `match.issue`
  — `0` when the log has no `run.resumed` event, or when its `run.resumed` names a different Issue, since
  the base is per-Issue and must never be lent to another Issue that happens to share the Run log; plus
  (2) the number of `refutation` events in that log whose `issue` equals `match.issue` and that are each
  followed, later in the log, by a `phase.started` event for `Implement` on that same Issue — i.e. only
  refutations whose correction pass actually started count toward the spent budget. Neither this
  derivation rule nor `correctionsSpent` itself is ever computed by prose or by test code: this shipped
  command is the single implementation, and it fails closed (`runlog error: no Run log for <runId>`,
  exit 1) when no Run log exists for the requested Run ID, rather than silently reporting `0`.
  `branch` is optional: when omitted, `reference/round-workflow.md` derives it itself from
  `common.issue_branch` and verifies it with `git branch --show-current` in the preserved worktree
  (see `implementationLocation`). Only explicit acceptance carries the derived match forward as
  `args.priorRun` (`run`, `worktree`, `issue`, `correctionsSpent`, `policyHash`, and `branch` when known)
  into `reference/round-workflow.md`, which appends `run.resumed` naming the prior Run and worktree
  instead of starting a fresh worktree, and resumes the spent correction count instead of resetting it.
  When the prior Run's `policyHash` differs from the effective policy resolved for this Run,
  `reference/round-workflow.md` appends `policy.changed` with the new hash so the drift is recorded
  before any Issue work resumes. The Run log is read only to offer that continuation and to derive
  `correctionsSpent`; it never decides readiness or completion — `frontier.py`, Issue `Status:` lines
  and `roadmap.py` do.
- `reference/round-workflow.md` appends every recorded-Run lifecycle event through `runlog.py append
  <unitId> <runId>` when the caller supplies both. A Run spans one or more rounds, each a separate
  invocation of this workflow sharing the same `runId`/`unitId`: only the first round (`args.isFirstRound`
  not explicitly `false`) appends `run.started` (with the repository root, a policy hash, the harness
  tier and the effective `staleAfterSeconds` in `data`) and, when resuming, `run.resumed` and
  `policy.changed`; every subsequent round of the same Run passes `args.isFirstRound = false` so these
  three events are never appended again — a Run log accepts only one `run.started` and rejects a
  duplicate. Every round, first or not, then appends `round.started`, one `phase.started` /
  `phase.finished` pair per phase that actually runs (Implement, Review and Critic per Issue, plus the
  optional Learner phase on the last round when it finds recurring evidence), one
  `subagent.started` / `subagent.stopped` pair per fresh agent carrying its role result,
  `review.finding` after the Reviewer returns, `refutation` on every non-accepted Critic verdict,
  `issue.blocked` when the correction ceiling is spent without acceptance, `issue.done` on successful
  integration, `run.cancelled` on the first red post-merge gate, and `round.finished`. Only the last round
  of a Run (`args.isLastRound = true`) appends `run.finished`, once, and only after the optional Learner
  phase (see below) has already run and recorded its own `phase.started`/`subagent.started`/
  `subagent.stopped`/`phase.finished` events — `run.finished` remains the final event of a completed Run,
  never followed by a subagent.
  The Critic's `subagent.stopped` carries a projection of its verdict, never the verdict unchanged: its
  `gateResult` is a real `gates.py --json` payload, and `runlog.py append` fails loudly on any
  `command`/`output`-tokenized field at any depth (its own rule), which a real `gates[].command` and
  `gates[].output_tail` are. `reference/round-workflow.md`'s `projectCriticResult` keeps `complete`,
  `criteria`, `gatesVerdict`, `gateFailures`, `refutations`, `requiredFixes` and `decisionsForOperator`
  as returned, and narrows `gateResult` to only its `verdict` and `requirements` — dropping `gates`
  entirely — so a genuine gates run never fails the append and the Run log still records only the
  Critic's role result and reasoning, never command output. Every other role's `subagent.stopped` still
  carries its result unprojected, and `runlog.py` still rejects it if it ever carries prohibited data.
  `issue.blocked` records only a Run-log fact: the Issue's `Status:` line stays `ready-for-agent` so
  `frontier.py` keeps offering it, and only `roadmap.py done` after Critic acceptance ever changes an
  Issue's authoritative status. Omitting `runId` or `unitId` disables recording entirely and leaves the
  round behaviorally identical (a headless/test fallback only; conversational agents must not omit them).
- Before any agent works in a worktree, the round workflow marks it with the Run — `runlog.py mark
  <runId> --cwd <worktree>`, stored in that worktree's own git directory — and clears it with
  `runlog.py unmark` when the Run ends, never between rounds. The tracked git hooks
  (`hooks/git/pre-commit`, `hooks/git/pre-push`) and `guard.py` resolve the Run in one order:
  `GANTRY_RUN_ID` when the caller exports it, then the marker, and a harness session ID only when
  nothing else names a Run and its Run log already exists — a Claude Code or OpenCode session ID is
  a session, not a Run, and no Run log is ever keyed by it. That is what makes a denial inside a Run
  always recorded as `hook.denied`; git keeps one git directory per worktree, so concurrent
  worktrees of one execution unit never attribute a denial to each other's Run. Because each round
  is a separate invocation, the Run's end enumerates `git worktree list --porcelain` and clears
  every marker naming that Run, so a worktree marked by an earlier round is never left behind.
- Use `frontier.py --scope <scope> --json` as the only authority for dependency rounds. Exit 1 for a
  cyclic or dangling blocker graph. Parked `draft`, `blocked`, and `needs-operator` Issues are reported
  and skipped.
- Before slicing, `spec.py --check` validates the Spec's structure and then the read-only Requirement
  Critic (Critic model) assesses ambiguity, coherence, verifiability and non-goal coverage. A blocking
  finding stops the run, quotes the finding, and tells the operator to amend the Spec; the Critic never
  edits it. Neither structural validation nor Requirement Review approves planning — only explicit
  operator approval does.
- Planning creates draft Issues and never edits `ROADMAP.md`. Present drafts and the critic verdict, then
  stop. Only explicit operator approval permits `roadmap.py status <ref> ready-for-agent`, followed by
  `roadmap.py waves` and `roadmap.py check`.
- **Execution phrasing and delegation to `gantry-plan`**: `Implement the <slug> Spec` is an execution-scope
  alias for an approved `<slug>` Spec; resolve it to that slug before scope validation. When `gantry` is invoked
  with any other free-text goal (e.g. a quoted string
  like `"add webhook support"`) or an unplanned spec (a spec without implementation issues in
  `.scratch/<slug>/issues/` or whose status is `draft`), it automatically delegates to `gantry-plan`.
  `gantry-plan` executes the Socratic Gate interview or spec validation, tracer-bullet vertical slicing,
  token budget audit, Plan Critic validation, and operator approval transition. Once approved, delegated
  execution automatically advances into the round implementation loop without prompting to start `gantry`.
- Each Issue follows `reference/round-workflow.md`: a fresh TDD implementer, a reviewer on both standards
  and Spec axes, one review fix pass, then a fresh adversarial Critic. The Critic alone can establish a
  complete delivery. Its refutation consumes at most the correction budget.
- A multi-Issue round uses one isolated worktree and branch per implementer. Integrate accepted branches
  serially, run gates after every merge, and stop on a failed integration gate. When an Issue execution fails,
  pause that Issue, preserve its worktree and branch, allow independent accepted Issues to integrate, and block
  the next round until explicit validated recovery. Create and identify each
  Issue branch through the `git.issueBranch` policy template (default
  `{prefix}{spec}-{number:02d}`), rendered by `common.issue_branch(policy, issue)`.
- Frontend changes require real browser validation. Declare an operator-approved absolute check named
  `browser-validation` in the repository policy; its command must run the browser checks or verify
  recorded browser evidence against the delivered revision, including relevant interactions, layout and
  accessibility. A successful executed check clears `gates.py`'s frontend requirement. Failed,
  skipped, unexecuted, differential or unrelated checks never clear it. The Critic independently
  inspects the command and evidence; naming a no-op check is not validation. Respect any stricter
  repository requirement, including a mandated browser tool. No prose claim or skip flag substitutes
  for the check.
- Only after Critic acceptance, green gates and a clean worktree may the orchestrator run
  `roadmap.py done <ref>`. Never hand-edit Issue status, criteria checkboxes or the roadmap.
- Round dashboard hooks automate lifecycle visibility: before the `Implement` phase begins in any round,
  the workflow queries `python3 <skillDir>/scripts/dashboard.py status --json`. If inactive, it asks the operator
  whether to start the dashboard (`dashboard.py start --daemon`) and displays the URL on approval, proceeding
  without prompts if declined; if already active, it logs the URL without prompting. Immediately after `Integrate`
  completes at round end, it queries `dashboard.py status --json`: if active, it prompts the operator asking
  whether to terminate the server daemon (`dashboard.py stop`).
- At the end of a Run, execute `python3 <skillDir>/scripts/cleanup.py --plan --json` from the Run worktree
  and present its JSON output as the actual, read-only cleanup plan for the operator's authorization.
  Only after explicit Cleanup Authorization may the workflow pass that unchanged JSON to
  `cleanup.py --yes --plan-file <authorized-plan.json>`; it revalidates the plan against the repository
  state and refuses any divergence. The workflow never executes `cleanup.py --yes` automatically.
- After the last round, the optional Learner (`reference/round-workflow.md`) reads only the refutation
  and review-finding events already recorded in the Run log and drafts a lesson candidate for each
  problem that recurred across Issues or attempts. The final Run report lists every lesson candidate,
  with its evidence and proposed target, as an operator decision: the workflow never writes a candidate
  into `AGENTS.md`, `CONTEXT.md`, a template or policy on its own. Pass `args.isLastRound = true` and
  `args.learnerRunLogs` only for that final frontier round; `learnerRunLogs` is the current Run's own
  Run-log path(s), normally `~/.gantry/state/<unit-id>/runs/<run-id>.jsonl`. When the Learner actually
  runs (recurring evidence found), it is recorded exactly like the Implement, Review and Critic phases —
  `phase.started`, `subagent.started`, `subagent.stopped` and `phase.finished` — appended after
  `round.finished` and before `run.finished`, so `run.finished` stays the last event of a completed Run.
  A skipped Learner phase (no logs, or nothing recurring) records none of those four events.
- After the last round (including the Learner phase), the final `roadmap.py check` and frontier reporting, offer to open a draft pull request from the Run branch to the configured target branch (`policy.git.target`). Generate an English PR body containing each completed Issue's authoritative criteria and Critic evidence. Ask the operator before calling `gh`. Open one draft pull request only on explicit confirmation. If `gh` is unavailable or the operator declines, report the Run branch and configured target as the handoff instead. Never merge, never auto-create a pull request, never create per-Issue pull requests, and never observe provider state. The final English Run report must state the capability-file support tier (`tier`).

## Harness-neutral execution

Use the host harness to ask the operator and spawn agents. Where native workflow scripts, structured
outputs, parallel agents or worktree isolation are available, use them. Otherwise execute the same
prompts from the reference files manually and validate their JSON-shaped results before advancing.
The deterministic scripts and workflow semantics stay identical in every harness. The host's command
runner contract is `runCommand(command, { cwd, input })`: `input`, when supplied, must be written to the
command's stdin, not appended to the command line. Every recorded Run event goes through
`runlog.py append <unitId> <runId>` this way, with the event JSON as `input` — a harness that implements
`runCommand` without stdin support breaks every recorded round, not just this one.

When coordinating directly in conversational or manual harnesses (Antigravity, Cursor, interactive CLI),
the coordinating agent MUST explicitly record Run lifecycle events via the CLI:
1. **Preflight**: resolve `unitId` (`python3 <skillDir>/scripts/runlog.py unit-id --cwd <repoRoot>`) and generate `runId="run-$(date +%s)"`.
2. **Start Run**: append `run.started` with repository root, policy hash, tier, and staleAfterSeconds.
3. **Mark worktree**: mark the active worktree with `python3 <skillDir>/scripts/runlog.py mark <runId> --cwd <worktree>`.
4. **Rounds and phases**: append `round.started`, and before/after each phase append `phase.started` and `phase.finished` with `{ issue, phase }`.
5. **Completion**: on issue completion after Critic acceptance, append `issue.done`. On Run completion, unmark with `python3 <skillDir>/scripts/runlog.py unmark --cwd <worktree>` and append `run.finished`.
Never omit `runId` or `unitId` during interactive execution; doing so disables telemetry and leaves the dashboard blind to active runs.

## References

- `reference/plan-workflow.md` — structural validation, Requirement Critic, research, draft, plan
  critic and mandatory operator stop.
- `reference/round-workflow.md` — TDD implementation, two-axis review, adversarial Critic and serial
  integration contract.
- `docs/role-execution.md` — cross-harness execution, model discovery, role overrides, and failure recovery.
- `templates/` — default Spec, PRD and Issue structures.
