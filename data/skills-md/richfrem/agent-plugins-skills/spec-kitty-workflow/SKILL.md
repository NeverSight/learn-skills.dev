---
name: Spec Kitty Workflow
description: Standard operating procedures for the Spec Kitty agentic workflow (Plan -> Implement -> Review -> Merge).
dependencies: ["skill:dual-loop", "skill:spec-kitty-implement", "skill:spec-kitty-merge", "skill:spec-kitty-review"]
---
# Spec Kitty Workflow

Standard lifecycle for implementing features using Spec Kitty.

**Command-specific guidance**: For detailed best practices on individual commands, see the `AUGMENTED.md` files co-located with each auto-synced command:
- `skills/spec-kitty-merge/references/AUGMENTED.md` — pre-merge safety, branch protection, conflict resolution
- `skills/spec-kitty-implement/references/AUGMENTED.md` — worktree discipline, commit hygiene
- `skills/spec-kitty-review/references/AUGMENTED.md` — review standards, batch review protocol

## 🚫 CRITICAL: Anti-Simulation Rules & Escalation Taxonomy

> **YOU MUST ACTUALLY RUN EVERY COMMAND LISTED BELOW.**
> Describing what you "would do", summarizing expected output, or marking
> a step complete without pasting real tool output is a **PROTOCOL VIOLATION**.
>
> **Proof = pasted command output.** No output = not done.

### Escalation Taxonomy (Protocol Violation Response)
If you detect a tool or user attempting to bypass the closure protocol or manually create spec files, you MUST interrupt the workflow using the strict 5-step Escalation Protocol:
1. **Stop**: Halt workflow creation immediately.
2. **Alert**: Loudly print: `🚨 PROTOCOL VIOLATION 🚨`.
3. **Explain**: State precisely which rule was broken (e.g., "Cannot skip review.").
4. **Recommend**: Output the standard operating procedure (e.g., "Please submit WP-xx for review: `spec-kitty review WP-xx`").
5. **Draft**: Refuse to execute the dangerous command until the state is fixed.

### Anti-Pattern Vaccination (Known Agent Failure Modes)
1. **Checkbox theater**: Marking `[x]` without running the command or verification tool
2. **Manual file creation**: Writing spec.md/plan.md/tasks.md by hand instead of using CLI
3. **Kanban neglect**: Not updating task lanes, so dashboard shows stale state
4. **Closure amnesia**: Finishing code but skipping review/merge/closure steps

---

## 0. Mandatory Planning Phase (Do NOT Skip)

Before implementing any code, you MUST generate artifacts using the CLI.
**Manual creation of `spec.md`, `plan.md`, or `tasks/` files is STRICTLY FORBIDDEN.**

### Pre-Execution Workflow Commitment
Before starting, display the following visual map to commit to the workflow state:
```text
┌────────────────────────────────────────────────────────┐
│               SPEC-KITTY LIFECYCLE MAP                 │
├────────────────────────────────────────────────────────┤
│ [ ] Phase 0: Plan (specify -> plan -> tasks)           │
│ [ ] Phase 1: Implement (implement WP -> code -> review)│
│ [ ] Phase 2: Close (accept -> retro -> merge -> sync)  │
└────────────────────────────────────────────────────────┘
```
*Check the box corresponding to your current execution phase.*

### Step 0a: Specify
To specify a feature, read the workflow instructions in `.windsurf/workflows/spec-kitty.specify.md` or use the CLI:
```bash
spec-kitty agent feature create-feature "<slug>"
```
**PROOF**: Paste output confirming spec.md was generated.

### Step 0b: Plan
To plan a feature, read the workflow instructions in `.windsurf/workflows/spec-kitty.plan.md` or use the CLI:
```bash
spec-kitty agent feature setup-plan --feature <SLUG>
```
**PROOF**: Paste output confirming plan.md was generated.

### Step 0c: Tasks
To generate tasks, read the workflow instructions in `.windsurf/workflows/spec-kitty.tasks.md`.
```bash
/spec-kitty.tasks
```
**PROOF**: Paste output confirming tasks.md and WP files were generated.

---

## 1. Start a Work Package (WP)

### Step 1a: Create worktree
```bash
spec-kitty agent workflow implement --task-id <WP-ID> --agent "<AGENT-NAME>"
```
**PROOF**: Paste the output. Extract the worktree path from it.

If output is truncated or unclear:
```bash
git worktree list
```
**CRITICAL**: Do NOT guess the path. Verify it exists before proceeding.

### Step 1b: Update kanban
```bash
python3 .kittify/scripts/tasks/tasks_cli.py update <FEATURE-SLUG> <WP-ID> doing --note "Starting implementation"
```
**PROOF**: Paste the CLI output confirming lane change.

Then verify the board:
```bash
/spec-kitty.status
```
**PROOF**: Paste the kanban board. Confirm your WP shows in "doing" lane.
**STOP**: Do NOT start coding until the kanban shows the WP in "doing".

---

## 2. Implementation Loop

