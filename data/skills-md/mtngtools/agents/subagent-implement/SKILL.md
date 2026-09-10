---
name: subagent-implement
description: Build several independent tickets at once — one subagent per ticket, one worktree each, off a single base the parent settled.
argument-hint: "The tickets (issue URLs or numbers), or the map they came from"
disable-model-invocation: true
metadata:
  type: skill
  invocation: human-only
  applies-to: [building, tickets, subagents, worktrees, git, tests, parallel]
---

# subagent-implement

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

`/implement` builds one settled ticket. This builds several at once, one subagent per ticket, where the tickets are genuinely independent of each other. Everything `/implement` says about the work still holds — this skill only changes who does it and how they are kept apart.

**The parallelism is the risk, not the feature.** Two agents that share a checkout corrupt it; two tickets that share a file produce two branches that cannot both land. Step 1 is where this skill earns its keep, and it is not setup to hurry through.

**How a fan-out is run** — isolation, the shell hazard, the brief, the prohibitions, and how results are verified — is [subagent dispatch](./dispatch.md), shared with `subagent-review`. Read it before dispatching anything.

## Process

### 1. Establish independence — before anything is created

A set of tickets is only parallel if none of them needs another's result and none of them will fight another for a file. Both have to be checked; neither is visible from inside a subagent.

Read every ticket in full, then check three things:

- **Blocking edges.** Whatever the tracker uses — `blocked by`, a task list on a parent, a dependency label. A blocked ticket is not in this fan-out at any cost; its blocker is, and it goes in the next round.
- **File overlap.** From the tickets and the specs they name, work out roughly which files each will touch. Two tickets converging on the same file are one serial unit, not two parallel ones. When the overlap is one shared file among otherwise separate work, run the owner first and stack the other on it.
- **Ordering that isn't written down.** A ticket that renames a concept and a ticket that adds a call site using it have no recorded edge and are still strictly ordered. Look for shared vocabulary between ticket bodies.

Then say what you found, in one line per ticket: **parallel**, **serial behind #n**, or **out of this round**.

**Where fewer than two tickets survive, say so and stop.** One ticket is `/implement`, and running this skill over it buys nothing but a layer of indirection between you and the work.

**Done when:** you can name the set going out in parallel and, for every ticket you excluded, the edge or overlap that excluded it.

### 2. Settle the base once, for all of them

The base rules are `/implement`'s step 1 and they do not relax here — they get stricter, because a wrong base is now wrong N times.

```
git fetch origin
git worktree list
gh pr list --state open
```

**The default is a freshly fetched `origin/main`** — never local `main`, never the current `HEAD`. Where an open PR overlaps the set, that is a question for the human, and it is theirs whether or not they are around to answer: stack on it, base on `main` anyway, or wait for it to merge.

**One base for the whole fan-out.** Different bases per ticket means the integration check in step 5 compares things that were never comparable, and the human gets N PRs that cannot be reasoned about together.

**Never dispatch into another session's worktree.** A `locked` entry or a directory this session did not create is someone's work in progress.

**Done when:** you can name the one base and say in one line why it is the base.

### 3. Create every worktree yourself, before dispatching

```
git worktree add .claude/worktrees/<ticket> -b <branch> <base>
```

One per ticket, all off the same base, all created by the parent — **never by the subagents**. Two agents creating worktrees concurrently race on the same git index, and the failure is a corrupt lock file, not a clean error.

Inside the repo, not beside it: `dispatch.md` has the reason.

**Done when:** `git worktree list` shows one worktree per parallel ticket, each on its own branch off the settled base.

### 4. Brief and dispatch

One agent per ticket. The brief carries everything `dispatch.md` requires, plus, for this shape:

- **The ticket in full** — body, acceptance criteria, and the specs it names. Not a summary; the agent cannot go and look at what you paraphrased away.
- **The build method**: use `/tdd` at pre-agreed seams, typecheck regularly, run single test files regularly, run the full suite once at the end. This is `/implement`'s step 3, carried in rather than invoked — `/implement` is `human-only` and a subagent reaching it would stop at its gate paragraph with nobody to answer.
- **The authorization line**: name the skill the human invoked and the date, so the agent does not stall on a confirmation it cannot get.
- **Commit, do not push, do not open a PR.** The parent handles what happens after, and a subagent pushing a bare `git push` is how work lands on a branch nobody named.
- **Return**: the branch name, the commit SHAs, the acceptance criteria met, the gate output it actually saw, and any return items — questions it could not ask, and calls it could not make.

**Done when:** every parallel ticket has an agent working in its own worktree, and you have said which ticket went to which branch.

### 5. Verify what came back — do not take it at face value

Agents report intent as outcome. `dispatch.md` says how to check; for this shape, per branch:

1. **Read the committed diff**, not the working tree, and check it against the ticket's acceptance criteria yourself.
2. **Run the gate on that branch**, whatever the agent said about it.
3. **Anything untracked in the worktree is a finding** — it was clean when you made it.
4. **An agent that returned nothing failed.** Say so; do not read silence as success.

Then the integration check: where the units touched anything in common, merge every branch into a scratch branch off the same base and run the gate once over that. Branches that each pass alone can still break together, and every agent was blind to the others by design. Throw the scratch branch away afterwards — it is a probe, not a deliverable.

**Done when:** every branch has been read and gated by you, and the integration check has run or you have said why it wasn't needed.

### 6. Report, and stop

One report, one voice — the session the human asked. Per ticket: the branch, whether its criteria are met, the gate result, and its return items. Then the integration result, and anything you capped, sampled, or dropped.

**Stop at the commits.** Opening the PRs is `/create-pr-for-branch`, one per branch, and it is a door a human opens. A fan-out is not a licence to open N pull requests nobody asked for.

## Where this sits in the flow

`/specs-to-tickets` writes the tickets; `/implement` builds one and **`/subagent-implement`** builds several. `/subagent-review` is the matching independent read over what came back. `/create-pr-for-branch` opens each PR; `/review-pr-in-worktree` judges it; `/squash-merge-and-clean-up` lands it.

`/implement-unattended` is this plus the authority grants, for when the human is not there to answer the questions the agents will raise.
