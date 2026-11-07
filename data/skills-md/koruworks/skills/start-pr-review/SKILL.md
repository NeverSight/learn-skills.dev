---
name: start-pr-review
description: Open a pull-request review session — you are the reviewer, not the author. Asks for the spec the change was written from, reads the project's principles and best practices, then reviews the diff for unnecessary complexity, smelly code and drift from the spec, reporting findings first and recording what the user decides on the PR itself. Hands over to start-acceptance once the findings are settled. Use when the user says they are starting a PR review, asks to review a pull request or a branch someone else wrote, or invokes /start-pr-review <pr or branch>.
---

# Start a pull-request review

Someone else wrote this change, and the user is about to judge it with you.
Your seat is the reviewer's: you find, cite and recommend; the user decides
what blocks, and the author learns why. Everything you find and everything
that changes during the session is recorded where the author will read it —
the PR — so that [end-pr-review](../end-pr-review/SKILL.md) can close the
session with a summary written from the record, not from memory.

## Before reading the diff

1. **Ask for the spec.** A change is reviewed against what it was supposed
   to do. Ask which document it was written from — a `PLAN.final.md`, a
   `TECHNICAL.final.md`, an issue, a conversation — and read it. If there is
   none, say so: the review is then against the PR description alone, which
   makes "does it do what was asked" a weaker question, and the user should
   know that before the findings arrive.
2. **Read the project's stated principles and best practices** — a
   `PRINCIPLES.md` (`docs/PRINCIPLES.md` is the usual place), `AGENTS.md`,
   `CONTRIBUTING.md`, the area docs for the code the PR touches — and
   `docs/acceptances/ATTENTION.md`, if the project has them. They are the
   review standard: every finding cites one of them, the spec, or the code.
3. **Survey the PR**: its description, `git log --oneline <main>..<branch>`,
   `git diff --stat <main>...<branch>`, and whether the branch is behind the
   main integration branch. Commit messages should make the intent of each
   change clear; where they do not, that is itself a finding.

## The review

Read the hunks that matter, then ask three questions of the whole and of
each part:

- **Does it do what the spec says — no more, no less?** Scope that crept in
  without a decision, and requirements that are missing, are both findings.
  A product decision the author took quietly is one for the user, not for
  the reviewer to wave through.
- **Is any of it unnecessary complexity?** A parallel mechanism beside one
  that exists, a second copy of something, a generic bucket, an abstraction
  with one caller, configuration nobody asked for, a dependency where the
  code already had the capability. Simplicity over complexity is the rule;
  the burden is on the complexity to justify itself.
- **Does any of it smell?** Long functions and large files that grew rather
  than split; duplicated state; mixed concerns; names that describe the
  mechanism rather than the intent; swallowed errors; dead code; and the
  classic bug sources merge-branch lists — timestamp comparisons, blocking
  I/O on a thread that answers a person, byte-based text handling,
  unlocalized strings. Tests proportionate to the change, or their absence.

**Report findings first**, ordered by severity, each with the file and line,
the citation, and what you recommend. The user decides which block, which
become follow-up work, and which are dismissed — one decision per question,
in plain terms, your recommendation first. Never fix anything before that
conversation: a reviewer who rewrites the change has stopped reviewing it.

## Recording and changing

- **The record is the PR.** Post each settled finding as a review comment on
  the line it concerns, with the decision, when you can (`gh` or the
  project's equivalent). When you cannot post from here, keep the same
  record in one message the user can post, and say so.
- **When the user asks you to fix a finding**, do it with
  [fix-bug](../fix-bug/SKILL.md), as its own commit on the PR branch with a
  message that says why, via [commit-changes](../commit-changes/SKILL.md).
  Never rewrite or force-push over the author's commits, and do not push
  unless asked. The author must be able to read, commit by commit, what
  changed in their work and why.

## Once the findings are settled

When every blocking finding is fixed or consciously accepted, start the
acceptance test with [start-acceptance](../start-acceptance/SKILL.md): the
PR's branch is the feature, and the spec is the scope. The review is not
over until a person has tried the change; the session closes with
[end-pr-review](../end-pr-review/SKILL.md).
