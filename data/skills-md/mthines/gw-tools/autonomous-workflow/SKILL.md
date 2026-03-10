---
name: autonomous-workflow
description: >
  Autonomous feature development workflow using isolated worktrees.
  Use to autonomously implement features from task description through tested PR delivery.
  Handles worktree creation, implementation, testing, iteration, documentation, and PR creation.
  Triggers on autonomous feature development, end-to-end implementation, or "implement X autonomously."
license: MIT
metadata:
  author: mthines
  version: '2.0.0'
  workflow_type: autonomous
  phases:
    - validation_questions
    - intake_planning
    - worktree_setup
    - implementation
    - testing_iteration
    - documentation
    - pr_creation
    - cleanup
---

# Autonomous Workflow

Execute complete feature development cycles autonomously—from task intake through tested PR delivery—using isolated Git worktrees.

---

## ⚠️ CRITICAL: Before Starting ANY Work

**You MUST complete these steps IN ORDER before writing any code:**

### Step 1: Detect Workflow Mode (MANDATORY)

Analyze the task scope to determine the workflow mode:

| Mode     | Criteria                             | Artifacts Required  |
| -------- | ------------------------------------ | ------------------- |
| **Full** | 4+ files OR complex/architectural    | **YES - MANDATORY** |
| **Lite** | 1-3 files AND simple/straightforward | No                  |

**When in doubt, choose Full Mode.**

### Step 2: Create Artifact Files (Full Mode ONLY)

For **Full Mode**, you MUST create these files in `.gw/{branch-name}/` **BEFORE Phase 1 Planning begins**:

```bash
# Create artifact directory
mkdir -p .gw/{branch-name}

# Create required files
touch .gw/{branch-name}/task.md
touch .gw/{branch-name}/plan.md
```

| File             | Purpose                                | When to Update                      |
| ---------------- | -------------------------------------- | ----------------------------------- |
| `task.md`        | Dynamic checklist, decisions, blockers | **At milestones (every 2-3 files)** |
| `plan.md`        | Implementation strategy, file list     | After Phase 1 analysis              |
| `walkthrough.md` | Final summary for PR                   | Phase 6 (MANDATORY)                 |

**⛔ DO NOT proceed to implementation without these files for Full Mode tasks.**

---

## ⚠️ ARTIFACT UPDATE TRIGGERS (Full Mode)

**Update `.gw/{branch}/task.md` at these key points:**

| Trigger                         | Update Action                     |
| ------------------------------- | --------------------------------- |
| Logical milestone (2-3 files)   | Batch update Completed items      |
| Phase transition                | Update Status section, move items |
| Decision made                   | Add row to Decisions Log          |
| Test iteration (fail→fix→rerun) | Log result in Test Iterations     |
| Blocker encountered             | Update Blockers section           |

**Batch updates preferred**: Update after completing a logical unit of work rather than after every single file. This reduces overhead while maintaining visibility.

### Step 3: Announce Mode Selection

State your mode selection explicitly:

> "This is a **Full Mode** task (affects 5+ files). Creating `.gw/{branch-name}/` artifacts now."

or

> "This is a **Lite Mode** task (2 files, simple fix). Proceeding without artifacts."

---

## Prerequisites: gw CLI Installation

Before Phase 2 (Worktree Setup), verify the `gw` CLI is installed:

```bash
which gw
```

### If gw is NOT installed

**STOP and prompt the user to install gw.** The workflow cannot proceed without it.

**Installation options (present to user):**

```bash
# Via npm (recommended)
npm install -g @gw-tools/gw

# Via Homebrew (macOS)
brew install mthines/gw-tools/gw

# Via pnpm
pnpm add -g @gw-tools/gw
```

**After installation, set up shell integration:**

```bash
# For zsh (add to ~/.zshrc)
echo 'eval "$(gw install-shell)"' >> ~/.zshrc
source ~/.zshrc

# For bash (add to ~/.bashrc)
echo 'eval "$(gw install-shell)"' >> ~/.bashrc
source ~/.bashrc

# For fish (add to ~/.config/fish/config.fish)
echo 'gw install-shell | source' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

**Verify installation:**

```bash
gw --version
gw --help
```

**Then initialize gw in the repository (if not already done):**

```bash
# For existing repositories
gw init

