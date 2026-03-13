---
name: Workflow Designer
slug: workflow-designer
description: Design and optimize AI-powered workflows for complex tasks
category: meta
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "design a workflow"
  - "create workflow"
  - "optimize workflow"
  - "workflow designer"
  - "plan workflow"
tags:
  - workflow-design
  - process-optimization
  - automation
---

# Workflow Designer

The Workflow Designer skill helps you design, document, and optimize multi-step AI-powered workflows. It applies process design principles to break down complex tasks into clear, executable sequences that leverage Claude Code's capabilities, external tools, and multi-agent coordination.

This skill guides you through workflow analysis, identifying optimal task decomposition, determining when to use automation versus human input, and documenting workflows in a format that's both human-readable and AI-executable. It helps you think through error handling, branching logic, validation steps, and integration points.

Use this skill when you're tackling complex, multi-step processes that could benefit from AI assistance, or when you need to transform ad-hoc procedures into repeatable, documented workflows.

## Core Workflows

### Workflow 1: Design New Workflow from Requirements
1. **Clarify** the goal:
   - What outcome is needed?
   - Who initiates the workflow?
   - What triggers completion?
2. **Identify** inputs and outputs:
   - What data/context is required to start?
   - What should the workflow produce?
   - What format should outputs take?
3. **Map** the process:
   - Break into logical phases
   - Identify decision points
   - Map dependencies between steps
   - Note parallel vs sequential operations
4. **Design** error handling:
   - What can go wrong at each step?
   - How should failures be handled?
   - What requires human intervention?
5. **Assign** responsibilities:
   - Which steps are AI-executable?
   - Which require human judgment?
   - Which need external tools/APIs?
6. **Document** the workflow:
   - Step-by-step instructions
   - Decision trees
   - Validation checkpoints
   - Success criteria
7. **Test** with sample scenario
8. **Refine** based on results

### Workflow 2: Optimize Existing Workflow
1. **Analyze** current workflow:
   - Map current steps
   - Identify bottlenecks
   - Note repetitive tasks
   - Find error-prone areas
2. **Identify** optimization opportunities:
   - What can be automated?
   - What can be parallelized?
   - What steps are unnecessary?
   - Where are handoffs inefficient?
3. **Redesign** with improvements:
   - Consolidate redundant steps
   - Automate repetitive tasks
   - Parallelize independent operations
   - Add validation early
4. **Compare** before/after:
   - Time savings
   - Error reduction
   - Complexity changes
   - Resource requirements
5. **Document** changes and rationale
6. **Plan** migration from old to new
7. **Test** new workflow thoroughly

### Workflow 3: Break Down Complex Task
1. **Understand** the complex task:
   - What makes it complex?
   - What are the components?
   - What are the constraints?
2. **Decompose** into subtasks:
   - Identify logical boundaries
   - Group related operations
   - Order by dependencies
3. **Define** interfaces:
   - Inputs for each subtask
   - Outputs from each subtask
   - Data flow between tasks
4. **Assign** to appropriate executors:
   - AI agents
   - External tools/MCPs
   - Human review points
5. **Add** coordination layer:
   - How do subtasks communicate?
   - What monitors overall progress?
   - How are results integrated?
6. **Document** the decomposition
7. **Validate** completeness

### Workflow 4: Add Error Handling & Resilience
1. **Map** potential failure points:
   - External API failures
   - Invalid inputs
   - Resource constraints
   - Timeout scenarios
2. **Design** error handling strategy:
   - Graceful degradation
   - Retry logic with backoff
   - Fallback options
   - Error reporting
3. **Add** validation checkpoints:
   - Pre-conditions before steps
   - Post-conditions after steps
   - Intermediate result validation
4. **Implement** recovery mechanisms:
   - State preservation
   - Resume from checkpoint
   - Rollback procedures
5. **Document** error scenarios:
   - What to do when X fails
   - How to recover
   - When to escalate
6. **Test** failure scenarios

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Design new workflow | "Design a workflow for [task]" |
| Optimize existing workflow | "Optimize this workflow: [description]" |
| Break down complex task | "Break down this task: [task]" |
| Add error handling | "Add error handling to this workflow: [workflow]" |
| Document workflow | "Document this process: [process]" |
| Visualize workflow | "Create a flowchart for [workflow]" |
| Validate workflow design | "Review this workflow design: [design]" |

## Best Practices

- **Start with Outcomes**: Define success before designing steps
  - What does "done" look like?
  - What artifacts should exist?
  - What state should system be in?

