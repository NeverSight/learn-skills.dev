---
name: implement-issue
description: Implement a GitHub issue end-to-end. Accepts issue number or URL, syncs to latest main/master, creates a feature branch, analyzes the issue, explores the codebase thoroughly, and implements the solution. REQUIRES Must be in a git repository with gh CLI available.
---

# Implement Issue Skill

Implement a GitHub issue from start to finish: branch setup, codebase analysis, and implementation.

## Prerequisites Check (MUST verify first)

Before proceeding, verify:

```bash
# 1. Check if in a git repository
git rev-parse --is-inside-work-tree

# 2. Check if gh CLI is available and authenticated
gh auth status

# 3. Check for uncommitted changes (warn user if any)
git status --porcelain
```

If checks fail, STOP and inform the user:

- Not in git repo → "This skill requires a git repository. Please navigate to a git project."
- gh not authenticated → "Please run `gh auth login` first."
- Uncommitted changes → "You have uncommitted changes. Please commit or stash them first."

## Input

The user provides an issue reference in one of these formats:

- Full URL: `https://github.com/owner/repo/issues/123`
- Short form (if in repo): `#123` or `123`

## Workflow

### Step 1: Extract Issue Information

```bash
# Get comprehensive issue metadata
gh issue view <ISSUE_NUMBER_OR_URL> --json number,title,body,state,author,labels,milestone,assignees,comments,createdAt,updatedAt

# Get repository info for branch naming
gh repo view --json owner,name,defaultBranchRef
```

Parse the issue to understand:
- **Title**: Brief summary of what needs to be done
- **Body**: Detailed requirements, acceptance criteria, context
- **Labels**: Type of work (bug, feature, enhancement, etc.)
- **Comments**: Additional context, discussions, clarifications

### Step 2: Sync to Latest Main/Master Branch

```bash
# Detect default branch (main or master)
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')

# Fetch latest changes
git fetch origin $DEFAULT_BRANCH

# Checkout and update default branch
git checkout $DEFAULT_BRANCH
git pull origin $DEFAULT_BRANCH
```

### Step 3: Create Issue Branch

Generate a branch name based on the issue:

**Branch naming convention**: `<type>/<issue-number>-<short-description>`

| Issue Type (from labels) | Branch Prefix |
|--------------------------|---------------|
| bug, bugfix | `fix/` |
| feature, enhancement | `feat/` |
| docs, documentation | `docs/` |
| refactor | `refactor/` |
| test | `test/` |
| chore | `chore/` |
| (default) | `issue/` |

**Examples**:
- Issue #42 "Add user authentication" → `feat/42-add-user-authentication`
- Issue #15 "Fix login redirect bug" → `fix/15-fix-login-redirect`
- Issue #99 "Update README" → `docs/99-update-readme`

```bash
# Create and checkout new branch
git checkout -b <BRANCH_NAME>
```

### Step 4: Deep Codebase Analysis

Before implementing, thoroughly understand the codebase:

#### 4.1 Project Structure Analysis

```bash
# Get project structure overview
ls -la
find . -type f -name "*.json" -path "*/package.json" -o -name "*.toml" -path "*/Cargo.toml" -o -name "*.go" -path "*/go.mod" 2>/dev/null | head -20

# Check for configuration files
ls -la *.json *.yaml *.yml *.toml .* 2>/dev/null | head -20
```

#### 4.2 Understand Existing Patterns

Use explore agents to understand:

1. **Architecture**: How is the codebase organized? What are the main modules?
2. **Patterns**: What coding patterns are used? (error handling, logging, testing)
3. **Related Code**: What existing code is related to this issue?
4. **Dependencies**: What libraries/frameworks are used?

```
# Fire multiple explore agents in parallel
background_task(agent="explore", prompt="Find the main entry points and understand the overall architecture of this codebase")
background_task(agent="explore", prompt="Find code related to [ISSUE_TOPIC] and understand existing patterns")
background_task(agent="explore", prompt="Find test patterns and testing conventions in this codebase")
```

#### 4.3 Identify Implementation Points

Based on the issue requirements, identify:
- Which files need to be modified
- Which new files need to be created
- What tests need to be added/updated
- What documentation needs updating

