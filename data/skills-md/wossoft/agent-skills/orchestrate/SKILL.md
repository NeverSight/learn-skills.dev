---
name: orchestrate
description: >
  Act as the orchestrator when the main agent (Claude Code, Codex, Grok, or another
  host) faces non-trivial work: decide what to do itself and what to dispatch to
  other CLI agents (Codex, Claude, cc-api, Grok, Antigravity) by role and difficulty,
  run them through agent-run, and verify results before integrating. Use for
  implementation, refactoring, diagnosis, research, or bulk chores; the default is
  to dispatch and spread work across workers rather than implement on the host.
  Also use whenever the user asks to delegate, parallelize, or get a second
  opinion. Skip for one- or two-line edits and pure Q&A.
---

# Orchestrate

The current main agent is the orchestrator. It owns scope, architecture decisions,
integration, final verification, and the report. Workers are disposable: each run is
a fresh conversation that sees only the task file.

## Roles

The orchestrator plans, decides, reviews, and integrates; workers implement. Default
to dispatch: the question is not "should I hand this off?" but "which worker gets
it?". The orchestrator keeps only:

- Scoping, decomposition, architecture decisions, and the interface contracts it
  writes into task files.
- Review, integration, final checks, and the report.
- Edits faster to make than to describe: one file, roughly 20 changed lines or
  fewer, intent fully clear.
- Work that depends on conversation context that cannot be written into a task
  file, and fixes after two failed revisions.

Everything else goes to a worker, including core logic, UI, and docs. The
orchestrator owns their design and acceptance, not their typing. Before editing
code yourself, check the list above; if the edit is not on it, write a task file.

Route by strength (tiers and user overrides in
[references/routing.md](references/routing.md)):

| Worker | Give it |
| --- | --- |
| `codex` | Medium and complex reasoning-heavy code at the default `complex` tier: backend, APIs, databases, migrations, core business logic, complex refactors, root-cause diagnosis, tests that protect business rules. `--tier hard` is the second brain: a read-only second opinion, architecture cross-check, or plan review (`--mode plan`), not an implementer. |
| `cc-api` | Medium-complexity Claude-style work on a separate quota at the default `complex` tier: frontend and UI components, docs, README, reports, skills and prompts, copy, scoped implementation. Do not give it hard tasks or pass `--tier hard`. |
| `grok` | Medium-complexity implementation at the default `complex` tier, plus fast work with live web and X context: bulk mechanical edits, renames, wiring, fixtures, i18n strings, config housekeeping, dependency and version checks and bumps, small scripts (`--tier simple`), current package or API facts, summaries of logs and files. Also a parallel read-only reviewer. |
| `agy` | Web research, visual/design review, document and media conversion. |
| `claude` | Frontend or docs when the orchestrator is not Claude. |

Spread the load:

- Do not funnel everything to Codex. Give Codex the complex, reasoning-heavy part
  and send the medium, mechanical, UI, and docs parts of the same task to `grok`
  and `cc-api` in parallel, each with distinct file ownership and the shared contract in its task
  file. Example: a feature becomes `codex` backend + `cc-api` frontend + `grok`
  wiring, fixtures, and strings.
- When the preferred worker is already busy and the task fits another, give it to
  an idle worker instead of queueing.
- For hard diagnosis or review, run two read-only workers in parallel (for example
  `codex --tier hard` and `grok`, both `--mode plan`) and compare their findings.
- Chore task files can be a few lines. Template overhead is not a reason to take
  work back.

Rules that apply to every host:

- Do not dispatch to your own product at the same tier just to offload work.
  Dispatching to yourself at a different tier (for example Codex host asking
  `codex --tier hard` for a second opinion) is fine. `cc-api` runs a separate
  config and quota, so a Claude host should use it for UI and docs; it is not
  self-dispatch.
- Dispatch without asking when the task falls in a role above. Dispatch independent
  subtasks in the same turn.
- If a worker CLI is unavailable or failing, fall back to another worker that fits,
  then to yourself. Do not install tools or change credentials to satisfy routing.
- Workers never re-delegate. agent-run refuses nested calls.

## Dispatch

Use this skill's `scripts/agent-run` (normally linked as `~/.local/bin/agent-run`;
`agent-run --help` for options).

1. Write the prompt to a file. Start from `agent-run template` (the same content as
   [references/task-template.md](references/task-template.md)). State goal, allowed
   files, contracts, relevant repository rules the worker may not load, prohibitions,
   and acceptance criteria. agent-run appends the worker contract and the report
   format (changed files / done / not done / uncertain).
2. Pick mode and tier:
   - Writable tasks use the default `--mode build`: an isolated worktree at HEAD with
     permission prompts skipped. It does not see uncommitted changes; if the task
     depends on them, describe them in the prompt or run serially with `--in-place`
     (permission controls stay on). Never commit or stash user changes to make a
     worktree run possible.
   - Read-only tasks (diagnosis, review, research) use `--mode plan` in the original
     checkout.
   - Choose `--tier` by difficulty: `complex` (default) for medium and complex
     work, `simple` for easy chores, `cu` for computer use, `hard` only for the
     `codex` second brain. Do not default to the highest tier.
   - Add `--check "<command>"` with the project-appropriate check for the change.
3. Run:

   ```bash
   agent-run codex api-pagination /path/to/prompt.md --repo /path/to/repo \
     --tier complex --check "dotnet build src/Api"
   ```

   For long runs use the host's background execution and watch
   `~/.agent-runs/<repo>/<task>/events.jsonl`; intervene on errors or long silence.
   `agent-run ls` lists runs. Exit codes: 0 done, 1 failed, 124 timeout, 2 bad args.

## Accept and integrate

Follow [references/review.md](references/review.md). Judge from `changes.txt`,
`patch.diff`, `check.log`, and the files themselves, never from the worker's own
summary. Exit 0 only means the process finished.

- PASS: apply the patch to the main checkout, preserving user changes, run the
  relevant checks there, then remove the worktree and branch.
- REVISION: a new run with the full original task, focused fixes, and prior artifact
  paths. After two failed attempts, stop redispatching; diagnose or implement on the
  host.
- Do not commit, push, or publish unless the user asked.

Report the outcome, the checks actually run, unverified runtime/browser/device
behavior, remaining risks, and which parts each agent did. If the orchestrator
wrote substantial code itself, say why it was not dispatched.
