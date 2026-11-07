---
name: story-writer
description: "Write and review functional requirements (FR), user stories, acceptance criteria and use cases for BAs; use when turning a raw idea/requirement into a clear, verifiable story, or grading the quality of an existing story/FR."
---

# Story Writer (FR, User Story, Acceptance Criteria, Use Case)

Goal: output that is **understood on reading and verifiable by testing**. The main job is to write clearly, not to fill in a template. Respond in the language the user is using.

## Hard rules
1. **Never invent business logic.** Where information is missing (rules, numbers, roles, exceptions), write it as a question in "To clarify"; do not fill it in to make it look complete.
2. **One story = one value, one user, one deliverable vertical slice.** If there are two "and"s in the "I want" part, split it.
3. **Every AC must be verifiable true/false** (BABOK 10.1: written atomically so a test case can exist) by observation: a concrete input, action and result. Vague words without criteria are forbidden: fast, easy to use, friendly, suitable, complete, smart, etc. (see `references/quality-checks.md`).
4. **Business rules are separated from operation steps**: write them separately as a BR-xx table, classify as definitional/behavioural, ask about the enforcement level; stories/use cases only refer to them (BABOK 10.47.4, 10.9; see `references/business-rules.md`).
5. **Non-functional items do not go inside functional AC.** When an NFR is found, record a temporary code and hand it to the `nfr-writer` skill.
6. Keep terminology consistent with the glossary the user provides; if there is none, build a short glossary.

## Writing process
1. Identify: who (a specific role, not a generic "user"), the goal, the value, the scope (in/out).
2. If the input is vague, ask at most 4 of the most important questions; if the user does not answer, write a draft with the assumptions stated.
3. Choose the form: story + AC (default); job story when context and motivation matter more than the role; use case when the flow has many steps, many actors, many exceptions; decision table when there are combinations of conditions.
4. Write using `templates/story-template.md`.
4b. A story whose turn has not come (end of the backlog): write only a preliminary version and state clearly that full AC do not exist yet (see `references/agile-context.md`).
5. **Self-check** against `references/quality-checks.md` before returning: look for defects in each AC, check INVEST, check the boundary cases.
6. Every output ends with: **Assumptions**, **To clarify**, **NFRs found** (if any).

## Review mode
Take an existing story/FR. Return a table: item | problem | why it is a problem | how to rewrite. Then give the full rewritten version. No vague criticism; every comment points to the exact sentence at fault.

## Reference files
- `references/quality-checks.md`: quality criteria (BABOK + INVEST from the Agile Extension), defect list and fixes.
- `references/ac-patterns.md`: how to write AC (rules/Given-When-Then), boundary cases to probe, use cases.
- `references/business-rules.md`: writing and classifying business rules (BABOK 10.9).
- `references/agile-context.md`: decomposition, elaboration, backlog, job story, BDD, story map (BABOK 10.2; Agile Extension v2 7.1–7.4, 7.18–7.21).
- `templates/story-template.md`: template and before/after example.
