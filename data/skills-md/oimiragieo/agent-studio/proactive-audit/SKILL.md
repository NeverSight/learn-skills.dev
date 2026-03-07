---
name: proactive-audit
description: >-
  Automated health checks for framework artifacts modified during a pipeline.
  Validates hook syntax, security patterns (SE-01/SE-02), skill wiring, agent
  consistency, and routing correctness. Invoked as the final pipeline step
  when framework artifacts were created, modified, or deleted.
version: 1.2.0
model: sonnet
category: validation
invoked_by: both
user_invocable: true
tools: [Read, Bash, Glob, Grep]
agents:
  - qa
  - developer
  - architect
best_practices:
  - Run all applicable checks from the check matrix
  - Use git diff as primary change detection method
  - Never skip SE-02 or SE-01 scans on hook/tool files
  - Report findings with severity and remediation steps
error_handling: strict
streaming: supported
verified: true
lastVerifiedAt: 2026-02-23T00:00:00.000Z
---

# Proactive Audit

## Overview

Automated health checks for framework artifacts that were modified during the current pipeline. This skill fills the gap between reactive verification (tests, lint) and proactive framework-level validation (wiring, syntax, security patterns).

**Core principle:** Framework artifact changes require the same rigor as code changes. If a skill was created, verify it is wired. If a hook was modified, verify it compiles. If an agent was changed, verify its tool/skill lists are consistent.

## When to Invoke

Invoke this skill as the **final pipeline step** whenever ANY of the following paths were created, modified, or deleted during the session:

- `.claude/hooks/**/*.cjs`
- `.claude/skills/**/SKILL.md`
- `.claude/agents/**/*.md`
- `.claude/workflows/**/*.md`
- `.claude/schemas/**/*.json`
- `.claude/templates/**/*`
- `.claude/CLAUDE.md`
- `.claude/lib/routing/routing-table.cjs`

**Invocation:**

```javascript
Skill({ skill: 'proactive-audit' });
```

## Mandatory Skills

| Skill                             | Purpose                            | When                 |
| --------------------------------- | ---------------------------------- | -------------------- |
| `task-management-protocol`        | Track audit progress               | Always               |
| `ripgrep`                         | Fast targeted artifact search      | During checks        |
| `code-semantic-search`            | Pattern discovery across artifacts | When investigating   |
| `token-saver-context-compression` | Compress large audit results       | When output is large |
| `verification-before-completion`  | Gate completion on zero CRITICAL   | Before marking done  |
| `memory-search`                   | Check prior audit patterns         | At start             |

## Step 1: Detect Changed Artifacts

Use git diff to identify which framework artifacts changed in this session:

```bash
# Primary: git diff against recent commits
git diff --name-only HEAD~5 -- .claude/hooks/ .claude/skills/ .claude/agents/ .claude/workflows/ .claude/schemas/ .claude/templates/ .claude/CLAUDE.md .claude/lib/routing/

# Secondary: check unstaged changes
git diff --name-only -- .claude/hooks/ .claude/skills/ .claude/agents/ .claude/workflows/ .claude/schemas/ .claude/templates/

# Tertiary: check untracked files
git ls-files --others --exclude-standard .claude/hooks/ .claude/skills/ .claude/agents/ .claude/workflows/ .claude/schemas/ .claude/templates/
```

Combine all three lists into a deduplicated set of changed artifact paths.

## Step 2: Apply Check Matrix

For each changed artifact, apply the relevant checks from this matrix:

### Hook Files (`.claude/hooks/**/*.cjs`)

| Check ID | Check                                       | Command                                                         | Severity |
| -------- | ------------------------------------------- | --------------------------------------------------------------- | -------- |
| H-01     | Syntax validity                             | `node --check <file>`                                           | CRITICAL |
| H-02     | SE-02: raw JSON.parse without safeParseJSON | `grep -n "JSON.parse(" <file>` then verify safeParseJSON import | HIGH     |
| H-03     | SE-01: shell injection via shell: true      | `grep -n "shell:\\s*true" <file>`                               | HIGH     |
| H-04     | Hook registered in settings.json            | `grep "<hook-filename>" .claude/settings.json`                  | MEDIUM   |
| H-05     | Exit code correctness                       | Verify try/catch wrapping, exit 0 on non-critical errors        | MEDIUM   |

