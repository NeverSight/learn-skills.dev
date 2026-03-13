---
name: migration-and-doc-consolidation
description: Execute end-to-end migrations and consolidate docs/scripts (remove dead files, keep canonical runbooks). Use when changing runtime model, reorganizing repo, or doing “repo cleanup”.
compatibility: Requires repo write access and ability to run build/tests.
allowed-tools: Bash(*) Read FileSearch(*)
metadata:
  intent: Avoid when user only wants advice; run only for actual repo changes.
---

# migration-and-doc-consolidation

## Activation gate
Use if:
- Migration (tech/runtime), repo restructuring, “porządkowanie”, doc consolidation, script maintenance.

## Procedure
1. Inventory:
   - entrypoints, scripts, docs, CI workflows.
2. Identify canonical run path:
   - one “golden” command set.
3. Remove/flag dead scripts (with grep references).
4. Update docs to point to canonical paths.
5. Validate: build/test/lint where available.

## Output
- Summary of changes + new canonical runbook + verification commands.
