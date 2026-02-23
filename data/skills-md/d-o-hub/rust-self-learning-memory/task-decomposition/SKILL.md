---
name: task-decomposition
description: Break down complex tasks into atomic, actionable goals with clear dependencies and success criteria. Use when planning multi-step projects, coordinating agents, or decomposing complex requests.
---

# Task Decomposition

Break down complex tasks into atomic, actionable goals with clear dependencies.

## When to Use

- Complex user requests with multiple components
- Multi-phase projects requiring coordination
- Tasks that could benefit from parallel execution
- Planning agent coordination strategies

## Decomposition Framework

### 1. Requirements Analysis

- Primary objective
- Implicit requirements (quality, performance)
- Constraints (time, resources)
- Success criteria

### 2. Goal Hierarchy

```
Main Goal
├─ Sub-goal 1
│  ├─ Task 1.1 (atomic)
│  └─ Task 1.2 (atomic)
├─ Sub-goal 2
└─ Sub-goal 3
```

### 3. Dependency Types

| Type | Symbol | Example |
|------|--------|---------|
| Sequential | A → B → C | B needs A's output |
| Parallel | A─┐ B─┐ C─┘ | Independent, concurrent |
| Converging | A─┐ B─┼─> D | D needs A, B, C |
| Resource | A, B | Sequential or pooled |

### 4. Success Criteria

For each task:
- **Input**: What data/state is needed
- **Output**: What artifacts will be produced
- **Quality**: Performance, testing, docs requirements

## Decomposition Patterns

| Pattern | Use Case |
|---------|----------|
| Layer-Based | Architectural changes (data, logic, API, test, docs) |
| Feature-Based | New features (MVP, error handling, optimization, integration) |
| Phase-Based | Large projects (research, foundation, core, integration, polish) |
| Problem-Solution | Debugging (reproduce, diagnose, design, fix, verify, prevent) |

## Quality Checklist

✓ Atomic and actionable
✓ Dependencies clearly identified
✓ Success criteria measurable
✓ No task too large (>4 hours)
✓ Parallelization opportunities identified

✗ Tasks too large or vague
✗ Missing dependencies
✗ Unclear success criteria
✗ Missing quality/testing tasks

## Integration with GOAP

Task decomposition is Phase 1 of GOAP:
1. Receive request
2. Apply decomposition
3. Create execution plan
4. Execute with monitoring
5. Report results
