---
name: ai-agent-implementation
description: Implement feature tasks using AI agents in logical batches, track completion status, identify blockers, and manage task handoffs. Use when you have an execution sequence and need AI agents to build tasks while maintaining progress tracking.
---

# AI Agent Implementation Skill

**Answers the question: How do I execute this feature with AI agents? What's done? What's next? What's blocking?**

This skill manages the **practical execution of feature tasks by AI agents**, handling task batching, progress tracking, and blocker identification without calendar overhead.

## When to Use

Use this skill when you:
- Have an execution sequence (from feature-planning skill)
- Are using AI agents to build features
- Need to track which tasks are done vs. in progress
- Have blockers to identify and manage
- Need to coordinate work between batches

**Key indicator**: You're asking "What should the agent build next?" or "What's the status of this feature?"

**Do NOT use this skill if**: 
- You don't have an execution sequence yet (use feature-planning first)
- You're not using AI agents (this is agent-specific)

## Prerequisites

⚠️ **CRITICAL**: This skill requires an execution sequence as input.

Before using this skill:

1. **Verify you have an execution sequence first**
   - If you don't have `docs/features/[feature-name]/implementation-sequence.md` → Use `feature-planning` first
   - If you have the sequence → Continue below

2. **Expected inputs from feature-planning**:
   - `docs/features/[feature-name]/implementation-sequence.md` file exists
   - Contains complete task list with dependencies
   - Batch groupings identified
   - Critical path marked

**If you don't have an execution sequence**:
- Load the `feature-planning` skill first
- Follow its workflow to sequence your tasks
- Once you have the sequence file, return here

## Inputs

- Execution sequence document (required): `docs/features/[feature-name]/implementation-sequence.md`
- Agent session logs (optional): What agents have completed so far

## Outputs

**MANDATORY FILE ORGANIZATION**: All feature files must be in `docs/features/<feature-name>/` subdirectory.

When this skill is used during execution, it creates/updates:

1. **Execution Progress** (`docs/features/[feature-name]/implementation-progress.md`)
   - Current status of all tasks
   - What's been completed
   - What's in progress
   - What's ready to start next
   - Any blockers or issues
   - **Example**: `docs/features/user-authentication/implementation-progress.md`

2. **Blocker Log** (`docs/features/[feature-name]/blockers.md`)
   - Current blockers preventing progress
   - Root cause analysis
   - Resolution status
   - **Example**: `docs/features/user-authentication/blockers.md`

3. **Session Summary** (`docs/features/[feature-name]/session-summary-[batch-num].md`)
   - What this agent batch completed
   - Test results and verification status
   - What to hand off to next agent/batch
   - Any issues discovered
   - **Example**: `docs/features/user-authentication/session-summary-1.md`

## Workflow Overview

The AI agent execution process:

```
Execution Sequence Input
    ↓
Agent Session 1: Execute Batch 1
    ↓
Track Completion & Verify
    ↓
Identify Blockers
    ↓
Next Agent Session: Execute Batch 2
    ↓
Repeat until all tasks complete
    ↓
Feature Complete
```

## Core Workflow

### Phase 1: Prepare for Agent Execution

**Input**: Execution sequence document

1. **Select batch for agent execution**:
   - Identify next uncompleted batch
   - Confirm all dependencies are met
   - Check for any blockers from previous batches
   - If blockers exist, resolve before proceeding

2. **Prepare batch context**:
   - Extract all tasks in this batch
   - Include acceptance criteria for each task
   - Document any integration points
   - List dependencies and what tasks feed into this batch

3. **Create agent prompt**:
   - Clear objective: "Execute these N tasks"
   - Task list with descriptions and acceptance criteria
   - Integration points and expected outputs
   - Success criteria for this batch
   - Known risks or technical complexity

### Phase 2: Agent Executes Batch

**Agent actions**:
- Receive batch with clear task list
- Execute tasks in sequence or parallel (as specified)
- Verify each task meets acceptance criteria
- Test integration with previous work
- Document completion and any issues

**You monitor**:
- Agent progress during execution
- Any failures or unexpected issues
- Blockers that emerge
- Quality of implementation

### Phase 3: Verify Batch Completion

1. **Check task completion**:
   - Does each task meet its acceptance criteria?
   - Are integration points working?
   - Any test failures?
   - Code quality acceptable?

2. **Identify issues**:
   - What didn't work as expected?
   - What needs rework?
   - What assumptions were wrong?

3. **Update progress**:
   - Mark completed tasks as ✅
   - Mark tasks needing rework as 🔄
   - Mark any new blockers as 🔴
   - Document what worked well

### Phase 4: Identify and Track Blockers

1. **Classify blockers**:
   - **Technical**: Feature doesn't work as designed
   - **Integration**: Task output doesn't match what next task needs
   - **Design**: Requirements were unclear or wrong
   - **External**: Waiting on something outside the feature (dependency, library, API)

