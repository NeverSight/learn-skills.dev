---
name: conductor-dev
description: Use for Conductor project orchestration and development cycles. Initialize Conductor and continue through the cycle unless the user explicitly requests initialization only.
---

# Conductor Dev

Conductor owns orchestration. It delegates ArkUI implementation to
`hmos-arkui-develop-skill`, architecture to `hmos-arkui-mvvm-pattern`, grounded
ArkTS/API evidence to `hmos-arkts-knowledge-retriever`, and build/device work to
`ohos-app-dev`.

## Read Efficiently

Read this file once per session. Load only the phase-specific files listed in
`references/context-policy.md`. Read `references/execution-policy.md` when
selecting a profile or verification set. Do not reread all workflow files at
phase boundaries.
On a continuing project, read `conductor/bootstrap.md` before the full state or
history. Do not run `--help` for a known script unless its invocation fails. Use
the fixed script signatures documented in this skill during normal execution.

## User-visible Output

Keep Conductor orchestration details internal. Do not narrate or paste full
PowerShell chains for directory creation, state initialization, question gates,
workflow planning, skill recording, context caching, or phase synchronization.
Run these steps quietly and report one concise status line. Always surface user
decisions, actionable failures, blockers, and build/lint/install/launch results.
Do not suppress errors or verification evidence.
For the approved execution transition, use `scripts/confirm_execution.py` with a
brief JSON file instead of a long `state_update.py` command with many `--set` flags.

## Required State

Before implementation, record these fields in `SESSION_STATE.json` and the
Track plan:

```text
risk_level: low | medium | high
execution_profile: lean | strict
risk_signals: persistence | device | network | security | architecture
product_status: unconfirmed | confirmed | assumptions_accepted
product_brief: problem, primary_user, desired_outcome, core_flow, mvp,
  non_goals, target_device, data_behavior, visual_direction, acceptance_criteria
product_confirmation: explicit user decision and assumptions
work_plan_status: pending | approved | changes_requested
track_kind: ui | logic | infrastructure
ui_impact: none | visual | interaction | runtime
required_skills, context_fingerprint, loaded_context, api_evidence_cache
loaded_skills, api_evidence_sources
ui_checkpoint, ai_workflow
current_phase, phase_status, track_status
last_completed_phase, next_phase
phase_requires_boundary_pass, verification_boundary
recovery, synchronization_record, verification_gate
execution_authorization
acceptance_results, runtime_evidence, scope_change
```

`SESSION_STATE.json` is the operational source of truth. `TASKS.md` is only the
backlog and acceptance list. The Track plan contains scope and decisions.
`conductor/learning.md` contains only consequential lessons and reusable tool
limitations. Use `sync_phase.py` to generate the phase summary.

`lean` is valid only with `risk_level: low`; medium/high-risk Tracks must use
`strict` unless the user explicitly records an approved exception.

Choose `workflow_profile=quick` for a low-risk local change, `standard` for a
normal UI Track, and `strict` for device, persistence, network, signing, or
submission work. The profile controls ceremony and output budgets; it never
weakens product confirmation or claims unrun verification as success.

When `workflow_plan.py` returns `required_architecture_skills`, load every
listed skill before implementation. A Standard UI Track with multiple stateful
interactions therefore receives an MVVM review; a one-state Quick Track does
not.

Use `initialize_state.py` to write risk/profile/kind/UI impact; do not hand-write
an invalid combination. A required recovery must be cleared by
`record_failure.py --state-file` before the phase can continue.

## Entry and Product Gate

1. Load the current state and active Track using the context policy.
2. A direction is clear only when the user has supplied a problem or
   opportunity, primary user, and intended outcome. An app name, category, or
   feature fragment alone is vague.
3. If the direction is vague, offer bounded options or focused questions and
   wait for the user's explicit choice or custom definition. For discrete
   choices, call the interactive `question` tool so the client renders an
   option bar. Only if that tool is unavailable or dismissed, use a Markdown
   table with stable option IDs, short trade-offs, and an explicit request for
   the user's selection. Never invent the audience, problem, MVP,
   visual direction, non-goals, or platform capability.
4. Ask until the brief covers the problem, primary user, desired outcome,
   smallest successful flow, MVP, non-goals, target device, data behavior,
   visual direction, and acceptance criteria. Do not compress these into one
   guessed answer; group missing fields into a small number of user questions.
5. Set `product_status: confirmed` only after the user confirms the brief, or
   `assumptions_accepted` only when the user explicitly asks to proceed with
   stated assumptions. Do not create an implementation Track before that state.
6. If no Figma input exists, record `designInput: unavailable` and continue
    only after the product direction is confirmed.

**Interactive question requirement:** when the `question` tool is available,
you MUST call it for every bounded user choice. Do not render a Markdown
`# Questions` section, numbered text choices, or a prose question instead.
Use Markdown choices only after the question tool is unavailable or dismissed.

After loading each selected Skill, record it with `record_skill_usage.py`. Before
execution, `loaded_skills` must contain every `required_skills` entry. If the
Track requires `hmos-arkts-knowledge-retriever`, record at least one cited API
or language evidence source in `api_evidence_sources`.
For ArkTS retriever Tracks, `verification_gate --execution` also requires a
recorded `evidence_cache.py` result.

