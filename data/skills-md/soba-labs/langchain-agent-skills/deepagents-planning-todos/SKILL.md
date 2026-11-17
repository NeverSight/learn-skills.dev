---
name: deepagents-planning-todos
description: Use the write_todos tool effectively for task planning and decomposition in Deep Agents. Use when users want to (1) implement task planning with write_todos, (2) break down complex tasks into subtasks, (3) track agent progress through todos, (4) debug why todos aren't completing, (5) design todo structures for different task types (research, coding, analysis), (6) understand todo status lifecycle and best practices, or (7) visualize todo progression from LangSmith traces.
---

# Deep Agents Planning and Todos

Master the `write_todos` tool for effective task planning and decomposition in Deep Agents.

## Use This Skill When

- You need to break down complex multi-step tasks (3+ steps) into trackable subtasks.
- You want to show users the plan before executing (user approval workflow).
- You're debugging why todos aren't completing as expected.
- You need patterns for different task types (research, coding, analysis, document processing).
- You want to visualize todo progression from LangSmith traces.

## When To Use write_todos

| Use write_todos | Execute Directly |
|-----------------|------------------|
| ✅ Complex multi-step tasks (3-6 steps) | ✅ Simple 1-2 step queries |
| ✅ Tasks requiring user approval first | ✅ Single tool calls |
| ✅ Long-running workflows needing progress tracking | ✅ Quick information lookups |
| ✅ Tasks where planning adds clarity | ✅ Straightforward API calls |

**Decision rule**: If you'd benefit from showing the user "Here's my plan..." before starting, use `write_todos`.

## Quick Start

```python
from deepagents import create_deep_agent

# TodoListMiddleware is included by default in create_deep_agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[search_tool, summarize_tool],
    system_prompt="You are a research assistant. Use write_todos for multi-step tasks."
)

# Agent workflow:
# 1. Call write_todos with initial plan
# 2. Ask user: "Does this plan look good?"
# 3. User approves → start executing
# 4. Update the todo list as work progresses
# 5. Keep todos aligned with the current plan and execution state
```

**Example todo creation:**
```python
# Agent calls write_todos internally:
{
  "name": "write_todos",
  "arguments": {
    "todos": [
      {"content": "Search for papers on LLM agents", "status": "pending"},
      {"content": "Read and extract findings from top 5 papers", "status": "pending"},
      {"content": "Identify common themes", "status": "pending"},
      {"content": "Write summary report", "status": "pending"}
    ]
  }
}
```

## Todo Structure and API

### Two-Field Structure
```json
{
  "content": "Task description (clear, actionable)",
  "status": "pending" | "in_progress" | "completed"
}
```

### Key Constraints

**Full-list updates**: Treat each `write_todos` call as a full state update and include all active todos.

**Per-turn discipline**: Prefer one `write_todos` update per model turn to avoid conflicting plan changes.

**Best granularity**: Keep lists to **3-6 items maximum** (avoid over-fragmentation).

### Tooling Note

Deep Agents documentation describes `write_todos` as the built-in interface for todo planning/tracking.
Keep todo state accurate by rewriting the list with updated statuses as execution progresses.

## Status Lifecycle

```
pending → in_progress → completed
```

