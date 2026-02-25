---
name: docs-init
description: '[Docs] ⚡⚡⚡⚡ Analyze the codebase and create initial documentation'
---

## Phase 1: Parallel Codebase Scouting

**You (main agent) must spawn scouts** - subagents cannot spawn subagents.

1. Run `ls -la` to identify actual project directories
2. Spawn 2-4 `scout-external` (preferred, uses Gemini 2M context) or `scout` (fallback) via Task tool
3. Target directories **that actually exist** - adapt to project structure, don't hardcode paths
4. Merge scout results into context summary

## Phase 2: Documentation Creation (docs-manager Agent)

Pass the gathered file list to `docs-manager` agent to create initial documentation:

- `docs/project-overview-pdr.md`: Project overview and PDR (Product Development Requirements)
- `docs/codebase-summary.md`: Codebase summary
- `docs/code-standards.md`: Codebase structure and code standards
- `docs/system-architecture.md`: System architecture
- Update `README.md` with initial documentation (keep it under 300 lines)

Use `docs/` directory as the source of truth for documentation.

## [CRITICAL] Code Evidence Requirements

All documentation MUST follow evidence rules from `.claude/skills/feature-docs/SKILL.md` → `[CRITICAL] MANDATORY CODE EVIDENCE RULE`

### Quick Reference

- **Format**: `**Evidence**: {FilePath}:{LineNumber}`
- **Status**: ✅ Verified / ⚠️ Stale / ❌ Missing
- **Verification**: 3-pass verification required before completion

### Evidence Verification Table (Required)

| Entity/Component | Documented Lines | Actual Lines | Status      |
| ---------------- | ---------------- | ------------ | ----------- |
| `Entity.cs`      | L6-15            | L6-15        | ✅ Verified |

**IMPORTANT**: **Do not** start implementing.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
