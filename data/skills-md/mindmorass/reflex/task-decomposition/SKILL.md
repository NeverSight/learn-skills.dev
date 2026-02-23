---
name: task-decomposition
description: Break down complex tasks into actionable, atomic steps that can be executed by individual agents.
---


# Task Decomposition Skill

## Purpose
Break down complex tasks into actionable, atomic steps that can be executed by individual agents.

## When to Use
- Receiving complex multi-step requests
- Planning new feature implementation
- Organizing large refactoring efforts
- Coordinating multi-agent workflows

## Decomposition Framework

### Step 1: Identify the Goal
```yaml
goal_analysis:
  end_state: "What does success look like?"
  constraints:
    - Time/resource limitations
    - Technical requirements
    - Dependencies on external systems
  success_criteria:
    - Measurable outcomes
    - Acceptance conditions
```

### Step 2: Break Down by Layer

#### Vertical Decomposition (by feature)
```
Feature Request
├── Component A
│   ├── Task A1
│   └── Task A2
├── Component B
│   ├── Task B1
│   └── Task B2
└── Component C
    └── Task C1
```

#### Horizontal Decomposition (by phase)
```
1. Research Phase
   ├── Understand requirements
   └── Analyze existing code

2. Design Phase
   ├── Define interfaces
   └── Plan architecture

3. Implementation Phase
   ├── Build core functionality
   └── Add edge case handling

4. Validation Phase
   ├── Write tests
   └── Review code
```

### Step 3: Ensure Atomicity

Each task should be:
- **Single responsibility** - Does one thing
- **Completable** - Has clear done criteria
- **Assignable** - Can be done by one agent
- **Verifiable** - Result can be checked

#### Bad (too vague):
```
- "Improve the API"
- "Make it faster"
- "Fix the bugs"
```

#### Good (atomic):
```
- "Add rate limiting to /api/users endpoint"
- "Add index to users.email column"
- "Fix null pointer in UserService.getUser()"
```

### Step 4: Map Dependencies

```yaml
dependencies:
  T1: []                    # Can start immediately
  T2: []                    # Can start immediately
  T3: [T1]                  # Needs T1
  T4: [T1, T2]              # Needs both T1 and T2
  T5: [T3, T4]              # Needs T3 and T4

critical_path: [T1, T3, T5]  # Longest dependency chain
parallel_groups:
  - [T1, T2]                 # Can run together
  - [T3, T4]                 # Can run after first group
```

### Step 5: Assign to Agents

| Task Type | Best Agent |
|-----------|------------|
| Research, fact-finding | Researcher |
| Writing code | Coder |
| Documentation | Writer |
| Data analysis | Analyst |
| Content harvesting | Harvester |
| Code review | Reviewer |
| Testing | Tester |
| Infrastructure | DevOps |

## Complexity Estimation

### Factors
- Number of files affected
- New vs. modifying existing code
- External dependencies
- Testing requirements
- Documentation needs

### Complexity Levels
| Level | Tasks | Agents | Time Estimate |
|-------|-------|--------|---------------|
| Simple | 1-3 | 1 | Minutes |
| Moderate | 4-10 | 1-2 | Hours |
| Complex | 11-25 | 2-4 | Days |
| Very Complex | 25+ | 4+ | Weeks |

## Templates

### Feature Implementation
```yaml
tasks:
  - id: research
    description: "Research existing implementation and requirements"
    agent: researcher

  - id: design
    description: "Design solution architecture"
    agent: planner
    depends_on: [research]

  - id: implement
    description: "Implement the feature"
    agent: coder
    depends_on: [design]

  - id: test
    description: "Write and run tests"
    agent: tester
    depends_on: [implement]

  - id: review
    description: "Code review"
    agent: reviewer
    depends_on: [test]

  - id: document
    description: "Update documentation"
    agent: writer
    depends_on: [implement]
```

### Bug Fix
```yaml
tasks:
  - id: reproduce
    description: "Reproduce and understand the bug"
    agent: coder

  - id: fix
    description: "Implement the fix"
    agent: coder
    depends_on: [reproduce]

  - id: test
    description: "Add regression test"
    agent: tester
    depends_on: [fix]

  - id: review
    description: "Review fix"
    agent: reviewer
    depends_on: [test]
```

### Infrastructure Setup
```yaml
tasks:
  - id: requirements
    description: "Document infrastructure requirements"
    agent: devops

  - id: provision
    description: "Create infrastructure resources"
    agent: devops
    depends_on: [requirements]

  - id: configure
    description: "Configure services"
    agent: devops
    depends_on: [provision]

  - id: validate
    description: "Validate setup works"
    agent: tester
    depends_on: [configure]

  - id: document
    description: "Document infrastructure"
    agent: writer
    depends_on: [configure]
```

## Anti-Patterns

### Over-Decomposition
Breaking tasks too small creates coordination overhead.
- Bad: "Open file" → "Read line 1" → "Read line 2"...
- Good: "Parse configuration file"

### Under-Decomposition
Tasks too large hide complexity and block parallelization.
- Bad: "Build the entire feature"
- Good: Break into research, design, implement, test, document

### Missing Dependencies
Forgetting dependencies causes failures mid-execution.
- Always ask: "What must exist before this can start?"

### Circular Dependencies
```
A depends on B
B depends on C
C depends on A  ← Problem!
```
Solution: Identify shared component, extract as separate task

## Checklist

Before finalizing decomposition:
- [ ] Each task has clear done criteria
- [ ] Dependencies are explicitly mapped
- [ ] No circular dependencies exist
- [ ] Parallel opportunities identified
- [ ] Appropriate agents assigned
- [ ] Complexity realistically estimated
- [ ] Validation/review tasks included
