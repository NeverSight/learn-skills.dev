---
name: merge-conflict-resolution
description: Resolve git merge/rebase conflicts safely without losing intended changes.
---

# Merge Conflict Resolution

## Purpose
Prevent accidental loss of intended changes when a git merge or rebase hits conflicts (e.g., documentation regressions like the `docs/architecture.md` incident referenced in Feature 024).

This skill is intended for **any agent** that can commit changes.

## Core Principle
A conflict is not a “choose ours/theirs” problem — it’s an **intent reconciliation** problem.

You must understand the intent of *both* changes before resolving anything. The correct resolution depends on intent, not on which side is `main`.

Often the right answer is “keep the intent of both changes”, which may require a manual edit that combines or restructures content.

Sometimes, intent is genuinely contradictory and cannot be resolved automatically. In that case, ask the user how to proceed.

## Hard Rules

### Must
- Analyze both sides first:
  - Identify what each side is trying to achieve (intent).
  - Identify which parts are compatible (can be merged) vs contradictory (need a decision).
- If the intent of either change is unclear, **ask the user questions until it is clear**. Do not guess.
- Resolve conflicts by editing the conflicted file(s) (not by blindly choosing one side).
- After resolution:
  - Verify that no conflict markers remain (`<<<<<<<`, `=======`, `>>>>>>>`).
  - Verify that `scripts/git-status.sh` shows no unmerged paths.
  - Validate that the resolved content preserves the intent of both changes (or reflects an explicit user decision when intent conflicts).

### Must Not
- Blindly run `git checkout --ours <file>` / `git checkout --theirs <file>` without validating intent.
- “Resolve” by deleting sections just to make conflicts disappear.
- Commit a conflict resolution without reviewing the resulting diff.

## When to Ask the Maintainer
If the conflict touches **source-of-truth docs** (e.g., `docs/spec.md`, `docs/architecture.md`) and the correct content is not unambiguous from the current task context, you must **ask the maintainer which version to keep/merge** before committing.

If the two change intents are contradictory (both cannot be true at the same time), you must ask the user to choose a direction. Do not attempt to “average” or invent a new intent.

## Required Analysis (Before Editing)

Before you modify any conflicted file, produce an explicit analysis in chat using this template:

```text
Conflict analysis

Change A intent:
- <what this change is trying to achieve>

Change B intent:
- <what this change is trying to achieve>

Compatibility:
- Compatible / Partially compatible / Contradictory
- Notes: <why>

Proposed resolution:
- <how you will preserve the intent of both changes>

Open questions (must answer before proceeding):
- <question 1>
```

If you cannot confidently state the intent for both changes, stop and ask.

## Clarifying Questions (When Intent Is Unclear)
If you are in doubt about the intent of a change, ask questions until you understand it. Useful prompts:
- “Which behavior/statement should be true after this merge?”
- “Is this change a refactor (no behavior change) or a behavior change?”
- “Do we need to keep both changes, or should one override the other?”
- “If both changes cannot be kept, which one is more important and why?”
- “Is there a spec/issue/PR description that defines the intended outcome?”

## Workflow (Recommended)

### 0. Confirm you are actually in a conflict
Use git to confirm the conflict state and list conflicted files:
```bash
scripts/git-status.sh
git diff --name-only --diff-filter=U
```

### 1. Identify conflicted files
```bash
scripts/git-status.sh
# or (machine-friendly)
git diff --name-only --diff-filter=U
```

### 2. Understand “ours” vs “theirs”
- During a **merge**:
  - “ours” = current branch (where you ran `git merge ...`)
  - “theirs” = the branch you’re merging in
- During a **rebase**:
  - “ours” / “theirs” semantics are different — prefer reading the conflict markers and using diffs rather than relying on naming.

### 3. Inspect what each side changed
For each conflicted file:
```bash
# See conflict hunks and surrounding context
sed -n '1,200p' <file>

# Compare current index stages (2=ours, 3=theirs) if available
# (These commands are safe even if a stage is missing.)
git show :2:<file> 2>/dev/null | head -50 || true
git show :3:<file> 2>/dev/null | head -50 || true
```

While inspecting, explicitly determine intent:
- What was added/removed/renamed, and why?
- Is one side a refactor and the other a feature? If yes, the resolution often needs both.
- Are there invariants that must remain true (docs accuracy, API behavior, tests)?

### 4. Resolve conflicts intentionally
- Edit the file to combine the correct parts from both sides.
- Remove conflict markers.
- Preserve required sections (especially for documentation).

### 5. Verify resolution quality
```bash
# Review what you’re about to commit
scripts/git-diff.sh

# Ensure git sees conflicts as resolved
scripts/git-status.sh
```

Also do a repo-wide check that no conflict markers remain. Prefer tooling that searches files directly (no scripts required), for example:
- VS Code Search panel: search for `<<<<<<< `, `=======`, and `>>>>>>> `
- If you are operating as a Copilot agent: use the workspace text-search tool to search for `<<<<<<<`, `=======`, and `>>>>>>>`
- Optional fallback (terminal): `git grep -n '^<<<<<<< ' || true` (repeat for the other markers)

### 6. Validate the *meaning*, not just the markers
After conflicts are resolved, validate correctness based on file type:

- Documentation changes:
  - Ensure the resulting documentation captures the intent of both changes and no relevant information is lost.
  - Ensure the docs do not contain contradictory statements introduced by the merge.
  - Check for common merge-regressions:
    - Deleted or duplicated headings/sections
    - Outdated statements reintroduced
    - Partial merges where one side’s detail vanished
  - If there are contradictions, resolve them explicitly or ask the user which statement is correct.

- Code changes:
  - Ensure all tests pass.
  - Ensure the intended new features or behavior changes of both changes still work.
  - If tests exist for the changed area, run those first; then broaden if needed.

### 7. Continue or conclude
- If this is a **merge**:
  ```bash
  git add <file>...
  git commit
  ```
- If this is a **rebase**:
  ```bash
  git add <file>...
  git rebase --continue
  ```

## Commit Message Requirement (For Merge Conflict Resolutions)
When you create a commit that resolves conflicts, the commit message must describe:
- Which files had conflicts (high level)
- How the conflict was resolved (e.g., “combined both intents”, “kept X and adapted Y to match”, “user chose A over B”)
- Why this resolution preserves the intended behavior/documentation

Template:
```text
<type>: resolve merge conflicts

Conflicts:
- <file/group>: <what conflicted>

Resolution:
- <how you preserved intent of both changes OR what decision was made>

Why:
- <why this is correct>
```

## Notes
- If you get stuck, prefer asking for guidance over guessing. A wrong conflict resolution can silently ship broken docs.
