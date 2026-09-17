---
name: writing-skills
description: Use when creating, revising, or validating reusable agent instructions.
---

# Write Instructions That Improve Decisions

A skill supplies knowledge or decision guidance the agent would otherwise lack.
Assume a capable reader. Prefer a small, clear rule with a concrete example to
repetition, threats, all-caps mandates, or a catalog of supposed rationalizations.

Before writing, identify the actual failure the skill should prevent and when the
skill should apply. Check existing instructions for overlap and contradiction.

Keep the structure simple:

- Frontmatter with a stable `name` and a `description` explaining when to use it.
- Essential decisions, constraints, and examples in `SKILL.md`.
- Supporting references or scripts only when they add reusable value.

Do not turn an ordinary request into a forced chain of skills, checklists,
announcements, documents, and approvals. Preserve real safety and authorization
boundaries. Make optional techniques genuinely optional.

## Validate behavior

Choose a few representative scenarios and state the expected behavior before
testing. Include the motivating failure and a counterexample where blindly
applying the new rule would be wrong.

For a material behavioral change, compare a baseline with the revision when
feasible. If permitted subagents are available, use independent fresh-context
agents for these scenarios and an independent review of the revised instructions.
They should respond to realistic tasks, not recite the rule being tested.
`testing-skills-with-subagents.md` provides a compact procedure.

Inspect outcomes for both improvement and regressions. Increase coverage when the
instruction is broad or results are inconsistent; do not impose an arbitrary
number of repetitions on every wording edit. Small samples are smoke tests, not
proof of reliable behavior across models and tasks.

Also check frontmatter, referenced paths, and any affected bootstrap or plugin
tests. Update active supporting prompts that would contradict the new rule.
Keep historical examples clearly labeled as historical.

Report what was tested, what happened, and what remains untested. Do not claim
success from keyword matching alone or build an evaluation platform for one edit.
