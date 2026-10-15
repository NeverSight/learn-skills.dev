---
name: herdr-agent-orchestration
description: "Coordinate multiple coding agents through Herdr panes in one workspace. Use when the user asks to plan, delegate, supervise, review, or dogfood work with OMP or other agents through Herdr. Requires HERDR_ENV=1."
version: 0.1.0
---

# Herdr Agent Orchestration

Use this skill when one agent coordinates other coding agents through Herdr. This is a coordination layer on top of the `herdr` skill at `skill://herdr`.

### Prerequisite

Install the upstream `herdr` skill before dispatching:

```bash
npx skills add ogulcancelik/herdr -g -s herdr
```

If the host cannot resolve `skill://herdr` (e.g. install targets other than OMP, or hosts where the herdr skill is not picked up), the following inline rules are the minimum safety floor. They are a strict subset of `skill://herdr` and are not a replacement for it.

Inline floor (always true):

- Verify `HERDR_ENV=1` before any `herdr` control command.
- Pane and agent creation commands return JSON; parse the id from `.result.*.id` and never infer from pane order.
- Lifecycle states: `idle` means the agent is ready; `working` means active; `blocked` means it needs input/approval; `done` is the same as `idle` until the tab has been seen by the user; `unknown` is not completion.
- `agent prompt --wait` returns on the first settled state; do not poll past `--wait` timeout unless a rolling wait is documented in the contract.
- `agent_prompt_stalled` returns when no lifecycle change is observed within 5s; treat as BLOCKED, not as a failure.
- Close only panes that this task created; never close the parent pane or other clients' panes.

## Hard constraints

- All of the inline floor rules above apply.
- Keep workers in the current Herdr workspace by default. Do not create a workspace, tab, worktree, or alternate cwd unless the user explicitly requests it. Create a worktree only when workers need separate Git branches/checkouts or genuinely different toolchain/runtime isolation.
- Prefer sibling panes in the current tab. Split right for a worker column, then split that column down for additional workers. Use `--no-focus` unless the user explicitly requested focus. After each split, verify the layout if focus or topology matters.
- Never infer IDs from pane order. Parse every creation response and use the returned ID.
- Use a unique agent name as the stable worker identity. Pane IDs are coordinates and may change after moves.
- Never treat `unknown` as completion. `idle` means settled/available, not proof that the requested turn completed; accept only after the report and coordinator verification are present. Prefer exact `done` when available.

## Coordination model

Use this contract in every worker prompt. The coordinator must create a per-run, private report directory before dispatch:

```bash
run_id=$(date -u +%Y%m%dT%H%M%SZ)
report_dir="${XDG_RUNTIME_DIR:-/tmp/herdr-reports}/$run_id"
mkdir -p -m 700 "$report_dir"
```

Use `$report_dir` as the base for all worker `REPORT:` paths. The default `/tmp/herdr-reports` directory is ephemeral and world-readable; do not place secrets, tokens, or sensitive raw diffs there. For sensitive workflows, switch to a restricted report directory under the current user's runtime/cache directory.

Contract fields (READ, WRITE, VERIFY, DO_NOT_TOUCH, DEPENDENCIES) are required when applicable and may be marked `none` when not. The report is authoritative if chat text disagrees.

```text
TASK_ID: <stable id>
ROLE: <role>
GOAL: <observable outcome>
READ: <files or directories, or none>
WRITE: <allowed files or directories; write permission only>
VERIFY: <worker smoke commands or scenarios, or none>
REPORT: $report_dir/<task-id>.md
DO_NOT_TOUCH: <write-prohibited paths; reads are allowed unless READ forbids them>
DEPENDENCIES: <completed task ids or none>

Do not modify files outside WRITE. If a dependency report is missing, stop and report BLOCKED. If WRITE and DO_NOT_TOUCH overlap, DO_NOT_TOUCH wins. Write the complete result to REPORT.
End your response with: STATUS: PASS|FAIL|BLOCKED and REPORT: <path>. The report is authoritative if chat text disagrees.
```

