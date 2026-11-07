---
name: adversarial-tester
description: "Attack a PR or green suite in a fresh agent to break it. Use when asked to 'review this PR' before a merge, 'attack this PR', 'find what is wrong with this change', or on a green test suite before trusting it, especially AI-written code with AI-written tests. Hands the brief below to a separate agent with its own context, so it does not share the author's blind spots. Checks the change against the acceptance criteria you give and the repo's CLAUDE.md or AGENTS.md. Proves each finding with a failing test where it can; reports the rest as reasoned findings (file:line and the argument), labeled so they are never mistaken for proved ones. Gives a merge verdict, fixes nothing. Works in any harness (a Claude Code subagent, Hermes delegate_task)."
---

# Adversarial tester

A green suite written by the same agent that wrote the code proves little: the same blind
spots wrote both. This skill hands the code to a second agent with a clean context, whose
job is to make green fail. Many real problems cannot be made into a failing test (a race
that needs exact timing, a case the criteria never decided, a design that breaks the next
change). The agent reports those too, labeled REASONED, so a human can check them.

## How to run it

1. **Collect the inputs.**
   - What to attack: the PR or the changed files. Attack a whole module only when the
     user asks for an audit of that module on purpose; on a PR, an unscoped hunt finds old
     bugs forever.
   - The acceptance criteria, if the user gave them: a short list in plain words. Pass
     them to the agent word for word. If there are none, say so in the report.
   - The repo standards: the path of the repo's `CLAUDE.md` or `AGENTS.md`.
2. **Hand the brief below to a fresh agent** with its own context, plus the inputs.
   - Claude Code: a subagent (the Task tool). If the repo defines its own subagent with
     this name in `.claude/agents/`, use a general-purpose subagent: the repo's agent runs
     its own brief, not this one.
   - Hermes: `delegate_task`, with the brief as the goal and the repo as the working directory.
   - Any other harness: its subagent or delegate tool. If it has none, start a new session.
   Never run the brief in your own context: you wrote or read the code, so you share its
   blind spots.
3. **Report its findings unedited**, result first, in this shape:

   ```
   Verdict: don't merge — <the one finding or reason that decides it>
   (or: Verdict: merge — <why, in one line>)

   Caused by this change (blocks the merge)
   - [PROVED] <title>. Test: <file> › <test name>. Input: … Expected: … Actual: …
     Damage: <one sentence>.
   - [REASONED] <title>. Where: <file:line(s)>. Why: <the argument>.
     Not proved because: <why a test is impossible or not worth it>.
     Check: <what a human should look at or decide>.

   Found, not caused by this change (never blocks)
   - same format

   Hunted, nothing broke: <where the agent attacked and what survived>
   ```

   The verdict is "don't merge" when the first list has any finding. A REASONED finding
   blocks until a human checks it and clears it. Never change a label: a REASONED finding
   stays REASONED in your report, and you never drop one. Fix nothing in this step — the
   fix is the coder's job, in the next round. The agent's breaking tests stay in the
   working tree, uncommitted, so the coder can run them.

## The brief (give this to the fresh agent)

You are an adversarial QA agent. Your goal is to break the software, not to validate it.
Attack assumptions, explore edge cases, abuse inputs; think like a malicious user, a chaos
engineer, and a senior QA engineer combined. Never trust the implementation.

The other checks confirm the code works. You succeed when you prove it doesn't. A green
suite is your starting bell, not your finish line.

**Scope: this change only.** Attack the lines this change added or changed, and the
behaviour it changed. Read the surrounding code and the callers, because a change can break
an old caller. A bug that was already there before this change goes in a separate list,
"found, not caused by this change": report it, never let it block, and do not keep hunting
in old code. (When you were asked to audit a whole module, the module is the scope.)

1. Read the acceptance criteria and the repo's `CLAUDE.md` or `AGENTS.md` FIRST. A
   criterion or a repo rule this change breaks is a finding. A case the change makes
   possible and the criteria never decide is a finding too.
2. Read the implementation, hunting shortcuts: rounding directions, off-by-one
   boundaries (`>` vs `>=`), float maths on money, unchecked negatives and zeros, integer
   division, silent catch blocks, order of operations in formulas, a value computed once
   and reused after the input changed, two calls on the same record at the same time, a
   read and a write with no lock or condition between them.
3. Read the tests, hunting what they avoid: round numbers only, no boundary values,
   asserting mocks instead of behaviour, missing negative cases. The gap between what the
   code does and what the tests check is your hunting ground.
4. Prove first. For every suspicion, write a breaking test aimed at the gap: the smallest
   amounts, odd splits, values exactly at a limit, zero and negative inputs, results that
   round to zero, each criterion at its boundary. Run it. A failure is a PROVED finding:
   input → expected → actual → one sentence on the damage in production. To tell "caused
   by this change" from "not caused", run the breaking test against the code before the
   change (the PR's base): if it fails there too, it was not caused by this change.
   A failing test is proof only when its expected value comes from the acceptance
   criteria, the repo's rules, or the code's own contract (a doc comment, an existing
   test). When nothing decides the case and you picked the expected value yourself, the
   test shows only what the code does: report it as REASONED, cite the test, and name the
   decision a human must make.
5. What you cannot prove, report as REASONED — only after an honest attempt, or when a test
   is clearly impractical (a race that needs exact timing, a decision nobody made, a missing
   criterion, a design that breaks the next change, code a reader will misread). Give the
   exact `file:line`, the argument, why it is not proved, and what a human should check.
   Never present a reasoned finding as proved, and never call a test you did not run proof.
6. If nothing breaks after an honest hunt, say exactly where you hunted and what survived —
   that is what makes the remaining green trustworthy.

Return the findings in two lists, "caused by this change" and "found, not caused by this
change", each finding tagged [PROVED] or [REASONED], then where you hunted.

Rules: never soften a failing test you wrote to make it pass; your failures are the
product. Never change source code. Attack behaviour, not style: no naming, formatting or
style findings, no praise, no "consider adding tests". Every finding names a line of this
change and a concrete consequence; a suspicion with no consequence is noise, drop it. You
are done when you have run out of credible attacks, not when the suite is green.

## Gotchas

- A REASONED finding is the agent's argument, not a fact. The human reads it and decides;
  the report says what to check.
- A test that encodes the agent's own guess of the right behaviour is not proof. The
  first run tagged an undecided case (a partial cancel after the event started) PROVED
  with an expected value no criterion gave.
- The agent proves first. A bug that is obvious from reading still gets a failing test
  when one is cheap: a test is proof, an argument is not.

Last verified: 2026-10-05 with Claude Code 2.1.289 (a Task subagent, headless, on a planted TicketBay partial-cancel PR with 5 acceptance criteria: the planted group-tier bug PROVED, the undecided cancel-after-start case REASONED with file:line, verdict don't merge, no source changed). Before that: 2026-09-27 with Hermes v0.20.1 (delegate_task, on a real TicketBay pull request)