1. **Navigate**: `cd .worktrees/<WP-ID>` — verify with `pwd`
2. **Setup**: Install dependencies if needed
3. **Code**: Implement the feature
4. **Test**: Run tests or manual verification
5. **Commit**: `git add . && git commit -m "feat(<WP>): description"` (local worktree)

---

## 3. Review & Handover

### Pre-Review Checklist (verify ALL before proceeding)
- [ ] All files committed in worktree (`git status` shows clean)
- [ ] Worktree path confirmed (`pwd` matches `.worktrees/<WP-ID>`)
- [ ] WP lane is `doing` (not already `for_review` or `done`)
- [ ] No untracked files that should be committed

### Step 3a: Verify clean state
Run `git status` to ensure all files are committed.
**PROOF**: Paste the output. Must show "nothing to commit, working tree clean".
**STOP**: Do NOT proceed if there are uncommitted changes.

### Step 3b: Update kanban to for_review
```bash
python3 .kittify/scripts/tasks/tasks_cli.py update <FEATURE-SLUG> <WP-ID> for_review --note "Implementation complete, ready for review"
```
**PROOF**: Paste the CLI output.

### Step 3c: Verify kanban updated
```bash
/spec-kitty.status
```
**PROOF**: Paste the board. WP must show in "for_review" lane.

### Step 3d: Sync specs in main repo
```bash
cd <PROJECT_ROOT>
git add kitty-specs
git commit -m "docs(specs): mark <WP-ID> complete"
```

---

## 4. Deterministic Closure Protocol

> **CRITICAL**: Every step below is MANDATORY. Skipping any step is a protocol violation.
> The closure chain is: **Review → Accept → Retrospective → Merge → Verify → Intel Sync**

### Step 4a: Review each WP
```bash
spec-kitty agent workflow review --task-id <WP-ID>
```
**PROOF**: Paste the review output. WP must move to `done` lane.

Repeat for each WP. Verify all WPs are in `done` lane:
```bash
/spec-kitty.status
```
**PROOF**: Paste the board. ALL WPs must show in "done" lane before proceeding.

### Step 4b: Accept feature
```bash
cd <PROJECT_ROOT>
spec-kitty accept --feature <SLUG>
```
The agent will ask for acceptance mode:
- **`--mode local`**: Merge locally (no branch protection on target)
- **`--mode pr`**: Push to feature branch and create PR (for protected branches)
- **`--mode checklist`**: Readiness check only, no merge

**PROOF**: Paste the JSON output showing `summary.ok: true`.

> **Known Issue**: Accept may fail with "missing shell_pid in WP frontmatter".
> **Fix**: Add `shell_pid: N/A` to the WP frontmatter, or use `--lenient` flag:
> ```bash
> spec-kitty accept --mode local --feature <SLUG> --lenient
> ```

**STOP**: Do NOT proceed if accept fails. Resolve all outstanding issues first.

### Step 4c: Retrospective (MANDATORY)
```bash
/spec-kitty_retrospective
```
**PROOF**: Paste confirmation that `kitty-specs/<SPEC-ID>/retrospective.md` was created/updated.

> **This step is NOT optional.** Every feature closure MUST include a retrospective.
> The retrospective file MUST exist in `kitty-specs/<SPEC-ID>/` before merge.

### Step 4d: Pre-merge remote backup (MANDATORY)

> ⚠️ **DATA SAFETY**: Before ANY merge or worktree cleanup, ALL WP branches
> MUST be pushed to GitHub origin and verified. This prevents data loss if
> the merge fails or worktrees are deleted before content is preserved.

**Push each WP branch to origin:**
```bash
cd <PROJECT_ROOT>
for wt in .worktrees/<FEATURE>-WP*/; do
  branch=$(basename "$wt")
  echo "Pushing $branch..."
  git -C "$wt" push origin "$branch"
done
```
**PROOF**: Paste push output for each branch.

**Verify remote state:**
```bash
for wt in .worktrees/<FEATURE>-WP*/; do
  branch=$(basename "$wt")
  local_sha=$(git -C "$wt" rev-parse HEAD)
  remote_sha=$(git ls-remote origin "$branch" | cut -f1)
  if [ "$local_sha" = "$remote_sha" ]; then
    echo "✅ $branch: verified on origin ($local_sha)"
  else
    echo "❌ $branch: MISMATCH (local=$local_sha remote=$remote_sha)"
  fi
done
```
**PROOF**: Paste verification output. ALL branches must show ✅.
**STOP**: Do NOT proceed to merge if any branch shows ❌.

### Step 4e: Pre-merge safety check (deterministic forecasting)
```bash
cd <PROJECT_ROOT>
git status
git worktree list
spec-kitty merge --feature <SLUG> --dry-run --json
```
**PROOF**: Paste all outputs. From the JSON, verify:
- [ ] You are in the **main repo root** (NOT inside a worktree)
- [ ] `git status` shows clean working tree
- [ ] `effective_wp_branches` lists only the branches that need merging
- [ ] `all_wp_branches` may be larger than `effective_wp_branches` (expected)
- [ ] No conflict warnings in the output

