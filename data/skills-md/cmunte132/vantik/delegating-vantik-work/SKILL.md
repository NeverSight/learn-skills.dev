---
name: delegating-vantik-work
description: >-
  How to hand a Vantik issue to Vantik's own coding agent and follow it
  through: when an issue is ready to delegate, how to avoid starting a second
  run beside a live one, what the implement-verify-review loop delivers, and
  how to read a run that finished as Needs review. Use when asked to delegate,
  hand off or run an issue in the background, and when checking on a
  delegated run.
---

# Delegating Vantik work

Vantik can work an issue itself, in a hosted sandbox, while you and the person
you work with get on with something else. `delegate_task` starts a run, and
`list_agent_runs` says how it is going. What comes back is a branch: a pull
request where a git host is connected, otherwise a worktree to review locally.

The run is judged against the issue's **Definition of Done** and nothing else.
The issue *is* the brief, so most of delegating well is making the issue good
enough to be one.

## Is the issue ready to hand over?

Delegate only when all four are true:

1. **It has a Definition of Done a stranger could check.** Every criterion
   concrete, every one testable. A run given an issue without criteria invents
   the requirements it was not given, and then meets them.
2. **It is one contained change.** Several independent changes are several
   issues, and each is its own run.
3. **The repository can check it.** The run executes the repository's own test,
   typecheck, lint and build commands. Work no command can verify — a design
   decision, a judgement about wording — is not ready to delegate.
4. **Nothing is already in flight on it.** Call `list_agent_runs` first. One run
   per issue at a time; `force` starts a second beside a live one, and that is
   almost never what anyone wants.

If one fails, fix the issue before delegating: `update_criteria` with `add` for
a missing criterion, `update_task` for a description that does not say where the
problem lives, `add_note` for context the run will need. That is cheaper than
reviewing a confident diff against imagined requirements.

## What a run does

1. **Implement.** An agent gets the issue, its Definition of Done and the
   repository's commands, and writes the change.
2. **Verify.** Vantik runs the repository's commands against the tree the agent
   left. Vantik runs them, not the agent: an agent that believes it ran the
   tests and did not is a common and quiet failure.
3. **Review.** A second agent, which did not write the change and may not edit
   it, reads the diff against the issue. Every finding cites a `file:line` or a
   failing command.
4. **Revise.** What the review found goes back to be fixed, and the loop returns
   to step 2.

It ends when the reviewer accepts the work and the checks pass. It also ends
when the budget is spent — review passes, money or wall clock, all set in
**Settings → Agents** — or when the loop stops making progress. Either way the
work is delivered; a run that did not get signed off finishes as **Needs
review**, and its pull request says so, with what the last review still
objected to.

## Following a run

`list_agent_runs` gives every attempt at the issue, newest first, with its
status, its branch and pull request, a summary, and why it stopped.

| Status | What it means | What to do |
| --- | --- | --- |
| `QUEUED`, `CLAIMED`, `RUNNING` | Under way | Leave it. Do not start another |
| `SUCCEEDED` | Reviewed, accepted, and the checks pass | Review the pull request like any other |
| `NEEDS_REVIEW` | Delivered without a sign-off | A person reads it, starting from what the last review objected to |
| `FAILED`, `EXPIRED` | Ended badly; `failure` and `error` say why | Fix the cause — often the issue itself — before a new run |
| `CANCELED` | Someone stopped it | Ask before starting it again |

When you tell the person how a run went, give them the pull request and the
status, and for anything but `SUCCEEDED`, the reason it gave.

## Do not

- **Delegate an issue you are working yourself.** Two actors on one issue is the
  collision `pick_up_task` exists to prevent. Hand it over or keep it.
- **Delegate to get a second opinion on your own diff.** The review in the loop
  reads the run's work, not yours.
- **Start the same run again unchanged after it failed.** The same issue gets
  the same result. Change what caused the failure first.
- **Delegate a thin issue to see what comes back.** A run spends real money, and
  a person still has to read what it produces.
