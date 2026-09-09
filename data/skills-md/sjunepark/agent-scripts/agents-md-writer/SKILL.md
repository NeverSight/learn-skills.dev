---
name: agents-md-writer
description: "Design or audit AGENTS.md and tool-specific instruction hierarchies for nested scope, conflicts, legacy or cross-tool migration, bloat, discovery, or precedence failures."
---

# AGENTS.md Writer

Treat agent instructions as a hierarchy of durable, scoped guidance rather than
as general project documentation.

## Workflow

1. Define the operation and target tools.
   - Identify the requested mode: design, audit, restructure, migration, or discovery debugging.
   - Identify every target tool and the instruction surfaces it recognizes.
   - When behavior depends on supported filenames, discovery, precedence, overrides, size limits, or reload timing, consult current official tool documentation before deciding. For Codex, start with the [official AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md/).
   - Finish with an explicit list of target tools, instruction surfaces, and questions the work must resolve.

2. Inventory the effective hierarchy.
   - List global, repository-root, nested, and tool-specific instruction sources in scope, including legacy files during migrations.
   - Record which tool loads each source, its scope, its load order, and any duplicate or conflicting guidance.
   - Continue until every candidate instruction source for each target tool is accounted for.

3. Ground proposed guidance in repository evidence.
   - Inspect the relevant package scripts, CI workflows, formatter and linter configuration, test commands, and authoritative project docs.
   - Trace every proposed rule to a non-obvious repository fact, recurring failure or review comment, hard constraint, or explicit team decision.
   - Prefer code structure, types, schemas, linters, tests, or hooks when they can enforce the behavior directly.
   - Finish with evidence and an intended scope for every proposed addition.

4. Design placement deliberately.
   - Keep shared guidance at the broadest intended scope within the authorized target. Reserve user-global files for explicitly personal or global guidance.
   - Where a target tool supports nesting, place subtree-specific guidance at the closest scope that needs it.
   - Edit the closest suitable existing file. Create a new file only when guidance is missing for a scope or precedence must change.
   - Keep cross-tool guidance in a common file only when every target tool reads it; otherwise use each tool's recognized surface.
   - For Codex, use `AGENTS.override.md` only when replacing the same directory's `AGENTS.md` is intentional. Verify other tools' override behavior independently.
   - Resolve each duplicate or conflict to one authoritative location whenever tool support allows it.

5. Make the smallest useful edit.
   - Write imperative rules with exact commands and paths.
   - Link to authoritative README or architecture docs instead of repeating explanatory detail; retain concise routing, invariants, and execution-critical context.
   - State hard safety and approval boundaries explicitly; phrase ordinary guidance as the desired behavior.
   - Keep the diff limited to the intended scopes, with every added line justified by the evidence collected above.

6. Verify the effective result.
   - Re-read the combined instruction chain in each target tool's documented load order and check for contradictions or stale commands.
   - When hierarchy or discovery changed, inspect active instruction sources from the repository root and a representative nested directory using each tool's supported introspection or dry-run path.
   - Report any tool behavior that could not be verified instead of presenting it as fact.
   - Finish only when each target tool's active files, precedence, and resulting guidance are verified or explicitly reported as unverified for every changed scope.
