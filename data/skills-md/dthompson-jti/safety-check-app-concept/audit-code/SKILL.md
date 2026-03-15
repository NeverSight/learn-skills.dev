---
name: audit-code
description: Technical code review (architecture, type safety, patterns). Use for pre-merge review or general code quality audit.
---

# Audit Code

Technical code review for architecture and quality.

## When to Use
- Pre-merge review
- General code quality check
- Architecture assessment

## Approach

### Step 1: Project Invariants (Required)
**Before auditing**, check `docs/knowledge-base/` for project-specific constraints:
- `AGENTS.md` — code patterns and prohibitions
- `RULES-*.md` — behavioral rules
- Flag any violation of documented invariants as **Critical** priority.

### Step 2: Technical Review Checklist
- [ ] Architectural soundness
- [ ] Dependency hygiene
- [ ] Type safety (`as any`, missing guards)
- [ ] AGENTS.md violations
- [ ] Edge cases: loading, empty, error states
- [ ] Accessibility: keyboard nav, screen reader

### Priority Scale
- **Critical (9-10)**: Crashes, data loss, security
- **High (7-8)**: Major UX issue, breaks functionality
- **Medium (4-6)**: Inconsistent UI, minor debt
- **Low (1-3)**: Minor stylistic issue

### Output
Structured findings by priority with evidence citations.
