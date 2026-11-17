---
name: langgraph-state-management
description: Design state schemas, implement reducers, configure persistence, and debug state issues for LangGraph applications. Use when users want to (1) design or define state schemas for LangGraph graphs, (2) implement reducer functions for state accumulation, (3) configure persistence with checkpointers (InMemorySaver/MemorySaver, SqliteSaver, PostgresSaver), (4) debug state update issues or unexpected state behavior, (5) migrate state schemas between versions, (6) validate state schema structure, (7) choose between TypedDict and MessagesState patterns, (8) implement custom reducers for lists, dicts, or sets, (9) use the Overwrite type to bypass reducers, (10) set up thread-based persistence for multi-turn conversations, or (11) inspect checkpoints for debugging.
---

# LangGraph State Management

## State Design Workflow

Follow this workflow when designing or modifying state for a LangGraph application:

1. **Identify data requirements** — What data flows through the graph?
2. **Choose a schema pattern** — Match the use case to a template
3. **Define reducers** — Decide how concurrent updates merge
4. **Configure persistence** — Select and set up a checkpointer
5. **Validate and test** — Run schema validation and reducer tests

## Quick Start

### Python — Minimal Chat State

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage

class State(MessagesState):
    pass

def chat_node(state: State):
    return {"messages": [AIMessage(content="Hello!")]}

graph = StateGraph(State).add_node("chat", chat_node)
graph.add_edge(START, "chat").add_edge("chat", END)
app = graph.compile()
```

### Python — Subclass MessagesState

For convenience, subclass the built-in `MessagesState` (includes `messages` with `add_messages` reducer):

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]
    query: str
```

### TypeScript — StateSchema with Zod

```typescript
import { StateGraph, StateSchema, MessagesValue, ReducedValue, START, END } from "@langchain/langgraph";
import { AIMessage } from "@langchain/core/messages";
import { z } from "zod/v4";

const State = new StateSchema({
  messages: MessagesValue,
  documents: z.array(z.string()).default(() => []),
  count: new ReducedValue(
    z.number().default(0),
    { reducer: (current, update) => current + update }
  ),
});

const graph = new StateGraph(State)
  .addNode("chat", (state) => ({ messages: [new AIMessage("Hello!")] }))
  .addEdge(START, "chat")
  .addEdge("chat", END)
  .compile();
```

## Schema Patterns

Choose the pattern matching the application type. See [references/schema-patterns.md](references/schema-patterns.md) for complete examples with both Python and TypeScript.

| Pattern | Use Case | Key Fields |
|---------|----------|------------|
| **Chat** | Conversational agents | Built-in `messages` from `MessagesState` |
| **Research** | Information gathering | `query`, `search_results`, `summary` |
| **Workflow** | Task orchestration | `task`, `status` (Literal), `steps_completed` |
| **Tool-Calling** | Agents with tools | `messages`, `tool_calls_made`, `should_continue` |
| **RAG** | Retrieval-augmented generation | `query`, `retrieved_docs`, `response` |

**Template files** are available in `assets/` for each pattern:
- `assets/chat_state.py` — Chat application
- `assets/research_state.py` — Research agent
- `assets/workflow_state.py` — Workflow orchestration
- `assets/tool_calling_state.py` — Tool-calling agent

For RAG state patterns, use reference examples in [references/schema-patterns.md](references/schema-patterns.md).

## Reducers

Reducers control how state updates merge when nodes write to the same field.

### Key Concepts

- **No reducer** → value is overwritten (last-write-wins)
- **With reducer** → values are merged using the reducer function
- A reducer takes `(existing_value, new_value)` and returns the merged result

### Python: Annotated Type with Reducer

```python
from typing import Annotated
import operator
from langgraph.graph import MessagesState

class State(MessagesState):
    # Overwrite (no reducer)
    query: str

    # Sum integers
    count: Annotated[int, operator.add]

    # Custom reducer
    results: Annotated[list[str], lambda left, right: left + right]
```

### TypeScript: ReducedValue and MessagesValue

