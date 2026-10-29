---
name: orchestrate-herdr
disable-model-invocation: true
description: "Dispatch spec (PRD) sub-issues to worker tabs; monitor to done. Tab, CLI, or runtime context selects herdr; without any of these: /ask-kit. Tab status or actions with no dispatch: herdr companion."
metadata:
  version: "0.8.0"
---

# Orchestrate herdr

Fan work out to one herdr-managed worker tab per unit (tracker sub-issue or harness prompt) and drive each to a test-backed end state when the task involves code. You are the **orchestrator**: never implement, never close your own tab.

## Inputs

**Run mode** — `spec` when `SPEC_REF` is present; otherwise `harness` per [`references/harness.md`](references/harness.md). Never guess an input.

- **SPEC_REF** (spec mode) — parent issue whose open sub-issues become workers: Linear `PRWL-100` / `ABC-123`, or a GitHub issue URL or number. From skill args (`SPEC_REF=...`, bare reference; legacy `SPEC_URL=`/`PRD_URL=` accepted) or intake.
- **WORKERS** (harness mode) — list of `{label, prompt}`; defined per harness reference.
- **AGENT** — worker runtime. Its `CLI_NAME` launch token serves PATH checks/tab labels; `AGENT_KIND` serves herdr `--kind`. Both come from [`references/intake.md`](references/intake.md), never the command's first token: Cursor's values differ.
- **CODING_CLI** — `CLI_NAME` plus the permission-mode flags from the user's established preference or intake choice. The prompt is never a launch argument (see Rules).
- **ISOLATION** — `worktree`, `branch`, or `shared`; it decides whether workers can run in parallel.
- **TRACKER** / **TRACKER_TAG** — workspace tracker of record (`G` / `L`). Derived per **Resolve** in [`references/tracker-map.md`](references/tracker-map.md), which holds the per-tracker commands cited by bold section name below.

**Factory stage.** Under a user-started `/factory run` on herdr, follow [`references/factory-stage.md`](references/factory-stage.md) instead of Intake.

## Rules

- **Zero attribution.** Omit co-author, AI, and tool attribution from prompts, commits, tracker comments, and reports.

- **Never implement.** The orchestrator reads, creates tabs, submits prompts, monitors, and reports — nothing else.
- **Herdr-managed tabs only,** created in the existing herdr workspace/session. No pane splits, no internal sub-agents, no nested coding sessions, and never launch `CODING_CLI` from inside another `CODING_CLI`.
- **Isolation is the user's choice, and herdr's job.** Keep the orchestrator's working directory. Create worktrees only in selected `worktree` mode through `herdr worktree create`, never hand-rolled Git. Verify project-owned placement per Intake before launch; unsupported placement blocks that worker. `branch` and `shared` tabs start in the orchestrator's folder, which must be the assigned repository's checkout.
- **Saved IDs only.** Every submit, read, monitor, and follow-up call uses a tab ID and agent name saved at creation — never the active tab, latest tab, visual order, or a guess.
- **Prompts are pasted and submitted into a ready CLI** — never passed as launch arguments/flags, never left staged or unsent, and **never pasted into a dead tab's shell**, where the prompt text would execute as commands.
- **Read completion evidence from the tab.** A task whose diff touches source or tests requires the test command and quoted passing output, however the worker describes it; a non-code task requires the evidence its prompt named, or the observable result when none was named. Spec tasks also require an `AC map:` covering every criterion. Missing proof stays incomplete; a summary alone is a claim.
- **Suggest, never auto-chain.** After the final report, suggest `/agentic-qa` for each PR whose `AC map` owes rows to it, `/code-review` on the workers' diffs, or `/release-notes` for what shipped — suggest only, then stop.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Transitions: tabs created, prompts submitted, any worker status change, final report.

### 1. Pre-flight

Fail fast before creating anything, naming what is missing:

1. `HERDR_ENV=1` is set — you are inside herdr. Not set → stop.
2. Load the herdr companion per **Companion** in [`references/herdr-commands.md`](references/herdr-commands.md) unless already in context — it ships inside the binary, so this is a load, not a gate. That file holds the herdr commands cited by bold section name below.
3. **Mode:** `SPEC_REF` present → **spec**; no `SPEC_REF` → **harness**. When the run uses tracker APIs (spec mode, or harness workers with issues), resolve `TRACKER` / `TRACKER_TAG` per **Resolve** and run that tracker's access check.
4. **Harness-only:** empty **WORKERS** after define step → stop.

### 2. Build the worker set

**Spec** — list open sub-issues per **Discover**. State the count and cross-check against the spec before tabs — under-fanning drops slices. Every open sub-issue; `ready-for-agent` does not filter. Identifier `<n>` per issue. Zero open → stop before Intake. A sub-issue blocked by another open sub-issue is not parallel work; list pairs per **Discover** and ask in Intake question 3.

