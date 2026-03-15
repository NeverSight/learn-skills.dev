---
name: 3-amigos-skill
description: >
  Facilitate a structured 3 Amigos conversation between Product, Development, and QA to
  define functionality before implementation, then extract implementation-ready functional
  requirements from the discussion.

  Use this skill whenever the user mentions 3 Amigos, backlog refinement with Product/Dev/QA,
  defining requirements before coding, clarifying scope and acceptance criteria, reviewing a
  requirements discussion transcript, or turning a feature discussion into user-story style
  requirements. Also use it when the user asks to identify ambiguities, assumptions, business
  rules, or open questions before development starts.
---

# Skill: 3 Amigos Facilitator And Extractor

Use this skill to run a structured 3 Amigos conversation and produce implementation-ready functional understanding.

## Mode Selection

You can operate in two modes:
1. Facilitation mode: the user wants an interactive 3 Amigos conversation.
2. Extraction mode: the user already has notes or a transcript and wants requirements extracted.

Choose the mode before proceeding.
- If the user provides a transcript, meeting notes, or a pasted conversation, use Extraction mode.
- If the user wants help discovering or clarifying the requirements interactively, use Facilitation mode.
- If it is ambiguous, ask one short clarifying question before continuing.

In both modes:
1. Keep the discussion focused on functionality, behavior, quality, and acceptance criteria.
2. Avoid implementation details and code generation.
3. Surface ambiguities, risks, and open questions before closure.
4. Keep the outcome useful for downstream work such as backlog refinement, implementation planning, or Gherkin generation.

## Workflow

### Step 1: Establish the working context
Identify the feature or problem being discussed.

Capture or confirm:
- The business goal.
- The primary users or actors.
- Whether the user wants facilitation or extraction.

### Step 2: Run the appropriate path
For Facilitation mode, read [references/meeting-facilitator.md](references/meeting-facilitator.md) and guide the conversation one question at a time.

For Extraction mode, read [references/feature-extractor.md](references/feature-extractor.md) and convert the discussion into functional requirements.

### Step 3: Deliver a complete requirements view
The result is not complete until it includes:
1. A clear functionality summary.
2. Scope boundaries or explicit scope gaps.
3. Acceptance criteria or testable behavioral statements.
4. Assumptions, dependencies, and open questions.

## Output Expectations

### Facilitation mode output
Return the structured meeting summary defined in [references/meeting-facilitator.md](references/meeting-facilitator.md).

### Extraction mode output
Return the requirement list and filename suggestion defined in [references/feature-extractor.md](references/feature-extractor.md).

If the transcript is incomplete or ambiguous, explicitly include the unresolved questions after the requirements.

## Activation Hints
Typical requests that should trigger this skill:
1. "Facilitate a 3 Amigos meeting"
2. "Help me define requirements with PO, Dev, and QA"
3. "Extract user-story requirements from this 3 Amigos transcript"
4. "Help us refine this backlog item before development"
5. "Identify acceptance criteria and open questions for this feature"
6. "Turn this product/dev/QA conversation into implementation-ready requirements"

## Completion Criteria
This skill is complete only when:
1. The functionality scope is clear and bounded.
2. Acceptance criteria are documented (or explicitly pending where unknown).
3. Open questions and assumptions are explicitly listed.
4. The output is suitable for direct handoff into implementation or test-specification work.

