---
name: herdr-agent-team
description: Run a multi-agent delivery team with enforced staffing, scope locks and verification gates. Use when coordinating several AI agents on one codebase — sizing the smallest team for a task, freezing a verified diff before a commit, keeping a writer's work independent from its verifier, or auditing why a change shipped. Ships a workflow-shape resolver, a durable task board, role contracts and the delivery protocol. Tuned for the Herdr app; the policy and scripts run with any agent runtime.
---

# Herdr agent team

A delivery discipline for agent teams working on real repositories. The point is
not more agents: it is that staffing, scope, and the commit gate are decided by
rules instead of by whoever is holding the conversation.

Everything here runs without a multiplexer. Herdr is the recommended runtime —
it gives you one space per project and child terminals under each controller —
but the policy, the resolver, and the task board work with any runtime that can
spawn a process and send a message.

## The four rules

1. **Smallest shape first.** Resolve a shape from the intake; raising it once
   needs a written reason, and a second raise is the Human's decision. A bigger
   team is never justified by model tier alone.
2. **Independent verification.** The agent that wrote the change must not be the
   agent that verifies it, and not on the same model. When routing collides,
   substitute an alternate, raise the tier, or report `partial`/`blocked`.
3. **Isolation for concurrency.** More than one independent workstream means
   separate git worktrees and one supervised controller. Two writers must never
   share a working tree.
4. **The intake is the staffing gate.** One intake file per task; every spawn
   passes the same file, and the launcher refuses any role the resolved shape
   does not include. Over-staffing becomes a refused launch, not a judgement
   call.

## Flow

| Step | Owner | Output |
|---|---|---|
| 1. Describe the task | PM | one intake file (JSON): task class, behavior change, risk, workstreams |
| 2. Resolve | `workflow-shape` | shape, staff, verifiers, tier, and why larger shapes were rejected |
| 3. Lock scope | PM | `Allowed files`, `Required behavior`, `Forbidden scope`, work branch |
| 4. Execute | worker | edits inside the allowed files only |
| 5. Freeze | worker | the staged diff frozen as a SHA-256 plus a readable artifact |
| 6. Verify | verifier(s) | PASS on that exact hash, with a revision budget of two |
| 7. Commit | worker, after the Human token | one commit whose diff is compared mechanically to the verified hash |
| 8. Deliver | worker or controller | push and PR only on exact Human authorization |

"Intake" here means only that task-description file — the resolver's input. No
tracker, issue sync, or external service is involved; wire one up yourself and
keep this same file as the contract.

The freeze-verify-commit step is the reason this exists: a commit is allowed
only for a diff hash that an independent verifier already passed, and any change
to the index invalidates every prior verdict.

## Quick start

```bash
# 1. Resolve the shape for this task (pure function: intake + team.json)
scripts/workflow-shape --intake examples/intake.json --team examples/team.json --format text

# 2. Read the catalogue when you need the full table
scripts/workflow-shape --list
scripts/workflow-shape --explain W4-fix-test

# 3. Record the task so the state is durable and auditable
export TASK_BOARD_ENV=1 TASK_AGENT_ROLE=pm
scripts/task-board create demo_task demo-1 --state planned --owner pm --controller pm
scripts/task-board transition demo_task demo-1 --to in_progress
scripts/task-board event demo_task demo-1 VERIFIER_ASSIGNED --payload '{"role":"tester"}'
scripts/task-board show demo_task demo-1
```

Copy `examples/team.json` into your project, edit the roles/models you actually
have, and pass `--team` (or set `TASK_TEAM_FILE`). The resolver is a pure
function: it never spawns anything and never writes files.

## Shapes

| Shape | Task | Opens |
|---|---|---|
| `W0-answer` | advisory, no repository write | nobody |
| `W1-doc` | documentation only | documenter |
| `W2-micro` | deterministic micro diff, no behavior change | coder (task-board proof replaces a verifier) |
| `W3-fix` | known-cause fix, acceptance not runnable | coder → reviewer |
| `W4-fix-test` | known-cause fix, runnable acceptance | coder → tester |
| `W5-refactor` | structural cleanup, no behavior change | refactor → reviewer |
| `W6-fix-refactor` | a fix whose root cause is structural | coder + refactor → reviewer + tester |
| `W7-feature` | new behavior, spec before code | sa + coder → reviewer + tester |
| `W8-investigate` | cause unknown | investigator |
| `W9-ops` | operational change, no source behavior change | coder → reviewer |
| `W10-deliver` | commit/push/PR of an already verified increment | nobody |

Full definitions, input fields, and the scoring rubric: `references/workflow-shapes.md`.

## Roles

Twelve role contracts live in `references/roles/`. They are written as identity
and policy, not as transport: replace "session" with your runtime's unit of an
agent process.

| Layer | Roles |
|---|---|
| bootstrap | `orchestrator` |
| project owner | `pm` |
| optional controller | `supervisor` |
| planner | `sa`, `investigator`, `researcher`, `designer` |
| worker | `coder`, `refactor` |
| verifier | `reviewer`, `tester` |
| document | `documenter` |