## Cycle

`initialization -> design_analysis -> strategy -> work_plan_approval ->
execution -> ui_approval (UI only) -> self_review_verification ->
synchronization -> handover`

Read `assets/conductor-template/workflows/cycle.md` for the short phase
checklist. Read `references/execution-policy.md` for risk, profile, UI impact,
verification, command-output budgets, and approval gates.

For low-risk `lean` work, recommendations may be concise, but Work Plan
Approval remains a separate explicit confirmation after the product brief.
Keep the recommendation and Work Plan decisions separate for strict or
medium/high-risk work. Do not edit application source before Work Plan Approval.

## Verification

- Run focused compile/checks during implementation.
- At an application-changing phase boundary, ensure one complete
  build/sign/device pass exists.
- Immediately after install/launch and the initial UI screenshot, use the
  interactive `question` tool to ask whether automated device interaction tests
  are approved. Record consent before lint or any interaction. Run clicks/input
  only after `record_test_consent.py --decision approved`; a declined decision
  blocks runtime completion rather than silently skipping evidence.
- Record runtime/source match with `record_runtime_evidence.py`; a mismatch
  blocks interaction tests and handover.
- Reuse a successful unchanged UI approval checkpoint; otherwise run the
  boundary pass.
- Repeat only after source, packaging, signing, runtime, or device-impacting
  changes, or after failure.
- Use `lint_cache.py` before lint. Its unchanged zero-file result is reusable
  until the tool version, configuration fingerprint, or target fingerprint
  changes.
- At execution start, run `context_cache.py`, reload/record context when it
  returns `RELOAD_CONTEXT`, then run `verification_gate.py --execution`.
- Only after `GATE_PASS`, run `authorize_execution.py` with the current source
  revision. Do not edit application source before `EXECUTION_AUTHORIZED`.
- Run `verification_gate.py --phase-boundary` before boundary validation and
  `verification_gate.py --post-verification` after the actual lint/build/device
  results are recorded. Run `verification_gate.py --handover` before handover.
  The gate is a compact preflight decision; it does not replace build, lint, or
  device commands.
- Record the actual boundary result with `record_boundary.py`; do not hand-edit
  `verification_boundary.status` to `passed`.
- The phase-boundary gate records `verification_boundary.status: gate_passed`;
  only actual build/sign/device evidence may change it to `passed`.
- A verification phase must actually call `context_cache.py`,
  `evidence_cache.py` when API evidence is relevant, and `lint_cache.py` before
  lint. A documented cache rule without the command result is not verification
  evidence.
- Use `context_cache.py` before rereading phase context and `evidence_cache.py`
  before repeating an API search. Reuse only when phase, files, SDK, and query
  fingerprints are unchanged.
- A missing device or required signing configuration is a blocker or an
  explicit `signing: not_configured` result, never a false success.
- Do not scan a repository with `Glob "**/*"` by default. Scope discovery to
  the target module, changed file types, and root configuration files.
- Do not dump full device logs into the conversation. Filter for the first
  actionable error and retain complete output in an artifact log.
- Always use `scripts/devecocli_docs_bridge.py` for both `devecocli docs search`
  and `devecocli docs read`; never call raw `devecocli docs read` in a normal
  workflow. Treat bridge output with `context_status=translation_required` as
  an internal queue, never as final context. Translate each queued snippet
  locally, preserve its `document_id`, and use only translated English
  `ready_context` for later reasoning.

Use `devecocli` through `ohos-app-dev` for build, lint, deployment, and device/UI
operations. Require a zero `devecocli` build exit code and successful build output.
Do not invoke Hvigor directly unless the user requests lower-level diagnostics.

## Fixed Script Invocations

Use these known signatures without running `-h` or `--help`:

```powershell
python record_acceptance.py --path <add|complete|filter|delete|persistence> --result <passed|blocked|not_attempted|out_of_scope> SESSION_STATE.json
python lint_cache.py --tool-version <version> --config-fingerprint <config> --target-fingerprint <target> [--record passed|failed|zero_files] SESSION_STATE.json
python context_cache.py SESSION_STATE.json --phase <phase> --files <file>... [--record]
python verification_gate.py SESSION_STATE.json --phase-boundary --context-phase <phase> --context-files <file>...
python record_boundary.py --status <passed|blocked> --source-revision <revision> --packaging-revision <revision> --signing <not_configured|skipped|passed|failed> --reason <reason> SESSION_STATE.json
python evidence_cache.py SESSION_STATE.json --topic <topic> --sdk <sdk> --query-fingerprint <query> --scope <components|state|signatures> --record --document-id <id> --section <section> --source-kind <kind> --summary <summary>
python verification_gate.py SESSION_STATE.json --execution --context-phase <phase> --context-files <file>... --evidence-topic <topic> --evidence-sdk <sdk> --evidence-query-fingerprint <query> --evidence-scope <components|state|signatures>...
python verification_gate.py SESSION_STATE.json --post-verification --lint-tool-version <version> --lint-config-fingerprint <config> --lint-target-fingerprint <target>
python state_update.py --required-skill <skill> --assumption "<assumption>" --next-action "<next action>" SESSION_STATE.json
python sync_phase.py SESSION_STATE.json --task-id <task-id> [--tasks-file TASKS.md]
python validate_state.py SESSION_STATE.json
python bootstrap_summary.py SESSION_STATE.json
python clean_ai_workflow.py AI_WORKFLOW.md
python verification_gate.py SESSION_STATE.json --handover
```

