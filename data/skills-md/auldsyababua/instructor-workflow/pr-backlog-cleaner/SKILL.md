---
name: pr-backlog-cleaner
description: Clean and normalize a large backlog of GitHub pull requests in messy repositories. This skill should be used when facing a repository with numerous stale, conflicted, or outdated PRs that need systematic review, conflict resolution, testing, and disposition (merge, close, or defer). Handles PR triage, automated rebasing, CI verification, risk assessment, and safe merging while maintaining default branch stability.
---

# PR Backlog Cleaner

## Overview

Clean and normalize large backlogs of GitHub pull requests systematically while keeping the default branch stable and deployable. This skill provides a comprehensive workflow for triaging, reviewing, rebasing, testing, and dispositioning PRs at scale, ensuring every PR ends in one of three states: merged safely, closed with reason, or explicitly deferred.

**NEW**: Integrates **pr-comment-analysis** subskill to systematically extract, analyze, and prioritize existing PR review feedback. This helps avoid re-litigating issues reviewers already identified, catch hidden impacts through automated analysis, and make informed merge/close/defer decisions based on the complete feedback picture.

## When to Use This Skill

Use this skill when:
- Facing a repository with numerous stale, outdated, or conflicted PRs
- Need to systematically clean up technical debt in pull request backlogs
- Want to safely merge or close PRs without destabilizing the default branch
- Managing a repository where PRs have accumulated without clear disposition
- Need to establish clear PR hygiene and backlog management practices
- **PRs have existing review feedback** that needs to be systematically analyzed and addressed (uses pr-comment-analysis subskill)

## Global Safety Constraints

**CRITICAL RULES - Never violate these:**

1. **No blind merging**: Do not modify or merge code without automated verification if any tests or CI are available
2. **No invention**: Do not invent repository structure, commands, or tools—infer them only from existing files and configs
3. **Minimal scope**: Do not modify unrelated files—restrict edits to files directly involved in the PR or minimally required for functionality
4. **Respect CI**: Do not bypass failing CI without explicit instruction from user
5. **Prefer small changes**: Prefer smaller, isolated changes over large refactors
6. **Prefer fresh PRs**: Prefer creating new clean PRs over attempting to merge extremely outdated or conflicted ones

## Core Workflow

### Phase 1: Repository Initialization

**Discover the environment before taking any action.**

#### 1.1 Identify Main Branch

```bash
# List all branches
git branch -a

# Identify protected/default branch
gh repo view --json defaultBranchRef
```

Look for: `main`, `master`, or other protected branches

#### 1.2 Identify Language and Tooling

Check for these files to determine tech stack:
- **Node.js**: `package.json`, `.nvmrc`
- **Python**: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
- **Java**: `pom.xml`, `build.gradle`, `build.gradle.kts`
- **Go**: `go.mod`, `go.sum`
- **Rust**: `Cargo.toml`, `Cargo.lock`
- **Ruby**: `Gemfile`, `Gemfile.lock`

Check for CI/build configs:
- `.github/workflows/*`
- `Jenkinsfile`
- `.gitlab-ci.yml`
- `azure-pipelines.yml`
- `.circleci/config.yml`

#### 1.3 Determine Test Commands

Extract test commands from:
1. **README.md** or **CONTRIBUTING.md** - Look for "Running Tests" sections
2. **CI workflows** - Parse `.github/workflows/*.yml` for test steps
3. **Package configs**:
   - `package.json`: `scripts.test`
   - `pyproject.toml`: `[tool.pytest]` or `[tool.tox]`
   - `pom.xml`: `<build><plugins>` for surefire/failsafe
   - `Cargo.toml`: cargo test is standard

**Common test commands by ecosystem:**
```bash
# Node.js
npm test
npm run test:unit
npm run test:integration

# Python
pytest
python -m pytest
tox
python -m unittest discover

# Java
mvn test
./gradlew test

# Go
go test ./...

# Rust
cargo test
```

#### 1.4 Verify Tests Run Locally

