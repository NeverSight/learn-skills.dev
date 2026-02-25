---
name: swe-implementer
description: "Called per-subtask by swe-orchestrator. Implements ONE subtask in dedicated branch. Uses context7 for current documentation."
---

# 💻 SWE Implementer

**Called By:** [swe-orchestrator](../swe-orchestrator/SKILL.md) → per subtask  
**Input:** Subtask details, branch name, `.plan/` file  
**Output:** Code + tests committed, `.plan/` updated, ready for review

## Quick Start

1. **Understand subtask**: Read planning details from `.plan/` file
2. **Create branch**: `git checkout -b feature/[issue]-[subtask-name]`
3. **Query context7**: Get current lib/framework docs BEFORE coding
4. **Implement**: Code + tests following [backend-coder](../backend-coder/SKILL.md) standards
5. **Validate**: `npm run lint` (0 errors) + `npm run test` (all pass)
6. **Commit**: Include code, tests, updated `.plan/`
7. **Hand off**: Ready for [swe-reviewer](../swe-reviewer/SKILL.md)

## Detailed Steps

### 1. Verify Dependencies
- Check `.plan/` file - any blocked subtasks?
- If dependency not met: Alert orchestrator, stop

### 2. Branch Setup
```bash
git checkout -b feature/[issue-number]-[subtask-name]
git pull origin main  # Ensure up-to-date
```

### 3. Research (MANDATORY)
Query **context7 MCP** for:
- Library/framework version docs
- API references
- Best practices for this task
- Known pitfalls to avoid

Why: Ensures current APIs, avoids deprecated patterns, follows best practices.

### 4. Implement

**Code:**
- Follow architecture from swe-architect
- Apply SOLID principles
- Clean, readable code
- Proper error handling
- Type safety

**Tests:**
- Unit tests: happy path + edge cases
- Integration tests: if specified
- All tests passing required

### 5. Validate Loop
```bash
npm run lint   # 0 errors?
npm run test   # All pass?
```
If failures: Fix → Repeat until all pass ✅

### 6. Final Checklist
- [ ] Subtask 100% implemented (no partial work)
- [ ] All tests passing
- [ ] 0 linting errors
- [ ] No debug code (console.logs, debugger)
- [ ] Only intended files modified
- [ ] Code is maintainable and clear

### 7. Update `.plan/` File
```markdown
### Subtask N: [Name]
- **Status:** ✅ Completed
- **Branch:** `feature/123-subtask-name`
- **Files:** [list of files changed]
- **Commit:** [Will add after commit below]
- **Notes:** [Implementation decisions]
```

### 8. Commit
```bash
git add .
git commit -m "feat(scope): implement subtask N - description

- Key change 1
- Key change 2

Relates to #[issue-number]"
```

### 9. Update `.plan/` with Commit Hash
```bash
# Get hash
git log -1 --pretty=format:"%H"

# Add to .plan/ file, then commit this small update
```

### 10. Done
Hand off to [swe-reviewer](../swe-reviewer/SKILL.md)

## Key Rules
- ✅ **One subtask only** per call
- ✅ **Dedicated branch** - keep independent
- ✅ **context7 mandatory** - query before coding
- ✅ **Tests required** - if specified, no exceptions
- ✅ **All checks must pass** - lint + tests before commit

## Blockers

**Dependency not met:**
- Alert orchestrator: "Cannot start - Subtask X not complete"

**Tests won't pass (>3 attempts):**
- Update `.plan/`: Status = 🛑 Blocked
- Post Blocker Report to issue
- Alert USER immediately

**Unclear scope:**
- Ask orchestrator for clarification

## Specialized Skills
- [vcs-branch](../vcs-branch/SKILL.md)
- [vcs-commit](../vcs-commit/SKILL.md)
- [backend-coder](../backend-coder/SKILL.md)
- **context7 MCP**
- [vcs-issue-management](../vcs-issue-management/SKILL.md)
