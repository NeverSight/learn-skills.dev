---
name: langgraph-agent-patterns
description: Implement multi-agent coordination patterns (supervisor-subagent, router, orchestrator-worker, handoffs) for LangGraph applications. Use when users want to (1) implement multi-agent systems, (2) coordinate multiple specialized agents, (3) choose between coordination patterns, (4) set up supervisor-subagent workflows, (5) implement router-based agent selection, (6) create parallel orchestrator-worker patterns, (7) implement agent handoffs, (8) design state schemas for multi-agent systems, or (9) debug multi-agent coordination issues.
---

# LangGraph Agent Patterns

Implement and configure multi-agent coordination patterns for LangGraph applications.

## Pattern Selection

Choose the right pattern based on your coordination needs:

| Pattern | Best For | When to Use |
|---------|----------|-------------|
| **Supervisor** | Complex workflows, dynamic routing | Agents need to collaborate, routing is context-dependent |
| **Router** | Simple categorization, independent tasks | One-time routing, deterministic decisions |
| **Orchestrator-Worker** | Parallel execution, high throughput | Independent subtasks, results need aggregation |
| **Handoffs** | Sequential workflows, context preservation | Clear sequence, each agent builds on previous |

**Quick Decision:**
- **Dynamic routing needed?** → Supervisor
- **Tasks can run in parallel?** → Orchestrator-Worker
- **Simple categorization?** → Router
- **Linear sequence?** → Handoffs

For detailed comparison: See references/pattern-comparison.md

## Pattern Implementation Guides

### Supervisor-Subagent Pattern

**Overview:** Central coordinator delegates to specialized subagents based on context.

**Quick Start:**

```bash
# Generate supervisor graph boilerplate
uv run scripts/generate_supervisor_graph.py my-team \
  --subagents "researcher,writer,reviewer"

# TypeScript
uv run scripts/generate_supervisor_graph.py my-team \
  --subagents "researcher,writer,reviewer" \
  --typescript
```

**Key Components:**
1. **State with routing**: `next` field for routing decisions
2. **Supervisor node**: Makes routing decisions based on context
3. **Subagent nodes**: Specialized agents with distinct capabilities
4. **Conditional edges**: Route from supervisor to subagents

**Example Flow:**
```
User Request → Supervisor → Researcher → Supervisor → Writer → Supervisor → FINISH
```

**For complete implementation:** See references/supervisor-subagent.md

### Router Pattern

**Overview:** One-time routing to specialized agents based on initial request.

**Key Components:**
1. **State with route**: Single routing decision field
2. **Router node**: Categorizes request (keyword, LLM, or semantic)
3. **Specialized agents**: Independent agents for each category
4. **Conditional routing**: Route to agent, then END

**Example Flow:**
```
User Request → Router → Sales Agent → END
                   ├→ Support Agent → END
                   └→ Billing Agent → END
```

**Routing Strategies:**
- **Keyword-based**: Fast, simple string matching
- **LLM-based**: Semantic understanding, flexible
- **Embedding-based**: Similarity matching
- **Model-based**: Fine-tuned classifier

**For complete implementation:** See references/router-pattern.md

### Orchestrator-Worker Pattern

**Overview:** Decompose task into parallel subtasks, aggregate results.

**Key Components:**
1. **State with subtasks**: Task decomposition and results accumulation
2. **Orchestrator node**: Splits task into independent subtasks
3. **Worker nodes**: Process subtasks in parallel
4. **Aggregator node**: Synthesizes results
5. **Send fan-out**: Return `Send(...)` objects from conditional edges and use a list reducer (for example `Annotated[list[dict], operator.add]`) so worker outputs accumulate

**Example Flow:**
```
Task → Orchestrator → Worker 1 ┐
                  → Worker 2  ├→ Aggregator → Result
                  → Worker 3 ┘
```

**Best Practices:**
- Ensure subtasks are independent
- Handle worker failures gracefully
- Limit concurrent workers for resource management
- Use LLM for result synthesis

**For complete implementation:** See references/orchestrator-worker.md

### Handoffs Pattern

**Overview:** Sequential agent handoffs with context preservation.

**Key Components:**
1. **State with context**: Shared context across handoffs
2. **Agent nodes**: Each agent hands off to next
3. **Handoff logic**: Explicit or conditional handoffs
4. **Context management**: Preserve and pass information

**Example Flow:**
```
Request → Researcher → Writer → Editor → FINISH
         (with context preservation)
```

**Handoff Strategies:**
- **Explicit**: Agent declares next agent
- **Conditional**: Based on completion criteria
- **Circular**: Agents can hand back for revisions

**For complete implementation:** See references/handoffs.md

## Examples

Runnable mini-projects (Python + JavaScript):

