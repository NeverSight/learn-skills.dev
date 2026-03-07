---
name: fix-review
description: Verify fix commits address security findings without introducing new bugs or regressions. Analyzes diffs for anti-patterns like removed validation, weakened access control, reduced error handling, reordered external calls, and changed integer operations. Generates structured FIX_REVIEW_REPORT with finding status tracking.
version: 1.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Bash, Grep, Glob, Write]
args: '<commit-ref|PR-number> [--findings-file <path>] [--output <report-path>]'
agents: [security-architect, code-reviewer, developer]
category: 'Security & Compliance'
tags: [security, fix-review, audit, vulnerability, regression, diff-analysis]
best_practices:
  - Always compare the fix against the original finding, not just the diff in isolation
  - Check for regression in adjacent code paths affected by the fix
  - Verify that the fix does not merely suppress the symptom while leaving the root cause
  - Look for anti-patterns that indicate incomplete or incorrect fixes
  - Track partial fixes explicitly -- they are more dangerous than unfixed findings
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

# Fix Review Skill

<!-- Agent: evolution-orchestrator | Task: #2 | Session: 2026-02-21 -->
<!-- License: CC-BY-SA-4.0 | Source: Trail of Bits (github.com/trailofbits/skills) -->
<!-- Attribution: Adapted from Trail of Bits fix-review skill -->

<identity>
Security-focused fix verification skill adapted from Trail of Bits audit methodology. Analyzes commit diffs against known findings to determine whether fixes are complete, partial, or introduce new issues. Detects common anti-patterns in security fix attempts and generates structured review reports.
</identity>

<capabilities>
- Commit diff analysis against known security findings
- Fix completeness verification (FIXED / PARTIALLY_FIXED / NOT_ADDRESSED / CANNOT_DETERMINE)
- Anti-pattern detection in fix attempts
- Regression risk assessment for adjacent code paths
- Structured FIX_REVIEW_REPORT generation
- Multi-commit fix tracking across branches
- Root cause vs symptom fix differentiation
- New issue introduction detection
</capabilities>

## Overview

This skill implements Trail of Bits' fix review methodology for the agent-studio framework. When a security audit produces findings and developers commit fixes, this skill systematically verifies that each finding is properly addressed without introducing new vulnerabilities or regressions.

**Source repository**: `https://github.com/trailofbits/skills`
**License**: CC-BY-SA-4.0
**Output**: Structured FIX_REVIEW_REPORT.md

## When to Use

- After developers commit fixes for security audit findings
- During PR review of security-related changes
- When verifying remediation of vulnerability reports
- Before closing security findings in tracking systems
- When reviewing patches for CVE remediations
- After automated security tool findings are addressed

## Iron Law

```
NO FINDING CLOSED WITHOUT FIX VERIFICATION
```

A finding is not fixed until the fix has been reviewed against the original finding description, verified to address the root cause, and confirmed not to introduce new issues.

## Fix Status Categories

| Status             | Meaning                                                                       |
| ------------------ | ----------------------------------------------------------------------------- |
| `FIXED`            | Finding is fully addressed. Root cause eliminated. No regressions introduced. |
| `PARTIALLY_FIXED`  | Some aspects addressed but gaps remain. More dangerous than unfixed.          |
| `NOT_ADDRESSED`    | Fix does not relate to the finding, or finding location unchanged.            |
| `CANNOT_DETERMINE` | Insufficient context or code complexity prevents definitive assessment.       |
| `NEW_ISSUE`        | Fix introduces a new vulnerability or regression.                             |

## Anti-Pattern Detection

The following anti-patterns indicate potentially incorrect or incomplete fixes:

### Anti-Pattern 1: Validation Removed

```
ALERT: Input validation was removed or weakened in the fix.
```

**Indicators**:

- Deleted input sanitization calls
- Relaxed regex patterns
- Removed length/type checks
- Weakened allowlist to blocklist

### Anti-Pattern 2: Access Control Weakened

```
ALERT: Authorization checks were reduced or bypassed in the fix.
```

**Indicators**:

- Removed authentication middleware
- Changed role checks from strict to permissive
- Added bypass conditions to access control
- Removed rate limiting

### Anti-Pattern 3: Error Handling Reduced

```
ALERT: Error handling was simplified or removed, potentially hiding failures.
```

**Indicators**:

- Replaced specific catch blocks with generic catch-all
- Added empty catch blocks
- Removed error logging
- Changed error responses from specific to generic (hiding useful diagnostics)

### Anti-Pattern 4: External Call Reordering

```
ALERT: Order of external calls changed, potentially creating race conditions or TOCTOU.
```

**Indicators**:

- Authorization check moved after data access
- Validation moved after processing
- Lock acquisition moved or removed
- Transaction boundaries changed

### Anti-Pattern 5: Integer Operation Changes

```
ALERT: Integer arithmetic modified, check for overflow/underflow/truncation.
```

**Indicators**:

- Changed integer types (int64 to int32, uint to int)
- Added/removed overflow checks
- Changed comparison operators (> to >=, == to !=)
- Modified loop bounds

### Anti-Pattern 6: Crypto Downgrade

```
ALERT: Cryptographic operations were changed in a potentially weakening way.
```

**Indicators**:

- Algorithm changed (AES-256 to AES-128, SHA-256 to SHA-1)
- Key length reduced
- Removed salt/nonce/IV
- Changed from authenticated to unauthenticated encryption

## Workflow

### Step 1: Load Findings

Read the original findings report to understand what was found:

```bash
# Read findings file
cat findings-report.md

# Or extract from issue tracker
gh issue view <issue-number>
```

### Step 2: Identify Fix Commits

Map each finding to its fix commit(s):

```bash
# View commits since the findings report
git log --oneline --since="<audit-date>"

# View a specific fix commit
git show <commit-hash>

# View PR diff
gh pr diff <pr-number>
```

### Step 3: Analyze Each Fix

For each finding-fix pair:

1. **Re-read the finding** description and affected code location
2. **Read the fix diff** line by line
3. **Check root cause**: Does the fix address the root cause or just the symptom?
4. **Check completeness**: Are all instances of the pattern fixed?
5. **Check anti-patterns**: Does the fix match any anti-pattern?
6. **Check regressions**: Does the fix break adjacent functionality?
7. **Assign status**: FIXED / PARTIALLY_FIXED / NOT_ADDRESSED / CANNOT_DETERMINE / NEW_ISSUE

### Step 4: Generate Report

## FIX_REVIEW_REPORT Format

```markdown
# Fix Review Report

**Date**: YYYY-MM-DD
**Reviewer**: [agent-type]
**Audit Reference**: [original audit report path]
**Commits Reviewed**: [list of commit hashes]

## Summary

| Status           | Count |
| ---------------- | ----- |
| FIXED            | N     |
| PARTIALLY_FIXED  | N     |
| NOT_ADDRESSED    | N     |
| CANNOT_DETERMINE | N     |
| NEW_ISSUE        | N     |

## Finding Reviews

### Finding F-001: [Title]

- **Original Severity**: Critical/High/Medium/Low/Informational
- **Original Location**: `file:line`
- **Fix Commit**: `<hash>`
- **Fix Status**: FIXED | PARTIALLY_FIXED | NOT_ADDRESSED | CANNOT_DETERMINE
- **Anti-Patterns Detected**: None | [list]

**Original Finding Summary**:
[Brief description of the finding]

**Fix Analysis**:
[Line-by-line analysis of what the fix does]

**Root Cause Addressed**: Yes/No/Partial
[Explanation]

**Regression Risk**: None/Low/Medium/High
[Explanation of potential regressions]

**Remaining Gaps** (if PARTIALLY_FIXED):

- [ ] Gap 1: [description]
- [ ] Gap 2: [description]

---

### Finding F-002: [Title]

[Same structure as above]

---

## New Issues Introduced

### NI-001: [Title]

- **Introduced By**: `<commit-hash>`
- **Location**: `file:line`
- **Severity**: Critical/High/Medium/Low
- **Description**: [What the new issue is]
- **Recommendation**: [How to fix it]

## Recommendations

1. [Prioritized list of remaining actions]
2. [Re-audit recommendations if needed]
```

## Integration with Agent-Studio

### Recommended Workflow

1. Run `audit-context-building` to deeply analyze the code
2. After fixes are committed, invoke `fix-review` to verify
3. Feed report to `code-reviewer` for additional review perspectives
4. Use `variant-analysis` to check if similar patterns exist elsewhere

### Complementary Skills

| Skill                    | Relationship                                      |
| ------------------------ | ------------------------------------------------- |
| `audit-context-building` | Provides deep context for understanding fixes     |
| `differential-review`    | Security-focused diff review (lower granularity)  |
| `variant-analysis`       | Finds unpatched variants of fixed vulnerabilities |
| `static-analysis`        | Automated confirmation of fix effectiveness       |
| `code-reviewer`          | General code quality review of fix commits        |

## Iron Laws

1. **NO FINDING CLOSED WITHOUT FIX VERIFICATION** — A finding is not fixed until the fix has been reviewed against the original finding, verified to address root cause, and confirmed not to introduce new issues.
2. **ALWAYS compare fix against original finding** — reviewing the diff in isolation misses context; the fix must address the specific vulnerability described.
3. **ALWAYS check for all instances** — if a pattern is fixed in one location, verify that all other instances of the same pattern are also fixed.
4. **NEVER close PARTIALLY_FIXED findings** — partial fixes are more dangerous than unfixed findings because they create false confidence.
5. **ALWAYS check adjacent code paths** — fixes that pass all anti-pattern checks can still introduce regressions in code that depends on the changed behavior.

## Anti-Patterns

| Anti-Pattern                             | Why It Fails                                                          | Correct Approach                                                 |
| ---------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Reviewing diff without reading finding   | Fix may address wrong issue or only surface symptom                   | Always re-read original finding before reviewing fix diff        |
| Closing finding after any code change    | Change may be unrelated or insufficient                               | Verify fix status is FIXED with root cause elimination confirmed |
| Ignoring partial fixes                   | PARTIALLY_FIXED is more dangerous than NOT_ADDRESSED (false security) | Track remaining gaps explicitly; keep finding open               |
| Skipping anti-pattern checklist          | Subtle regressions (weakened validation, reordered checks) go unseen  | Run all 6 anti-pattern checks on every fix diff                  |
| Not checking for variant vulnerabilities | Same bug pattern likely exists elsewhere in codebase                  | Invoke variant-analysis after confirming fix                     |

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md`

Check for:

- Original findings report and any prior fix review reports
- Known anti-pattern frequencies from previous fix reviews
- Previous fix quality patterns for this codebase

**After completing:**

- Anti-pattern frequency data -> `.claude/context/memory/learnings.md`
- Fix quality concern -> `.claude/context/memory/issues.md`
- Decision about finding status -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
