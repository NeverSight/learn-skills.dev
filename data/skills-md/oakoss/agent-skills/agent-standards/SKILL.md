---
name: agent-standards
description: 'Defines behavioral and cognitive standards for senior AI engineering agents. Use when configuring agent reasoning protocols, memory management, or context engineering strategies. Use for autonomous reasoning, tiered memory systems, verifiable goal execution, multi-agent orchestration, and token optimization.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Expert Instruction

## Overview

Foundational meta-skill that defines behavioral and cognitive standards for senior AI engineering agents. Establishes the reasoning pipeline, memory architecture, and context engineering practices that enable autonomous, long-horizon task execution with verifiable outcomes.

**When to use:** Configuring agent reasoning, managing context windows, establishing verification protocols, orchestrating multi-agent workflows, optimizing token usage.

**When NOT to use:** Domain-specific coding tasks (use specialized skills), UI/UX design, database schema work.

## Quick Reference

| Pattern                | Approach                                      | Key Points                                     |
| ---------------------- | --------------------------------------------- | ---------------------------------------------- |
| Perception             | Analyze terminal output, codebase, traces     | High-fidelity input ingestion                  |
| Hypothesis             | Generate multiple solution paths              | Evaluate before committing                     |
| Simulation             | Reason through change consequences            | Predict side effects                           |
| Action                 | Precise tool execution                        | Atomic, testable commits                       |
| Criticism              | Self-audit output                             | Check for bugs and style violations            |
| Context discovery      | Map framework versions and patterns           | Always discover before implementing            |
| Dependency audit       | Check existing tools before adding new ones   | Avoid unnecessary dependencies                 |
| Verifiable planning    | Define Definition of Done                     | Test pass, build success, or user approval     |
| Interactive alignment  | Ask the user for ambiguous requirements       | Confirm critical architectural decisions       |
| Atomic implementation  | Apply changes in logical, testable units      | Each commit should be independently verifiable |
| Audit and cleanup      | Run linter, remove debug artifacts            | No temporary code in final output              |
| Selective reading      | Use offset and limit parameters               | Avoid reading entire large files               |
| Symbol search          | Use grep/rg to find definitions               | Do not read entire directories                 |
| Few-shot anchoring     | Provide canonical examples                    | More effective than long rule lists            |
| Memory tiering         | Short-term, mid-term, long-term               | Match persistence to information lifetime      |
| Context packing        | Bundle related files                          | Structured markdown artifacts                  |
| Noise reduction        | Exclude node_modules, dist, binary artifacts  | Maximize signal-to-noise ratio in context      |
| Semantic summarization | Condense long logs into actionable facts      | Single-sentence failure descriptions           |
| Cognitive load pruning | Remove irrelevant history from active context | Free tokens for current task reasoning         |

## Common Mistakes

| Mistake                                                | Correct Pattern                                                                   |
| ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Failing silently when a tool call or build step errors | Always report status and errors explicitly to the user                            |
| Inventing APIs or methods that do not exist            | Search documentation or use web search to verify API signatures before using them |
| Writing verbose explanations instead of showing code   | Prioritize code-first communication; explain only when asked                      |
| Ignoring surrounding code style and conventions        | Mimic the existing codebase patterns, naming, and formatting                      |
| Hardcoding secrets or API keys in source files         | Use environment variables and `.env` file mapping                                 |
| Reading entire directories to find a single symbol     | Use grep or rg to locate definitions, then read only relevant sections            |
| Skipping verification after implementation             | Every task must have a verification signal before marking complete                |
| Storing sensitive data in memory or context files      | Run a secret scrub before persisting any memory vector                            |
| Loading full file contents into context unnecessarily  | Use partial reads with offset and limit for large files                           |
| Including duplicate information from multiple sources  | Deduplicate context to preserve token budget                                      |

## Delegation

- **Explore a codebase to map framework versions and active patterns**: Use `Explore` agent
- **Execute a complex multi-step implementation with atomic commits**: Use `Task` agent
- **Plan architecture for a long-horizon feature with dependency analysis**: Use `Plan` agent

## References

- [Cognitive architecture, reasoning stack, multi-agent orchestration, and cognitive load management](references/cognitive-architecture.md)
- [Tiered memory systems, short-term to long-term persistence, and shared memory](references/memory-systems.md)
- [Agent communication protocols including MCP, A2A, and ACP standards](references/agent-protocols.md)
- [Context engineering, token optimization, information hierarchy, and structured packing](references/context-engineering.md)