**Harness** — define **WORKERS** per [`references/harness.md`](references/harness.md). State the count before tabs.

### 3. Intake

Ask **one batched question set**, after Discover and never before — two of the four need the issue list. Name the affected issues and repos in the questions. Away-fallbacks and the full matrices: [`references/intake.md`](references/intake.md).

1. **Which coding agent.** Offer all six runtimes **by product name** per Intake roster; parenthesised token is `AGENT_KIND`. Never label an option with a bare binary. Offer every runtime whose launch token is on PATH and say which are missing.
2. **Which permission mode.** Reuse the user's established permission mode; otherwise offer the verified interactive preset or bare launch token per Intake. The selected mode becomes `CODING_CLI`.
3. **How work is isolated.** `worktree`, `branch`, or `shared`; recommend `worktree` whenever two open sub-issues share a repo.
4. **Leftover tabs and agents** from a previous run of this spec — monitor them, or create alongside.

### 4. Create worker tabs

Save the caller's workspace, tab, and folder per **Context**. One tab per worker: spec → `[CLI_NAME] - <TRACKER_TAG> #<n>`; harness → `[CLI_NAME] - <label>`. `ISOLATION` picks **Creating worktrees** or **Create tab**. Save each worker's context, tab/pane IDs, agent name, and verified checkout record per [`checkout binding`](references/checkout-binding.md). An unresolved repository or wrong native placement blocks launch.

### 5. Launch workers

Parallelize the slow parts across tabs:

- Start every worker per **Start agent**, `AGENT_KIND` as `--kind` and `CODING_CLI`'s flags after `--`. Each call blocks until its agent is ready, so issue them concurrently. `branch` isolation on a shared checkout is the exception: dispatch those workers one at a time. Never poll or sleep for readiness. `agent_not_ready` means it booted straight into an approval UI — surface that under Needs user, never relaunch it; any other error is a dead-CLI case under Monitor.
- Submit that issue's worker prompt per **Submit**.

A worker is not launched until its tab ID and agent name are saved, its prompt is accepted, and its first response is visible.

**Spec:** fill [`references/worker-prompt.md`](references/worker-prompt.md), one issue per worker. **Harness:** append its footer and checkout binding to that worker's prompt. Pass applicable instructions and the saved checkout record; workers verify identity and baseline before edits. Local lanes when useful; never cloud.

Code workers without `/tdd-loop` still owe test evidence; say so in the launch update.

### 6. Monitor

Wait on lifecycle state per **Watch** — it reacts the moment a worker settles, and needs no sweep. Read a settled tab per **Read**. After compaction or restart, recover per **Context** before any call.

- **States:** `blocked` → an approval or question UI; surface under Needs user, never relaunch or answer it. `idle` / `done` → read the tab for the report. `working` → leave it.
- **Stalls:** `unknown` never proves completion. After a start, submit, or wait error, inspect state and output before retrying; a timeout can follow successful submission. Agent gone → redo Launch workers once after confirming its process exited. A live long test stays running; silence alone never makes it blocked. Report a blocker only with an observed failure or missing human decision.
- **Labels:** human blocker on a tracker-assigned worker → `ready-for-human` and a decision comment per **Block**. Never edit issue titles (no `BLOCKER:`, `AFK:`, or `HITL:` markers).
- **Completion:** read each tab per **Read**; quote passing test output for code tasks, assigned evidence for non-code tasks.
- **Status board:** on every state-change wake, emit a one-line count — `N running · M completed · K blocked/needs-user` — naming any tab whose state changed.

### 7. Report

Report mode, agent, isolation, workspace/session ID, folder, tab map and assignments, each end state, task evidence, and `AC map` / `Decisions` / `Open items` (`AC map` in spec mode). In `worktree`/`branch` mode, list files changed by multiple branches (`git diff --name-only <base>...<branch>`) as merge risk.

## Completion criteria

- [ ] The final tab map accounts for every worker in the set (discovered sub-issues or harness **WORKERS**), including failed launches and exited workers; saved IDs and end states match read-back
- [ ] Each tab, read back, shows its submitted prompt and a worker response — nothing staged or unsent
- [ ] Each launched worker's checkout and instructions match its prompt; write tasks report baseline and first-write identity
- [ ] In `worktree` or `branch` mode, each worker's commits land on that issue's branch and no other
- [ ] Every worker is completed with code-test or assigned non-code evidence (plus spec `AC map`), blocked, or errored
- [ ] Each blocked tracker-assigned issue shows `ready-for-human` and a decision-naming comment in the **Verify** read-back, title unchanged
- [ ] The transcript ends with the final report and the `/agentic-qa` / `/code-review` / `/release-notes` suggestion — nothing after it