- **Keep Steps Atomic**: Each step should be single-purpose
  - One clear action
  - One clear output
  - Easy to validate
  - Easy to replace or improve

- **Make Dependencies Explicit**: Show what relies on what
  - Use directed graphs or numbered dependencies
  - Identify parallelizable operations
  - Note blocking dependencies

- **Plan for Failure**: Every workflow has edge cases
  - What if API is down?
  - What if input is malformed?
  - What if process takes too long?
  - What if user cancels?

- **Add Validation Early**: Catch issues before they cascade
  - Validate inputs before processing
  - Check outputs before passing to next step
  - Verify assumptions at decision points

- **Document Decision Points**: Make branching logic clear
  - What triggers each path?
  - What are the criteria?
  - Who makes the decision (AI vs human)?

- **Separate Concerns**: Group related operations
  - Data collection phase
  - Processing phase
  - Validation phase
  - Output generation phase

- **Make It Resumable**: Long workflows should support interruption
  - Save state at checkpoints
  - Enable resume from last checkpoint
  - Track progress explicitly

- **Test with Edge Cases**: Don't just test happy path
  - Malformed inputs
  - Missing dependencies
  - Timeout scenarios
  - Concurrent execution

## Workflow Design Patterns

### Sequential Pipeline
```
Input → Step 1 → Step 2 → Step 3 → Output
```
**Use when**: Each step depends on previous step's output
**Example**: Data ingestion → Validation → Transformation → Storage

### Parallel Execution
```
Input → [Step 1, Step 2, Step 3] → Merge → Output
```
**Use when**: Independent operations can run concurrently
**Example**: Lint, Test, Type-check → Aggregate results → Report

### Conditional Branching
```
Input → Decision → [Path A | Path B] → Merge → Output
```
**Use when**: Different paths based on conditions
**Example**: File type detection → [JSON parser | CSV parser] → Normalize

### Iterative Refinement
```
Input → Process → Validate → [Done? → Output | Refine → Process]
```
**Use when**: Output quality improves through iterations
**Example**: Generate code → Review → [Acceptable? → Deploy | Fix issues → Generate]

### Multi-Agent Orchestration
```
Input → Coordinator → [Agent A, Agent B, Agent C] → Synthesizer → Output
```
**Use when**: Complex task needs specialized sub-agents
**Example**: Feature request → Planner → [Designer, Developer, Tester] → Integrator → PR

### Event-Driven Workflow
```
Trigger → [Handler 1, Handler 2, Handler N] → Aggregate → Output
```
**Use when**: Workflow responds to events/webhooks
**Example**: Git push → [Build, Test, Deploy, Notify] → Status update

## Workflow Documentation Template

```markdown
## Workflow: [Name]

### Purpose
[What this workflow accomplishes]

### Triggers
- [What initiates this workflow]

### Inputs
- [Required inputs]
- [Optional inputs]

### Steps
1. **[Step Name]**
   - Action: [What happens]
   - Owner: [AI | Human | Tool]
   - Input: [What this step receives]
   - Output: [What this step produces]
   - Validation: [How to verify success]
   - On failure: [What to do if this fails]

2. **[Step Name]**
   [...]

### Decision Points
- **[Decision Name]**
  - Condition: [What determines the path]
  - If true: [Path A]
  - If false: [Path B]

### Outputs
- [What the workflow produces]
- [Where outputs are stored/sent]

### Success Criteria
- [How to know the workflow succeeded]

### Error Handling
- [Common failures and responses]

### Estimated Duration
- [How long this typically takes]

### Dependencies
- [External tools/services required]
- [Other workflows this depends on]
```

## Workflow Metrics to Track

When designing workflows, consider measuring:

- **Duration**: How long does the workflow take?
- **Success rate**: What percentage complete successfully?
- **Bottlenecks**: Which steps take longest?
- **Failure points**: Where do errors occur most?
- **Retry rate**: How often do steps need retrying?
- **Human intervention**: How often is manual action needed?
- **Resource usage**: What's the computational/financial cost?

## Common Pitfalls

- **Over-engineering**: Don't add complexity for problems that haven't occurred
- **Under-specifying**: Don't assume steps are obvious without documentation
- **Ignoring failures**: Don't design only for happy path
- **Tight coupling**: Don't make steps too dependent on implementation details
- **No rollback**: Don't make destructive operations irreversible
- **Missing validation**: Don't pass bad data between steps
- **Sequential when parallel works**: Don't serialize independent operations
- **No progress tracking**: Don't make long workflows black boxes