# With auto-copy files (recommended)
gw init --auto-copy-files .env,secrets/ --post-checkout "npm install"
```

Once `gw` is installed and configured, resume the workflow from Phase 2.

---

## Rules

| Rule                                                            | Description                                                                           |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [overview](./rules/overview.md)                                 | **HIGH** - Workflow phases, when to use, expected outcomes                            |
| [smart-worktree-detection](./rules/smart-worktree-detection.md) | **CRITICAL** - Fuzzy match task to current worktree, prompt to continue or create new |
| [phase-0-validation](./rules/phase-0-validation.md)             | **CRITICAL** - MANDATORY - Validate requirements before any work                      |
| [phase-1-planning](./rules/phase-1-planning.md)                 | **HIGH** - Deep codebase analysis and implementation planning                         |
| [phase-2-worktree](./rules/phase-2-worktree.md)                 | **CRITICAL** - MANDATORY - Create isolated worktree with `gw add`                     |
| [phase-3-implementation](./rules/phase-3-implementation.md)     | **HIGH** - Incremental implementation with continuous validation                      |
| [phase-4-testing](./rules/phase-4-testing.md)                   | **CRITICAL** - Fast iteration loop until tests pass (Ralph Wiggum pattern)            |
| [phase-5-documentation](./rules/phase-5-documentation.md)       | **MEDIUM** - Update README, CHANGELOG, API docs                                       |
| [phase-6-pr-creation](./rules/phase-6-pr-creation.md)           | **HIGH** - Create draft PR, deliver results                                           |
| [phase-7-cleanup](./rules/phase-7-cleanup.md)                   | **LOW** - Optional worktree removal after merge                                       |
| [decision-framework](./rules/decision-framework.md)             | **HIGH** - Branch naming, test strategy, iteration decisions                          |
| [error-recovery](./rules/error-recovery.md)                     | **HIGH** - Recovery procedures for common errors                                      |
| [safety-guardrails](./rules/safety-guardrails.md)               | **CRITICAL** - Validation checkpoints, resource limits, rollback                      |
| [parallel-coordination](./rules/parallel-coordination.md)       | **HIGH** - Multi-agent coordination, handoff protocol                                 |
| [artifacts-overview](./rules/artifacts-overview.md)             | **HIGH** - Three-artifact pattern (Task, Plan, Walkthrough), file locations           |
| [task-tracking](./rules/task-tracking.md)                       | **HIGH** - Dynamic task updates throughout workflow                                   |
| [walkthrough-generation](./rules/walkthrough-generation.md)     | **MEDIUM** - Final summary generation at Phase 6                                      |

## Templates

Structured templates for consistent artifact generation:

| Template                                                       | Purpose                |
| -------------------------------------------------------------- | ---------------------- |
| [task.template.md](./templates/task.template.md)               | Dynamic task checklist |
| [plan.template.md](./templates/plan.template.md)               | Implementation plan    |
| [walkthrough.template.md](./templates/walkthrough.template.md) | Final summary          |

## Quick Reference

### Full Mode (4+ files, complex changes)

| Phase             | Command/Action                                                                    |
| ----------------- | --------------------------------------------------------------------------------- |
| 0. Validation     | Ask clarifying questions, get user confirmation                                   |
| 1. Planning       | Analyze codebase, **POPULATE** `.gw/{branch}/task.md` and `plan.md`               |
| 2. Worktree       | `gw add feat/feature-name`                                                        |
| 3. Implementation | Code in worktree, **UPDATE `task.md` at milestones**                              |
| 4. Testing        | `npm test`, **LOG each iteration in `task.md`**                                   |
| 5. Documentation  | Update README, CHANGELOG                                                          |
| 6. PR Creation    | **CREATE `walkthrough.md`**, `gh pr create --draft`, **SHOW walkthrough to user** |
| 7. Cleanup        | `gw remove feat/feature-name` (after merge)                                       |

### Lite Mode (1-3 files, simple changes)

| Phase             | Command/Action                               |
| ----------------- | -------------------------------------------- |
| 0. Validation     | Quick clarification if needed                |
| 1. Planning       | Brief mental plan (no artifact files)        |
| 2. Worktree       | `gw add fix/bug-name` (optional for trivial) |
| 3. Implementation | Code directly, commit when done              |
| 4. Testing        | `npm test`, fix any failures                 |
| 5. PR Creation    | `gh pr create --draft`                       |

## Workflow Modes

| Mode     | Files Changed | Artifacts | Use When                             |
| -------- | ------------- | --------- | ------------------------------------ |
| **Lite** | 1-3 files     | No        | Simple fixes, small enhancements     |
| **Full** | 4+ files      | Yes       | Features, refactors, complex changes |

**Full Mode**: Creates `.gw/{branch}/` artifacts for progress tracking and context recovery.

**Lite Mode**: Faster execution without artifact overhead. Still uses worktree isolation.

## Key Principles

1. **Detect workflow mode FIRST**: Determine Full vs Lite before any other action.
2. **Create artifacts BEFORE planning (Full Mode)**: `.gw/{branch}/task.md` and `plan.md` are MANDATORY.
3. **Always validate first (Phase 0)**: Never skip directly to implementation.
4. **Always create worktree (Phase 2)**: Isolation is mandatory (can skip for trivial fixes).
5. **Update task.md at milestones**: Every 2-3 files or at logical checkpoints (not every file).
6. **Smart worktree detection**: Check if current worktree matches task before creating new.
7. **Iterate until correct**: No artificial iteration limits (Ralph Wiggum pattern).
8. **Fast feedback loops**: Run tests frequently, fix failures immediately.
9. **Self-validate continuously**: Check work at every step.
10. **⛔ CREATE walkthrough.md AND SHOW IT at Phase 6**: This is MANDATORY for Full Mode.
11. **Stop and ask when blocked**: Don't guess on ambiguity.

## Artifact System

Inspired by Google Antigravity, this workflow produces three artifacts in `.gw/{branch-name}/`:

| Artifact        | File             | Created | Purpose                                   |
| --------------- | ---------------- | ------- | ----------------------------------------- |
| **Task**        | `task.md`        | Phase 1 | Dynamic checklist, decisions, discoveries |
| **Plan**        | `plan.md`        | Phase 1 | Implementation strategy                   |
| **Walkthrough** | `walkthrough.md` | Phase 6 | Final summary for PR                      |

Files are gitignored and grouped by branch for easy browsing.

### ⚠️ CRITICAL: Artifact Update Requirements

| Artifact         | Update Frequency                | Blocking Gate                                          |
| ---------------- | ------------------------------- | ------------------------------------------------------ |
| `plan.md`        | Once in Phase 1                 | ⛔ Must be POPULATED (not empty) before Phase 2        |
| `task.md`        | At milestones (every 2-3 files) | ⛔ Must reflect completed work at phase transitions    |
| `walkthrough.md` | Once in Phase 6                 | ⛔ Must be CREATED AND SHOWN to user before completion |

## Workflow Flow

```
┌─────────────────────────────────────────────────────┐
│  MODE DETECTION ← MANDATORY FIRST STEP              │
│  Analyze task → Choose Full (4+ files) or Lite      │
│  Full Mode: Create .gw/{branch}/ artifacts NOW      │
└─────────────────────────────────────────────────────┘
    ↓
