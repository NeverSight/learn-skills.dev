---
name: decompose-task
description: Break large tasks (>100 lines) into atomic, verifiable sub-tasks. Use when a task scope is unclear, touches multiple files/modules, or exceeds comfortable single-commit size. Returns structured breakdown without implementing code.
---

# Task Decomposition

Analyze a task and decompose it into atomic, verifiable sub-tasks when scope exceeds ~100 lines.

## When to Use

- Estimated >100 lines of code change
- Multiple unrelated files changing
- Multiple state transitions or new states
- Backend + frontend changes beyond contract sync
- Vague descriptions ("implement pipeline", "add full support")

## Process

1. **Analyze scope**: Read relevant files, estimate lines per area
2. **Identify boundaries**: Find natural cut points (interfaces, modules, layers)
3. **Propose sub-tasks**: Create checkbox list with line estimates
4. **Return proposal** for human confirmation

## Sub-Task Criteria

Each sub-task should be:
- Completable in one atomic commit
- ~10-50 lines (occasionally up to 100)
- Independently testable or verifiable
- Clearly scoped with success criteria

## Output Format

```
[DECOMPOSITION COMPLETE]

Original task: [description]
Estimated total scope: ~[N] lines across [M] files

Proposed sub-tasks:
- [ ] [sub-task 1] (~N lines) - [brief rationale]
- [ ] [sub-task 2] (~N lines) - [brief rationale]
- [ ] ...

Recommended order: [1 → 2 → 3] or [1, 2 can parallel → 3]
Dependencies: [any blockers or prerequisites]
Questions for human: [if any]
```

## Guidelines

- Do NOT implement code—only analyze and decompose
- Do NOT update plan files directly—return proposal for human confirmation
- If task is already small (<100 lines), report that no decomposition is needed
- Prefer vertical slices (end-to-end thin features) over horizontal layers
