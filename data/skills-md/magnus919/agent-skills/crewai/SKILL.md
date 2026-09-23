---
name: crewai
description: >-
  Build role-based multi-agent systems with CrewAI. Agents with Role/Goal/Backstory, task
  design, crew composition (sequential or hierarchical), tool integration, callbacks, and
  production deployment. Use when orchestrating multi-agent teams or comparing agent
  frameworks. Do not use this skill for unrelated requests; route to the nearest named
  specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.1.0
  source: https://docs.crewai.com
---

# CrewAI Expert Skill

CrewAI is a framework for **role-based multi-agent orchestration**. Unlike LangGraph's low-level state-machine graphs, CrewAI provides a higher abstraction: agents are defined as Roles with Goals and Backstories, crews are composed with built-in sequential or hierarchical workflows, and inter-agent delegation is built into the framework.

## Core Paradigm

```python
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

@tool("search")
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

researcher = Agent(
    role="Senior Researcher",
    goal="Find accurate information on any topic",
    backstory="Expert researcher with 10 years of experience",
    tools=[search_web],
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Write clear reports from research findings",
    backstory="Experienced technical writer",
    verbose=True,
)

research_task = Task(
    description="Research the topic thoroughly",
    expected_output="A detailed research brief",
    agent=researcher,
)

write_task = Task(
    description="Write a report based on research",
    expected_output="A well-structured report",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
```

## Core Principles

1. **Agents are Roles, not functions.** Role + Goal + Backstory defines the agent's identity. Strong role definitions reduce hallucination.
2. **Tasks declare what, not how.** Description + expected_output defines the task. The agent figures out execution.
3. **Sequential is for pipelines, Hierarchical is for complexity.** Sequential runs tasks in order. Hierarchical uses a manager agent to delegate and validate.
4. **Manager LLM is required for Hierarchical.** Without `manager_llm`, hierarchical process fails silently.
5. **Delegation loops are real.** `allow_delegation=True` without `max_iter` bounds can cause infinite handoffs.
6. **Tool errors don't raise.** A failed tool call marks the task as failed but doesn't raise an exception. Check task output.

## Where to Start

| You already have... | Start here |
|---|---|
| Nothing — exploring CrewAI | Sequential crew with 2 agents (research → write) |
| Agents you want to coordinate | Build a Hierarchical crew with manager_llm |
| Tools you want to integrate | Use @tool decorator, add tools to relevant agents |
| A production deployment | Add callbacks, memory, error handling |

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Define agent | `Agent(role, goal, backstory)` | `references/agent-design.md` |
| Define task | `Task(description, expected_output, agent)` | `references/task-design.md` |
| Sequential crew | `Crew(process=Process.sequential)` | `references/crew-patterns.md` |
| Hierarchical crew | `Crew(process=Process.hierarchical, manager_llm=...)` | `references/crew-patterns.md` |
| Create tool | `@tool("name")` decorator | `references/tool-integration.md` |
| Add callbacks | `step_callback=fn` on Agent | `references/callbacks.md` |
| Enable memory | `memory=True` on Crew or Agent | `references/crew-patterns.md` |

## Framework Routing Guide

| Scenario | Reach for | Why |
|----------|-----------|-----|
| Role-based multi-agent teams | **CrewAI** | Role/Goal/Backstory is the native abstraction |
| State-machine multi-agent | **LangGraph** | Graph topology, subgraphs, human-in-the-loop |
| Conversational multi-agent | **AutoGen** | Agent chat as orchestration primitive |
| Chain/agent composition | **LangChain** | LCEL pipe operator for general chains |
| Documents to query / RAG | **LlamaIndex** | Data ingestion is the primary primitive |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Agent Design | Defining agents with roles, goals, backstories | `references/agent-design.md` |
| Task Design | Creating tasks with descriptions and outputs | `references/task-design.md` |
| Crew Patterns | Sequential, hierarchical, consensual crews | `references/crew-patterns.md` |
| Tool Integration | Creating tools with @tool decorator | `references/tool-integration.md` |
| Callbacks | Monitoring agent and task execution | `references/callbacks.md` |
| Memory System | Unified Memory class, cross-agent context | `references/memory-system.md` |
| Flows | Event-driven orchestration connecting crews | `references/flows.md` |
| FAQ & Troubleshooting | Common errors and fixes | `references/faq-and-troubleshooting.md` |

## Templates

| Template | When to use | File |
|----------|-------------|------|
| Research Crew | Sequential: researcher → writer → reviewer | `templates/research-crew.py` |
| Hierarchical Crew | Manager with specialist agents | `templates/hierarchical-crew.py` |
| Customer Support | Triage → specialist → response | `templates/support-crew.py` |

## Troubleshooting

| Symptom | Likely cause | Fix | Reference |
|---------|-------------|-----|-----------|
| Crew runs but no output | Agent stuck in delegation loop | Set `max_iter=15` on agent | `references/agent-design.md` |
| Hierarchical crew fails | No `manager_llm` set | Add `manager_llm=ChatOpenAI(model="gpt-4")` | `references/crew-patterns.md` |
| Task never completes | Agent exceeds max_iter | Increase `max_iter` or simplify task | `references/agent-design.md` |
| Tool not being called | Tool not added to agent | Add `tools=[my_tool]` to Agent definition | `references/tool-integration.md` |
| High token usage | Hierarchical mode | Manager processes all outputs — use cheaper LLM | `references/crew-patterns.md` |
| Memory between tasks not working | Crew-level memory not set | Add `memory=True` to Crew | `references/crew-patterns.md` |

## When NOT to Use CrewAI

- Single-agent task — too much abstraction for one agent
- Need fine-grained graph control (cycles, conditional branching) — use LangGraph
- Need conversational agent interactions — use AutoGen
- Need simple chain composition — use LangChain LCEL