**H-02 detail:** If `JSON.parse(` is found, check if the file also imports `safeParseJSON` from `.claude/lib/utils/safe-json.cjs`. If not, flag as HIGH finding. Exclude test files (`*.test.cjs`).

### Skill Files (`.claude/skills/**/SKILL.md`)

| Check ID | Check                                       | Command                                                   | Severity |
| -------- | ------------------------------------------- | --------------------------------------------------------- | -------- |
| S-01     | Skill appears in skill-catalog.md           | `grep "<skill-name>" .claude/docs/skill-catalog.md`       | HIGH     |
| S-02     | At least one agent has skill in frontmatter | `grep -r "<skill-name>" .claude/agents/ --include="*.md"` | MEDIUM   |
| S-03     | Skill appears in CLAUDE.md Section 8.5      | `grep "<skill-name>" .claude/CLAUDE.md`                   | MEDIUM   |
| S-04     | SKILL.md has valid frontmatter              | Verify `name:`, `description:`, `version:` fields exist   | MEDIUM   |
| S-05     | Validate skills (if available)              | `pnpm validate:skills 2>&1`                               | LOW      |

### Agent Files (`.claude/agents/**/*.md`)

| Check ID | Check                                           | Command                                                                        | Severity |
| -------- | ----------------------------------------------- | ------------------------------------------------------------------------------ | -------- |
| A-01     | Agent appears in agent-registry.json            | `grep "<agent-name>" .claude/context/agent-registry.json`                      | HIGH     |
| A-02     | Agent's skills: list references existing skills | For each skill in frontmatter, verify `.claude/skills/<skill>/SKILL.md` exists | MEDIUM   |
| A-03     | Agent's tools: list contains only valid tools   | Verify each tool name against known tool list                                  | MEDIUM   |
| A-04     | Agent appears in CLAUDE.md routing table        | `grep "<agent-name>" .claude/CLAUDE.md`                                        | MEDIUM   |

### Workflow Files (`.claude/workflows/**/*.md`)

| Check ID | Check                                        | Command                                                      | Severity |
| -------- | -------------------------------------------- | ------------------------------------------------------------ | -------- |
| W-01     | Workflow referenced in WORKFLOW_AGENT_MAP.md | `grep "<workflow-name>" .claude/docs/@WORKFLOW_AGENT_MAP.md` | MEDIUM   |
| W-02     | Referenced agents exist                      | For each agent name in workflow, verify agent file exists    | MEDIUM   |

### Schema Files (`.claude/schemas/**/*.json`)

| Check ID | Check                               | Command                                                                     | Severity |
| -------- | ----------------------------------- | --------------------------------------------------------------------------- | -------- |
| SC-01    | Valid JSON syntax                   | `node -e "JSON.parse(require('fs').readFileSync('<file>', 'utf8'))"`        | CRITICAL |
| SC-02    | Schema appears in schema-catalog.md | `grep "<schema-name>" .claude/context/artifacts/catalogs/schema-catalog.md` | MEDIUM   |

### Routing Files (`.claude/lib/routing/routing-table.cjs`, `.claude/CLAUDE.md`)

| Check ID | Check                    | Command                                              | Severity |
| -------- | ------------------------ | ---------------------------------------------------- | -------- |
| R-01     | routing-table.cjs syntax | `node --check .claude/lib/routing/routing-table.cjs` | CRITICAL |
| R-02     | Validate skills (full)   | `pnpm validate:skills 2>&1`                          | MEDIUM   |

## Step 3: Generate Report

Write a structured report to `.claude/context/reports/ecosystem-audit/proactive-audit-{ISO-date}.md` with this format:

