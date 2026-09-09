---
name: brainstorming
description: "Brainstorm from diverse perspectives through fresh subagents, then synthesize their insights. Explicit request only."
---

# Brainstorming

Treat the request supplied with `$brainstorming` as the topic. Fan it out to fresh subagents whose prompts use genuinely different thinking operations, then turn their contributions into one coherent landscape.

## 1. Design the Perspectives

1. Extract the topic, goal, known facts, constraints, and desired outcome from the invoking prompt and relevant conversation.
2. Choose at least three pairwise-distinct angles suited to the topic. Consider stakeholder viewpoints, upside, failure, feasibility, assumption inversion, analogy, second-order effects, time horizons, or a wildcard—not as a checklist, but as raw material for task-specific lenses.
3. Keep adding an angle while it covers a consequential aspect the existing angles do not. Stop when another angle would mostly duplicate one already chosen.

The perspective set is complete when it contains at least three non-overlapping lenses and every additional credible lens would add little new territory.

## 2. Dispatch Fresh Thinkers

Write each subagent prompt independently so its wording, questions, and reasoning frame embody its lens. Include enough shared facts for the subagent to understand the task without conversation history, while varying how the problem is posed—for example, as a counterfactual, critique, analogy search, stakeholder narrative, opportunity expansion, or constraint challenge. Scope each subagent to analysis and response only, and ask for concrete insights with the reasoning behind them.

Spawn one subagent per prompt with `fork_turns: "none"`. Omit the `model` and `reasoning_effort` arguments so each subagent inherits both from the caller. Launch independent prompts in parallel when slots permit; if capacity is constrained, continue as slots become available until every designed perspective has run.

Dispatch is complete when every designed perspective has an independently worded prompt and every prompt has been assigned to a fresh subagent.

## 3. Synthesize the Landscape

Wait for every subagent. Compare their contributions, then report:

- the strongest ideas and why they matter;
- surprising or unique angles;
- recurring themes, tensions, and tradeoffs;
- promising combinations across perspectives;
- open questions worth another round, when any remain.

Use the subagents as divergent thinkers and exercise the parent agent's judgment in synthesis. Preserve meaningful disagreement instead of forcing consensus. The brainstorm is complete when every contribution has been considered and the result exposes more useful territory than any single perspective alone.