**Best practices:**
1. Create todos with `"status": "pending"` for newly planned work.
2. Update to `"in_progress"` when starting work on a todo.
3. Mark `"completed"` when finished (don't delete - keeps context).
4. For interactive workflows, ask user approval ("Does this plan look good?") before starting execution.

**Typical workflow:**
```python
# Step 1: Create initial plan (all pending)
write_todos([
  {"content": "Research topic", "status": "pending"},
  {"content": "Write summary", "status": "pending"}
])

# Step 2: Ask user approval
# User: "Yes, proceed"

# Step 3: Start first task
write_todos([
  {"content": "Research topic", "status": "in_progress"},
  {"content": "Write summary", "status": "pending"}
])

# Step 4: Complete first task, start second
write_todos([
  {"content": "Research topic", "status": "completed"},
  {"content": "Write summary", "status": "in_progress"}
])

# Step 5: Finish all tasks
write_todos([
  {"content": "Research topic", "status": "completed"},
  {"content": "Write summary", "status": "completed"}
])
```

## Todo Patterns By Task Type

### Quick Reference

| Task Type | Pattern | Example Todos |
|-----------|---------|---------------|
| **Research** | gather → synthesize → report | Search docs, Read examples, Analyze patterns, Synthesize findings |
| **Coding** | design → implement → test | Design API, Implement endpoints, Write tests, Test end-to-end |
| **Analysis** | collect → process → analyze | Collect data, Process traces, Analyze patterns, Visualize results |
| **Document Processing** | read → extract → transform | Read files, Extract key info, Transform format, Output result |

**For detailed patterns with code examples**, see `references/todo-patterns.md`.

## Best Practices

### ✅ DO
- **Granularity**: Keep lists to 3-6 items max (clear milestones, not micro-tasks).
- **Naming**: Use clear, action-oriented descriptions ("Search for X", "Analyze Y").
- **User interaction**: Always ask approval before executing plan.
- **Status updates**: Update promptly as items complete (don't skip status transitions).
- **Context management**: Use with filesystem tools for complex workflows.

### ⚠️ DON'T
- **Over-fragment**: Avoid 10+ todos (too granular, hard to track).
- **Vague descriptions**: "Do research" → "Search LangChain docs for Deep Agents overview".
- **Skip approval**: Don't start executing without user confirmation.
- **Forget updates**: Always update status when transitioning tasks.
- **Drop existing context**: Include existing active items when rewriting todos.

## Troubleshooting

### Todo Not Completing

**Symptom**: Todo stuck in `in_progress`, agent loops or gets confused.

**Causes & fixes**:
- Missing status update → Ensure agent updates status when task finishes.
- Unclear completion criteria → Make content more specific ("Read 5 papers" vs "Do research").
- Agent forgot about todos → Add to system prompt: "Use write_todos to maintain and update the plan as work progresses."

### Agent Ignoring Todos

**Symptom**: Agent creates todos but doesn't follow them.

**Causes & fixes**:
- Missing system prompt guidance → Add: "Follow the todo list. Update status as you complete each item."
- One-off task (doesn't need todos) → Use direct execution for simple queries.
- Conflicting instructions → Remove competing planning instructions from prompt.

### Too Many Todos

**Symptom**: 10+ todos, hard to track, agent overwhelmed.

**Causes & fixes**:
- Over-planning → Simplify to 3-6 high-level milestones.
- Nested subtasks → Use todo hierarchy pattern (see `references/todo-patterns.md`).
- Wrong abstraction → Consider breaking into multiple agent invocations.

### Lost Context

**Symptom**: Agent loses track of what's been done.

**Causes & fixes**:
- No filesystem persistence → Use `FilesystemBackend` or `StoreBackend` for long sessions.
- Not maintaining todos → Update `write_todos` whenever status changes or scope shifts.
- Memory issues → Use `MemoryMiddleware` for long-term context.

## Visualizing Todos

Use the included script to parse LangSmith traces and visualize todo progression:

```bash
# Export trace from LangSmith (download JSON)
# Then run:
uv run skills/deepagents-planning-todos/scripts/visualize_todos.py trace.json

# Show Mermaid diagram:
uv run skills/deepagents-planning-todos/scripts/visualize_todos.py trace.json --format mermaid

# Show full timeline:
uv run skills/deepagents-planning-todos/scripts/visualize_todos.py trace.json --show-timeline
```

**Output example**:
```
Todo Timeline for trace abc123:

Initial Plan (Step 1):
  ⏳ [pending] Search for papers on LLM agents
  ⏳ [pending] Read and extract findings
  ⏳ [pending] Identify common themes
  ⏳ [pending] Write summary report

Final State:
  ✅ [completed] Search for papers on LLM agents
  ✅ [completed] Read and extract findings
  ✅ [completed] Identify common themes
  ✅ [completed] Write summary report
```

## Resources

**References (detailed patterns)**:
- `references/todo-patterns.md`: Task-specific patterns with code examples

**Examples (working code)**:
- `assets/examples/todo-driven-agent/`: Research agent demonstrating full workflow

**Example structures (templates)**:
- `assets/todo-structures/research-todos.json`: Research task breakdown
- `assets/todo-structures/coding-todos.json`: Coding task breakdown

**External docs**:
- Deep Agents overview: https://docs.langchain.com/oss/python/deepagents/overview
- Deep Agents customization (middleware defaults): https://docs.langchain.com/oss/python/deepagents/customization
- Deep Agents harness (planning capabilities): https://docs.langchain.com/oss/python/deepagents/harness
- LangChain To-do middleware: https://docs.langchain.com/oss/python/langchain/middleware/built-in
- LangSmith tracing for Deep Agents: https://docs.langchain.com/langsmith/trace-deep-agents
