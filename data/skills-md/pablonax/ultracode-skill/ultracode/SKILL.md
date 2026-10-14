---
name: ultracode
description: "Run a lightweight Ultracode workflow for serious coding tasks: plan, split, delegate when useful and allowed by the host, integrate, and verify. Use when the user explicitly invokes ultracode, $ultracode, ultra code, dynamic workflow, workflow orchestration, multi-agent workflow, subagent workflow, parallel agents, swarm, delegate this, split this across agents, or independent verification pass."
---

# Ultracode

Run a supervised workflow for work that needs planning, packetization, native agent delegation, integration, and verification.

This is a skill, not a runtime. It works by giving the current coding agent a disciplined operating procedure. It can be used in Codex, Claude Code, Antigravity, or another host that loads `SKILL.md`, but the host's own system rules and available tools always win.

## Contract

- Do not claim to be an official Claude, OpenAI, Google, or Antigravity feature.
- Ultracode itself is just a skill: no bundled runtime, hidden runner, or required scripts.
- Use task-specific tools exposed by the current host when the task needs them.
- Create and update workflow artifacts directly as Markdown and JSON files.
- Use native subagents when the current host exposes them, the task benefits from parallel work, and the user's request or host policy permits delegation.
- Do not commit, push, publish, or deploy unless the user explicitly asks for that action.
- Treat an explicit `ultracode`, `$ultracode`, or "ultra code" request as permission to choose delegated mode when the host allows that interpretation.
- In Codex, prefer real `spawn_agent` for useful independent packets when the request clearly invokes Ultracode or otherwise asks for subagents, delegation, parallel agents, a swarm, or equivalent agent work.
- For explicit Ultracode on a non-trivial task, delegated mode is the default when native agents exist and any independent sidecar work would help.
- Choose no native agents only when the task is small, tightly coupled, lacks useful independent packets, needs the next blocking decision locally, native agents are unavailable, or the user restricts delegation.
- In hosts with a different dynamic-workflow policy, follow that host's policy.
- If a host policy requires separate delegation wording, do not fight it; use workflow mode and mention that native delegation was not permitted.

Use the smallest workflow that can prove the result. Do not create ceremony for small tasks.

## First pass

Before acting, classify the task:

- type: research, code change, bug fix, migration, audit, docs, design, QA, release
- risk: low, medium, high
- blast radius: single file, module, repo-wide, external system
- verification: none, command, tests, build, browser, manual checklist
- delegation: useful, not useful, allowed by host, blocked by environment

Then choose one mode.

## Modes

### Direct mode

Use for small, clear tasks that do not benefit from packets.

Examples:

- answer a narrow question
- inspect one file
- run one command
- fix one typo
- change one small function

Behavior:

- Do the task directly.
- Do not create workflow artifacts unless the user asks.
- Verify with the narrowest useful check.
- Mention that full workflow was not needed only when useful.

### Workflow mode

Use when the task has multiple phases, meaningful uncertainty, or enough risk to benefit from separated work packets.

Examples:

- broad repo audit
- research plus implementation plan
- risky review where perspectives should stay separate
- multi-step refactor
- feature implementation with discovery, code changes, and verification

Behavior:

- Create a run directory using the run root rule below.
- Write `plan.md`, `orchestration.md`, `state.json`, packet files, result notes, `integration.md`, and `final-report.md`.
- Execute packets as isolated passes in the parent session when delegation is unavailable or not permitted.
- Keep packet notes under `results/`.
- Integrate all packet results before final verification.

### Delegated mode

Use when the host exposes native agent delegation, the task has independent packets, and delegation is permitted under that host's rules.

Strong delegation wording includes:

- subagents
- parallel agents
- swarm
- delegate or delegated workflow
- multi-agent workflow
- run agents
- split this across agents

An explicit `ultracode`, `$ultracode`, or "ultra code" invocation can also be treated as delegation permission when the host allows the skill to choose its own workflow depth. If host policy is stricter, use workflow mode.

Behavior:

