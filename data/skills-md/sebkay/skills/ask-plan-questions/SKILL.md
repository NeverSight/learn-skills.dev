---
name: ask-plan-questions
description: "Ask high-impact clarifying questions before implementation to reduce mistakes, rework, and hidden assumptions. Use when creating, reviewing, or updating a plan; when requirements are ambiguous; or when scope/constraints are not fully specified."
---

# Ask Plan Questions

Identify uncertainty in the plan and ask only the questions that materially reduce implementation risk.

Use the `AskQuestion` tool for every question.

Do not force a fixed number of questions. Ask only relevant questions, and stop once risk is acceptably low.

## Workflow

1. Review current context and plan.
2. Identify gaps that could cause defects, rework, or delivery delays.
3. Prioritize questions by impact and urgency.
4. Ask concise, concrete questions with the `AskQuestion` tool.
5. Ask in small batches (1-3 at a time) when many gaps exist.
6. Incorporate user answers before asking the next batch.
7. Continue until the remaining ambiguity is low-risk.

## Question Selection Rules

- Ask only questions that change implementation decisions.
- Skip questions already answered in the thread or files.
- Prefer specific questions over broad prompts.
- Tie each question to one risk area.
- De-prioritize style preferences unless they affect architecture or acceptance.

## Question Bank (pick only relevant items)

Use these as templates. Reword for project context.

1. What is the single success criterion for this task?
2. What is explicitly out of scope for this implementation?
3. Which environments must this work in (local, staging, production)?
4. Are there hard deadlines or sequencing constraints?
5. Which existing behavior must remain unchanged?
6. What are the non-negotiable technical constraints (language, framework, versions)?
7. What data contracts or schemas are fixed versus negotiable?
8. What are the expected edge cases and failure modes?
9. What performance/reliability targets must be met?
10. What security/privacy/compliance requirements apply?
11. What is the source of truth when docs and code disagree?
12. What acceptance tests define "done"?
13. What level of backward compatibility is required?
14. What rollout strategy is expected (flag, staged, immediate)?
15. Who is the final approver for tradeoff decisions?

## Completion Criteria

Finish questioning when all of the following are true:

- Scope boundaries are clear.
- Constraints and dependencies are explicit.
- Acceptance criteria are testable.
- Known high-risk assumptions are resolved or documented.
