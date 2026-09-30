---
name: afk-loop
description: How the team runs AFK agents — which work to hand to Copilot versus Claude Code, what makes a complete agent brief, how to review the pull request that comes back, and what to do when a run goes wrong.
---

# The AFK loop

How the team runs AFK agents: which work to hand over, how to dispatch it, what to check when a
pull request lands, and what to do when a run goes wrong.

Your repo's `AGENTS.md` is the other half of this. It states the contract an agent works to; this
skill is the human procedure around it.

**Dispatch is manual on purpose.** A team member assigns each `Ready for Agent` issue to Copilot by
hand while we dogfood the coding agent's cost and performance. No workflow fires when a project
field changes, so there is nothing to automate against yet in any case. Once agents pick work off
the frontier themselves, this file loses its reader and should be deleted rather than maintained.

Work state is the `Status` field on the board — see the `issue-tracker` skill.

## Copilot or Claude Code

**Can the work run unattended?**

- **Copilot** — the brief is complete enough that nobody needs to be present. A defined change,
  acceptance criteria that can be checked without asking anyone, no decisions left open.
- **Claude Code** — the work needs a human in the loop: an unfamiliar area to explore, decisions
  that will surface mid-flight, or anything you would want to steer as it happens.

That is the question `Ready for Agent` already answers, so an issue carrying that status is a
Copilot candidate by definition. See **Triage roles** in the `issue-tracker` skill.

## The agent brief

A structured comment posted on the issue when it moves to `Ready for Agent`, written by `/triage`
with `writing-lean`.
**The issue body and discussion are context; the brief is the contract** — it is what the agent
works from.

A brief is complete when it has all of:

- **Category and summary** — `bug` or `enhancement`, and one line on what needs to happen
- **Current and desired behaviour** — including edge cases and error conditions
- **Key interfaces** — types, signatures and config shapes to look for, described rather than
  located. No file paths, no line numbers: an issue may sit ready for weeks and the tree will move
  under it
- **Acceptance criteria** — concrete and independently verifiable, so the agent can tell it is done
- **Out of scope** — what must _not_ change

The full reference, with worked good and bad examples, is
[`AGENT-BRIEF.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/AGENT-BRIEF.md)
in Matt's `/triage` skill. It ships with the skills rather than this repo, so it is absent from a
Copilot container — which is why the checklist above is inlined, and why that link points at
GitHub rather than a local path.

It is written in label vocabulary (`ready-for-agent`), which we no longer use. Read that as
`Ready for Agent`; everything else about a brief is unchanged.

## Dispatching to Copilot

**Read the agent brief before you assign.** The status is a queue position; the brief is the gate.
The person dispatching is the last human to look before an agent spends a run, so refuse anything
that doesn't say what changes in behaviour, how you would know it's done, and what must _not_
change.

To dispatch:

1. Open the issue on GitHub — the 🤖 Frontier view lists what is dispatchable.
2. Under **Assignees**, choose **Copilot**.
3. Set `Status` to `In progress`.
4. Copilot opens a draft pull request shortly afterwards and works in it, pushing commits and
   ticking off its own task list as it goes.

Assigning from the command line does not work — Copilot isn't in the repo's assignee list, so
`gh issue edit <n> --add-assignee Copilot` fails. Use the UI.

## Reviewing an agent's pull request

**Every run ends by requesting review, including the runs that failed.** A review request means the
agent stopped, not that it succeeded — so classify the pull request before reading any code.

The three states a run can end in, the `Status` each carries, and what the agent must leave behind
in each are in **How a run ends**, in the repo's own `AGENTS.md` — that table is deliberately
per-repo. Read the pull request against it, then act:

- **Complete** — review it as you would anyone's pull request, and against the acceptance criteria
  in the issue's agent brief. The pull request template asks about this directly.
- **Blocked** — the agent named a question it could not answer or an action it could not take.
  Resolve it, then reply in the session so the run carries on. It is waiting on you, not stalled,
  and the work resumes where it stopped.
- **Error** — nothing resumes on its own. Decide whether the work goes back to an agent with a
  better brief or to a human, and set the `Status` to match that decision.

A pull request in none of the three states — ready for review but empty, or draft with no
explanation — is an agent defect rather than something to review. clhbid/clhbid.com#2254 is the
worked example: no changes, no acceptance criteria addressed, review requested anyway.

## When a run goes wrong

- **Steer a run that's heading the wrong way** without stopping it: open the session from the pull
  request and type a follow-up in the prompt box below the session log.
- **Stop a run in flight** with **Stop session** in the session log viewer. Commits already pushed
  are kept.
- **Close a bad pull request** rather than fixing it in place, and comment on the issue with what
  went wrong so the next attempt starts with it.
- **Set the status before you unassign.** A dispatched issue stays assigned to Copilot — through
  success, failure, and closure — and the frontier skips anything assigned, so a stalled issue is
  already out of the queue. Unassigning is what puts it back. Before you do, decide whether the
  failure showed the work isn't agent-suitable after all: set `Ready for Human`, or
  `Waiting on input` when it isn't specified well enough to hand over again. Unassign it still on
  `Ready for Agent` and the next dispatch walks into the same failure.
- **Suspect the brief before the agent.** A run that goes wrong usually traces back to a brief that
  left something open, and fixing the brief is what stops it recurring.
