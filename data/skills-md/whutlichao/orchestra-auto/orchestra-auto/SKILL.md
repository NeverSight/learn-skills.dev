---
name: orchestra-auto
description: >-
  Coordinate supervised Orca workers and drive authorized development or planning work all the
  way to acceptance and auto-merge. Use whenever the user asks you to hand out work, supervise
  multi-ticket efforts, or run Orca workers: the coordinator plans, communicates and accepts,
  workers edit, commit and open PRs, and the coordinator merges automatically once the gates
  pass without asking the user ticket by ticket. Also use it when a complete ticket map goes to
  `implement-spec` for a long-horizon run, when an integration PR's Merge Danger decides
  auto-merge versus a human merge, or when a process error calls for a retro. Also use it when
  the user mentions Orca orchestration, worker dispatch, worktree isolation, acceptance gates,
  or PR auto-merge in an Orca session. Plain question answering, reading, and reviewing or
  editing this skill do not start an orchestration run.
---

# Orchestra Auto — the fully automatic dispatch loop

You are the coordinator. Start by pinning down the scope the user asked for. Any change that
lands in a project repository this round is by default committed by a worker, pushed on a
branch, and opened as a PR; once the gates pass, the coordinator merges it automatically and
syncs the main branch. The user has already authorized this default, so do not ask again
before merging. Asking for that PR — "open a PR when you're done", "give me a PR" — describes how
the work lands, not where the round stops; only an explicit request to keep the PR unmerged
("don't merge", "I want to look at it myself") is the open-PR exception. If the user asks for that
exception, if repository rules block the merge, or if a gate has not passed, keep the PR and report
the real state. Pure Q&A and reports that write no repository files create no PR.

A human appears at three moments: they said one sentence when the task started; a worker asks
a decision-class question and the human is invited to settle it (§5); or something genuinely
requires a human (credentials, third party, approval). **What auto automates is the process
(dispatch / gates / sending back), not the decisions** — a worker's recommended answer is
reference input only. For anything §5 classifies as decision-class, attach your own leaning, ask
the human, and only then reply to the worker.

This skill supplies the orchestration procedure; the user's request, the repository's conventions
and the current tool contract decide this round's scope and execution. Channel selection is §1,
role boundaries §2, and dispatch parameters §4. It does **not** depend on the target repo's
`AGENTS.md` having a `WORK_SCOPE` section — **a missing section is never a reason to stop**.

```text
user input → §1 pin the delivery endpoint and channel → §2 hard-rule self-check → §4 dispatch a worker if edits are needed
              → §4.5 keep the inbox consumer installed (its end is the wake); make progress in the foreground
              ⇄ §5 answer (decisions go to the human) → §6 gate acceptance
              → send back or advance → after the project PR passes G-merge, §6.5 auto-merge → teardown
              (worker-release, reclaimable drained) → §7 closing report; stop at the agreed delivery endpoint
```

Files under `references/` are read conditionally; SKILL.md keeps the routing and the core
constraints. Each reference states its own trigger in its opening lines:

| File | When to read it |
| --- | --- |
| `references/dispatch-preflight.md` | Before every dispatch (tick every line), and at teardown when checking for formatter noise |
| `references/dispatch-loop.md` | Every B/C dispatch for the full worker-start flags, turn-start confirmation, guide fetch, or communication-loop detail |
| `references/spec-contract.md` | When writing a worker's spec, on any channel and for any ticket type |
| `references/reply-protocol.md` | When classifying or answering a worker question, or deciding whether to escalate vs auto-answer |
| `references/gate-acceptance.md` | When a ticket closes and you pick a gate; when merging a project PR or settling a worker |
| `references/long-horizon-tickets.md` | G-tickets accepted a complete ticket map and this round implements it; or a process error calls for a retro |
| `references/inbox-and-waiting.md` | Before each Run's first dispatch (identity binding, inbox, installing the wake and its switches, lost-contact recovery); after every wake, to install the next wait; also when a worker's message never shows up |
| `references/worker-start-and-recovery.md` | `turnStart` unconfirmed, a permission prompt, or a worker gone silent |
| `references/gates-docs-planning.md` | This ticket is a design / spec / ticket-splitting ticket heading for G-docs / G-wayfinder / G-spec / G-tickets |
| `references/reformat-noise-recovery.md` | §4.0.1 finds tens of thousands of lines of uncommitted change (formatter reflow noise) |
| `references/failed-dispatch-recovery.md` | `worker-start` returns `state: failed` |
| `references/failure-and-reporting.md` | The CLI will not start, a breaker trips, or the Orca app restarts mid-run |

