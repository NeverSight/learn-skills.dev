---
name: sonarqube-new-code-warning-fixer
description: >
  Analyze newly updated code with SonarQube MCP, list warnings,
  fix all warnings, and fix broken tests. Use when asked to scan changed
  files from uncommitted work or branch diffs against
  develop/master/main, then remediate issues end-to-end.
---

# SonarQube New Code Warning Fixer

## Overview

Use SonarQube MCP to inspect only newly updated code, report warnings
in a clear list, fix them, and finish with passing tests.
Scope selection supports uncommitted changes and branch diffs.

## Workflow

1. Determine update scope.
Run:
```bash
python3 scripts/list_newly_updated_files.py --mode auto --only code
```
- `auto`: use uncommitted changes when present; otherwise use branch diff.
- branch diff base: prefer `develop`, then `master`, then `main`.
- if no changed code files are found, report no warnings and stop.

2. Resolve SonarQube project key.
- infer from repo name first.
- call `mcp__sonarqube__search_my_sonarqube_projects`.
- if multiple close matches exist, choose exact key match when available.

3. Convert changed files to Sonar component keys.
Run:
```bash
python3 scripts/list_newly_updated_files.py --mode auto --only code --project-key "<project-key>"
```
- use `sonar_components.prod` and `sonar_components.test`.
- query production and test components separately to avoid Sonar qualifier errors.

4. Collect warnings on changed files with SonarQube MCP.
- primary issues: `mcp__sonarqube__search_sonar_issues_in_projects`
  - set `projects=[projectKey]`
  - set `issueStatuses=["OPEN","CONFIRMED"]`
  - batch components to keep requests small (around 25 to 50 files per call).
- security warnings: `mcp__sonarqube__search_security_hotspots`
  - set `projectKey`
  - pass the same file batch (path list, not component keys).
  - include unresolved statuses only.

5. Show warning list before fixing.
- sort by severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`.
- include: issue key, severity, rule, file, line, message.
- explicitly state `Warnings found: 0` when empty.

6. Fix all warnings in changed files.
- fix highest severity first.
- preserve behavior unless warning explicitly points to a bug.
- avoid widening scope beyond changed files except for necessary shared utilities.
- after edits, re-query Sonar for the same changed-file scope.

7. Fix broken tests and validate.
- run focused tests for touched modules first, then broader suite if needed.
- if the repo has no reliable targeted mapping, run project default test command.
- report remaining failures with exact test name and error.
- continue until warnings on changed files are resolved and tests pass, or clearly report blockers.

## Output Format

Use this order:
1. Scope summary.
2. Warning list.
3. Fixes applied.
4. Test results.
5. Residual blockers (if any).

## Resources

- changed-file scope helper: `scripts/list_newly_updated_files.py`
- Sonar query patterns and caveats: `references/sonarqube-mcp-patterns.md`

## Sharing

Install this skill from a skills repository:

```bash
npx skills add <repo-url-or-path> --skill sonarqube-new-code-warning-fixer
```

## Guardrails

- keep analysis scoped to newly updated code unless user asks for full-project scan.
- never hide unresolved warnings: list them explicitly.
- do not claim tests passed unless tests were actually run in this environment.
- if Sonar returns no results but warnings are expected,
  verify project key, file key format, and qualifier grouping
  before concluding.
