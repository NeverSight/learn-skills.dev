---
name: explain
description: Explain code and code changes at a chosen level of abstraction. Use when the user asks to understand code, an implementation, or a diff.
---

Explain the requested code or change at the user's chosen **level of abstraction**. Accept a level by number or name. When no level is explicitly provided, use **3. Design**.

A level determines which questions the explanation answers, not its length. Cover the requested level or levels; bring in another level only where it supplies necessary context.

## Levels

1. **Intent: why.** The problem the code solves and the outcome it enables. For a change, explain the reason for changing it. Leave the mechanics out.
2. **Behavior: what.** Observable inputs, outputs, effects, and the conditions that change them. For a change, describe the behavior before and after.
3. **Design: how the parts fit together.** Responsibilities, boundaries, interfaces, state ownership, and dependencies. Trace how the relevant parts collaborate to produce the behavior. Keep algorithms and individual edits for the lower levels.
4. **Implementation: how it works.** The functions, data structures, algorithms, and control flow that produce the behavior. Walk through the relevant execution path with concrete identifiers.
5. **Diff: exactly what changed.** The additions, deletions, and replacements in the selected comparison, with their locations and effects. Use small excerpts where the exact text matters.

## Process

1. Identify the target from the request and conversation. Read the relevant source and enough surrounding code to establish its role. For changes, inspect the comparison identified by the request or context. Ask only if the target or required comparison cannot be determined.
2. Lead with the answer at the selected level, then explain the relationships or sequence needed to understand it. Use the project's glossary vocabulary where available. Choose prose, a short list, or a small diagram according to what makes those relationships clearest.
3. Ground the explanation in the source: link relevant source locations where available, and distinguish observed behavior from inferred intent. Stop when the selected level's question is answered.

Keep the task read-only unless the user also requests changes.
