---
name: swe-reviewer
description: "Called per-subtask by swe-orchestrator. Reviews ONE completed subtask and creates a per-subtask MR."
---

# 🧐 SWE Reviewer

**Called By:** [swe-orchestrator](../swe-orchestrator/SKILL.md) → per subtask  
**Input:** Subtask branch, commit hash, `.plan/` file  
**Output:** Code reviewed, MR created, `.plan/` updated + issue comment, ready for merge

## Quick Start

1. **Switch to subtask branch**: `git checkout feature/[issue]-[subtask-name]`
2. **Review 6 quality checks** (see below)
3. **Create MR**: Per-subtask, focused on THIS subtask only
4. **Update `.plan/`**: Add MR link
5. **Post to issue**: Use template + show progress
6. **MITM**: Get USER approval
7. **Done**: Hand off to orchestrator

## Quality Gate (Must Pass All)

### 1. Architectural Consistency
- Changes align with design from swe-architect?
- Patterns and practices followed?
- Components organized correctly?

### 2. Code Quality (vs. [backend-coder](../backend-coder/SKILL.md))
- [ ] SOLID principles applied
- [ ] Error handling present
- [ ] Type safety (if applicable)
- [ ] No code smells
- [ ] Naming conventions consistent
- [ ] Complex logic documented

### 3. Testing Coverage
- [ ] All specified tests implemented
- [ ] Unit tests: happy path + edge cases
- [ ] Integration tests (if specified)
- [ ] No skipped/TODO tests
- [ ] Test names descriptive

### 4. Run Quality Checks
```bash
npm run lint   # 0 errors? ✅
npm run test   # All pass? ✅
npm run build  # Success? ✅
```

### 5. Files Modified
- [ ] ONLY THIS subtask's files changed
- [ ] No accidental edits elsewhere
- [ ] No debug code (console.logs, debugger)
- [ ] No commented-out code
- [ ] `.plan/` file updated

### 6. Branch Status
- [ ] Based on current main
- [ ] No merge conflicts
- [ ] Synced with origin

**IF any check fails:**
1. Document issue clearly
2. Return to implementer: "Need fix for [issue]"
3. Implementer commits fix to same branch
4. Re-review (restart Step 1)

**Do NOT create MR until all checks pass** ✅

## Create MR

Use [vcs-change-request](../vcs-change-request/SKILL.md):

**Title:**
```
feat([scope]): [subtask name] - Subtask N/Y
```

**Description template:**
```markdown
## Summary
[1-2 sentence summary of THIS subtask only]

Relates to #[issue-number]

## Changes
- [What was implemented]
- [Key components changed]
- [Edge cases handled]

## Testing
- ✅ Unit tests: X/X passing
- ✅ Integration tests: (if applicable)
- ✅ Linting: 0 errors
- ✅ Build: Success

## Files Changed
- `src/path/file1.ts` - [What changed]
- `test/path/file1.test.ts` - [Tests added]

## Focus Areas
[What reviewers should check carefully]
```

**Parameters:**
- Source: `feature/[issue]-[subtask-name]`
- Target: `main`
- Link issue: #[issue-number]
- Labels: feature/bugfix/etc

## Update `.plan/` with MR Link

```markdown
### Subtask N: [Name]
- **Status:** ✅ Completed
- **MR/PR:** [#456](link-to-mr)
- **Branch:** `feature/123-subtask-name`
```

Commit:
```bash
git add .plan/[issue-number]-[feature-name].md
git commit -m "docs: add MR link for subtask N"
git push
```

## Post to Issue

Draft **⚙️ Subtask Progress Update** comment:

```markdown
### ⚙️ Subtask Complete: [Name] (N/Y)

- **Branch:** `feature/123-subtask-name`
- **MR:** [#456](link)
- **Summary:** [What was implemented]
- **Quality:** ✅ All tests pass, 0 lint errors
- **Progress:** [N/Y] subtasks done ([XX]%)

---
> Ready for human review and merge
```

## MITM - Get Approval

**STOP and present to USER:**
> "Subtask [Name] reviewed and MR #456 created. All tests pass, code quality good. Ready to post to issue?"

**Feedback:**
- USER requests MR changes → Update description → Show again
- USER approves → Post to issue

## Done

Hand off to [swe-orchestrator](../swe-orchestrator/SKILL.md) for next steps.

## Key Rules

- ✅ **One subtask, one MR** - No bundling
- ✅ **Quality gate mandatory** - All checks must pass
- ✅ **Focused review** - THIS subtask only
- ✅ **MITM required** - Get USER approval before posting

## Blockers & Recovery

**Critical issue found:**
- Return to implementer: "Need fix for [specific issue]"
- Implementer commits fix to same branch
- Re-review

**Merge conflicts:**
- Alert orchestrator
- Rebase or merge main into feature
- Push and re-review

## Specialized Skills Used

- [**vcs-branch**](../vcs-branch/SKILL.md) - Branch sync
- [**vcs-change-request**](../vcs-change-request/SKILL.md) - Create MR
- [**vcs-issue-management**](../vcs-issue-management/SKILL.md) - Post to issue
- [**backend-coder**](../backend-coder/SKILL.md) - Code quality standards
