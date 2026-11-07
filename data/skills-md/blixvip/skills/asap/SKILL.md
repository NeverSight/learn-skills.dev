---
name: asap
description: Execute the current task through the shortest reliable path. Use when the user invokes /asap, says "as soon as possible," or makes speed the main priority. Minimize planning, narration, research, questions, scope, and edits while preserving correctness, safety, and a working result.
---

# ASAP

Complete the user's current task as quickly as possible without creating avoidable mistakes or unfinished work.

## Invocation

Use:

`/asap <task>`

When invoked without a new task, apply ASAP mode to the active or immediately preceding request.

## Operating Rules

1. Start immediately. Do not restate the request or produce a long plan.
2. Identify the exact deliverable and the minimum conditions required for it to count as done.
3. Use existing context and infer reasonable defaults instead of asking unnecessary questions.
4. Ask only when a missing answer makes progress impossible, unsafe, or likely to produce the wrong deliverable.
5. Inspect only the files, code, documentation, or data needed for the current task.
6. Prefer existing project patterns, components, utilities, commands, and dependencies.
7. Make the smallest complete change that satisfies the request.
8. Avoid broad refactors, rewrites, cleanup, optional features, speculative improvements, and unrelated fixes.
9. Use targeted searches and commands instead of scanning the entire project.
10. Parallelize independent reads, checks, or tool calls when possible.
11. If one approach stalls, switch quickly to the simplest reliable fallback.
12. Keep narration minimal. Report only blockers, important discoveries, and the final result.
13. Run the narrowest useful verification: a focused test, typecheck, build, lint check, or direct functional check.
14. Fix failures that block the requested result. Do not expand into unrelated cleanup.
15. Stop as soon as the requested result works and the completion conditions are met.

## Priority Order

1. A working result
2. The user's explicit requirements
3. Safety, security, and data integrity
4. Fast verification
5. Polish that is nearly free

## Never Sacrifice

ASAP mode must not bypass:

- safety or security controls
- authentication or permission requirements
- destructive-operation warnings
- required backups or migration safeguards
- critical validation
- the user's explicit constraints

Speed means removing waste, not removing essential correctness.

## Completion Response

Return a compact summary containing:

- what was completed
- the main files or outputs changed
- the verification performed
- any real remaining limitation or risk

Do not add optional suggestions unless they are necessary to use the result.
