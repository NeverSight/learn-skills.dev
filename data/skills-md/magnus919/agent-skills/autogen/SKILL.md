---
name: autogen
description: >-
  Build conversational multi-agent systems with Microsoft AutoGen. AssistantAgent,
  UserProxyAgent, GroupChat, code execution, nested chats, cancellation tokens, tool
  integration, and MCP support. Use when building conversation-driven multi-agent systems
  or comparing agent frameworks. Do not use this skill for unrelated requests; route to
  the nearest named specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.1.0
  source: https://microsoft.github.io/autogen
---

# AutoGen Expert Skill

AutoGen (by Microsoft Research) is a framework for **conversational multi-agent AI**. Unlike LangGraph's explicit graph topology or CrewAI's role-based crews, AutoGen uses **agent-to-agent conversations as the orchestration primitive**. Agents communicate through structured chat, with built-in patterns for nested conversations, group chat with routing, and code execution.

## Core Paradigm

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    model_client=model_client,
)
```

> **⚠️ UserProxyAgent is NOT a human user.** It is an automated proxy that can execute code. Despite the name, it runs autonomously unless `human_input_mode` is set to `ALWAYS`.

## Core Principles

1. **Conversations are the orchestration primitive.** Agents send messages, receive replies, and the conversation structure determines the workflow.
2. **UserProxyAgent is a code executor, not a human.** Despite the name, it runs autonomously by default. Set `human_input_mode="ALWAYS"` for actual human-in-the-loop.
3. **GroupChat routes between agents.** RoundRobinGroupChat cycles fixed-order. SelectorGroupChat uses an LLM to pick the next speaker.
4. **Nested chats delegate work.** An agent can spawn a sub-conversation between specialist agents and return the result.
5. **Docker is the safe code execution mode.** Local code execution (`LocalCommandLineCodeExecutor`) runs LLM-generated code on your machine — use Docker in production.
6. **Cancellation tokens stop runaway agents.** Always pass `CancellationToken` for long-running tasks.

## Where to Start

| You already have... | Start here |
|---|---|
| Nothing — exploring AutoGen | Create a two-agent chat (Assistant + UserProxy) |
| Agents that need to coordinate | Build a GroupChat with multiple agents |
| Agents that need code execution | Configure Docker code executor |
| A complex multi-step task | Use nested chats for sub-tasks |

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Two-agent chat | AssistantAgent + UserProxyAgent | `references/agent-types.md` |
| Multi-agent group | GroupChat with RoundRobinGroupChat | `references/group-chat.md` |
| Code execution | DockerCommandLineCodeExecutor | `references/code-execution.md` |
| Tool integration | `register_function()` or @tool | `references/tool-integration.md` |
| Nested chat | `initiate_chat()` from within a tool | `references/conversation-patterns.md` |
| Cancellation | `CancellationToken` | `references/conversation-patterns.md` |
| MCP tools | `McpWorkbench` | `references/tool-integration.md` |

## Framework Routing Guide

| Scenario | Reach for | Why |
|----------|-----------|-----|
| Conversation-driven multi-agent | **AutoGen** | Native agent-to-agent chat as orchestration |
| Role-based multi-agent teams | **CrewAI** | Role/Goal/Backstory is the native abstraction |
| State-machine multi-agent | **LangGraph** | Graph topology, subgraphs, human-in-the-loop |
| Chain/agent composition | **LangChain** | LCEL pipe operator for general chains |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Agent Types | AssistantAgent, UserProxyAgent | `references/agent-types.md` |
| Conversation Patterns | Send/receive, nested chats, cancellation | `references/conversation-patterns.md` |
| Group Chat | RoundRobin, Selector, MagenticOne | `references/group-chat.md` |
| Code Execution | Docker, local, cancellation tokens | `references/code-execution.md` |
| Tool Integration | register_function, @tool, MCP integration | `references/tool-integration.md` |
| v0.4 Migration | v0.2->v0.4 migration, AgentTool, streaming, termination | `references/v04-migration.md` |
| Validation Audit | Research validation of all API claims | `references/validation-audit.md` |
| FAQ & Troubleshooting | Common errors and fixes | `references/faq-and-troubleshooting.md` |

## Templates

| Template | When to use | File |
|----------|-------------|------|
| Two-Agent Chat | Simple assistant + code executor | `templates/two-agent-chat.py` |
| Group Chat | Multi-agent team with speaker routing | `templates/group-chat.py` |
| Code Execution Agent | Agent with Docker code execution | `templates/code-execution.py` |

## Troubleshooting

| Symptom | Likely cause | Fix | Reference |
|---------|-------------|-----|-----------|
| Agent loops forever | No termination condition | Add `is_termination_msg` or `max_turns` | `references/conversation-patterns.md` |
| Code execution fails | Docker not running | Start Docker or use LocalCommandLineCodeExecutor | `references/code-execution.md` |
| Nested chat never returns | Cancellation token not passed | Pass `CancellationToken` with timeout | `references/conversation-patterns.md` |
| v0.2 code doesn't work | v0.4 API changed | Follow migration guide | `references/faq-and-troubleshooting.md` |
| GroupChat speaker selection loops | SelectorGroupChat with no clear next | Use RoundRobinGroupChat for fixed order | `references/group-chat.md` |
| UserProxyAgent asking for input | `human_input_mode="ALWAYS"` | Set to `"NEVER"` for automated execution | `references/agent-types.md` |

## When NOT to Use AutoGen

- Simple single-agent task — overkill, use direct API call
- Need fine-grained graph control — use LangGraph
- Need role-based teams with fixed processes — use CrewAI
- Need chain composition — use LangChain LCEL
