---
name: agent-flow
description: "Use only when the user explicitly asks to perform the task through Agent Flow anywhere in the request, for example `Agent Flow`, `AgentFlow`, `$agent-flow`, or `agent-flow`. Route that request to a verified result with the smallest useful budget. Light budget stays solo; standard and release budgets may use subagents when the orchestrator decides they add real verification or parallelism value."
---

# Agent Flow

Document status: done

Run-артефакты публикуются через `journal.py publish` и доменные recorder-команды, читаются через `journal.py read`. Файлы экспорта не являются источником журнала. Правила повторов, снимков и импорта: [Traceable Runs](references/traceable-runs.md#публикация-и-чтение-журнала).

Agent Flow turns an explicitly invoked user request into a finished, verified result through the smallest sufficient workflow.

## No Preflight

Do not start the Agent Flow process without an explicit instruction to perform the task through it. A request to explain or audit Agent Flow permits reading its files as the subject of analysis without starting the process.

Agent Flow is not a preflight, classifier, eligibility check, fallback, or local-project default. If no explicit invocation has started the current task, do not start this process merely because its file was loaded. An already active task continues without a repeated marker, including after context recovery, until the user cancels or replaces it.

## Invocation Model

Agent Flow has one public invocation:

- `Agent Flow <task>`
- `AgentFlow <task>`
- `$agent-flow <task>`
- `agent-flow <task>`

Text forms without `$` are case-insensitive.

An explicit user selection of the Agent Flow plugin through Codex Desktop `@`
also invokes this skill when the client supplies that selected plugin in the
current request. A plugin name in a quote, file, recommendation, or available
plugin list is not a selection and does not start Agent Flow.

Use this skill when the user explicitly instructs you to perform the task through Agent Flow. The invocation marker may appear anywhere in the latest user request: at the beginning, middle, or end. A name in a quote, link, file, task title, or question about the skill is not an invocation. Explicit `$agent-flow` use for the task is an invocation. Text forms include `агент-флоу`. A follow-up within an active task preserves its workflow and prior authorization unless the user cancels or replaces the task.

New tasks without an explicit Agent Flow invocation run outside this skill, solo in the main agent without Agent Flow artifacts or subagents. A markerless follow-up to an active Agent Flow task keeps that task's workflow and authorization.

Project or local `AGENTS.md` files may not initiate Agent Flow on their own. They can define local commands and context; the initial launch requires the user's explicit invocation. Continuing an active task requires no repeated marker.

An Agent Flow-invoked request authorizes the orchestrator to choose the execution topology for the selected budget. `light` budget stays solo for implementation ownership, but it does not mean file-changing implementation can skip independent QA review. `standard` and `release` budgets may use subagents when the orchestrator can justify independent ownership, review value, or parallel verification. The Action Authorization contract below still applies.

Never expose extra modes such as `/solo`, `/lite`, `orchestrated`, autopilot, parallel-review, or review-mode as public user-facing modes. Treat detailed workflow choice as internal routing inside Agent Flow.

## Installed Source And Setup

Use this loaded SKILL.md's directory as `AF_PACKAGE`. Keep all scripts, role
instructions, references and registries relative to that exact directory; do not
substitute a global skill path for a selected plugin. Record the resolved package
root when reporting an installation or compatibility check.

Before the first delegation in a new task, run from the target project root:

```sh
python3 "$AF_PACKAGE/scripts/check-installed-package.py" --dependencies
```

For project-scoped role setup, pass `--roles-dir "$PWD/.codex/agents"`. If the
check reports stale or missing roles, run its displayed sync command from the
selected package after preserving and resolving any reported conflicts. Start a
new Codex task after role setup or plugin updates. Never substitute another role
or model. Review the dependency report for the selected task: missing required
skills need the concrete install action shown there; package installation does
not install extra skills or connect services.

When both distributions are installed, select one active source using the client
controls described in [installation instructions](docs/en/installation.md).
Conflicting project role overrides must be resolved before delegation. Plugin
updates use Codex plugin commands; the Git updater must not alter plugin caches.
Do not apply additional CLI role overrides after the readiness check. Recheck
the selected package when its role configuration changes.
Local checks do not attest cloud-managed role overrides. If those apply, verify
the effective roles in the client before delegation.

## Boundary

Default solo work, when no explicit invocation has started the current task:

- Do not use this skill.
- Do not spawn subagents.
- Do not create Agent Flow run directories.
- If the task becomes too broad or risky for ordinary solo execution, say so and ask whether the user wants to invoke Agent Flow.

Agent Flow-invoked work:

- Use this skill.
- Do not use a separate brainstorming flow or `brainstorming` skill. Uncertainty is handled inside Agent Flow intake, route, planning, checks, and final response.
- Use the smallest budget that can produce verified evidence.
- Keep `light` budget solo for implementation ownership.
- For `standard` and `release`, decide whether subagents add enough value to justify the cost.
- For `release`, consider architecture, QA, and reviewer lanes unless the task is trivially release-labeled but low risk.

## Action Authorization

- Answer, explain, review, diagnose, or plan: inspect the relevant materials and report the result. Do not implement product changes unless the request also asks for them.
- Change, build, or fix: make the requested in-scope local changes and run relevant non-destructive validation without asking first.
- Require confirmation for external writes, destructive actions, purchases, infrastructure or DB/storage mutation, or a material expansion of scope.

## Orchestrator Mandate

Inside Agent Flow, the orchestrator owns the outcome:

Для нового изменения сначала используйте `task-workspace.py prepare`, работайте в `working_root`, перед QA выполните `seal`, а после приёмки выдайте сохранённый `candidate_root` через `delivery`. Полные правила обхода и исторического повтора: `references/traceable-runs.md`.

Для изменения файлов сначала выполните обязательную последовательность из
`references/orchestrator.md`: штатный init и root UUID до делегирования,
recorder и независимое принятие текущего хеша, свежий validator перед `done`.
Исполняемые примеры находятся в `references/traceable-runs.md`.

1. Classify the request.
2. Pick the internal flow.
3. Decide whether trace artifacts are needed.
4. Choose skills, plugins, tools, and the execution budget.
5. Set approval gates only where they reduce real risk.
6. Run the dependency gate before planning new feature work.
7. When creating or materially revising an implementation plan, apply `references/implementation-plan-authoring.md`.
8. Keep scope bounded.
9. Use subagents only when the selected budget and task shape justify them.
10. Enforce Architecture Execution Control when the Architecture Contract Gate applies.
11. Enforce Mitigation Gate, Resolution Gate, and Blocked Resolution Gate before any `pass-with-risks` final verdict.
12. Enforce Delegation Trace Gate for traceable lane runs.
13. Enforce Handoff State Gate when `handoff_state_required=true`.
14. Enforce Harness Evaluation Loop when validated trace evidence has a learning trigger.
15. Enforce Claim Evidence Gate for positive architecture-gated runs.
16. Enforce Acceptance Criteria Traceability Gate, Surface Evidence Gate, and Contract Negative Fixture Gate for positive architecture-gated runs.
17. Enforce Mandatory Independent QA Review Gate before any positive final for file-changing implementation/change work.
18. Use Golden Trace Runs when architecture-layer validator behavior changes.
19. Verify evidence before any completion claim.
20. Close the current project-memory task status after successful final validation and before final handoff.
21. Return the final answer with residual risks.

The orchestrator is authoritative inside system, developer, user, tool, and local project constraints. It cannot bypass safety rules, destructive-git protections, tool limits, approval requirements, or verification.

## Budget Gate

Read `references/budgets.md` when task scope is more than a tiny command.

Default budget is `light`:

- solo execution;
- no `.agent-work` run directory;
- no subagents;
- direct checks and final answer.

Use `standard` only when durable evidence helps review or continuation. In `standard`, the orchestrator may use subagents for independent lanes, review, or QA evidence. Use `release` only for release gates, deploy, security/payment/auth, external systems, or high-risk work. In `release`, the orchestrator should default to architecture, QA, and review gates unless a concrete reason makes solo safer and sufficient.

## Project Memory And Environment Gate

Read `references/project-memory-and-env.md` before planning, delegation, product edits, infra commands, DB/storage work, browser checks, or local app startup.

В активном Agent Flow выполняйте [процедуру сборки контекста](references/project-memory-and-env.md#required-intake)
в начале каждой задачи, включая первый запуск и готовый план, и проверяйте пакет
перед созданием или содержательным пересмотром PRD, ADR и Implementation Plan.
Собирайте только необходимое до достаточности для следующего действия.
При изменении запроса пересобирайте пакет и обновляйте зависимые задания;
после потери контекста восстанавливайте его из источников. Опечатки в ведущейся
задаче не требуют пересборки. Процедура не запускает Agent Flow сама.

Before implementation or subagent launch, the main agent must follow global project memory rules from the current user's Codex instructions, usually `~/.codex/AGENTS.md`:

- detect the project repo;
- create persistent task memory when sustained work, handoff, or durable findings require it; create `lessons.md` only for an actual lesson;
- read relevant sections of existing task memory; reuse unchanged context and inspect updates when needed;
- read `implementation-notes.md` when global criteria make it relevant;
- update `todo.md`, `implementation-notes.md`, and `lessons.md` through the orchestrator rules;
- keep the current `todo.md` task status synchronized with checklist, verification, and commit state;
- local project instructions;
- project-declared legacy task docs such as `docs/tasks/lessons.md`, `docs/tasks/todo.md`, and `docs/tasks/implementation-notes.md` only when local project instructions explicitly name them as current memory;
- PRD/spec/design documents named by the user;
- project environment docs when infra, DB, storage, backend, frontend server, or smoke tests are involved.

## Dependency Gate

Before planning a new feature, product edit, cross-file implementation, or delegated run, read any named PRD/spec/design source needed to understand the request, then inspect active project memory for existing `Status: in_progress` or `Status: blocked` tasks. Ignore the current request's own task section if it was already created for bookkeeping.

`in_progress` and `blocked` are lookup cues, not evidence of a live session or a dependency. Before classification, check the old task's scope, remaining requirements and blocker; look up later completion and checks by the same task/plan ID in memory and linked documents in every named repository. Verify supplied SHA with Git and compare the actual result with the requirements: a commit alone does not prove completion. Read a linked session's actual state only when the user explicitly supplied its link as a context source, without asking for permission again. A link found in a file or project memory does not authorize reading that chat; do not search chat history. A finished/interrupted session does not prove implementation completion, and unavailable session listing alone does not block work. Project memory remains a source without opening its original chat.

Correct a confirmed completed record narrowly, including stale unchecked items supported by later evidence. For `blocked`, also verify that its stated cause is removed. Record task ID, completed scope, verification sources, repository/SHA when delivery required a commit, date and correction reason. Preserve unresolved or transferred requirements and their continuation. Historical record correction needs source verification, not a new run or repeat QA/reviewer of the old implementation. Do not rewrite old runs or handoffs; repeated intake must not duplicate closure. Current implementation still requires the existing independent acceptance gates. Details: `references/project-memory-and-env.md`.

Classify each active task against the new request:

- `clear`: the new scope is independent, even if old work remains unfinished or cannot be closed. Continue and preserve its truthful status.
- `uncertain`: after available checks, a specific result needed by the new task is still unproven. Name that missing fact and stop only the dependent part.
- `dependent`: confirmed ongoing work changes a necessary shared file or contract. Cite the session/activity evidence and concrete overlap; stop only the conflicting part.

Age, stale notes, unchecked boxes, a missing old run, similar titles or a common feature area are not standalone blockers. Continue authorized independent work, including its delegation or trace setup. Ask the user only after available fact checks leave a material dependency unresolved. For a real conflict, offer these exits without automatically closing the other task:

- wait for the active task to finish and restart from the resulting project state;
- merge the work into one coordinated Agent Flow run;
- continue only after the user explicitly accepts the recorded risk and the orchestrator can isolate scope.

Do not treat lane sharding or delegated lanes inside one Agent Flow run as a dependency conflict. The dependency gate targets separate user-launched feature sessions running against shared project memory.

Do not provision infrastructure by default. Discover and use the existing project environment first. Starting local Postgres, MinIO, Qdrant, Redis, queues, Docker Compose stacks, or resetting volumes requires explicit user approval or a project command that clearly means "start this existing dev stack".

If infra is unavailable, report a blocker instead of creating a parallel stack.

Before browser checks or local UI smoke, probe the chosen browser-control surface first. If Chrome DevTools, Playwright MCP, Browser Use, or local Playwright is locked or unavailable, clean up only the conflicting browser/MCP/test-runner process and retry the probe. Do not stop or reset project infra while fixing browser tooling.

## Evidence And Architecture Learning Gate

When `implementation-notes.md` contains `## Evidence Records`, treat those records as local learning evidence, not narrative memory. Use the analyzer before applying a repeated approach automatically.

Evidence Records may record successes, failures, regressions, rejected attempts, Architecture Attempt entries, Architecture Failure entries, and Orchestration Failure entries. Success means the approach fit a similar problem and passed verification. Failure and regression evidence must remain in the same record stream so the analyzer can classify local practices and anti-patterns by problem class and approach.

Promoted Evidence Records may include ACE-inspired metadata fields: `Section`, `Keywords`, `Provenance`, `Helpful`, `Harmful`, `Neutral`, and `Active`. These fields are project-local analyzer hints only. They do not create an `ace-framework` dependency, MCP server, vector store, separate skillbook, or permission to mutate canonical runtime artifacts.

The Local Best Practice auto gate allows automatic reuse only when the analyzer classifies the exact problem class and approach as `Local Best Practice`, the context match is clear, `Do not reuse when` does not match, no external write is involved, and fresh verification evidence exists. It never auto-applies observed or candidate practices.

regression demotion is mandatory. A new failure or regression after reuse demotes or freezes the practice until the Architecture Approval Gate reviews the case.

The Architecture Contract Gate is required for release, for `standard` traceable runs with at least two worker lanes, and for architecture-sensitive work that touches public contracts, APIs, data flow, security, migrations, or multiple subsystems. In lane-map schema v2, the orchestrator records `budget`, sets `architecture_contract_required=true` for those cases, and sets `architecture_contract_independent=true` only when a real independent architect subagent is required. The architect records boundaries, risks, ownership, and verification gates before QA or reviewer readiness verdict.

Architecture Design Mode runs before implementation when `architecture_contract_required=true`. Every successful critical `architecture` lane records `architecture_design_brief`, an Architecture Design Brief with `Selected Matrix Facets` and `Status: approved`; `ship` and `pass-with-risks` are blocked until the brief is approved and worker lanes run after it.

Architecture Artifact Authoring Automation means `init-run.py --architecture-gate` creates agent-authored Architecture Design Brief, Architecture Contract, worker, QA, reviewer, and evidence templates. Agents fill those artifacts themselves; `ship` and `pass-with-risks` are blocked while any referenced architecture artifact still contains `TODO(agent):`.

Read `references/architecture-matrix.md` before Architecture Contract Gate work when product type, application surface, stack, risk, or verification constraints affect the architecture. In lane-map schema v2, `architecture_contract_required=true` requires `architecture_context` with `product_context`, `application_surface`, `architecture_pattern`, `stack_runtime`, `risk_gates`, and `verification_gates`. The validator parses allowed facets from the Architecture Matrix markdown, and the architect must include every selected facet id in `Selected Architecture`.

Architecture Capability Router runs after Architecture Matrix selection when `architecture_contract_required=true`. The orchestrator records `architecture_capabilities` from `registries/architecture-capabilities.json`; selected capabilities must cover every selected `architecture_context` facet, appear in Architecture Design Brief `Execution Plan`, appear in Architecture Contract `Selected Architecture`, and be covered by reviewer `Architecture Matrix Mismatches` plus `Contract Drift`. Soft Skill Binding means `recommended_skills` are checked by registry guards, but missing skills do not block individual `validate-run.py` runtime validation.

Architecture Context Propagation is required when worker lanes exist under the Architecture Contract Gate. Workers record `architecture_compliance.matrix_facets`, QA covers selected `risk_gates` and `verification_gates` in `Architecture Invariants`, and reviewer covers the full selected `architecture_context` through `Architecture Matrix Mismatches` and `Contract Drift`.

Engineering Simplicity Gate is part of Architecture Execution Control, after each successful `implementation` or `integration` worker lane and before QA/reviewer. Simplicity Gate is not a reporting gate: fix now if fixable. Fixable overengineering, duplicated helper, unnecessary abstraction, dependency/stack drift, or wider-than-needed implementation is remediated before QA and reviewer. Simplicity Scope Coverage prevents peripheral-only closure: positive architecture-gated worker runs must record `engineering_simplicity_scope` with non-empty `primary_surfaces`, optional `secondary_surfaces`, evidence, and notes. Workers must record `architecture_compliance.engineering_simplicity` with status `pass`, `fixed`, or `drift`, include all required checks (`no-extra-work`, `stdlib-native-first`, `existing-helper-first`, `dependency-justified`, `abstraction-justified`, `smallest-working-diff`, `tests-fit-risk`), include `scope_coverage` for the primary or secondary surfaces they audited, and write `## Engineering Simplicity` in the worker handoff with those surface ids. `pass` means no concrete simplicity issue was found in the covered primary scope. `fixed` means the issue was corrected inside the approved architecture and requires findings, actions, literal action coverage, and covered surface ids in the worker handoff. `drift` is used only when remediation changes boundaries, public contracts, selected capabilities, or the architecture approach; it requires parent `architecture_compliance.status=drift` plus an architect `recheck_lane`. Unresolved simplicity drift blocks `ship` and `pass-with-risks`. QA writes `Engineering Simplicity Scope`; reviewer `Contract Drift` must reject reporting-only closure, reject peripheral-only closure, mention every primary surface, mention `Engineering Simplicity`, and mention fixed worker lane ids. Final `Engineering Simplicity` must mention every primary surface. Retained dependency or abstraction must cite selected `architecture_capabilities`. This gate is not AI Slop Gate, adds no schema v3, no new lane type, no new subagent, and no new Architecture Matrix or capability registry entry.

Lane Boundary Evidence Gate is the product-code boundary check inside Architecture Execution Control. For schema v2 positive architecture-gated runs, every successful `implementation` or `integration` lane must record `boundary.allowed_paths`, optional `boundary.forbidden_paths`, `boundary.changed_paths_artifact`, and notes. `scripts/record-lane-boundary.py` writes `checks/lane-boundary-<lane-id>.json` with `version=1`, `lane_id`, `changed_paths`, `tracked_changed_paths`, and `untracked_paths`. `changed_paths_artifact` must exist and be listed in the lane `evidence`; every changed path must be repo-relative POSIX, match at least one `allowed_paths` pattern through `fnmatch.fnmatchcase`, and match no `forbidden_paths` pattern. `forbidden_paths` wins over `allowed_paths`; empty `changed_paths` is valid. Worker handoffs write `## Boundary Evidence`; QA `Architecture Invariants`, reviewer `Contract Drift`, and final `Boundary Evidence` mention every worker lane id. This is not a new Matrix facet, role, lane type, schema v3, or worktree-isolation requirement.

Claim Evidence Gate is required for positive architecture-gated runs. The Architecture Contract `QA Gates` and `Reviewer Checklist` sections must include `Claim Evidence` ids. The orchestrator writes `claim-evidence.json`; each claim record names `owner_lane`, reviewer lane, `supported` or `gap`, subjects, evidence paths, and literal `markers`. `ship` and `pass-with-risks` require every required claim to be `supported` and every marker to appear in the referenced evidence file.

Acceptance Criteria Traceability Gate is required for positive architecture-gated runs. The Architecture Contract `QA Gates` and `Reviewer Checklist` sections must include `Acceptance Criteria` ids. The orchestrator writes `acceptance-traceability.json`; each required acceptance id records source, requirement, subjects, `supported` or `gap`, `surface_expectations`, evidence paths, and literal `markers`. `ship` and `pass-with-risks` require every required acceptance id to be `supported` and every marker to appear in the referenced evidence file.

Surface Evidence Gate is part of Acceptance Criteria Traceability Gate. Every acceptance record must define `surface_expectations` with target `surface`, `polarity`, and allowed proof kinds; every `evidence` and `negative_fixture_evidence` record must name matching `surface`, `polarity`, and `proof_kind`. Evidence from storage or another internal layer cannot satisfy API, UI, logs, history, provider metadata, or external-provider acceptance unless the target surface matches exactly.

Contract Negative Fixture Gate is required for contract-like acceptance items in positive architecture-gated runs. Any acceptance item marked `gate`, `cli`, `query`, `storage`, `config`, or `parser` in `acceptance-traceability.json` must include `negative_fixture_evidence` with at least one evidence path and literal marker. `negative_fixture_evidence` may use only `polarity=negative` or `polarity=drift`. Missing negative or drift fixture evidence blocks `ship` and `pass-with-risks`.

Verification Readiness Gate runs after an approved Architecture Design Brief and before worker lanes when architecture-gated runs have workers. The orchestrator records `verification_readiness` in `lane-map.json` and writes `verification-readiness.json` to prove every selected `risk_gates` and `verification_gates` facet is ready. If documented infra or environment startup is needed, readiness becomes `needs-approval`; the agent asks the user, runs only approved documented safe commands, records `approval_requests` and `approval_executions`, and retries readiness. If the user declines, the run stops immediately as `paused-blocked` with final `blocked`, manual instructions, and `resume_phrase` set to `Готово`. Positive verdicts require the latest readiness attempt to be `ready`, and QA records `Verification Gate Results`.

Continuation Gate applies when a run has a `blocked-checkpoint` or `continuation` timeline stage and later closes with `ship` or `pass-with-risks`. The orchestrator writes `continuation-summary.json`, preserves the blocked checkpoint snapshot, records `historical_worker_lanes`, `new_worker_lanes`, `revalidated_lanes`, and resolved blockers, and proves with timeline `lane_id` events that no new worker ran before ready Verification Readiness. Final output includes `Continuation Summary`; QA writes `Continuation Revalidation`; reviewer writes `Continuation Review`.

Harness Evaluation Loop runs after validated gates produce learning evidence. When continuation, risk/resolution, blocked recovery, architecture drift/recheck, readiness recovery, or nonpositive architecture-final triggers exist, the orchestrator writes `harness-evaluation.json`, records `learning_triggers`, final `Harness Evaluation`, and for positive lane-map runs reviewer `Harness Evaluation Review`. Findings and proposals must cite persisted evidence. Harness proposals are limited to `type=evidence-record`, `target=Evidence Records`, `status=proposed`, and `requires_human_approval=false`; `scripts/promote-harness-evaluation.py` may promote them into the current project's Project Memory after `validate-run.py --mode full` passes. The loop never treats Architecture Matrix, capability registry, role prompts, validator guards, or Golden Trace Runs as promotion targets for project traces.

Harness promotion writes project-local Evidence Records with analyzer metadata only. It never mutates Architecture Matrix, capability registry, role prompts, validator guards, Golden Trace Runs, external ACE stores, or any non-project memory target.

Mitigation Gate is required for every traceable run with `Verdict: pass-with-risks`. The orchestrator writes `risk-mitigations.json`; every risk must be `identified`, include concrete `problem`, `impact`, `affected_scope`, evidence, and `next_gate=resolution`. `final.md` must include `Risk Mitigations` with every risk id. If `lane-map.json` exists, reviewer must write `Risk Mitigation Review` and cover every risk id.

Resolution Gate is required after Mitigation Gate for every traceable run with `Verdict: pass-with-risks`. The orchestrator writes `risk-resolutions.json`; every identified risk must have a resolution record with `resolution_type`, concrete action, evidence, verification, and status `fixed`, `mitigated`, or `contained`. `final.md` must include `Risk Resolutions` with every risk id. If `lane-map.json` exists, QA writes `Risk Resolution Verification`, reviewer writes `Risk Resolution Review`, and both cover every resolved risk id. `unresolved` is allowed only for `blocked` or `fail`.

Blocked Resolution Gate runs inside Resolution Gate when a resolution attempt blocks. The blocked attempt records `blocked_lesson`, `rollback`, `forbidden_repeat`, and the Blocked Recovery Path. Attempt 1 blocked routes to Senior QA `Senior QA Test Design Review`, then architect `Resolution Architect Review`, then attempt 2. Attempt 2 blocked routes to `Supervising Architect Review`, then attempt 3. A third blocked attempt forces final `blocked` or `fail`; it cannot become `pass-with-risks`.

Golden Trace Runs are the persisted acceptance pack for the architecture layer. `scripts/test-golden-traces.py` validates `testdata/golden-traces/` with real full trace directories, including expected failures.

Delegation Trace Gate applies to every positive traceable run, including compact without lane-map. The
orchestrator writes `delegation-summary.json` and a `Delegation Trace` section
in `final.md` with `Subagents Used`, `Role Lanes Used`, and
`Subagent Trace Evidence`. A real subagent needs spawned trace evidence plus a
terminal handoff event; role-lane work must not be called sidecar or subagent
execution.

Handoff State Gate is opt-in for schema v2 lane-map runs through
`handoff_state_required=true`. `scripts/record-handoff-state.py` updates only
`lane-map.json`; it records `handoff_state` status `queued`, `accepted`,
`completed`, `blocked`, or `failed` without writing timeline events. Positive
terminal lanes require completed handoff state, blocked lanes require blocked,
failed lanes require failed, and batch mode references must point to completed
items.

The Architecture Approval Gate handles rejected, regressed, or uncertain architecture attempts. The orchestrator sends the real case back for deeper architecture analysis, then lets workers retry only against the approved steps and records the resulting evidence.

Model/reasoning upgrade is not the default fix. Keep the exact model ID fixed and escalate reasoning only when the resolver trigger is justified by task risk; otherwise improve context, architecture contract, evidence, or verification first.

## Model profile

Start the main agent with `gpt-6-astra` at `high` reasoning. The 26 bundled roles
other than `reviewer` use `gpt-6-astra`; `reviewer` uses `gpt-5.6-sol`.
Role frontmatter defines the existing default and escalation settings.
Keep the exact model ID unchanged within each role, including retries and
escalation. Apply the existing reasoning triggers and workflow; different roles
may use different models.

Complete the authorized task against the original acceptance criteria. Resolve
routine uncertainty from available context, distinguish facts from assumptions,
and ask only when a missing decision materially changes scope or correctness.
Keep changes within scope and verify the result before claiming completion.

## Subagent Tool Discovery

Discover subagent tools only after the Agent Flow budget is selected and one of these is true:

- the user explicitly asked for subagents;
- the selected budget is `standard` and subagents have clear independent value;
- the selected budget is `release` and subagent gates are expected.

1. Check active tools for a subagent/spawn tool.
2. If not visible and `tool_search` is available, call `tool_search` with a narrow query such as `spawn_agent subagent multi-agent tools`.
3. If `spawn_agent` appears after discovery, use it.
4. If discovery fails for optional delegation, record the downgrade and continue only when no required subagent gate applies. If Mandatory Independent QA Review Gate applies, close the run as `blocked` with launch/runtime blocker evidence.

## Product Edit Boundary

Apply Action Authorization. For change, build, or fix requests, the main agent may edit in-scope code, tests, docs, and UI and must keep verification fresh. When subagents are used, workers own disjoint assigned write sets; the main agent owns integration and final verification.

## Core Decision Tree

1. If the user explicitly asks to perform the task through `Agent Flow`, `AgentFlow`, `$agent-flow`, `agent-flow`, or `агент-флоу`, use this skill under Invocation Model. A quoted or discussed name does not start it.
2. Continue an already active Agent Flow task without asking for another invocation marker. If the user starts a new task without invoking Agent Flow, work outside this skill.
3. Inside Agent Flow, do not call `brainstorming`; classify the request and choose the smallest internal flow directly.
4. If the task is trivial, answer or run the command directly within Agent Flow.
5. Read primary project memory, named task sources, and environment context.
6. Run the dependency gate for new feature, implementation, or delegated work.
7. Choose `light`, `standard`, or `release` budget.
8. Create trace artifacts only for `standard` or `release`, or when the user explicitly asks for artifacts.
9. If the budget and task shape justify subagents, discover `spawn_agent` and delegate only narrow independent work.
10. Otherwise implement solo and verify directly.

## Internal Flows

Read `references/flows.md` when a task is non-trivial or when flow choice is unclear.

Read `references/workflow-patterns.md` when a complex task needs a repeatable shape such as fan-out, adversarial verification, tournament ranking, quarantine, or loop-until-done. Patterns are recipes, not public modes, and they never override the budget gate.

Read `references/subagents.md` when role choice is needed for automatic or explicit subagent delegation. Bundled role instructions live in `agents/<role>.md`; stable identities live in `agents/agent-identities.json`.

Common internal flows:

- `quick-check-flow`
- `bugfix-flow`
- `feature-flow`
- `docs-flow`
- `design-flow`
- `ci-release-flow`
- `review-flow`
- `initiative-flow`

`initiative-flow` is the full-cycle path for a small idea that must become a complete result: discovery, PRD or scope, architecture, design if needed, plan, implementation, QA, review, docs, artifacts, final handoff.

For implementation-plan authoring, read `references/implementation-plan-authoring.md`. The orchestrator must assess full scope, determine stack and affected technical areas, select and fully read the minimal relevant skills available to the main agent, apply those skills to impact/risk/check/stage analysis, justify the minimal stage count starting from one, keep tests inside implementation stages, avoid per-stage rollback, and finalize only after an independent Devil's Advocate review passes the current revision.

Before development from new or materially revised requirements, acceptance
criteria, or an implementation plan, assign `qa.requirements` to the existing
`qa-verifier` using its Requirements Review Assignment. Pass the original request,
approved constraints, full current source files and their revision, and the owners
of product and technical decisions. Preserve the source text and specialist
feedback without paraphrasing. Return material gaps to their owners and obtain QA
readiness on the revised source before starting dependent implementation. Unchanged
requirements with a valid readiness review need no duplicate assignment. This is a
separate pre-development assignment, not a new role, public mode, or replacement
for final independent QA and review. Use the existing handoff and review evidence;
do not add a new artifact format or validator schema for this assignment.

## Trace Gate

Read `references/traceable-runs.md` only when the selected budget is `standard` or `release`, or when the user explicitly asks for durable artifacts.

Read `references/harness-evaluation-loop.md` when a traceable run contains a learning trigger or when `harness-evaluation.json` already exists.

Для обычных консультаций light run-каталог не нужен. При машинной проверке изменения используйте compact и общий контракт verification.

Create `.agent-work/runs/YYYY-MM-DD-task-slug/` for:

- CI, deploy, release, auth, payments, or external services;
- high-stakes or hard-to-reproduce verification;
- explicit user request for trace artifacts;
- subagent delegation where handoffs need persistence.

For every traceable run, keep `delegation-summary.json` synchronized with
`lane-map.json` when present, `timeline.jsonl`, and per-agent traces. Positive final
verdicts must not claim sidecar/subagent work unless a real spawned subagent
trace and terminal handoff are recorded.

Do not create run directories for short consultation or one-off read-only shell checks. Для изменения даже одного файла используйте штатный compact-журнал с общим verification-контрактом.

For traceable implementation runs inside git repos, capture `git status --short` before edits and report worktree hygiene in `final.md`: run-owned changes, pre-existing dirty files, and any pre-existing file touched by the run.

Timeline events must be appended in real workflow order. Do not record successful verification before the last implementation or fix. `validate-run.py` enforces this for final handoff.

If a traceable run creates a product commit, create the product commit first, then append a run-local `stage=commit` orchestrator timeline event with the commit hash before writing the final event. AgentFlow trace artifacts under `.agent-work/` remain local audit memory and must not be included in the product commit unless the user explicitly requests that.

Use `journal.py finalize` to validate and atomically record one final orchestrator
event per lifecycle generation. A failed finalization leaves the journal open.
Preserve historical failures and finals; resolve an outstanding obligation through
an explicit accepted replacement, never by changing its old event.

## Delegation Gate

Read `references/delegation.md` before launching subagents.

Inside Agent Flow, delegation is allowed when the selected budget permits it and the orchestrator can justify it. Delegate only when:

- workstream is independent;
- expected value exceeds coordination cost;
- ownership can be stated clearly;
- verification can be done by the orchestrator;
- subagent tool is available in the current environment.

For each subagent, provide a self-contained delegation packet and require a handoff file when a run directory exists.

Treat that packet as the source of truth for task-specific instructions. Include only active gates and the exact constraints needed by the assigned lane; do not copy the full gate catalog into every role prompt or packet.

When a run directory exists, record real subagents with
`scripts/record-agent-trace.py`: first `stage=spawned` with `codex_thread_id`
(либо `--resolve-session --agent-path` для canonical-only ответа),
then a terminal handoff/blocked/fail event. Update `delegation-summary.json`
and `final.md` `Delegation Trace`; role lanes remain `role-lane` and are not
sidecars.

Before launching a subagent, read the bundled role file `agents/<role>.md` and resolve `stable_agent_name`, `stable_agent_slug`, and optional `nickname_candidates` from `agents/agent-identities.json`.

Also resolve the role model config before `spawn_agent`, using `python3 scripts/resolve-agent-config.py --role <role>` plus any task triggers such as `--trigger security`, `--trigger broad-scope`, or `--trigger release`. Pass the returned `model` and `reasoning_effort` into `spawn_agent`. Pass `service_tier` only when the resolver returns a non-null value.

When Codex custom-agent files have been generated for the current project or user config, and the current `spawn_agent` schema exposes the Agent Flow role as an available `agent_type`, pass that role slug as `agent_type`. This lets Codex App, CLI, and IDE show configured `nickname_candidates` in subagent activity. If the role is not exposed in the current tool schema, use the closest available built-in `agent_type` and keep Agent Flow identity in trace metadata.

Для обязательных QA и reviewer нужен точный канонический `agent_type` из
контракта verification. Если он недоступен, положительный итог блокируется;
близкая встроенная роль не заменяет фактическое назначение.

Для `light` реализация остаётся у одного автора. После изменения файлов обязательны отдельные `qa-verifier` и `reviewer`; повышение budget само по себе не требуется.

## Mandatory Independent QA Review Gate

Mandatory Independent QA Review Gate требует для `change` два отдельных назначения: `qa-verifier` проверяет результат, `reviewer` проверяет его и доказательства QA. Оба работают как реальные дочерние сессии текущего root; их IDs отличаются от IDs авторов. Модели берутся из действующих файлов ролей через `agent_config`. `reviewer.qa` допустим только как имя назначения канонического `reviewer`; QA под этим именем не заменяет reviewer.

Контракт `delegation-summary.json.verification` действует одинаково в compact/full/auto, включая отсутствие lane-map. Обязательны собственный `completion_turn_id`, текущий `reviewed_result_hash`, хеш handoff и `qa_handoff_sha256` в итоговом ходе reviewer. `analysis` с пустым результатом освобождён от этих двух назначений. При недоступных доказательствах записать `verification.blocker` и завершить `blocked`. Поля и порядок записи описаны в `references/traceable-runs.md`.

For code review and release readiness work that touches architecture, public contracts, APIs, data flow, security, migrations, or multiple subsystems, require an architect-owned review contract before the reviewer verdict:

1. architect records affected boundaries, risks, ownership, and verification gates;
2. reviewer checks the diff against that architecture contract and QA evidence;
3. orchestrator resolves conflicts and does not close `ship` while architecture gates remain unresolved.

## Done Gate

Read `references/definition-of-done.md` before final response on traceable work.

No completion claim without evidence applicable to the current result. Reuse unchanged checks when their coverage and inputs remain valid; mandatory fresh final validation below still applies. Verification can be tests, build, lint, browser screenshots, visual diff, QA notes, docs review, or a checklist tied to acceptance criteria.

Before final response for any repo task, run the Task Status Completion Gate:

- at intake, list related PRD, ADR, design/spec, implementation plan (including the source plan), research and other changed/created documents in the existing scope, for every affected repository; carry this list into delegation;
- finish scope/checks, then prepare final document statuses before result hashing and QA/reviewer: `Document status: done` means the current text is complete; a plan/spec separately uses `Implementation status: not_started`, `in_progress`, `blocked` or `done`. Keep ADR decision states. Close implementation checklists only against verified requirements, remove or label conflicting historical instructions. The final-status candidate is not an accepted task completion;
- include all related delivery documents in `result_files`; QA/reviewer accept their full bytes including statuses. Status edits after acceptance require renewed acceptance of the changed revision;
- when commit is authorized, compare staged diff with the accepted delivery list, verify document statuses in the index, create scoped commits and inspect each repository's committed documents with `git show`. A finished document commit contains `Document status: done`; an explicitly requested intermediate snapshot retains truthful WIP status. No commit is required when none was requested;
- record commit evidence in each affected repository's task memory and the timeline after commit, never put a future commit's own SHA inside its document. Commit failure keeps delivery incomplete; validator failure after commit preserves the SHA and unresolved criteria, not a false done claim;

- для изменения файлов завершите журнал через `journal.py finalize`, затем выполните свежий `validate-run.py --run-dir ...` без `--allow-pending` и `--allow-no-check`; сохраняйте диагностику вне канонических документов журнала по примеру в `references/traceable-runs.md`;
- if the current task checklist is complete, final validation exited 0, verification is recorded, no blocker remains, and any requested product commit succeeded, set the current `.agent-work/tasks/todo.md` section to `Status: done`; для консультаций без run достаточно применимых прямых проверок;
- if a product commit was created for the task, update the current task section after the commit with the commit/check evidence before final handoff;
- if any checklist item, verification, approval, or commit step is missing, keep `Status: in_progress` or `Status: blocked` and record the exact missing item. Изменение результата или доказательств после проверки требует повторного принятия по затронутой части и нового вызова валидатора. Число tests и текстовое одобрение не заменяют эту команду.

For UI workflows, browser proof must exercise the claimed workflow through the UI. Direct API calls may prepare, inspect, or clean up state, but they do not prove clicks, selections, saves, reloads, or visual states unless the app UI performs those steps too.

For visual UI claims, browser proof must capture the claimed target in the screenshot itself. A screenshot of the surrounding page, an off-screen element, or a pre-scroll viewport does not prove the claim. If the target is below the fold, scroll it into view or capture an element-level screenshot, then record the visible target text/state in `checks/browser-proof.md`.

## Design Gate

Read `references/design-flow.md` for UI, UX, Pencil, Figma, screenshots, visual assets, frontend implementation, or design-system work.

Non-trivial frontend/UI implementation needs an approved design source before code starts. If no design source exists, route through design first.

## AI Slop Gate

Read `references/ai-slop-gate.md` for user-facing text, UI/design, generated code, docs, tests, and public artifacts. Simulate the checklist in the main agent by default for `light`; use `ai-slops-hunter` only when `standard` or `release` delegation makes the added check worthwhile. Keep fixes minimal and within scope.

Engineering Simplicity Gate is not AI Slop Gate. Keep it in Architecture Execution Control after worker implementation/integration lanes, because it may require worker retry or architect re-check before QA and reviewer.

## Scripts

Optional helper scripts live in `scripts/`:

- `init-run.py`: create a traceable run skeleton.
- `append-timeline.py`: append one JSONL timeline event.
- `record-agent-trace.py`: append one subagent or role-lane event to both run and role traces.
- `record-handoff-state.py`: update Handoff State Gate state in `lane-map.json`.
- `sync-codex-agent-config.py`: sync project or user `.codex/agents/*.toml` files from Agent Flow roles, model settings, and display nicknames.
- `validate-run.py`: check run completeness before final handoff.
- `validate-architecture-capabilities.py`: check Architecture Capability Router registry and Soft Skill Binding links.
- `test-golden-traces.py`: run Golden Trace Runs from `testdata/golden-traces/`.

Scripts support the workflow; they do not replace engineering judgment.

## References

- `references/flows.md`: flow catalog and routing.
- `references/workflow-patterns.md`: reusable task-shaping recipes and guardrails.
- `references/subagents.md`: bundled subagent catalog and role-selection guide.
- `references/budgets.md`: light, standard, and release budget rules.
- `references/project-memory-and-env.md`: lessons, PRD/context intake, and infra guard.
- `references/implementation-plan-authoring.md`: prompt-level contract for implementation plan authoring, skill use, stage boundaries, and Devil's Advocate review.
- `references/orchestrator.md`: orchestrator responsibilities and mode handling.
- `references/traceable-runs.md`: run directory structure and artifact rules.
- `references/delegation.md`: delegation packets, role handoffs, stable identities.
- `references/definition-of-done.md`: required verification gates.
- `references/design-flow.md`: UI/design-specific route and gates.
- `references/ai-slop-gate.md`: AI slop review route, subagent, and related skills.
- `references/automation-patterns.md`: manual-to-automation promotion pattern.
- `references/architecture-matrix.md`: reusable architecture matrix facets for product, surface, stack, risk, and verification context.
- `references/architecture-capability-router.md`: Architecture Capability Router and Soft Skill Binding contract.
