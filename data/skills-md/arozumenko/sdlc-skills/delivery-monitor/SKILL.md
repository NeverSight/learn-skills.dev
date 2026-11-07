---
name: delivery-monitor
description: Delivery monitor for harness work items — the cycle-time and cadence sibling of tokenomics. Registers a plan (campaign → mission → task) with ranged, human-accepted estimates, records dispatch/merge/cancel transitions into a git-committed event ledger (.agents/telemetry/delivery/), backfills history from git, and reports cycle time, weekly throughput/velocity and estimate-vs-actual delta per level. Use when the user asks "how fast are we delivering", "register the plan / estimates", "record that TASK-023 merged", "delivery report / status", "enable delivery tracking", or "how good were our estimates". For cost per case use tokenomics; for sizing new work use automation-scoping.
license: Apache-2.0
compatibility: "Requires Node 18+ and git. Automatic dispatch capture on Claude Code only (SubagentStop hook, opt-in via scripts/install-hooks.mjs); every other host records transitions with the CLI and the git backfill."
metadata:
  authors:
    - Daniel Sallai <daniel_sallai@epam.com>
  version: "0.4.0"
---

# delivery-monitor — cycle time, cadence, estimate vs actual

`tokenomics` answers *what did it cost*; this skill answers *how long did it
take and how did that compare with what we said*. It never estimates, never
defaults a missing number, and labels every proxy as a proxy.

## Quick start

```bash
# 1. Register the plan BEFORE the first dispatch (the tech-lead's plan file carries a ```json delivery-plan block). Inside Claude
#    Code this also binds the calling session (subagents included) to the run — prints `SESSION claude:<id> -> <run>`.
node .claude/skills/delivery-monitor/scripts/delivery.mjs plan register --from docs/superpowers/plans/<plan>.md --id reg-1
# 2. The orchestrating session must be bound before it dispatches: the hook records dispatches only for a bound session (or one
#    whose branch maps to exactly one item of exactly one open run). A session that did not register the plan binds itself:
node .claude/skills/delivery-monitor/scripts/delivery.mjs session set sec/run-1     # host/session default to CLAUDE_CODE_SESSION_ID
#    Record transitions as they happen. A hook dispatch credited to the wrong item is withdrawn, then re-recorded:
node .claude/skills/delivery-monitor/scripts/delivery.mjs retract --agent <agent id> --plan sec/run-1 [--dry-run]   # or --observation <id>
node .claude/skills/delivery-monitor/scripts/delivery.mjs event TASK-023 done --sha <merge-sha> --id done-023
node .claude/skills/delivery-monitor/scripts/delivery.mjs event G12 done --sha <landing-sha> --id land-g12    # mission landing
node .claude/skills/delivery-monitor/scripts/delivery.mjs event INFRA-2 done --id done-infra-2    # landed no commit (infra, QA run, gate): no --sha, stamped now
# 3. Fill in history that predates the ledger
node .claude/skills/delivery-monitor/scripts/delivery.mjs backfill --git --plan sec/run-1 --head <sha>
#    GitHub-merged work (squash/merge-commit PRs, task PRs into a mission branch): read merged PRs via gh, or offline from JSON
node .claude/skills/delivery-monitor/scripts/delivery.mjs backfill --pr --plan sec/run-1 [--from-json prs.json] [--since <iso>] [--dry-run]
# 4. Optional: automatic dispatch start/end on Claude Code (+ shared telemetry submodule)
node .claude/skills/delivery-monitor/scripts/install-hooks.mjs            # --remove undoes, --doctor checks
# 5. Read
node .claude/skills/delivery-monitor/scripts/delivery.mjs status
node .claude/skills/delivery-monitor/scripts/delivery.mjs report [--json] [--html] [--from-json <f>] [--since 2026-09-01] [--level task] [--class M]
node .claude/skills/delivery-monitor/scripts/delivery.mjs report --html --out delivery.html
```

**Lifecycle rules.** Dispatch starts cannot be recovered after the fact: a plan registered (or a session bound) after the work
ran has no cycle time for it — backfill gives created/first-commit/done only. At campaign close, after the last landing, run
`delivery.mjs plan close <run>`; an open plan keeps admitting hook dispatches and makes every unpinned command ambiguous.
`status`/`report` say so when every item of an open plan is done or cancelled. `install-hooks.mjs --doctor` prints
`this session: … unbound` when the session you are in will record nothing.

**One task per subagent.** The hook attributes a subagent to the task named in its first brief. An agent that is messaged its
next task keeps billing that task's time to the first one; the hook flags it as a `task-crossing` diagnostic and does not
re-attribute it. The report's `agents:` line (`coverage.dispatch_agents`) shows how many agents were resumed or compacted and the
share of their turns above 500k context.

Plans may carry `branch_prefix` and `branch_map` (`[{pattern, ref}]`, regex with named groups → ref template, e.g.
`{"pattern": "-m(?<m>\\d+)-t(?<t>\\d+)$", "ref": "T{m}.{t}"}`) so branches like `feat/x-m1-t4` map to items without per-task aliases
(`references/plan-block.md`). Use **one** backfill mode per run: `--git` and `--pr` stamp the same merge with different clocks.

Contracts: `references/event-model.md`, `references/plan-block.md`, `references/metrics.md`, `references/spike-1.md`.
Design (in the sdlc-skills repo): `docs/superpowers/specs/2026-09-16-delivery-metrics-design.md`.