```bash
# Checkout default branch
git checkout <default_branch>
git pull origin <default_branch>

# Run identified test command
<test_command>
```

**Record:**
- ✅ Pass/fail status
- ⏱️ Approximate runtime
- 🔍 Any flaky or known failing tests (from CI config or output)

**If tests fail on default branch:**
- Document the baseline failure state
- Future PR tests must not introduce additional failures beyond this baseline

### Phase 2: Backlog Inventory

**Create a comprehensive inventory of all open PRs.**

#### 2.1 Retrieve PR List

```bash
# List all open PRs with detailed info
gh pr list --state open --json number,title,author,createdAt,updatedAt,additions,deletions,files,labels,statusCheckRollup --limit 1000 > pr_inventory.json
```

#### 2.2 Extract PR Metadata

For each PR, document:
- **PR number**
- **Title**
- **Author** (username)
- **Created date** (ISO format)
- **Last updated date** (ISO format)
- **CI status**: SUCCESS, FAILURE, PENDING, or N/A
- **Changed files count**
- **Additions/deletions** (lines changed)
- **Labels** (if present)

See `scripts/analyze_pr_backlog.py` for automated inventory generation.

#### 2.3 Classify PRs by Type

Based on title, description, and diff, classify as:

- **`bugfix`**: Fixes reported bugs or errors
- **`feature`**: Adds new functionality
- **`refactor`**: Restructures code without changing behavior
- **`infra`**: CI, build, tooling, deployment, configs
- **`docs`**: Documentation-only changes
- **`mixed`**: Contains multiple categories (upgrade risk)

#### 2.4 Assign Risk Levels

**Low Risk:**
- Only docs changes
- Trivial or localized changes without external dependencies
- Logging-only or comment-only updates

**Medium Risk:**
- Localized behavior changes
- Small features with tests
- Non-critical infrastructure changes

**High Risk:**
- Large refactors (>500 lines or >10 files)
- Cross-cutting changes affecting multiple modules
- Database migrations or schema changes
- Public API changes
- Changes with no tests in critical areas
- Mixed PRs combining multiple change types

#### 2.5 Create Structured Inventory

Store in `pr_backlog_analysis.md`:

```markdown
# PR Backlog Analysis

**Repository**: owner/repo
**Analysis Date**: 2025-01-19
**Total Open PRs**: 47
**Default Branch**: main
**Test Status**: ✅ Passing (baseline)

## PR Inventory

| PR# | Title | Author | Age (days) | Type | Risk | CI | Files | +/- |
|-----|-------|--------|------------|------|------|-----|-------|-----|
| 123 | Fix auth timeout | user1 | 45 | bugfix | medium | ✅ | 3 | +25/-10 |
| 124 | Update README | user2 | 120 | docs | low | ✅ | 1 | +15/-5 |
| 125 | Refactor database layer | user3 | 200 | refactor | high | ❌ | 25 | +500/-300 |

## Stale Candidates (>90 days, no recent activity)

- PR #124 (120 days)
- PR #125 (200 days)
```

### Phase 3: Global Policies

**Establish consistent rules for all PR processing.**

#### 3.1 Stale PR Policy

**Stale threshold**: 90 days with no commits or comments

**For stale PRs:**
- Mark as `stale-candidate`
- Review for obsolescence before closing
- Add comment with clear revival instructions

**Stale closure template:**
```
This PR has been inactive for >90 days and the branch is significantly behind the current `main` branch.

To revive this work:
1. Rebase on current main: `git rebase origin/main`
2. Resolve any conflicts
3. Ensure tests pass
4. Open a new PR with updated context

Closing for now to keep the backlog manageable. Thank you for the contribution!
```

#### 3.2 Merge Strategy

**Default: Squash and merge**
- Simplifies history
- Easier rollbacks
- Cleaner commit log

**Use merge commits only if:**
- Repository convention clearly demands it (check existing merge patterns)
- PR has carefully crafted commit history worth preserving