### Lifecycle

1. Inspect the current pane and layout.
2. Split a sibling pane without stealing focus.
3. Start a supported agent with a unique name and explicit model/role arguments.
4. Send exactly one scoped prompt with `--wait`.
5. Read the worker state and report.
6. Run coordinator-owned verification.
7. Record PASS, FAIL, or BLOCKED before dispatching dependent work.
8. Close the worker subpane after its report is collected and no follow-up turn is needed. A completed agent process does not automatically remove its pane.

For OMP, separate role ownership from model selection. Start each role as its own process when model isolation matters:

```bash
herdr agent start omp_plan --kind omp --pane <pane-id> -- --model kimi-code/k3 --thinking max
herdr agent start omp_implement --kind omp --pane <pane-id> -- --model kimi-code/kimi-for-coding-highspeed --thinking medium
herdr agent start omp_review --kind omp --pane <pane-id> -- --model zai/glm-5.2 --thinking high
herdr agent start omp_commit --kind omp --pane <pane-id> -- --model kimi-code/kimi-for-coding-highspeed --thinking medium
```

The actual model must be read from the launch arguments or worker report; do not infer it from the role name. OMP model roles can also be inspected with `omp config list` and `~/.omp/agent/config.yml` (`modelRoles.plan`, `modelRoles.commit`, `modelRoles.default`). OMP model selectors are fuzzy-matched; verify the available selector with `omp models` and confirm the selected model in process metadata or the worker report.

When the role is finished:

```bash
herdr agent get <agent-name>
herdr agent read <agent-name> --source recent-unwrapped --lines 120
test -f "$report_dir/<task-id>.md"
herdr pane close <created-pane-id>
```

Close only panes created by this orchestration task. Keep a pane open when the user requested an interactive follow-up, the worker is blocked, or a dependent task will reuse the same agent session.

## Plan, implement, review

For dogfooding, use distinct roles rather than asking every worker to implement. Each role is a separate OMP process when model isolation matters; role labels in the prompt do not change the model.

| Role | Goal | Default behavior | Recommended OMP model |
|---|---|---|---|
| `plan_worker` | scope, assumptions, dependency graph, acceptance criteria | read-only; never edits unless explicitly assigned | configured `plan` role or a high-reasoning model |
| `implement_worker` | edit the declared WRITE slice and run focused smoke verification | balanced task model, focused smoke checks | configured `task` role |
| `review_worker` | independent findings on the implementation; no edits by default | adversarial review with a different model from the implementer | a model distinct from the implementer |
| `commit_worker` | inspect status/diff; stage only approved paths; commit only when explicitly authorized | coordinator retains Git ownership unless delegated | configured `commit` role |
| `verify_worker` | run coordinator-selected checks; report observed output; do not modify source | shell-level checks with captured output | `smol` role or a focused model |

A plan worker's report is input to the coordinator, not authorization to edit. The coordinator must synthesize the plan, resolve conflicts, and then dispatch implementation work. Workers run only focused checks; the coordinator owns integration verification.

## Parallelism and dependencies

Herdr has no native task DAG or structured `worker_done` event. Encode dependencies in the coordinator's task list and dispatch only tasks whose dependencies are PASS.

- Run independent workers in sibling panes.
- Do not run workers concurrently when they write the same file.
- Keep `package.json`, lockfiles, Git operations, PR creation, and final integration verification coordinator-owned unless the user explicitly delegates them.
- For fan-in, wait for every worker, collect every report, then run one coordinator integration gate.
- If a worker is `blocked`, inspect its report/output and answer with a new prompt. Do not send blind keys.
- If a worker is `unknown`, inspect it and wait again; do not advance the DAG.

## Coordinator and reporter protocol

Use a coordinator/reporter split for every non-trivial workflow:

- **Coordinator** owns task decomposition, dependencies, pane creation, model selection, integration, final verification, Git, and user-facing status.
- **Reporter** owns observation and evidence for one declared task. It must not silently edit outside `WRITE`, invent verification, or treat a pane prompt as proof of completion.
- **Plan reporter** returns scope, assumptions, dependencies, acceptance criteria, and unresolved decisions. It does not authorize implementation.
- **Review reporter** returns findings only by default. It does not fix files unless explicitly assigned a fix slice.
- **Verify reporter** runs the named smoke/integration check and records observed output. It does not convert a failed command into PASS.
- **Commit reporter** may inspect status and diff, but commit/push/PR remain coordinator-owned unless explicitly delegated.

Every reporter emits exactly one terminal disposition in its report:

```text
PASS    = task completed, artifacts stable, evidence available
BLOCKED = cannot continue without input, approval, credential, or dependency
FAIL    = terminal error, crash, cancellation, or unrecoverable verification failure
```

Coordinator handling:

```text
PASS    -> validate report and declared file scope, then advance dependencies
BLOCKED -> inspect the request, answer with a new prompt or escalate to the user; do not blind-retry
FAIL    -> preserve evidence, mark the slice failed, and retry only under an explicit retry policy
```

Never conflate `BLOCKED` with `FAIL`. A blocked worker is waiting for input; a failed worker is terminal. If report status and chat status disagree, report status wins and the mismatch is a worker defect.

## Cross-tool dispatch

OMP, Claude Code, and other supported agents can occupy sibling panes in the same Herdr workspace. The coordination contract is tool-agnostic, but startup, permissions, model selection, and lifecycle detection are tool-specific.

Before dispatching a tool/model combination, verify:

1. The CLI exists and prints its version/help.
2. The Herdr integration is installed and current (`herdr integration status`).
3. The requested model/alias is passed in launch arguments and its routing context is recorded. A final provider model may differ intentionally when using a custom base URL, Bedrock, Vertex, LiteLLM, gateway, proxy, or server-side routing.
4. The worker can read its required skill/prompt inputs under its permission mode.
5. The worker can write the required report path under its permission mode.
6. The coordinator can observe `working` and a settled state.

For model-sensitive tasks, distinguish:

```text
launch_model       = CLI alias or explicit model argument
provider_or_gateway = direct API, Bedrock, Vertex, LiteLLM, proxy, or gateway route
resolved_model     = final model only when the route exposes it; otherwise UNAVAILABLE
permission_mode    = tool permission policy
```

`launch_model != resolved_model` is not automatically a failure. The acceptance question is whether the configured route is the intended route and whether the evidence is sufficient for the task.

Example topology:

```text
one Herdr workspace
├── omp coordinator       (default or strong model)
├── omp plan reporter     (--model kimi-code/k3 --thinking max)
├── claude implementer    (--model sonnet --permission-mode acceptEdits)
├── omp reviewer          (--model zai/glm-5.2 --thinking high)
└── claude verifier       (--model opus --permission-mode dontAsk)
```

For `npx skills` install targets, verified agent identifiers on the current skills CLI include `codex` and `claude-code`. OMP receives the skill through its own `herdr` integration rather than as a skills-CLI agent.

Permission mode is part of the dispatch contract. A Claude worker in `dontAsk` may read but cannot write a report, while an OMP worker may have different external-directory rules. If a required read or write is denied, classify the task `BLOCKED`, change the permission mode or report path deliberately, and rerun; do not ask the worker to bypass policy.

### Residual cross-tool findings

- Claude Code's `--model sonnet|opus` is a launch alias, not necessarily the provider's final model identity. A custom `ANTHROPIC_BASE_URL`, Bedrock, Vertex, LiteLLM, gateway, proxy, or server-side routing layer may intentionally override or translate it. A different TUI/provider label is therefore not itself a failure.
- For model-sensitive acceptance, record routing provenance separately: `launch_model`, `provider_or_gateway`, `resolved_model` (when exposed), `permission_mode`, and relevant routing configuration. Mark `resolved_model` as `UNAVAILABLE` when the provider does not expose it; do not infer failure from that absence.
- Claude `dontAsk` reliably supports read-only work but may reject report-file writes. Use a write-capable mode such as `acceptEdits` for workers whose declared `WRITE` includes a report file, and still verify the exact path.
- A Claude coordinator can describe and hand off an OMP task using the same contract, but a true Claude→OMP execution cell is not PASS until the Claude process itself creates the sibling pane, starts OMP, observes its report, and closes only the created pane. A report describing the handoff is not execution evidence.
- A blocked permission test is recovered only after changing the dispatch contract or permission mode, rerunning the task, obtaining a PASS report, and closing the replacement pane. The original blocked attempt remains part of the audit trail.

