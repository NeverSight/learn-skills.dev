---
name: Update Linear Post-Job
description: Three-step Linear update protocol after job completion - update child issue, check parent completion, update parent if all children done
category: workflow
usage: tracking
version: 1.0
created: 2025-11-05
converted_from: docs/agents/shared-ref-docs/post-job-linear-updates.md
---

# Update Linear Post-Job

## When to Use

Use this skill when:

- **Job completion** (Tracking Agent): After QA validates implementation and Planning Agent confirms job complete
- **Phase 7 of TDD workflow**: Tracking Agent handles PR/documentation and Linear updates
- **Work block tracking**: Need to update child issue status and check parent completion

**Triggers**:
- Planning Agent confirms job completion
- QA Agent approves implementation
- PR is merged and job is ready for closure
- Need to track work block progress in Linear

**TDD Workflow Context**:
- **7-Phase TDD**: Research → Spec → Linear Enrichment → QA (tests) → Action (code) → QA (validate) → Tracking (PR/docs) → Dashboard Update
- **This skill**: Executes during Phase 7 (Tracking Agent responsibilities)

## Workflow

### Step 1: Update Child Issue Status

**Purpose**: Mark the completed job (child issue) as Done in Linear

**Prerequisites**:
- Planning Agent confirmed job completion
- QA Agent approved implementation
- PR merged (if applicable)
- Handoff includes child issue ID

**Execute**:

```typescript
// Update child issue to Done
await mcp__linear-server__update_issue({
  id: "LAW-5",  // Child issue ID from handoff
  state: "Done"
})
```

**Then add completion comment**:

```typescript
await mcp__linear-server__create_comment({
  issueId: "LAW-5",
  body: `✅ **Job Complete**

**PR**: #14 (https://github.com/org/repo/pull/14)
**QA Status**: ✅ All tests passing
**Files Changed**: 8 files, +420/-15 lines

Ready for merge.`
})
```

**Comment Template Fields**:
- **PR**: Link to merged pull request (if applicable)
- **QA Status**: Confirmation that QA validation passed
- **Files Changed**: Summary of code changes
- **Additional Notes**: Any relevant completion details

**Error Handling**:

If update fails, add comment instead and continue:

```typescript
try {
  await mcp__linear-server__update_issue({ id: "LAW-5", state: "Done" })
} catch (error) {
  await mcp__linear-server__create_comment({
    issueId: "LAW-5",
    body: `⚠️ **Tracking Agent**: Could not update issue status to Done.

Error: ${error.message}

Job completion confirmed by Planning Agent. Manual status update needed.`
  })
  // Continue to Step 2 - don't block on child update failure
}
```

### Step 2: Check Parent Work Block Completion

**Purpose**: Determine if all child jobs in the work block are complete

**Execute**:

```typescript
// 1. Get parent issue details
const parentIssue = await mcp__linear-server__get_issue({
  id: "LAW-4"  // Parent work block ID from handoff
})

// 2. Get all child issues of parent
const childIssues = await mcp__linear-server__list_issues({
  team: "Linear-First-Agentic-Workflow",  // From .project-context.md
  parentId: "LAW-4"  // Parent work block ID
})

// 3. Check if ALL children are Done
const allChildrenDone = childIssues.nodes.every(
  issue => issue.state.name === "Done"
)
```

**Decision Point**:
- **If `allChildrenDone === true`**: Proceed to Step 3 (update parent)
- **If `allChildrenDone === false`**: Skip to Step 4 (report to Planning Agent)

**What to check**:
- All child issues must have `state.name === "Done"`
- Check all siblings (other child issues under same parent)
- Do not update parent if any child is still In Progress, Todo, or Blocked

### Step 3: Update Parent Work Block (If All Children Complete)

**Purpose**: Mark parent work block as Done when all child jobs complete

**Execute only if Step 2 determined all children are Done**:

```typescript
// Update parent work block to Done
await mcp__linear-server__update_issue({
  id: "LAW-4",
  state: "Done"
})

// Add completion comment to parent
await mcp__linear-server__create_comment({
  issueId: "LAW-4",
  body: `✅ **Work Block Complete**

All child jobs completed:
- LAW-5: Research Agent Upgrade ✅
- LAW-6: Planning Agent Refactor ✅
- LAW-7: Tracking Agent Updates ✅
[... list all completed children ...]

All PRs merged. Work block ready for closure.`
})
```

**Comment Template for Parent**:
- List all completed child jobs
- Confirm all PRs merged
- Note that work block is ready for closure

**Error Handling**:

If parent update fails, report to Planning Agent but don't block:

```typescript
try {
  await mcp__linear-server__update_issue({ id: "LAW-4", state: "Done" })
} catch (error) {
  // Report error to Planning Agent
  // Continue - job is still complete even if parent update fails
}
```

### Step 4: Report to Planning Agent

**Purpose**: Notify Planning Agent of completion and any issues

**Write completion report** to handoff location (specified by Planning Agent):

**If all updates successful**:

```markdown
**Tracking Agent Completion Report**

✅ **All Linear Updates Complete**

**Child Issue**: LAW-5 updated to Done
**Parent Work Block**: LAW-4 [updated to Done | still has N incomplete children]

**Summary**:
- PR #14 merged successfully
- Linear issues updated
- Work block [complete | in progress]

[If parent complete] Master Dashboard update delegated to Traycer per Phase 7 protocol.

Ready for next job.
```