**Rebase before merge:**
- Always rebase on latest default branch first
- Resolve conflicts before final merge

#### 3.3 Test Requirement Policy

**If automated tests exist:**
- ✅ Tests MUST pass before merging
- Align with default branch baseline (no new failures)

**If tests are broken on default branch:**
- Do not introduce additional failures
- Consider fixing baseline before merging PRs

**If no tests exist:**
- Restrict merging to:
  - Low-risk changes (docs, comments, logging)
  - Clearly localized fixes with verifiable behavior
- Avoid merging large refactors or cross-cutting changes

### Phase 4: Triage Order

**Process PRs in this priority order:**

**Priority 1: Low-hanging fruit**
1. Docs and low-risk infra changes
2. Small bugfix PRs with clear intent

**Priority 2: Value-add features**
3. Small to medium feature PRs (recent, low-to-medium risk)

**Priority 3: Complex work**
4. Refactors and high-risk PRs

**Priority 4: Problem cases**
5. Very old or heavily conflicted PRs

**Within each category, prioritize:**
- ✅ More recent activity over older
- 📦 Smaller diffs over larger
- 🟢 Passing CI over failing CI

### Phase 5: Per-PR Standard Flow

**Execute this workflow for each PR in triage order.**

#### Step A: Relevance Check

```bash
# View PR details
gh pr view <PR_NUMBER>

# Check linked issues
gh issue view <ISSUE_NUMBER>
```

**Determine if still relevant:**
- Is the problem/feature still needed?
- Has this been superseded by newer merged work?
- Is the approach still aligned with current architecture?

**If clearly obsolete:**
- Mark as `obsolete`
- Close with factual comment
- Move to next PR

**Template for obsolete closure:**
```
This PR is no longer relevant because [specific reason]:
- [Problem was solved by PR #XYZ]
- [Feature is no longer needed per issue #ABC discussion]
- [Architecture has moved in a different direction]

Closing this PR. Thank you for the contribution!
```

#### Step B: Metadata and Precheck

**Check CI status:**
```bash
gh pr checks <PR_NUMBER>
```

**If CI is green (✅):**
- Proceed to Step C (rebase)

**If CI is red (❌):**
- Inspect logs to determine if failures are:
  - **Unrelated**: Already failing on default branch (check baseline)
  - **PR-caused**: Introduced by this PR
- If unclear, treat as PR-caused until proven otherwise

**View CI logs:**
```bash
gh run view <RUN_ID> --log-failed
```

#### Step C: Local Checkout and Rebase

```bash
# Fetch PR branch
gh pr checkout <PR_NUMBER>

# OR manually:
git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
git checkout pr-<PR_NUMBER>

# Rebase onto latest default branch
git fetch origin
git rebase origin/<default_branch>
```

**Resolve conflicts:**

**Conflict resolution rules:**
1. Follow existing patterns from default branch
2. Do not introduce new patterns during conflict resolution
3. Do not modify files outside PR scope unless strictly required
4. Prefer default branch's version for infrastructure files (CI, build configs)

**After resolving conflicts:**

```bash
# Ensure code compiles (if applicable)
npm run build  # or mvn compile, cargo build, etc.

# Run tests for affected modules
<test_command>
```

**Test scope:**
- Full suite for small repos (<5 min runtime)
- Affected modules only for large repos
- At minimum, smoke tests for critical paths

**Push rebased branch:**
```bash
# Use force-with-lease to avoid clobbering external changes
git push origin pr-<PR_NUMBER> --force-with-lease
```

#### Step D: Structural Review and Comment Analysis

**Identify blast radius:**

1. **List affected modules/packages**
   ```bash
   # View changed files
   gh pr diff <PR_NUMBER> --name-only
   ```

2. **Detect impact areas:**
   - Public APIs (exported functions, REST endpoints)
   - Core domain logic (business rules, algorithms)
   - Database schema (migrations, models)
   - Shared utilities (used by multiple modules)

**Detect change type:**

