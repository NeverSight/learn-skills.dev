---
name: pr-review
description: Comprehensive PR code review skill for git repositories. Use when reviewing a GitHub/GitLab PR by providing a PR link. Analyzes changes against merge base, explains what the PR does, provides review guidelines, identifies issues sorted by severity, evaluates test coverage, and raises uncertain questions. REQUIRES Must be in a git repository with gh CLI available.
---

# PR Review Skill

Review a Pull Request comprehensively by analyzing the diff against the upstream merge base.

## Prerequisites Check (MUST verify first)

Before proceeding, verify:

```bash
# 1. Check if in a git repository
git rev-parse --is-inside-work-tree

# 2. Check if gh CLI is available and authenticated
gh auth status
```

If either check fails, STOP and inform the user:

- Not in git repo → "This skill requires a git repository. Please navigate to a git project."
- gh not authenticated → "Please run `gh auth login` first."

## Input

The user provides a PR link in one of these formats:

- Full URL: `https://github.com/owner/repo/pull/123`
- Short form (if in repo): `#123` or `123`

## Workflow

### Step 1: Extract PR Information

```bash
# Get comprehensive PR metadata
gh pr view <PR_URL> --json number,title,body,state,author,baseRefName,baseRefOid,headRefName,headRefOid,additions,deletions,changedFiles,files,commits,reviewDecision,reviews,labels,milestone,createdAt,updatedAt

# Get the diff
gh pr diff <PR_URL>

# Get list of changed files
gh pr diff <PR_URL> --name-only

# Get detailed file changes with additions/deletions
gh api repos/{owner}/{repo}/pulls/{number}/files
```

### Step 2: Analyze the Merge Base

```bash
# Get base and head commits
BASE_REF=$(gh pr view <PR_URL> --json baseRefOid -q .baseRefOid)
HEAD_REF=$(gh pr view <PR_URL> --json headRefOid -q .headRefOid)

# Find merge base (requires local clone)
git fetch origin $BASE_REF $HEAD_REF 2>/dev/null || true
git merge-base $BASE_REF $HEAD_REF 2>/dev/null || echo $BASE_REF
```

### Step 3: Deep Code Analysis

For each changed file, analyze:

1. **Read the full diff** - Understand every change
2. **Read surrounding context** - Use `gh api` or local files to understand the code being modified
3. **Identify patterns** - What coding patterns does this codebase use?
4. **Check for tests** - Are there corresponding test changes?

## Output Format (MANDATORY)

Your review MUST include ALL of the following sections in this exact order:

---

### 📋 PR Summary

**Title**: [PR Title]
**Author**: [Author]
**Branch**: [head] → [base]
**Files Changed**: [N] | **Additions**: +[N] | **Deletions**: -[N]

#### What This PR Does

[2-5 sentences explaining the purpose and scope of this PR. Be specific about what functionality is added/changed/removed.]

#### Key Changes

- [Bullet point 1: specific change]
- [Bullet point 2: specific change]
- [...]

---

### 📖 Review Guidelines

Based on the type of changes in this PR, reviewers should focus on:

| Area | Priority | What to Check |
|------|----------|---------------|
| [Area 1] | 🔴 High | [Specific guidance] |
| [Area 2] | 🟡 Medium | [Specific guidance] |
| [Area 3] | 🟢 Low | [Specific guidance] |

---

### 🚨 Issues Found

Issues are sorted by severity (Critical → High → Medium → Low → Nitpick).

#### 🔴 Critical (Must Fix)

[Issues that will cause bugs, security vulnerabilities, or data loss]

**[Issue Title]**

- **File**: `path/to/file.ts:L123`
- **Problem**: [Clear description]
- **Impact**: [What will go wrong]
- **Suggestion**: [How to fix]

#### 🟠 High (Should Fix)

[Issues that may cause problems or violate important patterns]

#### 🟡 Medium (Consider Fixing)

[Code quality issues, minor bugs, or pattern violations]

#### 🟢 Low (Nice to Have)

[Style issues, minor improvements]

#### 💭 Nitpicks

[Purely stylistic suggestions, optional improvements]

---

### 🧪 Test Coverage Analysis

#### Test Changes in This PR

| Test File | Type | Coverage |
|-----------|------|----------|
| [file] | [unit/integration/e2e] | [what it tests] |

#### Coverage Assessment

- **New code tested**: [Yes/No/Partial] - [explanation]
- **Edge cases covered**: [Yes/No/Partial] - [explanation]
- **Regression tests**: [Yes/No/N/A] - [explanation]

#### Recommended Additional Tests

1. [Specific test case that should be added]
2. [Another test case]

---

### ❓ Questions & Uncertainties

Things I'm not certain about and would like clarification on:

1. **[Question about design decision]**
   - Context: [Why I'm asking]
   - My assumption: [What I think the answer might be]

2. **[Question about edge case]**
   - Context: [Why this matters]
   - Potential issue: [What could go wrong]

---

### ✅ Review Verdict

| Aspect | Status | Notes |
|--------|--------|-------|
| Code Quality | 🟢/🟡/🔴 | [Brief note] |
| Security | 🟢/🟡/🔴 | [Brief note] |
| Performance | 🟢/🟡/🔴 | [Brief note] |
| Test Coverage | 🟢/🟡/🔴 | [Brief note] |
| Documentation | 🟢/🟡/🔴 | [Brief note] |

**Overall**: [APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]

---

## Review Checklist (Internal - Use for Analysis)

### Code Quality

- [ ] No code duplication
- [ ] Functions are focused and small
- [ ] Variable/function names are clear
- [ ] No dead code or commented-out code
- [ ] Error handling is appropriate
- [ ] No hardcoded values that should be configurable

### Security

- [ ] No secrets or credentials in code
- [ ] Input validation present where needed
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization checks in place
- [ ] Sensitive data properly handled

### Performance

- [ ] No N+1 query patterns
- [ ] No unnecessary re-renders (React)
- [ ] No memory leaks
- [ ] Efficient algorithms used
- [ ] No blocking operations in async contexts

### Breaking Changes

- [ ] API contracts preserved (or documented if changed)
- [ ] Database migrations are reversible
- [ ] Feature flags for risky changes
- [ ] Backward compatibility maintained

### Documentation

- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] CHANGELOG entry if user-facing

## Important Notes

1. **Be Specific**: Always reference exact file paths and line numbers
2. **Be Constructive**: Suggest fixes, don't just point out problems
3. **Prioritize**: Critical issues first, nitpicks last
4. **Context Matters**: Consider the codebase's existing patterns
5. **Ask Questions**: When uncertain, ask rather than assume