The finalization order is fixed: record acceptance and lint results, record
context, pass the phase-boundary gate, record the actual boundary, pass the
post-verification gate, set `next_action`, synchronize, validate, clean the AI
workflow, enter handover, pass the handover gate, then complete handover.

## Learning and Status

Record only failures that change an implementation decision, expose a reusable
lesson, affect reproducibility, require a fix/retry, or create a blocker.
Keep repeatable limitations under `## Known Tool Limitations` with command,
symptom, workaround, and scope. Show only the new lesson, not the entire log.
Keep `learning.md` as an index and current summary; put reusable limitations in
`learning/limitations.md` and consequential incidents in `learning/incidents.md`.

Use command levels from the execution policy. Send status at implementation,
compile, device validation, phase transition, synchronization, and around L2/L3
commands. Batch L0/L1 operations into the nearest milestone.

If a build or verification command times out, record
`BUILD_WRAPPER_TIMEOUT`/`wrapper-exit-unconfirmed` and stop that verification
step. Before any retry, run `record_failure.py` for the first consequential
cause and announce the separately authorized recovery command. Do not infer
success from a later `run` command's internal build.

## State Safety

When a phase completes, keep `current_phase` on that phase, set
`last_completed_phase` to it, and set `next_phase` only as an intention. Start
the next phase with a separate update that sets `current_phase = next_phase` and
`phase_status = in_progress`.

Run the installed validator at synchronization and before handover:

```powershell
python "<resolved-conductor-dev-root>\scripts\validate_state.py" SESSION_STATE.json
```

An invalid state blocks the transition. A Track is `handed_over` only after
verification, synchronization, and the handover report.

## Handover

Use the phase summary and state to produce a concise handover containing status,
boundary result, UI decision, blockers, deferred work, and artifact paths. Do
not repeat the full command transcript or learning history. Ask what to do next
only after the handover state is recorded.

## Resources

- `assets/conductor-template/workflows/cycle.md`: phase checklist.
- `assets/conductor-template/workflow.md`: project-facing workflow.
- `assets/conductor-template/setup_state.json`: initial state.
- `references/context-policy.md`: context and specialist loading.
- `references/execution-policy.md`: risk, profiles, verification, and output budgets.
- `references/agency-workflow.md`: state and synchronization model.
- `scripts/validate_state.py`: state transition validation.
- `scripts/lint_cache.py`: reusable lint result cache.
- `scripts/sync_phase.py`: phase summary and optional task synchronization.
- `scripts/context_cache.py`: phase context reuse check.
- `scripts/workflow_plan.py`: selects the smallest phase set for quick,
  standard, or strict work.
- `scripts/record_question_gate.py`: records decisions made through the
  interactive question bar.
- `scripts/quick_complete.py`: closes a Quick Track after focused verification
  without UI approval, device pass, synchronization, or handover.
- `scripts/change_impact.py`: classifies changed files and affected modules.
- `scripts/incremental_verify.py`: runs module-scoped incremental build and
  deploys with `devecocli run --skip-build`.
- `scripts/devecocli_docs_bridge.py`: calls `devecocli docs search --format
  json --limit 3` or `devecocli docs read <document-id>`, keeps short relevant
  snippets, and marks non-English text for local model translation instead of
  passing raw full documents into context.
- `scripts/evidence_cache.py`: API evidence reuse check.
- `scripts/ai_workflow.py`: incremental AI workflow recording.
- `scripts/prepare_artifacts.py`: creates screenshot and log directories.
- `scripts/record_skill_usage.py`: records loaded Skills and evidence sources.
- `scripts/record_failure.py`: records a consequential incident before retry.
- `scripts/clean_ai_workflow.py`: removes unfinished AI workflow placeholders.
- `scripts/verification_gate.py`: compact phase-boundary and handover preflight.
- `scripts/initialize_state.py`: writes only valid risk/profile initialization.
- `scripts/compact_command.py`: captures long command output and returns one-line results.
- `scripts/state_update.py`: validates and atomically updates session state.
- `scripts/bootstrap_summary.py`: creates a short session bootstrap summary.
- `scripts/authorize_execution.py`: creates the execution authorization token.
- `scripts/record_boundary.py`: records actual build/sign/device evidence.
- `scripts/record_test_consent.py`: records user consent for device automation.
- `scripts/record_acceptance.py`: records CRUD and in-scope or out-of-scope
  persistence path results.
- `scripts/record_runtime_evidence.py`: records foreground/source match.
- `scripts/record_scope_change.py`: records approval for out-of-plan files.