Phase 0: Validation ← MANDATORY
    ↓ (user confirms)
Phase 1: Planning
    ⛔ Full Mode: POPULATE plan.md + task.md (not empty!)
    ↓ (plan validated)
Phase 2: Worktree Setup ← MANDATORY (with smart detection)
    ↓ (worktree created)
Phase 3: Implementation
    📝 Full Mode: UPDATE task.md at milestones (every 2-3 files)
    ↓ (code complete)
Phase 4: Testing ← iterate until passing
    📝 Full Mode: LOG each test iteration in task.md
    ↓ (all tests pass)
Phase 5: Documentation
    ↓ (docs complete)
Phase 6: PR Creation
    ⛔ Full Mode: CREATE walkthrough.md + SHOW to user
    ↓ (draft PR delivered)
Phase 7: Cleanup (optional)
```

## Smart Worktree Detection

Before creating a new worktree, the workflow checks if the current context matches the task:

| Scenario                            | Action                                |
| ----------------------------------- | ------------------------------------- |
| On main/master                      | Always create new worktree            |
| Worktree name matches task keywords | Prompt user to continue or create new |
| No keyword match                    | Create new worktree                   |

## Fast Iteration Loop (Phase 4)

Based on the Ralph Wiggum pattern:

```
while not all_tests_pass:
    1. Run tests
    2. If pass: done
    3. If fail: analyze → fix → commit → continue
    4. Safety: warn at 10 iterations, stop at 20
```

## Troubleshooting Quick Reference

| Issue                  | Check                       | Recovery                                                              |
| ---------------------- | --------------------------- | --------------------------------------------------------------------- |
| Wrong worktree         | `gw list`, `pwd`            | `gw cd <correct-branch>`                                              |
| gw command not found   | `which gw`                  | `npm install -g @gw-tools/gw`                                         |
| Secrets missing        | `cat .gw/config.json`       | `gw sync <branch> .env`                                               |
| Agent stuck in loop    | `task.md` iteration history | Try alternative approach, ask user                                    |
| Tests keep failing     | `task.md` test results      | Focus on ONE failure, escalate at 7+                                  |
| Agent hallucinated cmd | Error message               | See [error-recovery](./rules/error-recovery.md#hallucinated-commands) |
| plan.md empty          | `cat .gw/{branch}/plan.md`  | STOP, populate plan.md before proceeding                              |
| task.md not updated    | `cat .gw/{branch}/task.md`  | Update immediately with all completed work                            |
| walkthrough.md missing | `ls .gw/{branch}/`          | Create before announcing completion                                   |

## Related Skills

- [git-worktree-workflows](../git-worktree-workflows/) - Worktree fundamentals
- [gw-config-management](../gw-config-management/) - Configure auto-copy and hooks

## References

Detailed examples and scenarios (loaded on-demand):

- [Complete Workflow Example](./references/autonomous-workflow-complete.md)
- [Error Recovery Scenarios](./references/error-recovery-scenarios.md)
- [Iterative Refinement Example](./references/iterative-refinement.md)

## Research Sources

- [Google Antigravity Artifacts](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/) - Three-artifact pattern
- [Ralph Wiggum AI Coding Loops](https://ralph-wiggum.ai) - Iteration pattern
- [Addy Osmani's LLM Workflow](https://addyosmani.com/blog/ai-coding-workflow/) - Fast feedback loops
- [Claude Code Worktree Support](https://code.claude.com/docs/en/common-workflows) - Best practices