```typescript
const State = new StateSchema({
  query: z.string(),                    // Last-write-wins
  messages: MessagesValue,              // Built-in message reducer
  count: new ReducedValue(              // Custom reducer
    z.number().default(0),
    { reducer: (current, update) => current + update }
  ),
});
```

### Built-in Reducers

| Reducer | Import | Behavior |
|---------|--------|----------|
| `add_messages` | `langgraph.graph.message` | Append, update by ID, delete |
| `operator.add` | `operator` | Numeric addition or list concatenation |
| `MessagesValue` | `@langchain/langgraph` | JS equivalent of `add_messages` |

### Bypass Reducers with Overwrite

Replace accumulated state instead of merging:

```python
from langgraph.types import Overwrite

def reset_messages(state: State):
    return {"messages": Overwrite(["fresh start"])}
```

### Delete Messages

```python
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

# Delete specific message
{"messages": [RemoveMessage(id="msg_123")]}

# Delete all messages
{"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}
```

For advanced reducer patterns (deduplication, deep merge, conditional update, size-limited accumulators), see [references/reducers.md](references/reducers.md).

## Persistence

Persistence enables multi-turn conversations, human-in-the-loop, time travel, and crash recovery.

### Choosing a Backend

| Backend | Package | Use Case |
|---------|---------|----------|
| **InMemorySaver** | `langgraph-checkpoint` (included) | Development, testing |
| **SqliteSaver** | `langgraph-checkpoint-sqlite` | Local workflows, single-instance |
| **PostgresSaver** | `langgraph-checkpoint-postgres` | Production, multi-instance |
| **CosmosDBSaver** | `langgraph-checkpoint-cosmosdb` | Azure production |

> **Agent Server note:** When using LangGraph Agent Server, checkpointers are configured automatically — no manual setup needed.

### Python Setup

```python
# Development
from langgraph.checkpoint.memory import InMemorySaver
graph = builder.compile(checkpointer=InMemorySaver())

# Production (PostgreSQL)
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:pass@host:5432/db"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # checkpointer.setup()  # Run once for initial schema
    graph = builder.compile(checkpointer=checkpointer)

    result = graph.invoke(
        {"messages": [{"role": "user", "content": "Hi"}]},
        {"configurable": {"thread_id": "session-1"}}
    )
```

### TypeScript Setup

```typescript
// Development
import { MemorySaver } from "@langchain/langgraph";
const graph = builder.compile({ checkpointer: new MemorySaver() });

// Production (PostgreSQL)
import { PostgresSaver } from "@langchain/langgraph-checkpoint-postgres";
const checkpointer = PostgresSaver.fromConnString(DB_URI);
// await checkpointer.setup();  // Run once
const graph = builder.compile({ checkpointer });
```

### Thread Management

Every invocation requires a `thread_id` to identify the conversation:

```python
config = {"configurable": {"thread_id": "user-123-session-1"}}
result = graph.invoke({"messages": [...]}, config)
```

### Subgraph Persistence

Provide the checkpointer only on the **parent graph** — LangGraph propagates it to subgraphs automatically:

```python
parent_graph = parent_builder.compile(checkpointer=checkpointer)
# Subgraphs inherit the checkpointer
```

To give a subgraph its own separate memory:

```python
subgraph = sub_builder.compile(checkpointer=True)
```

For backend-specific configuration, migration between backends, and TTL settings, see [references/persistence-backends.md](references/persistence-backends.md).

## State Typing

### Python: TypedDict (Recommended)

```python
from typing import TypedDict, Annotated, Literal

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next: Literal["agent1", "agent2", "FINISH"]
    context: dict
```

> **Note:** `create_agent` state schemas support `TypedDict` for custom agent state. Prefer TypedDict for agent state extensions.

### TypeScript: StateSchema with Zod

```typescript
import { StateSchema, MessagesValue, ReducedValue, UntrackedValue } from "@langchain/langgraph";
import { z } from "zod/v4";

const AgentState = new StateSchema({
  messages: MessagesValue,
  currentStep: z.string(),
  retryCount: z.number().default(0),

  // Custom reducer
  allSteps: new ReducedValue(
    z.array(z.string()).default(() => []),
    { inputSchema: z.string(), reducer: (current, newStep) => [...current, newStep] }
  ),

  // Transient state (not checkpointed)
  tempCache: new UntrackedValue(z.record(z.string(), z.unknown())),
});

// Extract types for use outside the graph builder
type State = typeof AgentState.State;
type Update = typeof AgentState.Update;
```

