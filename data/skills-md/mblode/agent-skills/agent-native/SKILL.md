---
name: agent-native
description: Designs agent-native applications where agents are first-class citizens with full tool parity, atomic primitives, and explicit completion signals. Covers tool design, context injection, agent-to-UI communication, and mobile checkpoint/resume patterns. Use when architecting an agentic system, designing tool surfaces, building agent-aware UI, implementing context.md patterns, or asking "how do I make my app agent-native."
---

# Agent-Native

Agent-native applications treat agents as first-class users. Whatever a human can do through the UI, an agent can achieve through tools. Features are outcomes described in prompts, achieved by an agent with atomic tools, operating in a loop until done.

## Reference Files

| File | Read When |
|------|-----------|
| `references/core-principles.md` | Default: understanding Parity, Granularity, Composability, and Emergent Capability |
| `references/tool-design.md` | Designing tools — atomic primitives, CRUD, domain tools, dynamic discovery |
| `references/files-and-context.md` | State management — entity directories, context.md, context injection, files vs database |
| `references/agent-ui-communication.md` | Building agent feedback — completion signals, partial completion, event types |
| `references/mobile-specifics.md` | iOS/mobile — checkpoint/resume, iCloud storage, background execution |

## Core Principles

- **Parity** — Agent can achieve anything users can do through the UI. Build a capability map; close every gap.
- **Granularity** — Tools are atomic primitives. Judgment and decision logic live in prompts, not tool implementations. To change behavior, edit prose, not code.
- **Composability** — New features = new prompts. With atomic tools and parity, you describe an outcome and the agent loops until it's achieved.
- **Emergent capability** — The agent handles requests you didn't design for. Observe what users ask; formalize patterns that emerge.
- **Improvement over time** — State persists via context files. Prompts can be updated for all users without shipping code.

## Design Workflow

1. **Capability audit** — Map every UI action to an agent equivalent. Close any gap. Read `core-principles.md`.
2. **Tool surface design** — Define atomic primitives for every entity (CRUD). Add domain tools only for vocabulary, guardrails, or efficiency. Read `tool-design.md`.
3. **Context and state planning** — Design the `context.md` file, entity directory structure, and system prompt injection. Read `files-and-context.md`.
4. **Agent-UI feedback design** — Define completion signals, event types, shared workspace, and approval gates. Read `agent-ui-communication.md`.
5. **Validate** — Run the checklist below. Describe an unbuilt outcome and test whether the agent can figure it out.

## Design Checklist

Copy and track during design:

```text
Agent-native design progress:
- [ ] Capability map: every UI action has an agent equivalent
- [ ] Tools are atomic primitives (judgment in prompts, not tools)
- [ ] Every entity has full CRUD tool coverage
- [ ] System prompt injects available resources and capabilities
- [ ] Agents and users share the same data space
- [ ] Agent actions reflect immediately in UI
- [ ] Completion is signaled explicitly (no heuristic detection)
- [ ] External APIs use dynamic capability discovery where possible
- [ ] Approval model matches stakes and reversibility
- [ ] Ultimate test: describe an unbuilt outcome — can the agent figure it out?
```

## Validation Loop

Before shipping, verify:

1. **Capability coverage** — Pick 5 random UI actions; confirm the agent can accomplish each without touching code.
2. **Tool atomicity** — Review every tool; if it contains `if/else` decision logic, split it.
3. **Context completeness** — Clear the agent's context and start a session; does it still know what exists?
4. **End-to-end scenario** — Give the agent an outcome you never explicitly built. Does it compose tools to get there?

## Anti-Patterns

- **Agent as router** — Agent routes to your code instead of acting with judgment; you've built a dispatcher, not an agent.
- **Workflow-shaped tools** — `analyze_and_organize` bundles decision logic into a tool; break into `read_file`, `move_file`, `write_file`.
- **Orphan UI actions** — User can do something the agent can't; breaks parity.
- **Context starvation** — Agent doesn't know what exists; inject resources and capabilities into every system prompt.
- **Gates without reason** — Domain tool is the only path when primitives should also work; default to open.
- **Heuristic completion detection** — Detecting done via consecutive idle iterations; require an explicit completion tool call.
- **Static API mapping** — 50 tools for 50 endpoints; use discover + access instead.

## Related Skills

- `define-architecture` — repo structure and module boundaries before going agent-native
- `agents-md` — audit CLAUDE.md / AGENTS.md for agent instruction quality
