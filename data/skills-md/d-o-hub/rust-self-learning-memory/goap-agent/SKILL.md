---
name: goap-agent
description: Invoke for complex multi-step tasks requiring intelligent planning and multi-agent coordination. Use when tasks need decomposition, dependency mapping, parallel/sequential/swarm/iterative execution strategies, or coordination of multiple specialized agents.
---

# GOAP Agent Skill

Goal-Oriented Action Planning for complex multi-step tasks with intelligent planning and multi-agent coordination.

## Quick Reference

- **[Methodology](methodology.md)** - Core GOAP planning cycle and phases
- **[Execution Strategies](execution-strategies.md)** - Parallel, Sequential, Swarm, Hybrid patterns
- **[Skills Reference](skills.md)** - Available skills by category
- **[Agents Reference](agents.md)** - Available task agents and capabilities
- **[Patterns](patterns.md)** - Common GOAP execution patterns
- **[Examples](examples.md)** - Complete GOAP workflow examples
- **[ADR-022](../../../plans/adr/ADR-022-GOAP-Agent-System.md)** - Architecture Decision Record

## When to Use

- Complex multi-step tasks (5+ distinct steps)
- Cross-domain problems (storage, API, testing, documentation)
- Tasks requiring parallel/sequential execution
- Quality-critical work with validation checkpoints
- Large refactors or architectural changes

## CRITICAL: Skills vs Task Agents

**Skills** (via `Skill` tool): Instruction sets that guide Claude directly
**Agents** (via `Task` tool): Autonomous sub-processes that execute tasks

Example:
- WRONG: `Task(subagent_type="rust-code-quality", ...)` → ERROR!
- CORRECT: `Skill(command="rust-code-quality")` → SUCCESS

See **[skills.md](skills.md)** for complete skills list and **[agents.md](agents.md)** for agent capabilities.

## Core Process

1. **ANALYZE** → Understand goals, constraints, resources
   - **Check ADRs**: Read relevant ADRs from `plans/adr/` before planning
2. **DECOMPOSE** → Break into atomic tasks with dependencies
3. **STRATEGIZE** → Choose execution pattern
4. **COORDINATE** → Assign to specialized agents
5. **EXECUTE** → Run with monitoring and quality gates
6. **SYNTHESIZE** → Aggregate results and validate success

See **[methodology.md](methodology.md)** for detailed phase-by-phase guidance and **[patterns.md](patterns.md)** for common execution patterns.

## ADR Integration Workflow

**MANDATORY**: Always check ADRs in `plans/adr/` before creating execution plans:

### Step 1: ADR Discovery
```bash
# List all ADRs to identify relevant ones
ls plans/adr/ADR-*.md
```

### Step 2: Read Relevant ADRs
- Search for ADRs related to your task domain
- Note architectural decisions and constraints
- Check ADR status (Accepted/Implemented vs Deprecated)

### Step 3: Incorporate into Planning
- Use ADR constraints when decomposing tasks
- Reference ADRs in execution plans
- Ensure compliance with architectural decisions

### Step 4: Update Progress in plans/
- Create/update execution plan files in `plans/`
- Document progress, blockers, and decisions
- Link to relevant ADRs in plan files
