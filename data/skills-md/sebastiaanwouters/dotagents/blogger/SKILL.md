---
name: blogger
description: Write interactive technical blog posts inspired by SamWho, Josh W. Comeau, and Grokking-style pedagogy. Use when asked to create deep but approachable educational content with first-principles buildup, narrative storytelling, active learning checkpoints, and practical production guidance.
references:
  - references/post-blueprint.md
  - references/interaction-design.md
  - references/samwho-style-analysis.md
  - references/joshwcomeau-style-analysis.md
  - references/grokking-style-analysis.md
---

# Interactive Tech Post (SamWho + Josh + Grokking)

## Overview

Create long-form technical posts that teach hard ideas with progressive buildup, strong narrative pacing, and hands-on interactivity. Blend SamWho-style bottom-up model building, Josh Comeau-style friendly demo-led teaching, and Grokking-style chapter pacing with active recall checkpoints. Deliver content and interaction specifications that remain portable across tooling stacks.

Use progressive disclosure:
- Start with `references/post-blueprint.md` and `references/interaction-design.md`.
- Pull style references only as needed: `references/samwho-style-analysis.md`, `references/joshwcomeau-style-analysis.md`, `references/grokking-style-analysis.md`.
- Keep context lean; do not load references that are not needed for the requested output mode.

Standalone + tech-neutral constraints:
- Output must remain useful without requiring external URLs, proprietary tools, or specific frameworks.
- Default to plain markdown, pseudocode, and abstract state models unless the user asks for a concrete stack.
- Avoid web-specific assumptions unless the user topic is explicitly web-focused.

## Workflow

1. Lock the brief in one pass.
2. Build a first-principles arc.
3. Attach interactivity to each core concept.
4. Add active-learning checkpoints and mini exercises.
5. Draft the post in SamWho + Josh + Grokking-informed voice.
6. Add implementation-agnostic interaction specs.
7. Run interaction utility + visual polish pass.
8. Run a quality pass against the checklist.

### 1. Lock The Brief

Capture or infer:
- Target concept and boundary of the topic.
- Reader level and assumed prerequisites.
- Desired output depth (outline, partial draft, full post, full post + code).
- Delivery context: markdown article, static site page, or docs portal.
- Constraints: length, tone, production-readiness, accessibility.
- Learning format preference: tutorial-only, tutorial + exercises, or tutorial + exercises + solutions.

If key info is missing, ask up to 3 concise questions. If questions are not possible, state assumptions explicitly and continue.

### 2. Build A First-Principles Arc

Use this section order unless the user asks otherwise:
1. Hook with a real problem.
2. Reader roadmap (what is covered, what is not).
3. Minimal mental model (with analogy if helpful).
4. First interactive toy model.
5. Checkpoint question ("predict before reveal").
6. Controlled complexity increase.
7. Mini exercise with hint or solution outline.
8. Trade-offs, support constraints, and failure modes.
9. Practical use in production.
10. Recap and "what to explore next."

Keep the buildup strict: each section depends only on concepts already introduced.

### 3. Attach Interactivity To Concepts

For each major section, add at least one of:
- Slider-driven parameter exploration.
- Step-through simulation with play/pause.
- Click-to-toggle state transitions.
- "Predict then reveal" checkpoint.
- Small sandbox input/output experiment.
- Inline code playground when syntax learning matters.
- Non-UI alternative (state table, step trace, or prompt/answer block) when widgets are unavailable.

For every interactive element include:
- Learning goal.
- Misconception or confusion it resolves.
- Control(s) available to the reader.
- State model.
- Success criteria (what the reader should notice).
- Before/after mental-model delta.
- Aesthetic intent (clarity, focus, and visual tone).

### 4. Add Active-Learning Checkpoints

For each major concept, include at least one:
- Prediction prompt.
- Short tracing exercise.
- "Spot the bug/trade-off" prompt.

For each exercise include:
- Expected time-to-complete (for example: "1-2 minutes").
- Optional hint.
- Concise answer or solution outline.

### 5. Draft In SamWho + Josh + Grokking-Informed Voice

Write with these constraints:
- Start with reader empathy and practical stakes before formal definitions.
- Teach with concrete examples before abstraction.
- Use short paragraphs and direct language.
- Use one clear section objective at a time.
- Use a conversational teaching voice without filler.
- Add short rhetorical questions where they reduce confusion.
- Explain trade-offs instead of declaring absolutes.
- Include caution notes when simplifications diverge from reality.
- Include support/accessibility caveats when relevant to real usage.
- Add short "what to notice" prompts around interactions.
- Add short recap bullets after major sections.
- Keep terminology and examples portable across domains.
- Treat beauty as functional: polish should improve focus, comprehension, and delight without distracting from the concept.

Do not copy sentences, branding, or character assets from SamWho, Josh W. Comeau, or Grokking books. Emulate structure and pedagogy only.

### 6. Add Interaction Specs (No Framework Lock-In)

When user requests build-ready guidance, produce:
1. Interaction spec (controls, states, transitions, render behavior).
2. Pseudocode or state-machine notation for the interaction loop.
3. Data contract for input/output and reset semantics.

Do not provide framework-specific instructions unless the user explicitly asks to expand scope.

### 7. Run Interaction Utility + Visual Polish Pass

Every interaction must pass all gates:
- Utility gate: removing the interaction would meaningfully reduce understanding.
- Insight gate: interaction reveals a non-obvious behavior, trade-off, or failure mode.
- Simplicity gate: controls are minimal and staged (do not front-load too many knobs).
- Feedback gate: each user action has immediate, interpretable output.
- Beauty gate: visual hierarchy, spacing, and motion improve clarity rather than decoration.

If any gate fails, simplify, replace, or remove the interaction.

### 8. Run Quality Checklist

Ship only when all checks pass:
- Concept is introduced bottom-up.
- Every section has a clear learning objective.
- Interactivity reinforces the concept, not decoration.
- Terminology is defined before use.
- Trade-offs and limitations are explicit.
- Long posts include a clear roadmap or table of contents.
- Reader gets at least one explicit "what to notice" prompt per interaction block.
- Each major concept includes an active-learning checkpoint.
- Exercises include hint/solution support when requested.
- Each interaction addresses a specific misconception or uncertainty.
- Interactions meet utility and polish gates, not just novelty.
- Conclusion summarizes and suggests next experiments.
- Output remains implementation-agnostic and portable.

## Output Modes

### Outline Mode
Return:
- Working title options.
- Section-by-section teaching arc.
- Interactive ideas per section.
- Checkpoint/exercise ideas per section.
- Prerequisites and estimated reading time.

### Draft Mode
Return:
- Full post draft.
- Inline callouts for interactive components.
- Inline callouts for checkpoint questions/exercises.
- Notes for diagrams or animations.

### Build Mode
Return:
- Full post draft.
- Interaction spec with pseudocode/state model.
- Exercise/checkpoint spec with hint and reveal behavior.
- Interaction utility + visual polish checklist.
- Brief test checklist for interaction behavior.

## References

- `references/samwho-style-analysis.md`: Patterns extracted from representative SamWho essays.
- `references/joshwcomeau-style-analysis.md`: Patterns extracted from representative Josh W. Comeau tutorials and essays.
- `references/grokking-style-analysis.md`: Patterns extracted from Grokking-style educational writing.
- `references/post-blueprint.md`: Reusable section templates and storytelling beats.
- `references/interaction-design.md`: Implementation-agnostic interactivity patterns and QA checks.
