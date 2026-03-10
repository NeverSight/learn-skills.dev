---
name: planning
description: PRD construction for work planning. Use this skill in PLAN phase to build .prd file with complete dependency graph of all items, edge cases, and subtasks before execution begins.
allowed-tools: Write
---

# Work Planning with PRD Construction

## Overview

This skill constructs `./.prd` (Product Requirements Document) files for structured work tracking. The PRD is a **single source of truth** that captures every possible item to complete, organized as a dependency graph for parallel execution.

**CRITICAL**: The PRD must be created in PLAN phase before any work begins. It blocks all other work until complete. It is frozen after creation—only items may be removed as they complete. No additions or reorganizations after plan is created.

## When to Use This Skill

Use `planning` skill when:
- Starting a new task or initiative
- User requests multiple items/features/fixes that need coordination
- Work has dependencies, parallellizable items, or complex stages
- You need to track progress across multiple independent work streams

**Do NOT use** if task is trivial (single item under 5 minutes).

## PRD Structure

Each PRD contains:
- **items**: Array of work items with dependencies
- **completed**: Empty list (populated as items finish)
- **metadata**: Total estimates, phases, notes

### Item Fields

```json
{
  "id": "1",
  "subject": "imperative verb describing outcome",
  "status": "pending",
  "description": "detailed requirement",
  "blocking": ["2", "3"],
  "blockedBy": ["4"],
  "effort": "small|medium|large",
  "category": "feature|bug|refactor|docs",
  "notes": "contextual info"
}
```

### Key Rules

**Subject**: Use imperative form - "Fix auth bug", "Add webhook support", "Consolidate templates", not "Bug: auth", "New feature", etc.

**Blocking/Blocked By**: Map dependency graph
- If item 2 waits for item 1: `"blockedBy": ["1"]`
- If item 1 blocks items 2 & 3: `"blocking": ["2", "3"]`

**Status**: Only three values
- `pending` - not started
- `in_progress` - currently working
- `completed` - fully done

**Effort**: Estimate relative scope
- `small`: 1-2 items in 15 min
- `medium`: 3-5 items in 30-45 min
- `large`: 6+ items or 1+ hours

## Complete Item Template

Use this when planning complex work:

```json
{
  "id": "task-name-1",
  "subject": "Consolidate duplicate template builders",
  "status": "pending",
  "description": "Extract shared generatePackageJson() and buildHooksMap() logic from cli-adapter.js and extension-adapter.js into TemplateBuilder methods. Current duplication causes maintenance burden.",
  "category": "refactor",
  "effort": "medium",
  "blocking": ["task-name-2"],
  "blockedBy": [],
  "acceptance": [
    "Single generatePackageJson() method in TemplateBuilder",
    "Both adapters call TemplateBuilder methods",
    "All 9 platforms generate identical package.json structure",
    "No duplication in adapter code"
  ],
  "edge_cases": [
    "Platforms without package.json (JetBrains IDE)",
    "Custom fields for CLI vs extension platforms"
  ],
  "verification": "All 9 build outputs pass validation, adapters <150 lines each"
}
```

## Comprehensive Planning Checklist

When creating PRD, cover:

### Requirements
- [ ] Main objective clearly stated
- [ ] Success criteria defined
- [ ] User-facing changes vs internal
- [ ] Backwards compatibility implications
- [ ] Data migration needed?

### Edge Cases
- [ ] Empty inputs/missing files
- [ ] Large scale (1000s of items?)
- [ ] Concurrent access patterns
- [ ] Timeout/hang scenarios
- [ ] Recovery from failures

### Dependencies
- [ ] External services/APIs required?
- [ ] Third-party library versions
- [ ] Environment setup (DB, redis, etc)
- [ ] Breaking changes from upgrades?

### Acceptance Criteria
- [ ] Code changed meets goal
- [ ] Tests pass (if applicable)
- [ ] Performance requirements met
- [ ] Security concerns addressed
- [ ] Documentation updated

### Integration Points
- [ ] Does it touch other systems?
- [ ] API compatibility impacts?
- [ ] Database schema changes?
- [ ] Message queue formats?
- [ ] Configuration propagation?

### Error Handling
- [ ] What fails gracefully?
- [ ] What fails hard?
- [ ] Recovery mechanisms?
- [ ] Fallback options?
- [ ] User notification strategy?

## PRD Lifecycle

### Creation Phase
1. Enumerate **every possible unknown** as work item
2. Map dependencies (blocking/blockedBy)
3. Group parallelizable items into waves
4. Verify all edge cases captured
5. Write `./.prd` to disk
6. **FREEZE** - no modifications except item removal

### Execution Phase
1. Read `.prd`
2. Find all `pending` items with no `blockedBy`
3. Launch ≤3 parallel workers (gm:gm subagents) per wave
4. As items complete, update status to `completed`
5. Remove completed items from `.prd` file
6. Launch next wave when previous completes
7. Continue until `.prd` is empty

### Completion Phase
- `.prd` file is empty (all items removed)
- All work committed and pushed
- Tests passing
- No remaining `pending` or `in_progress` items

