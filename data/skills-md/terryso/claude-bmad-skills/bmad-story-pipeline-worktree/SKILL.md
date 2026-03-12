---
name: bmad-story-pipeline-worktree
description: Run configurable BMAD pipeline in isolated worktree, merge only after tests pass
argument-hint: <story-number> e.g., 1-1 or 2-3 (optional, auto-selects if omitted)
---

# BMAD Story Pipeline (Worktree Edition)

Complete the delivery pipeline for story `{ARGUMENT}` using configurable workflow in an isolated git worktree, merge to main branch only after all tests pass.

## Pre-step: Determine Story Number

If `{ARGUMENT}` is empty or not provided:

1. Read `_bmad-output/implementation-artifacts/sprint-status.yaml` (or `docs/sprint/sprint-status.yaml`) to find stories
2. Find the first story with status "todo" or "in-progress"
3. Use that story number as `{STORY_ID}`
4. If no story found, ask user to specify story number

The story number format is typically `X-Y` (e.g., `1-1`, `2-3`).

Set `STORY_ID = {ARGUMENT}` for all subsequent steps.

---

## Difference from bmad-story-pipeline

| Feature | bmad-story-pipeline | bmad-story-pipeline-worktree |
|---------|---------------------|------------------------------|
| Working method | Develop on current branch | Develop in isolated worktree |
| Code isolation | None | Complete isolation |
| Merge condition | None enforced | Tests pass + fixes complete |
| Workflow config | workflow-steps.md | workflow-steps.md |
| Safety level | Medium | High |

---

## Phase 1: Create Worktree

**Do this yourself (not via Task agent):**

```
1. Get current project name, path and branch:
   ORIGINAL_REPO_PATH=$(pwd)
   PROJECT_NAME=$(basename $(pwd))
   CURRENT_BRANCH=$(git branch --show-current)

2. Create new branch name: feature/story-${STORY_ID}

3. Create worktree directory (in sibling directory):
   WORKTREE_PATH="../${PROJECT_NAME}-story-${STORY_ID}"

4. Execute git worktree command:
   git worktree add -b feature/story-${STORY_ID} "$WORKTREE_PATH" $CURRENT_BRANCH

   If branch already exists, use:
   git worktree add "$WORKTREE_PATH" feature/story-${STORY_ID}

5. Verify worktree created:
   git worktree list
```

**Variables saved for later phases:**
- `ORIGINAL_REPO_PATH` - Original repository path (for merge step)
- `WORKTREE_PATH` - Worktree path
- `STORY_ID` - Story number

**Progress output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Create Worktree
   🌿 Branch: feature/story-${STORY_ID}
   📁 Path: ${WORKTREE_PATH}
   📦 Original: ${ORIGINAL_REPO_PATH}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 2: Run Configurable Pipeline

**Switch to worktree directory first, then run the pipeline.**

Read workflow steps from **references/workflow-steps.md**.

Execute each step sequentially using Task tool (general-purpose agent):

```
Task(
  subagent_type: "general-purpose",
  description: "<Step description>",
  prompt: "Execute the command: <COMMAND_WITH_STORY_ID>
Return: 1) Step completion status 2) Key outputs 3) Any issues to note"
)
```

### Example Invocations

**Step 1 - Create Story:**
```
Task(
  subagent_type: "general-purpose",
  description: "Create user story {STORY_ID}",
  prompt: "Execute /bmad-bmm-create-story {STORY_ID} yolo to create story file. Return: 1) Story ID and Title 2) Created files 3) Any issues"
)
```

**Step 2 - ATDD Tests:**
```
Task(
  subagent_type: "general-purpose",
  description: "Generate ATDD tests for {STORY_ID}",
  prompt: "Execute /bmad-tea-testarch-atdd {STORY_ID} yolo to generate acceptance tests. Return: 1) ATDD checklist 2) Test files created 3) Any issues"
)
```

**Step 3 - Development:**
```
Task(
  subagent_type: "general-purpose",
  description: "Develop user story {STORY_ID}",
  prompt: "Execute /bmad-bmm-dev-story {STORY_ID} yolo to implement story code. Return: 1) Modified files 2) Summary of changes 3) Any issues"
)
```

**Step 4 - Code Review:**
```
Task(
  subagent_type: "general-purpose",
  description: "Code review for {STORY_ID}",
  prompt: "Execute /bmad-bmm-code-review {STORY_ID} yolo for adversarial review. Return: 1) Conclusion (pass/needs-fix) 2) Issues by severity 3) Any blocking issues"
)
```

**Step 5 - Trace Coverage:**
```
Task(
  subagent_type: "general-purpose",
  description: "Trace test coverage for {STORY_ID}",
  prompt: "Execute /bmad-tea-testarch-trace {STORY_ID} yolo for traceability matrix. Return: 1) Coverage percentage 2) Gate decision 3) Any gaps"
)
```

### Execution Flow

