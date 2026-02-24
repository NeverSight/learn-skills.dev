---
name: feature-planning
description: Sequence tasks from a feature breakdown into an optimal execution order, identify dependencies and parallelization opportunities, and create an agent-ready execution sequence. Use when you have a feature breakdown and need to determine the correct order to build tasks and which can run in parallel.
---

# Feature Planning Skill

**Answers the question: In what order should tasks be executed? Which can run in parallel? What blocks what?**

This skill focuses on **task sequencing and dependency analysis**, transforming a flat task list into a logical execution flow.

## When to Use

Use this skill when you have a **feature breakdown document** and need to:
- Determine the correct order to execute tasks
- Identify which tasks block other tasks
- Find opportunities for parallelization
- Create a sequenced task list for execution
- Understand dependencies and integration points

**Key indicator**: You're asking "In what order should these tasks be done?" and "Which can happen in parallel?"

**Do NOT use this skill if**: 
- You only have a feature spec/idea (use feature-breakdown first to identify all tasks)
- You need calendar dates and deadlines (not the focus of this skill)

## Prerequisites Check

⚠️ **CRITICAL**: This skill requires a feature breakdown document as input. Do NOT proceed without it.

Before using this skill:

1. **Verify you have completed `feature-breakdown` first**
   - If you only have a feature spec or idea → STOP and use `feature-breakdown` skill first
   - If you have a feature breakdown document → Continue below

2. **Expected inputs from feature-breakdown**:
   - `docs/features/[feature-name]-breakdown.md` file exists
   - Contains all 8 required sections
   - Has a complete task list with dependencies and acceptance criteria

**If you don't have a breakdown document**:
- Load the `feature-breakdown` skill first
- Follow its workflow to decompose your feature spec into tasks
- Once you have `docs/features/[feature-name]/breakdown.md`, return here

## Inputs

- Feature breakdown document (required): `docs/features/[feature-name]/breakdown.md`

## Outputs

**MANDATORY FILE ORGANIZATION**: All feature files must be in `docs/features/<feature-name>/` subdirectory.

When this skill completes, it creates:

1. **Sequenced Task List** (`docs/features/[feature-name]/implementation-sequence.md`)
   - All tasks organized in optimal execution order
   - Clear dependency relationships
   - Parallelization opportunities identified
   - Ready for AI agents to execute
   - **Example**: `docs/features/user-authentication/implementation-sequence.md`

## Workflow Overview

The feature planning process transforms a breakdown into an ordered execution sequence:

```
Feature Breakdown Input
    ↓
Extract Tasks & Dependencies
    ↓
Build Dependency Graph
    ↓
Identify Execution Sequence
    ↓
Mark Parallel Opportunities
    ↓
Create Sequenced Task List
    ↓
Ready for Execution
```

## Core Workflow

### Phase 1: Extract and Validate Breakdown

**Input**: Feature breakdown document

1. **Read breakdown structure**:
   - Extract all tasks with their IDs and descriptions
   - Document all dependencies (which tasks block which)
   - Note component mappings
   - List acceptance criteria for each task

2. **Validate task quality**:
   - Confirm each task has acceptance criteria
   - Verify dependencies are explicitly stated
   - Identify any circular dependencies
   - Check for gaps or missing tasks

### Phase 2: Build Dependency Graph

1. **Map all task dependencies**:
   - Create visual representation of what blocks what
   - Identify sequential tasks (must complete in order)
   - Identify parallel tasks (can run simultaneously)
   - Flag any circular dependencies or issues

2. **Identify critical path** (longest dependency chain):
   - Calculate total length of each dependency chain
   - Mark the longest chain as critical path
   - Note tasks on critical path that cannot slip

3. **Group related work**:
   - Group tasks by component
   - Identify natural groupings for batching
   - Recognize integration points requiring coordination

### Phase 3: Determine Execution Sequence

1. **Order tasks respecting dependencies**:
   - Start with tasks that have no dependencies (can start immediately)
   - Place dependent tasks after their prerequisites
   - Group parallel tasks together
   - Organize by logical component flow