- `assets/examples/supervisor-example/`
- `assets/examples/router-example/`
- `assets/examples/orchestrator-example/`
- `assets/examples/handoff-example/`

## State Design for Multi-Agent Patterns

Each pattern requires specific state schema design:

**Supervisor Pattern:**
```python
class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next: Literal["agent1", "agent2", "FINISH"]
    current_agent: str
```

**Router Pattern:**
```python
class RouterState(TypedDict):
    messages: list[BaseMessage]
    route: Literal["category1", "category2"]
```

**Orchestrator-Worker:**
```python
import operator
class OrchestratorState(TypedDict):
    task: str
    subtasks: list[dict]
    results: Annotated[list[dict], operator.add]
```

**Handoffs:**
```python
class HandoffState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_agent: str
    context: dict
```

**For detailed state patterns:** See references/state-management-patterns.md

## Validation and Visualization

### Validate Graph Structure

```bash
# Validate agent graph for issues
uv run scripts/validate_agent_graph.py path/to/graph.py:graph

# Checks for:
# - Unreachable nodes
# - Cycles without termination
# - Dead ends
# - Invalid routing
```

### Visualize Graph

```bash
# Generate Mermaid diagram
uv run scripts/visualize_graph.py path/to/graph.py:graph --output diagram.md

# View in browser or IDE with Mermaid support
```

## Common Patterns and Anti-Patterns

### Best Practices

**1. Clear Agent Responsibilities**
- Define non-overlapping capabilities
- Document each agent's purpose
- Avoid agent duplication

**2. Loop Prevention**
- Track iteration count in state
- Set maximum iterations
- Implement loop detection

**3. Context Management**
- Summarize context when it grows large
- Only pass necessary information
- Use structured context where possible

**4. Error Handling**
- Validate routing decisions
- Handle invalid routes gracefully
- Default to safe fallbacks

### Anti-Patterns to Avoid

**1. Over-Supervision**
```python
# ❌ Bad: Supervisor for simple linear flow
User → Supervisor → Agent1 → Supervisor → Agent2 → Supervisor

# ✅ Good: Use handoffs instead
User → Agent1 → Agent2 → FINISH
```

**2. Complex Router Logic**
```python
# ❌ Bad: Complex routing rules in router
if complex_condition_A and (condition_B or condition_C):
    route = determine_complex_route()

# ✅ Good: Use supervisor with LLM
route = llm.invoke("Analyze and route: {query}")
```

**3. Unmanaged State Growth**
```python
# ❌ Bad: Accumulating all messages forever
messages: list[BaseMessage]  # Grows unbounded

# ✅ Good: Summarize or limit
if len(messages) > 20:
    messages = summarize_context(messages)
```

## Debugging Multi-Agent Systems

### 1. Trace Agent Flow

Use LangSmith to visualize agent interactions:

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "<your-api-key>"
os.environ["LANGSMITH_PROJECT"] = "multi-agent-debug"

result = graph.invoke(input_state)
```

### 2. Log Routing Decisions

Add logging to routing nodes:

```python
def supervisor_node(state: SupervisorState) -> dict:
    decision = make_routing_decision(state)

    print(f"Supervisor routing to: {decision}")
    print(f"Current state: {len(state['messages'])} messages")
    print(f"Iteration: {state.get('iteration', 0)}")

    return {"next": decision}
```

### 3. Validate Graph Structure

```bash
# Detect common issues
uv run scripts/validate_agent_graph.py my_agent/graph.py:graph

# Check for:
# - Unreachable nodes
# - Infinite loops
# - Dead ends
```

### 4. Visualize Flow

```bash
# Generate diagram
uv run scripts/visualize_graph.py my_agent/graph.py:graph -o flow.md
```

## Performance Optimization

### Latency Optimization

**Supervisor Pattern:**
- Use faster models for routing (gpt-4o-mini)
- Cache routing decisions
- Implement early termination

**Router Pattern:**
- Use keyword matching for simple cases
- Cache routing for similar queries
- Avoid LLM calls when possible

**Orchestrator-Worker:**
- True parallelization already optimal
- Limit worker count to avoid rate limits
- Stream results to aggregator

**Handoffs:**
- Minimize context size
- Skip unnecessary handoffs
- Use cheaper models where appropriate

### Cost Optimization

**Token Usage:**
- Summarize context regularly
- Use structured output for reliability
- Employ cheaper models for simple tasks

**LLM Calls:**
- Cache routing decisions
- Use deterministic logic when possible
- Batch similar requests

**Pattern Selection:**
- Router < Handoffs < Orchestrator < Supervisor (cost)

## Testing Multi-Agent Patterns

### Unit Test Routing Logic

```python
def test_supervisor_routing():
    """Test supervisor routes correctly."""
    state = {
        "messages": [HumanMessage(content="Need research")],
        "next": "",
        "current_agent": ""
    }

    result = supervisor_node(state)
    assert result["next"] == "researcher"
