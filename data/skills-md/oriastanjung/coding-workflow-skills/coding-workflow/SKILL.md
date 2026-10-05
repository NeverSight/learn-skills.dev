---
name: coding-workflow
description: How the owner ships features — plan mode first (no plan, no start), then tickets, then one stacked PR per vertical slice via `gh stack`. A fresh subagent implements, a fresh reviewer subagent reviews every slice, a gate subagent runs lint, test, build and e2e, Main Agent merges and updates the ticket. Use for any implementation task larger than a one-line fix. Stress-test the plan with references/interrogating.md.
---

# Coding workflow

## Hard gate: a plan must exist

This skill starts only from an approved plan made in plan mode. If no plan
exists, stop. Tell the user to enter plan mode (`EnterPlanMode`), write the
plan, and get it approved. Do not implement anything without it, whatever the
request says.

The plan must be detailed enough that a junior engineer can implement it
without asking questions: vertical slices in order, files per slice, acceptance
criteria per slice, and the tests that prove each one.

While you write the plan, interrogate the user with `references/interrogating.md`
until every decision in it is settled. Do not use any other skill for this.

## Pipeline

Run the stages in order. Each stage has its own guide in `references/`.

| # | Stage | Guide |
|---|---|---|
| 0 | Plan exists, is interrogated and approved | this file, `references/interrogating.md` |
| 1 | Run `scripts/prerequisite.sh` | this file |
| 2 | Ask the two start questions | this file |
| 3 | Write or update the ticket | `references/write-or-update-ticket.md` |
| 4 | Implement and review the slice | `references/workflow.md`, `references/pr-review.md` |
| 5 | Open the stacked PR | `references/create-pr.md` |
| 6 | Merge, update the ticket, go to the next slice | `references/workflow.md` |

Repeat stages 4 to 6 slice by slice, one stacked PR at a time, until every
slice has passed every gate. Do not stop at a partial stack.

## Stage 1: prerequisites

```bash
bash ~/.claude/skills/coding-workflow/scripts/prerequisite.sh
```

If it fails, show the user the output and the fix it prints. Do not continue
until it passes.

## Stage 2: ask before starting

Ask both questions with `AskUserQuestion` before any work:

1. **Parallel or sequential subagents?**
   - Sequential: one subagent at a time. Recommended on the $20 plan, where
     parallel agents burn the usage limit fast.
   - Parallel: independent slices run at the same time. Recommended on Max or
     Max $200, where it gives a large speed-up.
2. **Does this work already have a ticket?** Offer the ticketing tools that
   are connected as MCP servers in this session (Linear, Jira, Trello, Slack,
   Obsidian, Plane, or any other). If none is connected, the fallback is
   GitHub Issues. Also ask which project the work belongs to.

## Stay on target with /goal

Tell the user to start the run with `/goal <the plan's objective>` so the
session stays focused on finishing every slice. The goal is done only when the
last stacked PR is merged and its ticket is closed.