The organisation is deliberately flat: the orchestrator bootstraps a project and
hands off; the PM is the project's chief of staff and owns scope, staffing,
gates and reporting; specialists execute and are leaves. Keep exactly one PM per
project — a second one splits the Human conversation and fights over the same
work.

### Placement

| Room | Who gets it |
|---|---|
| one space per project | every role of that project, and nothing else |
| a tab | orchestrator and PM — the two the Human talks in |
| a child terminal of its controller | every role below PM |

A child is `hc run --bg --parent <controller>` and inherits the controller's
working context; it ends when the controller ends. Start one with
`--outlive-parent` only when the work is deliberately meant to survive its
controller, and say why in the plan.

Rules that follow from the placement:

- **The controller closes what it opened.** PM closes its children when the task
  ends — reports collected, verification and commit gate reached, or `[STUCK]` —
  and a worker closes any child it opened before reporting.
- **Cleanup cascades.** Killing a controller ends its descendants, so nobody has
  to hunt grandchildren.
- **Depth is allowed, visibility is not.** Nesting works at any depth and
  `hc ls` shows the parent chain, but a sidebar renders one level; use `hc ls`
  when you need to know who belongs to whom.
- **Name by role and project** (`{role}-{project}` or
  `{role}-{project}-{workstream}`) so a terminal is identifiable without reading
  its transcript.

## Runtimes

Nothing here is tied to one CLI. A machine may have `pi`, `hermes`, `codex`,
`claude`, `opencode`, or `kiro-cli` — or only one of them — and the team still
works because a runtime is judged by verbs, not by name:

```bash
./scripts/runtime-probe          # what this machine has, and what each CLI can do
./scripts/roster coder critical  # role + tier -> runtime, model, selection, source
```

`references/runtime-adapters.md` records the six verbs (`launch`, `ask`, `send`,
`resume`, `model`, `permissions`), the verified invocation for each CLI, and the
degraded mode when a verb is missing. `roster` never invents a model: a pair that
is uninstalled, disabled, or off the allowlist is refused, and an empty result is
`[STUCK]` rather than a substitution. Neither script installs a CLI, logs in, or
reads a credential. `bash tests/runtime.test.sh` exercises both against fake
runtime binaries, offline.

## Communication

`references/communication-protocol.md` is the full contract: envelope, ACK /
STATUS / DONE / STUCK, file-first handoffs, dispatch accounting, the verification
loop, and the commit-review and remote-delivery gates. Two rules carry most of
the weight:

- every assignment names its reply target, and a completion is only ever pushed
  to the controller — never announced to your own session;
- a verifier sends exactly one verdict, bound to the diff hash it checked.

Delivery is Herdr's job. In the Herdr app (herdr-core) a message is
`hc send <terminal> "<text>"`; with the terminal CLI it is
`herdr agent prompt <agent> "<text>"`, falling back to `herdr pane run` plus
`herdr pane send-keys <pane> enter`. Children are `hc run --bg --parent`, while
spaces, tabs, and splits belong to `herdr-app do …`. Serialize per target,
file-first above ten lines, and never wait or poll — `hc wait`, `herdr agent wait`,
`herdr agent prompt --wait`, and `herdr pane wait-output` are blocking commands
this policy forbids, and reading a terminal is diagnostic only.

## What is not included

- Spawning and pane layout. The launcher starts roles and owns the topology;
  delivery into a running agent is Herdr's (`herdr agent prompt`), and the exact
  commands and prohibitions are in the protocol.
- Launching. `scripts/roster` resolves role and tier to one runtime/model pair
  from `examples/team.json`'s schema (`model_selection`, ordered allowlists,
  per-tier `primary`/`alternates`), and `scripts/runtime-probe` reports what the
  machine has — but the spawn command, panes, and enforcement of the result stay
  with your launcher.
- Trackers and issue sync. Intake is a file here; wire it to whatever tracker you
  use and keep the same shape.

## Pitfalls

- **The tier comes from the intake.** If a caller passes a tier that disagrees
  with the resolved shape, the resolver and the launcher should refuse rather
  than silently pick one.
- **Hash drift is a real failure.** Staging one extra file after a verifier
  passed invalidates the verdict. Re-freeze and re-verify; never amend.
- **Revision budget is two.** After that, accept what has no blocker or report
  `[STUCK]`. "One more round" is how a team burns a day.
- **A document task is not an implementation.** It does not need a coder, and
  normally needs no verifier at all.
- **A verifier reviews the diff against the gate, not the repository.** The
  `Acceptance Gate` with stable criterion IDs is the whole mandate; an assignment
  without it gets one `[STUCK] missing: acceptance gate`, not a self-invented
  standard. The `Verification Scope` block bounds the same work to the files the
  diff actually changed. Findings outside that boundary are `ADVISORY` and never
  produce `[CHANGES_REQUIRED]`. If a review is slow or is demanding a rewrite,
  check the brief's criteria and scope block before blaming the reviewer.
  Copy the shape from `examples/verifier-assignment.md`.
