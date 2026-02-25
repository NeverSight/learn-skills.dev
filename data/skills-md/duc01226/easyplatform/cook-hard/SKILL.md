---
name: cook-hard
description: '[Implementation] ⚡⚡⚡⚡ Thorough implementation with maximum verification'
argument-hint: [tasks]
---

**Ultrathink** to plan and implement these tasks with maximum verification:
<tasks>$ARGUMENTS</tasks>

**Mode:** HARD - Extra research, detailed planning, mandatory reviews.

## ⚠️ MUST READ Before Starting

**IMPORTANT: You MUST read these shared protocols before any code changes. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — Assumption validation, evidence chains, context anchoring
- **⚠️ MUST READ** `.claude/skills/shared/knowledge-graph-template.md` — Per-file analysis structure (for investigation phases)

**Core Rule:** Verify every assumption with actual code evidence before making changes. Search for all usages, read implementations, trace dependencies. If confidence < 90%, investigate further or ask user.

## Workflow

### 1. Deep Research Phase

- Launch 2-3 `researcher` subagents in parallel covering:
    - Technical approach validation
    - Edge cases and failure modes
    - Security implications
    - Performance considerations
- Use `/scout-ext` for comprehensive codebase analysis
- Generate research reports (max 150 lines each)

### 2. Comprehensive Planning

- Use `planner` subagent with all research reports
- Create full plan directory with:
    - `plan.md` - Overview with risk assessment
    - `phase-XX-*.md` - Detailed phase files
    - Success criteria for each phase
    - Rollback strategy

### 3. Verified Implementation

- Implement one phase at a time
- After each phase:
    - Run type-check and compile
    - Run relevant tests
    - Self-review before proceeding

### 4. Mandatory Testing

- Use `tester` subagent for full test coverage
- Write tests for:
    - Happy path scenarios
    - Edge cases from research
    - Error handling paths
- NO mocks or fake data allowed
- Repeat until all tests pass

### 5. Mandatory Code Review

- Use `code-reviewer` subagent
- Address all critical and major findings
- Re-run tests after fixes
- Repeat until approved

### 6. Documentation Update

- Use `docs-manager` to update relevant docs
- Use `project-manager` to update project status
- Record any architectural decisions

### 7. Final Report

- Summary of all changes
- Test coverage metrics
- Security considerations addressed
- Unresolved questions (if any)
- Ask user to review and approve

## When to Use

- Critical production features
- Security-sensitive changes
- Public API modifications
- Database schema changes
- Cross-service integrations

## Quality Gates

| Gate     | Criteria                  |
| -------- | ------------------------- |
| Research | 2+ researcher reports     |
| Planning | Full plan directory       |
| Tests    | All pass, no mocks        |
| Review   | 0 critical/major findings |
| Docs     | Updated if needed         |

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