2. **Document blocker**:
   - What's preventing progress?
   - Which tasks are blocked?
   - Root cause (if known)?
   - How long to resolve?

3. **Resolution path**:
   - Can it be fixed immediately? (do it)
   - Does it need design change? (clarify then rework)
   - Is it external? (document and wait, or work around)

### Phase 5: Plan Next Batch

1. **Review current state**:
   - What's completed ✅
   - What's in progress 🔄
   - What's blocked 🔴
   - What's ready to start ⏭️

2. **Select next batch**:
   - Find next batch with all dependencies met
   - Check for any blockers from previous work
   - Prepare batch context (same as Phase 1)

3. **Brief next agent**:
   - Pass execution progress
   - Identify any issues from previous batch
   - Provide clear task list for next batch
   - Highlight integration expectations

### Phase 6: Track Overall Progress

Maintain live progress document showing:

- **Completed batches**: Which are done ✅
- **Current batch**: What agent is working on now 🔄
- **Ready batches**: What's queued next ⏭️
- **Blocked**: What can't proceed and why 🔴
- **Overall %**: How close to done

## Output Format: Execution Progress

Create/update file: `docs/features/[feature-name]/implementation-progress.md`

**Directory**: `docs/features/[feature-name]/`  
**Filename**: `implementation-progress.md` (clear, representative name)  
**Example**: `docs/features/user-authentication/implementation-progress.md`

```markdown
# Execution Progress: [Feature Name]

**Last Updated**: [Date/Time]
**Overall Progress**: [X]% complete ([N] of [Total] tasks done)

---

## Status Summary

| Status | Count | Examples |
|--------|-------|----------|
| ✅ Complete | [N] | Task 1, Task 3, Task 5 |
| 🔄 In Progress | [N] | Task 2 (Agent Session X) |
| ⏭️ Ready to Start | [N] | Task 4, Task 6 |
| 🔴 Blocked | [N] | Task 7 (waiting for Task 2) |
| ⚠️ Rework Needed | [N] | Task 8 (test failure) |

---

## Completed Batches ✅

### Batch 1: [Name]
- **Completed**: [Date]
- **Tasks**: [List all tasks]
- **Status**: ✅ All tasks passed acceptance criteria
- **Issues**: None / [List any issues found and fixed]
- **Integration**: Working correctly with Batch 2
- **Handoff**: [What does next batch need to know?]

### Batch 2: [Name]
- **Completed**: [Date]
- **Tasks**: [List all tasks]
- **Status**: ✅ Complete, [N] test failures resolved
- **Issues**: [Describe any issues]
- **Integration**: [Status]
- **Handoff**: [What does next batch need to know?]

---

## Current Batch 🔄

### Batch [N]: [Name]
- **Started**: [Date]
- **Assigned To**: [Agent/Session]
- **Tasks**: 
  - Task [ID]: [Title] - [% complete]
  - Task [ID]: [Title] - [% complete]
- **Expected Completion**: [Date/time estimate]
- **Issues Encountered**: 
  - [Issue 1]: [Description and status]
  - [Issue 2]: [Description and status]
- **Integration Points**: [What needs to work with previous batch?]

---

## Ready to Start ⏭️

### Batch [N]: [Name]
- **Dependencies**: All met ✅
- **Blockers**: None
- **Tasks**: [List N tasks]
- **Expected Start**: [When agent will pick this up]

### Batch [N+1]: [Name]
- **Dependencies**: [Status]
- **Blockers**: [Any known issues?]
- **Tasks**: [List N tasks]
- **Ready**: [Date it will be ready]

---

## Blocked 🔴

### Task [ID]: [Title]
- **Blocker**: [What's preventing completion?]
- **Depends On**: [Task X - not complete yet]
- **Impact**: [What does this block?]
- **Resolution**: [When will dependency be done?]

---

## Blockers Log

See `[feature-name]-blockers.md` for detailed blocker tracking.

**Summary**:
- Critical blockers: [N]
- High priority: [N]
- Medium: [N]
- Waiting for: [External dependency X, Design decision Y, etc.]

---

## Recent Session Summaries

### Session [Date] - Agent [Name/Type]
- **Batch Executed**: [Batch name]
- **Tasks Completed**: [List]
- **Tests Passed**: [N] / [N]
- **Issues Found**: [List any]
- **Code Quality**: [Assessment]
- **Handoff Notes**: [What next agent needs to know]

### Session [Previous Date]
- [Previous session summary]

---

## Critical Path Status

Tasks that determine feature completion:
- Task [ID]: ✅ Complete
- Task [ID]: 🔄 In Progress (Agent Session X)
- Task [ID]: ⏭️ Ready (starting [Date])

**Overall critical path**: On track / At risk / Behind

---

## Next Actions

1. [Action 1]: By [Date]
2. [Action 2]: By [Date]
3. [Action 3]: By [Date]
```

