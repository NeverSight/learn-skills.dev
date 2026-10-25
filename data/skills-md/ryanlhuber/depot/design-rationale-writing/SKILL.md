---
name: design-rationale-writing
description: "Writes a concise rationale for a design decision covering the problem, options considered, the choice, and supporting evidence. Use when stakeholders who were not in the discussion need to understand or approve a decision."
---

# Design Rationale Writing

## Purpose
Write a concise rationale that explains a design decision for stakeholders: the problem, the options considered, the choice, and the reasoning and evidence behind it.

## When to use
- Use when: a decision needs to be understood, reviewed, or approved by people who were not in the design discussion.
- Do not use when: the content is a full design specification; this captures the decision, not every detail.

## Inputs
- Required: the decision made, the problem it addresses, and the options considered.
- Optional: requirements, evidence (research, test results, analytics), constraints, tradeoffs, audience and their priorities, open risks.
- Assumptions: unsupported claims are marked as assumptions.

## Process
1. Identify the audience and what they must decide or understand.
2. State the problem and the user or business outcome in one or two sentences.
3. List the requirements and constraints that shaped the decision, with their sources.
4. Summarize each option considered, with its main benefit and cost.
5. State the chosen option and the reasons, linking each reason to a requirement, evidence, or a labeled heuristic or preference.
6. State the tradeoffs accepted and the risks that remain, with how they will be monitored or validated.
7. Describe how to know whether the decision worked and the conditions under which to revisit it.
8. Cut anything that does not help the audience decide or understand.

## Rules and heuristics
- Required: separate evidence, requirements, heuristics, assumptions, and preferences; do not present preference as fact.
- Required: state limits and conflicting evidence; do not overstate confidence.
- Required: include the options that were rejected and why.
- Recommended: lead with the decision and its main reason; place detail after.
- Recommended: use the audience's language and avoid design jargon.

## Checks
- Each reason traces to a requirement, evidence, or labeled judgment.
- Rejected options and accepted tradeoffs are present.
- No claim of improvement lacks support or a stated validation plan.
- The text can be understood without attending the original discussion.

## Output
Return a short rationale document: decision summary, problem, constraints, options with tradeoffs, reasoning, risks, validation plan, and revisit conditions.

## Completion criteria
- The decision, options, reasoning, and risks are all present and sourced.
- A reader outside the discussion can restate the decision and its basis.