- **Mechanical**: Renames, formatting, simple refactors (low risk if tests pass)
- **Behavioral**: Logic changes, new features (requires test validation)
- **Mixed**: Combines mechanical and behavioral (higher risk)

**If PR mixes unrelated changes:**
- Example: Formatting + behavior + infra in one PR
- Mark as `mixed`
- Consider splitting into focused follow-up PRs
- If not feasible, upgrade to high-risk classification

**Extract and Analyze PR Comments (NEW - Subskill Integration):**

Use the **pr-comment-analysis** subskill to systematically analyze existing PR feedback:

1. **Extract all PR comments:**
   ```bash
   # Navigate to repository
   cd /path/to/repo

   # Run pr-comment-analysis comment grabber
   python /path/to/skills/pr-comment-analysis/scripts/pr-comment-grabber.py owner/repo <PR_NUMBER>
   ```

   This creates `pr-code-review-comments/pr<PR_NUMBER>-code-review-comments.json`

2. **Analyze extracted comments:**
   - Load the JSON file
   - Apply pr-comment-analysis prioritization (Critical → Design → Style)
   - Identify high-consensus issues (multiple reviewers flagging same problem)
   - Validate comments against project context (.project-context.md)
   - Research proposed fixes using ref.tools and Exa search
   - Perform impact analysis to catch ripple effects

3. **Integrate comment insights into PR disposition:**

   **For PRs with substantive review feedback:**
   - **Critical issues identified**: Address before merging or close if unsafe
   - **High-consensus concerns**: Multiple reviewers agreeing indicates real issues
   - **Context-validated fixes**: Prioritize fixes that are validated as correct
   - **Impact warnings**: Defer or carefully handle PRs with breaking change risks

   **Comment analysis outcomes:**
   - ✅ **Comments addressed, tests pass**: Safe to merge
   - ⚠️ **Critical issues unresolved**: Request fixes or close
   - 🔄 **Needs follow-up PR**: Merge simple parts, create new PR for complex issues
   - ❌ **High-impact risks identified**: Defer pending architectural discussion

4. **Document comment resolution:**
   ```markdown
   ## PR #123 Comment Analysis

   **Total comments**: 15
   **Critical issues**: 2 (both addressed)
   **Design improvements**: 5 (3 addressed, 2 deferred to #456)
   **Style nitpicks**: 8 (addressed)

   **Key insights:**
   - SQL injection vulnerability fixed (validated with parameterized queries)
   - Cache invalidation refactored (impact: 4 other files updated)
   - Breaking API change deferred (affects 12 consumers outside PR scope)
   ```

**Why use pr-comment-analysis during backlog cleanup:**
- **Avoid re-litigating**: See what reviewers already identified
- **Catch hidden issues**: Impact analysis finds problems reviewers couldn't see
- **Prioritize intelligently**: Focus on high-consensus, critical issues first
- **Make informed decisions**: Merge/close/defer based on complete feedback picture
- **Preserve institutional knowledge**: Don't lose valuable review insights when reorganizing PRs

#### Step E: Logic and Testing Review

**For bugfix PRs:**

✅ **Must have:**
- Regression test that reproduces the bug
- Test passes only with the fix applied

❌ **If no test exists and repo has tests:**
- Add a focused test in the appropriate test suite
- Or request author to add test before merging

**For feature PRs:**

✅ **Must have:**
- New behavior covered by tests
- Tests assert expected behavior and edge cases
- Tests are not trivial (no `expect(true).toBe(true)`)

**For refactor PRs:**

✅ **Validation:**
- No intentional behavior change (unless explicitly stated)
- Existing tests continue to pass
- If critical paths are untested:
  - Prefer not merging large refactors
  - Recommend adding characterization tests first
  - Or split into smaller, safer PRs

**Execute tests:**

```bash
# Run affected module tests
<test_command_for_module>

# Or run full suite
<test_command>
```

**Do not assume correctness without test execution when tests exist.**

#### Step F: Merge Decision

**Merge criteria (all must be satisfied):**

