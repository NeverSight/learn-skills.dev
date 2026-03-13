---
name: workflow-end
version: 1.0.0
description: '[Process] End the active workflow and clear state. Auto-added as last step of every workflow. Clears workflow tracking so next prompt gets fresh workflow detection.'
allowed-tools: TaskUpdate
---

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Workflow End

Finalize and close the active workflow, clearing state so the next user prompt triggers fresh workflow detection.

---

## When This Runs

This skill is the **last step of every workflow sequence**. It runs automatically after the final functional step (e.g., `/watzup`, `/status`, `/acceptance`).

**NOT for**: Manual invocation mid-workflow (use workflow switching via `/workflow-start` instead).

---

## What To Do

1. Mark this task as `completed` via `TaskUpdate`
2. Announce to the user: "Workflow **[name]** completed. Next prompt will trigger fresh workflow detection."
3. The `workflow-step-tracker` hook handles the actual state cleanup automatically when this skill completes

That's it. The hook does the heavy lifting.

---

## See Also

- **Skill:** `/workflow-start` - Start/switch workflows
- **Hook:** `workflow-step-tracker.cjs` - Clears state on final step completion
- **Hook:** `workflow-router.cjs` - Detects active vs inactive workflows