For each step:
1. Replace `{STORY_ID}` with the actual story number in the prompt
2. Call Task tool with the step's description and prompt
3. Wait for completion and capture result
4. Output progress: `[X/N] Step Name - Status`
5. If step fails, stop and report error

### Progress Display

After each step, output progress:

```
📊 Pipeline Progress: [X/N] ████████░░░░ 40%

✅ Step X: <Step Name>
   Result: <Brief result summary>
```

---

## Phase 3: Merge or Preserve

**Critical decision step: Check merge conditions**

Merge conditions:
1. All pipeline steps completed successfully
2. No HIGH/MEDIUM issues (or all fixed)
3. Tests pass

**If all conditions are met, execute merge yourself:**

```
1. Commit all changes in worktree:
   cd ${WORKTREE_PATH}
   git add .
   git commit -m "feat: complete story ${STORY_ID}"

2. Switch back to main repo:
   cd ${ORIGINAL_REPO_PATH}

3. Merge feature branch:
   git merge feature/story-${STORY_ID} --no-edit

4. Remove worktree:
   git worktree remove ${WORKTREE_PATH}

5. Optionally delete feature branch (if not needed):
   git branch -d feature/story-${STORY_ID}

6. Verify cleanup:
   git worktree list
```

**Progress output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Merge Branch
   🔀 Merge: feature/story-${STORY_ID} → [current branch]
   🗑️ Cleanup: worktree removed
   📝 Commit: [hash]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If merge conditions not met, preserve worktree for manual handling:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Merge Branch
   ❌ Merge conditions not met, preserving worktree
   📁 Path: ${WORKTREE_PATH}
   🔧 Manual handling needed:
   - [List unmet conditions]

   After handling, manually execute:
   cd ${WORKTREE_PATH}
   git add . && git commit -m "fix: resolve issues"
   cd ${ORIGINAL_REPO_PATH}
   git merge feature/story-${STORY_ID}
   git worktree remove ${WORKTREE_PATH}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4: Update Status to Done

**After successful merge, update status files.**

### 4.1 Update sprint-status.yaml

Use Edit tool to update status file:

```
File path: _bmad-output/implementation-artifacts/sprint-status.yaml (or docs/sprint/sprint-status.yaml)

Change story status from in-progress to done:
  {epic-num}-{story-num}-{story-name}: done
```

### 4.2 Update Story Document (if exists)

Use Edit tool to update story document status:

```
File path: _bmad-output/implementation-artifacts/{epic-num}-{story-num}-{story-name}.md

Update two places:

1. Top status line:
   Change "Status: in-progress" to "Status: done"

2. Tasks checklist (if any):
   Change all "- [ ]" to "- [x]" to mark tasks complete
```

**Progress output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Update Status
   📝 sprint-status.yaml: ${STORY_ID} → done
   📄 Story doc: Status: done, Tasks: ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Final Delivery Report

**Successful merge:**
```
╔════════════════════════════════════════════════════════╗
║         🎉 BMAD Story Pipeline Complete!               ║
╠════════════════════════════════════════════════════════╣
║  Story: ${STORY_ID}                                    ║
║                                                        ║
║  ✅ Phase 1 - Create Worktree                          ║
║  ✅ Phase 2 - Configurable Pipeline                    ║
║  ✅ Phase 3 - Merge Branch                             ║
║  ✅ Phase 4 - Update Status to Done                    ║
║                                                        ║
║  📊 Status: done                                       ║
╚════════════════════════════════════════════════════════╝
```

**Manual intervention required:**
```
╔════════════════════════════════════════════════════════╗
║     ⚠️ BMAD Story Pipeline - Manual Intervention       ║
╠════════════════════════════════════════════════════════╣
║  Story: ${STORY_ID}                                    ║
║                                                        ║
║  ✅ Phase 1 - Create Worktree                          ║
║  ❌ Phase 2 - Pipeline [failed at Step X]              ║
║  ⏸️ Phase 3 - Merge Branch [not started]               ║
║  ⏸️ Phase 4 - Update Status [not started]              ║
║                                                        ║
║  📁 Worktree: ${WORKTREE_PATH}                         ║
║  💡 Fix the issue and continue manually                ║
╚════════════════════════════════════════════════════════╝
```

---

## Error Handling

If any step fails:
1. Stop executing subsequent steps
2. Preserve worktree (don't delete)
3. Output error information and current state
4. Prompt user how to manually fix
5. Provide recovery commands

**Recovery command examples:**
```bash
# List all worktrees
git worktree list

# Continue working in worktree
cd ${WORKTREE_PATH}

# Commit after manual completion
git add . && git commit -m "fix: manual fix"

# Switch back to main repo and merge
cd ${ORIGINAL_REPO_PATH}
git merge feature/story-${STORY_ID}

# Cleanup worktree
git worktree remove ${WORKTREE_PATH}

# Optional: delete feature branch
git branch -d feature/story-${STORY_ID}
```

---

## Configuration

To customize the pipeline workflow, edit:
**references/workflow-steps.md**

Changes supported:
- Add/remove steps
- Modify step commands
- Reorder steps
- Change descriptions