1. ✅ Rebased cleanly on default branch
2. ✅ CI is green OR failures are confirmed unrelated and already in baseline
3. ✅ Change is relevant and aligned with current codebase
4. ✅ Tests exist and pass for changed behavior (where applicable)
5. ✅ No unresolved security concerns or dangerous patterns

**If all criteria satisfied:**

```bash
# Squash and merge (preferred)
gh pr merge <PR_NUMBER> --squash --delete-branch

# Use this commit message format:
# <Title> (#<PR_NUMBER>)
#
# <Brief summary of change>
# <Why this change was needed>
```

**If salvageable but needs fixes:**

Apply minimal changes to make mergeable:
```bash
# Make necessary fixes
git commit -m "Fix: <specific issue>"
git push origin pr-<PR_NUMBER> --force-with-lease

# Re-run tests
<test_command>

# Merge once criteria satisfied
gh pr merge <PR_NUMBER> --squash --delete-branch
```

**If too noisy or requires excessive rework:**

Create clean replacement PR:
```bash
# Create new branch from default
git checkout <default_branch>
git pull origin <default_branch>
git checkout -b clean-<feature_name>

# Cherry-pick or reimplement only essential changes
# (see Phase 6B for cherry-picking strategy)

# Open new PR
gh pr create --title "<Clear title>" --body "Cleaned up version of #<OLD_PR_NUMBER>"
```

**If obsolete, unsafe, or too costly:**

Close with clear reason:
```bash
gh pr close <PR_NUMBER> --comment "Closing because [specific reason]:
- [Obsolete: Superseded by #XYZ]
- [Unsafe: Introduces breaking changes without migration path]
- [Too costly: Requires major refactor beyond PR scope]

Thank you for the contribution!"
```

### Phase 6: Special Handling for Complex PRs

#### Strategy A: Integration Branch

**When multiple large/conflicting PRs affect the same areas:**

```bash
# Create integration branch
git checkout <default_branch>
git pull origin <default_branch>
git checkout -b integration/<feature_area>

# Sequentially merge PRs into integration branch
gh pr checkout <PR_1>
git checkout integration/<feature_area>
git merge pr-<PR_1> --no-ff

# Resolve conflicts, run tests
<test_command>

# Repeat for each related PR
gh pr checkout <PR_2>
git checkout integration/<feature_area>
git merge pr-<PR_2> --no-ff
<test_command>

# Analyze combined impact
<test_command>

# Cherry-pick stable parts back to clean PRs
# (see Strategy B)
```

**Benefits:**
- Test multiple PRs together safely
- Identify which combinations work
- Isolate problematic interactions

#### Strategy B: Cherry-Picking Valuable Changes

**When a PR contains both useful and problematic changes:**

```bash
# Identify valuable commits
git log --oneline pr-<PR_NUMBER>

# Create clean branch from default
git checkout <default_branch>
git checkout -b cherry-picked-<feature>

# Cherry-pick specific commits
git cherry-pick <commit_sha_1>
git cherry-pick <commit_sha_2>

# Test cherry-picked changes
<test_command>

# Open new focused PR
gh pr create --title "Clean version: <feature>" --body "Cherry-picked valuable changes from #<OLD_PR>"
```

**Use when:**
- PR has good core changes buried in noise
- PR mixes feature with unrelated refactoring
- Conflicts are easier to resolve by starting fresh

### Phase 7: Testing in Weak Test Suites

**If tests exist but coverage is weak:**

**Identify critical flows:**
- Authentication/authorization
- Payment processing
- Data persistence
- Core business logic algorithms

**Before risky merges:**
- Add tests around critical flows
- Or document untested areas and upgrade risk level

**If no tests exist at all:**

**Only merge:**
- Low-risk changes (docs, comments, logging)
- Clearly localized fixes with statically verifiable behavior

**Avoid merging:**
- Large refactors
- Cross-cutting changes
- Behavioral changes in critical paths

**Consider adding tests first:**
```bash
# Create baseline characterization tests
# Document current behavior, even if not ideal
# Provides safety net for future changes
```