## Dogfood matrix

Minimum matrix before declaring a cross-tool setup ready:

| Coordinator | Worker | Role | Model/permission | Required evidence |
|---|---|---|---|---|
| OMP | OMP | plan | explicit non-default model | model argv + PASS report |
| OMP | OMP | implement | task model | scoped diff + focused check |
| OMP | OMP | review | different model | independent findings report |
| OMP | OMP | commit | commit model, no push | status/diff + proposed commit |
| OMP | Claude | report/review | Sonnet or equivalent, write-capable mode | model UI/argv + report |
| OMP | Claude | implement | Sonnet, `acceptEdits` or deliberate approval mode | scoped file change + test |
| Claude | OMP | report/verify | explicit OMP model | model argv + report |
| Claude | Claude | Opus coordinator / Sonnet worker | explicit aliases | both lifecycle states + report |
| mixed | mixed | blocked/approval path | manual permission mode | blocked evidence + recovery prompt |

Mark a matrix cell `BLOCKED` when the tool or permission setup prevents the required evidence. Do not mark it PASS from a theoretical compatibility claim.

## Reporting and evidence

The default `/tmp/herdr-reports` directory is ephemeral and may be readable by other local users. Do not place secrets, tokens, or sensitive raw diffs there. For sensitive workflows, create a restricted report directory under the current user's runtime/cache directory and reference that path consistently in `REPORT` and the acceptance check.

Pane output is not durable. Alternate-screen agents may lose older output from host scrollback. Require a report file for any task that edits files, gates downstream work, or produces more than 50 lines of findings, and read it directly after the worker settles.

```markdown
# Worker Report
- Task: <task id>
- Role: <role>
- Status: PASS | FAIL | BLOCKED
- Files modified: <paths>
- Verification: <commands and observed results>
- Findings: <facts, risks, or questions>
- Dependencies: <task ids>
```

Coordinator acceptance is:

```text
worker state = done or idle
AND report exists and says PASS
AND declared files are the only changed files in the slice
AND coordinator verification passes
```

Use `herdr agent read <name> --source recent-unwrapped --lines 120` only for concise diagnostics. If output is truncated, read the known `REPORT` path from the contract; do not reconstruct missing output from the pane. If a worker touched a write-prohibited path, stop dependent dispatches and report BLOCKED with the exact paths; do not silently reset user changes.

## Cleanup

After reports and verification are collected, close only panes created for the task. Keep the parent pane and the user's existing workspace intact. Do not remove worktrees or branches as part of ordinary orchestration cleanup.

## Failure policy

- Treat `agent_prompt_stalled` (no observed lifecycle change within 5s) and an unexpected worker process exit as `BLOCKED` first and `FAIL` only after confirming the worker is not still completing the turn. Inspect the agent, then re-prompt or escalate.
- One failed worker: inspect the report, correct the prompt or dependency, then retry once with a changed prompt that names the failure mode; never retry the same prompt verbatim.
- Repeated failure: stop dispatching that dependent slice and report the exact blocker.
- Test failure: preserve the failure output in the coordinator report; do not mark PASS because a worker claims it is pre-existing.
- Security, data-loss, or ambiguous ownership issue: block and ask the user before editing.
- Rate-limit or provider-outage (HTTP 429, 5xx, timeouts, exhausted quota): classify as `BLOCKED`, do not advance dependent tasks, record the provider/model in the report, and back off with a single `agent prompt` retry after a coordinator-chosen delay. Do not loop the same prompt.
- Coordinator crash mid-run: rebuild state from the per-run `tasks.md` and the reports already on disk; dispatch only tasks whose dependencies are `completed` and whose report is missing. Never delete or rewrite the tasks file.

