---
name: orchestration
description: 'Coordinates skills, frameworks, and workflows throughout the project lifecycle using pattern-based sequencing, goal decomposition, phase-gate validation, and multi-agent orchestration. Use when starting multi-phase projects, sequencing frameworks, decomposing goals into capability plans, validating phase-gate readiness, coordinating subagents, or designing MCP-based tool orchestration.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Orchestration

## Overview

Coordinates skills, frameworks, and workflows across the project lifecycle. Combines pattern-based project classification with goal decomposition, hierarchical task planning, and multi-agent coordination.

Use this skill for project-level workflow decisions: which frameworks to activate, in what order, and how to validate progress between phases. For Claude Code-specific agent implementation details (agent configuration, batch sizing, prompt engineering), use the `agent-patterns` skill instead.

This skill does NOT replace project management tools. It provides the decision framework for sequencing capabilities and validating readiness at each transition point.

## Quick Reference

| Need                  | Action                                       |
| --------------------- | -------------------------------------------- |
| Identify project type | Classify as Pattern A / B / C                |
| Sequence frameworks   | Follow pattern-specific phase order          |
| Decompose a goal      | Extract required effects, match capabilities |
| Validate readiness    | Check phase-gate criteria before advancing   |
| Find alternatives     | Generate fallback capabilities per step      |
| Score a plan          | Evaluate cost, latency, risk, diversity      |
| Coordinate agents     | Select orchestration pattern for task type   |
| Pass context          | Use context distillation for subagents       |

## Pattern Identification

Classify every project before selecting frameworks or skills.

| Pattern               | Characteristics                                 | Timeline   |
| --------------------- | ----------------------------------------------- | ---------- |
| A: Simple Feature     | Existing system, well-understood, single-team   | 1-5 days   |
| B: New Product/System | From scratch, security/compliance matters       | 4-12 weeks |
| C: AI-Native/Complex  | AI agents, RAG, knowledge graphs, orchestration | 8-20 weeks |

## Phase Gates

Do not advance without meeting gate criteria.

| Gate              | Entry Criteria                                                        |
| ----------------- | --------------------------------------------------------------------- |
| Design (Phase 2)  | PRP complete, problem validated, success metrics, user stories        |
| Development (3)   | Architecture documented, data model designed, security threats mapped |
| Testing (Phase 4) | Features complete, unit tests over 80%, code review, SAST clean       |
| Deployment (5)    | All tests passing, UAT completed, security tested, coverage over 90%  |

## Scoring Function

Plans are evaluated using weighted utility:

| Factor    | Weight | Scores                                  |
| --------- | ------ | --------------------------------------- |
| Cost      | 0.3    | free=1.0, low=0.8, medium=0.5, high=0.2 |
| Risk      | 0.3    | safe=1.0, low=0.8, medium=0.5, high=0.2 |
| Latency   | 0.2    | instant=1.0, fast=0.7, slow=0.3         |
| Diversity | 0.2    | min(unique_domains / 5, 1.0)            |

Modifiers: recently used (within 3 steps) gets -30% penalty; novel capability gets +20% bonus.

## Multi-Agent Orchestration Patterns

| Pattern      | Use Case                                      |
| ------------ | --------------------------------------------- |
| Hierarchical | Parent delegates to specialized subagents     |
| Sequential   | Chain of experts (architect -> dev -> review) |
| Parallel     | Independent tasks running simultaneously      |
| Handoff      | One agent passes context to the next          |

Key rules: max delegation depth of 3, use context distillation (not full codebase), log all agent interactions.

## MCP Integration

MCP (Model Context Protocol) standardizes how agents connect to external tools, data sources, and prompt templates. The orchestrator discovers available MCP servers at startup and routes tool calls from subagents to the correct server.

| MCP Primitive | Role in Orchestration                                        |
| ------------- | ------------------------------------------------------------ |
| Resources     | Discover available data (schemas, configs, docs) before work |
| Tools         | Execute validated actions with typed arguments               |
| Prompts       | Reuse domain-specific instruction templates across agents    |
| Sampling      | Allow servers to request AI reasoning mid-execution          |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                                                  |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Treating all projects as Pattern A (simple feature) | Classify first: Pattern A (simple), B (new product), C (AI-native) before selecting frameworks   |
| Skipping phase gates to move faster                 | Enforce gate criteria before advancing; skipping causes compounding rework                       |
| Activating all available skills simultaneously      | Limit to 1-3 skills per phase with clear deliverables and handoffs                               |
| No decision logging for capability choices          | Log rationale, alternatives considered, scores, and rejection reasons at each step               |
| Building HTN plans without validating preconditions | Check project state (files, dependencies, env vars) against each capability's requirements first |
| Delegating without a clear objective manifest       | Every subagent needs an objective, constraints, max tokens, and available tools                  |
| Passing entire codebase to subagents                | Use context distillation to pass only relevant symbols and facts                                 |

## Delegation

- **Discover project pattern and classify scope**: Use `Explore` agent to survey the codebase, dependencies, and requirements
- **Execute multi-phase orchestration plan**: Use `Task` agent to implement phase-specific deliverables with gate validation
- **Design architecture and capability sequences**: Use `Plan` agent to decompose goals and build scored HTN plans

## References

- [goal-decomposition.md](references/goal-decomposition.md) -- HTN planning, goal analysis, capability matching, precondition validation, scoring, decision logging
- [project-patterns.md](references/project-patterns.md) -- Pattern A/B/C classification, phase sequences, skill coordination by phase, parallelization
- [multi-agent-coordination.md](references/multi-agent-coordination.md) -- Hierarchical, sequential, parallel orchestration patterns, delegation manifests, recursion limits
- [mcp-orchestration.md](references/mcp-orchestration.md) -- MCP architecture, resources, tools, prompts, multi-server orchestration, bidirectional sampling
- [context-distillation.md](references/context-distillation.md) -- Symbol indexing, fact extraction, recursive context reduction, token management
- [error-handling.md](references/error-handling.md) -- Objective drift, tool failure, context overflow, circuit breakers, recovery strategies, logging
