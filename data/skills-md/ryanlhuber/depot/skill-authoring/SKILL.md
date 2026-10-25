---
name: skill-authoring
description: "Creates or revises one portable agent skill: a focused SKILL.md with a description that triggers at the right time, clear inputs, an actionable process, checks, and tested behavior. Use when someone wants a new skill, a repeated workflow turned into a skill, or an existing skill tightened or fixed. Not for writing agents or workflows, and not for general documentation."
---

# Skill Authoring

## Purpose
Produce one skill that another capable AI can pick up cold, trigger at the right moment, and execute reliably without hidden context. The result is a skill folder, not a one-off prompt.

## When to use
- Use when: a capability should become a reusable skill, a skill is missing inputs or checks, a skill triggers too often or too rarely, or a skill has grown too long.
- Do not use when: the need is a specialist role that owns decisions, a multi-stage process, or documentation for people. Say which it is and stop.

## Inputs
- Required: the capability in one sentence, and at least two realistic requests that should use it.
- Optional: an existing skill or notes to revise, the repository's authoring rules, a near-miss request that should not use it, and the target skill folder.
- Assumptions: confirm the skill's single responsibility and its audience before drafting.

## Process
1. State the one responsibility and the result in a sentence. If it needs "and" between two kinds of work, propose splitting. Check the repository for a skill that already covers it and extend that one instead of duplicating it.
2. Write the frontmatter first. The name is lowercase, hyphenated, and matches the folder. The description says what the skill does, when to use it ("Use when ..."), and what it is not for, in under 1,024 characters. The description is the only text visible before the skill loads, so make it specific to the triggering situations.
3. List required and optional inputs and say what to do when a required input is missing: ask for it or stop, never invent it.
4. Write the process as ordered actions an AI can perform, with decision rules where judgment is needed. Mark required behavior and label recommendations.
5. Add checks that verify the result against evidence, and completion criteria that are observable.
6. Move bulky material (templates, schemas, long examples) into supporting files in the same folder and link them from `SKILL.md`. Keep `SKILL.md` near 80-120 lines.
7. Test with at least two of the realistic requests and the near-miss. Check that the skill triggers, that the output has the promised structure, and that it asks for missing input. Record each result as pass or fail with evidence.
8. Revise from failures, then cut anything that did not change a test result. Use the [skill starter](templates/skill-starter.md) when beginning a new skill.

## Rules and heuristics
- Required: one responsibility per skill. Do not route to other skills or agents, sequence stages, or require another skill for a focused task.
- Required: no harness, model, tool, or platform specifics in the skill. Describe capabilities and outcomes; name technologies only as replaceable examples.
- Required: no secrets, private data, or real people in examples.
- Required: state the skill's limits and what it does not guarantee.
- Recommended: write for execution, with steps and rules rather than background prose; use an example only where it settles an ambiguity.
- Recommended: give reasons for rules that could be mistaken for style so a future editor does not remove them.

## Checks
- The name matches the folder, and the description includes when to use the skill.
- Inputs, output, and completion criteria are observable and none relies on conversation context.
- Every test request produced the expected behavior, and the near-miss did not trigger it.
- No section can be removed without changing execution, and no instruction is duplicated from another skill.

## Output
Return the skill folder contents, the test requests with pass or fail evidence, and any open questions or known gaps. For a revision, also list what changed and why.

## Completion criteria
- The skill passes its tests or the failures are reported.
- A reader with no context could run it from the files alone.
- Nothing was added that the tests did not justify, and limits are stated.
