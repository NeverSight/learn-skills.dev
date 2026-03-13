---
name: architect-workflow
description: "Deterministic AI engineering workflow with multi-agent teams. Triggers: architect mode, consistency sweep, pipeline audit, team workflow"
---

# Architect Workflow

Professional team-based workflows for AI software engineering. Includes deterministic planning frameworks, consistency verification, and pipeline auditing.

## What's Included

### 1. Architect Mode (Command + Team)
A 6-phase framework for rigorous software engineering:
- **Phase 1-2**: Deconstruction & Research (no code)
- **Phase 3-4**: Planning & Approval gates
- **Phase 5**: Delegated implementation with enforced review loops
- **Phase 6**: Integration & completion report

Use when: Complex features, architectural changes, anything >3 files

**Trigger**: `/architect-workflow [goal]`

### 2. Consistency Sweep Team
4 specialized agents verify docs, config, and architecture stay in sync:
- **Docs Verifier**: Compare documentation against actual code
- **Dashboard Verifier**: Match UI components to backend config
- **Config Verifier**: Validate defaults, constants, schemas
- **Architecture Verifier**: Check structural docs match reality

Use when: After major refactors, before releases, maintaining large codebases

### 3. Pipeline Health Team
4 auditors investigate content generation pipelines for bugs and performance:
- **Draft Phase Auditor**: End-to-end draft flow analysis
- **Critique Phase Auditor**: Critique/re-draft loop verification
- **Validator Auditor**: Check validators and enforcers
- **Orchestration Auditor**: State machine and phase coordination

Use when: Debugging complex pipelines, performance tuning, quality audits

## Installation

This skill installs files to:
- `.claude/commands/architect-workflow.md` - The /architect-workflow command
- `.claude/teams/architect.md` - Architect Mode team workflow
- `.claude/teams/consistency-sweep.md` - Consistency verification team
- `.claude/teams/pipeline-perf.md` - Pipeline health audit team

## Quick Start

After installation:

```bash
# Launch architect mode
/architect-workflow "Add user authentication with JWT tokens"

# Or paste team definitions directly into Claude
# See team files in .claude/teams/
```

## Architect Mode Process

1. **Deconstruct**: Break down goals into objectives + research questions
2. **Research**: Spawn parallel Explore agents for codebase investigation
3. **Plan**: Write PLAN.md with tasks, sandboxes, success criteria
4. **Approve**: User reviews plan before any code is written
5. **Execute**: Implementers (Opus) + Reviewers (Sonnet) with accept/reject loops
6. **Integrate**: Final checks, cleanup temp files, completion report

**Key Feature**: NO CODE until Phase 5 approval - prevents "ready, fire, aim" loops

## Team Scaling

| Scope | Researchers | Implementers | Reviewers |
|-------|-------------|--------------|-----------|
| Small (≤3 files) | Skip (Quick Mode) | 1 Opus | 1 Sonnet |
| Medium (4-10 files) | 2 Explore | 2-3 Opus | 1 Sonnet |
| Large (10+ files) | 3 Explore | 3-4 Opus | 1-2 Sonnet |

## When to Use What

**Architect Mode**: Building new features, refactoring, architectural changes
**Consistency Sweep**: Post-refactor verification, release prep, doc maintenance
**Pipeline Health**: Debugging multi-stage flows, performance investigation, quality audits

## Philosophy

These workflows enforce discipline:
- Research before planning
- Planning before implementation
- Review before merging
- Measurable success criteria
- Explicit file sandboxes
- No code outside scope

Result: Higher quality, fewer bugs, better architecture decisions.