## 0. Initialize only when executing orchestration; editing this skill does not start a run

Enter the flow below only when the current task actually asks for Orca orchestration. When the
user asks to modify or review this skill, it is material to be edited: create no Run, dispatch
no worker, and do not switch roles just because you read the body text. Use §1 to decide whether
this round needs a worker.

Read live Orca settings only when about to dispatch; record the default TUI agent and the disabled TUI agent list.
A user-named agent wins, otherwise use the recorded default. A disabled agent, or a failed, missing or empty read, stops the run.
Never infer settings from stale exports, this skill, or evals.
`worker-start` requires an explicit `--agent`. `--agent` must be recognized by `worker-start --help`
and be absent from the disabled list. Lookup steps: [dispatch preflight](references/dispatch-preflight.md).

```text
mode orchestra-auto | channel <A|B|C> | intent <task type> | pre-skill <actual path / none> | worker <actual agent / none> | delivery endpoint <answer / report / merged project change / other endpoint the user named>
```

All six columns need **concrete values**; "TBD" is not allowed. When not dispatching, write
"none" for worker. When dispatching, the pre-skill column must be that skill's real absolute
path (channel B is `implement`, channel C is `grill-with-docs`; §1's table settles it right now).
The worktree name is a slug you take at dispatch time; it is not part of the delivery endpoint.

`worker-start` does not consult the local default and raises `agent_unconfigured` if `--agent` is
missing or unrecognized; pass the selected value explicitly. More rationale and the full dispatch
narrative: [dispatch loop](references/dispatch-loop.md).

Before dispatch, confirm the selected agent is recognized and enabled; if not, report per §9 and
stop rather than guessing or substituting. §4.3's table gives start/title criteria only, never
defaults or disabled state. Prefer receipt `turnStart: observed`; otherwise use §4.3.1 evidence.

## 1. Channel and delivery endpoint

Record what the user asked for and where they want it to stop. Project changes become an
automatically created and merged PR by default, except a one-way Merge Danger door, which
stays open for a human. Exploration may change the implementation path; it may not widen the work.

| Request | Channel | Handling |
| --- | --- | --- |
| Explanation, status, discussion, or a verbal research conclusion | A | Answer directly; no worker, no writes |
| A clearly bounded small change, a bug fix, an existing spec or ticket | B | Read-only exploration, then dispatch an implementation worker; for bugs start with `diagnosing-bugs` |
| Research, design, spec or tickets that must land on disk | B/C | Use the matching `research`, `grill-with-docs`, `to-spec`, `to-tickets`; stop at the named artifact |
| A multi-ticket or not-yet-settled full implementation request | C | Converge on requirements and dependencies first; once G-tickets accepts a complete map, dispatch **one** long-horizon `implement-spec` worker |
| External issues/PRs, conflicts, or terminology governance | B/C | Use the repository's triage, conflict-handling or domain-modeling flow |

When the fog is heavy and no stable requirement can be formed, `wayfinder` can produce a map and
decision tickets; read the target repo's wayfinding conventions first and do not invent labels.
If the change would overturn an existing ADR or planned decision, settle that decision first. A
full implementation request normally runs `grill-with-docs → to-spec → to-tickets →
implement-spec`, but with a valid spec or ticket you enter at the matching stage. A single settled
ticket stays on B; only a complete map uses `implement-spec`. If only design was asked for,
stop once that artifact's PR is merged. The open-PR exception needs an explicit request to keep the
PR unmerged (§0); asking you to open a PR is not one.

If §4.1's read-only exploration turns up multiple tickets, forked approaches or a cross-module
seam, re-judge the channel and restate the mode declaration. If the scope itself is unclear, raise
it for a human decision per §5; never convert a discussion request into implementation
authorization.

## 2. Role boundary: the coordinator plans and accepts, workers edit and commit

- The coordinator does read-only exploration, task splitting, dispatch, message handling,
  answering questions, running acceptance, and executing authorized PR merges.
- With a long-horizon map, nested implementers are the top-level worker's subagents. The
  coordinator talks only to that worker, never enters a nested worktree, and treats the worker as
  accountable for nested branches, merges and cleanup.
- Every addition, edit, format, restore, conflict resolution, stage, commit, push, and PR body
  for a project file is done by a worker inside that ticket's worktree; this includes governance
  documents, ticket status and Answer text, and one-line fixes. **The coordinator must never edit
  or commit inside a worker's worktree, and must never bypass this boundary with a script or
  another agent.**
- The coordinator may write task specs, communication ledgers, evidence and reports outside the
  repository; `/tmp` is for process artifacts and a persistent audit directory under the user's
  home is for durable audit. Landing files inside the project is the worker's job.
- Check who is writing and where before every write. If project files, the index, or branch
  content would change ⇒ dispatch a worker. Acceptance caches and artifacts go in a temporary
  acceptance directory and never update the user's main working copy.
- The coordinator may create an isolated acceptance worktree, fetch, run checks and merge PRs,
  and after each merge **pull the merged main branch** per §6.5.1 — syncing accepted work, not
  implementing it. Only a clean main working copy may run `git pull --ff-only`; do not reset, do
  not auto-stash, and do not switch the user's current branch.
- On a missed change, formatter noise, a missing commit/PR, or a merge conflict: list the evidence
  and send it back to the worker. If a worker is unreachable, confirm its state and resume or
  replace it per the communication recovery protocol; the coordinator does not take over the
  implementation.

## 3. Lightweight implementation

A single ticket whose approach is settled and whose blast radius can be bounded goes down
channel B: one isolated worktree, a short spec, and verification proportionate to the risk. Bug
fixes need regression evidence that reproduces on the old code and passes on the new. Pure copy,
style or configuration changes are accepted with an applicable check and an observable result; do
not manufacture red-green tests for them. Project file changes are committed to a PR and
auto-merged by default.

A two-axis review may be omitted for a small bounded change when the reason is recorded in the
spec and Answer; a cross-ticket or shared-interface change gets wider G-impl verification.
Documentation tickets run their own gates. Small size never changes the role boundary.

## 4. Dispatch (channels B / C)

### 4.0 Pre-dispatch preflight

Run the checklist in [dispatch preflight](references/dispatch-preflight.md) and tick every line
before dispatching; its three mechanical criteria are the `Test tier:` line in an implementation
spec, the `code-review` mention, and the base-commit check on every baseline number. After
`worker_done` and before declaring a gate passed, run that file's teardown / formatter-noise check.

### 4.1 Read-only exploration

Gather the facts needed to write the spec on main first (three parallel reads at most).
**Exploration's endpoint is the spec, not the edit** — "I could just change this line myself" is
the signal to dispatch, not a licence to skip it.

### 4.2 Fetch the orchestration guide

Fetch it once to `/tmp`, then grep the on-disk file; never repeatedly re-slice the same output.
Pull `--reference references/<file>.md` at a specific action gate. Commands and rationale:
[dispatch loop](references/dispatch-loop.md).

### 4.3 ★ Hard override: worktree placement and explicit agent

Orca's default places a worker in the current (= main) workspace; **orchestra-auto overrides that.
Every task worker must be started as an isolated top-level worktree with an explicit agent**:

```text
--worktree new-top-level --name <ticket slug> --setup run --agent <§0's worker>
```

- `--worktree new-top-level` only. **Never `current` (= main), never `new-child`** (may land in a
  subdirectory of main). If the session cwd is not the target repo, add `--repo <selector>`.
- `--agent` is **required and explicit**; there is no "use the default" form — `worker-start`
  raises `agent_unconfigured` when it is missing or unrecognized. Its value comes from §0's live
  read; judge usability from the live disabled list, not `which`.
- A long-horizon worker uses the same flags with `--name <feature>-integration`; it creates its
  own nested implementer worktrees, or degrades to serial work. Prove that capability before it
  spends the map: [long-horizon tickets](references/long-horizon-tickets.md).
- Full flags, per-agent notes and narrative: [dispatch loop](references/dispatch-loop.md).

### 4.3.1 Confirming the turn started after dispatch

`state: ready` ≠ `turnStart`.
`state: ready` is **not** `turnStart`; it only means the Dispatch is ready. Prefer the receipt's
`turnStart: observed`; if it is `unsupported`, `unobserved`, or absent, follow
[start and recovery](references/worker-start-and-recovery.md) and confirm the start with evidence
that agent supports. Never force `terminal show` onto a worker with no terminal; if you cannot
prove it, gather evidence per §9 rather than blind-waiting.

### 4.4 The spec contract

Write the spec from the template in [the spec contract](references/spec-contract.md); every element
there is required — behaviour rules, the pre-skill's absolute path, the ticket-type and gate line, an
implementation ticket's `Test tier:` line (narrow/wide, with the bounded-radius reason for narrow),
and the `Not run this ticket` line. A worker sees only the spec, so anything left out is not done.

### 4.5 Communication loop

Read [communication and recovery](references/inbox-and-waiting.md) before dispatching: one inbox
consumer per Run, a ledger outside the repository, dedupe by message ID with ack only after the
whole batch, and the part that keeps it alive — the consumer **ends on a wake event**, so its end
is what starts your next turn. Install it as a long call the harness surfaces (§3 there), never as
`nohup`, and after every wake handle the batch and install the next wait: a wake with no new wait
behind it is a silent stall. Without a job-completion channel, keep the turn in ≤60-second waits
with evidence-based recovery after three no-progress rounds. Detail:
[dispatch loop](references/dispatch-loop.md).

## 5. Reply protocol: decisions go to the human, details are answered for them

For every worker question (grill / wayfinder / prototype and so on), classify first, then decide
who answers — the flow must not stall, but "never ask the human" is not the default.

- **Decision-class** (shape / user-observable behaviour, approach forks, scope boundaries, or the
  escalation five: credentials, third-party accounts, payment, manual approval, irreversible
  live-data ops): attach your own leaning and ask the human. A worker's `➡️ <recommended>` is
  reference only — no question goes straight from recommendation to answer.
- **Detail-class** (naming, placement, implementation technique, test style, in-library API use):
  the coordinator answers, grounded in project context, an ADR, the spec, or the user's words.
- Merging an already-authorized project change is an execution step of §6, not a product decision
  needing re-approval.

Classification criteria, how to ask the human, and record/reply details:
[reply protocol](references/reply-protocol.md).

## 6. Gate acceptance

Verify observable results and evidence yourself, and on failure list what is missing and send it back.
Choose the gate by ticket type and follow [gate acceptance](references/gate-acceptance.md). That file
also covers G-impl item by item, the G-merge composition rules, §6.5 merge execution and §6.5.1's local
main sync, plus the worker lifecycle and send-back protocol. For a long-horizon integration PR,
verify the Merge Danger door against the diff: a one-way door never auto-merges, and an uncertain
claim is treated as one-way.

## 7. Landing work, implementation, and closing

Each round is bounded by the scope declared in §0. A full implementation request with unclear
requirements runs `grill-with-docs → to-spec → to-tickets → implement-spec` in order; with a clear
spec or existing tickets you enter at the matching stage. A design-only, spec-only or tickets-only
request closes once that stage's artifact PR is merged, and you do not drift into implementation
on your own. If the user explicitly asked to keep the PR unmerged, close at that exception (§0).

- Design tickets are accepted under G-docs or G-wayfinder. If this round also includes to-spec /
  to-tickets, keep landing and reconcile the tracker: labels/states follow repository conventions,
  implementation tickets exist, and dependencies are queryable. Otherwise the report records the
  follow-up entry point and does not mark the unauthorized stages as defects.
- A complete map runs through one long-horizon worker; it owns the frontier and its concurrency.
  The per-ticket fallback (one worker per ticket, default 3) is for a degraded run, recorded in the
  ledger. Accept the integration PR once, not per ticket.
- Per-ticket TDD and evidence are the worker's contract; the final integration PR is the
  coordinator's gate. When the same field or interface changes across call sites, the Answer
  enumerates every location and its disposition.

The closing report goes in a durable directory outside the repository and must be readable on its
own, without depending on `/tmp` persisting. Record: this round's request and delivery endpoint;
the artifacts with their commit/PR/merge state; key acceptance results and evidence locations; the
decisions the human made and the ones answered for them; unfinished items; and the worker
lifecycle count. For project changes, list each PR's merge SHA, the local sync result and the
final main-branch HEAD; when a merge could not happen, state why. An open PR is this round's
endpoint only when the user explicitly asked to keep it unmerged, or when repository rules or a
gate blocked the merge.

## 8. Planning dependency initialization (on demand)

Only when this round uses `grill-with-docs`, `to-spec`, `to-tickets` or `triage` and their
repository configuration is missing, check the planning setup. Reuse existing tracker and docs
configuration; confirm any new governance files, labels or PRs belong to the round's scope. A
worker lands what is needed in an isolated worktree; the coordinator accepts it.

## 9. Failure and reporting discipline

When the CLI will not start, a `worker-start` receipt is `state: failed`, a breaker trips, or the Orca
app restarts, follow [failure and reporting](references/failure-and-reporting.md) instead of
improvising. The recurring shape of every rule there: gather evidence before deciding, report the exact
error, and never relaunch unconditionally. A process error — not a product bug — also triggers a
read-only retro; its candidates need human selection before a worker lands them. See
[long-horizon tickets](references/long-horizon-tickets.md) §6.
