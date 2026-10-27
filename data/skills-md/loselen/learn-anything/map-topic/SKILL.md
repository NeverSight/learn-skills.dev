---
name: map-topic
description: Build a prerequisite map for a topic someone wants to learn, fitted to what they already know. Use when the user asks what to learn first, the prerequisites of a subject, a learning path or roadmap, or feels lost and doesn't know where to start. This skill runs the learning pipeline.
license: MIT
---

# Map topic

Based on Gagné's learning hierarchies.

## Pipeline

This skill runs the pipeline:

1. **Goal**: run clarify-goal and build for the reachable goal it returns.
2. **Draft**: build a rough graph. Don't show it yet.
3. **Check**: run check-level against the draft.
4. **Map**: show the final graph, fitted to the level check.
5. **Teach**: offer to start teach-me on the ready-next nodes.

If the user skips the level check, build from what they say they know.

## Building the graph

- Start from the goal task and ask, "What must someone already be able to do to learn this?" Each answer becomes a node one level down. Repeat until you reach what the learner already knows.
- Phrase nodes as abilities ("solve a 2×2 linear system"), not topics ("linear algebra").
- Put isolated facts in a side list. They have no prerequisites.
- When two different prerequisites each lead to a node, show both as alternatives.

## Output

- A Mermaid `graph TD` with rounded nodes (`A(Power rule)`), the goal on top, and arrows from prerequisite to dependent. Mark each node with one status: **solid**, **shaky**, **ready next** or **not yet**. Keep it under about 20 nodes.
- One study order, starting from the ready-next nodes.
- If the goal was lowered, the path to the long-term goal in one line.

## With a learning vault

If the user has a learning vault (a folder whose root `AGENTS.md` starts with `# Learning vault rules`), follow its rules and save the final map:

- Create or update the map note in `Maps/`: goal, graph, lesson links, facts.
- Create a lesson note in `Lessons/` for each new node, with `status: planned`. Reuse notes that already exist.
- Apply status changes from the level check and set each node's class from its lesson status, as the vault rules say. Don't ask for confirmation.
