---
name: writing-gpt-5-6-prompts
description: Use when creating, rewriting, optimising, reviewing, or handing off prompts, system prompts, developer instructions, agent briefs, delegation prompts, task specifications, or reusable prompt templates for GPT-5.5 or GPT-5.6, especially when wording is procedural, repetitive, over-scaffolded, vague about success, or unclear about evidence, autonomy, tools, validation, output, or stopping.
---

# Writing GPT-5.6 Prompts

## Principle

Write the smallest prompt that preserves the task or product contract. Treat GPT-5.6 as capable of inferring intent and choosing the method: specify the destination, evidence, boundaries, output, and finish line; prescribe the route only when the route itself is a requirement.

GPT-5.6 guidance takes precedence. Use GPT-5.5 guidance where it adds non-conflicting detail.

## Build the prompt

1. Infer the task, audience, relevant context, available capabilities, and intended level of action. Do not request information that can be safely inferred. Leave placeholders only for inputs whose absence would materially change the result.
2. Default to an outcome-led contract. Add ordered procedure only when order, safety, side effects, protocol compliance, exact commands, or deterministic validation makes the procedure invariant.
3. Include only sections that change behaviour:
   - role or context, when domain function matters;
   - goal and user-visible outcome;
   - success criteria;
   - relevant evidence or source rules;
   - hard constraints, allowed side effects, and approval boundaries;
   - required output, audience, and content priorities;
   - validation, fallback, and stopping conditions;
   - personality or collaboration style only when the experience requires it.
4. For action-taking prompts, define autonomy once. Distinguish inspection or advice from implementation; permit safe, in-scope local work and non-destructive validation; require approval for external writes, destructive or costly actions, purchases, or material scope expansion.
5. State each instruction once. Remove legacy scaffolding, duplicate rules, generic exhortations to think harder, broad brevity commands, unnecessary examples, tool guidance already present in tool descriptions, and schemas or controls enforced by the harness.
6. Reserve absolutes for genuine invariants. Express judgement calls as decision rules with observable triggers, including when ambiguity requires a question.
7. Make brevity content-preserving: name what must remain and what may be cut. Define tone through concrete writing choices rather than vague adjectives.
8. Where correctness can be checked, require evidence and validation of the final deliverable. Define missing-evidence behaviour and an explicit stop condition.

Read only the matching sections of `references/task-modules.md` when the target prompt involves research, editing or creative drafting, coding or visual work, tool orchestration, long-running work, subagents, or handoffs.

## Final check

Before returning the prompt, verify that:

- every instruction changes behaviour and appears once;
- success is objectively recognisable;
- autonomy and approval boundaries are unambiguous where actions are possible;
- every prescribed step is justified by an invariant;
- evidence, ambiguity, fallback, validation, output, and stopping rules are present when material;
- no external configuration or already-enforced schema is duplicated;
- the prompt preserves the user's requirements without inventing new ones.

Return only the finished prompt unless the user asks for analysis, alternatives, or a change log.
