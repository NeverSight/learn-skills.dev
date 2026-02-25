---
name: swe-orchestrator
description: "Orchestrates complete SDLC: Architect → Planner → Implementer (per-subtask) → Reviewer (per-subtask). Single entry point for complete feature development."
---

# 🎼 SWE Orchestrator

**Called By:** Issue author or team lead  
**Input:** GitHub issue with requirements  
**Output:** Merged feature branch, closed issue  
**Duration:** Full feature lifecycle (hours to days)

---

## Quick Start

**This skill orchestrates a COMPLETE feature end-to-end using 4 phases:**

```
Phase 1: swe-architect    → Analyze + diagram architecture
Phase 2: swe-planner      → Break into subtasks + create .plan/ file
Phase 3: swe-implementer  → Loop: implement each subtask (separate branch)
Phase 4: swe-reviewer     → Loop: review each subtask + create MR
Phase 5: Merge & Close    → Merge all MRs + close issue
```

**Source of Truth:** GitHub issue (requirements + approvals) + `.plan/` file in repo (persistent state)

---

## Full Flow

### Phase 1: Architecture Analysis
1. Read issue requirements
2. Call [swe-architect](../swe-architect/SKILL.md) → creates technical analysis + Mermaid diagram
3. **MITM**: Present to USER → Get approval
4. Post approved analysis to issue comment

### Phase 2: Planning & Breakdown
1. Call [swe-planner](../swe-planner/SKILL.md) with approved architecture
2. Planner breaks into 3-8 subtasks and creates `.plan/[issue]-[name].md`
3. **MITM**: Present plan to USER → Get approval  
4. Post approved plan to issue

### Phase 3-4: Per-Subtask Loop (Repeat for each subtask)
1. **Implement**: Call [swe-implementer](../swe-implementer/SKILL.md)
   - Creates feature branch: `feature/[issue]-[subtask-name]`
   - Implements subtask locally
   - Commits with message: `feat([scope]): [description]`
2. **Review**: Call [swe-reviewer](../swe-reviewer/SKILL.md)
   - Reviews quality gates (tests, code, coverage)
   - Creates per-subtask MR
   - Updates `.plan/` with MR link
3. **MITM**: Present to USER → "MR #[N] ready for review?"
4. Update `.plan/` with completion status and MR link
5. Post subtask progress comment to issue

### Phase 5: Merge & Completion
1. Human reviewers approve and merge MRs
2. Detect all MRs merged in `.plan/` file
3. Post final completion comment to issue
4. Close issue (status: 🎉 Complete)

---

## Master Progress Checklist

```markdown
- [ ] Phase 1: Architecture finalized
- [ ] Phase 2: Plan + .plan/ file created  
- [ ] Phase 3-4: All X subtasks done (Subtask 1, 2, 3...)
- [ ] Phase 5: All MRs merged, issue closed
```

---

## Critical Rules

✅ **Issue = Single Source of Truth** - All approvals, decisions, blocker alerts post to issue

✅ **`.plan/` file tracks state** - Persistent progress file updated after each phase

✅ **.plan/ file location** - `.plan/[issue-number]-[feature-name].md`

✅ **One subtask = One branch = One MR** - No bundling

✅ **Architecture first** - No implementation starts without architect approval

✅ **Quality gates mandatory** - swe-reviewer MUST verify all checks pass before MR

✅ **context7 mandatory** - swe-implementer queries context7 before coding

✅ **MITM at phase gates** - Present to USER before proceeding to next phase

✅ **Conventional commits** - All commits follow `type(scope): message` format

---

## Exception Handling

**IF blocked:** 
- Update `.plan/` with status = 🛑 BLOCKED
- Post blocker report to issue
- Alert USER

**IF merge conflict:**
- Re-run swe-implementer to rebase
- Re-run swe-reviewer to validate
- Post resolution to issue

**IF scope changes mid-project:**
- Return to Phase 1 (re-architect)
- Update Phase 2 plan
- Continue with Phase 3-4 as needed
- Post scope change to issue

**IF quality gate fails:**
- swe-reviewer documents issue
- swe-implementer addresses
- swe-reviewer re-reviews
- Loop until all checks pass

---

## Specialized Skills Orchestrated

**Core 4-phase skills:**
- [**swe-architect**](../swe-architect/SKILL.md) - Phase 1: Architecture analysis
- [**swe-planner**](../swe-planner/SKILL.md) - Phase 2: Decompose into subtasks
- [**swe-implementer**](../swe-implementer/SKILL.md) - Phase 3: Implement per-subtask
- [**swe-reviewer**](../swe-reviewer/SKILL.md) - Phase 4: Review + create MR

**Supporting skills:**
- [**vcs-issue-management**](../vcs-issue-management/SKILL.md) - Issue comments + templates
- [**vcs-branch**](../vcs-branch/SKILL.md) - Branch creation + sync
- [**vcs-commit**](../vcs-commit/SKILL.md) - Conventional commits
- [**vcs-change-request**](../vcs-change-request/SKILL.md) - MR/PR creation
- **context7 MCP** - Query for documentation + context
- [**mermaid-diagrams**](../mermaid-diagrams/SKILL.md) - Architecture diagrams
- [**backend-coder**](../backend-coder/SKILL.md) - Code quality standards

---

## When to Use This Skill

**Use orchestrator when:**
- Starting a new GitHub issue that requires implementation
- Issue is ready with clear requirements
- Need full end-to-end feature delivery (architecture → code → review → merge)
- Team wants coordinated, auditable workflow

**DO NOT use orchestrator when:**
- Just reviewing an existing MR (use swe-pr-reviewer instead)
- Quick bug fix requiring no planning (use swe-implementer + swe-reviewer directly)
- Only architectural analysis needed (use swe-architect alone)