For Pydantic validation, advanced type patterns, and migration from untyped state, see [references/state-typing.md](references/state-typing.md).

## Validation and Debugging

### Validate State Schema

Run the validation script to check schema structure:

```bash
uv run scripts/validate_state_schema.py my_agent/state.py:MyState --verbose
```

Checks for: schema parsing issues, empty schemas, reducer annotation problems, message fields without reducers, routing fields without Literal types, and unsupported/unclear schema class patterns.

### Test Reducers

Test reducer functions for correctness and edge cases:

```bash
uv run scripts/test_reducers.py my_agent/reducers.py:extend_list --verbose
```

Tests: basic merge, empty inputs, None handling, type consistency, nested structures, large inputs.

### Inspect Checkpoints

Debug state evolution by inspecting saved checkpoints:

```bash
# List recent checkpoints
uv run scripts/inspect_checkpoints.py ./checkpoints.db

# Inspect specific checkpoint
uv run scripts/inspect_checkpoints.py ./checkpoints.db --checkpoint-id abc123 --thread-id thread-1

# View full history for a thread
uv run scripts/inspect_checkpoints.py ./checkpoints.db --thread-id thread-1 --history
```

`inspect_checkpoints.py` accepts either a direct SQLite DB path or a directory containing `checkpoints.db`.

### Migrate Persisted State

When state shape changes require updating persisted checkpoint values:

```bash
# Dry run first
uv run scripts/migrate_state.py ./checkpoints.db migrations/add_field.py --dry-run

# Apply migration
uv run scripts/migrate_state.py ./checkpoints.db migrations/add_field.py
```

Migration script format:

```python
def migrate(old_state: dict) -> dict:
    new_state = old_state.copy()
    new_state["new_field"] = "default_value"    # Add field
    new_state.pop("deprecated_field", None)      # Remove field
    return new_state
```

### Common State Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| State not updating | Missing reducer | Add `Annotated[type, reducer]` |
| Messages overwritten | No `add_messages` reducer | Use `MessagesState` (or `Annotated[list[BaseMessage], add_messages]`) |
| Duplicate entries | Reducer appends without dedup | Use dedup reducer from [references/reducers.md](references/reducers.md) |
| State grows unbounded | No cleanup | Use `RemoveMessage` or trim strategy |
| Agent state schema rejected | Non-TypedDict `state_schema` in `create_agent` | Use a `TypedDict` agent state schema |
| Parallel update conflict | Multiple `Overwrite` on same key | Only one node per super-step can use `Overwrite` |

For detailed debugging techniques, LangSmith tracing, and checkpoint inspection patterns, see [references/state-debugging.md](references/state-debugging.md).

## Resources

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_state_schema.py` | Validate schema structure and typing |
| `scripts/test_reducers.py` | Test reducer functions |
| `scripts/inspect_checkpoints.py` | Inspect checkpoint data |
| `scripts/migrate_state.py` | Migrate checkpoint state values |

### References

| File | Content |
|------|---------|
| [references/schema-patterns.md](references/schema-patterns.md) | Schema examples for chat, research, workflow, RAG, tool-calling |
| [references/reducers.md](references/reducers.md) | Reducer patterns, Overwrite, custom reducers, testing |
| [references/persistence-backends.md](references/persistence-backends.md) | Backend setup, thread management, migration |
| [references/state-typing.md](references/state-typing.md) | TypedDict, Pydantic, Zod, validation strategies |
| [references/state-debugging.md](references/state-debugging.md) | Debugging techniques, LangSmith tracing, common issues |

### State Templates

| File | Pattern |
|------|---------|
| `assets/chat_state.py` | Chat with `MessagesState` |
| `assets/research_state.py` | Research with custom reducers |
| `assets/workflow_state.py` | Workflow with Literal status |
| `assets/tool_calling_state.py` | Tool-calling agent with `MessagesState` |