## Long startup and slow models

`herdr agent start` defaults to a 30-second startup timeout. Cold-starting a slow reasoning model, a first-run model download, or a delayed provider handshake can exceed it. Pass `--timeout` explicitly when the role uses a slow model or a cold provider. Example:

```bash
herdr agent start omp_review --kind omp --pane <pane-id> -- --model zai/glm-5.2 --thinking high
herdr agent wait omp_review --until idle --timeout 180000
```


## Per-agent dispatch notes

Use this section to choose a launch pattern, permission mode, and report path for each supported agent kind. `herdr agent start` accepts `--kind <kind> --pane <pane-id> -- <agent-args...>`. Verified on `herdr 0.7.5` with the following kinds; other kinds listed by `herdr agent start` follow the same skeleton.

Common rules for every kind:

- Coordinator must `mkdir -p /tmp/herdr-reports` (or a restricted equivalent) before dispatch.
- Pass the prompt as a positional argument or via the agent's native flag; never both.
- Herdr's own `--timeout` is for `agent start` readiness, not for the agent CLI. Do not forward it as a `--timeout` to the agent unless the agent accepts it in that position.
- Treat the agent's TUI banner as informational, not authoritative. Verify `launch_model` and `permission_mode` from launch argv, integration status, and the worker's own report.

### OMP

- Verified: integration v6, agent TUI shows the requested model in the status line.
- Launch example:
  ```bash
  herdr agent start omp_worker --kind omp --pane <pane-id> -- --model zai/glm-5.2 --thinking high --no-session
  ```
- Model selection: explicit `--model` (provider/model). `--model` is fuzzy-matched; verify with `omp models` and the worker report.
- Permissions: managed by OMP's own `tools.approval`; no agent-side permission mode flag.
- Report path: any path the worker can write; default `/tmp/herdr-reports/<task-id>.md`.
- Known footgun: a single OMP process keeps its default model. Different roles with different models need separate OMP processes.

### Claude Code

- Verified: integration v7, `claude` 2.1.220.
- Launch example:
  ```bash
  herdr agent start claude_worker --kind claude --pane <pane-id> -- --model sonnet --permission-mode acceptEdits
  ```
- Model selection: `--model <alias-or-full>` (e.g. `sonnet`, `opus`, `claude-opus-5`). The TUI banner may not match the resolved provider model when a custom `ANTHROPIC_BASE_URL`, Bedrock, Vertex, LiteLLM, gateway, or proxy is in use. Record `launch_model`, `provider_or_gateway`, `resolved_model` (when exposed), and `permission_mode` separately.
- Permissions: `--permission-mode dontAsk` is read-mostly and may reject report-file writes. Use `acceptEdits` for workers that must write a report file. Use `bypassPermissions` only in externally sandboxed environments.
- Report path: any path the worker can write; default `/tmp/herdr-reports/<task-id>.md`. Place the path under the agent's writable root to avoid `external_directory` prompts.
- Known footgun: short, single-line prompts are more reliable than multi-line heredoc contracts. Multi-line prompts can trigger a clarification request before the worker reads the contract.

### OpenCode

- Verified: `opencode` 1.18.x; integration not installed by `herdr integration install opencode` on this host (the kind still works because Herdr detects the binary).
- Launch example:
  ```bash
  herdr agent start opencode_worker --kind opencode --pane <pane-id> -- --model zai-coding-plan/glm-4.7 --prompt "concise single-line task"
  ```
