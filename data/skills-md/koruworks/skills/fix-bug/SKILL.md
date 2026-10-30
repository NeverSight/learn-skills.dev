---
name: fix-bug
description: Fix bugs and make small improvements while leaving the codebase better than it was found. Use when the user asks to fix a bug, clean something up, or make a minor improvement. Every fix explains the root cause for the reviewer, justifies the chosen solution against alternatives, and looks for the simplification the bug is pointing at — and asks before any product decision, large-blast-radius change or persisted schema/format change.
---

# Bug fixes and small improvements

Keep the project's stated principles (a `PRINCIPLES.md`, `AGENTS.md`,
`CONTRIBUTING.md` or similar), if it has them, in mind for every change —
and these in any case: instrument before guessing, prefer the capability the
code already has, and start from the outcome rather than the proposed
mechanism.

Read `docs/acceptances/ATTENTION.md` too, if the project has one — the
systematic lessons from acceptance testing. A bug that matches an entry there
is an instance of a pattern: fix the instance, and say so, so the pattern's
record grows.

**Never assume or take a product decision.** Even a small fix can change what
the customer sees or how the product behaves — an error message, an edge-case
outcome, a default. When it does, stop and ask the user what the final
customer experience should be. Recommend a solution with your reasoning — the
user decides.

**The same goes for anything with a large blast radius.** An architectural
change, a new dependency, a change to the data or domain model — anything that
requires deep understanding of the system and is expensive to reverse — does
not belong in a bug fix without asking first. Ask in simple terms: one
decision per question, what each option means, and what you recommend.

**A persisted schema or format change is announced before it is planned in.**
Any bump of a persisted schema or format version, and any new migration — a
database schema, a file format, a wire or sync format, a settings layout —
says so to the user in those words, "this changes the database schema" (or
"…the file format"), and gets a yes before anything depends on it. A migration
stamps every store it touches and is rarely rolled back, so it is a decision
to take up front, not a surprise at implementation time. Before the first run
that carries one, remind the user to isolate it: run it against disposable
data — a separate data directory, profile or test database — never a shared
or real one.

**Check against the main integration branch first.** Diagnosis must be based
on the latest code: fetch and check how far the branch is behind the main
integration branch (e.g. `main` or `dev`) — `git fetch`, then
`git log --oneline <branch>..<main>`. If it is behind, say so and ask before
bringing it in (see [merge-branch](../merge-branch/SKILL.md)) — a merge
changes the branch and has its own review gate. The drift matters either way:
the bug may already be fixed, moved, or caused by code that has since changed,
so do not investigate stale code silently.

## When fixing a bug

1. **Explain the cause.** Before writing the fix, state what actually went
   wrong and why, in terms a reviewer can verify. If the cause is uncertain,
   add instrumentation and reproduce first — never ship speculative fixes.
2. **Justify the solution.** Describe the fix, the alternatives considered,
   and why this one is better — simpler, more resilient, closer to the
   existing model, or removing the class of bug rather than the instance.
3. **Ask why it happened.** A bug is evidence of a weak spot. Look for the
   simplification it points at: a duplicated mechanism, a missing invariant, a
   component that could not be inspected. Fix or flag that too, so the code
   comes out more resilient, not just patched.

## When improving (and every time you touch code)

- Every touch is an opportunity to leave the code better: clearer names,
  removed duplication, a seam for observability.
- **Large files:** when a change lands in a large file, look for a natural way
  to break it down — smaller files, classes, functions or modules — extracting
  the reusable mechanism and leaving domain behaviour with its domain. Do not
  create generic buckets.

Keep changes small and reviewable; if a refactor grows beyond the fix, propose
it separately rather than bundling it.
