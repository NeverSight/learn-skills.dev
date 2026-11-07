---
name: factory
disable-model-invocation: true
description: "Shows where a spec (PRD), ticket, or PR stands in the factory workflow and names the one skill that moves it on. Read-only unless the user starts /factory run. Never closes issues or passes staging."
metadata:
  version: "6.1.0"
---

# factory

Derive state and next skill from tracker, PR, check, review and deploy evidence. Reports are stateless; runs preserve execution checkpoints.

## Inputs

- **Mode** — `report` (default) or `run`, from the first argument. Enter `run` only when the user's own request says it; a status question never does.
- **Reference** — one of: a spec (PRD) issue (`PRWL-100`, a GitHub issue URL or number), a ticket, a PR number or URL, or the word `start` for an idea with no spec yet. `run` also takes a label name (`/factory run automate`): every open issue carrying it. Missing → ask; never guess from the current branch. Optional `reviewer=<harness>/<provider>/<model>` overrides the default reviewer for this run.
- **Tracker of record** — Linear (via Linear MCP) or GitHub (via `gh`), read from the workspace `AGENTS.md`. Unclear → ask.
- **Staging branch** — default `staging`; confirm with `git ls-remote --heads origin <branch>` before any state that depends on it.

## Rules

- **Report mode is read only.** It reads the tracker, `gh`, and git. It writes nothing remote and edits no file; every state change belongs to the skill it names.
- **Report mode suggests, never auto-chains.** Name the next skill with the exact invocation, then stop. The user runs it. Only `run` mode, started by the user, carries a suggestion out.
- **Gates need evidence, not status words.** A gate passes only on the observable signal in [`references/states.md`](references/states.md): required CI evidence for head (or authoritative no-applicable-CI policy with mandatory local proof), head-bound QA/risk evidence, and deploy-watch proof for the merge commit. A label, a chat claim, or "CI is fine" does not pass a gate.
- **Head SHA binds everything.** Review, QA, and risk evidence counts only for the PR's current `headRefOid`; an approval counts only when its review's `commit.oid` is head. A new push sends the PR back to CI.
- **Staging is the ceiling.** `READY_FOR_OWNER` is terminal. Never suggest production deploys, production PRs/merges, or flag rollouts. Default branches are owner-only except explicitly authorized, non-production delivery `local`; name the owner otherwise.
- **Unreadable signals stop.** A signal the table needs can't be read (tracker access denied, no deploy workflow found) → report `UNKNOWN` with what is missing. Never guess the more advanced state. A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error.
- **Zero attribution.** No co-author, AI, or tool attribution in any output, except **Reviewer provenance** in `references/records.md`.
- At phase transitions use the portable status and waiting contract in [`references/session-handoff.md`](references/session-handoff.md).

## Workflow

### 1. Resolve the unit of work

From the reference, build the list of units to place: a spec expands to all its sub-issues, open and closed (state the count); a ticket or PR is one unit. For each ticket, find its PR: `gh pr list --search "<issue-id>" --state all --json number,headRefName,baseRefName,state` or the tracker's linked-PR field. Closed and merged tickets stay in the list — they may still be in `STAGING`. A `qa-escape` marker other than `not-deployed` places its ticket by the newest later PR.

### 2. Read the signals

Per unit, read only what the state table needs. Before interpreting checks, apply [`references/ci-policy.md`](references/ci-policy.md); it distinguishes known no-CI policy from pending, failed, absent required checks and unreadable policy:

```bash
gh pr view <pr> --json state,isDraft,baseRefName,headRefOid,mergeCommit,mergedAt,reviewDecision,reviews,statusCheckRollup,autoMergeRequest,body,comments,commits
gh pr diff <pr> --name-only
gh run list --workflow <deploy-workflow> --branch <staging-branch> --json headSha,status,conclusion,url
gh issue view <issue> --json state,comments
```

Read unresolved review threads with a paginated GraphQL `reviewThreads` query; unreadable thread state is `UNKNOWN` before a merge.

Read QA/risk/deploy evidence on the PR and issue records through [`references/records.md`](references/records.md). Linear comments use readable headings and fields; legacy records remain readable. Newest valid evidence for the required revision wins. The `Acceptance criteria` verdict clearing `BUILDING` must name head: read the body, otherwise the newest `## QA handoff` whose `Change:` SHA is head. Old-head acceptance does not count.

### 3. Place each unit

Match the signals against the table in [`references/states.md`](references/states.md), top row first — the first row whose condition holds is the state. States in order: `OUTCOME`, `TICKETS`, `QA_RETURNED`, `BUILDING`, `CI_STUCK`, `CI`, `QA_STUCK`, `CHANGES`, `QA`, `REVIEW`, `HUMAN_REVIEW`, `MERGE`, `READY_FOR_OWNER`, `DEPLOY_FAILED`, `STAGING`, plus `UNKNOWN`.

### 4. Check the gate and pick one next skill