2. **Identify parallelization opportunities**:
   - Mark which tasks CAN run simultaneously
   - Group parallel tasks for batch execution
   - Document why tasks can/cannot run in parallel

### Phase 4: Create Sequenced Task List

Generate the sequenced task list with this structure:

**Sequenced Task Structure**:

```markdown
## Task [ID]: [Task Title]

**Component**: [Which component(s)]

**Depends On**: [List prerequisite task IDs, or "None"]

**Parallel With**: [Other task IDs that can run simultaneously, or "None"]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Integration Points**: [What does this task interface with?]

**Risks**: [Any technical risks or complexity?]
```

**Organization principles**:

1. **Order tasks sequentially** - respect dependencies
2. **Group parallel tasks** - related parallel work together
3. **Mark critical path** - indicate which tasks determine overall completion
4. **Note integration points** - show what requires coordination
5. **Include all details** - make each task self-contained and clear

### Phase 5: Identify Batch Groupings

For single developer + AI agent execution:

1. **Group tasks into logical batches** (1-3 tasks per batch):
   - Batch 1: Foundation/Setup tasks
   - Batch 2: Component A implementation
   - Batch 3: Component B implementation
   - Batch 4: Integration & Testing
   - Etc.

2. **Each batch should**:
   - Be executable without waiting for other work
   - Have clear success criteria
   - Be able to complete before next batch starts
   - Have manageable scope for one agent session

## Output Format

Create a single file: `docs/features/[feature-name]/implementation-sequence.md`

- **Directory**: Must use feature-specific subdirectory: `docs/features/[feature-name]/`
- **Filename**: `implementation-sequence.md` (clear, representative name)
- **Example**: `docs/features/user-authentication/implementation-sequence.md`
- **MANDATORY**: All feature files in same directory to maintain organization

```markdown
# Execution Sequence: [Feature Name]

## Overview

**Total Tasks**: [N]
**Critical Path Length**: [N] tasks
**Parallel Opportunities**: [N] groups of parallel tasks

## Dependency Graph

[Visual ASCII representation or text description of dependencies]

## Sequenced Task List

[All tasks in order, following structure above]

## Batch Groupings (For Agent Execution)

### Batch 1: [Batch Name]
- Task [ID]: [Title]
- Task [ID]: [Title]
- Can execute in parallel: [Yes/No]
- Prerequisites: [None or list]

### Batch 2: [Batch Name]
[etc]

## Critical Path

Tasks that determine overall completion time:
- Task [ID] → Task [ID] → Task [ID]
- Total length: [N] tasks
- Cannot slip without delaying project

## Integration Points

Key coordination requirements:
- Task A output becomes Task B input
- [etc]

## Next Steps

Execute batches sequentially, using this sequence as the source of truth.
```

## Guidelines

### Dependency Rules

- **Hard Dependency**: Task B cannot start until Task A is 100% complete
- **Soft Dependency**: Task B can start during Task A but needs early completion milestone
- **No Dependency**: Tasks are completely independent

### Parallelization

Tasks can run in parallel if:
- They have no dependencies on each other
- They work on different components
- They don't share resources

Tasks must run sequentially if:
- One's output feeds into the other's input
- They modify the same file/component
- One sets up infrastructure the other needs

### Critical Path

The critical path is what determines overall completion. If ANY task on the critical path slips, the entire feature slips.

**Identify critical path by**:
1. Calculate total length of each dependency chain
2. Find the longest chain
3. These are the critical tasks

## Common Pitfalls to Avoid

❌ **Ignoring dependencies**: Ordering tasks that block each other

❌ **Assuming parallel work**: Tasks that look independent but share dependencies

❌ **Missing integration points**: Not recognizing when one task needs output from another

❌ **Circular dependencies**: Task A depends on B, B depends on A

❌ **Vague grouping**: Batches that are too large to execute in one session

## See Also

For reference materials, see the included reference documents:
- `sequencing-guide.md`: How to analyze and sequence dependencies
- `batch-organization.md`: How to group tasks for execution