### Phase 8: Stale PR Closure

**For each `stale-candidate` PR:**

1. **Verify stale criteria:**
   - Age > 90 days (or configured threshold)
   - No commits in last 90 days
   - No comments in last 90 days
   - No indication work is actively planned

2. **Check for dependencies:**
   - Is another team/PR waiting on this?
   - Is this referenced in active issues?

3. **Close if truly stale:**
   ```bash
   gh pr close <PR_NUMBER> --comment "<stale closure template from Phase 3.1>"

   # Add label
   gh pr edit <PR_NUMBER> --add-label "stale-closed"
   ```

**Label consistently:**
- `stale-closed`: Closed due to inactivity
- `obsolete`: Closed because no longer relevant
- `superseded`: Closed because replaced by newer PR

### Phase 9: State Tracking and Reporting

**Maintain progress tracking in `pr_cleanup_report.md`:**

```markdown
# PR Cleanup Report

**Repository**: owner/repo
**Cleanup Started**: 2025-01-19
**Cleanup Completed**: 2025-01-22
**Default Branch**: main

## Summary

**Starting State:**
- Total open PRs: 47
- Stale PRs (>90 days): 18
- Failing CI: 12
- Passing CI: 35

**Final State:**
- Merged: 28
- Closed (obsolete): 11
- Closed (stale): 6
- Deferred (needs discussion): 2

## Merged PRs

| PR# | Title | Type | Risk | Outcome |
|-----|-------|------|------|---------|
| 123 | Fix auth timeout | bugfix | medium | ✅ Merged after rebase |
| 126 | Add logging | infra | low | ✅ Merged (squash) |

## Closed PRs

| PR# | Title | Reason | Age (days) |
|-----|-------|--------|------------|
| 124 | Update README | Superseded by #130 | 120 |
| 125 | Refactor DB | Too risky without tests | 200 |

## Deferred PRs

| PR# | Title | Reason | Next Steps |
|-----|-------|--------|------------|
| 140 | Major API redesign | Needs architecture discussion | Schedule RFC review |

## Default Branch Status

**Before cleanup:**
- CI status: ✅ Passing
- Test count: 450 tests
- Coverage: ~65%

**After cleanup:**
- CI status: ✅ Passing
- Test count: 465 tests (+15 from merged PRs)
- Coverage: ~67% (+2%)
- No regressions introduced
```

**Termination condition:**

Stop when:
1. ✅ All open PRs have been processed
2. ✅ Each PR is merged, closed, or explicitly deferred
3. ✅ Default branch stability preserved (CI status ≥ baseline)
4. ✅ Cleanup report documented

## Resources

### scripts/

**`analyze_pr_backlog.py`**
- Generates comprehensive PR inventory from GitHub API
- Classifies PRs by type and risk level
- Outputs structured JSON and markdown reports
- Usage: `python scripts/analyze_pr_backlog.py owner/repo`

**`rebase_and_test.sh`**
- Automates PR checkout, rebase, and test execution
- Handles common rebase failure scenarios
- Reports test results in standardized format
- Usage: `./scripts/rebase_and_test.sh <PR_NUMBER>`

**`close_stale_prs.py`**
- Identifies and closes stale PRs based on age threshold
- Adds standardized closure comments
- Applies appropriate labels
- Usage: `python scripts/close_stale_prs.py owner/repo --threshold 90`

### references/

**`github_api_reference.md`**
- Comprehensive guide to GitHub CLI (`gh`) commands for PR management
- API patterns for PR listing, status checks, merging
- Rate limiting and pagination best practices

**`conflict_resolution_patterns.md`**
- Common conflict scenarios and resolution strategies
- Language-specific conflict patterns (package.json, go.mod, requirements.txt)
- When to accept theirs vs ours vs manual merge

**`test_frameworks_reference.md`**
- Test command references for major ecosystems
- How to run subset tests by module/package
- Interpreting test output and CI logs

### Integrated Subskills