For each unit, state the gate out of its current state and whether its evidence is present. Pick exactly one next skill per unit from the table's `next` column. When that skill runs or changes code, name the worktree it will use — `<project-repo>/.worktrees/pr-<n>` for a PR, `.worktrees/qa-escape-<issue>` for an escape. For a spec with several units, order the suggestions so a blocked unit (`QA_RETURNED`, `DEPLOY_FAILED`, `CI_STUCK`, `QA_STUCK`, `CHANGES`, `UNKNOWN`) comes before progress on healthy ones; healthy units follow oldest `Since` first, and a unit in one state for more than 3 days is flagged `stalled`. Units that share a gate and skill collapse into one suggestion.

### 5. Report and stop

Print the output below. Report mode ends here: do not run the suggested skill, even when the user is away; the next move is theirs.

## Run mode

The user's `/factory run <reference>` approves the whole chain. Read [`references/run.md`](references/run.md) first; its **Stage map** names the late-stage files ([`references/review-and-delivery.md`](references/review-and-delivery.md), [`references/returned-by-qa.md`](references/returned-by-qa.md)) to read when a unit first reaches those states.

Read [brief](references/builder-brief.md) before dispatch; [receipts](references/supervisor-receipts.md) when continuing; [drafts](references/delivery-drafts.md) during QA.

1. **Intake.** Resolve units as in step 1 and apply **Triage** before builder/runtime work. A fully specified ticket may receive its narrow eligibility transition under run authority; ambiguous work parks. Post missing criteria only to restate existing outcomes. Apply **Start** for builder and reviewer selection.

   Unresolved execution setup → stop with its handoff. Preserve choices on resume. Only the exhausted review-route recovery in **Start** asks a new execution question.
2. **Loop.** Wait for active children and continue automatically; a worker turn ending is not a factory stop. Follow **Dependency-aware scheduling**: isolated independent units may overlap within capacity; the parent serializes integration. For each ready unit: place it (steps 2–4), carry out its `Next` per **Stage map**, and place it again; log it and apply **Lessons**. Per unit: status In Progress, its own worktree and **Task stack**, a builder worker on the selected backend, agentic QA in a QA worker, a PR, CI, the **Review loop** between the reviewer and the builder, risk review, **Merge**, **Handover** with status In Review, **Cleanup**, **Promotion**, **Staging**. For setup or local-runtime blockers, read [`references/readiness-and-recovery.md`](references/readiness-and-recovery.md); **Loading a stage skill** governs recovery and stops.
3. **Parks.** Park units awaiting a person — high risk review, a spent cap, reporter-only facts — with evidence; continue the run. No tracked compose file or issue body is edited; no issue is closed.
4. **Run report.** When no automatic work remains, print the output table, parked units' [standard handoffs](references/session-handoff.md), drafted criteria, **Production readiness**, and **Lessons**.

## Output

```
Factory — <reference>  (<n> units)

| Unit | PR | State | Since | Gate evidence | Next |
| ---- | -- | ----- | ----- | ------------- | ---- |
| #418 | #87 | CI | 2026-10-02 14:10 | run 9912 failed on a1b2c3d (unit-tests) | /ci-loop 87 |
| #419 | #88 | HUMAN_REVIEW | 2026-09-28 09:02 (stalled) | risk-review tier=high on 4e5f6a7 (migration) | engineer review — no skill |
| #420 | #85 | READY_FOR_OWNER | 2026-10-01 17:45 | deploy run 9890 success on merge 7c8d9e0, smoke passed | owner promotes — factory ends |

Escapes: 2 qa-escape on this spec — 1 after agentic-qa verified (honesty gap: #418 missed-empty-state)
Next: /ci-loop 87
```

At most one table row per unit; `Gate evidence` names the run, SHA, or comment — never a bare "pass". `Since` is the timestamp of the signal that placed the unit (head push, marker, run), read this run. The closing `Next:` line carries the single most urgent suggestion. When a unit is `UNKNOWN`, its row says which signal is missing. The `Escapes:` line counts the spec's reproduced `qa-escape` markers, excluding class `not-a-regression`, and how many name a PR (`pr=`) whose final head carried a `verified` agentic-qa marker — that count is the honesty gap; name each one.

## Completion criteria

- [ ] Every unit in the spec appears in the table, and the printed unit count matches the total sub-issue count, open and closed, read from the tracker
- [ ] Every `Gate evidence` cell names a run ID, SHA, or comment marker that was actually read this run
- [ ] Report mode: `git status` and the PRs show no change made by this run, and no next skill was invoked
- [ ] Run mode: readiness/repair evidence names checkout/runtime, causes, changed conditions, and rechecks within all caps
- [ ] Run mode: every unit ends merged with its delivery record read back, or parked with a named reason; cleanup read-back shows no task runtime resource or `/tmp/<task-id>/` left, or names each one; no issue was closed and no tracked Compose file changed
