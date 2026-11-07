---
name: write-handoff
description: Write docs/<feature>/HANDOFF.md — the briefing a fresh agent session needs to pick up unfinished work with none of the conversation, covering where the branch and checkout are, what is pushed, what to merge first, what was built and which documents are authoritative, where to resume, and the traps that cost this session time. Use when an implementing run (execute-plan, execute-roadmap, build-feature) stops with work still owed, when context is about to run out, or when the user invokes /write-handoff <feature> or asks to hand work to another agent or session. For handing finished work to a person to test and accept, use write-acceptance instead.
---

# Hand the work to the next agent

Work is stopping with something still owed, and the session that knows why is
about to disappear. The next agent starts cold: no conversation, no
reasoning, only the tree and whatever you leave behind.
`docs/<feature>/HANDOFF.md` (in the project's planning folder, unless it uses
another) is what you leave behind.

You are judged on whether that agent's **first hour is productive rather than
archaeological** — whether it knows where the work is, what to do first, and
which of the things it is about to discover are already understood.

**This is not [write-acceptance](../write-acceptance/SKILL.md).** That one
hands *finished* work to a person to test and accept. This one hands
*unfinished* work to an agent. Different reader, different question — a run
that both finished a phase and left one owed writes both.

## When to write one

- The requested scope is not complete: phases deferred, blocked on a
  decision, or stopped for the day.
- Your context is running out mid-task.
- The work moves to another branch, checkout, machine, or person's session.

**Do not write one when the scope is done.** Finished work is described by
`EXECUTION.md` and retired by [close-plan](../close-plan/SKILL.md) or
[close-roadmap](../close-roadmap/SKILL.md); a handoff for it is a fourth
summary of the same run that will go stale and be believed anyway.

## What goes in it

**Start with the state of the tree, because that is what goes wrong first.**
Name the branch and the checkout (or worktree) path, whether the working tree
is clean, and **what has and has not been pushed** — an agent that assumes
`origin` has the work will act on a branch that does not exist. Then the
first action: if the main integration branch (e.g. `main` or `dev`) has
moved, say "merge `<main>` before anything else touches the tree", and say it
before anything else on the page.

- **Where to resume, first and unmissable.** One sentence naming the next
  thing to do. Everything else on the page is context for it.
- **What was built — as pointers, not a retelling.** Name the documents that
  are authoritative (the final plan, the decision records, the generated
  reference) and say plainly that the summary is not the specification. A
  prose recap becomes a second, wrong copy of the plan the moment anything
  changes.
- **The commit list, only where it explains something.** `EXECUTION.md`
  already holds what landed with hashes — link it rather than restating the
  table. What belongs here is the commit whose shape is surprising: the one
  that renumbered the decision records, the one that is merge-only, the one
  still exclusive to this branch.
- **The traps.** The conflict that will recur and the rule that settled it
  last time, the test that fails at the branch base and is not yours, the
  flake and its tell, the thing that looks broken and is not. This is the part
  that cannot be recovered from the tree, so it is the part with the most
  value per line — a trap you name once is a trap the next agent does not pay
  for.
  A trap that is systematic — one the next feature would hit too — also goes
  in `docs/acceptances/ATTENTION.<feature>.md` as a candidate for
  [end-acceptance](../end-acceptance/SKILL.md), if the project keeps
  `docs/acceptances/`: the handoff is deleted when it is consumed, the
  lesson must not be.
- **The decisions taken while the user was away**, with a pointer to the
  questions log (wherever the project keeps open questions; if it has no
  convention, a questions section or file beside the plan). The next agent
  must not silently re-decide them, and must know which are still open.
- **What is deliberately not done**, so the next agent extends the work
  rather than "fixing" an intentional gap.

**Date it and name the session's scope** in the opening line — "written at
the end of the run that built Milestone 1". A handoff is true as of a moment;
an undated one is trusted long after it stops being right.

## How to write it

- **Assume the reader has read the project's agent orientation (an
  `AGENTS.md`, `CONTRIBUTING.md` or similar) and nothing else.** Say so, and
  point at it. Do not restate the repo's standing rules; do point at the area
  docs for the code this work touches.
- **Be concrete about paths, branches and commands.** "The worktree" is not
  an address; `../myapp-wt/spell-check` on branch `spell-check/p4` is.
- **Prefer the fact that is expensive to rediscover.** Anything an agent can
  learn in one `git log` or one grep does not need a paragraph. Anything that
  took you an hour to work out needs one.
- Keep it short enough to be read in full before work starts. A handoff
  nobody finishes hands off nothing.

## Where it sits

- Write it to `docs/<feature>/HANDOFF.md` and commit it as the last commit of
  the run, so it describes the tree the next agent actually clones.
- **Update it in place** rather than appending a second one; a stale handoff
  beside a current one is worse than neither.
- [resume-handoff](../resume-handoff/SKILL.md) is the reader. It checks every
  claim against the tree before trusting it, so write the checkable facts in
  a checkable form — commit hashes, ahead/behind counts, the checkout path,
  the names of the tests that are red on the parent — and never lean on a
  private memory or note the next session may not have. Once the user has
  agreed the direction, it deletes the page: a handoff is consumed, not
  maintained, and the session that consumed it writes the next one from its
  own tree.
- [close-plan](../close-plan/SKILL.md) or
  [close-roadmap](../close-roadmap/SKILL.md) retires it when the feature's
  docs are closed out.
