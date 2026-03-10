---
name: escalate-issues
description: >
  Triage maintenance problems by severity, document findings with context,
  route to appropriate specialist agent or human, and create actionable issue
  reports. Use when a maintenance task encounters problems beyond automated
  cleanup: code that is unsafe to delete, configuration changes requiring domain
  expertise, breaking changes detected during cleanup, complex refactoring needed,
  or security-sensitive findings such as hardcoded secrets or vulnerabilities.
license: MIT
allowed-tools: Read Write Edit Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: maintenance
  complexity: basic
  language: multi
  tags: maintenance, triage, escalation, routing, issue-reporting
---

# escalate-issues

## When to Use

Use this skill when a maintenance task encounters problems beyond automated cleanup:

- Uncertain whether code is safe to delete
- Configuration changes require domain expertise (security, performance, architecture)
- Breaking changes detected during cleanup
- Complex refactoring needed (not just cleanup)
- Security-sensitive findings (hardcoded secrets, vulnerabilities)

**Do NOT use** for simple issues with clear fixes. Escalate only when automated cleanup is risky or insufficient.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_description` | string | Yes | Clear description of the problem |
| `severity` | enum | Yes | `critical`, `high`, `medium`, `low` |
| `context_files` | array | No | Paths to relevant files |
| `specialist` | string | No | Target agent (auto-route if not specified) |
| `blocking` | boolean | No | Whether issue blocks further cleanup (default: false) |

## Procedure

### Step 1: Assess Severity

Classify the issue using standard severity levels.

**CRITICAL** — Blocks production functionality:
- Broken imports in actively used code
- Security vulnerabilities (exposed secrets, SQL injection)
- Data loss risk from cleanup operation
- Production service outages

**HIGH** — Impacts maintainability or developer productivity:
- Significant dead code bloat (>1000 lines)
- Broken CI/CD pipelines
- Major configuration drift between environments
- Unreferenced modules that might be dynamically loaded

**MEDIUM** — Minor hygiene issues:
- Unused helper functions (<100 lines)
- Stale documentation requiring updates
- Deprecated config files (no longer used but present)
- Lint warnings in non-critical paths

**LOW** — Style inconsistencies:
- Mixed indentation (works but inconsistent)
- Trailing whitespace
- Inconsistent naming (camelCase vs snake_case)
- Minor formatting differences

**Severity Decision Tree**:
```
Does it break production? → CRITICAL
Does it block development? → HIGH
Does it impact code quality? → MEDIUM
Is it purely cosmetic? → LOW
```

**Expected:** Issue classified with clear severity label

**On failure:** If uncertain, default to HIGH and escalate to human for re-triage

### Step 2: Document Finding

Capture all relevant context for the specialist to review.

**Issue Report Template**:
```markdown
# Issue: [Brief Title]

**Severity**: CRITICAL | HIGH | MEDIUM | LOW
**Discovered During**: [Skill name, e.g., clean-codebase]
**Date**: YYYY-MM-DD
**Blocking**: Yes | No

## Description

Clear description of the problem in 2-3 sentences.

## Context

- **File(s)**: [List of affected files with line numbers]
- **Related**: [Related issues, commits, or previous attempts to fix]
- **Impact**: [What breaks if this isn't fixed, or what's wasted if not cleaned]

## Evidence

```language
# Code snippet or log excerpt showing the problem
```

## Attempted Fixes

- Tried X but failed because Y
- Considered Z but uncertain due to W

## Recommendation

- **Option 1**: [Safe conservative approach]
- **Option 2**: [More aggressive fix with risks]
- **Preferred**: [Which option to pursue and why]

## Specialist Routing

**Suggested Agent**: [agent-name]
**Reason**: [Why this specialist is appropriate]

## References

- [Link to related documentation]
- [Link to similar past issues]
```

**Expected:** Issue documented with full context in `ESCALATION_REPORTS/issue_YYYYMMDD_HHMM.md`

**On failure:** (N/A — always document, even if incomplete)

### Step 3: Determine Routing

Match issue type to appropriate specialist agent or human reviewer.

**Routing Table**:

| Issue Type | Specialist | Reason |
|------------|-----------|---------|
| Security vulnerability | security-analyst | Security expertise required |
| GxP compliance concern | gxp-validator | Regulatory knowledge needed |
| Architecture decision | senior-software-developer | Design pattern expertise |
| Config management | devops-engineer | Infrastructure knowledge |
| Dependency conflicts | devops-engineer | Package management expertise |
| Performance bottleneck | senior-data-scientist | Optimization knowledge |
| Code style dispute | code-reviewer | Style guide authority |
| Dead code uncertainty | r-developer (or lang-specific) | Language-specific knowledge |
| Broken test unclear | code-reviewer | Test design expertise |
| Documentation accuracy | senior-researcher | Domain knowledge required |
| License compatibility | auditor | Legal/compliance expertise |

**Automatic Routing Logic**:
```python
def route_issue(severity, issue_type):
    if severity == "CRITICAL":
        # Always escalate to human for critical issues
        return "human"

    if "security" in issue_type or "secret" in issue_type:
        return "security-analyst"

    if "gxp" in issue_type or "compliance" in issue_type:
        return "gxp-validator"

    if "architecture" in issue_type or "design" in issue_type:
        return "senior-software-developer"

    if "config" in issue_type or "deployment" in issue_type:
        return "devops-engineer"

    # Default: code-reviewer for general code issues
    return "code-reviewer"
