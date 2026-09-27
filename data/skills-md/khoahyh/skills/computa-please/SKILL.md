---
name: computa-please
description: Route engineering work from decision through the final human gate.
disable-model-invocation: true
---

# Computa Please

Deliver the requested outcome through the least process that can prove it. Subtract before adding, preserve real compatibility obligations, and spend verification in proportion to risk. Let deterministic mechanisms own known transitions, side-effect guards, retries, and compact evidence; use the model for decisions that require interpretation.

## Outcome And Authority

Establish the intended result, scope, success evidence, and authority from the request and accepted artifacts. Choose the route by the requested terminal outcome, not by the presence of a PR. Keep this framing in the conversation unless [Durable State](#durable-state) is needed.

Carry the agreed outcome through implementation and proportionate verification without asking permission for routine edits or safe checks. Autonomy operates within the agreed scope; a newly discovered dependency or a comprehensive spec does not automatically enlarge it. Use the [Work Frame](references/execution.md#work-frame) to distinguish this delivery from rollout prerequisites and follow-up work, including when preparing a spec or handoff prompt.

Resolve inspectable facts yourself. Ask only when a missing decision changes the outcome, consequential behavior, scope, or authority. For unresolved product, public-contract, domain, security, money, data-lifecycle, deployment, ownership, or architectural choices, use [Design Readiness](references/design-readiness.md). A clear, bounded request needs no ceremonial approval or separate spec.

Before any repository-content or Durable State write, or Recall/Pickup artifact recovery, follow [VCS Actions](references/vcs.md) to establish the one task-owned checkout (the **Task Worktree**). Re-anchor tools, artifacts, and delegates there. Commit, push, publication, merge, deploy, destructive data changes, and external messages require explicit authority; authorized local work does not imply it. The Finish Loop runbook owns delivery authority, including explicitly requested stack merges and CI waivers.

If an instruction forces a pause or conflicts with the intended outcome, identify the limiting instruction and distinguish it from your interpretation. Report the smallest decision or permission needed to continue.

## Route

Use only the selected route and references whose conditions apply. A matched reference owns its procedure and completion criterion; read it before the action it governs.

| Mode          | Requested outcome and route                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Discuss       | Compare, evaluate, or decide. Read-only and ephemeral by default; finish with a recommendation, tradeoff, or decision.                                                                                                                                                                                                                                                                                                                 |
| Spec          | A durable implementation plan. Use the [Work Frame and Subtraction](references/execution.md#work-frame), then `tech-spec` for contracts, call stacks, file ownership, and pending Proof. Production code stays read-only. A requested comprehension map selects or resumes Spec; use [Comprehension Map](references/comprehension-map.md) at its checkpoint.                                                                           |
| Implement     | Verified local changes or draft-only publication. Use the accepted request, spec, Feature Contract, and handoff where present, then follow [Execution](references/execution.md). A Feature Contract alone routes to Spec when implementation boundaries remain unresolved.                                                                                                                                                             |
| Finish Loop   | Drive accepted work, a PR, or an explicitly scoped stack through delivery: get it green, make it merge-ready, ship, land, merge, or verify post-merge workflows. Follow [Finish Loop](references/finish-loop.md) from its Entry Gate; its executable runtime owns transitions and external-action replay protection. Resolve merge authority from the user's request and prior context.                                                |
| Debug         | Diagnose a failure, regression, flake, or performance problem with `diagnosing-bugs`. Finish diagnosis with the symptom reproduced or bounded and root cause or remaining uncertainty explicit. For an authorized fix, follow [Execution](references/execution.md) and rerun the original repro. Load telemetry skills only when the observed path needs them.                                                                         |
| Review        | Find defects, independently of author confidence or prior conclusions. Follow the [Review Gate](#review-gate); report findings first with severity and file/line references. A one-pass PR status check is Discuss, not delivery.                                                                                                                                                                                                      |
| Recall/Pickup | Recover artifacts and live state in the Task Worktree, distinguish inherited claims from reverified facts, and route the remainder. Resume a Finish Loop only from a nonterminal reduced runtime state with a recorded Entry Gate choice. A closed run provides no authority.                                                                                                                                                          |
| Reflect       | Use observed corrections, retries, churn, successful recipes, and the [behavior evaluation harness](scripts/agent-runtime/README.md#behavior-evaluation) to improve the workflow. Capture a baseline, change one policy or mechanism, compare the candidate, and inspect every regression. Prefer deleting or replacing instructions; propose changes and their evaluation before editing unless implementation is already authorized. |

Default evaluative or genuinely ambiguous requests to Discuss; explicit change requests to Implement. A discussion becomes persistent or mutating only with the corresponding authority. An explicitly requested temporary `show-me` HTML visual may be created outside the project without authorizing production changes.

For a bounded operation such as restacking, syncing, submitting existing work, or updating a PR description, use only the applicable VCS, verification, and description procedures. Finish when the requested state transition is observed, intended changes are preserved, and relevant checks pass or a blocker is named. Existing PRs do not select Finish Loop. An authorized semantic repair expands scope only by that repair; readiness, CI monitoring, and landing remain separate outcomes unless already requested.

Compact at a real phase boundary when exploration, planning, implementation, review, or delivery has produced context that no longer changes the next step. Retain the goal, authority, decisions, compact evidence, unresolved risks, and next action; leave raw logs and superseded attempts behind pointers. After compaction or pickup, reload this router once, recover the active step and live constraints, and re-evaluate the route and applicable references. Reuse a reference read recorded in working context or a durable handoff; reload when its content or the applicable authority changes.

## Browser Tools

When browser automation or UI inspection is required, follow [Browser Tools](references/execution.md#browser-tools).

## Review Gate

- **Requested review:** follow the named review skill and its target, authority, and completion contract.
- **Normal review:** use the repository's review workflow, or inspect every changed hunk and confirm or reject each candidate defect through its owning call path and relevant evidence. Verification commands are not independent review.
- **Local Review:** Finish Loop and PR-bound Implement or Debug work follow [Local Review](references/local-review.md) after focused behavioral Proof and before the final basic-verification checkpoint and draft publication. It owns one provider-pass budget, the frozen target, Codex Autoreview, disposition, remediation, and Review Receipt.

Non-PR Implement and Debug work is exempt unless independent review is requested. Mechanical maintenance of existing work follows the exemption in Local Review; substantive repairs retain its gate. Review mode uses Requested or Normal review. A worktree review needs no commit unless its selected tool requires one and the user authorizes it. Use `review-remediation` for a frozen feedback set; keep CI repair in its own workflow.

Finding, CI, restack, and external-review remediation never trigger another local pass. Preserve a receipt across a mechanical target change only after proving the semantic patch and relevant base inputs unchanged. New product scope or other unreviewed behavior makes the receipt incomplete and returns control at the Human Gate; it does not replenish the review budget. Independent remote review remains a later delivery layer.

## Delegation

Delegate an independent investigation or isolated deliverable when it can shorten the critical path, resolve an uncertainty, or keep noisy exploration, documentation lookup, log analysis, or broad search out of the primary context. Split by context cost and ownership, not simulated job titles. Keep tightly coupled work with one implementation owner. Keep no more than two delegates running concurrently unless the user explicitly requests broader parallelism. The cap limits concurrency, not total delegation: queue additional work, start the next delegate when a slot opens, and continue useful primary work while both slots are occupied. Wait only when the active delegates are on the critical path and no independent work remains. The primary owns delegation decisions. Delegate authority stays inside the agreed scope; spare agent capacity is not a reason to open another workstream.

Give each delegate the task-owned path and revision, bounded outcome, necessary context, read-only or exclusive write ownership, and expected evidence. Prove the first vertical slice before distributing dependent implementation. Shared contracts, migrations, test databases, and Git/Graphite mutations need one owner; disjoint filenames alone do not establish independence. While a delegate owns a surface, work elsewhere and inspect its changes after handoff.

Request one concise result with changes or sourced facts, checks, and blockers. Resume for a concrete correction or new bounded deliverable, not status polling or repeated requests to restate a report. Batch necessary contract corrections; repeated coordination means the split is too coupled and should return to one owner. The primary owns integration, scope reconciliation, the final diff, and Durable State.

Research and implementation delegates return scoped changes, facts with sources, or observed check results. Independent defect finding and readiness judgment belong to the Review Gate. Resolve unsupported or conflicting claims before relying on them.

### Oracle Advisor

Research delegates return evidence and unresolved decisions to the primary. The primary resolves routine design through established project patterns and consults `oracle` for a read-only second opinion only when evidence leaves a consequential invariant or costly-to-reverse cross-system decision unresolved, after two evidence-producing attempts leave the next mechanism unclear, or when the user explicitly requests it.

Do not consult `oracle` for code location, documentation lookup, routine design, mechanical changes, a clear failure, or a first unsuccessful attempt. Give it the exact decision, task path and revision, settled constraints and authority, decisive evidence and unknowns, and the primary's proposed path with its strongest alternative. Missing product intent, risk acceptance, or action authority goes to the user through the primary.

The primary verifies pivotal claims and owns the decision, implementation, Proof, and user interaction. Oracle advice does not expand scope, grant authority, or replace review or verification.

## Durable State

Keep state conversational unless the user requests persistence, work must survive sessions, agents or people must coordinate, or a Finish Loop needs its event log. Then follow [VCS Actions: Durable State](references/vcs.md#durable-state). Finish Loop state is reduced from its runtime-owned event log; prose handoffs summarize it but do not replace it. Keep workflow state out of product diffs, commits, and PRs.

## Response Style

Use plain language over jargon, and reference technical details only to the degree that it helps illustrate an idea or your work to the user. Communicate complex concepts in a clear and cohesive manner, and calibrate your writing to the level of background knowledge assumed from the user's prompt and context.

## Visuals And PR Bodies

When an inline visual would materially clarify structure, sequence, state, interaction, or a before-and-after change, load `show-me` and use its smallest useful view. Follow it with exactly: `Say “create HTML” for a richer visual.` On explicit acceptance, create and open one renderer-owned temporary HTML file outside the project, not product code or Durable State.

Before drafting, returning, creating, or updating a PR body, use `visual-pr`. It owns the PR body template, visual outline, publication, and final response; do not maintain a competing local PR-description contract.

## Stop Cleanly

The **Human Gate** is the final handoff: the agreed outcome has its evidence and applicable review or delivery conditions, or a named blocker prevents completion. Scope checkpoints can occur earlier without reopening settled decisions or pausing independent authorized work. Once focused and required checks pass, finish; adjacent improvements belong to follow-up work.

Report the result, changed artifacts or no change, strongest relevant check and outcome, any omitted required check, residual risk or blocker, and any next human decision. For a Finish Loop, use its terminal report and delivery ceiling. Then stop; a new outcome needs new authority.
