---
name: code-review
description: Review current branch changes with a team of specialized reviewers (security, performance, test coverage). Use when you want a thorough code review of your branch before merging.
---

# Code Review

A team-based code review workflow that spawns three specialized reviewers to analyze the current branch's changes.

## When This Skill Activates

- User asks to review current branch or PR
- User mentions "code review", "review changes", "review branch"
- User wants feedback before merging

## Workflow

### Step 1: Gather Branch Context

Before spawning reviewers, collect the diff and context:

1. Run `git log main..HEAD --oneline` to get the list of commits on this branch
2. Run `git diff main...HEAD` to get the full diff against the base branch
3. Identify all changed files with `git diff main...HEAD --name-only`

If the diff is too large (> 5000 lines), summarize per-file changes and have reviewers focus on their specific areas.

### Step 2: Create Review Team

Create a team named `code-review` and spawn three reviewer agents in parallel:

#### Reviewer 1: Security Reviewer (`security-reviewer`)

- **Agent type**: `general-purpose`
- **Focus**: Security implications of the changes
- **Checklist**:
  - Input validation and sanitization
  - Authentication/authorization changes
  - Sensitive data exposure (secrets, tokens, PII)
  - Injection vulnerabilities (SQL, XSS, command injection)
  - Dependency security (new packages, known CVEs)
  - Error handling that may leak internal details
  - CORS, CSP, or other security header changes
- **Output format**: List findings with severity (Critical / High / Medium / Low / Info)

#### Reviewer 2: Performance Reviewer (`performance-reviewer`)

- **Agent type**: `general-purpose`
- **Focus**: Performance impact of the changes
- **Checklist**:
  - Algorithm complexity (time/space)
  - Unnecessary re-renders or recomputations
  - Memory leaks (event listeners, subscriptions, timers not cleaned up)
  - Bundle size impact (new dependencies, large imports)
  - N+1 queries or redundant API calls
  - Caching opportunities missed
  - Lazy loading and code splitting considerations
- **Output format**: List findings with impact level (High / Medium / Low / Negligible)

#### Reviewer 3: Test Coverage Reviewer (`test-reviewer`)

- **Agent type**: `general-purpose`
- **Focus**: Test quality and coverage
- **Checklist**:
  - New code has corresponding tests
  - Edge cases and error paths are tested
  - Test descriptions are clear and meaningful
  - Mocks are appropriate (not over-mocked)
  - Integration/E2E coverage for critical paths
  - Existing tests updated for changed behavior
  - Missing negative test cases
- **Output format**: List findings with priority (Must Have / Should Have / Nice to Have)

### Step 3: Assign Review Tasks

Create tasks for each reviewer and assign them. Each reviewer should:

1. Read the full diff (or their relevant subset for large diffs)
2. Analyze changes against their specific checklist
3. Report findings with clear file paths, line references, and severity/priority
4. Mark their task as completed when done

### Step 4: Compile Review Report

After all three reviewers complete, compile their findings into a unified report:

```
## Code Review Summary

**Branch**: {branch_name}
**Commits**: {commit_count} commits
**Files Changed**: {file_count}

---

### Security Review
{security findings, grouped by severity}

### Performance Review
{performance findings, grouped by impact}

### Test Coverage Review
{test coverage findings, grouped by priority}

---

### Action Items
{consolidated list of items that should be addressed before merge}
```

### Step 5: Shutdown

After presenting the report to the user, gracefully shutdown all reviewers and clean up the team.

## Important Notes

- Reviewers should read actual code, not guess based on file names
- Each finding must reference specific file paths and line numbers
- Do not report style/formatting issues unless they affect readability significantly
- Focus on substance: bugs, risks, and missing coverage
- If no issues found in a category, explicitly state "No issues found" rather than omitting the section
