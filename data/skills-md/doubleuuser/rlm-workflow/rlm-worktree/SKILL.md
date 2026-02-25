---
name: rlm-worktree
description: 'Use when starting any RLM requirement to set up an isolated git worktree. REQUIRED before Phase 1 - creates isolated workspace, verifies clean test baseline, and prevents main branch pollution. Trigger phrases: "create worktree", "worktree isolation", "set up worktree", "do not work on main".'
---

# RLM Git Worktree Isolation (Phase 0)

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing parallel development without switching branches. This prevents:
- Pollution of main/master branch during development
- Accidental commits to production branches
- Context switching overhead
- Conflicts between parallel requirements

**Core Principle:** Systematic directory selection + safety verification = reliable isolation.

**The Iron Law for RLM Worktrees:**
```
NEVER WORK ON MAIN/MASTER BRANCH WITHOUT EXPLICIT CONSENT
```

## Trigger examples

- `Create an isolated worktree for this requirement`
- `Set up Phase 0 worktree isolation for run '2026-02-24-add-oauth'`
- `I'm on main; move me to a worktree`
- `Use .worktrees/ and ensure it is git-ignored`

## When to Use

**REQUIRED for all RLM runs:**
- New features
- Bug fixes
- Refactoring
- Experiments/prototypes

**Insert as Phase 0:**
```
Phase 0R: 00-requirements.md (user-created first)
    ->
Phase 0W: 00-worktree.md (isolated workspace setup; this skill)
    ->
Phase 1: 01-as-is.md
```

## The Worktree Rule

<HG>
Do NOT proceed with any RLM phase until:
1. Isolated worktree is created on feature branch
2. Worktree directory is git-ignored (if project-local)
3. Clean test baseline is verified
4. User has explicitly consented if main branch work requested
</HG>

## Directory Selection Process

### Step 1: Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### Step 2: Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
grep -i "worktrees" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### Step 3: Ask User (if no convention exists)

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden - RECOMMENDED)
2. ~/.config/rlm-workflow/worktrees/<project-name>/ (global location)

Which would you prefer? (1/2)
```

**Default:** `.worktrees/` (option 1)

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify directory is ignored before creating worktree:**

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:**

Per "Fix broken things immediately" rule:
1. Add appropriate line to .gitignore:
   ```
   # RLM worktrees
   .worktrees/
   ```
2. Commit the change:
   ```bash
   git add .gitignore
   git commit -m "chore: ignore RLM worktree directory"
   ```
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### For Global Directory (~/.config/rlm-workflow/worktrees)

No .gitignore verification needed - outside project entirely.

## Worktree Creation Process

### Step 1: Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
branch_name="rlm/${run_id}"
```

### Step 2: Check Current Branch

```bash
current_branch=$(git branch --show-current)

if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
    # STOP - Require explicit consent
    echo "WARNING: Currently on $current_branch branch."
    echo "RLM Workflow requires isolated worktrees."
    echo ""
    read -p "Create worktree and switch to feature branch? (yes/no): " consent
    
    if [ "$consent" != "yes" ]; then
        echo "Aborted. Please run from a feature branch or consent to worktree creation."
        exit 1
    fi
fi
```

