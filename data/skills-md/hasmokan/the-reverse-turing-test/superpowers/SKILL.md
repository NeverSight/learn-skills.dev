---
name: superpowers
description: Agent development workflow and discipline skills. Use when developing features, debugging issues, managing code branches, writing plans, or ensuring code quality through TDD and systematic processes. Triggers on any software development task that benefits from structured workflows.
license: MIT
metadata:
  author: jesse
  version: "1.0.0"
---

# Superpowers - Agent Development Workflows

Comprehensive agent development skill collection optimized for AI-assisted coding workflows. Contains 14 skills across 5 categories, prioritized by workflow stage to guide development from ideation to completion.

## When to Apply

Reference these skills when:
- Starting a new feature or project (brainstorming, writing-plans)
- Debugging any issue (systematic-debugging)
- Writing or modifying code (test-driven-development)
- Managing branches and isolation (using-git-worktrees)
- Completing and integrating work (finishing-a-development-branch)
- Receiving or requesting code review (receiving-code-review, requesting-code-review)

## Skill Categories by Workflow Stage

| Stage | Category | Skills | Priority |
|-------|----------|--------|----------|
| 1 | Ideation & Planning | `brainstorming`, `writing-plans` | CRITICAL |
| 2 | Implementation | `test-driven-development`, `subagent-driven-development`, `executing-plans` | CRITICAL |
| 3 | Debugging | `systematic-debugging` | HIGH |
| 4 | Code Review | `requesting-code-review`, `receiving-code-review` | HIGH |
| 5 | Completion | `verification-before-completion`, `finishing-a-development-branch` | HIGH |
| 6 | Utilities | `using-git-worktrees`, `dispatching-parallel-agents`, `using-superpowers`, `writing-skills` | MEDIUM |

## Quick Reference

### 1. Ideation & Planning (CRITICAL)

- `brainstorming` - Collaborative design exploration before implementation
- `writing-plans` - Create detailed implementation plans with bite-sized tasks

### 2. Implementation (CRITICAL)

- `test-driven-development` - RED-GREEN-REFACTOR cycle for all code
- `subagent-driven-development` - Execute plans with fresh subagent per task
- `executing-plans` - Batch execution with checkpoints in separate session

### 3. Debugging (HIGH)

- `systematic-debugging` - Four-phase root cause investigation before fixes

### 4. Code Review (HIGH)

- `requesting-code-review` - Dispatch code reviewer subagent after implementation
- `receiving-code-review` - Technical evaluation, not performative agreement

### 5. Completion (HIGH)

- `verification-before-completion` - Evidence before claims, always
- `finishing-a-development-branch` - Merge, PR, keep, or discard options

### 6. Utilities (MEDIUM)

- `using-git-worktrees` - Isolated workspaces for parallel development
- `dispatching-parallel-agents` - One agent per independent problem domain
- `using-superpowers` - How to find and invoke skills
- `writing-skills` - TDD applied to process documentation

## Core Principles

Each skill enforces key discipline principles:

| Principle | Skills | Iron Law |
|-----------|--------|----------|
| **Test First** | `test-driven-development` | No production code without failing test |
| **Root Cause First** | `systematic-debugging` | No fixes without investigation |
| **Evidence First** | `verification-before-completion` | No claims without verification |
| **Plan First** | `brainstorming`, `writing-plans` | No code without design |

## How to Use

Read individual skill files for detailed instructions:

```
brainstorming/SKILL.md
test-driven-development/SKILL.md
systematic-debugging/SKILL.md
```

Each skill file contains:
- Overview and core principle
- When to use (and when NOT to)
- Step-by-step process
- Common mistakes and red flags
- Integration with other skills

## Full Compiled Document

For the complete guide with all skills expanded: `AGENTS.md`
