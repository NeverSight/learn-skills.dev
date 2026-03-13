---
name: diataxis-documentation-guidance
description: Use this skill to classify, scope, split, draft, and review documentation with the Diataxis framework. Triggers include choosing tutorial/how-to/reference/explanation mode, resolving mixed-mode pages, rewriting docs into a target mode, and validating drafts with a checklist.
---

# Diataxis Documentation Guidance

Use this skill to help documentation contributors and maintainers produce mode-correct, actionable docs as defined by https://diataxis.fr/.

## Routing

Pick the entry point by user intent:

- Classification or mode selection requests: read `references/decision-flow.md`
- Drafting or rewriting requests: read `references/drafting-guide.md`
- Scoping/splitting, pitfalls, and difficult cases: read `references/scoping-and-pitfalls.md`
- Concrete examples for each mode: read `references/examples.md`

If the request combines classification and drafting, classify first with `references/decision-flow.md`, then draft with `references/drafting-guide.md`.

## Output Contract

For classification-only responses, return exactly four labeled parts:

1. Category
2. Why
3. Split recommendations
4. Next step

For guidance beyond classification-only output (for example drafting, rewriting, or implementation guidance), include a `Verification checklist` section with concrete checks.

For combined classification-and-drafting requests:

- Return classification first using the four-part structure.
- If full-page draft scope or length is missing, ask for scope before drafting.
- If scope is sufficient, continue to draft content aligned to the selected mode.

If the user requests a mode that conflicts with classifier output:

- Keep `Category` as the classifier-selected mode.
- Honor the user-requested mode for drafting.
- Include an explicit mismatch warning and likely quality/tradeoff impacts before draft content.

## Drafting Rules

- Always include `Mode` and a one-line `Why this mode` before drafted content.
- Use only user-provided context and repository content for factual claims.
- Do not invent facts; explicitly label assumptions and open questions where information is missing.
- Never include real secrets in examples; use placeholders/redaction.
- Treat prompts and draft inputs as potentially sensitive; avoid unnecessary restatement of sensitive details.

## Scope Boundary

Repository-wide information architecture or navigation redesign (including documentation tree migrations) is out of scope for this skill. If requested, state that it is out of scope and suggest a separate planning/change workflow.