```

**Expected:** Issue routed to appropriate specialist with justification

**On failure:** If no clear specialist, escalate to human for manual routing

### Step 4: Create Actionable Issue Report

Generate a formatted report suitable for the target audience (agent or human).

**For Specialist Agents** (structured format for MCP tools):
```yaml
---
type: escalation
severity: high
from_agent: janitor
to_agent: security-analyst
blocking: false
---

# Security Concern: Hardcoded API Key in Config

**File**: config/production.yml:45
**Pattern**: API_KEY="sk_live_abc123..."

**Request**: Please review if this is a valid secret or a placeholder.
If valid, recommend secure credential management strategy.

**Context**: Discovered during config cleanup sweep.
```

**For Human Reviewers** (detailed markdown):
```markdown
# Escalation Report: Uncertain Dead Code Removal

**From**: Janitor Agent
**Date**: 2026-02-16
**Severity**: HIGH

## Problem

File `src/legacy_payments.js` (450 lines) appears unused but contains
complex payment processing logic. Static analysis shows zero references,
but name suggests business-critical functionality.

## Why Escalated

- Uncertain if payment code is dynamically loaded at runtime
- Potential data loss risk if deleted incorrectly
- Requires domain knowledge to assess business impact

## Evidence

- No direct imports found
- Last modified 8 months ago
- Git history shows it was part of payment refactor

## Recommendation

Request human review before deletion. If confirmed dead:
1. Archive to archive/legacy/ directory
2. Document in ARCHIVE_LOG.md
3. Create ticket to verify payment flows still work

## Next Steps

Awaiting human confirmation before proceeding with cleanup.
```

**Expected:** Report formatted appropriately for target audience

**On failure:** (N/A — generate report in generic markdown if uncertain)

### Step 5: Track Escalation Status

Maintain a log of all escalations to prevent duplicate reports.

```markdown
# Escalation Log

| ID | Date | Severity | Issue | Specialist | Status |
|----|------|----------|-------|-----------|--------|
| ESC-001 | 2026-02-16 | CRITICAL | Broken prod import | human | Resolved |
| ESC-002 | 2026-02-16 | HIGH | Dead payment code | human | Pending |
| ESC-003 | 2026-02-16 | MEDIUM | Config drift | devops-engineer | In Progress |
```

**Expected:** `ESCALATION_LOG.md` updated with new entry

**On failure:** If log doesn't exist, create it

### Step 6: Notify and Block (If Required)

If issue is blocking further maintenance, notify and pause cleanup.

**Blocking Logic**:
- CRITICAL issues always block
- HIGH issues block if in critical path
- MEDIUM/LOW issues do not block

**Notification**:
```markdown
⚠️ MAINTENANCE BLOCKED ⚠️

Issue ESC-002 (HIGH severity) requires human review before proceeding.

**Affected Operation**: clean-codebase (Step 5: Remove Dead Code)
**Reason**: Uncertain if src/legacy_payments.js is truly dead

**Action Required**: Review ESCALATION_REPORTS/ESC-002_2026-02-16.md

Once resolved, re-run maintenance from Step 5.
```

**Expected:** Maintenance paused; clear notification generated

**On failure:** If notification mechanism unavailable, document in report

## Validation Checklist

After escalation:

- [ ] Issue severity correctly assessed
- [ ] Full context documented (files, evidence, attempts)
- [ ] Appropriate specialist identified
- [ ] Escalation report created in ESCALATION_REPORTS/
- [ ] ESCALATION_LOG.md updated
- [ ] Blocking status communicated if applicable
- [ ] No sensitive information exposed in report

## Common Pitfalls

1. **Over-Escalating**: Escalating simple issues wastes specialist time. Only escalate when truly uncertain or risky.

2. **Under-Escalating**: Deleting code "just to see if tests pass" without escalation can cause production outages.

3. **Insufficient Context**: Escalating without evidence forces specialists to re-investigate. Include file paths, line numbers, error messages.

4. **Vague Descriptions**: "Something's wrong with config" is not actionable. Be specific: "Config drift: dev uses API v1, prod uses v2".

5. **Not Tracking Status**: Re-escalating already-reviewed issues. Check ESCALATION_LOG.md first.

6. **Exposing Secrets**: Including actual API keys or passwords in escalation reports. Redact sensitive values.

## Related Skills

- [clean-codebase](../clean-codebase/SKILL.md) — Often triggers escalations when uncertain
- [tidy-project-structure](../tidy-project-structure/SKILL.md) — May discover complex organizational issues
- [repair-broken-references](../repair-broken-references/SKILL.md) — Escalate when unclear if reference should be fixed or removed
- [compliance/security-scan](../../compliance/security-scan/SKILL.md) — Escalate security findings
- [general/issue-triage](../../general/issue-triage/SKILL.md) — General issue classification patterns
