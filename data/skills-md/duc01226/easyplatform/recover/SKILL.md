---
name: recover
description: '[Tooling & Meta] Restore workflow context from checkpoint after session loss'
---

# Recover Workflow Context

Restore workflow state and todo items from checkpoint files after context compaction or session loss.

## Usage

Use this command when:

- Context was compacted and you've lost track of the workflow
- Session was interrupted and needs to resume
- Todo items need to be restored from a checkpoint
- The automatic recovery didn't trigger

## Recovery Process

### Step 1: Find Latest Checkpoint

Look for checkpoint files in the reports directory:

```bash
ls -la plans/reports/memory-checkpoint-*.md | tail -5
```

Or search for all recent checkpoints:

```bash
find plans -name "memory-checkpoint-*.md" -mmin -60 | head -5
```

### Step 2: Read Checkpoint File

Read the most recent checkpoint to understand the saved state:

```
Read the checkpoint file at: plans/reports/memory-checkpoint-YYMMDD-HHMMSS.md
```

### Step 3: Extract Recovery Metadata

The checkpoint file contains a JSON metadata block at the end:

```json
{
  "sessionId": "...",
  "activePlan": "plans/YYMMDD-slug/",
  "workflowType": "feature",
  "currentStep": "cook",
  "remainingSteps": ["test", "code-review"],
  "pendingTodos": [...]
}
```

### Step 4: Restore Todo Items

**IMMEDIATELY call TodoWrite** with the pending todos from the checkpoint.

### Step 5: Read Active Plan (if exists)

If `activePlan` is set in the metadata, read the plan file.

### Step 6: Continue Workflow

Resume from the `currentStep` identified in the metadata. Execute the remaining workflow steps in order.

## Recovery Checklist

- [ ] Located most recent checkpoint file
- [ ] Read checkpoint content
- [ ] Extracted recovery metadata JSON
- [ ] Restored todo items via TodoWrite
- [ ] Read active plan (if applicable)
- [ ] Identified current workflow step
- [ ] Ready to continue from interrupted step

## Automatic vs Manual Recovery

| Scenario                      | Recovery Type | Trigger                   |
| ----------------------------- | ------------- | ------------------------- |
| Session resume after compact  | Automatic     | `session-resume.cjs` hook |
| New session in same directory | Manual        | This `/recover` command   |
| Explicit user request         | Manual        | This `/recover` command   |
| No workflow state found       | Manual        | This `/recover` command   |

## Related Commands

- `/checkpoint` - Create a manual checkpoint (before expected loss)
- `/compact` - Manually trigger context compaction
- `/context` - Load project context
- `/watzup` - Generate progress summary

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