> **v1.0.1 Feature**: The `--dry-run --json` flag outputs a deterministic merge plan
> showing exactly which branches will be merged. Confirm the effective tips before proceeding.

### Step 4f: Merge from main repo
```bash
cd <PROJECT_ROOT>
spec-kitty merge --feature <SLUG> --push
```

> **ALWAYS use `--push`** to ensure merged main is immediately backed up to origin.
> Without `--push`, worktree cleanup can destroy the only copies of feature branches.

> **LOCATION RULE**: ALWAYS run merge from the **main repository root**.
> NEVER `cd` into a worktree to merge. The `@require_main_repo` decorator
> will block execution from worktrees.

If merge fails mid-way:
```bash
spec-kitty merge --feature <SLUG> --resume
```
**PROOF**: Paste the merge output showing success.

### Step 4f: Post-merge verification
```bash
git log --oneline -5
git worktree list
git branch
git status
rm -f .kittify/workspaces/<SLUG>-WP*.json
```
**PROOF**: Paste all outputs. Verify:
- [ ] Merge commit(s) visible in log
- [ ] No orphaned worktrees remain for this feature
- [ ] WP branches have been deleted
- [ ] Working tree is clean
- [ ] Workspace tracking JSONs removed from `.kittify/workspaces/`
282. 
283. ### Step 4g: Update kanban to done
```bash
python3 .kittify/scripts/tasks/tasks_cli.py update <FEATURE-SLUG> <WP-ID> done --note "Merged and cleaned up"
```
**PROOF**: Paste CLI output + final `/spec-kitty.status` board.

---

## Known Back-End Failure Modes

| Failure | Root Cause | Fix |
|:--------|:-----------|:----|
| Merge blocked by `@require_main_repo` | Agent ran merge from inside a worktree | `cd <PROJECT_ROOT>` first, then `spec-kitty merge --feature <SLUG>` |
| Accept fails with "missing shell_pid" | WP frontmatter missing `shell_pid` field | Add `shell_pid: N/A` to frontmatter, or use `--lenient` |
| Orphaned worktrees after merge | Merge failed mid-cleanup | `git worktree remove .worktrees/<WP-FOLDER>` then `git branch -d <WP-BRANCH>` |
| Lost data during merge | Agent merged from worktree instead of main repo | Always use `--feature <SLUG>` flag from project root |
| Retrospective skipped | Agent treated it as optional | Retrospective file must exist before merge is allowed |
| No closure state recorded | No post-merge verification step | Run Step 4f verification checklist |

---

## 5. Dual-Loop Mode (Protocol 133)

When Spec Kitty runs inside a Dual-Loop session, roles are split:

| Step | Who | Action |
|------|-----|--------|
| Specify/Plan/Tasks | **Outer Loop** (Antigravity) | Generates all artifacts |
| Implement | **Outer Loop** creates worktree, then **Inner Loop** codes | Inner Loop receives Strategy Packet |
| Review/Merge | **Outer Loop** | Verifies output, commits, merges |

**Inner Loop constraints**:
- No git commands — Outer Loop owns version control
- Scope limited to the Strategy Packet — no exploratory changes
- If worktree is inaccessible, may implement on feature branch (fallback — log in friction log)

**Cross-reference**: [dual-loop SKILL](../../../agent-loops/skills/dual-loop/SKILL.md) 

---

## 6. Task Management CLI

The tasks CLI manages WP lane transitions. **Always use this instead of manually editing frontmatter or checkboxes.**

```bash
# Move a WP between lanes (planned -> doing -> for_review -> done)
python3 .kittify/scripts/tasks/tasks_cli.py update <FEATURE-SLUG> <WP-ID> <LANE> --note "reason"

# Force-move (when kitty-specs artifacts leak from serial implementation)
python3 .kittify/scripts/tasks/tasks_cli.py update <FEATURE-SLUG> <WP-ID> done --force --note "reason"

# View kanban board
/spec-kitty.status

# Accept feature readiness
spec-kitty accept --feature <FEATURE-SLUG>

# Validate encoding (prevents dashboard blank pages)
spec-kitty validate-encoding --feature <FEATURE-SLUG>
spec-kitty validate-encoding --feature <FEATURE-SLUG> --fix
```

**Valid lanes**: `planned`, `doing`, `for_review`, `done`

**Dashboard**: `/spec-kitty.dashboard` reads lane data from WP frontmatter.

---

## Common Issues

- **"Base workspace not found"**: WP depends on a merged WP. Create worktree off `main`:
  ```bash
  git worktree add .worktrees/<WP-FOLDER> main
  cd .worktrees/<WP-FOLDER>
  git checkout -b <WP-BRANCH-NAME>
  ```
- **"Already on main"**: Merge commands must run from project root, not inside a worktree.
- **Kanban not updating**: Verify you're using the CLI, not manually editing frontmatter.
