---
name: skill-auto-update
description: Keep agent skills aligned with durable feedback by distilling comments, corrections, and repeated guidance into the narrowest existing skill. Use on every turn, and especially when feedback reveals a reusable rule, a repeated miss, or a better abstraction that should replace a task-specific example.
---

# Skill Auto Update

Use this skill to keep project skills aligned with what feedback keeps teaching.

## Activation

This skill is most effective when the workspace `AGENTS.md` tells the AI to use it on every turn. Add a short rule such as: `Use $skill-auto-update on every turn to distill durable feedback into the narrowest existing skill.`
Treat routine use as a silent background check. Do not announce that you are using this skill unless it produces a user-relevant skill edit or the user explicitly asks about it.

## Run this loop

1. Scan the current turn for durable feedback signals such as user corrections, review comments, comments on issues or pull requests, repeated instructions, and explicit "do this / avoid this" guidance.
2. Ignore one-off facts, task-local preferences, and literal examples that do not imply a reusable rule.
3. Rewrite the signal as a principle: capture the idea, not the anecdote; state the invariant in one short sentence; prefer imperative wording such as `Prefer`, `Keep`, `Move`, or `Avoid`.
4. Translate taste or persona goals into concrete engineering rules; prefer `Keep functions small and cohesive` over `code like Uncle Bob`.
5. Update the narrowest existing skill that owns the rule. Prefer updating an existing skill over creating a new one.
6. Search the target skill for the same idea, including paraphrases and nearby rules.
7. If the idea already exists, do not duplicate it. Tighten the existing rule only when the new feedback adds missing scope, rationale, or priority.
8. Create a new skill only as a last resort: only when the lesson is durable and no existing skill or section can contain it cleanly.
9. When a new rule subsumes older examples, remove or compress the examples instead of keeping both.
10. If the same rule is missed again, increase its score instead of adding another bullet.
11. Keep the edit minimal. Prefer one changed bullet over new sections, long explanations, copied examples, repeated examples, or checklists of symptoms.
12. If no durable lesson exists, make no skill edit and do not mention the check.

## Score rules

- Treat score as an optional weight for repeated misses.
- Use no score marker for a fresh rule unless recurrence already matters.
- Append ` [score: N]` to the rule when increasing weight.
- Start at `2` for the second clear miss and increment by one for later misses.
- Cap scores at `5`.
- Do not raise score for a mere style preference.

## Rule shape

- Good: `Keep shared components data-driven; move module-specific policy back to the owning feature. [score: 3]`
- Bad: `Do not repeat the status-action-button mistake from the custom module table.`

## Editing standard

- Keep skill text concise and imperative.
- Avoid historical commentary, changelogs, and case-specific prose.
- Prefer strengthening an existing rule over adding a sibling rule that says the same thing differently.
- Prefer a new section inside an existing skill over creating a new skill.
- Prefer general rules over examples; add at most one generic example only when the rule would otherwise be ambiguous.
- When a rule and an example say the same thing, keep the rule and delete the example.
- Do not multiply examples for the same rule; replace them with one generic example or none.