### Step 3: Create Worktree with New Branch

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$run_id"
    ;;
  ~/.config/rlm-workflow/worktrees/*)
    path="~/.config/rlm-workflow/worktrees/$project/$run_id"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$branch_name"
cd "$path"
```

### Step 4: Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then 
    echo "Detected Node.js project"
    npm install
fi

# Rust
if [ -f Cargo.toml ]; then 
    echo "Detected Rust project"
    cargo build
fi

# Python
if [ -f requirements.txt ]; then 
    echo "Detected Python project (requirements.txt)"
    pip install -r requirements.txt
elif [ -f pyproject.toml ]; then 
    echo "Detected Python project (pyproject.toml)"
    poetry install || pip install -e .
fi

# Go
if [ -f go.mod ]; then 
    echo "Detected Go project"
    go mod download
fi

# Java/Maven
if [ -f pom.xml ]; then 
    echo "Detected Maven project"
    mvn compile -q
fi

# Java/Gradle
if [ -f build.gradle ] || [ -f build.gradle.kts ]; then 
    echo "Detected Gradle project"
    ./gradlew compileJava --quiet 2>/dev/null || gradlew compileJava --quiet 2>/dev/null
fi

# .NET
if [ -f *.csproj ] || [ -f *.sln ]; then 
    echo "Detected .NET project"
    dotnet restore
fi
```

### Step 5: Verify Clean Test Baseline

Run tests to ensure worktree starts clean:

```bash
# Detect test command and run
if [ -f package.json ]; then
    # Check for npm test script
    if grep -q '"test"' package.json; then
        echo "Running npm test..."
        npm test
    fi
elif [ -f Cargo.toml ]; then
    echo "Running cargo test..."
    cargo test
elif [ -f requirements.txt ] || [ -f pyproject.toml ]; then
    echo "Running pytest..."
    pytest -q || python -m pytest -q
elif [ -f go.mod ]; then
    echo "Running go test..."
    go test ./...
elif [ -f pom.xml ]; then
    echo "Running Maven tests..."
    mvn test -q
elif [ -f build.gradle ] || [ -f build.gradle.kts ]; then
    echo "Running Gradle tests..."
    ./gradlew test --quiet 2>/dev/null || gradlew test --quiet 2>/dev/null
elif [ -f *.csproj ] || [ -f *.sln ]; then
    echo "Running dotnet tests..."
    dotnet test --verbosity quiet
fi
```

**If tests fail:**
- Report failures
- Ask whether to proceed or investigate
- Document decision in Phase 0 artifact

**If tests pass:**
- Report baseline verified
- Record test count and pass rate

### Step 6: Record in Phase 0 Artifact

```markdown
## Worktree Details

**Location:** `/full/path/to/.worktrees/run-id`
**Branch:** `rlm/run-id`
**Created from:** `main` (commit: abc123)
**Setup commands executed:**
- npm install
- npm test (47 passing, 0 failing)

**Baseline verified:** ✅
```

## Main Branch Protection

### Automatic Detection

When user invokes "Implement requirement 'run-id'" from main/master:

```bash
branch=$(git branch --show-current)

if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  !   MAIN BRANCH PROTECTION                                ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║  You are currently on the $branch branch.                  ║"
    echo "║                                                            ║"
    echo "║  RLM Workflow requires isolated worktrees to:             ║"
    echo "║  • Prevent accidental commits to production               ║"
    echo "║  • Enable parallel requirement development                ║"
    echo "║  • Maintain clean main branch history                     ║"
    echo "║                                                            ║"
    echo "║  Options:                                                  ║"
    echo "║  1. Create worktree (RECOMMENDED)                          ║"
    echo "║  2. Switch to existing feature branch                      ║"
    echo "║  3. Abort and run from feature branch                      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Default to worktree creation
    echo "Creating worktree by default (press Ctrl+C to abort)..."
    sleep 3
fi
```

### Explicit Consent Required

If user explicitly requests main branch work:

```markdown
## Main Branch Work Acknowledgment

User has explicitly requested to work on main branch.

**Acknowledged risks:**
- [ ] Commits go directly to production branch
- [ ] No isolation for this requirement
- [ ] Cannot run parallel requirements
- [ ] Harder to discard if abandoned

**Consent:** User has chosen to proceed on main branch
**Reason:** [user-provided reason]
**Recorded:** [timestamp]

**Recommendation:** Use worktrees for future requirements.
```

## Phase 0 Artifact Template

**File:** `/.codex/rlm/<run-id>/00-worktree.md`

```markdown
Run: `/.codex/rlm/<run-id>/`
Phase: `00 Worktree Setup`
Status: `DRAFT` | `LOCKED`
Inputs:
- Current git repository state
- User preference (for worktree location)
Outputs:
- `/.codex/rlm/<run-id>/00-worktree.md`
- Isolated worktree at `[location]`
Scope note: This document records isolated workspace setup and verifies clean test baseline.

## Directory Selection

**Convention checked:**
- [ ] `.worktrees/` exists
- [ ] `worktrees/` exists
- [ ] CLAUDE.md preference found
- [ ] User preference obtained

**Selected location:** `.worktrees/` (project-local, hidden)

## Safety Verification

**Gitignore check:**
```bash
$ git check-ignore -q .worktrees && echo "IGNORED" || echo "NOT IGNORED"
IGNORED
```

**Result:** ✅ Directory is properly ignored

## Worktree Creation

**Command:**
```bash
git worktree add .worktrees/run-id -b rlm/run-id
```

**Output:**
```
Preparing worktree (new branch 'rlm/run-id')
HEAD is now at abc1234 Previous commit message
```

**Branch created:** `rlm/run-id`
**Location:** `/full/path/to/project/.worktrees/run-id`

## Project Setup

**Detected project type:** Node.js (package.json found)

**Commands executed:**
```bash
cd .worktrees/run-id
npm install
```

**Output:**
```
added 472 packages in 8s
```

## Test Baseline Verification

**Command:**
```bash
npm test
```

**Results:**
- Total: 47 tests
- Passed: 47
- Failed: 0
- Skipped: 0

**Baseline:** ✅ Clean (all tests passing)

## Main Branch Protection

**Original branch:** `main`
**Worktree branch:** `rlm/run-id`
**Isolation:** ✅ Working in isolated worktree

## Traceability

- RLM process -> Isolated workspace established | Evidence: worktree at `.worktrees/run-id`

## Coverage Gate

- [ ] Worktree location selected following priority rules
- [ ] Directory verified as git-ignored (if project-local)
- [ ] Worktree created successfully on feature branch
- [ ] Project setup completed without errors
- [ ] Clean test baseline verified (all tests passing)
- [ ] Main branch protection confirmed (working in isolation)

Coverage: PASS / FAIL

## Approval Gate

- [ ] Isolated workspace ready for development
- [ ] No pending setup issues
- [ ] Ready to proceed to Phase 1/2

Approval: PASS / FAIL

LockedAt: `YYYY-MM-DDTHH:MM:SSZ`
LockHash: `<sha256-hex>`
```

## Integration with RLM

### Phase 0 -> Phase 1 Transition

Phase 0 must be locked before proceeding:

1. Verify worktree exists and is properly configured
2. Check Phase 0 gates are PASS
3. Lock Phase 0 artifact
4. Proceed to Phase 1 (requirements already exist)
5. All subsequent phases execute in worktree context

### Worktree Context for All Phases

Once Phase 0 is complete:
- All RLM commands run from worktree directory
- Git operations target feature branch
- Main branch remains untouched
- Development is fully isolated

### Phase 6/7 (Global Updates)

When updating global artifacts:
1. Changes are made in worktree context
2. Commits go to feature branch
3. User merges feature branch to main when ready
4. DECISIONS.md and STATE.md updates are part of the merge

## Common Mistakes

### Skipping ignore verification

- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always use `git check-ignore` before creating project-local worktree

### Assuming directory location

- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > CLAUDE.md > ask

### Proceeding with failing tests

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

### Hardcoding setup commands

- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, Cargo.toml, etc.)

## Red Flags

**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check
- Work on main/master without explicit consent and documentation

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline
- Create feature branch (rlm/run-id pattern)
- Document worktree location in Phase 0 artifact

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md -> Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| On main/master branch | Create worktree (default) |
| User insists on main | Document consent, proceed with caution |
| No package.json/Cargo.toml | Skip dependency install |

## Real-World Impact

From development sessions:
- **Before worktrees:** 15% of requirements had accidental main branch commits
- **After worktrees:** 0% accidental main branch commits
- **Parallel development:** 3+ requirements can be worked simultaneously
- **Clean main branch:** Production history is clean and linear
- **Easy discard:** Abandoned requirements don't pollute main branch

## References

- **REQUIRED:** Use this skill for ALL RLM runs
- **TRIGGERS:** At start of "Implement requirement 'run-id'"
- **OUTPUT:** `00-worktree.md` artifact + isolated worktree
- **NEXT:** Continue with Phase 1 (requirements) in worktree context