- Model selection: `--model provider/model` (e.g. `google/gemini-3.5-flash`, `zai-coding-plan/glm-4.7`, `openai/gpt-5.4`, `openrouter/anthropic/claude-opus-4.7`).
- Permissions: pass `--auto` after `--` to skip non-dangerous confirmations; outside-directory writes still require an interactive allow/deny unless `--auto` covers them. Use a writable report path under the agent's CWD.
- Report path: prefer a path inside the current workspace (e.g. `./.opencode-reporter.md`); OpenCode's external-directory allow-list is per-host.
- Known footgun: long heredoc prompts are condensed; OpenCode may ask a clarification question before it acts. Prefer a single-line prompt with explicit output path and `STATUS:`/`REPORT:` lines.

### Codex

- Verified: integration v6; `codex-cli` 0.146.0; binary at `~/.hermes/node/bin/codex` on this host.
- Launch example:
  ```bash
  herdr agent start codex_worker --kind codex --pane <pane-id> -- --model gpt-5.4 --sandbox workspace-write "Read <file> and write a short report to <path> ending with STATUS and REPORT lines."
  ```
- Model selection: `--model <alias>`; Codex may deprecate the requested model and prompt for `Try new model` / `Use existing model`. Pick `Use existing model` if the requested model is intentional.
- Permissions: `--sandbox read-only` is the default; reads succeed but `ps`, `herdr agent get`, and writes outside the workspace require `--sandbox workspace-write` or `--dangerously-bypass-approvals-and-sandbox`. The CLI accepts the prompt as a positional `[PROMPT]`, not as `--prompt`. Herdr's `--timeout` does not forward to the agent.
- Hooks: first launch after a Codex update may surface a "Hooks need review" prompt. Pre-approve with `herdr agent send-keys <agent> down enter` (or `esc` to reject) before expecting `working` state.
- Report path: any path under the workspace; for non-workspace paths add `--add-dir <path>` to grant write access.
- Known footgun: argv is not exposed in Codex's session metadata; treat `LAUNCH`/`ARGV` fields in the report as derived from the launch invocation, not from Codex itself. The visible TUI model may not match the requested alias.

### Other supported kinds

