---
name: long-running-agent-harness
description: Plans and structures large-scale work for AI agents across many sessions. Human and AI iterate to produce a design doc; run an Initializer sub-agent once to create feature list, runbook, and backlog in _working/; then repeatedly run a Coding sub-agent until all features pass. At milestones (e.g. end of a work-unit group), pause for human check-in, re-run Initializer, then continue. Prompts are passed to sub-agents when spawning (no copying into .cursor/rules). Use when planning multi-session agent work, long-horizon coding from a design, or handoff between coding sessions.
---

# Long-running agent harness

Plan and scaffold work so an AI agent can make **incremental, verifiable progress** across many context windows. Flow: **design doc (human + AI)** → **Initializer once** (creates feature list, runbook, backlog, progress) → **Coding agent in a loop** until done. The implementation backlog defines **one work unit per session** and helps identify **milestones** for human check-in. Based on [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## Problem

Agents work in discrete sessions with no memory. Without structure they tend to: (1) try to do too much in one go and leave half-implemented, undocumented state; (2) declare the job done too early; (3) leave bugs or undocumented progress. A **harness** gives each new session a clear picture of state and one concrete unit of work.

## Workflow overview

| Phase | Who | What |
|-------|-----|------|
| **0. Design doc** | Human + AI | Iterate in chat (or doc) with the user to produce one design doc: scope, acceptance criteria, tech stack, run/verify steps. No implementation. |
| **1. Initializer (once)** | AI (sub-agent) | Run the Initializer prompt. Reads `_working/design.md`. Creates/refreshes in `_working/`: feature list (YAML), runbook, implementation backlog, progress file, optional init script. Does **not** implement features or create project scaffolding (assumes existing repo). |
| **2. Coding loop** | AI (sub-agent each time) | Run Coding agent sessions: read progress → pick **one work unit** from the backlog → implement → verify using runbook → update progress and feature list → commit. **At milestones** (e.g. end of a work-unit group): pause, check in with the human; when satisfied, re-run Initializer, then continue. **Loop until all features pass or the user stops.** |

The top-level agent invokes the Initializer and each Coding session as **sub-agents**, passing the relevant prompt each time (no need to copy prompts into `.cursor/rules/`). Use whatever mechanism Cursor provides to spawn a sub-agent or new task and pass the prompt content (e.g. the contents of the Initializer or Coding prompt file).

## Phase 0: Design doc (human + AI)

- **Goal**: One design doc that defines scope, acceptance criteria, and enough context for the feature list and runbook.
- **Process**: Human and AI iterate (in chat or a shared doc). AI suggests structure and content; human refines. Optionally use the **doc-coauthoring** skill for the design doc.
- **Output**: Design doc at `_working/design.md`. This is the **input** to the Initializer (which creates the feature list and other harness artifacts).

## Two-phase execution (Initializer + Coding agent)

### Initializer (run once)

Run the Initializer prompt (e.g. via sub-agent). It:

1. Reads the design doc and any existing context.
2. Creates or refreshes in `_working/`: `agent-runbook.md`, `implementation-backlog.md`, `agent-progress.md`, `feature_list.yaml`, and optionally `init_<app\>.sh`.
3. Does **not** implement features. Output: list of artifacts and the recommended first coding target.

### Coding agent (every session, until done)

Run the Coding agent prompt (e.g. via sub-agent). Each session:

1. **Session start**: If any of `_working/agent-progress.md`, `_working/agent-runbook.md`, `_working/implementation-backlog.md`, `_working/feature_list.yaml` are missing → run Initializer first.
2. **Get bearings**: Read `_working/agent-progress.md` → `_working/implementation-backlog.md` → `_working/feature_list.yaml` → `_working/design.md` → `_working/agent-runbook.md` → recent git log.
3. **Pick one unit**: At most one page/feature from the backlog that still has failing (or unimplemented) criteria.
4. **Implement**: Implement only that unit. Add tests. Run lint/typecheck/tests from the runbook; fix failures.
5. **Feature list**: Set `passes: true` **only** for criteria verified this session.
6. **Handoff**: Append a "Session N" block to progress; commit; leave repo runnable.

**Loop**: After each session, if not all features pass and the user has not stopped, run the Coding agent again (new sub-agent). Repeat until the next **milestone** or all features pass.

**Milestone check-in**: At important points (e.g. end of a logical work-unit group, or when the design doc defines a milestone), **pause** the coding loop. Check in with the human: summarise progress, show what’s done and what’s next. The human may revise the plan, adjust the current implementation, or change priorities. When the human is satisfied, **re-run the Initializer** (to refresh backlog and progress from any plan changes), then **resume the Coding agent loop** until the next milestone or completion.

## Artifact layout

All harness artifacts live under **`_working/`** (scratch space for the agent; see workspace rules).

| Location | Purpose | Who updates |
|----------|---------|-------------|
| **`_working/design.md`** | Scope, acceptance criteria, tech stack; input to feature list and Initializer. | Human + AI (Phase 0). |
| **`_working/agent-progress.md`** | Current state, last session summary, next target, session history. | Coding agent at end of each session. |
| **`_working/agent-runbook.md`** | How to start app, lint/typecheck, run tests; **how to verify** (e.g. unit, E2E, browser automation—exact commands and steps). | Initializer; human when tooling changes. |
| **`_working/implementation-backlog.md`** | Ordered work units (one per session); route, acceptance criteria, dependencies. Defines milestones (e.g. end of a group). | Initializer from design/context. |
| **`_working/feature_list.yaml`** | Acceptance criteria in **YAML**; each item has `passes: true/false`. | Initializer creates and maintains; Coding agent sets `passes: true` only after verification per runbook. |
| **`_working/init_<app>.sh`** (optional) | One-command start (e.g. install deps, start servers). | Initializer or human. |

Detailed templates and full prompt bodies live in [references/REFERENCE.md](references/REFERENCE.md).

## Rules to enforce in prompts

- **Incremental**: One work unit per Coding session. If a unit is large, split across sessions and set "continue [unit X]" as next target.
- **Clean state**: Each session ends with a commit and a progress update. No partial broken scaffolding.
- **Feature list discipline**: Never remove or reorder items. Never set `passes: true` without running the corresponding verification.
- **Runbook as source of truth**: Coding agent must use runbook commands for verify; do not guess or invent commands.

## Feature list format (YAML example)

```yaml
acceptance_tests:
  - description: log in as admin redirects to app (root / dashboard)
    category: auth
    passes: false
    steps:
      - Start a new browser session
      - Navigate to the login page
      - Log in as the admin user
      - Verify redirect to /
  - description: invalid resource id shows 404 or clear error
    category: edge-case
    passes: false
    steps: [...]
```

The feature list is **YAML only**; when updating `passes`, preserve the rest of the file structure.

## Reference

- Directory layout, artifact templates, and prompt bodies for sub-agents: [references/REFERENCE.md](references/REFERENCE.md).
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