## File Location

**CRITICAL**: PRD must be at exactly `./.prd` (current working directory root).

- ✅ `/home/user/plugforge/.prd`
- ❌ `/home/user/plugforge/.prd-temp`
- ❌ `/home/user/plugforge/build/.prd`
- ❌ `/home/user/plugforge/.prd.json`

No variants, no subdirectories, no extensions. Absolute path must resolve to `cwd + .prd`.

## JSON Format

PRD files are **valid JSON** for easy parsing and manipulation.

```json
{
  "project": "plugforge",
  "created": "2026-02-24",
  "objective": "Unify agent tooling and planning infrastructure",
  "items": [
    {
      "id": "1",
      "subject": "Update agent-browser skill documentation",
      "status": "pending",
      "description": "Add complete command reference with all 100+ commands",
      "blocking": ["2"],
      "blockedBy": [],
      "effort": "small",
      "category": "docs"
    },
    {
      "id": "2",
      "subject": "Create planning skill for PRD construction",
      "status": "pending",
      "description": "New skill that creates .prd files with dependency graphs",
      "blocking": ["3"],
      "blockedBy": ["1"],
      "effort": "medium",
      "category": "feature"
    },
    {
      "id": "3",
      "subject": "Update gm.md agent instructions",
      "status": "pending",
      "description": "Reference new skills, emphasize codesearch over cli tools",
      "blocking": [],
      "blockedBy": ["2"],
      "effort": "medium",
      "category": "docs"
    }
  ],
  "completed": []
}
```

## Execution Guidelines

**Wave Orchestration**: Maximum 3 subagents per wave (gm:gm agents via Task tool).

```
Wave 1: Items 1, 2, 3 (all pending, no dependencies)
  └─ 3 subagents launched in parallel

Wave 2: Items 4, 5 (depend on Wave 1 completion)
  └─ Items 6, 7 (wait for Wave 2)

Wave 3: Items 6, 7
  └─ 2 subagents (since only 2 items)

Wave 4: Item 8 (depends on Wave 3)
  └─ Completes work
```

After each wave completes:
1. Remove finished items from `.prd`
2. Write `.prd` (now shorter)
3. Check for newly unblocked items
4. Launch next wave

## Example: Multi-Platform Builder Updates

```json
{
  "project": "plugforge",
  "objective": "Add hooks support to 5 CLI platforms",
  "items": [
    {
      "id": "hooks-cc",
      "subject": "Add hooks to gm-cc platform",
      "status": "pending",
      "blocking": ["test-hooks"],
      "blockedBy": [],
      "effort": "small"
    },
    {
      "id": "hooks-gc",
      "subject": "Add hooks to gm-gc platform",
      "status": "pending",
      "blocking": ["test-hooks"],
      "blockedBy": [],
      "effort": "small"
    },
    {
      "id": "hooks-oc",
      "subject": "Add hooks to gm-oc platform",
      "status": "pending",
      "blocking": ["test-hooks"],
      "blockedBy": [],
      "effort": "small"
    },
    {
      "id": "test-hooks",
      "subject": "Test all 5 platforms with hooks",
      "status": "pending",
      "blocking": [],
      "blockedBy": ["hooks-cc", "hooks-gc", "hooks-oc"],
      "effort": "large"
    }
  ]
}
```

**Execution**:
- Wave 1: Launch 3 subagents for `hooks-cc`, `hooks-gc`, `hooks-oc` in parallel
- After all 3 complete, launch `test-hooks`

This cuts wall-clock time from 45 min (sequential) to ~15 min (parallel).

## Best Practices

### Cover All Scenarios
Don't under-estimate work. If you think it's 3 items, list 8. Missing items cause restarts.

### Name Dependencies Clearly
- `blocking`: What does THIS item prevent?
- `blockedBy`: What must complete before THIS?
- Bidirectional: If A blocks B, then B blockedBy A

### Use Consistent Categories
- `feature`: New capability
- `bug`: Fix broken behavior
- `refactor`: Improve structure without changing behavior
- `docs`: Documentation
- `infra`: Build, CI, deployment

### Track Edge Cases Separately
Even if an item seems small, if it has edge cases, call them out. They often take 50% of the time.

### Estimate Effort Realistically
- `small`: Coding + testing in 1 attempt
- `medium`: May need 2 rounds of refinement
- `large`: Multiple rounds, unexpected issues likely

## Stop Hook Enforcement

When session ends, a **stop hook** checks if `.prd` exists and has `pending` or `in_progress` items. If yes, session is blocked. You cannot leave work incomplete.

This forces disciplined work closure: every PRD must reach empty state or explicitly pause with documented reason.

## Integration with gm Agent

The gm agent (immutable state machine) reads `.prd` in PLAN phase:
1. Verifies `.prd` exists and has valid JSON
2. Extracts items with `status: pending`
3. Finds items with no `blockedBy` constraints
4. Launches ≤3 gm:gm subagents per wave
5. Each subagent completes one item
6. On completion, PRD is updated (item removed)
7. Process repeats until `.prd` is empty

This creates structured, auditable work flow for complex projects.