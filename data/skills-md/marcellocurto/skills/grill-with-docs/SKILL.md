---
name: grill-with-docs
description: Stress-test a plan through questions while recording the resulting domain terms and decisions.
disable-model-invocation: true
---

# Grill with Docs

Stress-test the requested plan through conversation and keep agreed domain language and lasting decisions in the project's documentation.

## Load the local guidance

Use the `grilling` skill for questions and decision dependencies, and the `domain-modeling` skill for terminology and architectural records, when available. Locate these repository-owned skills through the available skill catalog and use its supplied locations or loading mechanism; do not infer sibling directories. If either skill is unavailable, continue with the combined procedure below. Do not fetch or substitute an external skill.

## Establish documentation scope

A request to use this workflow includes updating the local glossary and architectural decision records as the user settles decisions. These documentation rules apply when using the supporting skills too. In read-only or proposed-edit mode, keep proposed text in the conversation and do not create or edit files. If the user limits writes to particular documents, update only those documents and keep other proposed records in the conversation.

Inspect the existing glossary, context map, relevant ADRs, and only the code needed to ground the discussion. Follow established documentation locations and formats. When no convention exists, use `CONTEXT.md` for domain terms and `docs/adr/` for qualifying decisions; create them only when there is agreed content to record.

## Question, resolve, record

1. Establish the decision the user wants to resolve and reuse answers already given. Ask questions whose prerequisites are settled, explain the consequential tradeoffs, and recommend an answer when evidence supports it. Defer dependent questions until their inputs are known.
2. Look up facts in the available code and documentation rather than asking the user to supply discoverable information. Keep verified behavior, proposed changes, and unresolved assumptions distinct. The user decides product meaning and tradeoffs; a recommendation or unanswered question is not agreement.
3. After each answer, check for ambiguity or a conflict that would change the meaning. Ask only the clarification needed to resolve that conflict. Treat a clear answer as agreement without requiring another confirmation solely to record it.
4. Capture the agreed result according to the rules below, then continue with the questions it unlocks. If an answer revises an earlier decision, update the affected record so the documentation and discussion agree.

## What to record

- **Domain terms:** Record resolved project-specific concepts, their meaning, and misleading synonyms in the relevant glossary. Keep implementation choices, open questions, and conversation history out of it. When no existing glossary format governs, use the format guidance provided by the `domain-modeling` skill if available; otherwise a concise definition and any terms to avoid are sufficient.
- **Architectural decisions:** Record a settled choice when reversing it has meaningful cost, its rationale would otherwise be unclear, and it resolves a real tradeoff. Include the decision, why it was chosen, and material consequences or rejected alternatives worth preserving. When no existing ADR format governs, use the format guidance provided by the `domain-modeling` skill if available; otherwise a short title and a paragraph explaining the choice and reason are sufficient. Do not create an ADR for every answer.
- **Other answers:** Keep routine choices, tentative proposals, and unresolved questions in the conversation unless the user has requested another destination. Do not turn them into glossary definitions, accepted ADRs, specifications, or tracker issues automatically.

Read back each documentation change and verify that it preserves the user's meaning without promoting an inference to an agreed requirement. Continue under the existing documentation authorization; ask again only when the proposed write exceeds it.

## Finish

Finish when the requested decision is understood or the user pauses the discussion. Report the settled conclusions, remaining material questions, and documentation changed. In read-only or proposed-edit mode, present the proposed text and identify its intended location without claiming it was saved.

Agreement on a design and authorization to record it do not authorize implementation, commits, pushes, or external publication. Continue into those actions only when the user has authorized them.
