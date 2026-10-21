---
name: how
description: Explain how a subsystem works, trace a runtime flow, or determine where code and ownership belong before making a change.
---

# How

Build a working mental model from the code. Explain entry points, data flow, ownership, boundaries, and non-obvious behavior. Use **why** when the user wants historical motivation.

## Choose the mode

- **Explain**. Trace and explain the current system.
- **Critique**. Explain first, then identify architectural problems and practical improvements.

Treat one module or symbol as simple. Treat a flow across several modules or services as complex.

## Explore

For a simple question, inspect and explain inline.

For a complex question, divide the system into two to four non-overlapping slices. If the host supports subagents and the user permits them, assign each slice to a read-only subagent using the parent model. Use different available models only for an explicitly requested multi-model critique. If delegation is unavailable or forbidden, inspect the slices inline in the same order.

Each slice must:

1. Find the real entry point.
2. Trace callers, callees, state, and types from input to output.
3. Read code instead of inferring behavior from file names.
4. Record specific files and symbols.
5. Note behavior a newcomer would probably misunderstand.

Use `references/explorer-prompt.md` for delegated exploration and `references/explainer-prompt.md` for synthesis.

## Explain

Reconcile the slices into one account. Resolve contradictions by reading the code. Do not paste raw exploration reports.

Use only the sections the question needs:

- **Overview**. What the subsystem does and why it exists.
- **Key concepts**. The small set of types, services, or abstractions needed to follow the flow.
- **How it works**. The trigger, ordered steps, decisions, state changes, and output.
- **Where things live**. The files and symbols a maintainer should open first.
- **Gotchas**. Hidden state, surprising coupling, or edge cases.

## Critique

Explain the system before judging it. When permitted, ask two or more read-only critics to assess the same explanation and source files independently. Prefer different available model families when the host supports model selection. Otherwise perform one inline critique against the same rubric.

Read `references/critique-rubric.md` and `references/critic-prompt.md`. Classify each finding:

- **Act on**. A current correctness, security, or maintainability problem.
- **Consider**. A real concern whose value is uncertain.
- **Noted**. Valid but low priority.
- **Dismissed**. Incorrect, context-free, or only stylistic.

Present the explanation first. Then present the critique and cite the files that support each finding.