- Create workflow artifacts before delegation.
- Keep the immediate blocking task in the parent session.
- Delegate only bounded sidecar work that can run in parallel.
- Default to 2-4 sidecar agents for useful independent work.
- Do not exceed 5 sidecar agents total across the run without explicit user approval.
- Run at most one broad implementation wave and one review or verification wave unless the user approves more.
- Prefer delegation for read-heavy exploration, tests, triage, and summarization.
- Use write-heavy agents only when file ownership is disjoint and clear.
- In Codex, use `explorer` agents for read-only questions and `worker` agents for concrete code changes when available.
- In other hosts, use the closest native agent/task primitive.
- Tell write-capable agents they are not alone in the codebase and must not revert edits made by others.
- Wait only when a delegated result blocks the next parent step.
- Integrate all results before final verification.

If native delegation is unavailable, fall back to workflow mode and say so briefly.

## Host delegation primitives

Use the native primitive exposed by the current host. If the named primitive is unavailable in the current session, use workflow mode.

| Host | Preferred primitive | Notes |
| --- | --- | --- |
| Codex | `spawn_agent`, then `wait_agent`, `send_input`, or `close_agent` as needed | Use `explorer` for read-only packets and `worker` for bounded write packets. Treat `$ultracode` as delegated-workflow intent when policy permits; if policy blocks delegation, fall back to workflow mode and say so. |
| Claude Code | Native Task/subagent or dynamic workflow tool, when exposed | If only the skill text is available, write packet artifacts and execute isolated parent-session passes. |
| Antigravity | Native agent/task primitive, when exposed | If no delegation primitive is present, use workflow mode with packet artifacts. |
| Other hosts | Closest native agent/task primitive | Never invent a runner. Fall back cleanly when no primitive exists. |

## Codex native delegation

When running inside Codex and delegated mode is selected:

- Use Codex's native `spawn_agent` tool. Do not try to launch agents through Python, shell scripts, subprocesses, or local workflow files.
- Spawn `explorer` agents for independent read-only discovery, tracing, risk review, test discovery, and verification planning.
- Spawn `worker` agents only for bounded implementation packets with explicit, non-overlapping ownership.
- When setting `agent_type` to `explorer` or `worker`, do not also request a full-history context fork. Use a self-contained prompt with the repo path and packet context, or omit `agent_type` when a full-history fork is required.
- In every worker prompt, include: `You are not alone in the codebase. Do not revert edits made by others. Adapt to nearby changes.`
- Do not delegate the parent critical path or work needed for the next immediate decision.
- Do not wait immediately after spawning unless the parent session is blocked on that result.
- If `spawn_agent` is available and the request invokes Ultracode or explicitly mentions agents, parallel work, delegation, a swarm, or splitting across agents, prefer real spawned agents over simulated packet passes whenever host policy permits it.
- If `spawn_agent` is unavailable, permission is not clear, or no independent packet would benefit from an agent, use workflow mode with packet files and record the concrete no-delegation reason.

## Workflow artifacts

Run root rule:

- Default to `.workflow/ultracode/`.
- If project instructions name a different scratch or workflow directory, use that instead.
- Use `.context/ultracode/` only when workspace instructions explicitly name `.context/` as the scratch area.

Default run root:

```text
.workflow/ultracode/
```

Workspace override, only when instructed:

```text
.context/ultracode/
```

Run layout:

```text
<run-root>/<slug>/
  plan.md
  orchestration.md
  state.json
  packets/
  results/
  integration.md
  final-report.md
```

Create optional heavy artifacts only when they reduce risk:

```text
eval-contract.md    # full contract only
contracts/          # only when one packet produces a surface another consumes
handoffs/           # only when separate handoff files reduce integration risk
final-audit.md      # high-risk or full-contract runs
```

Read `references/packet-schema.md` when filling packet files, result files, `orchestration.md`, or `state.json`.

## Eval contracts

Before splitting work, choose the smallest contract level:

- `none`: tiny direct task.
- `inline`: ordinary workflow or delegated task. Put 5-12 lines in `plan.md`.
- `full`: high-risk, cross-surface, migration, public API/schema/CLI/UI flow/auth/data contract, or write-capable agents sharing integration surfaces.

Inline contract template:

```text
Eval contract:
- Outcome:
- Shared surfaces:
- Required checks:
- Blocking conditions:
- Handoff evidence:
```

Read `references/eval-contracts.md` before creating a full contract.

## Plan

Keep `plan.md` concrete. Include:

- goal
- success criteria
- current context
- constraints
- risk level
- approval gates
- mode
- work packets
- eval contract
- integration policy
- verification plan
- completion criteria

