---
name: spec-conformance-review
description: Review a diff against the spec, issue, or plan it claims to implement, reporting missing or partial requirements, scope creep, and implementations that look wrong, each quoting the spec line. Use when a branch, PR, or working tree is described as implementing a named spec, ticket, or plan, and the question is whether it built what was asked. Do not use for code quality, style, or correctness review on its own; those are a separate axis.
---

# Spec Conformance Review

Code review answers "is this good code?". This review answers "is this what was
asked for?". The two are separate axes: a diff can be clean and miss half its
requirements, or deliver everything through a tangle. Findings from the two axes
are never merged or reranked against each other, because a single ranked list
hides whichever axis lost.

## 1. Pin the range and the spec

Take the fixed point the user names (a commit, branch, tag, or `main`) and
compare with the three-dot form, `git diff <point>...HEAD`, so the comparison is
against the merge base; list the commits with `git log <point>..HEAD --oneline`.
Confirm the ref resolves and the diff is non-empty before reading anything.

Find the spec in this order: references in the commit messages or branch name
(issue ids, a spec path); a path the user passed; a spec under `docs/`, `specs/`,
or the project's planning directory matching the feature. If none exists, ask.
If the user says there is none, stop and report "no spec available" rather than
inventing requirements from the code.

## 2. Read the spec first, then the diff

List every requirement the spec states, including the explicit exclusions and
the acceptance criteria. Only then read the diff, requirement by requirement.

## 3. Report in three sections, quoting the spec

- **Missing or partial**: a requirement with no implementation, or one that
  covers part of the stated behavior. Quote the spec line; name where the diff
  stops short.
- **Not asked for**: behavior, options, endpoints, or abstractions in the diff
  that the spec does not call for. Scope creep is a finding even when the code is
  good, because nobody reviewed the decision to build it.
- **Implemented but looks wrong**: a requirement that has code against it where
  the code's behavior differs from the spec's words (an off-by-one boundary,
  a different default, a case the spec names that the branch never takes).

Each finding carries the quoted spec text and the file and hunk it concerns.
Distinguish "the spec is silent" from "the spec forbids": silence is a question
for the user, not a finding.

## 4. Close

End with one line: findings per section and the worst single gap. When a
code-quality review ran alongside, present its report under its own heading, and
give no combined verdict; the user weighs the axes.