**pr-comment-analysis** (skills/pr-comment-analysis/)
- Extracts all comments from GitHub PRs (inline + conversation)
- Consolidates feedback from multiple reviewers
- Prioritizes by severity (Critical → Design → Style)
- Validates proposed fixes against project context
- Performs impact analysis to catch breaking changes
- See: `skills/pr-comment-analysis/SKILL.md` for complete documentation

## Quick Start

**Step 1: Initial setup**
```bash
# Clone the repo and ensure clean state
git clone https://github.com/owner/repo
cd repo
git checkout <default_branch>

# Verify tests run
<identify and run test command>
```

**Step 2: Generate inventory**
```bash
# Use the analysis script
python scripts/analyze_pr_backlog.py owner/repo

# Review the generated pr_backlog_analysis.md
```

**Step 3: Start processing**
```bash
# Process PRs in priority order (Phase 4)
# For each PR, follow Phase 5 standard flow

# Use automation scripts to speed up:
./scripts/rebase_and_test.sh <PR_NUMBER>
```

**Step 4: Handle special cases**
```bash
# For complex PRs, use Phase 6 strategies
# For stale PRs, use Phase 8 process
```

**Step 5: Document and complete**
```bash
# Fill out pr_cleanup_report.md as you progress
# Ensure all PRs are dispositioned
# Verify default branch stability
```

## Best Practices

**1. Document decisions**
- Add comments to PRs explaining why merged, closed, or deferred
- Keep cleanup report updated in real-time
- Note any deviations from standard flow

**2. Communicate changes**
- Notify PR authors when closing or significantly modifying their work
- Be respectful and factual in closure comments
- Offer clear revival instructions for stale PRs

**3. Maintain stability**
- Never merge if tests are failing (unless baseline already broken)
- Run tests after every rebase
- Keep default branch green throughout cleanup

**4. Prefer automation**
- Use scripts for repetitive tasks (analysis, rebasing, closing stale PRs)
- Automate test execution
- Generate reports programmatically

**5. Track progress**
- Update cleanup report after each PR disposition
- Monitor overall backlog reduction
- Identify patterns (common failure types, frequent conflict areas)

**6. Know when to defer**
- Architecture decisions need broader discussion → defer
- Massive refactors without tests → defer or request tests first
- PRs requiring subject matter expertise you don't have → defer with clear next steps

## Anti-Patterns to Avoid

❌ **Merging without testing**
- Always run tests before merging (when tests exist)
- Verify CI is green or understand why it's red

❌ **Force pushing to default branch**
- Never force push to main/master
- Use force-with-lease for PR branches only

❌ **Modifying unrelated files**
- Stay within PR scope during conflict resolution
- Don't "clean up" unrelated code while rebasing

❌ **Assuming CI failures are flaky**
- Investigate all CI failures
- Confirm flakiness with multiple runs if suspected

❌ **Closing PRs without explanation**
- Always add comment explaining closure reason
- Provide revival instructions for stale PRs

❌ **Inventing repository conventions**
- Follow existing patterns for test commands, merge strategy
- Don't introduce new tooling without discussion

## Troubleshooting

**Problem: Rebase conflicts are overwhelming**
- Solution: Use Strategy B (cherry-picking) to extract valuable changes
- Or: Create integration branch (Strategy A) to resolve incrementally

**Problem: Tests fail after rebase but not on PR branch**
- Cause: Default branch introduced breaking changes
- Solution: Update PR code to match new interfaces/contracts from default

**Problem: CI is red on default branch (baseline broken)**
- Solution: Document baseline failures, ensure PRs don't add new failures
- Consider: Fix baseline before merging more PRs

**Problem: PR author hasn't responded in months**
- Solution: Follow stale PR process (Phase 8)
- Or: If valuable, create clean replacement PR and credit original author

**Problem: Unsure if PR is still relevant**
- Solution: Check linked issues, recent commits to related areas
- Ask: Would we accept this if submitted fresh today?
- When in doubt: Close with clear revival instructions