For non-trivial workflow mode after explicit Ultracode, include the concrete reason native agents were not used.

Do not let the plan replace execution.

## Orchestration

Keep `orchestration.md` short and operational. Include:

- parent critical path
- packet list with owners
- agents to spawn or invoke, if allowed
- delegation count, wave count, and fallback reason
- wait points
- fallback if delegation is unavailable
- verification order

Use it as the execution contract, not as a transcript.

## Delegation policy

Before spawning or invoking another agent:

- Identify the parent critical path and keep it local.
- Confirm the delegated packet is bounded and non-blocking.
- Assign explicit ownership.
- State whether the packet is read-only or write-capable.
- Avoid duplicating packet work across agents.

Never use delegation to avoid understanding the integration path.

## Approval gates

Ask one clear approval question before:

- deletion, overwrite, mass rename, or force push
- publishing, deployment, emailing, or posting
- production data changes
- credentials, secrets, billing, or user accounts
- broad codemods
- expensive or long-running agent swarms
- irreversible repository operations

If approval is missing, continue only with safe read-only work, local drafts, or non-destructive checks.

Read `references/approval-gates.md` when risk is ambiguous.

## Packet design

Good packets are narrow, bounded, and evidence-based.

Good read-only packets:

- find entry points for a feature
- trace data flow from route to storage
- find existing tests and fixtures
- identify migration risk
- compare current behavior with docs

Good write-capable packets:

- update backend validation in named files
- add tests for one module
- update docs only
- refactor one isolated adapter

Bad packets:

- fix the whole thing
- figure it out
- implement everything
- review whatever changed
- edit any files you need

For code-edit packets, assign non-overlapping files or modules.

## Agent prompts

Read-only agent prompt shape:

```text
You are working in the same repo as other agents.

Task:
<specific read-only objective>

Do:
- inspect only the sources listed below unless one nearby hop is required
- cite file paths and line numbers where possible
- return concise findings with evidence

Do not:
- edit files
- run destructive commands
- duplicate other packet work

Expected output:
- summary
- evidence
- risks
- recommended parent action
```

Write-capable agent prompt shape:

```text
You are not alone in the codebase. Other agents may edit other files.
Do not revert edits made by others. Adapt to nearby changes.

Ownership:
<files or module>

Task:
<specific implementation task>

Do:
- edit only the owned files unless blocked
- add or update focused tests if the owned area has tests
- list changed files in your final answer

Do not:
- change public behavior outside this packet
- run broad formatting over unrelated files
- rewrite unrelated code
- commit, push, publish, or deploy

Expected output:
- files changed
- summary
- verification run
- risks or blockers
```

## Integration

The parent session owns integration.

After packet work:

- Read each result.
- Check claimed file edits.
- Check changed surfaces against the eval contract when one exists.
- Resolve disagreements using source files, tests, docs, or primary sources.
- Reject outputs that lack evidence.
- Update `integration.md`.
- Update `state.json`.

Never paste raw agent logs as the final answer.

## Verification

Choose checks by risk.

Low risk:

- inspect diff
- run a targeted test if available

Medium risk:

- targeted tests
- typecheck or lint
- affected build

High risk:

- full tests if practical
- build
- browser or CLI smoke
- manual checklist
- independent review pass

Final audit rules:

- Re-read `plan.md`, `orchestration.md`, and the full contract when present.
- Verify declared deliverables exist or changed.
- Run required checks or mark them as skipped with a reason.
- Mark checks as `pass`, `fail`, `trust-prior`, or `skipped`.
- Put final audit evidence in `final-report.md`.
- Create `final-audit.md` for high-risk or full-contract runs.

Report skipped checks honestly.

## Final answer

Keep the final answer shorter than `final-report.md`. Include:

- outcome
- important files changed or artifacts created
- verification run
- skipped checks
- remaining risk

## References

- Read `references/packet-schema.md` when creating packet files, result files, `orchestration.md`, or `state.json`.
- Read `references/eval-contracts.md` before full contracts or cross-surface delegation.
- Read `references/approval-gates.md` before risky or ambiguous work.
- Read `references/execution-examples.md` when mode behavior is unclear.
- Read `references/forward-testing.md` when testing or improving this skill.
