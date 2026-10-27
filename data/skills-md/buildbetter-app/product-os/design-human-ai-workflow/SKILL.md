---
name: design-human-ai-workflow
description: Design a reliable human-AI workflow with explicit roles, autonomy, context, review, control, recovery, feedback, and accountability. Use when adding copilots, agents, recommendations, generation, or automation to a real workflow and deciding what the AI may do versus what people must control.
---

# Design Human AI Workflow

## Contract

Design the joint system, not an AI feature in isolation. Autonomy must match uncertainty, reversibility, user expertise, and consequence. A human approval step is not a control when the reviewer lacks context, time, or a meaningful alternative.

## Workflow

1. Map the current job, actors, information, tools, decisions, handoffs, exceptions, incentives, and failure recovery.
2. Identify where AI could retrieve, transform, recommend, generate, decide, or act. Compare it with simpler automation and unchanged human work.
3. Assign responsibility for each step: human only, AI proposes, AI acts with confirmation, AI acts within limits, or AI acts with retrospective review.
4. Define context sources, freshness, permissions, provenance, uncertainty, and what the system must never infer or retain.
5. Design previews, explanations, confidence or evidence cues, editing, approval, cancellation, undo, escalation, and safe defaults appropriate to the risk.
6. Handle ambiguity, tool failure, partial completion, conflicting instructions, stale state, unavailable reviewers, and repeated failure without silent continuation.
7. Define learning and feedback loops without making users responsible for endless correction or turning unreviewed feedback into truth.
8. Measure task success, effort, time, quality, override, recovery, trust calibration, distributional effects, and automation-induced errors.

## BuildBetter Acceleration

If BuildBetter MCP is available, search organization skills first. Use calls, workflows, signals, surveys, projects, documents, and synthetic persona exploration to understand work and failure modes. Do not grant access, run external actions, or contact customers without explicit authority.

## Output

Return current workflow, opportunity assessment, responsibility and autonomy map, context contract, interaction states, controls, exception paths, feedback system, measures, and rollout assumptions.

## Quality Gate

Reject AI added without a user outcome, automation that removes meaningful control, review steps that cannot catch errors, hidden external actions, and interfaces that communicate confidence without evidence.

## Provenance

Independently authored. Informed by [ai-native-ux](https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-native-ux), [ai-product-strategy](https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-product-strategy), and [building-with-ai-agents](https://github.com/RefoundAI/lenny-skills/tree/main/skills/building-with-ai-agents).
