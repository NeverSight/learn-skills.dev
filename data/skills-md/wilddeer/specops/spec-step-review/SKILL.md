---
name: spec-step-review
description: You MUST use this to review implementation against spec before marking complete.
version: 1.0.0
---

# spec-step-review

Review code changes against spec requirements with production-ready rigor.

## Input

Before starting, you need:
- Spec file path - what was supposed to be implemented
- Progress file path (if exists) - context on what steps were completed
- Research file path (if exists) - contains objective, defined terms, findings, decisions
- Git range (optional) - defaults to uncommitted changes

## Process

### 1. Gather Context

**Read project docs:**
- README.md - project overview, conventions, setup
- AGENTS.md (if exists) - agent guidelines, project rules
- Any other relevant project documentation

**Read the spec docs:**
- Spec file: understand what was supposed to be implemented
- Progress file: what steps are marked complete
- Research file: defined terms, architectural decisions, constraints

**Get the changes to review:**
```bash
# Default: uncommitted changes (staged + unstaged)
git diff HEAD

# If specific range provided:
git diff {BASE_SHA}..{HEAD_SHA}
```

### 2. Review Against Spec

For each requirement in the spec, verify the implementation:

| Spec Says | Check |
|-----------|-------|
| "Create X" | Does X exist and match spec exactly? |
| "X must do Y" | Does X actually do Y? Test it. |
| "Format: ..." | Does output match specified format? |
| "Error when..." | Are error cases handled as specified? |

### 3. Code Quality Review

**Project Standards:**
- Follows conventions from README/AGENTS.md?
- Matches existing codebase patterns?
- Adheres to documented project rules?

**Architecture:**
- Sound design decisions?
- Matches patterns in research/spec?
- Scalability considerations?
- Security concerns?

**Code Quality:**
- Clean separation of concerns?
- Proper error handling?
- Type safety (if applicable)?
- DRY principle followed?
- Edge cases handled?
- Linter passes with no new errors/warnings? (run per project docs)
- Tests pass? (run per project docs)

**Third-Party Libraries:**
- Check library docs/source for correct API usage (use Context7 or web search)
- Verify against the EXACT version in package.json/requirements.txt/etc.
- APIs change between versions - don't assume patterns from other versions work

**Testing:**
- Tests actually test logic (not just mocks)?
- Edge cases covered?
- Integration tests where needed?
- All tests passing?

**Production Readiness:**
- Breaking changes documented?
- Backward compatibility considered?
- No obvious bugs?

**Side Effects:**
- Search for usages of modified functions/classes/interfaces
- Check callers weren't broken by signature or behavior changes
- Verify no unintended impact on code outside the change scope

### 4. Categorize Issues

**Critical (Must Fix)**
- Bugs, security issues, data loss risks
- Broken functionality
- Spec requirements not met

**Important (Should Fix)**
- Architecture problems
- Missing error handling
- Test gaps
- Partial spec compliance

**Minor (Nice to Have)**
- Code style
- Optimization opportunities
- Documentation improvements

**For each issue, include:**
- File:line reference
- What's wrong
- Why it matters (link to spec if applicable)
- How to fix (if not obvious)

### 5. Return Result

Return exactly one of:

**APPROVED**
```
Result: APPROVED
Spec: [spec file path]
Changes: [uncommitted / git range]

### Checklist
- [x] Project docs read (README, AGENTS.md)
- [x] All spec requirements verified
- [x] Project standards followed
- [x] Architecture sound
- [x] Code quality acceptable
- [x] Third-party libs verified against exact versions
- [x] Linter passes
- [x] Tests pass
- [x] No unintended side effects on code outside scope

### Strengths
[What's well done - be specific with file:line references]

### Assessment
All spec requirements verified. Code is production-ready.
```

**APPROVED_WITH_RECOMMENDATIONS**

Use when implementation is correct but you have suggestions or observations worth discussing (edge cases not covered by spec, potential improvements, patterns that could be documented).

```
Result: APPROVED_WITH_RECOMMENDATIONS
Spec: [spec file path]
Changes: [uncommitted / git range]

### Checklist
- [x] Project docs read (README, AGENTS.md)
- [x] All spec requirements verified
- [x] Project standards followed
- [x] Architecture sound
- [x] Code quality acceptable
- [x] Third-party libs verified against exact versions
- [x] Linter passes
- [x] Tests pass
- [x] No unintended side effects on code outside scope

### Strengths
[What's well done - be specific with file:line references]

### Assessment
All spec requirements verified. Code is production-ready.

### Recommendations
[Suggestions, observations, edge cases not in spec - each as a bullet point]
```

**NEEDS_FIXES**
```
Result: NEEDS_FIXES
Spec: [spec file path]
Changes: [uncommitted / git range]

### Checklist
- [x] Project docs read (README, AGENTS.md)
- [ ] All spec requirements verified
- [x] Project standards followed
- [x] Architecture sound
- [ ] Code quality acceptable
- [x] Third-party libs verified against exact versions
- [x] Linter passes
- [ ] Tests pass
- [x] No unintended side effects on code outside scope
(mark [x] what passed, [ ] what failed or has issues)

### Issues

#### Critical (Must Fix)
[List with file:line, issue, spec reference, fix suggestion]

#### Important (Should Fix)
[List with file:line, issue, why it matters, fix suggestion]

#### Minor (Nice to Have)
[List - optional, only if noteworthy]

### Strengths
[What's well done - be specific]

### Assessment
[1-2 sentences: what needs to happen before approval]
```

**GAP**
```
Result: GAP
Spec: [spec file path]
Gap: [what the spec doesn't define that blocks review]
Context: [what you were trying to verify]
Recommendation: [what needs clarification in spec]
```

## Rules

- Always read project docs (README, AGENTS.md) before reviewing
- Verify third-party library usage against docs for the exact installed version
- Review against spec FIRST - spec compliance is primary
- Verify compliance with project standards from docs
- Never say "looks good" without verifying each spec requirement
- Be specific - always include file:line references
- Categorize by actual severity - not everything is Critical
- Acknowledge strengths - don't just list problems
- Give clear verdict - APPROVED, APPROVED_WITH_RECOMMENDATIONS, or NEEDS_FIXES, never ambiguous
- If spec is unclear on what to verify, return GAP
- Don't nitpick style unless it violates project standards