`herdr agent start` advertises these kinds on this host (verify on the user's host with `herdr agent start --help`): `pi`, `claude`, `codex`, `gemini`, `cursor`, `devin`, `agy`, `cline`, `omp`, `mastracode`, `opencode`, `copilot`, `kimi`, `kiro`, `droid`, `amp`, `grok`, `hermes`, `kilo`, `qodercli`, `maki`.

For any kind not covered above:

1. Read the binary's `--help` and `herdr agent start` for the kind.
2. Confirm the integration status with `herdr integration status`. Install with `herdr integration install <kind>` if missing.
3. Match the launch pattern to the agent's CLI: positional `[PROMPT]`, `--prompt "..."`, or subcommand `exec`/`run`. Pass the prompt only once.
4. Set permission mode to one that allows the declared `WRITE` paths.
5. Verify the launch model with `herdr agent get <name>` and the worker report.
6. Record `argv`, `permission_mode`, `model` (TUI), `provider_or_gateway`, and `resolved_model` (when exposed).

## Per-agent prompt template

For agents that accept a positional prompt (OpenCode, Codex, Gemini), use a single-line prompt that states the read, write, verification, and closing protocol explicitly:

```text
Read <file> and write a concise 5-line reporter report to <path> describing <subject>. include the launch model and argv. end with STATUS: PASS|FAIL|BLOCKED and REPORT: <path> lines. Use only file read and write.
```

For agents that accept a multi-line contract (OMP, Claude Code), use the structured contract block under `## Coordination model`. The two forms are interchangeable; pick the form the agent can ingest without asking for clarification.
## Coordinator task list and external memory

Herdr has no native task store. Use a coordinator-owned task list as external memory for every multi-step orchestration:

```text
TaskID | Role | Status | Dependencies | Pane | Agent | Last update
```

Keep one row per dispatched task. Update the row immediately after `agent prompt --wait` returns or after reading the worker report. Do not rely on `herdr agent list` or pane UI as the source of truth — those are snapshots, not a log.

Rules:

- Statuses: `pending`, `ready`, `dispatched`, `completed`, `failed`, `blocked`.
- A task is `ready` only when all `Dependencies` are `completed`.
- Dispatch only `ready` tasks. Hold the slice on the first `failed` or `blocked` until the prompt is corrected or a user decision is recorded.
- Treat the file as an audit log. Append timestamped notes; never silently rewrite history.
- Persist the file alongside reports so a resumption can read both. Suggested location: `/tmp/herdr-reports/<run-id>-tasks.md`.

Suggested shell:

```bash
task_file=/tmp/herdr-reports/$(date -u +%Y%m%dT%H%M%SZ)-tasks.md
exec >>"$task_file"
```

## Handoff classification

Classify inherited context before dispatching, the same way Orca orchestration distinguishes coordinated dispatch from full handoff:

- **Coordinated dispatch**: a live coordinator owns the DAG and waits for this task. Follow the contract, the report file, the cleanup step, and the dependency update. Do not close until the task is recorded.
- **Full handoff**: ownership transfer, not supervision. The original actor is not monitoring a DAG. Do not create task rows, do not wait on `completed`, do not poll the worker pane after prompt delivery.
- **Handoff request words**: "hand off", "handoff", "handover", "give this to another agent", "another agent", "another worktree", "send this to another agent" default to full handoff even when the user names a model or effort level.
- **Supervision request words**: "supervise", "monitor", "wait for results", "track completion", "DAG", "decision gate", "coordinate workers", "blocking ask" keep the task on the coordinator-owned task list.

If the user names a next owner agent (e.g. "then use opencode to create a PR"), the coordinator routes, synthesizes, and supervises; the named owner performs the edits.

## Blocking ask and decision gate

Use a blocking ask when a worker needs a coordinator answer mid-task:

```bash
ask_file=/tmp/herdr-reports/<task-id>-ask.md
: >"$ask_file"
cat <<EOF >"$ask_file"
TASK_ID: <task-id>
QUESTION: <single concrete question>
OPTIONS: yes | no | specify
EOF
herdr agent prompt <agent-name> "Read $ask_file, choose one option, and end with STATUS: PASS and a one-line answer." --wait --timeout 300000
```

Inspect the worker reply. Record the answer in the task list. Do not retry; the worker has already consumed the input.

A **decision gate** is coordinator-managed: use it to record a user decision that unblocks dependent tasks. The simplest durable representation is a file under the run directory plus a row in the task list:

```text
| gate-<id> | decision | open | - | - | - | question text |
| gate-<id> | decision | resolved | - | - | - | user answer  |
```

Prefer one user prompt per gate. Do not split a single question across multiple gates.

## Heartbeat and long-running supervision

For long tasks, watch for two failure modes a wait window can miss: a stalled `--wait` and a worker that crashed silently between snapshots. Use a rolling window:

```bash
herdr agent prompt <agent-name> "continue" --wait --timeout 900000
herdr agent get <agent-name>
herdr agent read <agent-name> --source recent-unwrapped --lines 80
```

If `agent get` shows the agent is still `working` or producing activity, keep waiting. A `done`/`idle`/visible work in the recent buffer is a liveness signal; absence of either is a check, not a failure. Treat repeated idle with no report file as `BLOCKED` only after the heartbeat window elapses.

## Rolling waits and stop conditions

Rolling waits are acceptable in Herdr; there is no native `check --wait`. Stop waiting when any of the following becomes true:

- The worker sends `STATUS: PASS|FAIL|BLOCKED` with a valid report.
- The pane disappears, the shell exits, or the worker process is no longer running.
- The user explicitly asks to stop the slice.
- A coordinator-side dependency changes (e.g. user rescinds a request).

Do not kill a worker just because it has not produced a completion message. Coding tasks can take 15–60 minutes.

## Recovery: reset, but not during active coordination

There is no global Herdr reset for orchestration state. If a coordinator-owned task list file becomes inconsistent (e.g. wrong `completed` flag, lost gate resolution), repair it explicitly by writing a new row with a note. Do not delete or rewrite history; never delete reports while any dependent task references them.

For long-running server-style work, prefer `pane run` over `agent prompt` so the lifecycle is shell-level, not agent-lifecycle-bound. Capture output to a log file under the run directory and tail it on demand.

## Example: five-step coordinated run

```bash
# Step 0 — coordinator: per-run private report directory and task list
run_id=$(date -u +%Y%m%dT%H%M%SZ)
report_dir="${XDG_RUNTIME_DIR:-/tmp/herdr-reports}/$run_id"
mkdir -p -m 700 "$report_dir"
task_file="$report_dir/tasks.md"
: >"$task_file"
parent_pane="$HERDR_PANE_ID"

# Step 1 — read-only plan worker (no edits)
split=$(herdr pane split --pane "$parent_pane" --direction right --cwd "$PWD" --no-focus)
plan_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')
herdr agent start plan_worker --kind omp --pane "$plan_pane" -- --model kimi-code/k3 --thinking max
herdr agent prompt plan_worker "$(cat <<EOF
TASK_ID: plan
ROLE: plan_worker
GOAL: outline the change in three numbered steps with deliverables and acceptance
READ: $PWD
WRITE: $report_dir/plan.md only
VERIFY: report ends with STATUS: PASS and a RECOMMENDATION line
REPORT: $report_dir/plan.md
DO_NOT_TOUCH: project files
DEPENDENCIES: none
EOF
)" --wait --timeout 600000

# Step 2 — implement worker, depends on plan
split=$(herdr pane split --pane "$plan_pane" --direction down --cwd "$PWD" --no-focus)
impl_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')
herdr agent start implement_worker --kind omp --pane "$impl_pane" -- --model kimi-code/kimi-for-coding-highspeed --thinking medium
herdr agent prompt implement_worker "$(cat <<EOF
TASK_ID: impl
ROLE: implement_worker
GOAL: edit the slice described by /plan
READ: $report_dir/plan.md
WRITE: src/<slice> only
VERIFY: git diff --stat src/ shows only the declared slice and a focused smoke test passes
REPORT: $report_dir/impl.md
DO_NOT_TOUCH: package.json, lockfiles, Git history
DEPENDENCIES: plan
EOF
)" --wait --timeout 1800000

# Step 3 — review worker, depends on impl
split=$(herdr pane split --pane "$impl_pane" --direction down --cwd "$PWD" --no-focus)
review_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')
herdr agent start review_worker --kind omp --pane "$review_pane" -- --model zai/glm-5.2 --thinking high
herdr agent prompt review_worker "$(cat <<EOF
TASK_ID: review
ROLE: review_worker
GOAL: independent findings on /impl
READ: $report_dir/plan.md, $report_dir/impl.md, src/<slice>
WRITE: $report_dir/review.md only
VERIFY: every finding cites a file and line; no findings = 'no issues' line
REPORT: $report_dir/review.md
DO_NOT_TOUCH: all source files, Git history
DEPENDENCIES: impl
EOF
)" --wait --timeout 600000

# Step 4 — owner: collect reports, close created panes only
for p in "$plan_pane" "$impl_pane" "$review_pane"; do
  herdr pane close "$p"
done

# Step 5 — owner: only if the user asked for a commit
git add -A
git commit -m "feat: <scope> (plan→impl→review)"
```

## Skill boundary with `orchestration` and `orca-cli`

- Use this skill (`herdr-agent-orchestration`) when the user wants pane-based agent coordination, with the coordinator owning Herdr primitives directly.
- Use the `orchestration` skill when the user wants Orca's structured task/dispatch lifecycle with `worker_done` authority and decision gates.
- Use `orca-cli` for full ownership handoffs where the user does not ask for supervision, wait, or DAG coordination.

Do not advertise Orca's `worker_done` semantics when running in pure Herdr mode. Do not advertise Herdr pane ownership when running in Orca mode. Pick one layer per session unless the user explicitly asks for both.
