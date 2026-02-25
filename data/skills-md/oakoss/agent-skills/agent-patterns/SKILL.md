---
name: agent-patterns
description: |
  Multi-agent design patterns for Claude Code and AI development systems. Covers custom subagents, built-in subagents (Explore/Plan/General-purpose), fungible vs specialized agents, delegation, orchestration, batch workflows, context hygiene, and failure recovery.

  Use when: designing multi-agent systems, creating custom subagents, delegating bulk operations, orchestrating parallel work, choosing between fungible and specialized agents, configuring agent frontmatter, or debugging agent coordination issues.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://code.claude.com/docs/en/sub-agents
user-invocable: false
---

# Agent Patterns

Multi-agent design, delegation, and orchestration in Claude Code and AI-assisted development. Default to fungible agents for large-scale software dev; use specialized agents only for peer review or discourse-based workflows.

Subagents in Claude Code are specialized AI assistants that run in isolated context windows with custom system prompts, specific tool access, and independent permissions. They preserve main conversation context by keeping exploration, test runs, and verbose operations out of the primary thread.

Key constraint: subagents cannot spawn other subagents. Multi-step orchestration requires chaining subagents from the main conversation.

## Quick Reference

| Pattern                   | Description                                       | When to Use                                  |
| ------------------------- | ------------------------------------------------- | -------------------------------------------- |
| Fungible swarm            | Identical agents pick tasks from a shared board   | Large-scale software dev, resilient systems  |
| Sequential pipeline       | Each agent builds on previous output              | Multi-step workflows with clear dependencies |
| Hierarchical              | Manager decomposes, workers execute in parallel   | Complex tasks with independent subtasks      |
| Peer collaboration        | Agents iterate until consensus                    | Code review, quality-critical outputs        |
| Orchestrator delegation   | Main conversation chains subagents                | Multi-phase workflows, parallel specialists  |
| Two-stage review          | Spec compliance check, then code quality check    | High-stakes code, complex requirements       |
| Question-first delegation | Agent asks clarifying questions before proceeding | Ambiguous tasks, expensive-to-redo work      |
| Review loop enforcement   | Fix-review cycle with max iteration escalation    | Any review workflow needing convergence      |

| Built-in Subagent | Model    | Tools     | Purpose                                           |
| ----------------- | -------- | --------- | ------------------------------------------------- |
| Explore           | Haiku    | Read-only | File discovery, code search, codebase exploration |
| Plan              | Inherits | Read-only | Codebase research during plan mode                |
| General-purpose   | Inherits | All tools | Complex research, multi-step operations           |
| Bash              | Inherits | Terminal  | Running terminal commands in separate context     |
| Claude Code Guide | Haiku    | Read-only | Answering questions about Claude Code features    |

| Configuration            | Value                                                                             |
| ------------------------ | --------------------------------------------------------------------------------- |
| Custom agent location    | `.claude/agents/*.md` (project), `~/.claude/agents/*.md` (user)                   |
| CLI agents               | `--agents '{...}'` (session only, JSON format)                                    |
| Plugin agents            | Plugin `agents/` directory (lowest priority)                                      |
| Required fields          | `name`, `description`                                                             |
| Optional fields          | `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `hooks`, `color` |
| Model values             | `sonnet`, `opus`, `haiku`, `inherit` (default)                                    |
| Permission modes         | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`                  |
| Nesting limit            | Subagents cannot spawn other subagents (one level only)                           |
| Foreground vs background | Foreground blocks main conversation; background runs concurrently                 |
| Batch size               | 5-8 items per agent (standard tasks)                                              |
| Parallel agents          | 2-4 simultaneously                                                                |

## When to Use Subagents vs Main Conversation

| Use Subagents When                                              | Use Main Conversation When                                 |
| --------------------------------------------------------------- | ---------------------------------------------------------- |
| Task produces verbose output (test suites, logs, API responses) | Task needs frequent back-and-forth or iterative refinement |
| Enforcing specific tool restrictions or permissions             | Multiple phases share significant context                  |
| Work is self-contained and can return a summary                 | Making a quick, targeted change                            |
| Parallel independent research paths                             | Latency matters (subagents start fresh and gather context) |

## Tool Access Patterns

| Agent Role         | Recommended Tools                       | Rationale                                     |
| ------------------ | --------------------------------------- | --------------------------------------------- |
| Read-only reviewer | `Read, Grep, Glob`                      | Cannot modify code; safe for audits           |
| File creator       | `Read, Write, Edit, Glob, Grep`         | NO Bash; avoids heredoc approval spam         |
| Script runner      | `Read, Write, Edit, Glob, Grep, Bash`   | Full access for build/deploy tasks            |
| Research agent     | `Read, Grep, Glob, WebFetch, WebSearch` | External data access for documentation lookup |

Subagents inherit all tools by default (including MCP tools). Use `tools` as an allowlist or `disallowedTools` as a denylist to restrict access. MCP tools are not available in background subagents.

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                                            |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Expecting subagents to spawn sub-subagents                  | Subagents cannot nest; chain subagents from the main conversation instead                                  |
| Giving Bash tool to agents that only create files           | Use Write and Edit tools only; Bash causes approval spam from heredoc usage                                |
| Omitting `disallowedTools` for sensitive operations         | Use `disallowedTools` to explicitly deny dangerous tools even when inheriting                              |
| Spawning too many agents (5+) for a small task              | Start with 2-3 agents; coordination overhead outweighs benefit at higher counts                            |
| Burying critical instructions past line 300 of agent prompt | Put critical rules immediately after frontmatter; models deprioritize late instructions                    |
| Using specialized agents for large-scale software dev       | Use fungible agents with a shared task board; specialized agents create single points of failure           |
| Not including "FIX issues found" in delegation prompts      | Without explicit action directive, agents only report problems without making changes                      |
| Setting model to Haiku for content generation               | Default to Sonnet; Haiku only for script execution, fast lookups, or pass/fail checks                      |
| Not writing clear descriptions for custom agents            | Claude uses the `description` field to decide when to auto-delegate; vague descriptions prevent delegation |
| Using MCP tools in background subagents                     | MCP tools are not available in background subagents; run in foreground instead                             |
| Not preloading skills into subagents                        | Subagents do not inherit skills from the parent; list them explicitly in the `skills` field                |

## Delegation

- **Explore codebase before designing agent prompts**: Claude auto-delegates to the built-in Explore subagent (Haiku, read-only) for file discovery and code search; supports quick, medium, and very thorough modes
- **Plan multi-agent architecture for complex projects**: Use plan mode; Claude delegates research to the Plan subagent before presenting a plan
- **Execute batch operations across many files**: Chain General-purpose subagents from the main conversation with identical prompts and non-overlapping item lists
- **Isolate high-volume operations**: Delegate test runs, log processing, or doc fetching to subagents to keep verbose output out of your main context
- **Run parallel research**: Spawn multiple subagents simultaneously for independent investigations; Claude synthesizes findings when all complete
- **Resume interrupted work**: Ask Claude to continue a previous subagent; resumed agents retain full conversation history including tool calls and reasoning

> For project-level workflow sequencing, phase-gate validation, goal decomposition, and capability scoring, use the `orchestration` skill.

## References

- [Agent types and design patterns](references/agent-types.md)
- [Delegation patterns and batch workflows](references/delegation-patterns.md)
- [Sub-agent configuration and prompt engineering](references/sub-agent-configuration.md)
- [Communication and orchestration patterns](references/orchestration.md)
- [Troubleshooting and anti-patterns](references/troubleshooting.md)