```markdown
<!-- Agent: qa | Task: #N | Session: YYYY-MM-DD -->

# Proactive Audit Report

**Date:** YYYY-MM-DD
**Artifacts Scanned:** N
**Findings:** N CRITICAL, N HIGH, N MEDIUM, N LOW
**Overall:** PASS | FAIL

## Changed Artifacts

- path/to/artifact1 (type: hook)
- path/to/artifact2 (type: skill)

## Findings

### CRITICAL

| ID   | File          | Check  | Detail                 | Remediation      |
| ---- | ------------- | ------ | ---------------------- | ---------------- |
| H-01 | hooks/foo.cjs | Syntax | SyntaxError at line 42 | Fix syntax error |

### HIGH

| ID   | File          | Check | Detail                                      | Remediation                                               |
| ---- | ------------- | ----- | ------------------------------------------- | --------------------------------------------------------- |
| H-02 | hooks/bar.cjs | SE-02 | JSON.parse at line 15 without safeParseJSON | Import safeParseJSON from .claude/lib/utils/safe-json.cjs |

### MEDIUM

(same table format)

### PASS

| ID   | File          | Check  | Result |
| ---- | ------------- | ------ | ------ |
| H-01 | hooks/baz.cjs | Syntax | OK     |

## Summary

- Total checks run: N
- Passed: N
- Failed: N
- Pass rate: N%
```

## Step 4: Return Verdict

After generating the report:

- If ANY CRITICAL findings exist: return `FAIL` with the report path and list of critical findings
- If ANY HIGH findings exist: return `WARN` with the report path and list of high findings
- If only MEDIUM/LOW findings: return `PASS` with the report path and note about medium findings
- If no findings: return `PASS` with the report path

## Iron Laws

1. **ALWAYS** run every applicable check from the check matrix — skipping "small" changes is how undetected wiring failures accumulate across sessions.
2. **NEVER** trust task metadata alone for change detection — use `git diff` as the primary source of changed artifact paths.
3. **NEVER** report PASS without actually executing each check command — self-attested PASS without evidence violates verification-before-completion.
4. **NEVER** ignore SE-02 (prototype pollution) findings in hook files — a single compromised hook can corrupt all subsequent tool calls in the pipeline.
5. **ALWAYS** validate hook syntax with `node --check` before reporting findings — broken hooks silently block the entire tool pipeline.

## Anti-Patterns

| Anti-Pattern                                  | Why It Fails                                                                 | Correct Approach                                                        |
| --------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Skipping checks for "small" changes           | Small wiring failures accumulate silently until a pipeline breaks            | Run all checks regardless of perceived change size                      |
| Trusting task metadata for change detection   | Metadata can be incomplete or stale; misses unstaged changes                 | Use `git diff --name-only` + `git ls-files --others` as primary source  |
| Self-attesting PASS without running commands  | Unverified PASS masks real failures; violates verification-before-completion | Execute every check command and capture output as evidence              |
| Ignoring SE-02 (prototype pollution) in hooks | One polluted hook corrupts `Object.prototype` globally across all tool calls | Flag SE-02 as HIGH severity and block pipeline until fixed              |
| Reporting findings without remediation steps  | Developers know what broke but not how to fix it                             | Include specific remediation for every finding with file+line reference |

## Severity Guide

| Severity | Meaning                                | Action Required                            |
| -------- | -------------------------------------- | ------------------------------------------ |
| CRITICAL | Framework will break                   | Fix immediately, block pipeline completion |
| HIGH     | Security risk or invisible artifact    | Fix before next session, warn user         |
| MEDIUM   | Missing integration, incomplete wiring | Fix in follow-up task                      |
| LOW      | Best practice violation, cosmetic      | Track for future improvement               |

## Integration with Router Step 0.7

The router invokes this skill via Step 0.7 in the Router Output Contract (CLAUDE.md Section 0.1). The router:

1. Detects that framework artifacts were modified during the pipeline
2. Spawns a QA agent with this skill as the final pipeline step
3. Reads the audit report
4. If CRITICAL findings: spawns developer to fix them before claiming completion
5. If HIGH findings: warns user and notes findings in pipeline summary
6. If PASS: proceeds to claim pipeline completion

## Related Skills

- `verification-before-completion` -- General evidence-based completion gates
- `checklist-generator` -- IEEE 1028 quality checklists
- `sharp-edges` -- Known hazard patterns (SE-01 through SE-07)

## Related References

- `.claude/context/plans/proactive-audit-design-2026-02-22.md` -- Design document
- `.claude/rules/security.md` -- SE-01 and SE-02 patterns
- `.claude/rules/artifact-integration.md` -- Must-have integration requirements