### Step 5: Create Implementation Plan

Before coding, create a detailed todo list:

```
todowrite([
  { id: "1", content: "Understand issue requirements fully", status: "completed", priority: "high" },
  { id: "2", content: "Analyze related codebase areas", status: "completed", priority: "high" },
  { id: "3", content: "[Specific implementation task 1]", status: "pending", priority: "high" },
  { id: "4", content: "[Specific implementation task 2]", status: "pending", priority: "medium" },
  { id: "5", content: "Add/update tests", status: "pending", priority: "high" },
  { id: "6", content: "Run tests and fix issues", status: "pending", priority: "high" },
  { id: "7", content: "Update documentation if needed", status: "pending", priority: "low" },
  { id: "8", content: "Final verification", status: "pending", priority: "high" }
])
```

### Step 6: Implement the Solution

Follow these principles:

1. **Match Existing Patterns**: Follow the codebase's established conventions
2. **Incremental Changes**: Make small, focused changes
3. **Test as You Go**: Verify each change works before moving on
4. **Document Complex Logic**: Add comments where necessary

For each implementation task:
1. Mark todo as `in_progress`
2. Make the changes
3. Run `lsp_diagnostics` on changed files
4. Mark todo as `completed`

### Step 7: Testing

```bash
# Run project tests (detect test command from package.json, Makefile, etc.)
# Common patterns:
npm test
yarn test
go test ./...
cargo test
pytest
make test
```

Ensure:
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Edge cases covered

### Step 8: Final Verification

```bash
# Check for any linting issues
# (detect lint command from project config)

# Verify build succeeds
# (detect build command from project config)

# Review all changes
git diff --stat
git diff
```

### Step 9: Commit Changes

```bash
# Stage all changes
git add -A

# Create commit with conventional commit message
# Format: <type>(scope): <description>
#
# Reference the issue number in the commit body
git commit -s -m "<type>: <short description>

<detailed description of changes>

Closes #<ISSUE_NUMBER>"
```

**Commit message examples**:
- `feat: add user authentication system`
- `fix: resolve login redirect loop`
- `docs: update API documentation`

## Output Format

After completing the implementation, provide:

---

### Implementation Summary

**Issue**: #[NUMBER] - [TITLE]
**Branch**: `[BRANCH_NAME]`
**Status**: [Implemented / Partially Implemented / Blocked]

#### Changes Made

| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file.ts` | Modified | [What was changed] |
| `path/to/new-file.ts` | Added | [What was added] |

#### Implementation Details

[2-5 sentences explaining what was implemented and how it addresses the issue]

#### Tests Added/Updated

- [Test 1 description]
- [Test 2 description]

#### Verification Results

| Check | Status | Notes |
|-------|--------|-------|
| Build | Pass/Fail | [Notes] |
| Tests | Pass/Fail | [Notes] |
| Lint | Pass/Fail | [Notes] |
| Diagnostics | Clean/Issues | [Notes] |

---

### Next Steps

Suggest to the user:

1. **Review changes**: `git diff origin/<DEFAULT_BRANCH>...HEAD`
2. **Push branch**: `git push -u origin <BRANCH_NAME>`
3. **Create PR**: `gh pr create --title "<PR_TITLE>" --body "<PR_BODY>"`

Or offer to create the PR automatically if requested.

---

## Important Notes

1. **Understand Before Implementing**: Spend adequate time understanding the issue and codebase
2. **Ask for Clarification**: If issue requirements are unclear, ask before implementing
3. **Minimal Changes**: Only change what's necessary to implement the issue
4. **Follow Conventions**: Match the existing codebase style and patterns
5. **Test Thoroughly**: Ensure changes don't break existing functionality
6. **Document**: Update documentation if the change affects public APIs or user-facing features

## Error Handling

| Situation | Action |
|-----------|--------|
| Issue not found | Verify issue number/URL, check repository access |
| Branch already exists | Ask user: use existing branch or create new with suffix? |
| Merge conflicts | Report to user, suggest resolution steps |
| Tests failing | Investigate if pre-existing or caused by changes |
| Unclear requirements | Ask user for clarification before proceeding |
| Implementation blocked | Document blockers, suggest alternatives |
