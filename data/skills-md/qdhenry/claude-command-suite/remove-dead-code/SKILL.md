---
name: remove-dead-code
description: Safely identifies and removes dead code in TypeScript/JavaScript projects using multi-agent analysis with automatic backup branches. Use when cleaning up unused exports, orphaned files, dead imports, unreachable functions, or unused dependencies.
---

<essential_principles>

**Safety-first dead code removal.** Every removal is protected by an automatic backup branch. Multi-agent analysis reduces false positives. No code is deleted without cross-validation.

**1. Backup Before Everything**

Before any modification, create a timestamped backup branch from the current HEAD. This is non-negotiable. The branch name format is `backup/dead-code-removal/{timestamp}`.

**2. Parallel Scout + Validator Pattern**

Multiple scout agents analyze different aspects of dead code in parallel. A validator agent then cross-checks all findings against the full codebase before anything is flagged for removal. Only code confirmed dead by both scouts AND validator gets removed.

**3. Conservative by Default**

When in doubt, keep the code. False negatives (missing some dead code) are acceptable. False positives (removing live code) are not. Dynamic imports, reflection, test utilities, and public API surface are always treated as potentially live.

**4. Never Remove Without Reporting First**

The scan workflow produces a report. The user reviews the report. Only then does the remove workflow execute against confirmed items.

</essential_principles>

<intake>
What would you like to do?

1. **Scan** - Analyze codebase for dead code (read-only, produces report)
2. **Remove** - Remove confirmed dead code (requires prior scan report)
3. **Validate** - Verify removal didn't break anything (post-removal checks)

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "scan", "analyze", "find", "detect", "report" | `workflows/scan-dead-code.md` |
| 2, "remove", "delete", "clean", "prune" | `workflows/remove-dead-code.md` |
| 3, "validate", "verify", "check", "test" | `workflows/validate-removal.md` |
| Unclear | Ask: "Would you like to scan first (recommended) or do you already have a scan report?" |

**Default flow:** Scan → Review report → Remove → Validate

**After reading the workflow, follow it exactly.**
</routing>

<safety_rules>
- NEVER remove code without creating a backup branch first
- NEVER remove code that appears in test files as a test subject (test helpers ARE candidates)
- NEVER remove re-exported types that could be part of a public API
- NEVER remove files matching patterns: `*.config.*`, `*.setup.*`, `*.d.ts`, entry points
- ALWAYS preserve code referenced by dynamic imports (`import()` expressions)
- ALWAYS preserve code that might be used via string-based lookups or reflection
- ALWAYS check `package.json` `exports`, `main`, `types`, and `bin` fields before removing
- ALWAYS check framework conventions (Next.js pages/routes, Convex functions, etc.)
</safety_rules>

<reference_index>
All domain knowledge in `references/`:

**Detection:** detection-patterns.md - What to scan for and how to identify dead code
**Agents:** agent-coordination.md - How multi-agent parallel analysis works
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| scan-dead-code.md | Multi-agent analysis producing a dead code report |
| remove-dead-code.md | Safe removal with backup branch and atomic commits |
| validate-removal.md | Post-removal build, test, and type-check verification |
</workflows_index>

<success_criteria>
Dead code removal is successful when:
- Backup branch exists with pre-removal state
- All flagged items were cross-validated by multiple agents
- Build passes after removal (`tsc --noEmit`, `npm run build`)
- All tests pass after removal
- No new TypeScript errors introduced
- Removal summary report generated with what was removed and why
</success_criteria>
