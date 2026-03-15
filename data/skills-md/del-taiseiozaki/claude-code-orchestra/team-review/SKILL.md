---
name: team-review
description: |
  Parallel code review using Agent Teams. Spawns specialized reviewers
  (security, quality, test coverage) to review implementation from
  different perspectives simultaneously. Run after implementation.
metadata:
  short-description: Parallel review with Agent Teams
---

# Team Review

**Parallel review using Agent Teams. Review from multiple perspectives simultaneously after implementation is complete.**

## Prerequisites

- Implementation is complete (after `/team-implement` or manual implementation)
- All tests are passing

## Workflow

```
Step 1: Gather Diff
  Collect change diffs from the implementation scope
    ↓
Step 2: Spawn Review Team
  Launch specialized reviewers in parallel
    ↓
Step 3: Synthesize Findings
  Integrate review results and prioritize
    ↓
Step 4: Report to User
  Present findings and recommended actions
```

---

## Step 1: Gather Diff

**Identify the scope of changes to review.**

```bash
# All changes from main branch
git diff main...HEAD

# Changed files list
git diff main...HEAD --name-only

# Commit history
git log main..HEAD --oneline
```

---

## Step 2: Spawn Review Team

**Launch reviewers with specialized perspectives in parallel.**

```
Create an agent team to review implementation of: {feature}

The following files were changed:
{changed files list}

Spawn reviewers:

1. **Security Reviewer**
   Prompt: "You are a Security Reviewer for: {feature}.

   Review all changed files for security vulnerabilities:
   - Hardcoded secrets or credentials
   - SQL injection, XSS, command injection
   - Input validation gaps
   - Authentication/authorization issues
   - Sensitive data exposure in logs/errors
   - Dependency vulnerabilities

   Changed files: {list}

   Reference: .claude/rules/security.md

   For each finding:
   - Severity: Critical / High / Medium / Low
   - File and line number
   - Description of the issue
   - Recommended fix

   Save report to .claude/docs/research/review-security-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/security-reviewer.md

   Use this format:
   # Work Log: Security Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Focus areas: {list}
   ## Findings
   - [{severity}] {file}:{line} — {issue summary}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

2. **Quality Reviewer**
   Prompt: "You are a Quality Reviewer for: {feature}.

   Review all changed files for code quality:
   - Adherence to coding principles (.claude/rules/coding-principles.md)
   - Single responsibility violations
   - Deep nesting (should use early return)
   - Missing type hints
   - Magic numbers
   - Naming clarity
   - Function length (target < 20 lines)
   - Library constraint violations (.claude/docs/libraries/)

   Use Codex CLI for deep analysis of complex logic:
   codex exec --model gpt-5.4 --sandbox read-only --full-auto "{question}" 2>/dev/null

   Changed files: {list}

   For each finding:
   - Severity: High / Medium / Low
   - File and line number
   - Current code
   - Suggested improvement

   Save report to .claude/docs/research/review-quality-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/quality-reviewer.md

   Use this format:
   # Work Log: Quality Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Focus areas: {list}
   ## Findings
   - [{severity}] {file}:{line} — {issue summary}
   ## Codex Consultations
   - {question asked to Codex}: {key insight from response}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

3. **Test Reviewer**
   Prompt: "You are a Test Reviewer for: {feature}.

   Review test coverage and quality:
   - Run: uv run pytest --cov=src --cov-report=term-missing
   - Check: Are all happy paths tested?
   - Check: Are error cases covered?
   - Check: Are boundary values tested?
   - Check: Are edge cases handled?
   - Check: Are external deps properly mocked?
   - Check: Do tests follow AAA pattern?
   - Check: Are tests independent (no order dependency)?

   Reference: .claude/rules/testing.md

   For each gap:
   - File/function missing coverage
   - What test cases are needed
   - Priority: High / Medium / Low

   Save report to .claude/docs/research/review-tests-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/test-reviewer.md

   Use this format:
   # Work Log: Test Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Coverage: {percentage}
   ## Findings
   - [{priority}] {file/function}: {missing test case description}
   ## Test Execution Results
   - Total: {N} tests, Passed: {N}, Failed: {N}
   - Coverage: {percentage}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

Wait for all reviewers to complete.
```

### Optional: Competing Hypotheses (for debugging)

For bug investigation, add adversarial reviewers:

```
Spawn 3-5 teammates with different hypotheses about the bug.
Have them actively try to disprove each other's theories.
```

---

## Step 3: Synthesize Findings

**Integrate results from all reviewers and assign priorities.**

Read review reports:
- `.claude/docs/research/review-security-{feature}.md`
- `.claude/docs/research/review-quality-{feature}.md`
- `.claude/docs/research/review-tests-{feature}.md`

### Prioritization

| Priority | Criteria | Action |
|----------|----------|--------|
| **Critical** | Security vulnerabilities, data loss risk | Must fix before merge |
| **High** | Bugs, missing critical tests, type errors | Should fix before merge |
| **Medium** | Code quality, naming, patterns | Fix if time allows |
| **Low** | Style, minor improvements | Track for later |

---

## Step 4: Report to User

**Present the integrated review results to the user.**

```markdown
## Review Results: {feature}

### Summary
- Security: {N} findings (Critical: {n}, High: {n}, Medium: {n})
- Code Quality: {N} findings (High: {n}, Medium: {n}, Low: {n})
- Test Coverage: {N}% ({above/below} the 80% target)

### Critical / High Findings

#### [{Severity}] {Issue Title}
- **File**: `{file}:{line}`
- **Issue**: {description}
- **Recommended Fix**: {recommended fix}

...

### Recommended Actions
1. {Action 1 — Critical fix}
2. {Action 2 — High priority fix}
3. {Action 3 — Test gap to fill}

### Medium / Low Findings
{Brief list — details in review reports}

---
Shall we proceed with fixes?
```

### Cleanup

```
Clean up the team
```

---

## Tips

- **Reviewer specialization**: Each reviewer focuses on a different perspective to prevent blind spots
- **Codex utilization**: Quality Reviewer delegates complex logic analysis to Codex
- **Report persistence**: Save review results in `.claude/docs/research/` for reference during fixes
- **Competing hypotheses mode**: Adversarial review pattern is effective for bug investigation
- **Cost awareness**: 3 reviewers = 3x token consumption. For small changes, a subagent-based review is sufficient
