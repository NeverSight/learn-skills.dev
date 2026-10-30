---
name: merge-branch
description: Merge changes from another branch while reviewing them against the project's principles — a merge is a review gate, not a mechanical operation. Use when the user asks to merge a branch, bring changes in from another branch, or resolve a merge. Flags unclear intent, unnecessary complexity and likely bug sources before merging, asks the user about any product decision a conflict would settle, and recommends merging the main integration branch into the other branch first when that is the easier direction.
---

# Merge a branch

A merge is the moment changes enter the shared line, so it doubles as a review
gate. Judge the incoming changes against the project's stated principles (a
`PRINCIPLES.md`, `AGENTS.md`, `CONTRIBUTING.md` or similar), if it has them,
before they land.
`docs/acceptances/ATTENTION.md`, if the project has one, is part of that
standard: a change that repeats a lesson acceptance already taught is a
finding.

**Never assume or take a product decision.** Resolving a conflict or reviewing
a change can quietly decide what the customer sees or how the product behaves —
which behaviour wins, which flow survives. When it does, stop and ask the user
what the final customer experience should be. Recommend a resolution with your
reasoning — the user decides.

**The same goes for anything with a large blast radius.** A conflict resolved
by reshaping the architecture, the data or domain model, or a dependency —
anything expensive to reverse once it is on the shared line — is not yours to
settle inside a merge. Ask first.

**Ask in simple terms.** One decision per question, in plain language, with
your recommendation first and what each option means for the customer. Never
bundle several decisions into one question, and never merge past a question
that is still open.

**Write the answers down.** Every product decision the user makes during the
merge goes into the merge commit message: the question, the option chosen, and
why. The next person reading `git log` should not have to reconstruct it.

Below, `<main>` is the main integration branch (e.g. `main` or `dev`).

## Before merging

1. **Survey what is coming in.** `git log --oneline <target>..<branch>` and
   `git diff --stat <target>...<branch>`, then read the hunks that matter.
   Commit messages should make the intent of each change clear — if the intent
   of a change is not clear from the diff and its messages, ask rather than
   guess.
2. **Review against the principles.** In particular:
   - **Simplicity over complexity.** A change that introduces unnecessary
     complexity — a parallel mechanism, a second copy of something that
     exists, a generic bucket — gets flagged and discussed before it merges,
     not after.
   - **Potential bug sources.** Look for the classic ones: duplicated state,
     timestamp comparisons, blocking I/O on a thread that answers the user,
     byte-based text handling, unlocalized strings.
3. **If the target branch serves another platform**, ask of every incoming
   change what it means there, and record what does not translate — in the
   merge commit or wherever the project tracks platform catch-up — rather than
   letting it become a silent no-op.
4. **Report findings first.** List what the branch does, anything unclear, and
   anything that conflicts with the principles. The user decides whether a
   finding blocks the merge or becomes follow-up work.

## Choosing the merge direction

**If it is easier to merge `<main>` into the other branch first, say so — do
not merge the branch into `<main>` first.** This is the usual case when the
branch is long-lived or conflicts are expected: merge `<main>` → branch,
resolve and verify there where breakage is contained, then merge the (now
clean) branch → `<main>`. Recommend the direction with your reasoning and let
the user confirm.

## Merging

- Resolve conflicts by understanding both sides' intent, never by picking a
  side mechanically. When a conflict reveals the same thing built twice, that
  is a finding, not just a conflict.
- Record in the merge commit message every product decision the user made
  along the way, and any finding they chose to accept as follow-up work.
- After merging, verify: build, run tests proportionate to the change, and
  state explicitly what was and was not verified.
- Do not push unless asked.
