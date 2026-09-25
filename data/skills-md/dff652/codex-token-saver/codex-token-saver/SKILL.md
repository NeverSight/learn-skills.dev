---
name: codex-token-saver
description: Reduce avoidable Codex token and context usage in long-running or repository-scale work by minimizing repeated reads, inefficient polling, context drift, and unnecessary high-capability model use. Apply when users ask to save Codex quota, streamline a long task, or make an agent workflow more context-efficient; do not apply to ordinary short tasks that need no optimization.
---

# Codex Token Saver

Optimize the workflow without weakening correctness, verification, safety, or the user's requested outcome. Treat token savings as a secondary constraint: never skip a necessary file, source, test, or approval merely to reduce usage.

## Choose the lightest useful intervention

Before changing the workflow, identify the actual waste:

- repeated reads of unchanged project context;
- frequent polling while another process is still running;
- a long conversation carrying obsolete decisions;
- a capable or costly model doing bounded mechanical work;
- drift, speculative expansion, or repeated rework.

Apply only the relevant measures below. Do not add process overhead to a short, well-bounded task.

## Reuse context instead of rereading it

- Separate durable context from changing evidence. Durable context includes project purpose, architecture, coding conventions, fixed constraints, and standard commands. Changing evidence includes new requirements, edits, failures, logs, and test results.
- Reuse a concise durable summary when it is already trustworthy. Re-read only the files or sections that may have changed or that the current decision actually depends on.
- Search for symbols and paths before opening large files. Prefer targeted ranges and focused queries to broad directory or document reads.
- Do not rely on memory when correctness depends on current file contents. Check timestamps, diffs, search results, or the relevant source before deciding that a reread is unnecessary.
- For large documents, extract searchable text once when layout is irrelevant. Keep and inspect the original when images, tables, pagination, or formatting affect the task.

## Wait efficiently on long-running work

- Prefer event-driven waits or the longest safe wait interval supported by the current tool over rapid, empty polling loops.
- Do not repeatedly call an empty input/poll operation when the previous operation already returned a reusable session or cell identifier.
- When an outer execution call wraps an inner wait, give the outer call enough time to receive the inner result, including a reasonable buffer. Respect the platform's current maximums and higher-priority instructions; do not hard-code an interval that the active environment forbids.
- During genuinely long waits, send concise user-facing progress updates at the cadence required by the current environment.

## Checkpoint long projects

For work that spans many phases or is likely to resume in another task, create or refresh `DEV_STATE.md` in the project only when persistence is useful and writing it is within scope. Keep it compact and factual:

```markdown
# Development State

## Goal
## Verified current state
## Decisions and reasons
## Files changed
## Tests and results
## Next action
## Blockers or open questions
```

- Record validated state, not a transcript.
- Remove superseded plans instead of accumulating them.
- Treat the repository and test results as the source of truth when they conflict with the checkpoint.
- On resume, read the checkpoint first, then inspect only the files needed to verify that it is still current.

## Route work by difficulty when authorized

When model selection or delegation is available and permitted:

- Keep ambiguous goal interpretation, architecture decisions, task decomposition, and final integration with the strongest appropriate model.
- Give a lower-cost model bounded tasks with explicit inputs, outputs, constraints, and acceptance checks, such as focused review, isolated implementation, or test-failure triage.
- Do not delegate merely to save tokens when coordination or rework is likely to cost more.
- Never assume current model prices or quota multipliers. If cost is part of the recommendation, verify it using current official OpenAI documentation.
- Follow the environment's authorization rules for subagents and model changes; this skill does not grant permission to spawn agents or change models.

## Prevent drift and rework

- If execution diverges from the request, stop the unproductive branch, restate the target and current evidence, then continue from the smallest valid next step.
- Keep temporary side questions out of the main implementation context when the product offers a separate side conversation and the answer is not needed in the primary history.
- Prefer the simplest implementation that satisfies the stated need, build a runnable minimum before optional expansion, use mature dependencies when appropriate, and avoid shortcuts that create foreseeable maintenance debt.
- Do not repeatedly retry the same failed action without inspecting the failure and changing the approach.

## Report the result

At completion, briefly state which optimizations materially changed the workflow, what was still read or tested for correctness, and any remaining uncertainty. Avoid claiming a percentage of tokens saved unless measured from actual usage data.
