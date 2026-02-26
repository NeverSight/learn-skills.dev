---
name: china-model-selection-guide
description: China model selection and task-routing guide for Doubao-Seed-2.0-Code, GLM-5, MiniMax-M2.5, and Kimi-K2.5. Use when users need to choose the best-fit model by input type, task complexity, engineering constraints, and delivery goals, including staged multi-model workflows.
---

# China Model Selection Guide

Follow this flow to recommend models. Load `references/china-model-selection-guide.md` for the full Chinese playbook, scenarios, strengths, and prompt templates.

## Quick Triage

Answer two questions first, then give a primary pick.

1. Identify core input type
- Visual-first input (UI mockups, screenshots, sketches): prefer `Doubao-Seed-2.0-Code`
- Very long text or many files (dozens of docs, full codebase): prefer `Kimi-K2.5`
- Structured engineering prompts (clear coding requirements, Shell commands): prefer `GLM-5` or `MiniMax-M2.5`

2. Identify task complexity
- Complex reasoning or autonomous planning (system design, codebase refactor): prefer `GLM-5`
- Cross-language engineering (Python/C++, Java/Go): prefer `MiniMax-M2.5`
- Clear task but heavy execution (UI-to-code, template generation): prefer `Doubao-Seed-2.0-Code`

## Tie-Break Rules

When multiple models fit, decide in this order.

1. Satisfy hard constraints first: vision, long-context, cross-language, agentic planning
2. Then compare cost and latency: pick better price/performance at similar quality
3. Finally split by phase: allow multi-model routing inside one project

## Composite Task Routing

Use this default pipeline.

1. Planning: `GLM-5` for architecture, decomposition, interfaces, schema decisions
2. Build:
- Frontend and visual replication: `Doubao-Seed-2.0-Code`
- Backend scripts, cross-language tasks, terminal automation: `MiniMax-M2.5`
3. Integration debugging: route hard cross-module issues back to `GLM-5`
4. Documentation handoff: send codebase and large document sets to `Kimi-K2.5`

## Output Format

Always include these in recommendations.

1. Decision: primary model + fallback model
2. Rationale: map to input type, complexity, and constraints
3. Risks: likely weak points and rollback strategy
4. Execution: a ready-to-use prompt draft

## References

- Full guide and examples (Chinese): `references/china-model-selection-guide.md`