## Output Format: Blocker Log

Create/update file: `docs/features/[feature-name]/blockers.md`

**Directory**: `docs/features/[feature-name]/`  
**Filename**: `blockers.md` (clear, representative name)  
**Example**: `docs/features/user-authentication/blockers.md`

```markdown
# Blocker Log: [Feature Name]

---

## Current Blockers 🔴

### Blocker 1: [Title]

**Severity**: Critical / High / Medium

**Affected Tasks**: Task [ID], Task [ID]

**Description**: [What's blocking progress?]

**Cause**: [Why is this happening?]

**Impact**: [If not resolved, what doesn't get built?]

**Resolution**: [How will this be fixed?]

**Owner**: [Your role, or external dependency name]

**Target Resolution**: [Date/time]

---

## Recently Resolved ✅

### Blocker: [Title]

**Reported**: [Date]
**Resolved**: [Date] (resolved in [Duration])

**Cause**: [What was the issue?]

**Solution**: [How was it fixed?]

**Lessons**: [What did we learn?]

---

## External Blockers ⏸️

Waiting on things outside this feature:

- [Dependency/Library]: Waiting for [What?] - Expected [Date]
- [External Service]: [Status] - Expected [Date]
```

## Session Handoff Format

After each agent session, create brief summary in feature directory:

**File path**: `docs/features/[feature-name]/session-summary-[batch-num].md`  
**Filename pattern**: `session-summary-1.md`, `session-summary-2.md`, etc.  
**Example**: `docs/features/user-authentication/session-summary-1.md`

```markdown
# Session Summary: Batch [N] - [Date]

**Batch**: [Batch name]
**Agent**: [AI model/type used]
**Duration**: [Session length]

## Completed Tasks ✅

- Task [ID]: [Title] - ✅ Complete, all acceptance criteria met
- Task [ID]: [Title] - ✅ Complete, [N] test failures fixed

## Tasks Needing Rework 🔄

- Task [ID]: [Title] - Test failure: [Description]
  - Status: Being reworked
  - Expected completion: [When]

## Blockers Encountered 🔴

- [Blocker description] - Added to blocker log

## Integration Status

- Previous batch: ✅ Working correctly
- Next batch: ⏭️ Ready to start when this completes

## Handoff for Next Agent

[Copy what next agent needs to know]
- What these tasks built
- Any quirks or gotchas
- Integration requirements
- Files/paths that matter
```

## Guidelines

### Task Completion Criteria

A task is ✅ COMPLETE when:
- All acceptance criteria are met
- Code is in repository (merged or staged)
- Tests pass (if applicable)
- Integration with previous work verified
- No known issues

A task is 🔄 IN PROGRESS when:
- Agent is actively building it
- Some work is done but not all acceptance criteria met
- Waiting on integration testing

A task is ⏭️ READY when:
- All dependencies are complete
- No blockers exist
- Agent can start immediately

A task is 🔴 BLOCKED when:
- Cannot proceed due to external dependency
- Depends on incomplete task
- Needs clarification or decision

### Batch Sizing

- **Too small**: 1 task per batch (too granular)
- **Good size**: 1-3 related tasks per batch (can complete in one session)
- **Too large**: 4+ tasks (too much context, may not complete)

### Blocker Resolution

**Immediate fixes**:
- Rework task: Have agent fix it
- Clarify requirements: Get clear spec, agent redoes task
- Code quality: Agent improves, retests

**Wait & Proceed**:
- External dependency: Work on other batches, revisit later
- Design decision: Move to next batch while waiting
- Known limitation: Document and proceed

**Cannot Proceed**:
- Critical blocker with no workaround: Stop, resolve, continue

## Common Patterns

### Pattern: Task Fails Tests
1. Agent reports: "Test X failed"
2. You: Review failure, identify cause
3. Either: Rework task, or clarify requirements
4. Agent: Re-executes task
5. Update progress when fixed

### Pattern: Dependencies Not Met
1. Agent reports: "Can't start because Task X not done"
2. You: Verify Task X completion
3. If complete: Task needs output from Task X (integration issue)
4. If incomplete: Move this batch down, work on different batch
5. Return to blocked task when dependency ready

### Pattern: Integration Breaks
1. Agent reports: "Task works alone, breaks when integrated"
2. You: Review what task outputs vs. what next task expects
3. Either: Fix task implementation, or fix integration point
4. Agent: Tests integration again
5. Mark complete only when integrated successfully

## See Also

Reference documents:
- `batch-execution-template.md`: Template for batch execution
- `blocker-triage-guide.md`: How to handle different blocker types
- `example-ai-implementation.md`: Complete end-to-end example with User Authentication system
