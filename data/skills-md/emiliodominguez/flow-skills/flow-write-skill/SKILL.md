---
name: flow-write-skill
description: "Write or fix an agent skill. Use when an agent ignores, misapplies or fails to load a skill, or to create a SKILL.md with a trigger description, lean body and evals. Hands off to `flow-review`."
metadata:
  stage: build
---

# Write a skill

A skill is a pointer plus a procedure. The description decides whether it loads; the body
decides what the agent does once it has. Write only what changes behavior you have observed.

## Phase 1: Prove the gap

- Name the task, the observed failure and who hits it. Check existing skills and instruction
  files first; extend or fix one before adding another that competes for the same trigger.
- Run the task without the new guidance in a fresh context and record what the agent actually
  does, including the excuses it gives for skipping steps. If the baseline already succeeds,
  write nothing.
- Decide the scope: one job, one trigger family. Two unrelated triggers mean two skills.

## Phase 2: Write the description

The description is always in context, so every word costs tokens across every session.

- Lead with a short noun phrase for what it is, then `Use when` plus concrete triggers: user
  phrasings, symptoms, file types or situations. Include near-miss boundaries ("not for X; use Y").
- Do not summarize the procedure. An agent that reads the steps in the description may follow
  them and skip the body.
- Third person, key word first, no host or model names. Stay within the repository's length
  budget and end with any handoff convention it uses.

## Phase 3: Write the body

Match the form of guidance to the failure you observed:

| Failure | Form |
| --- | --- |
| Knows the rule, skips it under pressure | One firm rule, the reason, and a red-flags list of the excuses you recorded |
| Produces the wrong shape | A positive recipe or template showing the expected output |
| Keeps omitting an element | A required slot in the template |
| Should vary by situation | A condition keyed to something observable |

- Phases or a numbered process, then `Anti-patterns` and `Done when` with checkable exits.
- Explain why instead of stacking capitalized MUSTs. Avoid vague escape hatches ("unless it
  matters"); they erase the rule.
- Keep the body short (aim for a few hundred words). Move situational detail to
  `references/<topic>.md`, one level deep, and say exactly when to read each file.
- Put deterministic, repeatable steps in `scripts/`, invoked through their interpreter, and
  templates in `assets/`. Never embed secrets, host-specific paths or invocation syntax.

## Phase 4: Test it

- **Triggering:** about ten prompts that should load the skill and ten near misses that should
  not. Check both directions; tune the description, not the body, for trigger problems.
- **Behavior:** rerun the baseline task with the skill in a fresh context, several times. Compare
  against the no-skill run on concrete assertions. An assertion that passes either way tests nothing.
- Fix only observed gaps, then run the repository's validators and size checks.

## Anti-patterns

- Writing a skill for a failure nobody has observed.
- A description that restates the workflow, or so generic it triggers on everything.
- Walls of rules for every edge case instead of a reference loaded on demand.
- Declaring a skill works because it validates, without a behavior comparison.

## Done when

- A recorded baseline shows the gap, and the skill run closes it on the same task.
- Trigger checks pass for positive and near-miss prompts.
- The skill passes repository validation and stays within its size budgets.

Review the result with `flow-review`.