**If errors occurred**:

```markdown
**Tracking Agent Completion Report**

⚠️ **Linear Updates Completed With Errors**

**Child Issue**: LAW-5 - [updated successfully | update failed, manual intervention needed]
**Parent Work Block**: LAW-4 - [checked, N of M children complete | check failed]

**Errors**:
- [List any errors encountered]

**Action Required**:
- [List manual steps needed to resolve errors]

Job completion confirmed despite Linear update errors.
```

**Important**: Do NOT update Master Dashboard - this is delegated by Traycer per Phase 7 protocol

## Reference

### Complete Example Flow

**Scenario**: LAW-5 (Research Agent Upgrade) complete, parent is LAW-4

```typescript
// Step 1: Update child issue
await mcp__linear-server__update_issue({
  id: "LAW-5",
  state: "Done"
})

await mcp__linear-server__create_comment({
  issueId: "LAW-5",
  body: "✅ Job complete. PR #14 merged."
})

// Step 2: Check parent completion
const parentIssue = await mcp__linear-server__get_issue({ id: "LAW-4" })

const childIssues = await mcp__linear-server__list_issues({
  team: "Linear-First-Agentic-Workflow",
  parentId: "LAW-4"
})

const allDone = childIssues.nodes.every(i => i.state.name === "Done")

// Step 3: Update parent if all children complete
if (allDone) {
  // All 9 child jobs complete
  await mcp__linear-server__update_issue({
    id: "LAW-4",
    state: "Done"
  })

  await mcp__linear-server__create_comment({
    issueId: "LAW-4",
    body: "✅ All 9 child jobs complete. Work block done."
  })
}

// Step 4: Report to Planning Agent
// Write completion report to handoff location
// Do NOT update Master Dashboard (delegated by Traycer)
```

### Branch Creation Context

**Note**: This skill executes AFTER branch creation and PR merge

**7-Phase TDD Workflow**:
1. **Phase 1**: Research (no branch yet)
2. **Phase 2**: Spec clarification (no branch yet)
3. **Phase 3**: Linear Enrichment (no branch yet)
4. **Just before Phase 4**: Create branch
5. **Phase 4-6**: QA creates tests → Action implements → QA validates (on branch)
6. **Phase 7**: Tracking Agent handles PR/docs and Linear updates ← **This skill**

**Branch Naming Convention** (for reference):

Pattern: `feat/<parent-issue-id>-<child-issue-id>-<slug>`

Examples:
```bash
# Work Block: LAW-4, Child Job: LAW-5
feat/law-4-law-5-research-agent-upgrade

# Work Block: LAW-350, Child Job: LAW-351
feat/law-350-law-351-webhook-server-setup
```

### Related Tools

- **Linear MCP**: `mcp__linear-server__update_issue`, `mcp__linear-server__get_issue`, `mcp__linear-server__list_issues`, `mcp__linear-server__create_comment`
- **Project Context**: `.project-context.md` (contains team name for Linear queries)
- **Handoff Files**: Planning Agent provides child/parent issue IDs

### Related Documentation

- **Original Reference**: [post-job-linear-updates.md](/srv/projects/traycer-enforcement-framework-dev/docs/agents/shared-ref-docs/post-job-linear-updates.md) (deprecated - use this skill instead)
- **Agent Prompts**:
  - Tracking Agent: `docs/agents/tracking/tracking-agent.md`
  - Planning Agent: `docs/agents/planning/planning-agent.md`
- **Related Ref-Docs**:
  - `tdd-workflow-protocol.md` - Full 7-phase TDD workflow
  - `master-dashboard-creation-protocol.md` - Dashboard update protocol (delegated by Traycer)
  - `linear-update-protocol.md` - General Linear API usage

### Decision Matrix

| Condition | Action |
|-----------|--------|
| Child update succeeds | Proceed to parent check |
| Child update fails | Add error comment, continue to parent check |
| All children Done | Update parent to Done, add completion comment |
| Some children incomplete | Skip parent update, report status to Planning Agent |
| Parent update fails | Report error, continue (don't block on parent failure) |
| All updates complete | Report success to Planning Agent |

### Common Pitfalls to Avoid

**❌ Don't**: Update Master Dashboard directly
- **Why**: Dashboard updates are delegated by Traycer per Phase 7 protocol
- **Instead**: Report completion to Planning Agent, let Traycer coordinate dashboard update

**❌ Don't**: Block if parent update fails
- **Why**: Child job is complete regardless of parent status
- **Instead**: Report error to Planning Agent, mark job as complete

**❌ Don't**: Assume all children Done without querying
- **Why**: Another agent might have deferred a child job
- **Instead**: Always query all child issues and check state

**❌ Don't**: Update child issue state to "Closed" or "Canceled"
- **Why**: "Done" is the correct state for completed jobs
- **Instead**: Always use "Done" state

### Version History

- v1.0 (2025-11-05): Converted from post-job-linear-updates.md to skill format
  - Extracted 3-step workflow from reference doc
  - Added error handling examples
  - Clarified decision points and delegation boundaries
  - Included complete example flow
