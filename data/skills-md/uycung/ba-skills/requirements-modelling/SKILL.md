---
name: requirements-modelling
description: "Choose and build requirements models for BAs: process (as-is/to-be), entity states, data and data dictionary, decision tables, use cases, scope, functional decomposition, interfaces, role and permission matrix; use when a text description is not clear enough or when you need to check the completeness of a flow, lifecycle or rule set."
---

# Requirements Modelling

Framework from BABOK v3 section 7.1 (Specify and Model Requirements) and techniques 10.11, 10.12, 10.15, 10.17, 10.22, 10.24, 10.35, 10.39, 10.41, 10.44, 10.47. Respond in the user's language. A model is a means to **understand, communicate and expose gaps**, not an end in itself (7.1.4.1: models help confirm understanding and find information gaps and duplicated information).

## Hard rules
1. **Choose the model by the question it must answer**, do not draw everything. Start by asking who will view it and what they need to understand or decide (`references/model-selection.md`).
2. **Never invent elements.** Put into the model only what is in the documents or what the user says. Where something is missing, write "?" in the model and list it under **open questions**; inferred parts carry the label [Inferred], assumed parts [Assumption].
3. **Each model comes with**: purpose, audience, scope (in/out), level of abstraction, unconfirmed elements, open questions. A model without a scope leaves nobody knowing whether it is complete.
4. **Keep meaning consistent across representations** (7.1.4.4): the same entity, state or role must have the same name in the process, data and state models, stories and rules. Use the user's glossary; if there is none, build a short glossary.
5. **Keep rules out of the model**: conditions and thresholds sit in the rule table (BR-xx), and the model refers to the code (BABOK 10.9). A decision with many conditions uses a decision table instead of being crammed into a branching grid.
6. **Conceptual level first.** Logical/physical data models (normalization, foreign keys, indexes) belong to the implementer; the BA stops at the conceptual model unless the user asks (10.15.2).
7. The default output is a **description in tables/text with a Mermaid diagram** so it can be pasted anywhere. Mermaid is only a quick drawing tool, not BABOK notation; if the team uses BPMN/UML/its own tool, hand over the tables and the element list so they can redraw it.

## Process
1. **Identify the purpose of the model**: understand the current state (as-is), agree the future (to-be), check completeness, prepare stories/tests, or hand over to devs. Ask at most the 3 most missing questions.
2. **Choose the model type** per `references/model-selection.md`; you may need two or three complementary types (a process model for the flow, a state model for an entity's lifecycle, a decision table for one decision).
3. **Build a draft** following the matching reference file; start high level, then divide into levels of detail (process 10.35.2, decomposition 10.22).
4. **Self-check** against the "Check" section in the reference file: completeness within the model, cross-check against other models (see `requirements-review`).
5. **Return**: the model, open questions, assumptions, the list of BR rules to be pulled out, and the stories/NFRs that may arise (hand off to `story-writer`, `nfr-writer`).

## Collaboration
From meeting notes: `requirements-elicitation` first. Writing stories/AC from a model: `story-writer`. Checking a model: `requirements-review`. Linking a model to requirements: `requirements-trace`.

## Reference files
- `references/model-selection.md`: model selection table, model groups, abstraction levels.
- `references/process-state.md`: process model, state model, state table.
- `references/data-models.md`: concept model, data model, data dictionary.
- `references/decision-usecase.md`: decision tables, trees, DRD; use cases and scenarios.
- `references/scope-roles-interfaces.md`: scope, functional decomposition, interfaces, role and permission matrix.
- `templates/model-examples.md`: an example of each type (composed by the skill, Mermaid syntax checked).
