---
name: implement-unattended-no-subagents
description: Build a settled ticket with the human away and no fan-out — naming and decision authority granted, built and reviewed by this session alone, handed back with every borrowed call tabled on the PR.
argument-hint: "The ticket (issue URL or number), or the spec to build"
disable-model-invocation: true
metadata:
  type: skill
  invocation: human-only
  applies-to: [building, tickets, approvals, naming, worktrees, prs]
---

# implement-unattended-no-subagents

> **human-only.** Start this only when a human asks for it by name. This skill hands out naming and decision authority; a skill chaining into it would be manufacturing the human's approval on their behalf. If you arrived here from anywhere but a human naming it, stop.

`/implement-unattended` minus the fan-out. Same grants, same ledger, same handback — **one session doing the building itself, in one worktree, serially.**

Reach for this rather than the fanned-out version when:

- **The repo restricts subagent use.** That restriction outranks any skill, and this is how you work unattended inside it.
- **The tickets are not independent** — a blocking edge or a shared file makes them one serial unit, and a fan-out over them produces branches that cannot both land.
- **There is one ticket.** Fanning out over one buys nothing but a layer between you and the work.
- **You want the session's own attention on it**, undivided. A single agent that reads the whole tree beats six that each read a slice, when the work is subtle rather than wide.

Read [working unattended](../implement-unattended/unattended.md) first. It is the whole of what changes when there is nobody to ask, and it points at the ledger every borrowed call is held in.

## Process

### 1. Take the terms before touching anything

Read `unattended.md`, and through it the borrowed-authority ledger and `grant-decision-authority`'s **What may be borrowed** section. Then run the ledger's grep:

```
grep -rn "TEMPORARY AGENT" .
```

Hits mean a previous session left loans standing. They go in your PR table as well — a marker you did not make is not yours to remove.

**Done when:** you can state the bounds you are working under, and the tree is either clean of markers or you have listed the ones you inherited.

### 2. Settle the base, then work in a worktree

`/implement`'s steps 1 and 2, unchanged:

```
git fetch origin
git worktree list
gh pr list --state open
git worktree add .claude/worktrees/<ticket> -b <branch> <base>
```

A freshly fetched `origin/main` is the default — never local `main`, never the current `HEAD`. Inside the repo, not beside it.

**Where an open PR overlaps this ticket, that is normally a question for the human, and they are not here.** So it becomes a decision made under the grant: base on `main`, stack on the PR, or leave the ticket blocked — pick one, mark it, and put it in the table as a row. Do not stack on an open PR silently.

**Done when:** the session is in its own worktree, on its own branch, and you can say in one line why that base.

### 3. Build it

`/implement`'s step 3: `/tdd` at pre-agreed seams, typecheck regularly, single test files regularly, the full suite once at the end.

The difference is what happens at a call you cannot approve:

- **In bounds** — make it, write the marker at the site of the act, and continue.
- **Out of bounds** — park it. Do everything that does not depend on it, write down the question and what you would have chosen, and carry on. A parked call that blocks the whole ticket ends the ticket, not the session.

**Done when:** the criteria are met and the gate is green, or the remainder is parked with reasons.

### 4. Review it yourself

Nobody else is going to read this before the human does. Run `/code-review`, and go over the same dimensions `subagent-review` fans out — **serially, one at a time, rather than all at once**, because the point of separating them is that each gets its own attention:

spec and ticket conformance · correctness and failure modes · comments the diff falsified · what should have changed and didn't · tests · tree and commit hygiene · every `TEMPORARY AGENT` marker in the range.

That last one is the check that every borrowed call actually reached the table.

**Done when:** each dimension has been walked and its findings either fixed or written into the handback.

### 5. Commit, PR, table, note

Commit to the worktree's branch — **never to `main`**. Then `/create-pr-for-branch`, with the body leading on the ledger's table, generated from the grep, and the reviewer note verbatim beneath it. Parked calls go under the table as their own list.

**Open it normally, not as a draft.**

**Done when:** the branch has a PR whose table matches its grep exactly, and nothing has been merged.

### 6. Hand back

The handback shape is in `unattended.md`: what got done, what you borrowed, what you parked, what you could not finish, what you dropped, and the one thing you would ask if you could ask one thing.

Then stop. **Do not wait, poll, or schedule a re-check.**

## Where this sits in the flow

`/specs-to-tickets` writes the ticket; **`/implement-unattended-no-subagents`** builds it with nobody watching and stops at an open PR. `/review-pr-in-worktree` judges it when someone is back, `/respond-to-pr-review` is where the table's rows get answered and the markers come out, and `/squash-merge-and-clean-up` lands it.

`/implement-unattended` is the same mode with the build fanned out across subagents and reviewed by them.
