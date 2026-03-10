---
name: tool-selector
description: Before executing a task, analyze the available tool set (web search, code execution, file read/write, API calls, database queries, memory tools), select the optimal tools, plan execution order, and prevent unnecessary tool calls. Triggers on multi-step tasks, "which tool should I use", "plan the tools", or whenever multiple tools could apply.
---

# Tool Selector Protocol

Determine which tools are needed to solve the task, plan the most efficient sequence, and eliminate unnecessary calls before they happen.

**Core principle:** Every tool call costs time, tokens, and rate limits. The right tool, in the right order, called once.

---

## Tool Catalog

| Tool | Cost | Side Effect | Best For |
|------|------|-------------|----------|
| Web search | Medium | None (read-only) | Current info, external sources |
| Code execution | Medium | Environment-dependent | Computation, transformation, testing |
| File read | Low | None | Local data, config, content |
| File write | Medium | Persistent change | Saving output, updates |
| API call | High | Rate limits, cost | External service integration |
| Database query | Medium-High | Persistent on writes | Data read/write |
| Memory/context | Low | None | Retrieve previous information |

---

## Selection Algorithm

For each tool candidate, ask these questions in order:

```
1. Can this tool actually solve this task?           → No = eliminate
2. Can a cheaper/simpler tool do the same job?       → Yes = use that instead
3. Was this tool already called for this task?        → Yes = use cached result
4. Is this call actually needed right now?            → No = defer
5. Does this tool depend on another tool's output?    → Yes = add to sequence
```

---

## Anti-Patterns — Block These

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Reading the same file repeatedly | Each read costs tokens | Cache on first read |
| Web search for known information | Unnecessary latency | Use existing knowledge |
| Serial API calls (could be parallel) | Slow | Plan parallel calls |
| Tool chain when one tool suffices | Extra steps | Consolidate |
| Read before write (when unnecessary) | Extra call | Skip the read |
| Loading memory every step | Token waste | Load once, reference |

---

## Output Format

```
TOOL SELECTOR
Task    : [task summary]
Selected: N tools | Total calls: N | Blocked: N

## Tool Plan

| Step | Tool | Purpose | Depends On | Cached? |
|------|------|---------|------------|---------|
| 1 | [tool] | [why] | — | No |
| 2 | [tool] | [why] | #1 | Yes — use #1 output |

## Blocked Calls

| Blocked | Reason | Alternative |
|---------|--------|-------------|
| [tool call] | [rationale] | [what to do instead] |

## Optimization Notes
- [Parallel opportunities]
- [Cached outputs]
- [Rate limit warnings]

Approve? Proceed?
```

---

## Tool Combination Guide

| Task Type | Typical Chain | Block |
|-----------|---------------|-------|
| Research & Report | Search → File read → Code (analyze) → File write | Searching same topic twice |
| Data Processing | File read → Code → File write | Re-reading file each step |
| API Integration | Memory (creds) → API → Code (parse) → DB write | Re-auth per request |
| Code Development | File read → Code (test) → File write → Code (verify) | Full test suite on every change |
| Database Operation | Memory (schema) → DB (SELECT) → Code (prepare) → DB (write) | Running same SELECT twice |

---

## When to Skip

- Single-tool task ("read this file")
- User already specified which tool to use
- Single-step, side-effect-free task

---

## Guardrails

- **Never call an API when cached data suffices** — always check cache first.
- **Prefer low-cost tools** — file read over web search when local data exists.
- **Cross-skill**: works with `parallel-planner` (parallel tool calls) and `task-decomposer` (tool needs per subtask).
