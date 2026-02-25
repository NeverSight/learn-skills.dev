---
name: docs-update
description: '[Docs] ⚡⚡⚡ Analyze the codebase and update documentation'
---

## Phase 1: Parallel Codebase Scouting

**You (main agent) must spawn scouts** - subagents cannot spawn subagents.

1. Run `ls -la` to identify actual project directories
2. Spawn 2-4 `scout-external` (preferred, uses Gemini 2M context) or `scout` (fallback) via Task tool
3. Target directories **that actually exist** - adapt to project structure, don't hardcode paths
4. Merge scout results into context summary

## Phase 2: Documentation Update (docs-manager Agent)

Pass the gathered file list to `docs-manager` agent to update documentation:

- `README.md`: Update README (keep it under 300 lines)
- `docs/project-overview-pdr.md`: Update project overview and PDR (Product Development Requirements)
- `docs/codebase-summary.md`: Update codebase summary
- `docs/code-standards.md`: Update codebase structure and code standards
- `docs/system-architecture.md`: Update system architecture
- `docs/project-roadmap.md`: Update project roadmap
- `docs/deployment-guide.md` [optional]: Update deployment guide
- `docs/design-guidelines.md` [optional]: Update design guidelines

## Additional requests

<additional_requests>
$ARGUMENTS
</additional_requests>

## [CRITICAL] Code Evidence Requirements

All documentation MUST follow evidence rules from `.claude/skills/feature-docs/SKILL.md` → `[CRITICAL] MANDATORY CODE EVIDENCE RULE`

### Quick Reference

- **Format**: `**Evidence**: {FilePath}:{LineNumber}`
- **Status**: ✅ Verified / ⚠️ Stale / ❌ Missing
- **Verification**: 3-pass verification required before completion

### Stale Evidence Detection

When updating documentation:

1. **Read actual source files** at claimed line numbers
2. **Verify evidence matches** documented behavior
3. **Update stale references** - mark with ⚠️ if line numbers changed
4. **Refresh line numbers** after code changes

### Evidence Verification Table (Required)

| Entity/Component | Documented Lines | Actual Lines | Status      |
| ---------------- | ---------------- | ------------ | ----------- |
| `Entity.cs`      | L6-15            | L6-15        | ✅ Verified |
| `Handler.cs`     | L45-60           | L52-67       | ⚠️ Stale    |

## Important

- Use `docs/` directory as the source of truth for documentation.

**IMPORTANT**: **Do not** start implementing.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