```

### Integration Testing

```python
def test_full_workflow():
    """Test complete multi-agent workflow."""
    graph = create_supervisor_graph()

    result = graph.invoke({
        "messages": [HumanMessage(content="Write article about AI")]
    })

    # Verify agents were called in correct order
    assert "researcher" in result["agent_history"]
    assert "writer" in result["agent_history"]
```

### Test Graph Structure

```bash
# Validate before deployment
python3 scripts/validate_agent_graph.py graph.py:graph
```

## Migration Between Patterns

### Router to Supervisor

When routing logic becomes complex:

```python
# Before: Complex router
def route(query):
    if complex_rules(query):
        return category

# After: Supervisor with LLM
def supervisor(state):
    return llm_routing_decision(state)
```

### Handoffs to Supervisor

When need dynamic routing:

```python
# Before: Fixed sequence
Agent1 → Agent2 → Agent3

# After: Dynamic routing
Supervisor ⇄ Agent1/Agent2/Agent3
```

### Sequential to Parallel

When tasks become independent:

```python
# Before: Sequential
Agent1 → Agent2 → Agent3

# After: Parallel
Orchestrator → [Agent1, Agent2, Agent3] → Aggregator
```

## Common Use Cases

### Customer Support System

**Pattern:** Router + Supervisor
```
Router → Sales Supervisor → Sales Agents
     ↓
     Support Supervisor → Support Agents
```

### Research & Writing Pipeline

**Pattern:** Supervisor or Handoffs
```
Supervisor ⇄ Researcher
         ⇄ Writer
         ⇄ Editor
```

### Data Analysis Pipeline

**Pattern:** Orchestrator-Worker
```
Orchestrator → Data Collectors → Aggregator
```

### Document Processing

**Pattern:** Orchestrator-Worker + Supervisor
```
Router → PDF Orchestrator → Workers → Aggregator
     ↓
     DOCX Orchestrator → Workers → Aggregator
```

## Scripts Reference

### generate_supervisor_graph.py

Generate supervisor-subagent boilerplate:

```bash
uv run scripts/generate_supervisor_graph.py <name> [options]

Options:
  --subagents AGENTS    Comma-separated list (default: researcher,writer,reviewer)
  --output DIR          Output directory (default: current directory)
  --typescript          Generate TypeScript instead of Python
```

### validate_agent_graph.py

Validate graph structure:

```bash
uv run scripts/validate_agent_graph.py <module_path>

Format: path/to/module.py:graph_name

Checks:
  - Unreachable nodes
  - Cycles
  - Dead ends
  - Invalid routing
```

### visualize_graph.py

Generate Mermaid diagrams:

```bash
uv run scripts/visualize_graph.py <module_path> [options]

Options:
  --output FILE         Output file (default: stdout)
  --diagram-only        Skip documentation, output diagram only
```

## Troubleshooting

### "Agents not coordinating correctly"

**Check:**
1. State schema supports your pattern (see state-management-patterns.md)
2. Routing logic validates correctly
3. Context is preserved across agents

### "Infinite loops detected"

**Solutions:**
1. Add iteration counter to state
2. Implement max iteration limit
3. Add loop detection logic
4. Validate with validate_agent_graph.py

### "Poor routing decisions"

**Solutions:**
1. Improve supervisor prompt with clear agent descriptions
2. Use structured output for reliability
3. Add examples to routing prompt
4. Use better model for routing decisions

### "High latency"

**Solutions:**
1. Consider router pattern for simple cases
2. Use faster models for routing
3. Implement parallel execution where possible
4. Cache routing decisions

### "High token usage"

**Solutions:**
1. Summarize context regularly
2. Use cheaper models for simple tasks
3. Implement context windowing
4. Choose more efficient pattern

## Additional Resources

- **Pattern Details:**
  - Supervisor: references/supervisor-subagent.md
  - Router: references/router-pattern.md
  - Orchestrator-Worker: references/orchestrator-worker.md
  - Handoffs: references/handoffs.md

- **State Management:** references/state-management-patterns.md
- **Pattern Comparison:** references/pattern-comparison.md
- **Working Examples:** assets/examples/

- **LangGraph Documentation:**
  - Multi-Agent Patterns: https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant; https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs-customer-support; https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base
  - Conditional Edges: https://docs.langchain.com/oss/python/langgraph/graph-api
  - Map-Reduce: https://docs.langchain.com/oss/python/langgraph/graph-api#map-reduce-and-the-send-api
