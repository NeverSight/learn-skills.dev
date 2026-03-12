---
name: bmad-epic-pipeline-worktree
description: Deliver entire Epic using configurable pipeline in isolated worktrees
argument-hint: <epic-number> e.g., 1 or 2 (optional, auto-selects smallest epic with incomplete stories if omitted)
---

# BMAD Epic Pipeline (Worktree Edition)

Deliver all incomplete user stories in Epic `{ARGUMENT}` using configurable pipeline, each story developed in isolated worktree and merged only after tests pass.

## Pre-step: Determine Epic Number

**If no epic number is provided (`{ARGUMENT}` is empty):**

1. Read `_bmad-output/implementation-artifacts/sprint-status.yaml` (or `docs/sprint/sprint-status.yaml`)
2. Find all stories with status not `done` (format: `X-Y-story-name`)
3. Extract Epic numbers X from these stories
4. Select the smallest Epic number as `{ARGUMENT}`
5. Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Auto-selected Epic: {ARGUMENT} (has incomplete stories)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example:**
- Status file has `3-2-llm-prompt-template: backlog`, `3-3-xxx: in-progress`, `4-1-xxx: done`
- Incomplete Epics: 3
- Auto-select Epic: 3

---

## Difference from bmad-epic-worktree

| Feature | bmad-epic-worktree | bmad-epic-pipeline-worktree |
|---------|-------------------|------------------------------|
| Story delivery | bmad-story-worktree | bmad-story-pipeline-worktree |
| Workflow config | Fixed 8-step flow | Configurable via workflow-steps.md |
| Customization | Limited | Full pipeline customization |
| Safety level | High | High |

---

## Execution Strategy

1. Read all incomplete stories under the Epic
2. Sort by Story number ascending
3. Execute `/bmad-story-pipeline-worktree` for **each** story sequentially
4. Only start next story after previous one completes
5. If any story fails, stop and preserve current state

---

## Execution Flow

### Step 1: Collect Epic Story List

Read sprint-status.yaml, collect all incomplete stories under specified Epic:

```
Task(
  subagent_type: general-purpose,
  description: "Collect Epic {ARGUMENT} story list",
  prompt: "Read _bmad-output/implementation-artifacts/sprint-status.yaml (or docs/sprint/sprint-status.yaml), collect all stories for Epic {ARGUMENT}:

1. Filter entries with key format '{ARGUMENT}-Y-story-name'
2. Keep only stories with status not 'done'
3. Sort by Story number Y ascending
4. Return story list with format:
   - Story number: 'X.Y', Story name, Current status
   - Number of incomplete stories

If no incomplete stories found, return 'Epic {ARGUMENT} has no incomplete stories'"
)
```

**Progress output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Epic {ARGUMENT} - Story List

   Story  | Name                    | Status
   -------|-------------------------|--------
   {ARGUMENT}.1 | {story-name-1}     | backlog
   {ARGUMENT}.3 | {story-name-3}     | in-progress
   ...

   📊 Total: {N} incomplete stories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 2~N: Deliver Stories Sequentially

**For each incomplete story, execute in order:**

```
For story {STORY_NUM} (i-th of N total):

Execute /bmad-story-pipeline-worktree {STORY_NUM}

Wait for completion before continuing to next story
```

**Each story delivery progress:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Story [{i}/{N}]: {STORY_NUM}
   📝 Name: {story-name}
   ⏳ Executing configurable pipeline...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[... Execute bmad-story-pipeline-worktree phases ...]
   Phase 1: Create Worktree
   Phase 2: Configurable Pipeline (from workflow-steps.md)
   Phase 3: Merge Branch
   Phase 4: Update Status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Story [{i}/{N}]: {STORY_NUM} Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If any story fails:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Story [{i}/{N}]: {STORY_NUM} Failed
   ⚠️ Stopping subsequent story delivery
   📁 Please handle manually before continuing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Final Delivery Report

**All complete:**
```
╔════════════════════════════════════════════════════════╗
║         🎉 BMAD Epic Pipeline Complete!                ║
╠════════════════════════════════════════════════════════╣
║  Epic: {ARGUMENT}                                      ║
║                                                        ║
║  ✅ Story 1: {story-1} - done                          ║
║  ✅ Story 2: {story-2} - done                          ║
║  ...                                                   ║
║  ✅ Story N: {story-N} - done                          ║
║                                                        ║
║  📊 Total: {N}/{N} stories completed                   ║
║  🎯 Epic status: done                                  ║
╚════════════════════════════════════════════════════════╝
```

**Partial completion (has failures):**
```
╔════════════════════════════════════════════════════════╗
║      ⚠️ BMAD Epic Pipeline - Partial Completion        ║
╠════════════════════════════════════════════════════════╣
║  Epic: {ARGUMENT}                                      ║
║                                                        ║
║  ✅ Story 1: {story-1} - done                          ║
║  ✅ Story 2: {story-2} - done                          ║
║  ❌ Story 3: {story-3} - failed                        ║
║  ⏸️ Story 4: {story-4} - not started                   ║
║  ...                                                   ║
║                                                        ║
║  📊 Progress: {completed}/{total} stories completed    ║
║  📁 Failed story: {failed-story}                       ║
║  💡 Handle failed story then re-run to continue        ║
╚════════════════════════════════════════════════════════╝
```

---

## Error Handling

If any story delivery fails:
1. Stop subsequent story delivery
2. Preserve failed story's worktree (if any)
3. Output failure information and completed progress
4. Prompt user to handle manually

**Resume delivery:**
```bash
# 1. Manually fix failed story
cd {WORKTREE_PATH}
# Fix issues...
git add . && git commit -m "fix: resolve issues"
cd {ORIGINAL_REPO_PATH}
git merge feature/story-{STORY_NUM}
git worktree remove {WORKTREE_PATH}

# 2. Re-run epic delivery, will auto-skip completed stories
/bmad-epic-pipeline-worktree {ARGUMENT}
```

---

## Configuration

Pipeline workflow uses `bmad-story-pipeline-worktree`'s configuration.

To customize the pipeline, edit:
**bmad-story-pipeline-worktree/references/workflow-steps.md**

Changes supported:
- Add/remove steps
- Modify step commands
- Reorder steps
- Change descriptions

---

## Relationship with bmad-story-pipeline-worktree

- **bmad-epic-pipeline-worktree** is the batch version of **bmad-story-pipeline-worktree**
- Internally loops to call `/bmad-story-pipeline-worktree {story-num}`
- Each story has independent worktree, independent pipeline, independent merge
- Guarantees sequential execution, next starts only after previous completes
- Each story completion auto-updates: sprint-status.yaml + story design document
- Uses configurable workflow from workflow-steps.md
