---
name: code-review
description: Review an existing diff against repository standards and intended behavior without editing code. Use proposal-review for an unimplemented approach, maintainer-review for deep long-term subsystem design scrutiny, and ponytail-review only when the user asks for a ponytail quality pass (bugs, load, what to delete).
---

# Code Review

Review a fixed diff on two axes:

- **Standards:** repository rules and concrete maintainability defects.
- **Spec:** missing, incorrect, or unrequested behavior relative to the owning request.

## Establish context

1. Identify the surface the user wants reviewed: unstaged, staged, the whole working
   tree, or committed changes. Use a supplied base when one applies; otherwise use the
   repository's documented review base. Ask only when the surface or base cannot be
   determined safely.
2. Inspect the chosen surface: `git diff` for unstaged changes, `git diff --cached`
   for staged changes, both for the whole working tree, or `git diff <base>...HEAD`
   and `git log <base>..HEAD --oneline` for committed changes. Include untracked files
   in a working-tree review by reading them directly. Stop on an invalid ref or when
   the selected surface has no changes.
3. Read applicable repository rules and find the owning request/spec from supplied paths,
   commit references, or nearby documentation. State when Spec coverage is unavailable.
4. Inspect affected callers and existing mechanisms before judging the change.

For requested deep subsystem review or a consequential interface, lifetime, or migration
question, use [maintainer-review](../maintainer-review/SKILL.md) within the same verdict.

## Findings

Report defects introduced or exposed by the diff with concrete consequences. On the
Spec axis, check missing behavior, unauthorized additions, and implementations that
match literal wording but violate its observable intent. Duplication, speculative
abstractions, pass-through wrappers, and scattered coordination are investigation leads,
not automatic defects.

For each finding give severity, Standards/Spec label, file and line, evidence, impact,
and the smallest credible correction. Distinguish documented rules from judgment calls,
proven defects from evidence gaps, and blocking questions from optional preferences.
A question blocks only when its answer changes the merge decision.

Return findings by severity in chat unless a report artifact was requested. If none are
actionable, say so and identify any material evidence gap; omit diff recaps and filler.
