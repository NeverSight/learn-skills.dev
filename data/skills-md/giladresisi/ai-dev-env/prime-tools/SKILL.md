---
name: prime-tools
description: Use when about to build or modify agent tools and needing to load tool docstring patterns and best practices first
---

# Prime for Tool Development

Load tool development patterns from Module 3 to prepare for building agent tools.

## Context

You are about to work on building or modifying agent tools that will be used by Pydantic AI agents. Load the comprehensive patterns and best practices we established in Module 3 for writing agent-optimized tool docstrings.

## Read

Read the tool docstring patterns: @.agents/reference/adding_tools_guide.md

## Process

Understand and internalize:

1. **Core Philosophy** - How agent tool docstrings differ from standard docstrings
2. **7 Required Elements** - One-line summary, "Use this when", "Do NOT use", Args with guidance, Returns, Performance Notes, Examples
3. **Agent Perspective** - Writing for LLM comprehension and tool selection
4. **Token Efficiency** - Documenting token costs and optimization strategies
5. **Anti-patterns** - Common mistakes that confuse agents
6. **Template Structure** - The exact format to follow

Pay special attention to:

- "Use this when" (affirmative guidance for tool selection)
- "Do NOT use" (negative guidance to prevent tool confusion)
- Performance Notes (token costs, execution time, limits)
- Realistic examples (not "foo", "bar", "test.md")

## Report Back

Provide a concise summary with:

### Key Principles (5 bullets max)

- [What are the core principles you understood?]

### Critical Distinctions

- [What makes agent tool docstrings different from standard docstrings?]
- [Why does "Do NOT use" matter?]

### Template Internalized

- [Confirm you understand the structure you'll follow]

### Ready to Apply

- [One sentence confirming you're ready to write agent-optimized tool docstrings]

Keep it scannable - I want to verify understanding in 30 seconds.