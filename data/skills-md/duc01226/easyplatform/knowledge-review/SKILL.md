---
name: knowledge-review
version: 1.0.0
description: '[Research] Review knowledge artifacts for completeness, citation quality, confidence accuracy, and template compliance.'
allowed-tools: Read, Grep, Glob, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

## Quick Summary

**Goal:** Review knowledge artifacts for quality, completeness, and protocol compliance.

**Workflow:**

1. **Read artifact** — Load the knowledge report/course/strategy
2. **Template compliance** — Verify all enforced sections present
3. **Citation audit** — Check inline citations and source table
4. **Confidence check** — Verify scores match evidence
5. **Output review** — Summary with pass/warn/fail per check

**Key Rules:**

- Every section from template must be present and non-empty
- Every factual claim must have inline citation
- Confidence scores must match evidence basis
- READ-ONLY — do not modify the artifact

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Knowledge Review

## Review Checklist

### 1. Template Compliance

- [ ] All enforced sections present
- [ ] No sections are empty placeholders
- [ ] Section order matches template

### 2. Citation Audit

- [ ] Every factual claim has inline citation `[N]`
- [ ] Every source in Sources table is referenced in text
- [ ] No orphan citations
- [ ] Sources table has: Title, URL, Author, Date, Tier

### 3. Confidence Accuracy

- [ ] Per-finding confidence scores declared
- [ ] Overall confidence declared
- [ ] Scores match evidence basis (not inflated)
- [ ] Findings <60% flagged prominently

### 4. Source Quality

- [ ] Tier distribution appropriate (not all Tier 4)
- [ ] At least 50% Tier 1-2 sources for key claims
- [ ] Recency appropriate for topic type

### 5. Knowledge Gaps

- [ ] Gaps section is present and honest
- [ ] Known limitations declared
- [ ] Suggestions for further research included

### 6. Cross-Validation

- [ ] Key claims verified by 2+ sources
- [ ] Discrepancies noted where sources conflict
- [ ] Single-source claims marked as unverified

### 7. Actionability

- [ ] Recommendations are concrete (not vague)
- [ ] Next steps are evidence-based
- [ ] Executive summary captures key findings

## Output Format

```markdown
## Knowledge Review Result

**Status:** PASS | WARN | FAIL
**Artifact:** {path}

### Checks (N/7 passed)

- [x] Template compliance
- [x] Citation audit
- [ ] Confidence accuracy — {issue}
- [ ] Source quality — {issue}
      ...

### Issues

- {specific issues found}

### Verdict

{APPROVED | REVISE | BLOCKED}
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
