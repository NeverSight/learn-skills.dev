---
name: langgraph-error-handling
description: Implement LangGraph error handling with current v1 patterns. Use when users need to classify failures, add RetryPolicy for transient issues, build LLM recovery loops with Command routing, add human-in-the-loop with interrupt()/resume, handle ToolNode errors, or choose a safe strategy between retry, recovery, and escalation.
---

# LangGraph Error Handling

## Use This Skill For
- Adding `RetryPolicy` to flaky nodes (API, DB, model/tool calls)
- Designing LLM recovery loops (`Command` + error state + retry counters)
- Adding human approval/escalation with `interrupt()` and resume
- Handling prebuilt `ToolNode` failures
- Debugging transactional failure behavior in parallel supersteps

## Strategy Selection

Use this order:

1. Transient/infrastructure issue (`429`, timeout, `5xx`, temporary DB lock) -> `RetryPolicy`
2. Recoverable by model/tool args correction -> store error in state and route back with `Command`
3. Needs user approval or missing info -> `interrupt()` + resume
4. Unknown/programming bug -> let it bubble up and debug

| Error Type | Owner | Primary Mechanism |
|---|---|---|
| Transient | System | `RetryPolicy` |
| LLM-recoverable | LLM | State update + `Command(goto=...)` |
| User-fixable | Human | `interrupt()` + `Command(resume=...)` |
| Unexpected | Developer | Raise/log/debug |

For full taxonomy, load [references/error-types.md](references/error-types.md).

## Minimal Patterns

### 1) Retry Transient Failures

```python
from langgraph.types import RetryPolicy

builder.add_node(
    "call_api",
    call_api,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0),
)
```

```ts
builder.addNode("callApi", callApi, {
  retryPolicy: { maxAttempts: 3, initialInterval: 1.0 },
});
```

Notes:
- Python and JS default retry behavior differs by exception type.
- Prefer targeted `retry_on`/`retryOn` for non-transient domains.

### 2) LLM Recovery Loop

Use `MessagesState` in Python for message state.

```python
from typing import Literal
from typing_extensions import NotRequired
from langgraph.graph import MessagesState
from langgraph.types import Command

class State(MessagesState):
    error: NotRequired[str]
    retry_count: NotRequired[int]

def agent(state: State) -> Command[Literal["tool", "__end__"]]:
    if state.get("retry_count", 0) >= 3:
        return Command(goto="__end__")
    if state.get("error"):
        return Command(goto="tool")
    return Command(goto="tool")
```

```ts
import { StateGraph, Command, END } from "@langchain/langgraph";

// If a node returns Command in JS, add `ends` on addNode.
builder.addNode("agent", agentNode, { ends: ["tool", END] });
```

### 3) Human-In-The-Loop Escalation

```python
from langgraph.types import interrupt, Command

def human_review(state):
    approved = interrupt({
        "question": "Proceed?",
        "payload": state["pending_action"],
    })
    return Command(goto="execute" if approved else "cancel")

# resume
graph.invoke(Command(resume=True), config={"configurable": {"thread_id": "t-1"}})
```

```ts
import { Command, interrupt } from "@langchain/langgraph";

const approved = interrupt({ question: "Proceed?" });
// later
await graph.invoke(new Command({ resume: true }), {
  configurable: { thread_id: "t-1" },
});
```

Requirements:
- Compile with a checkpointer for interrupt flows.
- Reuse the same `thread_id` on resume.

For deep HITL patterns, load [references/human-escalation.md](references/human-escalation.md).

## ToolNode Error Handling

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools, handle_tool_errors=True)
tool_node = ToolNode(tools, handle_tool_errors="Please try again.")
tool_node = ToolNode(tools, handle_tool_errors=(ValueError, TypeError))
```

Use custom handlers when you need deterministic error shaping for model recovery.
For broader tool-recovery design, load [references/llm-recovery.md](references/llm-recovery.md).

## Critical Behavior (Do Not Skip)

1. **Supersteps are transactional**: one failing parallel branch fails the whole superstep state update.
2. **RetryPolicy retries failing branches**, not successful siblings.
3. **`interrupt()` re-runs the node on resume**: side effects before interrupt must be idempotent, or moved after interrupt / separate node.
4. **JS `Command` routing requires `ends` metadata** on `addNode(...)`.
5. **Use explicit retry limits** (`max_attempts`, plus state counters for recovery loops).

## Local Assets In This Skill

### Scripts
- `scripts/classify_error.py`: classify exception category and recommended handling
- `scripts/wrap_with_retry.py`: generate boilerplate node wrappers with retry/recovery/escalation options

Run from repo root:

```bash
uv run skills/langgraph-error-handling/scripts/classify_error.py TimeoutError --verbose
uv run skills/langgraph-error-handling/scripts/wrap_with_retry.py call_llm --with-llm-recovery
```

### Examples
- `assets/examples/retry-example/`: retry + recovery loop (Python and JS)
- `assets/examples/human-loop-example/`: interrupt/resume approval flow (Python and JS)

## Load References On Demand

- `references/error-types.md`: error taxonomy and classification rules
- `references/retry-strategies.md`: retry tuning, backoff, circuit-breaker-style patterns
- `references/llm-recovery.md`: recovery-loop and ToolNode strategies
- `references/human-escalation.md`: human approval, interrupts, and escalation patterns

## Common Failure Modes

| Symptom | Root Cause | Fix |
|---|---|---|
| `interrupt()` fails at runtime | no checkpointer | compile with checkpointer |
| Resume starts new run | different `thread_id` | reuse same `thread_id` |
| JS Command route not taken | missing `ends` | add `ends` to `addNode` |
| Infinite loop | no termination counter/condition | add retry counter + terminal branch |
| Retry never triggers | exception excluded by retry filter | set explicit `retry_on`/`retryOn` |
