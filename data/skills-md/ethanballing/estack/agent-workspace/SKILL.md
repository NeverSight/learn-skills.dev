---
name: agent-workspace
description: Familiarize with, initialize, audit, migrate, validate, or explicitly clean up a project's agent workspace. Use for read-only working understanding and readiness, AGENTS.md routers, organizing .agents resources, or whole-directory restructuring with knowledge preservation. Familiarize, audit and validate are read-only; mutation requires a selected scope.
---

# Agent workspace

1. **Resolve scope.** Identify the target and operation from the request. Resolve actual paths, ancestors, governing instructions and privacy/export rules. Inspect owners, hidden resources, symlinks, nested repositories and Git state as relevant to that operation; never change the Git index. Git is optional; never initialize it. A bare invocation with unclear intent authorizes inspection, not destructive work.
2. **Retrieve relevant owners.** Follow the selected mode's references and local prerequisites. Familiarize retrieves working context without a structural audit. Use [layout](references/layout.md) for structural assessment. For audit/migration, assess the whole selected directory, including legacy containers and mixed artifacts, by purpose and audience under [migration safeguards](references/migration.md): every candidate group needs a disposition or explicit boundary/unresolved choice, beyond the edited-file list. Preserve domain instructions.
3. **Perform the selected mode.** Use the table below. Explicit mutating requests authorize routine scoped edits, moves, and removal with recovery; ask only about consequential unresolved choices. Before substantial changes, read the [migration safeguards](references/migration.md). For meaningful setup uncertainty, consult an available `grill-with-docs` or `grilling` skill selectively. If unavailable, ask the smallest useful question about purpose, boundaries, or ownership directly. Clear requests need no interview.
4. **Verify, close out and report.** Familiarize uses its [readiness procedure](references/familiarize.md#verify-and-report-readiness); other modes follow [validation](references/validation.md). Mutating operations finish [temporary-artifact closeout](references/migration.md#temporary-migration-artifacts) after validation. Report actual reads/findings or changes, checks, unresolved limits and any justified recovery retention. An already suitable workspace may require no writes.

| Mode | Procedure |
| --- | --- |
| Familiarize | Follow [familiarization](references/familiarize.md) read-only: understand the selected workspace, report readiness and gaps, and leave records/backlog unchanged. |
| Initialize | Follow [safe initialization](references/initialize.md) and [layout](references/layout.md); create only justified missing resources and preserve existing roles/content. |
| Audit | Evaluate instructions, knowledge, ownership, duplication, stale claims, navigation, scope, loading cost, and compatibility using [validation](references/validation.md). Leave target content unchanged. |
| Migrate | Read and follow [migration](references/migration.md) before writes. Restructure agent records and artifacts by purpose; consolidate knowledge, preserve meaning, and repair dependencies and discovery routes. |
| Validate | Apply [validation](references/validation.md) read-only; separate errors, heuristic warnings, and semantic review. |
| Cleanup | Only when explicitly requested, consolidate superseded operational records using the full [migration](references/migration.md) safeguards. Age alone never justifies deletion. |

Keep actual source/product code, human documentation, and user deliverables in appropriate conventional locations; classify internal working code by purpose. Workspace organization is not authorization to execute backlogs, modify unrelated code/infrastructure, install skills/tools, or manage sessions. Never automatically stage, commit, push, change tracking/ignore rules, remotes, or global settings. Never modify existing skill installations as a workspace operation.
